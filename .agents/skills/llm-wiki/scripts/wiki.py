#!/usr/bin/env python3
"""llm-wiki CLI — ingest raw sources into the OKF bundle, lint it, query it (stateless).

    python wiki.py ingest [--prune] [--all] [--min-mentions N] [--root DIR]
    python wiki.py lint   [--root DIR]
    python wiki.py query  "question" [--k 6] [--root DIR]
    python wiki.py index  [--root DIR]      # regenerate index.md from the pages

There is no `.wiki-state.json`: the Markdown pages under `wiki/` are the only source of truth. The
LLM writes each page directly (prompts.py); `wiki.py` discovers raw files, calls the model, writes
the pages, regenerates `index.md` by scanning the bundle, appends to `log.md`, and lints. `lint`,
`index` and the discovery logic need no API key; `ingest` and `query` do (see llm.py).
"""

from __future__ import annotations

import argparse
import os
import re
import sys

import prompts
import util

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


# ----------------------------------------------------------------------------- shared


def _read(path: str) -> str:
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def _schema(root: str) -> str:
    path = os.path.join(root, util.SCHEMA_REL)
    if not os.path.exists(path):
        raise SystemExit(f"Missing {util.SCHEMA_REL}. The bundle must carry its own schema.")
    return _read(path)


def _templates() -> str:
    path = os.path.join(SCRIPT_DIR, "..", "references", "page-templates.md")
    return _read(path) if os.path.exists(path) else ""


def _llm():
    import llm

    return llm


def _generated() -> str:
    try:
        import llm

        model = llm.model_id()
    except Exception:
        model = "unknown"
    return f'{{ by: "llm-wiki-dci/{model}", at: {util.now_iso()} }}'


def _raw_meta(content: str, date: str) -> dict:
    resource = ""
    m = re.search(r"^(?:source|url|link)\s*:\s*[\"']?(\S+)", content, re.MULTILINE)
    if m:
        resource = m.group(1).strip().strip("\"'")
    author = "human:unknown"
    m = re.search(r"^author\s*:\s*[\"']?([^\"'\n]+)", content, re.MULTILINE)
    if m and m.group(1).strip():
        author = f"human:{util.slugify(m.group(1).strip())}"
    return {"resource": resource, "author": author, "last_modified": f"{date}T00:00:00Z"}


def _source_record(wiki: str, sid: str) -> dict:
    text = _read(os.path.join(wiki, f"sources/{sid}.md"))
    author = re.search(r'author:\s*"?(human:[^"\n]+|process:[^"\n]+|[^"\n/]+/[^"\n]+)"?', text)
    lm = re.search(r"last_modified:\s*(\S+)", text)
    return {
        "sid": sid,
        "title": util.frontmatter_field(text, "title") or sid,
        "author": (author.group(1).strip() if author else "human:unknown"),
        "last_modified": (lm.group(1).strip() if lm else ""),
    }


def _raw_sources_block(sid: str, raw_file: str, title: str, meta: dict) -> str:
    return "\n".join(
        [
            '  - id: "raw"',
            f'    resource: "../../raw/{raw_file}"',
            f'    title: "{title}"',
            f'    author: "{meta["author"]}"',
            f'    last_modified: {meta["last_modified"]}',
        ]
    )


def _sources_block(records: list[dict]) -> str:
    lines = []
    for r in records:
        lines += [
            f'  - id: "{r["sid"]}"',
            f'    resource: "../sources/{r["sid"]}.md"',
            f'    title: "{r["title"]}"',
            f'    author: "{r["author"]}"',
            f'    last_modified: {r["last_modified"]}',
        ]
    return "\n".join(lines)


def _section(text: str, heading: str) -> str:
    m = re.search(rf"(?ms)^##\s+{re.escape(heading)}\s*\n(.*?)(?=^##\s|\Z)", text)
    return m.group(1).strip() if m else ""


def _evidence(wiki: str, sids: list[str]) -> str:
    blocks = []
    for sid in sids:
        text = _read(os.path.join(wiki, f"sources/{sid}.md"))
        summary = _section(text, "Summary")
        claims = _section(text, "Key Claims")
        blocks.append(f"=== source id: {sid} ===\n{summary}\n\nKey claims:\n{claims}")
    return "\n\n".join(blocks)


def _known_block(wiki: str) -> str:
    lines = []
    for kind in ("entities", "concepts"):
        for cid in util.list_pages(wiki, kind):
            desc = util.frontmatter_field(_read(os.path.join(wiki, f"{cid}.md")), "description")
            lines.append(f"  {cid}: {desc}")
    return "\n".join(lines) or "  (none yet — this is an empty wiki)"


