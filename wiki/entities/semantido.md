---
type: Entity
title: "semantido"
description: "An open-source, application-native semantic layer for the GenAI era that authors meaning as Python decorators on SQLAlchemy models and enforces it in CI."
tags: ["project", "semantic-layer"]
generated: { by: "llm-wiki-dci/claude-opus-4-8", at: 2026-10-24T00:00:00Z }
sources:
  - id: "where-it-all-started-why-building-a-semantic-layer-for-genai"
    resource: "../sources/where-it-all-started-why-building-a-semantic-layer-for-genai.md"
    title: "Where it all started. Why Building a semantic layer for GenAI."
    author: "human:dragos-crintea"
    last_modified: 2026-01-16T00:00:00Z
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

# semantido

## Overview
semantido is an open-source semantic layer built for the GenAI era, created by Dragos Crintea under
Hikari Labs and available on PyPI and GitHub.[^where-it-all-started-why-building-a-semantic-layer-for-genai][^the-semantic-layer-landscape-what-you-need-to-know-before-choosing-one] It is *application-native*:
rather than running as a separate service, it extends the SQLAlchemy models a Python application
already has with semantic decorators, so a table's definition and its meaning live in the same file,
versioned in the same pull request.[^the-semantic-layer-landscape-what-you-need-to-know-before-choosing-one]

Its guiding idea, repeated across releases, is to author semantics where the code lives — the one
place drift is caught — and to let that curation reach every consumer through per-consumer
serialization (Markdown for context windows, OSI YAML for tools, JSON for programs) and, increasingly,
through enforcement in CI.[^semantics-where-the-code-lives-interchange-where-the-stack-lives-semantido-v0-3-0-release][^the-semantic-layer-can-now-fail-your-build-semantido-v0-5-release]

## Key Facts
- **Type:** project (open-source Python library)
- **Creator / Parent:** [Dragos Crintea](dragos-crintea.md) / [Hikari Labs](hikari-labs.md)[^the-semantic-layer-landscape-what-you-need-to-know-before-choosing-one]
- **Domain:** semantic layer for GenAI and agentic analytics[^where-it-all-started-why-building-a-semantic-layer-for-genai]
- Open-source, available via `pip install semantido` on PyPI and on GitHub.[^where-it-all-started-why-building-a-semantic-layer-for-genai]
- Application-native: extends [SQLAlchemy](sqlalchemy.md) models with semantic decorators, so meaning deploys with the app at zero extra operational overhead.[^the-semantic-layer-landscape-what-you-need-to-know-before-choosing-one]
- Governed in the same repository and code-review process as the application, so definitions refresh with CI/CD and do not drift.[^the-semantic-layer-landscape-what-you-need-to-know-before-choosing-one]
- v0.3.0 (2026-07) added a first-class time-dimension model and a three-format exporter (OSI YAML, Markdown, JSON).[^semantics-where-the-code-lives-interchange-where-the-stack-lives-semantido-v0-3-0-release]
- Its Markdown export is ~780 tokens vs OSI YAML's ~1,719 for the same layer — a ~2.2× difference.[^semantics-where-the-code-lives-interchange-where-the-stack-lives-semantido-v0-3-0-release]
- v0.4.1 (2026-07) added a concept registry — three families of typed edges, no OWL and no reasoner, ~100 lines of protocol.[^two-agents-walk-into-an-mcp-the-concept-registry-an-ontology-grade-rigor-at-sqlalchemy-decorator-cost-semantido-v0-4-1-release]
- v0.5 (2026-08) added `grain`, a standalone groundings document, and `semantido.lint` (sqlglot, checks SL001–SL010) whose ERROR findings fail CI.[^the-semantic-layer-can-now-fail-your-build-semantido-v0-5-release]
- Targets [MCP](mcp.md): serializes definitions into an MCP-compatible format for agent access.[^the-semantic-layer-landscape-what-you-need-to-know-before-choosing-one][^semantics-where-the-code-lives-interchange-where-the-stack-lives-semantido-v0-3-0-release]
- **Limitations:** no caching (unsuited to sub-second dashboards), no BI-tool integration yet, and Python-native by design.[^the-semantic-layer-landscape-what-you-need-to-know-before-choosing-one]
- **Status:** active, pre-1.0 (v0.5 as of 2026-08).[^the-semantic-layer-can-now-fail-your-build-semantido-v0-5-release]

