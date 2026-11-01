---
type: Source
title: "Two agents walk into an mcp: the Concept Registry, an ontology-grade rigor at SQLAlchemy-decorator cost. Semantido v0.4.1 release."
description: "semantido v0.4.1 adds a concept registry — three families of typed edges that let two agents who never shared a schema disagree safely about what a word means, with no OWL and no reasoner."
tags: ["semantido", "ontology", "release"]
generated: { by: "llm-wiki-lite/1.0", at: 2026-10-24T00:00:00Z }
resource: "https://dragoscrintea.me/articles/05-concept-registry-a-ontology-grade-rigor-at-sqlalchemy-decorator-cost"
sources:
  - id: "raw"
    resource: "../../raw/Two agents walk into an mcp_ the Concept Registry, an ontology-grade rigor at SQLAlchemy-decorator cost. Semantido v0.4.1 release..md"
    title: "Two agents walk into an mcp: the Concept Registry, an ontology-grade rigor at SQLAlchemy-decorator cost. Semantido v0.4.1 release."
    author: "human:dragos-crintea"
    last_modified: 2026-07-22T00:00:00Z
---

# Two agents walk into an mcp: the Concept Registry, ontology-grade rigor at SQLAlchemy-decorator cost. Semantido v0.4.1 release.

## Summary
v0.4.1 adds a concept registry: the tier where meaning becomes a first-class object, sitting on the
semantics → ontology continuum. It is deliberately not an ontology engine — no OWL, no reasoner, no
RDF triple store — and tests how little ontological structure is actually needed for two agents that
never shared a schema to interoperate without silently conflating meanings.[^raw]

The worked experiment is two banks: one on an EMIR reporting stack, one on MiFIR, with no shared ids,
schemas or vocabulary. What they share only incidentally is outward mappings to public anchors — FIBO,
ISO 20022, GLEIF. A ~100-line, three-rule protocol computes alignments from those mappings alone: the
EMIR and MiFIR "counterparty" both declare themselves narrower than the same FIBO concept, so the
sibling rule fires and the receiving agent refuses to substitute (RELATED_NOT_SUBSTITUTABLE) with an
auditable reason; amounts sharing an ISO 20022 anchor flow through; an unmapped concept yields NO_BRIDGE
and a clarifying question. The design goal is to convert silent substitution errors into inspectable
refusals.[^raw]

Mechanically, a `ConceptRegistry` holds `Concept` nodes (id, label, required definition, synonyms) with
three families of edges: concept-to-concept (SAME_AS, BROADER/NARROWER, RELATED, DISTINCT_FROM),
concept-to-external (version-pinned SKOS mappings such as `fibo@2025Q3`), and concept-to-physical
(`@semantic_table(concept=…)` validated at sync time, the same moment `time_dimension` is checked). The
Markdown exporter gains Concepts and Disambiguation sections so an agent resolves by concept id, never
by a colliding label.[^raw]

## Key Claims
- v0.4.1 ships a concept registry: three families of typed edges, no OWL, no reasoner, ~100 lines of protocol.[^raw]
- The experiment: two banks (EMIR and MiFIR) that share no ids or schemas interoperate using only their outward mappings to public anchors (FIBO, ISO 20022, GLEIF).[^raw]
- The EMIR and MiFIR "counterparty" are siblings — both narrower than the same FIBO concept — so the protocol refuses to substitute them (RELATED_NOT_SUBSTITUTABLE) with an audit reason.[^raw]
- Interop came from typed mapping relations, version pins, and hierarchy declarations — not from a reasoner or a merged ontology.[^raw]
- A `Concept` has an id, label, required definition, and synonyms, plus concept-to-concept, concept-to-external (SKOS), and concept-to-physical edges.[^raw]
- Every external mapping names a version-pinned source (e.g. `fibo@2025Q3`) and a SKOS relation (exact/close/narrow/broad/related match).[^raw]
- Concept-to-physical bindings are validated at sync time, so a typo'd concept id fails the build, not the agent's answer.[^raw]
- The Markdown exporter gains Concepts and Disambiguation sections so agents resolve by concept id, never by a colliding label.[^raw]

## Entities Mentioned
- [Dragos Crintea](../entities/dragos-crintea.md) — author
- [semantido](../entities/semantido.md) — the subject of the release
- [SQLAlchemy](../entities/sqlalchemy.md) — the decorator surface the registry reuses
- [MCP](../entities/mcp.md) — the setting ("two agents walk into an MCP"); claims are one MCP call away
- [Hikari Labs](../entities/hikari-labs.md) — the author's company and advisory
- **FIBO**, **ISO 20022**, **GLEIF** (`entities/fibo`, `entities/iso-20022`, `entities/gleif`) — the public anchors the alignment relies on (candidates)

## Concepts Covered
- [Ontology](../concepts/ontology.md) — "how much ontology do I need?"; the registry is the minimal answer
- [Semantic drift](../concepts/semantic-drift.md) — bindings validated at sync so a typo fails the build, not the answer
- [Semantic layer](../concepts/semantic-layer.md) — the concept tier extends the layer upward
- **Concept registry** (`concepts/concept-registry`) — the release's headline feature (candidate)

## Notable Quotes
> "ontology-grade rigor at SQLAlchemy-decorator cost"
— The author, the pitch for the concept registry

> "Typed mapping relations, version pins, and hierarchy declarations were enough to turn silent substitution errors into inspectable, auditable refusals."
— The author, on what did the work

## Notes
- Fifth in the series; the EMIR/MiFIR counterparty homonym recurs as the flagship case for `semantido.lint` in v0.5.
- The alignment protocol lives in `examples/04_federated_agents` and is a reference pattern, not yet a shipped feature.

[^raw]: Two agents walk into an mcp: the Concept Registry, an ontology-grade rigor at SQLAlchemy-decorator cost. Semantido v0.4.1 release.. Dragos Crintea. 2026-07-22.
