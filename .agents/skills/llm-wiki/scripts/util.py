"""Stateless helpers for the wiki pipeline.

There is no `.wiki-state.json`: the Markdown pages under `wiki/` are the only source of truth. The
LLM writes each page directly (see prompts.py); these helpers discover raw files, resolve slugs and
dates, scan the pages to count mentions, and regenerate `index.md` by reading the bundle.
"""

from __future__ import annotations

import datetime as _dt
import os
import re

WIKI_DIR = "wiki"
RAW_DIR = "raw"
SCHEMA_REL = "wiki/SCHEMA.md"

TEXT_EXTS = {".md", ".txt", ".html", ".json", ".csv", ".xml", ".rst", ".yaml"}
RESERVED = {"index.md", "log.md", "SCHEMA.md"}
PAGE_DIRS = ("sources", "entities", "concepts", "relationships", "overviews")

_DATE_PREFIX = re.compile(r"^(\d{4}-\d{2}-\d{2})[-_. ]")
_FM_DATE = re.compile(
    r"^(?:publication_date|published|date|last_modified)\s*[:=]\s*[\"']?(\d{4}-\d{2}-\d{2})",
    re.MULTILINE,
)
_FM_FIELD = lambda key: re.compile(rf"^{key}\s*:\s*[\"']?(.*?)[\"']?\s*$", re.MULTILINE)
_CID = re.compile(r"(?:entities|concepts)/[a-z0-9][a-z0-9-]*")


