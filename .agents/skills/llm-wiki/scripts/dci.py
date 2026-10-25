"""dci.py — Direct Corpus Interaction: tool-calling agent over the compiled wiki/ bundle.

The model never reads the corpus directly. It uses three tools (list_pages, grep_wiki,
read_page) injected as tool-result messages, following a standard ReAct loop.

Usage (from the project root):
    uv run python .agents/skills/llm-wiki/scripts/dci.py "your question here"
    uv run python .agents/skills/llm-wiki/scripts/dci.py --k 10 "your question here"

Environment:
    ANTHROPIC_API_KEY   required
    LLM_MODEL           optional; defaults to claude-opus-4-5
"""

from __future__ import annotations

import argparse
import os
import re
import sys
import time
from pathlib import Path

# ── resolve paths ──────────────────────────────────────────────────────────────
SCRIPT_DIR   = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parents[2]          # scripts/ → llm-wiki/ → skills/ → .agents/ → root
WIKI_ROOT    = PROJECT_ROOT / "wiki"

sys.path.insert(0, str(SCRIPT_DIR))           # so util and prompts are importable
import prompts
import util

# ── model ──────────────────────────────────────────────────────────────────────
DEFAULT_MODEL = "claude-opus-4-5"


# ─────────────────────────────────────────────────────────────────────────────
# Corpus loading
# ─────────────────────────────────────────────────────────────────────────────

def load_corpus(wiki_root: Path) -> dict[str, str]:
    """Read every wiki page into memory once. Returns {concept_id: text}."""
    pages: dict[str, str] = {}
    for subdir in util.PAGE_DIRS:
        folder = wiki_root / subdir
        if folder.is_dir():
            for md in sorted(folder.glob("*.md")):
                if md.name in util.RESERVED:
                    continue
                page_id = f"{subdir}/{md.stem}"
                pages[page_id] = md.read_text(encoding="utf-8")
    return pages


# ─────────────────────────────────────────────────────────────────────────────
# Tool implementations
# ─────────────────────────────────────────────────────────────────────────────

def make_tools(wiki_root: Path) -> tuple[dict[str, object], str]:
    """
    Build the tool-function dispatch map and the pre-built wiki index string.
    Returns (funcs, wiki_index_text).
    """
    pages      = load_corpus(wiki_root)
    wiki_index = util.build_index(str(wiki_root))

    def list_pages_fn() -> str:
        """Return the full wiki index so the model can orient itself."""
        return wiki_index

    def grep_wiki_fn(pattern: str) -> str:
        """Search a regex (or plain text) across all wiki pages with line provenance."""
        try:
            rx = re.compile(pattern, re.I)
        except re.error:
            rx = re.compile(re.escape(pattern), re.I)
        hits = []
        for page_id, text in pages.items():
            for lineno, line in enumerate(text.splitlines(), 1):
                if rx.search(line):
                    hits.append(f"{page_id}:{lineno}: {line}")
        return "\n".join(hits[:40]) or "(no matches)"

    def read_page_fn(page: str, start: int = 0) -> str:
        """Read a wiki page by concept ID; paginate with start= for long pages."""
        if page not in pages:
            return f"(unknown page: {page!r} — call list_pages to see valid IDs)"
        chunk     = pages[page][start : start + 12_000]
        remaining = max(0, len(pages[page]) - start - 12_000)
        suffix    = (
            f"\n\n[…{remaining} chars remaining — call read_page with start={start + 12_000}]"
            if remaining else ""
        )
        return chunk + suffix

    funcs = {
        "list_pages": list_pages_fn,
        "grep_wiki":  grep_wiki_fn,
        "read_page":  read_page_fn,
    }
    return funcs, wiki_index


# ─────────────────────────────────────────────────────────────────────────────
# Tool schemas (Anthropic messages API format)
# ─────────────────────────────────────────────────────────────────────────────

DCI_TOOLS = [
    {
        "name": "list_pages",
        "description": (
            "Read the wiki index to discover all page IDs and their one-line descriptions. "
            "Call this first to orient yourself before searching or reading."
        ),
        "input_schema": {"type": "object", "properties": {}, "required": []},
    },
    {
        "name": "grep_wiki",
        "description": (
            "Search exact text or a regex across all wiki pages. "
            "Returns up to 40 matching lines with page-ID:line-number provenance. "
            "Use short lexical queries: names, identifiers, key terms."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "pattern": {
                    "type": "string",
                    "description": "Plain text or Python regex (case-insensitive) to search for.",
                }
            },
            "required": ["pattern"],
        },
    },
    {
        "name": "read_page",
        "description": (
            "Read a complete wiki page by its concept ID (e.g. 'entities/semantido'). "
            "Pages longer than 12 000 chars are truncated; use start= to paginate."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "page": {
                    "type": "string",
                    "description": "Concept ID exactly as shown by list_pages.",
                },
                "start": {
                    "type": "integer",
                    "description": "Byte offset to start reading from (default 0).",
                },
            },
            "required": ["page"],
        },
    },
]


# ─────────────────────────────────────────────────────────────────────────────
# System prompt
# ─────────────────────────────────────────────────────────────────────────────

