---
type: Entity
title: "SQLAlchemy"
description: "The Python ORM that most Python data applications use; semantido extends its models with semantic decorators so meaning lives next to the schema."
tags: ["tool", "python"]
generated: { by: "llm-wiki-lite/1.0", at: 2026-10-24T00:00:00Z }
sources:
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

# SQLAlchemy

## Overview
SQLAlchemy is the Python ORM that, in the author's framing, most Python data applications already use.
[semantido](semantido.md) is built directly on it: semantido's semantics are written as decorators and
annotations on SQLAlchemy models, so the table definition and its meaning live in the same file and
ship in the same deployment.[^the-semantic-layer-landscape-what-you-need-to-know-before-choosing-one]

## Key Facts
- **Type:** tool (Python ORM)
- Described as the ORM most Python data applications already use.[^the-semantic-layer-landscape-what-you-need-to-know-before-choosing-one]
- semantido extends SQLAlchemy models with semantic decorators rather than introducing a new service.[^the-semantic-layer-landscape-what-you-need-to-know-before-choosing-one]
- semantido's `@semantic_table(...)` decorator and column attributes (e.g. `time_dimension`, `concept=`) are declared on SQLAlchemy classes and validated against the physical schema at sync time.[^semantics-where-the-code-lives-interchange-where-the-stack-lives-semantido-v0-3-0-release][^two-agents-walk-into-an-mcp-the-concept-registry-an-ontology-grade-rigor-at-sqlalchemy-decorator-cost-semantido-v0-4-1-release]
- The decorated models are the "Tier 2" that semantido's v0.5 linter reads.[^the-semantic-layer-can-now-fail-your-build-semantido-v0-5-release]

## Relevance
SQLAlchemy is the substrate that makes semantido "application-native." Because meaning is authored on
the ORM classes, it inherits the application's code-review and deployment process — the mechanism the
author credits for preventing drift.[^the-semantic-layer-landscape-what-you-need-to-know-before-choosing-one]

## Related
- [semantido](semantido.md) — built on SQLAlchemy ([semantido builds on SQLAlchemy](../relationships/semantido-builds-on-sqlalchemy.md))
- [Semantic layer](../concepts/semantic-layer.md) — authored here, on the ORM models

## Source History
- [the-semantic-layer-landscape-what-you-need-to-know-before-choosing-one](../sources/the-semantic-layer-landscape-what-you-need-to-know-before-choosing-one.md) — semantido extends SQLAlchemy models
- [semantics-where-the-code-lives-interchange-where-the-stack-lives-semantido-v0-3-0-release](../sources/semantics-where-the-code-lives-interchange-where-the-stack-lives-semantido-v0-3-0-release.md) — decorators validated at sync time
- [two-agents-walk-into-an-mcp-the-concept-registry-an-ontology-grade-rigor-at-sqlalchemy-decorator-cost-semantido-v0-4-1-release](../sources/two-agents-walk-into-an-mcp-the-concept-registry-an-ontology-grade-rigor-at-sqlalchemy-decorator-cost-semantido-v0-4-1-release.md) — concept bindings on columns
- [the-semantic-layer-can-now-fail-your-build-semantido-v0-5-release](../sources/the-semantic-layer-can-now-fail-your-build-semantido-v0-5-release.md) — decorated models as the lint input

[^the-semantic-layer-landscape-what-you-need-to-know-before-choosing-one]: The Semantic Layer landscape, what you need to know before choosing one.. Dragos Crintea. 2026-05-17.
[^semantics-where-the-code-lives-interchange-where-the-stack-lives-semantido-v0-3-0-release]: Semantics where the code lives. Interchange where the stack lives. Semantido v0.3.0 release.. Dragos Crintea. 2026-07-10.
[^two-agents-walk-into-an-mcp-the-concept-registry-an-ontology-grade-rigor-at-sqlalchemy-decorator-cost-semantido-v0-4-1-release]: Two agents walk into an mcp: the Concept Registry, an ontology-grade rigor at SQLAlchemy-decorator cost. Semantido v0.4.1 release.. Dragos Crintea. 2026-07-22.
[^the-semantic-layer-can-now-fail-your-build-semantido-v0-5-release]: The semantic layer can now fail your build - semantido v0.5 release.. Dragos Crintea. 2026-08-28.
