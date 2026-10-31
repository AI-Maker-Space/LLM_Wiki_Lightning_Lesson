---
type: Relationship
title: "Semantics vs Ontology"
description: "Semantics (what something means) must precede ontology (how that knowledge is organised); the series inverts the common industry order and builds semantido's concept tier on it."
tags: ["semantics", "ontology"]
relation: compares
between: ["concepts/semantics", "concepts/ontology"]
generated: { by: "llm-wiki-dci/claude-opus-4-8", at: 2026-10-24T00:00:00Z }
sources:
  - id: "what-is-a-semantic-layer-after-all"
    resource: "../sources/what-is-a-semantic-layer-after-all.md"
    title: "What is a semantic layer after all?"
    author: "human:dragos-crintea"
    last_modified: 2026-02-06T00:00:00Z
  - id: "two-agents-walk-into-an-mcp-the-concept-registry-an-ontology-grade-rigor-at-sqlalchemy-decorator-cost-semantido-v0-4-1-release"
    resource: "../sources/two-agents-walk-into-an-mcp-the-concept-registry-an-ontology-grade-rigor-at-sqlalchemy-decorator-cost-semantido-v0-4-1-release.md"
    title: "Two agents walk into an mcp: the Concept Registry. Semantido v0.4.1 release."
    author: "human:dragos-crintea"
    last_modified: 2026-07-22T00:00:00Z
---

# Semantics vs Ontology

## Summary
The series' central ordering claim is that semantics must come before ontology: first define what a
thing means in a specific context, then build the ontology graph on top. The author argues the
industry tends to do the opposite — reaching for ontologies before meaning — which he considers
backwards.[^what-is-a-semantic-layer-after-all]

## Key Differences

| Dimension | [Semantics](../concepts/semantics.md) | [Ontology](../concepts/ontology.md) |
|---|---|---|
| Concern | What something *means* in context[^what-is-a-semantic-layer-after-all] | How knowledge is *organised* once meaning is known[^what-is-a-semantic-layer-after-all] |
| Order | Comes first[^what-is-a-semantic-layer-after-all] | Built on top of semantics[^what-is-a-semantic-layer-after-all] |
| In semantido | Descriptions, synonyms, context on the schema[^two-agents-walk-into-an-mcp-the-concept-registry-an-ontology-grade-rigor-at-sqlalchemy-decorator-cost-semantido-v0-4-1-release] | The concept registry — minimal, referential, no OWL/reasoner[^two-agents-walk-into-an-mcp-the-concept-registry-an-ontology-grade-rigor-at-sqlalchemy-decorator-cost-semantido-v0-4-1-release] |

## Tradeoffs
- Building ontology before meaning risks organising knowledge you have not actually defined — the error the series warns against.[^what-is-a-semantic-layer-after-all]
- The concept registry shows how little ontology is needed in practice: typed edges, version pins and hierarchy, rather than a full reasoner.[^two-agents-walk-into-an-mcp-the-concept-registry-an-ontology-grade-rigor-at-sqlalchemy-decorator-cost-semantido-v0-4-1-release]

## Evidence
- "Semantics must come before ontology. First define what something means in a specific context, then build the ontology."[^what-is-a-semantic-layer-after-all]
- The concept registry is positioned explicitly on the "semantics → ontologies" continuum as the next tier up.[^two-agents-walk-into-an-mcp-the-concept-registry-an-ontology-grade-rigor-at-sqlalchemy-decorator-cost-semantido-v0-4-1-release]

## Related
- [Semantics](../concepts/semantics.md) — what must come first
- [Ontology](../concepts/ontology.md) — what is built on top
- [Semantic layer](../concepts/semantic-layer.md) — the layer that carries both tiers

## Source History
- [what-is-a-semantic-layer-after-all](../sources/what-is-a-semantic-layer-after-all.md) — the ordering claim and definitions
- [two-agents-walk-into-an-mcp-the-concept-registry-an-ontology-grade-rigor-at-sqlalchemy-decorator-cost-semantido-v0-4-1-release](../sources/two-agents-walk-into-an-mcp-the-concept-registry-an-ontology-grade-rigor-at-sqlalchemy-decorator-cost-semantido-v0-4-1-release.md) — the minimal-ontology concept registry

[^what-is-a-semantic-layer-after-all]: What is a semantic layer after all?. Dragos Crintea. 2026-02-06.
[^two-agents-walk-into-an-mcp-the-concept-registry-an-ontology-grade-rigor-at-sqlalchemy-decorator-cost-semantido-v0-4-1-release]: Two agents walk into an mcp: the Concept Registry, an ontology-grade rigor at SQLAlchemy-decorator cost. Semantido v0.4.1 release.. Dragos Crintea. 2026-07-22.
