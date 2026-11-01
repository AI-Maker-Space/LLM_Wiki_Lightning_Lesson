---
type: Source
title: "The semantic layer can now fail your build - semantido v0.5 release."
description: "semantido v0.5 turns the layer from a descriptor into an enforcer, adding grain, a standalone groundings document, and a sqlglot-based linter whose ERROR findings fail CI."
tags: ["semantido", "semantic-layer", "release"]
generated: { by: "llm-wiki-lite/1.0", at: 2026-10-24T00:00:00Z }
resource: "https://dragoscrintea.me/articles/06-the-semantic-layer-can-now-fail-your-build"
sources:
  - id: "raw"
    resource: "../../raw/The semantic layer can now fail your build - semantido v0.5 release..md"
    title: "The semantic layer can now fail your build - semantido v0.5 release."
    author: "human:dragos-crintea"
    last_modified: 2026-08-28T00:00:00Z
---

# The semantic layer can now fail your build - semantido v0.5 release.

## Summary
v0.5 is the release where semantido stops being a descriptor and starts enforcing. Where v0.3 gave
the layer a sense of time and v0.4 gave it a concept registry — both authoring mechanisms — v0.5 adds
three guardrails: `grain` (the level at which a concept identifies its subject), a standalone
groundings document that separates portable meaning from deployment bindings, and `semantido.lint`, a
static checker that fails the CI build when a guardrail trips.[^raw]

Grain is motivated by a reconciliation trap: joining Bloomberg and Refinitiv feeds on `isin` fans out
to 12 rows for one instrument because ISIN counts issues while FIGI and RIC count listings — a
"semantically legal" join that the query planner, type checker and schema registry all accept. The
grain field makes the issue/listing/product distinction machine-readable, and the linter compares
grain strings across a join. Groundings, meanwhile, split a concept's portable meaning (governance
cadence) from its physical bindings (migration cadence), guarded by a `definition_checksum` that
detects a definition changing while its column bindings lag.[^raw]

`semantido.lint` is built on sqlglot and parses the layer and its joins without a database connection.
It emits Findings at two severities — ERROR (must fail CI) and WARNING — across ten checks (SL001–SL010),
including SL008 (joins across different grains), SL009 (joins equating DISTINCT_FROM concepts), and
SL010 (two DISTINCT_FROM concepts both claiming the same `skos:exactMatch`). The thesis: a layer that
only advises is documentation, and documentation drifts; enforcement catches only the contradictions
you were disciplined enough to declare.[^raw]

## Key Claims
- v0.5 turns semantido from a descriptor into an enforcer: a layer that only advises is just documentation, which drifts.[^raw]
- It adds three features: `grain`, a standalone groundings document, and `semantido.lint`.[^raw]
- Grain is the level at which a concept identifies its subject (e.g. ISIN = issue, RIC = listing, UPI = product); the field is free-form and semantido ships no grain taxonomy.[^raw]
- Joining feeds on `isin` fans out to 12 rows for one instrument (3 × 4 listings) because ISIN counts issues while FIGI/RIC count listings — a join nothing flags as broken.[^raw]
- A concept is portable meaning (governance cadence); a grounding is a deployment fact (schema-migration cadence); v0.5 splits them into separate files.[^raw]
- `definition_checksum` detects a definition being rewritten while its column bindings were never updated.[^raw]
- `semantido.lint` is built on sqlglot, runs without a database, and has two severities: ERROR (fails CI) and WARNING.[^raw]
- The ten checks (SL001–SL010) include SL008 (grain-mismatched joins), SL009 (joins equating DISTINCT_FROM concepts), and SL010 (DISTINCT_FROM concepts both claiming the same `skos:exactMatch`).[^raw]
- The most expensive joins are the ones that are semantically legal; enforcement catches only the contradictions that were declared.[^raw]

## Entities Mentioned
- [Dragos Crintea](../entities/dragos-crintea.md) — author
- [semantido](../entities/semantido.md) — the subject of the release
- [SQLAlchemy](../entities/sqlalchemy.md) — the decorated models the linter reads
- [Hikari Labs](../entities/hikari-labs.md) — the author's company and advisory
- **Open Semantic Interchange / ossie** (`entities/osi`) — the Apache Ossie integration v0.5 was tested against (candidate)

## Concepts Covered
- [Semantic layer](../concepts/semantic-layer.md) — now an artifact that can fail a release, not just a document
- [Semantic drift](../concepts/semantic-drift.md) — the central target; `definition_checksum` and the linter guard against it
- [Ontology](../concepts/ontology.md) — the concept tier (v0.4) that grain and the linter now enforce
- [Text2SQL](../concepts/text2sql.md) — the generated joins the linter parses and gates
- **Grain** (`concepts/grain`) and **concept registry** (`concepts/concept-registry`) — the primitives being enforced (candidates)

## Notable Quotes
> "a semantic layer that advises only, it's just documentation, and documentation drifts quickly. v0.5 fails your CI build, if any of the guardrails trigger."
— The author, stating the release's thesis

> "the most expensive joins are the ones that are semantically legal."
— The author, on why enforcement matters

## Notes
- Sixth and latest in the series; closes the arc from "author meaning" (v0.3/v0.4) to "enforce meaning" (v0.5), with an external-source authority guardrail promised for v0.6.
- Reuses the EMIR/MiFIR counterparty homonym from v0.4.1 as the flagship lint case.

[^raw]: The semantic layer can now fail your build - semantido v0.5 release.. Dragos Crintea. 2026-08-28.
