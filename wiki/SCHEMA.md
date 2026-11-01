# Wiki Schema

_Conventions governing this LLM Wiki. The tools include this file in every LLM prompt; agents read
it before any wiki operation._

## Purpose and Scope

This wiki accumulates **external knowledge only**: articles, papers, research, industry developments and technical concepts.

## Architecture

Karpathy's split between untouched sources and compiled knowledge. The compiled half is an [Open Knowledge Format](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md) bundle conforming to **OKF v0.2** only,
with no superseded fields and no body citation lists.

1. **Raw sources** (`../raw`) are immutable. The LLM or agent reads them and never edits, renames or deletes them.
2. **The compiled wiki** (`wiki/`) LLM generated and maintained Markdown organized by type.
3. **This schema** governs structure, naming and workflows.

## Page Types

OKF has no fixed type taxonomy, so these folders and `type` values are this wiki's choice.

| `type` | Folder | Holds | Body sections |
|---|---|---|---|
| `Source` | `sources` | one summary per raw file | Summary, Key Claims, Entities Mentioned, Concepts Covered, Notable Quotes, Notes |
| `Entity` | `entities` | people, companies, projects, tools (subtype is the first tag) | Overview, Key Facts, Relevance, Related |
| `Concept` | `concepts` | techniques, patterns, ideas | Definition, How It Works, Key Points, Applications, Related Concepts |
| `Relationship` | `relationships` | how two entities or concepts relate, including comparisons | Summary, Key Differences, When to Use Each, Tradeoffs, Evidence, Related |
| `Overview` | `overviews` | high-level synthesis | Big Picture, Key Concepts, Key Entities, Relationships, Recent Developments, Open Questions and Contradictions |

OKF rules applied: one concept per file; the **concept ID is the path inside `wiki/` without
`.md`** (`entities/<slug>`); `index.md` and `log.md` are reserved names and never concepts.

## Frontmatter (OKF v0.2 §4–§5)

Each wiki page must have frontmatter at the top of the file, in YAML format. The frontmatter
defines the type of the page, its title, description, tags, and other metadata. The frontmatter
is required for all wiki pages.

```yaml
---
type: Entity                                    # REQUIRED, always first
title: "<Display Name>"
description: "<One sentence.>"
tags: ["company"]
generated: { by: "llm-wiki/<model>", at: 2026-01-01T00:00:00Z }
status: draft                                   # optional; absent means stable
sources:
  - id: "<source-slug>"                         # footnote key
    resource: "../sources/<source-slug>.md"     # REQUIRED in every entry
    title: "<Source title>"
    author: "human:<author-id>"                 # actor convention
    last_modified: 2026-01-01T00:00:00Z
---
```

- **Datetime:** every timestamp-valued key is ISO 8601 with an explicit UTC offset. Plain dates are
  not used in frontmatter.
- **Freshness** is `generated.at`, the last meaningful change to the content. It never goes in a file name.
- **Actors** (§7):
  - `<producer>/<version>` for tools;
  - `human:<id>` for people;
  - `process:<id>` for automated checks;
- **Trust tiers** (§5.3):
  - no `verified` means unverified;
  - only non-human actors means machine-confirmed;
  - any `human:` actor means human-reviewed.
  Pages start unverified;
- **Lifecycle** (§5.4): `status` is written only when it is `draft` or `deprecated`.
- **Source pages** add `resource`, the article's canonical URL. Their single `sources` entry
  (`id: "raw"`) points at `../../raw/<file>`.
- **Relationship pages** add the producer keys `relation` (compares, builds-on, uses, competes-with,
  part-of, acquires, supersedes, other) and `between: [<id-a>, <id-b>]`.

## Naming

- **raw/** recommended form: `YYYY-MM-DD-slug.ext`, using the publication or capture date. Any file
  name is accepted.
  - **Date resolution:** the date comes from the file-name prefix, else front matter
    (`publication_date`, `date` or `last_modified`; YAML `---` or TOML `+++`), else the file's
    modification time.
  - **Flat folder:** `../raw` is read flat, so files in subfolders are ignored and lint reports them.
  - **Text formats only:** .md, .txt, .html, .json, .csv, .xml, .rst, .yaml. Convert other formats
    to Markdown first.
  - **Decide names before the first ingest.** A raw name (minus any date prefix) becomes its source
    ID, so renaming a raw file later counts as a withdrawal plus a new source.
- **wiki/:** `slug.md` only, never a date prefix. The path is a stable concept ID.
- **Source pages:** the raw name without date prefix and extension. On a clash, a `-2` suffix is
  assigned (checked against the source pages that already exist in `wiki/sources/`).
- **Relationships:** `a-vs-b` for comparisons, `a-<relation>-b` otherwise.
- **Slugs:** lowercase, hyphen-separated, ASCII.

## Links and Attribution (OKF v0.2 §5.1, §6)

- **Links between pages** are ordinary relative Markdown links inside the bundle
  (`[Name](../entities/<slug>.md)`). They never leave `wiki/`; raw files are referenced only
  through `sources[].resource`.
- **Provenance lives in frontmatter `sources`.** Each claim ends with a footnote keyed to a
  `sources[].id` (`...claim.[^<source-slug>]`), and the footnote definitions sit at the end of the
  page. On source pages, claims and quotes carry `[^raw]`.
- **Cross-references are bidirectional.**

## When to Create vs Update Pages

- **Create** an entity or concept page once it has **3+ mentions** across wiki pages (source
  summaries and relationships). Until then, it is a *candidate*: named in source summaries and
  listed in `index.md`, with no page.
- **Update** an existing page when a new source adds to it. When in doubt, update rather than create.
- **Create a relationship page** only when a source makes an explicit claim about how two things
  relate.

## Ingest Order

Sequential, oldest first:

1. Save the raw source to `../raw`.
2. Read the raw source fully.
3. Write the source summary in `sources`.
4. THEN create or update entity, concept and relationship pages **by reading the source summary**.

Facts are stored as `(text, source id, date)`, which keeps the citation chain intact and pruning exact.

## Revisions and Withdrawals

- **Raw file re-saved with changes:** re-ingest it; its facts are removed and re-extracted.
- **Raw file removed:** prune it. Its summary and facts are retracted, empty pages are deleted, and
  the remaining prose is refreshed.
- **A newer source revises a figure:** keep both facts, newest first, and mark the older one
  *superseded by* the newer source.
- **A raw file without a date prefix:** warn and suggest a dated name; never rename it automatically.

## Log (OKF v0.2 §9)

`log.md` groups entries under ISO `## YYYY-MM-DD` headings, newest first. Each entry is one bullet
starting with a bold word (`* **Ingest**: ...`).

## Quality Standards

- **Shape:** every page has `type`; no wiki file name carries a date; every body link resolves inside `wiki/`.
- **Frontmatter:** every `sources` entry has a `resource`; authors and `generated.by` are actors; datetime carry offsets;
- **Citations:** every claim cites a source.
- **Links:** every page except sources and overviews has an inbound link.
- **Authored pages:** pages are written by the LLM following the templates; `index.md` is
  regenerated by scanning the pages and `log.md` is appended, so edit those two through the tooling.
- **Overview:** updated when a source materially changes the big picture.