def now_iso() -> str:
    return _dt.datetime.now(_dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def slugify(text: str) -> str:
    text = re.sub(r"[^a-z0-9]+", "-", text.lower().strip())
    return text.strip("-") or "untitled"


def source_slug(filename: str) -> str:
    """Source id = the raw name minus any date prefix and extension, slugified."""
    stem = os.path.splitext(filename)[0]
    return slugify(_DATE_PREFIX.sub("", stem))


def resolve_date(filename: str, path: str, content: str) -> tuple[str, bool]:
    """(YYYY-MM-DD, had_prefix): file-name prefix, else frontmatter, else mtime."""
    m = _DATE_PREFIX.match(filename)
    if m:
        return m.group(1), True
    fm = _FM_DATE.search(content)
    if fm:
        return fm.group(1), False
    ts = os.path.getmtime(path)
    return _dt.datetime.fromtimestamp(ts, _dt.timezone.utc).strftime("%Y-%m-%d"), False


def list_raw(root: str) -> list[dict]:
    """Flat listing of ingestable raw files, oldest first."""
    raw_dir = os.path.join(root, RAW_DIR)
    out = []
    if not os.path.isdir(raw_dir):
        return out
    for name in sorted(os.listdir(raw_dir)):
        path = os.path.join(raw_dir, name)
        if not os.path.isfile(path) or os.path.splitext(name)[1].lower() not in TEXT_EXTS:
            continue
        with open(path, encoding="utf-8", errors="replace") as fh:
            content = fh.read()
        date, had_prefix = resolve_date(name, path, content)
        out.append({"name": name, "path": path, "date": date, "had_prefix": had_prefix, "slug": source_slug(name), "content": content})
    out.sort(key=lambda r: (r["date"], r["name"]))
    return out


def _read(path: str) -> str:
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def frontmatter_field(text: str, key: str) -> str:
    end = text.find("\n---", 3) if text.startswith("---") else -1
    block = text[:end] if end != -1 else text
    m = _FM_FIELD(key).search(block)
    return m.group(1).strip() if m else ""


def list_pages(wiki: str, kind: str) -> list[str]:
    d = os.path.join(wiki, kind)
    if not os.path.isdir(d):
        return []
    return sorted(f"{kind}/{n[:-3]}" for n in os.listdir(d) if n.endswith(".md") and n not in RESERVED)


def page_exists(wiki: str, cid: str) -> bool:
    return os.path.exists(os.path.join(wiki, f"{cid}.md"))


def _section(text: str, heading: str) -> str:
    """Return the body of a `## heading` section, up to the next `## `."""
    m = re.search(rf"(?ms)^##\s+{re.escape(heading)}\s*\n(.*?)(?=^##\s|\Z)", text)
    return m.group(1) if m else ""


def scan_mentions(wiki: str) -> dict:
    """Count how many source summaries (+ relationships) mention each entity/concept id.

    Returns {cid: {"count": n, "sources": set(), "name": str}}.
    """
    out: dict[str, dict] = {}
    for cid in list_pages(wiki, "sources"):
        sid = cid.split("/", 1)[1]
        text = _read(os.path.join(wiki, f"{cid}.md"))
        seen = set()
        for section in ("Entities Mentioned", "Concepts Covered"):
            for ref in _CID.findall(_section(text, section)):
                if ref not in seen:
                    seen.add(ref)
                    rec = out.setdefault(ref, {"count": 0, "sources": set(), "name": ref.split("/")[-1]})
                    rec["count"] += 1
                    rec["sources"].add(sid)
    for cid in list_pages(wiki, "relationships"):
        text = _read(os.path.join(wiki, f"{cid}.md"))
        for ref in _CID.findall(frontmatter_field(text, "between") or ""):
            rec = out.setdefault(ref, {"count": 0, "sources": set(), "name": ref.split("/")[-1]})
            rec["count"] += 1
    return out


def candidate_descriptions(wiki: str) -> dict:
    """Short gloss per mentioned id, pulled from the source pages' bullet text."""
    gloss: dict[str, str] = {}
    for cid in list_pages(wiki, "sources"):
        text = _read(os.path.join(wiki, f"{cid}.md"))
        for section in ("Entities Mentioned", "Concepts Covered"):
            for line in _section(text, section).splitlines():
                m = re.search(r"`((?:entities|concepts)/[a-z0-9-]+)`.*?—\s*(.*)", line)
                if m:
                    gloss.setdefault(m.group(1), m.group(2).rstrip(" (candidate)").strip())
    return gloss


def build_index(wiki: str, min_mentions: int = 3) -> str:
    counts = scan_mentions(wiki)
    gloss = candidate_descriptions(wiki)
    out = [
        "# Wiki Index",
        "",
        "_Index of the OKF v0.2 bundle. One entry per page, shown by concept ID (path under `wiki/`",
        "without `.md`). Candidates have no page yet — they are named in source summaries and promoted",
        "to a page once they reach 3+ mentions._",
        "",
        "## Sources",
    ]
    for cid in list_pages(wiki, "sources"):
        desc = frontmatter_field(_read(os.path.join(wiki, f"{cid}.md")), "description")
        out.append(f"- [`{cid}`]({cid}.md) — {desc}")
    out.append("")

    for kind, label in (("entities", "Entities"), ("concepts", "Concepts")):
        out.append(f"## {label}")
        pages = list_pages(wiki, kind)
        out.append("_Pages:_" if pages else "_Pages:_ none yet.")
        for cid in pages:
            desc = frontmatter_field(_read(os.path.join(wiki, f"{cid}.md")), "description")
            out.append(f"- [`{cid}`]({cid}.md) — {desc}")
        cands = sorted(c for c, r in counts.items() if c.startswith(f"{kind}/") and not page_exists(wiki, c))
        if cands:
            out.append("")
            out.append("_Candidates (mentions):_")
            for c in cands:
                out.append(f"- `{c}` ({counts[c]['count']}) — {gloss.get(c, '')}")
        out.append("")

    out.append("## Relationships")
    rels = list_pages(wiki, "relationships")
    if rels:
        for cid in rels:
            desc = frontmatter_field(_read(os.path.join(wiki, f"{cid}.md")), "description")
            out.append(f"- [`{cid}`]({cid}.md) — {desc}")
    else:
        out.append("_Pages:_ none yet.")
    out.append("")

    out.append("## Overviews")
    ovs = list_pages(wiki, "overviews")
    out += [f"- [`{cid}`]({cid}.md)" for cid in ovs] or ["_Pages:_ none yet."]
    out.append("")
    return "\n".join(out)


def write_index(root: str, min_mentions: int = 3) -> None:
    wiki = os.path.join(root, WIKI_DIR)
    with open(os.path.join(wiki, "index.md"), "w", encoding="utf-8") as fh:
        fh.write(build_index(wiki, min_mentions) + "\n")


def append_log(root: str, entries: list[str], date: str | None = None) -> None:
    """Prepend entries under today's ISO heading in wiki/log.md (newest group first)."""
    wiki = os.path.join(root, WIKI_DIR)
    path = os.path.join(wiki, "log.md")
    date = date or now_iso()[:10]
    body = _read(path) if os.path.exists(path) else "# Log\n"
    bullet = "\n".join(f"- {e}" for e in entries)
    heading = f"## {date}"
    if heading in body:
        body = body.replace(heading, f"{heading}\n{bullet}", 1)
    else:
        body = body.rstrip() + f"\n\n{heading}\n{bullet}\n"
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(body if body.endswith("\n") else body + "\n")
