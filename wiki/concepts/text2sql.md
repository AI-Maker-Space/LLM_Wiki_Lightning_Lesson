---
type: Concept
title: "Text2SQL"
description: "Generating SQL from a natural-language prompt with an LLM; brittle on real schemas without a semantic layer, and reframed as a capability question rather than a syntax one."
tags: ["text2sql", "genai"]
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
  - id: "the-semantic-layer-can-now-fail-your-build-semantido-v0-5-release"
    resource: "../sources/the-semantic-layer-can-now-fail-your-build-semantido-v0-5-release.md"
    title: "The semantic layer can now fail your build - semantido v0.5 release."
    author: "human:dragos-crintea"
    last_modified: 2026-08-28T00:00:00Z
---

# Text2SQL

## Definition
Text2SQL is the use of an LLM to generate SQL queries from a natural-language prompt (for example,
"show me the exercises I burn the most calories on").[^where-it-all-started-why-building-a-semantic-layer-for-genai]
It is the task that first exposed, for the author, why models need a semantic layer.

## How It Works
The model maps a natural-language request to SQL against a schema. Without explicit meaning it does so
brittlely — sometimes identifying the right columns, sometimes not — because it has no idea what the
fields are, what they store, or how they relate.[^where-it-all-started-why-building-a-semantic-layer-for-genai]
Supplying schema-in-context semantics (descriptions, relationships, a primary time axis, guardrails)
constrains the model toward a deterministic, correct query, and the author's early work split SQL
handling into generation, validation and execution.[^where-it-all-started-why-building-a-semantic-layer-for-genai][^semantics-where-the-code-lives-interchange-where-the-stack-lives-semantido-v0-3-0-release]

## Key Points
- Generated SQL was brittle; prompt engineering, decomposition, query rewriting and few-shot examples gave only marginal improvements.[^where-it-all-started-why-building-a-semantic-layer-for-genai]
- Adding table semantics to the prompt improved SQL generation by orders of magnitude.[^where-it-all-started-why-building-a-semantic-layer-for-genai]
- Structured data such as SQL needs explicit semantics; implicit inference is only partial.[^what-is-a-semantic-layer-after-all]
- The real question is not "can AI write SQL" but whether people move meaningfully faster — without a layer you get wrong answers at scale, worse than no answers.[^the-semantic-layer-landscape-what-you-need-to-know-before-choosing-one]
- Serialization matters for the generating model: on a probe, OSI YAML dropped data types that Markdown kept, hurting SQL generation when absent.[^semantics-where-the-code-lives-interchange-where-the-stack-lives-semantido-v0-3-0-release]
- Even fluent, well-formed SQL can be wrong when a join is "semantically legal" but crosses grains.[^the-semantic-layer-can-now-fail-your-build-semantido-v0-5-release]

## Applications
Text2SQL and natural-language analytics are the headline use case the semantic layer serves; the
accuracy lift from adding a layer (~40% → 80%+) is the series' central quantitative claim.[^the-semantic-layer-landscape-what-you-need-to-know-before-choosing-one]

## Related Concepts
- [Semantic layer](semantic-layer.md) — what makes Text2SQL reliable ([semantic layer improves Text2SQL](../relationships/semantic-layer-improves-text2sql.md))
- [Hallucination](hallucination.md) — the failure mode brittle Text2SQL exhibits
- [Semantic drift](semantic-drift.md) — why generated queries silently go wrong over time

## Source History
- [where-it-all-started-why-building-a-semantic-layer-for-genai](../sources/where-it-all-started-why-building-a-semantic-layer-for-genai.md) — the brittle-Text2SQL origin story
- [what-is-a-semantic-layer-after-all](../sources/what-is-a-semantic-layer-after-all.md) — why tabular data needs explicit semantics
- [the-semantic-layer-landscape-what-you-need-to-know-before-choosing-one](../sources/the-semantic-layer-landscape-what-you-need-to-know-before-choosing-one.md) — reframing and accuracy figures
- [semantics-where-the-code-lives-interchange-where-the-stack-lives-semantido-v0-3-0-release](../sources/semantics-where-the-code-lives-interchange-where-the-stack-lives-semantido-v0-3-0-release.md) — serialization and SQL generation
- [the-semantic-layer-can-now-fail-your-build-semantido-v0-5-release](../sources/the-semantic-layer-can-now-fail-your-build-semantido-v0-5-release.md) — semantically-legal-but-wrong joins

[^where-it-all-started-why-building-a-semantic-layer-for-genai]: Where it all started. Why Building a semantic layer for GenAI.. Dragos Crintea. 2026-01-16.
[^what-is-a-semantic-layer-after-all]: What is a semantic layer after all?. Dragos Crintea. 2026-02-06.
[^the-semantic-layer-landscape-what-you-need-to-know-before-choosing-one]: The Semantic Layer landscape, what you need to know before choosing one.. Dragos Crintea. 2026-05-17.
[^semantics-where-the-code-lives-interchange-where-the-stack-lives-semantido-v0-3-0-release]: Semantics where the code lives. Interchange where the stack lives. Semantido v0.3.0 release.. Dragos Crintea. 2026-07-10.
[^the-semantic-layer-can-now-fail-your-build-semantido-v0-5-release]: The semantic layer can now fail your build - semantido v0.5 release.. Dragos Crintea. 2026-08-28.
