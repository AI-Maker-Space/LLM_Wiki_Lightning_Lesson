---
type: Source
title: "What is a semantic layer after all?"
description: "Disambiguates the overloaded term 'semantic layer' through Dave McComb's work, arguing that meaning must precede ontology and that LLMs need an explicit, LLM-ready semantic layer for tabular data."
tags: ["semantic-layer", "semantics"]
generated: { by: "llm-wiki-lite/1.0", at: 2026-10-24T00:00:00Z }
resource: "https://dragoscrintea.me/articles/02-what-is-a-semantic-layer-after-all"
sources:
  - id: "raw"
    resource: "../../raw/What is a semantic layer after all?.md"
    title: "What is a semantic layer after all?"
    author: "human:dragos-crintea"
    last_modified: 2026-02-06T00:00:00Z
---

# What is a semantic layer after all?

## Summary
The second article in the series sets out to disambiguate the term "semantic layer," which the
author argues has been overloaded by marketing — ironic, since *semantics* literally means the study
of meaning. Its central ordering claim is that semantics must come before ontology: first define
what something means in a given context, then build the ontology on top.[^raw]

The article explains how LLMs come to "understand" meaning — through statistical patterns and
contextual embeddings formed during pre-training — and why that breaks down on business-specific
context and especially on tabular data, where relationships are not explicit. The author frames
hallucination as the model lacking a mapping between its training and the context it is given, and
notes that RAG grounds text well but structured data needs an explicit semantic layer. The memorable
analogy: semantics are the "high-tech glasses" that let a vision-impaired LLM "see" relationships it
was never trained on.[^raw]

Drawing on Dave McComb's 2003 book *Semantics in Business Systems*, the article distinguishes
semantics (what something means) from ontology (how knowledge is organised once you know what it
means), and argues that source systems hold both application logic and data whose relationships are
lost when the two are separated. It concludes that semantic layers, once a nice-to-have in BI, are
now a non-negotiable requirement that demands a metadata architecture optimised for LLM
consumption — what the author calls a Semantic Layer Service.[^raw]

## Key Claims
- The term "semantic layer" has been overloaded (largely by marketing), despite semantics meaning the study of meaning.[^raw]
- Order of operations: semantics must come before ontology — define meaning in context first, then build the ontology.[^raw]
- LLMs acquire meaning through statistical patterns and contextual embeddings in pre-training, unlike fixed-vector methods such as word2vec.[^raw]
- Models struggle with business-specific context and with tabular data, where relationships must be provided explicitly.[^raw]
- The author argues hallucination arises partly because the model lacks a mapping between its training and the context of a user interaction — "nothing else than weights and biases."[^raw]
- RAG grounds large text corpora, but tabular data (Excel, SQL) needs an explicit semantic layer.[^raw]
- The argument draws on Dave McComb's *Semantics in Business Systems: The Savvy Manager's Guide* (2003).[^raw]
- Ontology organises knowledge once meaning is known; semantics concerns what something means — so semantics comes first.[^raw]
- Semantic layers were a BI nice-to-have but are now a non-negotiable requirement, demanding a metadata architecture optimised for LLM consumption.[^raw]

## Entities Mentioned
- [Dragos Crintea](../entities/dragos-crintea.md) — author
- [semantido](../entities/semantido.md) — the author's semantic layer, offered as the LLM-ready answer
- **Dave McComb** (`entities/dave-mccomb`) — author of *Semantics in Business Systems* (2003), the book the article builds on (candidate)

## Concepts Covered
- [Semantics](../concepts/semantics.md) — the study of meaning, framed as foundational for LLMs
- [Ontology](../concepts/ontology.md) — organisation of knowledge, which must follow semantics
- [Semantic layer](../concepts/semantic-layer.md) — the LLM-ready metadata architecture the article argues for
- [Text2SQL](../concepts/text2sql.md) — the structured-data case that needs explicit semantics
- [Hallucination](../concepts/hallucination.md) — reframed as a missing training-to-context mapping
- **RAG** (`concepts/rag`) — grounds text but is insufficient for tabular data (candidate)
- **Contextual embeddings** (`concepts/embeddings`) — how LLMs encode context-dependent meaning (candidate)

## Notable Quotes
> "Semantics must come before ontology. First define what something means in a specific context, then build the ontology."
— The author, stating the article's central ordering claim

> "We put words on everything / Then we put meaning on the words / Then we disagree"
— Dave McComb, quoted from *Semantics in Business Systems*

> "**Ontology** … concerns itself with the organization of knowledge once you know what it means. **Semantics** concerns itself more directly with what something means."
— Dave McComb, quoted from *Semantics in Business Systems*

## Notes
- Second in the series; explicitly builds on article 1 and promises a vendor comparison next (which becomes `sources/the-semantic-layer-landscape-what-you-need-to-know-before-choosing-one`).
- Introduces `concepts/ontology` as a counterpart to `concepts/semantics`; the two are compared in `relationships/semantics-vs-ontology`.
- Dave McComb is a strong candidate entity but appears substantively only in this source.

[^raw]: What is a semantic layer after all?. Dragos Crintea. 2026-02-06.
