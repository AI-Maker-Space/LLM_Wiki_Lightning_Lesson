# Wiki Index

_Index of the OKF v0.2 bundle. One entry per page, shown by concept ID (path under `wiki/` without
`.md`). Candidates have no page yet — they are named in source summaries and promoted to a page once
they reach 3+ mentions._

## Sources
- [`sources/where-it-all-started-why-building-a-semantic-layer-for-genai`](sources/where-it-all-started-why-building-a-semantic-layer-for-genai.md) — How brittle Text2SQL led the author to build semantido. (2026-01-16)
- [`sources/what-is-a-semantic-layer-after-all`](sources/what-is-a-semantic-layer-after-all.md) — Disambiguates "semantic layer" and argues meaning precedes ontology. (2026-02-06)
- [`sources/the-semantic-layer-landscape-what-you-need-to-know-before-choosing-one`](sources/the-semantic-layer-landscape-what-you-need-to-know-before-choosing-one.md) — A CDO's guide to six semantic-layer vendor categories. (2026-05-17)
- [`sources/semantics-where-the-code-lives-interchange-where-the-stack-lives-semantido-v0-3-0-release`](sources/semantics-where-the-code-lives-interchange-where-the-stack-lives-semantido-v0-3-0-release.md) — semantido v0.3.0: time dimension + three-format exporters. (2026-07-10)
- [`sources/two-agents-walk-into-an-mcp-the-concept-registry-an-ontology-grade-rigor-at-sqlalchemy-decorator-cost-semantido-v0-4-1-release`](sources/two-agents-walk-into-an-mcp-the-concept-registry-an-ontology-grade-rigor-at-sqlalchemy-decorator-cost-semantido-v0-4-1-release.md) — semantido v0.4.1: the concept registry. (2026-07-22)
- [`sources/the-semantic-layer-can-now-fail-your-build-semantido-v0-5-release`](sources/the-semantic-layer-can-now-fail-your-build-semantido-v0-5-release.md) — semantido v0.5: grain, groundings, and a CI-failing linter. (2026-08-28)

## Entities
_Pages:_
- [`entities/dragos-crintea`](entities/dragos-crintea.md) — author of the series and builder of semantido
- [`entities/hikari-labs`](entities/hikari-labs.md) — the company behind semantido
- [`entities/mcp`](entities/mcp.md) — Model Context Protocol; semantido's live-tools path
- [`entities/semantido`](entities/semantido.md) — the open-source application-native semantic layer
- [`entities/sqlalchemy`](entities/sqlalchemy.md) — the Python ORM semantido extends

_Candidates (mentions):_
- `entities/osi` (2) — Open Semantic Interchange, the vendor-neutral format semantido exports
- `entities/ai-makerspace` (1) — ran the 2025 AI Makers bootcamp
- `entities/astrojs` (1) — web framework in the gym-assistant project
- `entities/atscale` (1) — open-standard semantic layer (SML)
- `entities/crewai` (1) — alternative agent framework
- `entities/cube` (1) — headless semantic layer
- `entities/databricks` (1) — warehouse-native semantic layer
- `entities/dave-mccomb` (1) — author of *Semantics in Business Systems*
- `entities/dbt` (1) — transformation-native semantic layer (MetricFlow)
- `entities/fibo` (1) — public anchor ontology in the federated-agents experiment
- `entities/gemini-3` (1) — used to generate the articles' images
- `entities/gleif` (1) — public anchor (LEI) in the federated-agents experiment
- `entities/iso-20022` (1) — public anchor in the federated-agents experiment
- `entities/langchain` (1) — framework used in the gym-assistant project
- `entities/looker` (1) — BI-native semantic layer (LookML)
- `entities/malloy` (1) — open-standard semantic layer language
- `entities/power-bi` (1) — BI-native semantic layer (Fabric)
- `entities/snowflake` (1) — warehouse-native semantic layer
- `entities/supabase` (1) — storage in the gym-assistant project

## Concepts
_Pages:_
- [`concepts/hallucination`](concepts/hallucination.md) — plausible-but-wrong output from missing meaning
- [`concepts/ontology`](concepts/ontology.md) — organising knowledge once its meaning is known
- [`concepts/semantic-drift`](concepts/semantic-drift.md) — meaning diverging from the schema it describes
- [`concepts/semantic-layer`](concepts/semantic-layer.md) — curated metadata translating business meaning for LLMs
- [`concepts/semantics`](concepts/semantics.md) — the study of meaning
- [`concepts/text2sql`](concepts/text2sql.md) — generating SQL from natural language with an LLM

_Candidates (mentions):_
- `concepts/concept-registry` (2) — semantido's minimal, reasoner-free ontology tier
- `concepts/grain` (2) — the level at which a concept identifies its subject
- `concepts/definition-vs-description-system` (1) — the author's vendor diagnostic
- `concepts/embeddings` (1) — contextual embeddings in LLM pre-training
- `concepts/governance-vs-flexibility` (1) — the central vendor trade-off
- `concepts/prompt-engineering` (1) — decomposition, rewriting, few-shot examples
- `concepts/rag` (1) — retrieval augmentation, sufficient for text but not tabular data
- `concepts/time-dimension` (1) — the v0.3 primary-axis primitive
- `concepts/vertical-agent` (1) — a domain-specific agent (the gym assistant)

## Relationships
- [`relationships/semantic-layer-improves-text2sql`](relationships/semantic-layer-improves-text2sql.md) — the layer lifts NLQ accuracy from ~40% to 80%+
- [`relationships/semantido-builds-on-sqlalchemy`](relationships/semantido-builds-on-sqlalchemy.md) — semantics as decorators on ORM models
- [`relationships/semantido-uses-mcp`](relationships/semantido-uses-mcp.md) — the layer serialized to MCP for agents
- [`relationships/semantics-vs-ontology`](relationships/semantics-vs-ontology.md) — meaning must precede organisation

## Overviews
- [`overviews/overview`](overviews/overview.md) — synthesis of the series and the semantido releases
