---
type: Concept
title: "Semantic drift"
description: "When declared meaning diverges from the schema and data it describes; the series' recurring enemy, which semantido fights by authoring meaning next to code and enforcing it in CI."
tags: ["semantic-layer", "governance"]
generated: { by: "llm-wiki-dci/claude-opus-4-8", at: 2026-10-24T00:00:00Z }
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

# Semantic drift

## Definition
Semantic (or metric) drift is when a declared definition diverges from the schema and data it is
supposed to describe — the documentation says one thing while the tables have moved on. The series
treats it as the core failure a semantic layer exists to prevent, and as the line between a definition
system and a mere description system.[^the-semantic-layer-landscape-what-you-need-to-know-before-choosing-one]

## How It Works
Drift sets in when meaning lives apart from the code — in a separate YAML repo, a BI tool, or a
warehouse object — and is re-keyed and maintained by hand. semantido's counter is to author meaning on
the models themselves so a change is a reviewed pull request, validate declarations against the
physical schema at sync time, and (from v0.5) split a concept's portable meaning from its physical
groundings, guarding the link with a `definition_checksum` and the `semantido.lint` checks.[^semantics-where-the-code-lives-interchange-where-the-stack-lives-semantido-v0-3-0-release][^the-semantic-layer-can-now-fail-your-build-semantido-v0-5-release]

## Key Points
- The decisive vendor test is how long a table-definition change takes to propagate consistently to every AI query, dashboard and report; manual steps signal a description system that drifts.[^the-semantic-layer-landscape-what-you-need-to-know-before-choosing-one]
- "Semantics that drift from the schema are bugs," and should surface at semantic-layer creation, not in a consumer's SQL three tools downstream.[^semantics-where-the-code-lives-interchange-where-the-stack-lives-semantido-v0-3-0-release]
- Validating concept/axis bindings at sync time makes a typo fail the build, not the agent's answer.[^two-agents-walk-into-an-mcp-the-concept-registry-an-ontology-grade-rigor-at-sqlalchemy-decorator-cost-semantido-v0-4-1-release]
- `definition_checksum` catches a definition being rewritten while its column bindings were never updated.[^the-semantic-layer-can-now-fail-your-build-semantido-v0-5-release]
- A layer that only advises is documentation, which drifts; v0.5 fails CI when a guardrail trips.[^the-semantic-layer-can-now-fail-your-build-semantido-v0-5-release]

## Applications
Drift is the reason the series favours an application-native, git-governed layer: authoring meaning
next to the code and enforcing it in CI is presented as the only reliable way to keep AI-generated
queries correct as schemas evolve — a problem the author expects to compound in agentic workflows.[^the-semantic-layer-can-now-fail-your-build-semantido-v0-5-release]

## Related Concepts
- [Semantic layer](semantic-layer.md) — the mechanism that prevents drift
- [Semantics](semantics.md) — the meaning that drifts
- [Ontology](ontology.md) — the concept tier whose drift v0.5 enforces against

## Source History
- [the-semantic-layer-landscape-what-you-need-to-know-before-choosing-one](../sources/the-semantic-layer-landscape-what-you-need-to-know-before-choosing-one.md) — the propagation test; definition vs. description systems
- [semantics-where-the-code-lives-interchange-where-the-stack-lives-semantido-v0-3-0-release](../sources/semantics-where-the-code-lives-interchange-where-the-stack-lives-semantido-v0-3-0-release.md) — drift as a bug caught at sync time
- [two-agents-walk-into-an-mcp-the-concept-registry-an-ontology-grade-rigor-at-sqlalchemy-decorator-cost-semantido-v0-4-1-release](../sources/two-agents-walk-into-an-mcp-the-concept-registry-an-ontology-grade-rigor-at-sqlalchemy-decorator-cost-semantido-v0-4-1-release.md) — typo'd bindings fail the build
- [the-semantic-layer-can-now-fail-your-build-semantido-v0-5-release](../sources/the-semantic-layer-can-now-fail-your-build-semantido-v0-5-release.md) — checksum and lint enforcement

[^the-semantic-layer-landscape-what-you-need-to-know-before-choosing-one]: The Semantic Layer landscape, what you need to know before choosing one.. Dragos Crintea. 2026-05-17.
[^semantics-where-the-code-lives-interchange-where-the-stack-lives-semantido-v0-3-0-release]: Semantics where the code lives. Interchange where the stack lives. Semantido v0.3.0 release.. Dragos Crintea. 2026-07-10.
[^two-agents-walk-into-an-mcp-the-concept-registry-an-ontology-grade-rigor-at-sqlalchemy-decorator-cost-semantido-v0-4-1-release]: Two agents walk into an mcp: the Concept Registry, an ontology-grade rigor at SQLAlchemy-decorator cost. Semantido v0.4.1 release.. Dragos Crintea. 2026-07-22.
[^the-semantic-layer-can-now-fail-your-build-semantido-v0-5-release]: The semantic layer can now fail your build - semantido v0.5 release.. Dragos Crintea. 2026-08-28.
