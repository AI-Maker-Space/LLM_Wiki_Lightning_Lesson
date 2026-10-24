---
name: llm-wiki-lite
description: Build and maintain a schema-driven LLM Wiki entirely by hand, with no scripts and no state file - the script-free counterpart to llm-wiki. The LLM reads immutable raw/ sources and writes the wiki/ bundle (a valid Open Knowledge Format bundle of sources, entities, concepts, relationships and overviews) directly as Markdown. Use this when the user wants to ingest articles, papers or notes into a wiki/Obsidian vault/OKF bundle, keep a small research knowledge base up to date, or answer questions from it, and prefers zero setup (no Python, no API key beyond the agent, no install) over scripted automation. For a large or long-lived corpus, use the scripted llm-wiki skill instead — it drives the model from scripts and adds `lint` and `index` commands.
compatibility: No dependencies. Everything is done by the agent reading and writing Markdown.
---

# LLM Wiki (lite)

The script-free version of `llm-wiki`. There is **no tooling** — you, the LLM, are the whole
pipeline. You read the raw sources and write the pages by hand. (The scripted `llm-wiki` is also
stateless and also has the LLM write the pages; it just automates the orchestration.)

**`wiki/` is an OKF v0.2 bundle.** One concept per file; a concept's ID is its path inside `wiki/`
without `.md` (e.g. `entities/semantido`). Every page has YAML frontmatter with `type` first, then
title, description, tags, `generated: {by, at}` and keyed `sources`. Links are relative Markdown
links inside the bundle; claims cite sources with `[^<source-id>]` footnotes. `index.md`, `log.md`
and `SCHEMA.md` are reserved names, never concepts.

**The edit rule.** Write only inside `wiki/`. Never edit, rename or delete anything in `raw/`.

**Before any operation**, read `wiki/SCHEMA.md` (the authoritative conventions for this vault) and
`references/page-templates.md` (the page layouts), then `wiki/index.md` to see what already exists.

## How these workflows run

There are no scripts. **The user asks in natural language and you (the agent) carry out the
operation by reading and writing Markdown directly** — the same five operations as the full
`llm-wiki` skill, done by hand instead of by `wiki.py`. The user never runs anything.

| When the user… | What you do, by hand | Workflow |
|---|---|---|
| "ingest raw", "add these articles", "update my wiki" | read each raw file and write/update its pages | 1 |
| "I deleted X from raw", "prune removed sources" | strip that source's facts and fix the pages | 2 |
| "what do my sources say about X?", "does the wiki cover Y?" | read `index.md` + pages, answer with citations | 3 |
| "check / audit the wiki" | work through the self-check checklist | 4 |
| "reformat the pages", "I changed a template" | re-apply the templates to the pages by hand | 5 |

## Workflow 1 — Ingest a source

Process raw files **one at a time, oldest first**. The date comes from the file-name prefix
(`YYYY-MM-DD-…`), else the frontmatter (`published`/`date`/`last_modified`), else the file's
modification time. For each source:

1. **Read the raw file fully.**
2. **Write the source summary** to `wiki/sources/<slug>.md` using the Source template. The slug is
   the raw name minus any date prefix and extension, lowercased and hyphenated. Fill in: a 2–3
   paragraph Summary, Key Claims (each ending in `[^raw]`), Entities/Concepts Mentioned, Notable
   Quotes (verbatim), and Notes. Add the `[^raw]` footnote definition at the bottom.
3. **Create or update entity/concept pages — by reading the summary you just wrote, not the raw
   file.** Apply the **3-mention rule**: an entity or concept gets its own page only once it has
   **3+ mentions** across the wiki (source summaries + relationships). Count by reading the existing
   pages and `index.md`. Below the threshold it is a *candidate*: named in the source summary and
   listed in `index.md`, with no page yet.
   - When you create a page, use the Entity/Concept template and cite every fact with the source's
     footnote key (`[^<source-slug>]`).
   - When you update a page, add only new facts, each with its citation. When a newer source revises
     a figure, keep both facts (newest first) and mark the older one *superseded by* the newer source.
   - Keep cross-references bidirectional: if page A links to B, B links back to A.
