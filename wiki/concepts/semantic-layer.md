---
type: Concept
title: "Semantic layer"
description: "A layer of curated, governed metadata that translates between the real-world meaning of business data and an LLM's statistical 'understanding', raising retrieval and query accuracy."
tags: ["semantic-layer", "genai"]
generated: { by: "llm-wiki-dci/claude-opus-4-8", at: 2026-10-24T00:00:00Z }
sources:
  - id: "where-it-all-started-why-building-a-semantic-layer-for-genai"
    resource: "../sources/where-it-all-started-why-building-a-semantic-layer-for-genai.md"
    title: "Where it all started. Why Building a semantic layer for GenAI."
    author: "human:dragos-crintea"
    last_modified: 2026-01-16T00:00:00Z
  - id: "what-is-a-semantic-layer-after-all"
    resource: "../sources/what-is-a-semantic-layer-after-all.md"
    title: "What is a semantic layer after all?"
    author: "human:dragos-crintea"
    last_modified: 2026-02-06T00:00:00Z
  - id: "the-semantic-layer-landscape-what-you-need-to-know-before-choosing-one"
    resource: "../sources/the-semantic-layer-landscape-what-you-need-to-know-before-choosing-one.md"
    title: "The Semantic Layer landscape, what you need to know before choosing one."
    author: "human:dragos-crintea"
    last_modified: 2026-05-17T00:00:00Z
  - id: "semantics-where-the-code-lives-interchange-where-the-stack-lives-semantido-v0-3-0-release"
    resource: "../sources/semantics-where-the-code-lives-interchange-where-the-stack-lives-semantido-v0-3-0-release.md"
    title: "Semantics where the code lives. Interchange where the stack lives. Semantido v0.3.0 release."
    author: "human:dragos-crintea"
    last_modified: 2026-07-10T00:00:00Z
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

# Semantic layer

## Definition
A semantic layer is a body of curated, governed metadata that translates between the actual meaning of
business workflows and the data they produce, and the "understanding" an LLM gained from training.[^what-is-a-semantic-layer-after-all]
The series argues the term has been overloaded by marketing, but in its useful sense it supplies the
meaning and relationships that neither the physical schema nor the model's training make explicit.[^what-is-a-semantic-layer-after-all]

## How It Works
Meaning is declared as metadata — descriptions, synonyms, relationships, a primary time axis and grain,
and typed concepts — attached to the schema, then serialized for whoever consumes it: token-lean
Markdown for a model's context window, structured YAML (OSI) for the tool ecosystem, and a live MCP
service for agents querying at plan time.[^semantics-where-the-code-lives-interchange-where-the-stack-lives-semantido-v0-3-0-release]
The value is not the format but the curation the format carries; in [semantido](../entities/semantido.md)
that curation is authored next to the code and, from v0.5, enforced so the layer can fail a build.[^semantics-where-the-code-lives-interchange-where-the-stack-lives-semantido-v0-3-0-release][^the-semantic-layer-can-now-fail-your-build-semantido-v0-5-release]

## Key Points
- Adding table semantics to an LLM's context prompt improved SQL generation by orders of magnitude in the author's first experiments.[^where-it-all-started-why-building-a-semantic-layer-for-genai]
- Natural-language query accuracy is ~40% without a semantic layer and 80%+ with one.[^the-semantic-layer-landscape-what-you-need-to-know-before-choosing-one]
- Once a BI nice-to-have, it is now a non-negotiable requirement that demands a metadata architecture optimised for LLM consumption.[^what-is-a-semantic-layer-after-all]
- The real procurement decision is governance vs. flexibility, and whether a vendor sells a definition system or a description system — only definition systems solve the problem.[^the-semantic-layer-landscape-what-you-need-to-know-before-choosing-one]
- The curation is the product; the serialization formats are only how it ships.[^semantics-where-the-code-lives-interchange-where-the-stack-lives-semantido-v0-3-0-release]
- A layer that only advises is documentation, which drifts; enforcement turns it into an artifact that can fail CI.[^the-semantic-layer-can-now-fail-your-build-semantido-v0-5-release]

## Applications
Semantic layers underpin Text2SQL and agentic analytics, and are built in several vendor styles —
BI-native, headless, transformation-native, warehouse-native, open-standard and application-native.[^the-semantic-layer-landscape-what-you-need-to-know-before-choosing-one]
The concept tier extends upward into a concept registry so agents that never shared a schema can
interoperate.[^two-agents-walk-into-an-mcp-the-concept-registry-an-ontology-grade-rigor-at-sqlalchemy-decorator-cost-semantido-v0-4-1-release]

## Related Concepts
- [Text2SQL](text2sql.md) — the task a semantic layer most directly improves ([semantic layer improves Text2SQL](../relationships/semantic-layer-improves-text2sql.md))
- [Semantics](semantics.md) — the study of meaning the layer operationalises
- [Semantic drift](semantic-drift.md) — the failure a good layer prevents
- [Ontology](ontology.md) — the tier built on top of the layer's semantics

## Source History
- [where-it-all-started-why-building-a-semantic-layer-for-genai](../sources/where-it-all-started-why-building-a-semantic-layer-for-genai.md) — origin: semantics improve SQL generation
- [what-is-a-semantic-layer-after-all](../sources/what-is-a-semantic-layer-after-all.md) — definition and LLM-ready metadata
- [the-semantic-layer-landscape-what-you-need-to-know-before-choosing-one](../sources/the-semantic-layer-landscape-what-you-need-to-know-before-choosing-one.md) — accuracy figures and vendor categories
- [semantics-where-the-code-lives-interchange-where-the-stack-lives-semantido-v0-3-0-release](../sources/semantics-where-the-code-lives-interchange-where-the-stack-lives-semantido-v0-3-0-release.md) — curation and per-consumer serialization
- [two-agents-walk-into-an-mcp-the-concept-registry-an-ontology-grade-rigor-at-sqlalchemy-decorator-cost-semantido-v0-4-1-release](../sources/two-agents-walk-into-an-mcp-the-concept-registry-an-ontology-grade-rigor-at-sqlalchemy-decorator-cost-semantido-v0-4-1-release.md) — concept tier
- [the-semantic-layer-can-now-fail-your-build-semantido-v0-5-release](../sources/the-semantic-layer-can-now-fail-your-build-semantido-v0-5-release.md) — enforcement

[^where-it-all-started-why-building-a-semantic-layer-for-genai]: Where it all started. Why Building a semantic layer for GenAI.. Dragos Crintea. 2026-01-16.
[^what-is-a-semantic-layer-after-all]: What is a semantic layer after all?. Dragos Crintea. 2026-02-06.
[^the-semantic-layer-landscape-what-you-need-to-know-before-choosing-one]: The Semantic Layer landscape, what you need to know before choosing one.. Dragos Crintea. 2026-05-17.
[^semantics-where-the-code-lives-interchange-where-the-stack-lives-semantido-v0-3-0-release]: Semantics where the code lives. Interchange where the stack lives. Semantido v0.3.0 release.. Dragos Crintea. 2026-07-10.
[^two-agents-walk-into-an-mcp-the-concept-registry-an-ontology-grade-rigor-at-sqlalchemy-decorator-cost-semantido-v0-4-1-release]: Two agents walk into an mcp: the Concept Registry, an ontology-grade rigor at SQLAlchemy-decorator cost. Semantido v0.4.1 release.. Dragos Crintea. 2026-07-22.
[^the-semantic-layer-can-now-fail-your-build-semantido-v0-5-release]: The semantic layer can now fail your build - semantido v0.5 release.. Dragos Crintea. 2026-08-28.
