---
type: Source
title: "Where it all started. Why Building a semantic layer for GenAI."
description: "A first-person account of how brittle Text2SQL led the author to build semantido, an open-source semantic layer for the GenAI era."
tags: ["genai", "semantic-layer"]
generated: { by: "llm-wiki-dci/claude-opus-4-8", at: 2026-10-24T00:00:00Z }
resource: "https://dragoscrintea.me/articles/01-where-it-all-started-why-building-a-semantic-layer-for-genai"
sources:
  - id: "raw"
    resource: "../../raw/Where it all started. Why Building a semantic layer for GenAI..md"
    title: "Where it all started. Why Building a semantic layer for GenAI."
    author: "human:dragos-crintea"
    last_modified: 2026-01-16T00:00:00Z
---

# Where it all started. Why Building a semantic layer for GenAI.

## Summary
This is the first article in a planned series of eight on building semantic layers for GenAI applications. The author recounts jumping onto the GenAI bandwagon in mid-2024 out of curiosity, finding the field to be high-noise and low-signal, and investing roughly GBP 15k in 2025 courses to get a sense of direction. Drawing on a career spent as a Principal / Solution Architect and (Senior) Data Engineer, the author argues that the low (~10%) success rate of AI projects comes down to three culprits: security, system architecture, and data.[^raw]

The turning point came while building a "gym assistant" vertical agent during the 2025 AI Makers bootcamp (Cohort 5), using Langchain, AstroJS, and Supabase. Using an LLM to generate SQL from user prompts (Text2SQL) proved brittle: the model sometimes identified table columns correctly and sometimes did not. Prompt engineering, prompt decomposition, query rewriting, and few-shot examples yielded only marginal improvements. The realisation was that the LLM had no idea what the fields were, what they stored, or how they related to each other.[^raw]

Framing the problem through linguistics — semantics as the study of meaning — the author concludes that because an LLM is fundamentally about language, meaning and relationships matter. Adding table semantics to the context prompt improved SQL generation by orders of magnitude and, as a side effect, encouraged splitting SQL handling into three stages (generation, validation, execution). This experience motivated the author to build and open-source semantido, a semantic layer for the GenAI era.[^raw]

## Key Claims
- This is the first article in a planned series of eight about building semantic layer(s) for GenAI applications.[^raw]
- The author jumped onto the GenAI bandwagon in mid-2024 and invested roughly GBP 15k in 2025 on courses for direction.[^raw]
- The author's career was spent as a Principal / Solution Architect or (Senior) Data Engineer.[^raw]
- GenAI / AI projects are cited as having "a mere 10% success rate."[^raw]
- The three culprits behind GenAI project failure are, in the author's opinion, security, system architecture, and data.[^raw]
- The author claims 80% or more of a business's data is locked in SQL stores, document stores, Confluence, Word, PowerPoint, and PDF files.[^raw]
- During the 2025 AI Makers bootcamp (Cohort 5) the author built a gym-assistant vertical agent using Langchain, AstroJS, and Supabase, planned to launch at the end of Q1.[^raw]
- The author used an LLM to generate SQL from user prompts (Text2SQL); the generated SQL was brittle and inconsistently identified table columns.[^raw]
- Prompt engineering, prompt decomposition, query rewriting, few-shot examples, and considering CrewAI (itself based on Langchain) gave only marginal improvements.[^raw]
- The root cause was that the LLM had no knowledge of what the table fields were, what they stored, or how they related to each other.[^raw]
- Adding table semantics to the context prompt improved SQL generation by orders of magnitude.[^raw]
- As a side effect, SQL handling was split into three parts: generation, validation, and execution.[^raw]
- semantido is an open-source semantic layer for the GenAI era, built by the author and available on PyPI and GitHub.[^raw]
- The article's images were generated with Gemini 3, and the author states no AI was used in writing the text.[^raw]

## Entities Mentioned
- [semantido](../entities/semantido.md) — the author's open-source semantic layer for the GenAI era
- [Dragos Crintea](../entities/dragos-crintea.md) — author of the article and builder of semantido
- **Langchain** (`entities/langchain`) — framework used to build the gym-assistant agent; described as headache-inducing (candidate)
- **CrewAI** (`entities/crewai`) — alternative agent framework considered, itself based on Langchain (candidate)
- **AstroJS** (`entities/astrojs`) — web framework used in the gym-assistant project (candidate)
- **Supabase** (`entities/supabase`) — storage mechanism used in the gym-assistant project (candidate)
- **AI Makerspace** (`entities/ai-makerspace`) — ran the 2025 AI Makers bootcamp (Cohort 5) the author attended (candidate)
- **Gemini 3** (`entities/gemini-3`) — model used to generate the article's images (candidate)

## Concepts Covered
- [Semantic layer](../concepts/semantic-layer.md) — the central topic; adding meaning and relationships to data for GenAI
- [Text2SQL](../concepts/text2sql.md) — generating SQL from natural-language prompts via an LLM; brittle without semantics
- [Semantics](../concepts/semantics.md) — the study of meaning, framed as why LLMs need data meaning and relationships
- **Prompt engineering** (`concepts/prompt-engineering`) — decomposition, query rewriting, and few-shot examples tried with marginal results (candidate)
- **Vertical agent** (`concepts/vertical-agent`) — the gym-assistant built as a domain-specific agent (candidate)

## Notable Quotes
> "The LLM had **NO IDEA** what those fields where, what they stored, and how they relate to each other."
— The author, describing the root cause of brittle Text2SQL

> "Adding table semantics to the context prompt improved my SQL generation by orders of magnitude."
— The author, on the effect of the semantic layer

> "In linguistics, semantics is the scientific study of meaning."
— Quoted by the author from Wikipedia's definition of semantics

## Notes
- First in a series of eight; later articles cover what semantics are, the vendor landscape, and the semantido v0.3–v0.5 releases.
- Opened [semantido](../entities/semantido.md), [Semantic layer](../concepts/semantic-layer.md), [Text2SQL](../concepts/text2sql.md) and [Semantics](../concepts/semantics.md), all of which became pages once the series pushed them past the 3-mention threshold.
- `concepts/prompt-engineering` and `concepts/vertical-agent` remain candidates, mentioned only here.

[^raw]: Where it all started. Why Building a semantic layer for GenAI.. Dragos Crintea. 2026-01-16.