def _write_page(wiki: str, cid: str, text: str) -> None:
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```[a-z]*\n", "", text)
        text = re.sub(r"\n```$", "", text)
    path = os.path.join(wiki, f"{cid}.md")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text.rstrip() + "\n")


# ----------------------------------------------------------------------------- ingest


def cmd_ingest(args) -> int:
    root, wiki = args.root, os.path.join(args.root, util.WIKI_DIR)
    schema, templates = _schema(root), _templates()
    system = prompts.system(schema, templates)
    gen = _generated()
    raws = util.list_raw(root)
    live = {r["slug"]: r for r in raws}
    log: list[str] = []

    if args.prune:
        removed = _prune(root, wiki, set(live), system, gen, log)
        print(f"Pruned {len(removed)} withdrawn source(s)." if removed else "Nothing to prune.")

    todo = [r for r in raws if args.all or not util.page_exists(wiki, f"sources/{r['slug']}")]
    if not todo and not args.prune:
        print("No new raw files to ingest (source pages already exist; use --all to re-ingest).")
        return 0

    llm = _llm()
    new_sids: list[str] = []
    created, updated = [], []
    try:
        for r in todo:
            sid = r["slug"]
            meta = _raw_meta(r["content"], r["date"])
            title = util.frontmatter_field(r["content"], "title") or sid
            print(f"Ingesting {r['name']} (date {r['date']}) …")
            page = llm.complete_text(system, prompts.SOURCE.format(
                generated=gen, sources_block=_raw_sources_block(sid, r["name"], title, meta),
                resource=meta["resource"], sid=sid, raw_file=r["name"],
                known=_known_block(wiki), raw=r["content"]))
            _write_page(wiki, f"sources/{sid}", page)
            new_sids.append(sid)
            log.append(f"**Ingest**: `sources/{sid}` from `{util.RAW_DIR}/{r['name']}`.")
            if not r["had_prefix"]:
                ext = r["name"].rsplit(".", 1)[-1]
                log.append(f"**Warn**: `{r['name']}` has no date prefix; suggested `raw/{r['date']}-{sid}.{ext}` (not renamed — user's decision).")

        new_set = set(new_sids)
        mentions = util.scan_mentions(wiki)
        for cid, rec in sorted(mentions.items()):
            kind = cid.split("/", 1)[0]
            if kind not in ("entities", "concepts"):
                continue
            exists = util.page_exists(wiki, cid)
            if not exists and rec["count"] < args.min_mentions:
                continue
            if exists and not (rec["sources"] & new_set):
                continue
            ev_sids = sorted(rec["sources"])
            kind_title = "Entity" if kind == "entities" else "Concept"
            current = f"CURRENT PAGE:\n{_read(os.path.join(wiki, cid + '.md'))}" if exists else "This is a new page."
            page = llm.complete_text(system, prompts.TOPIC.format(
                action=("Update" if exists else "Create"), kind=kind_title.lower(), kind_title=kind_title,
                cid=cid, generated=gen, sources_block=_sources_block([_source_record(wiki, s) for s in ev_sids]),
                source_ids=", ".join(ev_sids), current=current, evidence=_evidence(wiki, ev_sids)))
            _write_page(wiki, cid, page)
            (updated if exists else created).append(cid)

        want_overview = False
        for sid in new_sids:
            plan = _plan(llm, system, wiki, sid)
            for rel in plan.get("relationships", []):
                rid = _relationship_id(rel)
                if _ingest_relationship(llm, system, wiki, rel, rid, gen):
                    created.append(f"relationships/{rid}")
            want_overview = want_overview or plan.get("overview", False)
        if want_overview or (new_sids and not util.list_pages(wiki, "overviews")):
            _ingest_overview(llm, system, wiki, root, gen)
            log.append("**Overview**: refreshed.")
    except llm.LLMError as exc:
        print(f"\nIngest stopped: {exc}", file=sys.stderr)
        print("Set up the model (pip install anthropic + ANTHROPIC_API_KEY or `ant auth login`), then re-run.", file=sys.stderr)
        return 2

    if created:
        log.append(f"  Pages created: {', '.join(sorted(created))}")
    if updated:
        log.append(f"  Pages updated: {', '.join(sorted(updated))}")
    util.write_index(root, args.min_mentions)
    util.append_log(root, log)
    print(f"Ingested {len(todo)} source(s); index.md rebuilt.")
    return cmd_lint(args)


