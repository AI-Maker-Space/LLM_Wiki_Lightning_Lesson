---
type: Source
title: "Semantics where the code lives. Interchange where the stack lives. Semantido v0.3.0 release."
description: "semantido v0.3.0 ships a first-class time-dimension model and a three-format exporter (OSI YAML, Markdown, JSON), arguing the curation a format carries — not the format — is the product."
tags: ["semantido", "semantic-layer", "release"]
generated: { by: "llm-wiki-lite/1.0", at: 2026-10-24T00:00:00Z }
resource: "https://dragoscrintea.me/articles/04-semantics-where-the-code-lives-interchange-where-the-stack-lives"
sources:
  - id: "raw"
    resource: "../../raw/Semantics where the code lives. Interchange where the stack lives. Semantido v0.3.0 release..md"
    title: "Semantics where the code lives. Interchange where the stack lives. Semantido v0.3.0 release."
    author: "human:dragos-crintea"
    last_modified: 2026-07-10T00:00:00Z
---

# Semantics where the code lives. Interchange where the stack lives. Semantido v0.3.0 release.

## Summary
The v0.3.0 release post pairs two features — a first-class time-dimension model and a rebuilt
exporters module — and argues they belong together: the time model is the *curation* that makes a
schema agent-friendly, and the exporters are how that curation reaches every consumer. semantido is
positioned as the authoring layer (semantics written in Python on SQLAlchemy models, versioned in the
same pull request as the schema), with Open Semantic Interchange (OSI) as the interchange layer it now
exports natively.[^raw]

The article's thesis is that the value of a semantic layer is not the format but the curation the
format carries. On a synthetic core-banking table with five temporal columns, a curated `is_time`
policy collapses eight naively-flagged "time axes" to one primary axis with its grain, dropping audit
timestamps with an explicit "do not use as a time axis" instruction. Declaring the primary axis at
table level is validated against the physical schema at sync time: a typo'd or non-temporal axis fails
immediately rather than drifting downstream.[^raw]

A serialization analysis shows the industry's interchange standard (OSI) carries *less* information
than a plain Markdown export — no data types, no grain, no way to name a primary axis — while costing
~2.2× the tokens as prompt context (≈1,719 vs ≈780). The conclusion is "serialize per consumer":
token-lean Markdown into the context window, structured YAML into the toolchain, and a live MCP server
for tool access — all from one synchronized source of truth.[^raw]

## Key Claims
- semantido v0.3.0 ships a first-class time-dimension model (primary axis per table, secondary axes per column, a `TimeGrain` enum) and a rebuilt exporters module.[^raw]
- The exporters serialize one synchronized semantic layer three ways: OSI YAML for interchange, Markdown for LLM prompt context, and JSON for programs.[^raw]
- A declared time axis is validated against the physical schema at sync time; a missing, non-temporal, or over-fine axis fails or warns immediately.[^raw]
- On a synthetic banking model, a curated policy reduces eight naively-flagged time columns to one PRIMARY axis and drops audit columns with an explicit exclusion instruction.[^raw]
- An agent-friendly environment needs three query-time guarantees: disambiguation, defaults/conventions, and guardrails — none of which live in the physical schema.[^raw]
- The Markdown export is ~780 tokens vs OSI YAML's ~1,719 — a ~2.2× difference for the same layer — and OSI loses data types that Markdown keeps.[^raw]
- semantido is the authoring layer (Python on SQLAlchemy models); OSI is the vendor-neutral interchange layer, and v0.3.0 targets OSI v0.2.0.[^raw]
- An agent consumes the layer three ways — context (Markdown), interchange (OSI import), and live tools (an MCP server over the layer).[^raw]

## Entities Mentioned
- [Dragos Crintea](../entities/dragos-crintea.md) — author
- [semantido](../entities/semantido.md) — the subject of the release
- [SQLAlchemy](../entities/sqlalchemy.md) — the models semantics are authored on
- [MCP](../entities/mcp.md) — the third consumption path (a live server over the layer)
- [Hikari Labs](../entities/hikari-labs.md) — the author's company and advisory
- **Open Semantic Interchange (OSI)** (`entities/osi`) — the vendor-neutral format semantido exports natively (candidate)

## Concepts Covered
- [Semantic layer](../concepts/semantic-layer.md) — curation as the product; three serializations
- [Semantic drift](../concepts/semantic-drift.md) — "semantics that drift from the schema are bugs," caught at sync time
- [Text2SQL](../concepts/text2sql.md) — the text-to-SQL probe used to score serializations
- [Hallucination](../concepts/hallucination.md) — the failure the curation aims to reduce
- **Time dimension** (`concepts/time-dimension`) and **TimeGrain** (`concepts/grain`) — the v0.3 curation primitives (candidates)

## Notable Quotes
> "The value of a semantic layer is not in the format, it's in the curation the format carries."
— The author, stating the release's thesis

> "semantics that drift from the schema are bugs, and bugs should surface at semantic layer creation, not in a consumer's SQL three tools downstream."
— The author, on validating semantics at sync time

## Notes
- Fourth in the series and the first release post; begins the "author where the code lives, interchange where the stack lives" theme that v0.4.1 and v0.5 extend.
- Introduces OSI and `grain`/time-dimension as candidates; grain becomes central in `sources/the-semantic-layer-can-now-fail-your-build-semantido-v0-5-release`.

[^raw]: Semantics where the code lives. Interchange where the stack lives. Semantido v0.3.0 release.. Dragos Crintea. 2026-07-10.
