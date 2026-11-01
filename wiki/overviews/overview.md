---
type: Overview
title: "Overview"
description: "A high-level synthesis of Dragos Crintea's semantic-layer-for-GenAI series and the semantido releases it documents."
tags: ["overview", "semantic-layer"]
generated: { by: "llm-wiki-lite/1.0", at: 2026-10-24T00:00:00Z }
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

# Overview

## Big Picture
This wiki is compiled from Dragos Crintea's 2026 article series on building a semantic layer for the
GenAI era, and from the release notes of [semantido](../entities/semantido.md), the open-source,
application-native semantic layer he builds at [Hikari Labs](../entities/hikari-labs.md). The through
argument is simple and consistent: LLMs only approximate meaning statistically, so on business data —
especially tabular data — they misinterpret and [hallucinate](../concepts/hallucination.md) unless the
missing [semantics](../concepts/semantics.md) are made explicit. A [semantic layer](../concepts/semantic-layer.md)
supplies that meaning, turning brittle [Text2SQL](../concepts/text2sql.md) into a reliable capability —
the series cites natural-language accuracy rising from ~40% to 80%+ once a layer is in place.[^where-it-all-started-why-building-a-semantic-layer-for-genai][^the-semantic-layer-landscape-what-you-need-to-know-before-choosing-one]

The series moves from *why* to *how to choose* to *how to build*. It first disambiguates an overloaded
term and argues meaning must precede ontology[^what-is-a-semantic-layer-after-all]; then maps six
vendor categories and reframes the real decision as governance vs. flexibility — and ultimately whether
a vendor sells a *definition system* or a *description system*, the latter being one that
[drifts](../concepts/semantic-drift.md).[^the-semantic-layer-landscape-what-you-need-to-know-before-choosing-one]
semantido's answer is to author meaning as decorators on [SQLAlchemy](../entities/sqlalchemy.md) models
so it lives in the same file, review and deployment as the schema, and to expose it per consumer —
Markdown for context, OSI for tools, and a live [MCP](../entities/mcp.md) service for agents.[^semantics-where-the-code-lives-interchange-where-the-stack-lives-semantido-v0-3-0-release]

The release arc then hardens that idea: v0.3 adds a first-class time dimension and exporters, v0.4.1
adds a concept registry that lets agents who never shared a schema disagree safely without a reasoner,
and v0.5 turns the layer from a descriptor into an enforcer — `grain`, a groundings document, and
`semantido.lint`, whose errors fail CI.[^semantics-where-the-code-lives-interchange-where-the-stack-lives-semantido-v0-3-0-release][^two-agents-walk-into-an-mcp-the-concept-registry-an-ontology-grade-rigor-at-sqlalchemy-decorator-cost-semantido-v0-4-1-release][^the-semantic-layer-can-now-fail-your-build-semantido-v0-5-release]

## Key Concepts
- [Semantic layer](../concepts/semantic-layer.md)
- [Text2SQL](../concepts/text2sql.md)
- [Semantics](../concepts/semantics.md)
- [Hallucination](../concepts/hallucination.md)
- [Ontology](../concepts/ontology.md)
- [Semantic drift](../concepts/semantic-drift.md)

## Key Entities
- [semantido](../entities/semantido.md)
- [Dragos Crintea](../entities/dragos-crintea.md)
- [Hikari Labs](../entities/hikari-labs.md)
- [SQLAlchemy](../entities/sqlalchemy.md)
- [MCP](../entities/mcp.md)

## Relationships
- [Semantics vs Ontology](../relationships/semantics-vs-ontology.md)
- [Semantic layer improves Text2SQL](../relationships/semantic-layer-improves-text2sql.md)
- [semantido builds on SQLAlchemy](../relationships/semantido-builds-on-sqlalchemy.md)
- [semantido uses MCP](../relationships/semantido-uses-mcp.md)

## Recent Developments
- The latest source (v0.5, 2026-08-28) makes the layer enforceable: `semantido.lint` can fail a build, with an external-source-authority guardrail promised for v0.6.[^the-semantic-layer-can-now-fail-your-build-semantido-v0-5-release]

## Open Questions and Contradictions
- Whether the concept registry's minimal structure generalises beyond the one EMIR/MiFIR schema pair with incidentally-shared public anchors is explicitly posed as open.[^two-agents-walk-into-an-mcp-the-concept-registry-an-ontology-grade-rigor-at-sqlalchemy-decorator-cost-semantido-v0-4-1-release]
- The series backs the industry's OSI interchange standard yet shows it carries less information than a plain Markdown export (no data types, grain or primary axis) at ~2.2× the tokens — an unresolved tension between adopting OSI and pushing to fix it.[^semantics-where-the-code-lives-interchange-where-the-stack-lives-semantido-v0-3-0-release]
- Enforcement catches only the contradictions the author was disciplined enough to declare: a quiet linter may mean a clean layer or an under-specified one.[^the-semantic-layer-can-now-fail-your-build-semantido-v0-5-release]

[^where-it-all-started-why-building-a-semantic-layer-for-genai]: Where it all started. Why Building a semantic layer for GenAI.. Dragos Crintea. 2026-01-16.
[^what-is-a-semantic-layer-after-all]: What is a semantic layer after all?. Dragos Crintea. 2026-02-06.
[^the-semantic-layer-landscape-what-you-need-to-know-before-choosing-one]: The Semantic Layer landscape, what you need to know before choosing one.. Dragos Crintea. 2026-05-17.
[^semantics-where-the-code-lives-interchange-where-the-stack-lives-semantido-v0-3-0-release]: Semantics where the code lives. Interchange where the stack lives. Semantido v0.3.0 release.. Dragos Crintea. 2026-07-10.
[^two-agents-walk-into-an-mcp-the-concept-registry-an-ontology-grade-rigor-at-sqlalchemy-decorator-cost-semantido-v0-4-1-release]: Two agents walk into an mcp: the Concept Registry, an ontology-grade rigor at SQLAlchemy-decorator cost. Semantido v0.4.1 release.. Dragos Crintea. 2026-07-22.
[^the-semantic-layer-can-now-fail-your-build-semantido-v0-5-release]: The semantic layer can now fail your build - semantido v0.5 release.. Dragos Crintea. 2026-08-28.
