# Log

## 2026-11-01
- **Reformat**: corrected `generated.by` on all 22 pages from `llm-wiki-dci/claude-opus-4-8` to `llm-wiki-lite/1.0` — `dci` (the notebook reader) is never a page producer; this bundle was built by the `llm-wiki-lite` workflow. `generated.at` left unchanged (pure reformat). Also aligned the source: `SCHEMA.md` example and `wiki.py` `_generated()` now stamp `llm-wiki/<model>` for the scripted skill.

## 2026-10-24
- **Ingest**: full corpus via the `llm-wiki-lite` workflow — six sources, oldest first: `where-it-all-started-why-building-a-semantic-layer-for-genai` (2026-01-16), `what-is-a-semantic-layer-after-all` (2026-02-06), `the-semantic-layer-landscape-what-you-need-to-know-before-choosing-one` (2026-05-17), `semantics-where-the-code-lives-…-v0-3-0-release` (2026-07-10), `two-agents-walk-into-an-mcp-…-v0-4-1-release` (2026-07-22), `the-semantic-layer-can-now-fail-your-build-…-v0-5-release` (2026-08-28).
- **Create**: entity pages `semantido`, `dragos-crintea`, `hikari-labs`, `sqlalchemy`, `mcp` (each ≥3 mentions).
- **Create**: concept pages `semantic-layer`, `text2sql`, `semantics`, `hallucination`, `ontology`, `semantic-drift` (each ≥3 mentions).
- **Create**: relationship pages `semantics-vs-ontology`, `semantic-layer-improves-text2sql`, `semantido-builds-on-sqlalchemy`, `semantido-uses-mcp`.
- **Create**: `overviews/overview` — synthesis of the series and the semantido v0.3–v0.5 arc.
- **Candidates**: 19 entity and 9 concept candidates below the 3-mention threshold recorded in `index.md` (notably `entities/osi`, `concepts/grain`, `concepts/concept-registry` at 2 mentions each).
- **Warn**: none of the six raw files carry a date prefix. Suggested dated names use each article's publication date (e.g. `raw/2026-01-16-where-it-all-started-why-building-a-semantic-layer-for-genai.md`). Not renamed — that is the user's decision.
