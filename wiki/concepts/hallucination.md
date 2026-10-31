---
type: Concept
title: "Hallucination"
description: "An LLM producing plausible but wrong output; the series frames it as semantic misinterpretation from missing knowledge, reducible but never eliminable, and mitigated by curated semantics."
tags: ["genai", "reliability"]
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
  - id: "semantics-where-the-code-lives-interchange-where-the-stack-lives-semantido-v0-3-0-release"
    resource: "../sources/semantics-where-the-code-lives-interchange-where-the-stack-lives-semantido-v0-3-0-release.md"
    title: "Semantics where the code lives. Interchange where the stack lives. Semantido v0.3.0 release."
    author: "human:dragos-crintea"
    last_modified: 2026-07-10T00:00:00Z
---

# Hallucination

## Definition
Hallucination is an LLM producing a confident but wrong answer. The series frames it specifically as a
semantic misinterpretation caused by missing knowledge: the model guesses where it lacks the meaning it
needs, especially over tabular data whose relationships are not explicit.[^what-is-a-semantic-layer-after-all][^semantics-where-the-code-lives-interchange-where-the-stack-lives-semantido-v0-3-0-release]

## How It Works
The author argues a model hallucinates partly because it has no mapping between its training and the
context of a user interaction — and since the output is "nothing else than weights and biases," a wrong
answer always has nonzero probability.[^what-is-a-semantic-layer-after-all] On a schema, the model
sees columns but not which date is the time axis, whether an amount is signed, or what "your accounts"
means; every such gap is a semantic misinterpretation waiting to happen.[^semantics-where-the-code-lives-interchange-where-the-stack-lives-semantido-v0-3-0-release]

## Key Points
- The model originally "hallucinated" on the author's table columns because it had no idea what they stored or how they related.[^where-it-all-started-why-building-a-semantic-layer-for-genai]
- Framed as a missing training-to-context mapping; given weights and biases, some answer is always possible.[^what-is-a-semantic-layer-after-all]
- Semantics are the "high-tech glasses" that let a vision-impaired LLM "see" relationships absent from its training.[^what-is-a-semantic-layer-after-all]
- semantido aimed "from day one" to make an agent hallucinate less, while accepting (citing *LLMs Will Always Hallucinate*) that zero hallucination is near-impossible.[^semantics-where-the-code-lives-interchange-where-the-stack-lives-semantido-v0-3-0-release]
- Curated schema-in-context — deterministic labels on columns — steers the model onto a more deterministic path.[^semantics-where-the-code-lives-interchange-where-the-stack-lives-semantido-v0-3-0-release]

## Applications
Reducing hallucination on structured data is the practical payoff of a [semantic layer](semantic-layer.md)
and the reason brittle [Text2SQL](text2sql.md) improves so much once meaning is supplied.[^semantics-where-the-code-lives-interchange-where-the-stack-lives-semantido-v0-3-0-release]

## Related Concepts
- [Semantics](semantics.md) — the missing ingredient whose absence causes hallucination
- [Text2SQL](text2sql.md) — where hallucinated column/relationship guesses show up
- [Semantic layer](semantic-layer.md) — the mitigation

## Source History
- [where-it-all-started-why-building-a-semantic-layer-for-genai](../sources/where-it-all-started-why-building-a-semantic-layer-for-genai.md) — hallucination on unexplained columns
- [what-is-a-semantic-layer-after-all](../sources/what-is-a-semantic-layer-after-all.md) — the weights-and-biases framing and the glasses analogy
- [semantics-where-the-code-lives-interchange-where-the-stack-lives-semantido-v0-3-0-release](../sources/semantics-where-the-code-lives-interchange-where-the-stack-lives-semantido-v0-3-0-release.md) — curation to reduce it

[^where-it-all-started-why-building-a-semantic-layer-for-genai]: Where it all started. Why Building a semantic layer for GenAI.. Dragos Crintea. 2026-01-16.
[^what-is-a-semantic-layer-after-all]: What is a semantic layer after all?. Dragos Crintea. 2026-02-06.
[^semantics-where-the-code-lives-interchange-where-the-stack-lives-semantido-v0-3-0-release]: Semantics where the code lives. Interchange where the stack lives. Semantido v0.3.0 release.. Dragos Crintea. 2026-07-10.
