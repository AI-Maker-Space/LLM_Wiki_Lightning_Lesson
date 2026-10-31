---
title: "Two agents walk into an mcp: the Concept Registry, an ontology-grade rigor at SQLAlchemy-decorator cost. Semantido v0.4.1 release."
source: "https://dragoscrintea.me/articles/05-concept-registry-a-ontology-grade-rigor-at-sqlalchemy-decorator-cost"
author:
published: 2026-07-22
created: 2026-10-24
description: "semantido v0.4.1 ships a concept registry: three families of typed edges that let two agents who have never shared a schema disagree safely about what a word means, no OWL, no reasoner, ~100 lines of protocol."
tags:
  - "clippings"
---
![Hero image representing two agents.](https://dragoscrintea.me/_next/static/media/image_1.3_i1a3bwesakd.png)

## Two agents walk into an MCP: semantido v0.4.1 and the Concept Registry, ontology-grade rigor at SQLAlchemy-decorator cost

> **TL;DR** — semantido v0.4.1 ships a concept registry: three families of typed edges that let two agents who have never shared a schema disagree safely about what a word means. No OWL, no reasoner, ~100 lines of protocol.
> 
> - **Why this article** — Semantic layers tell an agent what things are called; they don't stop two agents from conflating homonyms like the EMIR vs. MiFIR "counterparty." v0.4.1 tests how little ontology you actually need to close that gap.
> - **Most important take** — Interop didn't come from a reasoner or a merged ontology. Typed mapping relations, version pins, and hierarchy declarations were enough to turn silent substitution errors into inspectable, auditable refusals.
> - **A challenging thought** — This worked on one schema pair with public anchors (FIBO, ISO 20022, GLEIF) shared by accident. The open question is whether the minimal structure generalizes — so run `examples/04_federated_agents` and try to make two agents conflate something. When you succeed, file the issue.

Upfront disclosure: the Concept Registry was purely vibe-coded.

For a while now I have been thinking about the next layer in the metaphysics continuum: semantics → ontologies. I already have semantics, what am I missing to build an ontology? And moreover, how much of an ontology do I need for a conversation between two agents to actually make "sense"?

The semantido spirit is to define everything where the action really happens, right next to the code that generates it, and v0.4.1 is the release where the concept tier becomes a first-class object.

Thus, the concept registry. This is not an ontology engine: there is no OWL, no reasoner, no Protégé artifact to keep in sync, no RDF triple store. Validation is referential only, by design. The experiment is whether a minimal structure is enough for two agents that have never shared a schema to interoperate without silently conflating meanings. Everything else in the release exists to test that hypothesis.

## The experiment: agents who have never met

> The setup: two banks. Bank A runs an EMIR reporting stack with its own registry; Bank B runs a MiFIR stack, also with its own registry. The registries share no ids, no schemas, no vocabulary agreement — the two organizations have never aligned anything, which is the only realistic assumption in wholesale banking. What they do share, incidentally rather than by coordination, is that both mapped some concepts outward to public anchors: FIBO, ISO 20022, GLEIF. This is postulated as an axiom.

> When an agent from Bank B asks Bank A's agent a question, the consumer computes alignments from those outward mappings alone. The protocol is about a hundred lines and three rules. If both sides pinned different versions of an anchor source, the verdict is capped at CANDIDATE\_REVERIFY — the anchor itself may have moved. If both concepts declared themselves narrower than the same anchor, they are siblings under a broader notion and possibly disjoint: RELATED\_NOT\_SUBSTITUTABLE. Otherwise, the verdict composes at the strength of the weaker relation. Every verdict carries its own reasoning.

Run the experiment and watch the counterparty trap not spring:

```
counterparty.emir <-> counterparty.mifir   RELATED_NOT_SUBSTITUTABLE
  fibo#FND/Parties/Parties/Counterparty: both narrower than the
  anchor — siblings under a broader notion, possibly disjoint
```

Both banks, independently, declared their counterparty concept `narrow_match` against the FIBO Counterparty, because both senses genuinely are jurisdiction-scoped narrowings of the general notion. The sibling rule fires, and the receiving agent refuses to substitute, with a reason a human can audit. Meanwhile, notional and transaction\_amount align exactly through their shared ISO 20022 anchor and flow straight through; Bank A's trade\_report, which was never mapped outward at all, yields NO\_BRIDGE and a clarifying question instead of a guess. The scoreboard the experiment prints distinguishes correct answers, silent errors, and false refusals, and the design goal is exactly this trade: convert silent errors into inspectable refusals, without drowning in false ones.

![semantido audit trail via a concept registry](https://dragoscrintea.me/_next/static/media/image_4.29rn83qizkibl.png)

Notice what did the work. Not a reasoner. Not a merged ontology. Typed mapping relations (the no-bare-pointer rule), version pins (the pin-cap rule), and hierarchy declarations. Every "pedantic" constraint from the authoring API reappears here as a safety property.

## Implementing this in code: three families of edges

![semantido concept registry - edges](https://dragoscrintea.me/_next/static/media/image_2.0peh600998sjt.png)

This section answers my first hypothesis question: how much information do I need to provide, or rather, how little can I get away with while maintaining query understanding?

A `ConceptRegistry` holds `Concept` nodes: id, label, a required definition, synonyms — and three kinds of edges radiating from them.

**Concept-to-concept edges** use a small typed vocabulary: SAME\_AS, BROADER/NARROWER, RELATED, and DISTINCT\_FROM, the explicit homonym declaration. Declaring two concepts distinct is an act of authorship, not inference:

```python
registry = ConceptRegistry("hikari.regreport")

counterparty = registry.concept(
    "counterparty",
    definition="A legal entity that is party to a financial transaction.",
)
emir = registry.concept(
    "counterparty.emir",
    label="counterparty",  # same label — deliberate homonym
    definition="Counterparty within the meaning of EMIR Art. 2(8)-(9).",
    broader=counterparty,
)
registry.concept(
    "counterparty.mifir",
    label="counterparty",
    definition="Buyer/seller identification in a MiFIR transaction "
               "report (RTS 22); legally distinct from the EMIR notion.",
    broader=counterparty,
    distinct_from=emir,
)
```

**Concept-to-external edges** are SKOS-aligned `ExternalMapping` s to outside ontologies, glossaries, or regulations such as FIBO, ISO 20022, or a DataHub glossary. First, there is no way to state a mapping without stating its relation: the helpers are `exact_match`, `close_match`, `narrow_match`, `broad_match`, and `related_match`. Second, every mapping names a version-pinned source: `fibo@2025Q3`, not "FIBO".

**Concept-to-physical edges** reuse conventions semantido users already know: `@semantic_table(concept="trade_report")` at table level, and `cpty_lei_concept = "counterparty.emir"` as a column attribute, mirroring the existing `{column}_description` pattern exactly. Bindings are validated at sync time, the same moment `time_dimension` is checked so a typo'd concept id fails your build, not your agent's answer.

In this first iteration this configuration performed really well. That does not mean we can generalize it, and this is where I would need your help as well. I would like to validate this against a wider set of use-cases, and if you happen to be looking for a lightweight agentic interop layer, semantido's concept registry might be the thing.

## The exporters' additive layout paid off

![semantido concept registry - edges](https://dragoscrintea.me/_next/static/media/image_3.3mxe3e7ecy669.png)

A registry nobody renders is a diary. In v0.4.1 the concept registry reaches every export method, and the Markdown exporter the format my own serialization benchmarks say LLMs should be reading gains the two sections the design was always aiming at.

The **Concepts** section embeds each concept with its definition, its bindings ("realized by: emir\_trade\_state.cpty\_lei"), its external mappings with pins and justifications, and its relations. It embeds only the `subset()` closure of concepts actually referenced by your tables and columns, an organization-wide registry of four hundred concepts does not bloat a six-table export.

Here is what that renders to actual exporter output from Bank A's schema in the federated-agents example, excerpted:

```markdown
## Concepts (5 in scope)

This schema realizes business concepts. The concept id is the
authoritative reference; labels may collide (see Disambiguation).

### \`counterparty.emir\` — counterparty
- **Definition**: Counterparty within the meaning of EMIR Art. 2(8)-(9).
- **Realized by**: emir_trade_state.cpty_lei
- **External**: narrower than → \`FND/Parties/Parties/Counterparty\`
  [fibo@2025Q3] — EMIR sense is jurisdiction- and instrument-scoped
- **External**: exact match → \`field:1.9\` [esma_emir@2024refit]
- **Relation**: broader → \`legal_entity\`

### \`legal_entity\` — legal entity
- **Definition**: An LEI-identified legal person or structure.
- **Realized by**: — (context only, not bound in this schema)
- **External**: exact match → \`lei\` [gleif@2026-06]
```

Note `legal_entity`: nothing in this schema binds it, yet it travels in through `counterparty.emir` 's broader edge. Every claim an agent might need about `counterparty.emir` is one hop (one MCP call) away: it is narrower than the FIBO notion (not equal to it, with the reason stated), it is exactly EMIR field 1.9 at the 2024 refit, and every anchor is pinned to a version another agent can compare against its own.

The **Disambiguation** section is generated from `find_homonyms()` and is the direct countermeasure to the negative-DDL finding:

```markdown
## Disambiguation

The surface forms below are claimed by more than one distinct
concept. Always resolve by concept id, never by a label.

### "counterparty" — 2 distinct concepts
- \`counterparty.emir\` (trades.cpty_lei): Counterparty within the
  meaning of EMIR Art. 2(8)-(9).
- \`counterparty.mifir\` (not bound here): Buyer/seller identification
  in a MiFIR transaction report (RTS 22).

Do not treat these as equivalent; do not join or compare their
columns as if they carried the same meaning.
```

This converts a silent lexical collision into an explicit context. The vocabulary tier told the model what things are called; this section tells it what it is not allowed to conflate.

## What this is not, and what's next

The alignment protocol lives in `examples/04` and is not yet ported as a semantido feature: it is a reference implementation of a pattern I want to stress-test on different use-cases.

The pitch: ontology-grade rigor at SQLAlchemy-decorator cost, now with evidence. Two registries that never met disagree safely about the meaning of a word, in a hundred lines of protocol and zero lines of OWL.

`pip install semantido`, run `examples/04_federated_agents`, and try to make two agents conflate something. When you succeed — and somewhere in the gap between anchors, someone will — file the issue. That's the experiment.

Hikari Labs helps data and AI leadership teams evaluate and implement semantic layer architecture for GenAI applications. If you are planning this decision for 2026, the advisory workshop is a two-hour structured conversation that produces a vendor shortlist and a decision framework tailored to your existing stack. [Book here.](https://dragoscrintea.me/intake-workshop)

[Subscribe to my newsletter](#newsletter-form) to stay up to date with the latest articles and open-source projects.

**Disclaimer:**

- This article is a personal reflection of my own experiences and opinions and does not represent any of my employer(s) views.
- AI was used in structuring and grammar correcting this article. I care about my readers and respect their time and keep token usage to a minimum.
- Some of the images used in this article have been generated with Gemini 3 Pro, based on the article text given in the prompt. Others are made with Excalidraw by yours truly.
- [semantido](https://pypi.org/project/semantido/) , the open-source semantic layer built for GenAI applications, is available on GitHub.