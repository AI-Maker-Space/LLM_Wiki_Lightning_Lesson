---
name: llm-wiki
description: Build and maintain a schema-driven LLM Wiki - a Karpathy-style knowledge base where immutable raw/ sources are compiled by an LLM into a wiki/ folder that is a valid Open Knowledge Format (OKF) bundle of entities, concepts, relationships, sources and overviews - and search large document collections with DR-DCI (retrieval-steered direct corpus interaction - pull ranked documents into a workspace, then grep and read them). Use this skill whenever the user wants to ingest articles, papers or notes into a wiki, Obsidian vault or OKF bundle, keep a research knowledge base up to date, lint or prune a wiki, answer questions from a wiki, verify a claim against original sources, or find exact facts, figures or multi-hop answers across hundreds to millions of documents - even if they only say "add this to my knowledge base", "what do my sources say about X", or "search the corpus".
compatibility: Python 3.10+. LLM steps need the `anthropic` or `openai` package plus ANTHROPIC_API_KEY or OPENAI_API_KEY in the environment (LLM_PROVIDER and LLM_MODEL optional; LLM_MODEL required for openai).
---

# LLM Wiki

**`wiki/` is an OKF v0.2 bundle.** It holds one concept per file, and a concept's ID is its path
inside `wiki/` without `.md` (e.g. `entities/tessellate-labs`). Every page has YAML frontmatter
with `type` first, then title, description, tags, `generated: {by, at}` and keyed `sources`.
Links are relative Markdown links inside the bundle, and claims cite sources with footnotes
keyed to `sources[].id`. Point any OKF tool at `wiki/` and it works.

**The edit rule.** Write only inside `wiki/`, and only through the scripts. Never modify `raw/`.


## How these workflows run

You (the agent) carry out every operation by running the `wiki.py` CLI in the shell — **the user
asks in natural language and you run the script**, then read its output and report back. The user
never runs anything themselves. `SCHEMA.md` and `scripts/prompts.py` do the thinking; the CLI is the
door.

Run from the project root (the folder holding `wiki/` and `raw/`), prefixing each command with
`python .agents/skills/llm-wiki/scripts/`:

| When the user… | Run | Workflow |
|---|---|---|
| "ingest raw", "add these articles", "update my wiki" | `wiki.py ingest` | 1 |
| "I deleted X from raw", "prune removed sources" | `wiki.py ingest --prune` | 2 |
| "what do my sources say about X?", "does the wiki cover Y?" | `wiki.py query "…"` | 3 |
| "check / audit / lint the wiki" | `wiki.py lint` | 4 |
| "the index looks stale", "rebuild the index" | `wiki.py index` | 5 |

`ingest` and `query` call the LLM (need a provider — see Tooling); `lint` and `index` do not.

The wiki is **stateless**: the Markdown pages under `wiki/` are the only source of truth. The LLM
writes each page directly; there is no `.wiki-state.json` and no byte-identical rebuild.

## Workflow 1 — Ingest sources

Run `wiki.py ingest`. It processes each raw file that has no source page yet, oldest first (date
from the file-name prefix, else frontmatter, else mtime); `--all` re-ingests every file. For each
one the LLM:

- writes the source summary to `wiki/sources/<slug>.md`;
- writes or updates entity/concept pages once something reaches **3+ mentions** across the pages
  (tune with `--min-mentions N`), leaving the rest as candidates in `index.md`, with each fact cited
  and an older fact marked *superseded by* a newer source that revises it;
- writes a relationship page when a source makes an explicit claim about how two things relate;
- writes/refreshes the overview when the big picture materially changes.

It then regenerates `index.md` by scanning the pages, appends to `log.md`, runs `lint`, and prints a
summary. Afterwards, read the new `log.md` entries: a raw file with **no date prefix** is recorded
there with a suggested dated name — pass that to the user and let them rename it (never rename
anything in `raw/` yourself).

## Workflow 2 — Prune withdrawn sources

When the user removes a file from `raw/`, run `wiki.py ingest --prune`. For each withdrawn source,
the LLM rewrites every page that cited it so its facts, quotes and footnotes are gone and the prose
matches what remains; the source summary is deleted, pages left with nothing are deleted, and
`index.md` is regenerated and linted. (Without a state file this is model-driven rather than exact,
so review the result — see Workflow 4.)

## Workflow 3 — Query the wiki

Run `wiki.py query "<the user's question>"`. The command selects the most relevant pages from
`index.md`, reads them, and returns a prose answer that cites pages by concept ID, prefers the
newest source where facts disagree, and flags superseded facts. Relay the answer and its citations,
and open a cited page if the user wants more detail. The question is logged in `log.md`.

**Natural-language example**

> **User:** "Using my wiki, why did the author start building a semantic layer?"
>
> **You run:**
> ```
> python .agents/skills/llm-wiki/scripts/wiki.py query "why did the author start building a semantic layer?"
> ```
> **You relay (shape of the answer):** "Brittle Text2SQL — an LLM generating SQL against the
> author's gym-assistant tables kept misreading columns because it had no idea what the fields meant
> or how they related. Adding table semantics to the prompt fixed it, which motivated building
> semantido (cites `sources/where-it-all-started-why-building-a-semantic-layer-for-genai`)."

If no provider is configured, fall back to answering by hand: read `index.md`, open the relevant
pages, and answer with the same citation rules.

## Workflow 4 — Audit (lint)

Run `wiki.py lint`. It prints one line per finding:

- **ERROR** — a broken body link, a missing `type`, or a date in a `wiki/` file name (exit code 1);
- **WARN** — an entity/concept/relationship page with no inbound link (an orphan);
- **PENDING** — a candidate still below the mention threshold (informational, not a defect).

Report everything except PENDING to the user. `ingest` and `index` run `lint` automatically, so you
mostly run it on its own to re-check after a manual change or when the user asks for an audit.

## Workflow 5 — Regenerate the index

Run `wiki.py index` to rebuild `index.md` by scanning the pages (pages listed by ID, plus candidates
with their mention counts). No LLM. Use it if `index.md` looks out of date after hand-edits.

## Tooling

The full command reference (flags, exit codes, troubleshooting) is in this folder's `README.md`.
Architecture (stateless): the LLM writes each Markdown page directly, following `wiki/SCHEMA.md` and
`references/page-templates.md` (`scripts/prompts.py`); `scripts/wiki.py` discovers raw files, calls
the model, writes the pages, and `scripts/util.py` scans the pages to count mentions and regenerate
`index.md`. The pages are the only source of truth — there is no state file. `scripts/llm.py` is the
provider-agnostic client: set `LLM_PROVIDER` (`anthropic` default | `openai`), `LLM_MODEL` (defaults
to `claude-opus-5-5` for anthropic; required for openai), the matching `ANTHROPIC_API_KEY` /
`OPENAI_API_KEY`, and `pip install anthropic` (or `openai`).

## Customising

- The vault's own `../../../wiki/SCHEMA.md` governs that vault and is included in every LLM prompt.
- `scripts/prompts.py` holds the prompts; each returns a finished Markdown page (or, for `query`
  selection and relationship planning, a tiny list/JSON). `references/page-templates.md` documents
  the page layout and `references/schema-guide.md` the frontmatter and naming rules.
- `scripts/util.py` controls raw discovery, slug/date resolution, mention counting and `index.md`.
- Thresholds: `--min-mentions` (default 3).

