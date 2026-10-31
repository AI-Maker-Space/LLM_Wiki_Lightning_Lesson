---
type: Concept
title: "Ontology"
description: "The organisation and classification of knowledge once its meaning is known; the series asks how little of it is needed, and semantido's concept registry is a minimal, reasoner-free answer."
tags: ["ontology", "semantics"]
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
  - id: "the-semantic-layer-can-now-fail-your-build-semantido-v0-5-release"
    resource: "../sources/the-semantic-layer-can-now-fail-your-build-semantido-v0-5-release.md"
    title: "The semantic layer can now fail your build - semantido v0.5 release."
    author: "human:dragos-crintea"
    last_modified: 2026-08-28T00:00:00Z
---

# Ontology

## Definition
Ontology is the branch of metaphysics dealing with the structure of systems, now associated with the
organisation and classification of knowledge. It is closely related to semantics, the distinction
being that ontology organises knowledge *once you know what it means*, while semantics concerns what
something means in the first place.[^what-is-a-semantic-layer-after-all]

## How It Works
Because meaning must precede organisation, an ontology is built on top of a semantic foundation.[^what-is-a-semantic-layer-after-all]
The series then asks a practical question — how little ontology is actually needed for two agents to
interoperate — and answers it with semantido's concept registry: not an ontology engine (no OWL, no
reasoner, no triple store) but typed concept-to-concept edges, version-pinned external mappings, and
hierarchy declarations, validated referentially.[^two-agents-walk-into-an-mcp-the-concept-registry-an-ontology-grade-rigor-at-sqlalchemy-decorator-cost-semantido-v0-4-1-release]

## Key Points
- Semantics comes before ontology: define meaning in context, then build the ontology on top.[^what-is-a-semantic-layer-after-all]
- The concept registry is positioned on the "semantics → ontologies" continuum as the concept tier of the layer.[^two-agents-walk-into-an-mcp-the-concept-registry-an-ontology-grade-rigor-at-sqlalchemy-decorator-cost-semantido-v0-4-1-release]
- Minimal structure — typed mapping relations, version pins, hierarchy — was enough to let two agents disagree safely without a reasoner or merged ontology.[^two-agents-walk-into-an-mcp-the-concept-registry-an-ontology-grade-rigor-at-sqlalchemy-decorator-cost-semantido-v0-4-1-release]
- v0.5's `grain` and linter enforce the concept tier, catching DISTINCT_FROM and contradictory-mapping errors a reasoner would otherwise be needed for.[^the-semantic-layer-can-now-fail-your-build-semantido-v0-5-release]

## Applications
The concept registry delivers "ontology-grade rigor at SQLAlchemy-decorator cost," enabling federated
agents to align on meaning through shared public anchors (FIBO, ISO 20022, GLEIF) without a merged
ontology.[^two-agents-walk-into-an-mcp-the-concept-registry-an-ontology-grade-rigor-at-sqlalchemy-decorator-cost-semantido-v0-4-1-release]

## Related Concepts
- [Semantics](semantics.md) — what must come first ([semantics vs ontology](../relationships/semantics-vs-ontology.md))
- [Semantic layer](semantic-layer.md) — the foundation the concept tier extends
- [Semantic drift](semantic-drift.md) — what enforcing the concept tier prevents

## Source History
- [what-is-a-semantic-layer-after-all](../sources/what-is-a-semantic-layer-after-all.md) — ontology vs. semantics and the ordering
- [two-agents-walk-into-an-mcp-the-concept-registry-an-ontology-grade-rigor-at-sqlalchemy-decorator-cost-semantido-v0-4-1-release](../sources/two-agents-walk-into-an-mcp-the-concept-registry-an-ontology-grade-rigor-at-sqlalchemy-decorator-cost-semantido-v0-4-1-release.md) — the minimal concept registry
- [the-semantic-layer-can-now-fail-your-build-semantido-v0-5-release](../sources/the-semantic-layer-can-now-fail-your-build-semantido-v0-5-release.md) — enforcing the concept tier

[^what-is-a-semantic-layer-after-all]: What is a semantic layer after all?. Dragos Crintea. 2026-02-06.
[^two-agents-walk-into-an-mcp-the-concept-registry-an-ontology-grade-rigor-at-sqlalchemy-decorator-cost-semantido-v0-4-1-release]: Two agents walk into an mcp: the Concept Registry, an ontology-grade rigor at SQLAlchemy-decorator cost. Semantido v0.4.1 release.. Dragos Crintea. 2026-07-22.
[^the-semantic-layer-can-now-fail-your-build-semantido-v0-5-release]: The semantic layer can now fail your build - semantido v0.5 release.. Dragos Crintea. 2026-08-28.