4. **Create a relationship page** (Relationship template) only when the source makes an explicit,
   substantive claim about how two things relate (a comparison, "X is built on Y", "X acquires Y").
   Name it `a-vs-b` for comparisons, `a-<relation>-b` otherwise.
5. **Rewrite the overview** (`wiki/overviews/overview.md`) only when the source materially changes
   the big picture — a new major topic, a reversal, a contradiction, a significant revision.
6. **Update `index.md` and `log.md`.** The index lists every page by concept ID plus the current
   candidates with their mention counts. `log.md` groups entries under ISO `## YYYY-MM-DD` headings,
   newest first, each a bullet starting with a bold word (`- **Ingest**: …`).
7. **Self-check** against SCHEMA's Quality Standards (see the checklist below). Fix, then report
   anything you could not resolve to the user.

If a raw file has **no date prefix**, warn the user and suggest a dated name (from its publication
date); do not rename it — that is their decision.

## Workflow 2 — Prune a withdrawn source

If a raw file was removed, withdraw its source exactly:

1. Delete `wiki/sources/<slug>.md`.
2. Open every entity/concept/relationship page and remove each fact that cites that source, along
   with its footnote. Remove any *superseded by* marker that pointed at it.
3. Delete pages left with no facts and no sources. Rewrite the prose on pages that lost facts so it
   matches what remains.
4. Update `index.md` (recount mentions; demote pages that drop below 3 mentions back to candidates)
   and add a `- **Prune**: …` entry to `log.md`.

## Workflow 3 — Query the wiki

1. Read `index.md` (every entry shows its concept ID), open the relevant pages under `wiki/`.
2. Answer, citing pages by concept ID (e.g. `entities/semantido`). Prefer the newest source when
   facts disagree; a fact marked *superseded by* has been revised.
3. Add a `- **Query**: "…"` entry to `log.md` noting the pages referenced.

**Natural-language example**

> **User:** "Using my wiki, why did the author start building a semantic layer?"
>
> **You:** read `wiki/index.md`, open `wiki/sources/where-it-all-started-why-building-a-semantic-layer-for-genai.md`
> (and any entity/concept pages it links), then answer:
>
> "Brittle Text2SQL — an LLM generating SQL against the author's gym-assistant tables kept
> misreading columns because it had no idea what the fields meant or how they related. Adding table
> semantics to the prompt fixed it, which motivated building semantido
> (cites `sources/where-it-all-started-why-building-a-semantic-layer-for-genai`)."
>
> Then log the query in `log.md`.

## Workflow 4 — Audit (self-check)

Run this after every ingest or prune, and whenever the user asks you to check or audit the wiki.
There is no mechanical linter, so this is you re-reading the bundle against SCHEMA's quality
standards. Report anything you cannot fix:

- **Shape:** every page's frontmatter starts with `type`; no `wiki/` file name carries a date;
  every body link resolves to a file that exists inside `wiki/`.
- **Frontmatter:** every `sources` entry has a `resource`; `generated.by` and authors use the actor
  convention (`human:<id>`, `<producer>/<version>`); timestamps carry a UTC offset.
- **Citations:** every claim ends in a `[^<source-id>]` footnote; source-page claims use `[^raw]`.
- **Links:** every entity/concept/relationship page has at least one inbound link from another page.
- **Candidates:** anything with fewer than 3 mentions is listed in `index.md` only, with no page.

## Workflow 5 — Reformat pages

When a convention changes — a new template layout, a renamed section, a frontmatter tweak — re-apply
it by reading each affected page and rewriting it to match `references/page-templates.md`, preserving
its facts and citations. This is hand work on every page (the scripted `llm-wiki` automates the same
rewrites with `ingest --all`, and regenerates `index.md` with `index`). If you find yourself doing
this often across many pages, that is the signal to switch to `llm-wiki` (see below).

## Relationship to the full skill

This skill trades `llm-wiki`'s scripted automation (and its `lint` and `index` commands) for zero
setup. Both are stateless and both have the LLM write the pages, so the `wiki/` bundle is identical
in shape and you can move between them over the same bundle. See this folder's `README.md` for a
step-by-step guide and `../llm-wiki/README.md` for the scripted version.