## Relevance
semantido is the throughline of this wiki: the author's own answer to the problems the series
diagnoses. In the vendor landscape it defines a sixth, "application-native" category with no direct
equivalent — the semantic layer as part of the application rather than a separate BI tool, pipeline,
service or warehouse feature.[^the-semantic-layer-landscape-what-you-need-to-know-before-choosing-one]
Its release arc tracks a clear thesis: author meaning next to the code (v0.3), give it ontological
structure (v0.4), and enforce it so the layer can fail a build rather than drift silently (v0.5).[^semantics-where-the-code-lives-interchange-where-the-stack-lives-semantido-v0-3-0-release][^two-agents-walk-into-an-mcp-the-concept-registry-an-ontology-grade-rigor-at-sqlalchemy-decorator-cost-semantido-v0-4-1-release][^the-semantic-layer-can-now-fail-your-build-semantido-v0-5-release]

## Related
- [SQLAlchemy](sqlalchemy.md) — semantido is built on it ([semantido builds on SQLAlchemy](../relationships/semantido-builds-on-sqlalchemy.md))
- [MCP](mcp.md) — semantido serializes to it ([semantido uses MCP](../relationships/semantido-uses-mcp.md))
- [Hikari Labs](hikari-labs.md) — the company behind semantido
- [Dragos Crintea](dragos-crintea.md) — its creator
- [Semantic layer](../concepts/semantic-layer.md) — the concept semantido implements
- [Semantic drift](../concepts/semantic-drift.md) — the failure semantido is designed to prevent

## Source History
- [where-it-all-started-why-building-a-semantic-layer-for-genai](../sources/where-it-all-started-why-building-a-semantic-layer-for-genai.md) — introduces semantido as the motivation
- [the-semantic-layer-landscape-what-you-need-to-know-before-choosing-one](../sources/the-semantic-layer-landscape-what-you-need-to-know-before-choosing-one.md) — positions it as the application-native category
- [semantics-where-the-code-lives-interchange-where-the-stack-lives-semantido-v0-3-0-release](../sources/semantics-where-the-code-lives-interchange-where-the-stack-lives-semantido-v0-3-0-release.md) — v0.3.0 time model + exporters
- [two-agents-walk-into-an-mcp-the-concept-registry-an-ontology-grade-rigor-at-sqlalchemy-decorator-cost-semantido-v0-4-1-release](../sources/two-agents-walk-into-an-mcp-the-concept-registry-an-ontology-grade-rigor-at-sqlalchemy-decorator-cost-semantido-v0-4-1-release.md) — v0.4.1 concept registry
- [the-semantic-layer-can-now-fail-your-build-semantido-v0-5-release](../sources/the-semantic-layer-can-now-fail-your-build-semantido-v0-5-release.md) — v0.5 grain, groundings, lint

[^where-it-all-started-why-building-a-semantic-layer-for-genai]: Where it all started. Why Building a semantic layer for GenAI.. Dragos Crintea. 2026-01-16.
[^the-semantic-layer-landscape-what-you-need-to-know-before-choosing-one]: The Semantic Layer landscape, what you need to know before choosing one.. Dragos Crintea. 2026-05-17.
[^semantics-where-the-code-lives-interchange-where-the-stack-lives-semantido-v0-3-0-release]: Semantics where the code lives. Interchange where the stack lives. Semantido v0.3.0 release.. Dragos Crintea. 2026-07-10.
[^two-agents-walk-into-an-mcp-the-concept-registry-an-ontology-grade-rigor-at-sqlalchemy-decorator-cost-semantido-v0-4-1-release]: Two agents walk into an mcp: the Concept Registry, an ontology-grade rigor at SQLAlchemy-decorator cost. Semantido v0.4.1 release.. Dragos Crintea. 2026-07-22.
[^the-semantic-layer-can-now-fail-your-build-semantido-v0-5-release]: The semantic layer can now fail your build - semantido v0.5 release.. Dragos Crintea. 2026-08-28.
