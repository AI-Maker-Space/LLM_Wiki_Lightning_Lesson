---
type: Source
title: "The Semantic Layer landscape, what you need to know before choosing one."
description: "A CDO's procurement guide to six categories of semantic-layer vendors, arguing the real decision is governance vs. flexibility and whether a vendor sells a definition system or a description system."
tags: ["semantic-layer", "vendors"]
generated: { by: "llm-wiki-lite/1.0", at: 2026-10-24T00:00:00Z }
resource: "https://dragoscrintea.me/articles/03-semantic-layer-landscape-what-you-need-to-know"
sources:
  - id: "raw"
    resource: "../../raw/The Semantic Layer landscape, what you need to know before choosing one..md"
    title: "The Semantic Layer landscape, what you need to know before choosing one."
    author: "human:dragos-crintea"
    last_modified: 2026-05-17T00:00:00Z
---

# The Semantic Layer landscape, what you need to know before choosing one.

## Summary
Written for Chief Data / Analytics Officers, this article maps the crowded semantic-layer vendor
space into six categories and argues that the real procurement decision is a governance-vs-flexibility
trade-off, not a feature checklist. The author's sharper framing: is a vendor selling a *definition
system* (the source of truth everything downstream follows) or a *description system* (documentation
that can drift)? Only definition systems solve the problem.[^raw]

The piece anchors the stakes in numbers: natural-language query accuracy sits around 40% without a
semantic layer and jumps to 80%+ with one — figures the author says Snowflake Cortex, Databricks
Genie and Google research converge on, and which the author validated on a fitness analytics pipeline
(≈30% baseline on GPT-4o rising to ≈90%, across ~16 tables in three schemas). The 40% gap is cast as
an infrastructure problem, not a prompting or model problem.[^raw]

The six categories are BI-native (Power BI/Fabric, LookML/Looker), headless (Cube), transformation-native
(dbt MetricFlow), warehouse-native (Snowflake, Databricks), open-standard (Malloy, AtScale SML), and
application-native (semantido). The author's own tool, semantido, occupies the application-native slot:
it extends SQLAlchemy models with semantic decorators so the table and its meaning live in one file,
deploys with the app with zero extra operational overhead, is governed by the same git review as code,
and is MCP-ready — at the cost of no caching and no BI-tool integration yet.[^raw]

## Key Claims
- Natural-language query accuracy is ~40% without a semantic layer and 80%+ with one (per Snowflake Cortex, Databricks Genie, and Google research).[^raw]
- The author validated ~30% → ~90% accuracy on a fitness analytics pipeline (GPT-4o, ~16 tables across three schemas) once a semantic layer was added.[^raw]
- The core decision is governance vs. flexibility; the deeper question is whether a vendor sells a definition system or a description system — only the former solves the problem.[^raw]
- There are six vendor categories, plotted on lock-in risk vs. agentic readiness.[^raw]
- Semantic layers are not new: LookML dates to ~2012, Cube launched 2019, dbt's metric layer existed from ~2021; AI made the semantic layer a core dependency in 2024.[^raw]
- The decisive test for any vendor: when a table definition changes, how long until that change propagates consistently to every AI-generated query, dashboard, and report.[^raw]
- semantido is application-native: it extends SQLAlchemy models with semantic decorators, so definitions deploy with the app, are governed in the same repo, and never drift — but it has no caching and no BI-tool integration yet.[^raw]

## Entities Mentioned
- [Dragos Crintea](../entities/dragos-crintea.md) — author and builder of semantido
- [semantido](../entities/semantido.md) — the application-native category (category 6)
- [SQLAlchemy](../entities/sqlalchemy.md) — the Python ORM semantido extends with decorators
- [MCP](../entities/mcp.md) — the protocol semantido targets for exposing schemas to agents
- [Hikari Labs](../entities/hikari-labs.md) — the author's company; hosts the semantido repo and the advisory workshop
- **Power BI / Microsoft Fabric**, **LookML / Looker**, **Cube**, **dbt MetricFlow**, **Snowflake**, **Databricks**, **Malloy**, **AtScale** (`entities/power-bi`, `entities/looker`, `entities/cube`, `entities/dbt`, `entities/snowflake`, `entities/databricks`, `entities/malloy`, `entities/atscale`) — the other five vendor categories (candidates)

## Concepts Covered
- [Semantic layer](../concepts/semantic-layer.md) — the subject; the vendor categories are ways to build one
- [Text2SQL](../concepts/text2sql.md) — reframed: the point is faster, correct work, not "can AI write SQL"
- [Semantic drift](../concepts/semantic-drift.md) — the propagation test; definition vs. description systems
- **Governance vs. flexibility** (`concepts/governance-vs-flexibility`) — the central trade-off (candidate)
- **Definition vs. description system** (`concepts/definition-vs-description-system`) — the author's diagnostic (candidate)

## Notable Quotes
> "Is this vendor selling you a definition system or a description system? Only the former actually solves the problem."
— The author, on the architectural question under every vendor choice

> "Natural language query accuracy without a semantic layer sits around 40%. With one, it jumps to 80% or more."
— The author, citing Snowflake, Databricks and Google figures

## Notes
- Third in the series; the "definition vs. description system" lens recurs in later release posts as the drift that `semantido.lint` enforces against.
- Many vendor entities appear only here, so they remain candidates; semantido's category-6 position is captured on `entities/semantido`.

[^raw]: The Semantic Layer landscape, what you need to know before choosing one.. Dragos Crintea. 2026-05-17.