def _plan(llm, system: str, wiki: str, sid: str) -> dict:
    text = _read(os.path.join(wiki, f"sources/{sid}.md"))
    summary = _section(text, "Summary") + "\n" + _section(text, "Key Claims")
    try:
        return llm.complete_json(system, prompts.PLAN.format(
            sid=sid, existing=", ".join(util.list_pages(wiki, "relationships")) or "(none)", summary=summary))
    except llm.LLMError:
        return {}


def _relationship_id(rel: dict) -> str:
    a, b = rel.get("a", "").split("/")[-1], rel.get("b", "").split("/")[-1]
    return f"{a}-vs-{b}" if rel.get("relation") == "compares" else f"{a}-{rel.get('relation', 'other')}-{b}"


def _ingest_relationship(llm, system: str, wiki: str, rel: dict, rid: str, gen: str) -> bool:
    cid = f"relationships/{rid}"
    a, b = rel.get("a", ""), rel.get("b", "")
    # only relate pages that exist, so body links resolve
    if not (util.page_exists(wiki, a) and util.page_exists(wiki, b)):
        return False
    exists = util.page_exists(wiki, cid)
    ev = sorted(set(util.scan_mentions(wiki).get(a, {}).get("sources", set())) |
                set(util.scan_mentions(wiki).get(b, {}).get("sources", set())))
    if not ev:
        return False
    current = f"CURRENT PAGE:\n{_read(os.path.join(wiki, cid + '.md'))}" if exists else "This is a new page."
    page = llm.complete_text(system, prompts.RELATIONSHIP.format(
        action=("Update" if exists else "Create"), cid=cid, a=a, b=b, relation=rel.get("relation", "other"),
        generated=gen, sources_block=_sources_block([_source_record(wiki, s) for s in ev]),
        source_ids=", ".join(ev), current=current, evidence=_evidence(wiki, ev)))
    _write_page(wiki, cid, page)
    return not exists


def _ingest_overview(llm, system: str, wiki: str, root: str, gen: str) -> None:
    sids = [c.split("/", 1)[1] for c in util.list_pages(wiki, "sources")]
    exists = util.list_pages(wiki, "overviews")
    page = llm.complete_text(system, prompts.OVERVIEW.format(
        action=("Update" if exists else "Create"), generated=gen,
        sources_block=_sources_block([_source_record(wiki, s) for s in sids]),
        source_ids=", ".join(sids), index=util.build_index(wiki), evidence=_evidence(wiki, sids)))
    _write_page(wiki, "overviews/overview", page)


def _prune(root: str, wiki: str, live: set, system: str, gen: str, log: list) -> list[str]:
    llm = _llm()
    removed = []
    for cid in util.list_pages(wiki, "sources"):
        sid = cid.split("/", 1)[1]
        if sid in live:
            continue
        removed.append(sid)
        os.remove(os.path.join(wiki, f"{cid}.md"))
        for kind in ("entities", "concepts", "relationships"):
            for pid in util.list_pages(wiki, kind):
                path = os.path.join(wiki, f"{pid}.md")
                page = _read(path)
                if f"[^{sid}]" not in page:
                    continue
                out = llm.complete_text(system, prompts.WITHDRAW.format(sid=sid, page=page))
                if out.strip() == "DELETE":
                    os.remove(path)
                else:
                    _write_page(wiki, pid, out)
        log.append(f"**Prune**: withdrew `{sid}` (raw file removed).")
    return removed


# ----------------------------------------------------------------------------- lint


_LINK_RE = re.compile(r"(?<!\!)\[[^\]]*\]\(([^)]+)\)")
_FENCE_RE = re.compile(r"```.*?```", re.DOTALL)


