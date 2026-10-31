---
type: Concept
title: "Semantics"
description: "The study of meaning — in linguistics and, in Dave McComb's broader sense, of what the symbols inside a computer really mean in the real world; the foundation an LLM lacks for business data."
tags: ["semantics", "meaning"]
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
  - id: "the-semantic-layer-can-now-fail-your-build-semantido-v0-5-release"
    resource: "../sources/the-semantic-layer-can-now-fail-your-build-semantido-v0-5-release.md"
    title: "The semantic layer can now fail your build - semantido v0.5 release."
    author: "human:dragos-crintea"
    last_modified: 2026-08-28T00:00:00Z
---

# Semantics

## Definition
Semantics is the study of meaning. The series starts from the linguistic definition — how words,
phrases and sentences convey concepts and relationships — and adopts Dave McComb's broader one, in
which meaning can reside in things other than words, and what matters is whether the people and
programs handling information agree on what the symbols inside a computer mean in the real world.[^what-is-a-semantic-layer-after-all]

## How It Works
Because an LLM is fundamentally about language, meaning and relationships are central to it, yet the
model only approximates meaning through statistical patterns in training data.[^where-it-all-started-why-building-a-semantic-layer-for-genai][^what-is-a-semantic-layer-after-all]
A semantic layer makes the missing, business-specific meaning explicit and governed, so it can be
served to the model and kept from drifting away from the schema.[^semantics-where-the-code-lives-interchange-where-the-stack-lives-semantido-v0-3-0-release]

## Key Points
- Because an LLM is "all about language," semantics play a central role in how it succeeds or fails.[^where-it-all-started-why-building-a-semantic-layer-for-genai]
- The term "semantic" has been overloaded (largely by marketing), ironic for a word meaning the study of meaning.[^what-is-a-semantic-layer-after-all]
- Semantics must come before ontology: define what something means in context first, then organise it.[^what-is-a-semantic-layer-after-all]
- "Semantics that drift from the schema are bugs," so meaning should be authored where drift is caught — next to the code.[^semantics-where-the-code-lives-interchange-where-the-stack-lives-semantido-v0-3-0-release]
- Every semantido release has tried to make meaning easier to write, and then (from v0.5) enforceable.[^the-semantic-layer-can-now-fail-your-build-semantido-v0-5-release]

## Applications
Operationalising semantics as governed metadata is exactly what a [semantic layer](semantic-layer.md)
does; it is the prerequisite for reliable [Text2SQL](text2sql.md) and for building an
[ontology](ontology.md) on top.[^what-is-a-semantic-layer-after-all]

## Related Concepts
- [Ontology](ontology.md) — what is built once meaning is known ([semantics vs ontology](../relationships/semantics-vs-ontology.md))
- [Semantic layer](semantic-layer.md) — semantics made into governed metadata
- [Hallucination](hallucination.md) — what happens when the model lacks the right meaning

## Source History
- [where-it-all-started-why-building-a-semantic-layer-for-genai](../sources/where-it-all-started-why-building-a-semantic-layer-for-genai.md) — semantics matter because an LLM is about language
- [what-is-a-semantic-layer-after-all](../sources/what-is-a-semantic-layer-after-all.md) — the definition and McComb's broadening
- [semantics-where-the-code-lives-interchange-where-the-stack-lives-semantido-v0-3-0-release](../sources/semantics-where-the-code-lives-interchange-where-the-stack-lives-semantido-v0-3-0-release.md) — semantics that drift are bugs
- [the-semantic-layer-can-now-fail-your-build-semantido-v0-5-release](../sources/the-semantic-layer-can-now-fail-your-build-semantido-v0-5-release.md) — making meaning enforceable

[^where-it-all-started-why-building-a-semantic-layer-for-genai]: Where it all started. Why Building a semantic layer for GenAI.. Dragos Crintea. 2026-01-16.
[^what-is-a-semantic-layer-after-all]: What is a semantic layer after all?. Dragos Crintea. 2026-02-06.
[^semantics-where-the-code-lives-interchange-where-the-stack-lives-semantido-v0-3-0-release]: Semantics where the code lives. Interchange where the stack lives. Semantido v0.3.0 release.. Dragos Crintea. 2026-07-10.
[^the-semantic-layer-can-now-fail-your-build-semantido-v0-5-release]: The semantic layer can now fail your build - semantido v0.5 release.. Dragos Crintea. 2026-08-28.