def build_system(wiki_index: str) -> str:
    first_line = wiki_index.splitlines()[0] if wiki_index else "an OKF wiki bundle"
    return (
        prompts.DCI_SYSTEM
        + f"""

Available tools:
  • list_pages()                 — get the full wiki index (call this first)
  • grep_wiki(pattern)           — fast text/regex search across all pages
  • read_page(page, start=0)     — read a page by concept ID; paginate with start=

Strategy:
  1. Call list_pages() to orient yourself.
  2. Use grep_wiki() to pinpoint relevant page IDs.
  3. read_page() the candidates; follow pagination hints if truncated.
  4. Synthesise and cite pages by concept ID, e.g. (entities/semantido).

This wiki covers: {first_line}
"""
    )


# ─────────────────────────────────────────────────────────────────────────────
# Agent loop
# ─────────────────────────────────────────────────────────────────────────────

def run_agent(
    question: str,
    *,
    wiki_root: Path = WIKI_ROOT,
    max_turns: int = 8,
    model: str | None = None,
) -> dict:
    """
    Run the DCI agent for one question. Returns a result dict with keys:
        answer, trace, evidence_chars, latency_s, stopped, turns
    """
    import anthropic  # imported here so the module is usable without it installed

    resolved_model = model or os.environ.get("LLM_MODEL", DEFAULT_MODEL)
    client         = anthropic.Anthropic()
    funcs, wiki_index = make_tools(wiki_root)
    system         = build_system(wiki_index)

    messages: list[dict] = [{"role": "user", "content": question}]
    trace: list[dict]    = []
    evidence_chars       = 0
    t0                   = time.perf_counter()

    for turn in range(max_turns):
        response = client.messages.create(
            model=resolved_model,
            max_tokens=4096,
            system=system,
            tools=DCI_TOOLS,
            messages=messages,
        )

        # Serialise content blocks to plain dicts so messages stay JSON-safe
        serialised_content = [
            block.model_dump() if hasattr(block, "model_dump") else dict(block)
            for block in response.content
        ]
        messages.append({"role": "assistant", "content": serialised_content})

        if response.stop_reason == "end_turn":
            answer = " ".join(
                block.text
                for block in response.content
                if hasattr(block, "text")
            ).strip()
            return {
                "answer":         answer,
                "trace":          trace,
                "evidence_chars": evidence_chars,
                "latency_s":      round(time.perf_counter() - t0, 2),
                "stopped":        "answer",
                "turns":          turn + 1,
            }

        # Dispatch tool calls
        tool_results: list[dict] = []
        for block in response.content:
            if block.type != "tool_use":
                continue
            name = block.name
            args = block.input or {}
            try:
                if name not in funcs:
                    raise KeyError(f"unknown tool {name!r}")
                result = str(funcs[name](**args))
            except Exception as exc:
                result = f"(tool error: {type(exc).__name__}: {exc})"
            evidence_chars += len(result)
            trace.append({"tool": name, "args": args, "chars": len(result)})
            tool_results.append({
                "type":        "tool_result",
                "tool_use_id": block.id,
                "content":     result,
            })

        messages.append({"role": "user", "content": tool_results})

    return {
        "answer":         "(max turns reached — try a more specific question or raise max_turns)",
        "trace":          trace,
        "evidence_chars": evidence_chars,
        "latency_s":      round(time.perf_counter() - t0, 2),
        "stopped":        "max_turns",
        "turns":          max_turns,
    }


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────

def _print_result(result: dict) -> None:
    print(result["answer"])
    print(
        f"\n[{result['stopped']} | turns={result['turns']} | "
        f"{result['latency_s']}s | {result['evidence_chars']:,} evidence chars]"
    )
    if result["trace"]:
        print("\nTool trace:")
        for step in result["trace"]:
            args_str = ", ".join(f"{k}={v!r}" for k, v in step["args"].items())
            print(f"  → {step['tool']}({args_str})  [{step['chars']:,} chars]")


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        prog="dci.py",
        description="Ask a question answered from the compiled wiki/ bundle via tool-calling.",
    )
    parser.add_argument("question", help="Natural-language question to answer.")
    parser.add_argument(
        "--root", default=str(PROJECT_ROOT),
        help="Project root holding wiki/ (default: auto-detected from script location).",
    )
    parser.add_argument(
        "--max-turns", type=int, default=8,
        help="Maximum agent turns before giving up (default: 8).",
    )
    parser.add_argument(
        "--model", default=None,
        help=f"Model ID to use (default: $LLM_MODEL or {DEFAULT_MODEL}).",
    )
    args = parser.parse_args(argv)

    if not os.environ.get("ANTHROPIC_API_KEY"):
        print(
            "error: ANTHROPIC_API_KEY is not set.\n"
            "Copy .env.example to .env, paste your key, then:\n"
            "  set -a && source .env && set +a",
            file=sys.stderr,
        )
        return 1

    result = run_agent(
        args.question,
        wiki_root=Path(args.root) / "wiki",
        max_turns=args.max_turns,
        model=args.model,
    )
    _print_result(result)
    return 0 if result["stopped"] == "answer" else 1


if __name__ == "__main__":
    sys.exit(main())