def _lint(root: str) -> list[tuple[str, str]]:
    wiki = os.path.join(root, util.WIKI_DIR)
    issues: list[tuple[str, str]] = []
    if not os.path.isdir(wiki):
        return [("ERROR", "wiki/ bundle does not exist. Run `ingest` first.")]

    page_files = []
    for sub in util.PAGE_DIRS:
        d = os.path.join(wiki, sub)
        if os.path.isdir(d):
            page_files += [f"{sub}/{n}" for n in os.listdir(d) if n.endswith(".md")]

    inbound: dict[str, int] = {}
    for rel in page_files:
        text = _read(os.path.join(wiki, rel))
        if not re.match(r"^---\s*\ntype:\s*\w+", text):
            issues.append(("ERROR", f"{rel}: frontmatter must start with `type:`."))
        if util._DATE_PREFIX.match(os.path.basename(rel)):
            issues.append(("ERROR", f"{rel}: wiki file name carries a date prefix."))
        defs = set(re.findall(r"(?m)^\[\^([^\]]+)\]:", text))
        refs = set(re.findall(r"\[\^([^\]]+)\](?!:)", text))
        for missing in sorted(refs - defs):
            issues.append(("ERROR", f"{rel}: footnote [^{missing}] has no definition."))
        body = _FENCE_RE.sub("", text)
        for target in _LINK_RE.findall(body):
            tgt = target.split("#", 1)[0].strip()
            if not tgt or tgt.startswith(("http://", "https://", "mailto:")):
                continue
            resolved = os.path.normpath(os.path.join(os.path.dirname(os.path.join(wiki, rel)), tgt))
            if not os.path.exists(resolved):
                issues.append(("ERROR", f"{rel}: broken link → {target}"))
            elif tgt.endswith(".md"):
                inbound[os.path.relpath(resolved, wiki)] = inbound.get(os.path.relpath(resolved, wiki), 0) + 1

    for rel in page_files:
        if not rel.startswith(("sources/", "overviews/")) and inbound.get(rel, 0) == 0:
            issues.append(("WARN", f"{rel}: no inbound link from another page (orphan)."))

    counts = util.scan_mentions(wiki)
    for cid, rec in sorted(counts.items()):
        if not util.page_exists(wiki, cid) and rec["count"] < 3:
            issues.append(("PENDING", f"{cid}: candidate with {rec['count']} mention(s), below threshold 3."))
    return issues


def cmd_lint(args) -> int:
    issues = _lint(args.root)
    for level, msg in issues:
        print(f"[{level}] {msg}")
    real = sum(1 for lv, _ in issues if lv != "PENDING")
    pending = sum(1 for lv, _ in issues if lv == "PENDING")
    print(f"\nlint: {real} issue(s) to report, {pending} PENDING candidate(s).")
    return 1 if any(lv == "ERROR" for lv, _ in issues) else 0


# ----------------------------------------------------------------------------- query / index


def cmd_query(args) -> int:
    root, wiki = args.root, os.path.join(args.root, util.WIKI_DIR)
    llm = _llm()
    system = prompts.system(_schema(root), _templates())
    try:
        picked = llm.complete_text(system, prompts.QUERY_SELECT.format(k=args.k, index=util.build_index(wiki), question=args.question))
    except llm.LLMError as exc:
        print(f"Query needs the model: {exc}", file=sys.stderr)
        return 2
    ids = [ln.strip() for ln in picked.splitlines() if re.match(r"^[a-z]+/[a-z0-9-]+$", ln.strip())][: args.k]
    pages = []
    for cid in ids:
        path = os.path.join(wiki, f"{cid}.md")
        if os.path.exists(path):
            pages.append(f"=== {cid} ===\n{_read(path)}")
    answer = llm.complete_text(system, prompts.QUERY_ANSWER.format(pages="\n\n".join(pages), question=args.question))
    util.append_log(root, [f'**Query**: "{args.question}" — referenced {", ".join(ids) or "no pages"}.'])
    print(answer)
    return 0


def cmd_index(args) -> int:
    util.write_index(args.root, args.min_mentions)
    print("index.md regenerated from the pages.")
    return cmd_lint(args)


# ----------------------------------------------------------------------------- main


def main(argv=None) -> int:
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--root", default=os.getcwd(), help="project root holding wiki/ and raw/ (default: cwd)")
    common.add_argument("--min-mentions", type=int, default=3, help="mentions required before a page is created")

    parser = argparse.ArgumentParser(prog="wiki.py", description=__doc__, parents=[common], formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_ing = sub.add_parser("ingest", parents=[common], help="ingest new raw sources (the LLM writes the pages)")
    p_ing.add_argument("--prune", action="store_true", help="withdraw sources whose raw file was removed")
    p_ing.add_argument("--all", action="store_true", help="re-ingest every raw file, not only those without a source page")
    p_ing.set_defaults(func=cmd_ingest)

    sub.add_parser("lint", parents=[common], help="audit the bundle").set_defaults(func=cmd_lint)
    sub.add_parser("index", parents=[common], help="regenerate index.md from the pages").set_defaults(func=cmd_index)

    p_q = sub.add_parser("query", parents=[common], help="answer a question from the wiki")
    p_q.add_argument("question")
    p_q.add_argument("--k", type=int, default=6, help="max pages to consult")
    p_q.set_defaults(func=cmd_query)

    args = parser.parse_args(argv)
    args.root = os.path.abspath(args.root)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
