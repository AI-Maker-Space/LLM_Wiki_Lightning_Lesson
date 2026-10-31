---
title: "Semantics where the code lives. Interchange where the stack lives. Semantido v0.3.0 release."
source: "https://dragoscrintea.me/articles/04-semantics-where-the-code-lives-interchange-where-the-stack-lives"
author:
published: 2026-07-10
created: 2026-10-24
description: "semantido 0.3 ships a first-class time-dimension model, alongside a complete exporter overhaul that serializes one semantic layer as OSI YAML, Markdown, and JSON. This article explains why the two belong in one release: curated metadata is the difference between an AI agent finding eight false time axes or finding the right one."
tags:
  - "clippings"
---
![Hero image representing multiple export types for a semantic layer.](https://dragoscrintea.me/_next/static/media/hero_image_article_4.1j2ed3b3pz3jr.png)

## TLDR;

- **Why this article**: semantido 0.3 ships two new features, a first-class time-dimension model, and a complete exporter overhaul. This article explains the importance of this release: what an AI agent actually needs from a database, why that knowledge must be authored next to the code, and how one governed semantic layer now reaches every consumer in the stack, as OSI YAML for tools, Markdown for context windows, and JSON for programs.
- **Most important take**: the value of a semantic layer is not in the format, it's in the curation the format carries. On the same synthetic banking schema, the same OSI export goes from eight candidate "time axes" to one unambiguous primary axis purely on the strength of metadata a human declared. The curation is the product; the formats are how it ships.
- **A challenging thought**: the interchange standard the industry is rallying behind carries less information than a plain Markdown export, OSI has no data types, no grain, no way to name a primary axis, and costs 2.2× the tokens as prompt context. If your agents read the semantic model as text, the humble format may beat the standard. Perhaps the most valuable thing semantic-layer vendors can do right now isn't adopting OSI, it's pushing what's missing into it.

> Update on the numbers on this article after the new ossie v0.2.0dev schema release. OSI serialization size: 6,877 → 6,975 chars, ~1,719 → ~1,743 tokens, about +1.4%. Markdown and enriched Markdown are byte-identical (their exporters remains the same). ossie is still at ~2.2× Markdown.

## Intro

Agents do not fail at SQL syntax. They will produce fluent, well-formatted queries with ease, and you would think... what a wonderful and well-oiled system.

I am here to disappoint you: you can't fire your SQL team to fund your 11 <sup>th</sup> yacht. Not now and not in the future either, and the reason for this will become obvious if you have the patience to read this article.

As the industry is slowly starting to realize, agents amazingly fail at "understanding" meaning. Let's examine these examples:

- Which of the seven date columns in the table **is** the time axis
- Whether an amount is signed
- Or "your accounts" mean active accounts only from the CRM system and not the Delivery one.

Every one of those failures is a semantic misinterpretation through a lack of knowledge. The schema tells the agent far less than a human would know.

From day one *semantido* aimed to make an agent hallucinate less. It would be near impossible to have zero hallucinations as this article nicely puts it: [LLMs Will Always Hallucinate, and We Need to Live With This](https://arxiv.org/abs/2409.05746) . By providing the right schema-in-context information through a combination of deterministic labels attached to columns at code-base level, this instructs the LLM to take a more deterministic path when it comes to SQL generation.

So what's new you might ask.

[semantido v0.3.0](https://github.com/hikarilabs/semantido) brings a first-class time dimension to the semantic model, alongside a rebuilt exporters' module. Let’s unpack them:

1. A first-class time-dimension model, split into:
	- A primary time axis (declared per table in the semantido's semantic\_table annotation)
		- Secondary time axes declared at column level
		- A `TimeGrain` enum for native resolution
	All of this is validated against the physical schema at sync time. If a declared axis does not exist, is not temporal, or claims a grain finer than its column type can represent, the sync fails immediately rather than pushing wrong information downstream.
2. A rebuilt exporters module. A new `semantido.exporters` package that serializes one synchronized semantic layer in three ways:
	- OSI - YAML for interchange
		- Markdown for LLM schema-in-context prompt
		- JSON for programmatic consumers

One source of truth, one serialization per consumer.

This post is about why those two features are released together: the time-dimension model is the *curation* that makes a schema agent-friendly, and the exporters are how that curation reaches every agent or consumer system in the stack. Version 0.3.0 also brings a deterministic byte-identical semantic layer export, making the generated artifacts easier to diff and cache.

*semantido* is the authoring layer, the semantics are written in Python, right on the SQLAlchemy models, versioned and updated in the same pull request as the schema. [Open Semantic Interchange](https://github.com/open-semantic-interchange/OSI) (OSI), the vendor-neutral format, is the interchange layer, and v 0.3.0 exports it natively. A caveat here, OSI is an ongoing endeavour, so this semantido release targets `OSI v0.2.0`. semantido is where meaning is written and governed; OSI is how it is presented to any downstream OSI-aware consumer, `semantido.exporters.to_osi_yaml` is where the magic happens.

## What an agent actually needs

![semantido disambiguation feature](https://dragoscrintea.me/_next/static/media/2.Disambiguation.22xs5-wjmav3d.png)

Strip away the vendor language and an agent-friendly environment comes down to three guarantees at query time.

1. **disambiguation**: when several columns could plausibly answer a question, the environment says which one is the default.
2. **defaults and conventions**: the unwritten rules a human analyst carries in their head, active accounts unless stated otherwise, signed amounts where negative means debit made explicit.
3. **guardrails**: the columns and interpretations that look right and are wrong, marked as such before the agent reaches for them.

None of these live in the physical schema. `INFORMATION_SCHEMA` will happily tell an agent that a table has five `DATE` / `TIMESTAMP` columns; it will never say which one the business considers the time axis. That knowledge lives in people's heads and code review comments, unless something captures it as governed metadata. In my mind capture works best where drift is caught: next to the code.

## A worked example: five dates, one axis

The example used in this post is adversarial by design: a synthetic core-banking `transaction_info` table with five temporal columns: `booking_date`, `value_date`, `settlement_date`, `created_at`, `updated_at`, of which exactly one is the axis an agent should `GROUP BY` for "monthly transaction volume". Booking versus value versus settlement date is a genuine trap with regulatory consequences, and the ETL audit timestamps beside them look identical at the type level.

In *semantido v0.3.0*, the disambiguation for a primary time column is declared at table level:

```python
@semantic_table(
    description="Posted account transactions, one row per movement...",
    application_context="Amounts are signed: negative = debit...",
    time_dimension="booking_date",                 # THE primary axis
)
class TransactionInfo(SemanticDeclarativeBase):
    booking_date = Column(Date)
    booking_date_time_grain = "day"                # native resolution

    value_date = Column(Date)
    value_date_is_time_dimension = True            # a secondary axis
```

The bridge validates it at creation time: the declared axis must exist and must be a temporal column; grains are normalized to a canonical `TimeGrain` with invalid enum values failing. A grain finer than the physical type can represent raises a warning. This is how v0.3.0 reports these failures:

```
ValueError: TransactionInfo time dimension: settlemnt_date
            must be a column in the table

ValueError: TransactionInfo: booking_date_time_grain='DAILY' is not
            a valid TimeGrain. Valid values: second, minute, hour,
            day, week, month, quarter, year

UserWarning: Snapshot.snapshot_date: time_grain=hour is finer than
             the DATE column type can represent; the declared grain
             cannot be satisfied by the data.
```

The first two are errors, because a typo in an axis name or an invented grain is unambiguous drift. (Yes, `settlemnt_date` is misspelled on purpose, that typo is exactly the class of drift the validator exists to catch.) The third is a warning because a schema mid-migration is a legitimate state, the metadata may be ahead of the column type on purpose. Either way, the mistake surfaces where the author is looking, in the same commit that introduced it.

This is the library's core claim applied to time: semantics that drift from the schema are bugs, and bugs should surface at semantic layer creation, not in a consumer's SQL three tools downstream. The primary axis is a keyword on the table decorator as a design feature: a keyword can hold one value, so two primary axes on one table are impossible to declare.

It is also worth noting what the validation deliberately does *not* do: it never guesses. A table with no declared primary axis exports no primary marker because a wrong axis presented as governed metadata is worse than an absent one.

## What the exporter writes

OSI's entire first-class time vocabulary is a single boolean: `dimension.is_time`. No grain, no hierarchies, and no way to say which of several dates is primary. I compared three policies on a synthetic banking model, using semantido's real exporter.

- With time metadata **off**, zero columns are flagged; the agent guesses.
- With **naive type inference** flag everything temporal all eight columns across two tables are marked as time dimensions, including `created_at` and `updated_at`: a one-in-five signal-to-noise ratio on the transactions table.
- With the **curated** policy flag, which is the default in the v0.3 exporter, four business dates are flagged, `booking_date` carries a `PRIMARY` marker with its grain, and the audit columns are dropped entirely, with an explicit "do not use as a time axis" instruction attached.

It is worth being precise about which signal does the work, because there are three and they are not equal. The decision is driven by curated `is_time` semantics, and it decomposes into two parts solving different problems.

1. *Exclusion*, the audit part, removes false positives, cutting five candidates to three.
2. *Designation*, the primary axis, resolves the ambiguity among true positives, cutting three to one.

For the agent's task, designation seemed to be the most decisive part in the entire export, and it is exactly the one OSI does not natively express: it travels in `ai_context` instructions and a vendor extension.

`TimeGrain`, meanwhile, drives none of this comparison; every business date here is day-grained. It sits on the *vertical* axis i.e. (how far down you may aggregate). Add a month-end snapshot table, and grain becomes important: the axis is unambiguous. Different signals, different failure classes, both needed.

## Interchange: write once, import anywhere

Here is where OSI becomes a component in semantido's architecture. Because semantido's export is spec-conformant to OSI, it becomes an *input* to every tool that supports OSI. Any OSI importer, be that a warehouse building semantic views, or a BI platform, a metrics layer, an agent framework consuming semantic models, will be able to ingest the semantido-authored model into its own schema without knowing semantido exists.

That is the write-once promise: the curation happens in one governed place, in code review, and propagates outward, instead of being re-keyed into each tool's proprietary modeling UI and drifting independently in each.

Two design choices in the exporter protect that promise.

- Everything OSI core has a field for: datasets, fields, descriptions, relationships with cardinality, synonyms will map directly, so a generic importer gets a complete, correct model.
- Everything OSI core lacks a field for, and semantido provides: privacy levels, sample values, default SQL filters, the primary axis, grains go in `custom_extensions` under `vendor_name: SEMANTIDO`, and is *mirrored into `ai_context` as plain instructions* wherever it matters to an LLM.

A semantido-aware importer gets lossless round-trip material; a naive importer ignores the extensions and still receives the guidance as text; an agent reading the YAML as context gets the instructions either way.

However, extensions are extensions. Until OSI matures into *the* format, semantido will track the spec closely and map its semantics into whatever OSI natively supports.

## The complete mapping

The above claims deserve a field-by-field audit, so here is the full mapping of how semantido's semantic model translates into OSI core, concept by concept.

Each entry falls into one of five conversion classes:

1. **direct** (a native OSI field exists)
2. **restructured** (the information survives but changes shape)
3. **prose** (it lands in `ai_context` as instructions)
4. **extension** (it travels only in the semantido's `custom_extensions` block)
5. **lost**

As many big names back OSI's semantics, I would love to see how they actually map to it, that is if they had a mapping to start with.

| semantido concept | OSI core destination | conversion |
| --- | --- | --- |
| `Table.name` / schema | `dataset.name`, `dataset.source` | direct |
| `Table.description` | `dataset.description` | direct |
| `Table.synonyms` | dataset `ai_context.synonyms` | direct |
| `Column.name` | `field.name` + ANSI expression | direct |
| `Column.description` | `field.description` | direct |
| `Column.synonyms` | field `ai_context.synonyms` | direct |
| `Relationship.description` | `relationship.description` | direct |
| `Column.is_time_dimension` | `dimension.is_time` | direct |
| `Table.sql_filters` | semantido extension | extension |
| `Column.privacy_level` | semantido extension | extension |
| `Column.sample_values` | semantido extension | extension |
| `Relationship.relationship_type` | semantido extension | extension |
| FK / `references` | `relationships` from/to columns | restructured |
| `Relationship.join_condition` | relationship column pairs, deduplicated | restructured |
| `Table.primary_key` (single column) | `dataset.primary_key` (list) | restructured - composite keys truncated |
| `Column.application_rules` | field `ai_context.instructions` | prose |
| `Table.time_dimension` (primary axis) | `ai_context` "PRIMARY" note + extension | prose + extension |
| `Column.time_grain` | `ai_context` note + extension | prose + extension |
| `application_glossary` | model `ai_context.instructions` | prose - flattened |
| `application_context` + `business_context` | dataset `ai_context.instructions` | prose - two fields merge into one |
| `Column.data_type` | — | **lost** - OSI fields carry no types |

First, six of the twenty-one concepts depend wholly or partly on the semantido extension block, which is why the exporter mirrors the agent-relevant ones into `ai_context`: the extension preserves conversion consistency for round-trips.

Second, the interchange format loses information the humble Markdown export keeps, which is exactly where the serialization question stops being... academic.

## The token economics of serialization

![semantido token comparison, Markdown vs OSI](https://dragoscrintea.me/_next/static/media/3.Serialization.2mgfh_h3s7q1i.png)

Why care about token counts? Because there is a second consumer of a semantic layer besides tools: the model's context window. Here the comparison gets interesting, because semantido ships a Markdown exporter designed precisely for prompt context, and it is dramatically cheaper.

On the synthetic banking model, the Markdown export is roughly **780 tokens** against the OSI YAML's **1,719**, a **2.2×** difference for the same semantic layer. OSI's structure has real costs as prompt text: expression dialect blocks, extension envelopes, and YAML scaffolding that a tool parses happily but a context window pays for.

Cheaper is not automatically better, and a structural audit shows neither export dominates on content. Markdown carries the **data types**, exactly the information the structural map shows OSI losing, and a genuine handicap for SQL generation when absent. But the Markdown exporter today emits *none* of the structured time metadata: no primary axis, no grain, no audit demotion, no default filters, no glossary. Those signals exist in the 0.3 semantic layer; wiring them into the Markdown serializer is the obvious next step on the exporter roadmap, and the experiment below is effectively its specification.

So I’ve set up a clean experiment, worth making rather than hand-waving. Three contexts:

- Markdown as shipped
- OSI YAML as shipped
- Markdown *enriched* with exactly the missing signals as plain text

All these were fed as the only schema context to a text-to-SQL model over six probe questions, each targeting one signal, scored deterministically.

The enriched Markdown carries every signal in the matrix, including the types OSI lacks, at roughly **1,040 tokens** approximately 60% of OSI's cost. The two serializations serve two different consumers: Markdown (with the time-semantics block promoted into the exporter) for the context window, and OSI for the tool ecosystem.

The full experiment is in the repository here: [03\_md\_vs\_osi\_context](https://github.com/hikarilabs/semantido/tree/main/examples/03_md_vs_osi_context)

## Three ways an agent consumes the layer

![semantido exporters feature](https://dragoscrintea.me/_next/static/media/4.Conclusion.2gl4oo5mx-uh3.png)

"Agent-friendly" means something different in each of the three consumption paths, and the serializations do make a difference, as we have seen above.

The first path is **context**: the semantic model rendered as text in the prompt. This is where token economics dominate and the Markdown export earns its keep; every token of YAML scaffolding is a token not spent on the user's question or retrieved rows. It is also where `ai_context` mirroring matters most: "do not use as a time axis" works on any model with no parsing at all.

The second path is **interchange**: the agent lives inside a platform, a warehouse, a BI assistant that imports the OSI model into its own semantic store. The agent never sees the YAML; it benefits through the native representation the host builds from it. Here spec conformance is the moat: every downstream consumer improves at once.

The third path is **tools**: the agent queries the semantic layer live over a protocol rather than reading a snapshot. This is what an MCP server over the layer provides — the agent asks "what is the time dimension of transaction\_info?" at plan time and gets the governed answer, paying tokens only for what the current question needs. Snapshot context is inexpensive and static. Mature setups will use both, as they draw from the same synchronized layer.

## Outro

**Author semantics where the schema lives**. That is the only place drift is caught. Validation happens at creation time

**Interchange them where the stack lives**, because no single tool owns the semantic model anymore, and a spec-conformant OSI export makes every OSI importer a downstream consumer of your curation for free.

**Serialize per consumer**: token-lean Markdown into the context window, structured YAML into the toolchain, both from one source of truth.

semantido 0.3 is available now: `pip install semantido` (add `[osi]` for YAML export). Everything in this post is runnable from `examples/02_osi_time_dimension` in the repository: [02\_osi\_time\_dimension](https://github.com/hikarilabs/semantido/tree/main/examples/02_osi_time_dimension) holding the synthetic anking model with the three-strategy axis comparison, and `examples/03_md_vs_osi_context` repository: [03\_md\_vs\_osi\_context](https://github.com/hikarilabs/semantido/tree/main/examples/03_md_vs_osi_context) holding the serialization experiment.

If you maintain an OSI importer and want to test against semantido-produced models, or if you have opinions on where grain and primary axes should land in the OSI spec itself, I'd genuinely like to hear from you.

Hikari Labs helps data and AI leadership teams evaluate and implement semantic layer architecture for GenAI applications. If you are planning this decision for 2026, the advisory workshop is a two-hour structured conversation that produces a vendor shortlist and a decision framework tailored to your existing stack. [Book here.](https://dragoscrintea.me/intake-workshop)

[Subscribe to my newsletter](#newsletter-form) to stay up to date with the latest articles and open-source projects.

**Disclaimer:**

- This article is a personal reflection of my own experiences and opinions and does not represent any of my employer(s) views.
- AI was used in structuring and grammar correcting this article. I care about my readers and respect their time and keep token usage to a minimum.
- Some of the images used in this article have been generated with Gemini 3 Pro, based on the article text given in the prompt. Others are made with Excalidraw by yours truly.
- [semantido](https://pypi.org/project/semantido/) , the open-source semantic layer built for GenAI applications, is available on GitHub.