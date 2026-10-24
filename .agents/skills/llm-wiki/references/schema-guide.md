# LLM Wiki Guide

Detailed reference for page formats and conventions. See `wiki/SCHEMA.md` for the authoritative rules.

## Frontmatter by Page Type

All pages require `type` (always **first**), `title`, `description`, `tags`, and `generated`.
Every `sources` entry requires a `resource` field.

### Source: Required fields
`type`, `title`, `description`, `tags`, `generated`, `sources` (single entry with `id: "raw"`, `resource: "../../raw/<file>"`), `resource` (canonical URL of the article)

### Entity: Required fields
`type`, `title`, `description`, `tags`, `generated`, `sources`

### Concept: Required fields
`type`, `title`, `description`, `tags`, `generated`, `sources`

### Relationship: Required fields
`type`, `title`, `description`, `tags`, `generated`, `sources`, `relation`, `between`


## Naming Rules

Slugs are lowercase, hyphen-separated, ASCII. No date prefix ever appears in `wiki/` file names.

| Type | Folder | Pattern | Example |
|------|--------|---------|---------|
| Entity | `wiki/entities/` | `kebab-case.md` | `entities/atlan.md` |
| Concept | `wiki/concepts/` | `kebab-case.md` | `concepts/semantis-layer.md` |
| Source | `wiki/sources/` | `kebab-case.md` (raw name minus date prefix and extension) | `sources/some-article.md` |
| Relationship | `wiki/relationships/` | `a-vs-b.md` for comparisons; `a-<relation>-b.md` otherwise | `relationships/atlan-vs-semantido.md` |
| Overview | `wiki/overviews/` | `kebab-case.md` | `overviews/overview.md` |
| Raw (input only) | `raw/` | `YYYY-MM-DD-slug.ext` recommended; any name accepted | `raw/2026-04-09-some-article.md` |

## Log Entry Format

`log.md` groups entries under ISO `## YYYY-MM-DD` headings, newest first. Each entry is a single
bullet starting with a bold action word (`Ingest`, `Create`, `Prune`, `Query`, …).

```markdown
## 2026-10-24
- **Ingest**: <source-slug> — <what was read>
- **Create**: entity pages `<slug>`, `<slug>` (each ≥3 mentions)
- **Query**: "<question>" — pages referenced: `<concept-id>`, `<concept-id>`
```