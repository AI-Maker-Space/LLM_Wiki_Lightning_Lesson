---
type: Relationship
title: "Semantic layer improves Text2SQL"
description: "A semantic layer is what turns brittle Text2SQL into a reliable capability; the series reports accuracy jumping from ~40% to 80%+ once meaning is supplied in context."
tags: ["semantic-layer", "text2sql"]
relation: other
between: ["concepts/semantic-layer", "concepts/text2sql"]
generated: { by: "llm-wiki-lite/1.0", at: 2026-10-24T00:00:00Z }
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
---

# Semantic layer improves Text2SQL

## Summary
The semantic layer is the dependency that makes [Text2SQL](../concepts/text2sql.md) reliable. Without
explicit meaning the model guesses at columns and relationships; supplying a
[semantic layer](../concepts/semantic-layer.md) in context constrains it toward correct queries. The
series reports the lift concretely: natural-language query accuracy rises from ~40% without a layer to
80%+ with one.[^where-it-all-started-why-building-a-semantic-layer-for-genai][^the-semantic-layer-landscape-what-you-need-to-know-before-choosing-one]

## Evidence
- Adding table semantics to the context prompt improved the author's SQL generation by orders of magnitude.[^where-it-all-started-why-building-a-semantic-layer-for-genai]
- Natural-language query accuracy is ~40% without a semantic layer and 80%+ with one (per Snowflake Cortex, Databricks Genie and Google research).[^the-semantic-layer-landscape-what-you-need-to-know-before-choosing-one]
- The author validated ~30% → ~90% on a fitness analytics pipeline (GPT-4o, ~16 tables across three schemas) after adding a layer.[^the-semantic-layer-landscape-what-you-need-to-know-before-choosing-one]
- The 40% gap is framed as an infrastructure problem, not something a better model or prompt would fix.[^the-semantic-layer-landscape-what-you-need-to-know-before-choosing-one]

## Related
- [Semantic layer](../concepts/semantic-layer.md) — the enabling dependency
- [Text2SQL](../concepts/text2sql.md) — the task it improves
- [Hallucination](../concepts/hallucination.md) — the failure the layer suppresses

## Source History
- [where-it-all-started-why-building-a-semantic-layer-for-genai](../sources/where-it-all-started-why-building-a-semantic-layer-for-genai.md) — order-of-magnitude improvement
- [the-semantic-layer-landscape-what-you-need-to-know-before-choosing-one](../sources/the-semantic-layer-landscape-what-you-need-to-know-before-choosing-one.md) — the 40% → 80%+ figures

[^where-it-all-started-why-building-a-semantic-layer-for-genai]: Where it all started. Why Building a semantic layer for GenAI.. Dragos Crintea. 2026-01-16.
[^the-semantic-layer-landscape-what-you-need-to-know-before-choosing-one]: The Semantic Layer landscape, what you need to know before choosing one.. Dragos Crintea. 2026-05-17.
