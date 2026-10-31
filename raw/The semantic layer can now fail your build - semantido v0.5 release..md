---
title: "The semantic layer can now fail your build - semantido v0.5 release."
source: "https://dragoscrintea.me/articles/06-the-semantic-layer-can-now-fail-your-build"
author:
published: 2026-08-28
created: 2026-10-24
description: "v0.5 is the release where semantido stops being a descriptor and starts enforcing it. the three features of this release are grain - at which a concept identifies itself, a separate groundings document splitting meaning from deployment bindings and a linter that runs a sqlglot with ten static checks."
tags:
  - "clippings"
---
![Hero image representing multiple gates of a semantic layer.](https://dragoscrintea.me/_next/static/media/06_article_hero.459mkgq1txcau.jpg)

## TLDR;

- **Why this article**: semantido `v0.3` gave the layer a concept of time, `v0.4` gave it a concept registry, both authoring mechanisms. `v0.5` adds the concept of a `grain`, a standalone groundings document and `semantido.lint`, three things that provide the base guardrails of a semantic layer
- **Most important take**: a semantic layer that advises only, it's just documentation, and documentation drifts quickly. `v0.5` fails your CI build, if any of the guardrails trigger.
- **A challenging thought**: the most expensive joins are the ones that are semantically legal. Enforcement can only catch the contradictions you were disciplined enough to declare. A quiet linter means either a clean layer or an under-specified registry.

So far every semantido release has made meaning *easier to write*. `v0.3` provided the time dimension; `v0.4` gave concepts a registry so that two agents with completely different schemas could disagree safely about the meaning of a query. Both of them are authoring mechanisms.

But somewhere along the lines, when working on semantido's Apache Ossie integration, a full agentic loop for EMIR/MiFIR, and a security master example integration, this version was not designed as a coherent release. The implementation of the concept registry was purely vibe-coded, spec-driven development, more like a dart shot and see where it lands.

However, this turned out to be quite a trove when tested extensively across the three use cases mentioned above.

What v0.5 adds:

## grain: the level at which a concept identifies its subject

Let's take the `Concept.grain` example present in the security master use-case implementation of semantido.

```python
isin = registry.concept(
    "isin",
    "ISO 6166 identifier. Identifies an issue — one security as issued — "
    "irrespective of where it trades.",
    grain="issue",
)

ric = registry.concept(
    "ric",
    "Refinitiv Instrument Code. Identifies a listing on one venue.",
    grain="listing",
    distinct_from=isin,
)
```

In this scenario, an ISIN identifies an issue, a RIC identifies a listing, and a UPI identifies a product. These are not synonyms; they are more like cardinalities when expressed in a database schema. As an example, let's take one instrument: Vodafone Group plc ordinary shares, `ISIN GB00BH4HKS39`, counted three times, once at each grain:

```
ONE instrument, as each grain counts it
  issue grain   (ANNA register rows)   : 1
  listing grain (Bloomberg FIGIs)      : 3
  listing grain (Refinitiv RICs)       : 4
```

This is interpreted as one *issue* (as financial instrument issuance) listed on three venues covered by Bloomberg and four venues covered by Refinitiv.

```sql
SELECT ... FROM bloomberg_feed b JOIN refinitiv_feed r ON b.isin = r.isin
```

The result:

```
-> 12 rows for 1 instrument   (3 listings x 4 listings)
```

The mechanism is quite straightforward, ISIN is not a key on either side. Bloomberg has FIGI, and Refinitiv has RIC, ISIN is a column on both, and repeated for each venue entry. Thus `ON b.isin = r.isin` is a many-to-many join, and an equi-join over a repeated key will emit **every pair** whose keys match. So three matches on the left and four on the right are twelve rows (rows left x rows right).

The matrix is shown below, courtesy of Claude.

```
FIGI          venue        px   RIC       venue        px  =?   classification
------------------------------------------------------------------------------
BBG00B2VFT35  XLON      74.82   VOD.L     XLON      74.82  ==   MEANINGFUL — like for like
BBG00B2VFT35  XLON      74.82   VOD.MI    XMIL       0.87  <>   FALSE BREAK — different venues
BBG00B2VFT35  XLON      74.82   VODl.CHI  CHIX      74.80  <>   FALSE BREAK — different venues
BBG00B2VFT35  XLON      74.82   VODl.DE   XETR       0.87  <>   FALSE BREAK — different venues
BBG00KDBWTF1  XETR       0.87   VOD.L     XLON      74.82  <>   FALSE BREAK — different venues
BBG00KDBWTF1  XETR       0.87   VOD.MI    XMIL       0.87  ==   FALSE PASS — agrees by coincidence
BBG00KDBWTF1  XETR       0.87   VODl.CHI  CHIX      74.80  <>   FALSE BREAK — different venues
BBG00KDBWTF1  XETR       0.87   VODl.DE   XETR       0.87  ==   MEANINGFUL — like for like
BBG00LMR8QT4  XMIL       0.87   VOD.L     XLON      74.82  <>   FALSE BREAK — different venues
BBG00LMR8QT4  XMIL       0.87   VOD.MI    XMIL       0.87  ==   MEANINGFUL — like for like
BBG00LMR8QT4  XMIL       0.87   VODl.CHI  CHIX      74.80  <>   FALSE BREAK — different venues
BBG00LMR8QT4  XMIL       0.87   VODl.DE   XETR       0.87  ==   FALSE PASS — agrees by coincidence

   7  FALSE BREAK — different venues
   2  FALSE PASS — agrees by coincidence
   3  MEANINGFUL — like for like

signal: 3/12 rows = 25%
```

What the reconciliation wants is the diagonal, i.e., where the venues agree. London against London, Xetra against Xetra, Milan against Milan. What the join did is exactly the opposite, it computed the whole matrix. Everything else beside the diagonal compares the price in one venue against another, which was not the intent of this ask.

Seven of the rows disagree and are raised as `BREAKS`. London quotes 74.82 and Xetra 0.87 about a factor of 86 off.

If we look closer to this matrix, we see a hidden agreement in the form of \`FALSE PASS → Xetra against Milan. They agree, but simply because they quoted the same price in the same currency that day. The fan-out slips in comparisons that were never valid, and if any of those pairs had a genuine discrepancy, they would clear the check silently. These types of phantom breaks cost hours, and in an agentic case these errors will compound across its workflows.

No error is raised because, technically, nothing is broken. Query planner, type checker, the linter, or schema registry all are a faithful description of the data. It's the fact that ISIN counts issuance whereas FIGI and RIC count listings. This is getting worse when the matrix gets bigger.

```
BBG  RTR   rows  useful  noise  signal
  3    4     12       3      9     25%
  5    6     30       5     25     17%
  8   11     88       8     80      9%
 12   15    180      12    168      7%
```

Asking on the right grain would produce the desired answer, collapsing twelve rows to one and increasing the accuracy from 25% to 100%.

```sql
ON b.isin = r.isin AND b.venue = r.venue WHERE b.venue = 'XLON'
-- -> 1 row: ('GB00BH4HKS39, 74.82, 74.82)
```

Declaring a grain is the first step toward making this distinction machine-readable; however, on its own it does not catch the above query.

The grain field is free-form as semantido won't ship a grain taxonomy because those are exactly what the domain will provide, i.e. `issue` / `listing` / `product` is the security master idiom and `trade` / `position` / `account` is the clearing idiom. The linter compares the **grain** strings, two concepts declare the same grain, or they don't.

## Groundings: separating what a thing means from where it currently lives

The second feature in this release is a file split between **concept** and **grounding**.

A **concept** is the *portable meaning*. It changes when the business changes its mind, with a governance attached to it.

A **grounding** is a *deployment fact*, the binding of one **concept** to its physical tables and columns that are realising it. Groundings change at schema migration speed. For example, move a book from Calypso to Murex and every grounding in the domain is rewritten, whilst no concept definition changes.

having both in one file forces meaning to inherit the infrastructure cadence. v0.5 separates them.

```python
from semantido.exporters import to_groundings_yaml, to_groundings_file, load_groundings

print(to_groundings_yaml(layer))
```
```yaml
format: semantido/groundings
version: '1'
namespace: secmaster
groundings:
  isin:
    definition_checksum: 728c544e1eb5
    columns:
    - bloomberg_feed.isin
    - refinitiv_feed.isin
  ric:
    definition_checksum: 7f343fda473f
    tables:
    - refinitiv_feed
    columns:
    - refinitiv_feed.ric
```

Definitions:

- an **anchor** is a single physical reference inside a grounding, such as a `table.name` or a `table.column` pair. Anchors are what are checked for existence.
- the **grounding document** is a *derived* artifact, it's not maintained by hand. The groundings are authored implicitly every time `concept="isin"` appears on a column.
- **definition checksum** is a stable fingerprint of a concept definition text, recorded at the moment the grounding was captured. this exists to detect the failure that is always caught later in reviews: the definition was rewritten in the registry, but the column bindings were never updated, and every downstream consumer is reading a column aliases a meaning no longer exists. The checksum guards this.

### Where groundings sit: the three-tier picture

![Three tiers, three owners, three rates of change](https://dragoscrintea.me/articles/06-the-semantic-layer-can-now-fail-your-build/three_tiers_concept.svg)

Groundings are actually not a tier in itself, it's an edge between the two of them. Tier 1 says ISIN identifies an `issue`. Tier 3 says `bloomberg_feed.isin` is a VARCHAR(12). The grounding is the claim that connects them, and it's the only one that has no single owner. Governance owns the concept, the production system owns the column; the binding between them is the one who wrote the decorator. This is what I’ve always seen degrading with time if the teams which implemented that are lazy and not updating it when the meaning changes, or even worse, not having it at all. This is why v0.5 makes it explicit with its own checksum.

In v0.5 `concepts.yaml` is Tier 1. The decorated models are Tier 2. `grounding.yaml` is the edge, written down so it can be checked.

The Tier 2 example in the diagram is the one I will point to someone that asks what a semantic layer is **for**: "UK equity RICs quote in pence whilst the ISIN level record is denominated in GBP." No DDL will ever contain that sentence, no schema registry will infer it, and without it every cross-venue price comparison will produce a hundred-fold break.

## semantido.lint: the check set, and two severities

The third feature is the one that makes the first two enforceable. `semantido.lint` is a static checker built on sqlglot and parses the semantic layer and the joins it declares without a database connection and without executing anything.

```python
from semantido.lint import lint_layer

for finding in lint_layer(layer, groundings="groundings.yaml"):
    print(finding.code, finding.severity.value, finding.location, finding.message)
```

A **Finding** carries four fields: `code`, `severity`, `location` and `message`. A **Severity** has two types `ERROR` and `WARNING` which gates a CI process. `ERROR` must fail whereas `WARNINGS` are okay to pass but check them out anyway.

| Code | Severity | What it catches |
| --- | --- | --- |
| SL001 | error | `sql_filters` that don't parse |
| SL002 | error | filters referencing unknown tables or columns |
| SL003 | error | join conditions that don't parse, or use unqualified/unknown columns |
| SL004 | warning | sample values that contradict the declared column type |
| SL005 | warning | one synonym claimed by multiple tables or columns |
| SL006 | warning | two concepts sharing a surface form with no `DISTINCT_FROM` edge |
| SL007 | error | groundings whose anchors have vanished, or whose checksum has drifted |
| SL008 | error | joins equating columns bound to concepts of **different grain** |
| SL009 | error | joins equating concepts asserted **`DISTINCT_FROM`** |
| SL010 | error | `DISTINCT_FROM` concepts both claiming the same **`skos:exactMatch`** |

This table evolved over three minor releases of v0.5, with the latest addition of SL009.

Let's unpack them, and in particular the last three, which will fire in specific order.

### SL007 is the ground check.

```
SL007 error   groundings.ric   anchor column 'refinitiv_feed.ric_code' no longer
exists in the layer
SL007 error   groundings.ric   definition_checksum drift: the definition changed
after this grounding was recorded (recorded deadbeefcafe, current 7f343fda473f)
— re-review the binding and regenerate the groundings file
```

Two different failures are invisible throughout the pipeline:

1. The first is a *migration* that did not update the documentation.
2. The second is a *meaning drift*, the definition moved, and the binding didn't follow.

### SL008 owns the mismatch-scheme family.

In releasing v0.5 and testing it against the EMIR/MiFIR synthetic data, SL008 did not fire, i.e., it did not catch the fan-out described at the beginning of this article. Run against `b.isin = r.isin` it is silent; both sides have the concept `isin` and grain `issue`. A join will fan-out if its key matches on both sides. Different grains will imply different schema identifiers, which implies a different value space resulting in an **empty set**, shown below courtesy of Claude.

| Join | Grains | SL008 | Rows returned |
| --- | --- | --- | --- |
| `isin = ric` | issue vs listing | fires | 0 |
| `uti = tvtic` | contract vs execution | fires | 0 |
| `isin = isin` | issue vs issue | silent | 12 |
| `claim_id = claim_id` | claim vs claim | silent | fan-out |

The fan-out is outside its reach.

The flagship case for the whole concept registry is the **Counterparty homonym**. Under EMIR, a counterparty is either entity party to a derivative contract. Under MiFIR, it's the market-side entity you faced, a client you dealt *for* is not a counterparty, it's the buyer or seller. Two concepts, one word, both columns holding an LEI.

Declare that properly, join across it, and lint it:

```
findings: 1
  SL008 relationships[1] | grain-mismatched join: uti (contract) vs tvtic (execution)
```

The grain crossing fires. The counterparty join doesn't.

### SL009 catches joins between concepts declared as DISTINCT\_FROM regardless of their grain.

SL009 was added in v0.5.3 precisely because of this, it fires whenever a join equality connects two concepts the registry asserts are `DISTINCT_FROM` regardless of grain.

```
SL009 error relationships[0]
  join equates concepts asserted DISTINCT_FROM: emir_trade_report.other_cpty_lei
  is 'counterparty.emir' but mifir_transaction_report.market_cpty_lei is
  'counterparty.mifir' — these are different concepts that share a surface
  form; joining them equates things the registry says are distinct
```

The severity is marked as `ERROR`. If at join time a `DISTINCT_FROM` exists, this contradicts a hard declaration and must fail.

### SL010 The FIBO mapping

`skos:exactMatch` is symmetric **and transitive**. So if two concepts both claim an exactMatch to the same external IRI, SKOS entails that they are interchangeable with each other. Declare a `DISTINCT_FROM` edge between them as well, and the registry now asserts both that they are distinct and that they are the same:

```python
emir = registry.concept("counterparty.emir", "...", label="Counterparty",
    external=exact_match("fibo", FIBO_COUNTERPARTY))
mifir = registry.concept("counterparty.mifir", "...", label="Counterparty",
    distinct_from=emir,
    external=exact_match("fibo", FIBO_COUNTERPARTY))   # contradiction
```

An external reasoner over the exported Turtle would reject that. `semantido` accepted it silently until 0.5.3.

```
SL010 error registry.counterparty.emir
  contradictory mapping: 'counterparty.emir' and 'counterparty.mifir' are
  asserted DISTINCT_FROM, but both claim exactMatch to '…/Counterparty'.
  skos:exactMatch is transitive, so this entails the two concepts are
  interchangeable. Use closeMatch or broadMatch for a regime-specific
  reading of a shared external concept
```

`skos:closeMatch` is deliberately *not* transitive, exactly so that similarity doesn't propagate across schemes. Two distinct concepts may legitimately closeMatch the same external concept, and SL010 stays silent for closeMatch, broadMatch, narrowMatch, and relatedMatch. Which is also the better modeling: neither regime's sense *is* FIBO's general Counterparty, each is a narrower, regime-scoped reading.

SL010 is the first check that compares an **external** claim against an **internal** one. Every check before it looks inside a single kind of claim: SQL against schema, groundings against definitions, concepts against each other. This one sits between the registry and the outside world, which extends the linter's founding argument; these are exactly the places everything starts to drift slowly but surely.

### The homonym and how to catch one

SL006 / SL008 / SL009 form now a complete triangle around the homonym problem: one looks for a collision, the other catches a cardinality error, and the last one catches notation errors.

## Before and after. v0.4 -> v0.5

None of the above is a real *new capability* in the sense that v0.4 could not express it. It actually did very well in prose. The difference is what the machine can act on.

### Grain

`**v0.4**`. `Concept` had six fields: `id`, `label`, `definition`, `synonyms`, `mappings`, `relations`. Grain was, however, implicitly and **not** explicitly defined, which is to say more prompt engineering inside a governance rule. It reads as a warning label, and it works on a LLM model in a good mood. It cannot be queried, diffed not enforced. Two concepts, as shown below, declaring in prose "issue grain" have no computable relationship between them.

```python
isin = registry.concept(
    "isin",
    "ISO 6166 identifier. IMPORTANT: issue grain — one security as issued, "
    "irrespective of venue. Do NOT join to venue-level identifiers.",
)
ric = registry.concept(
    "ric",
    "Refinitiv Instrument Code. IMPORTANT: listing grain — one venue. Many "
    "RICs per ISIN is expected and is NOT a break.",
    distinct_from=isin,
)
```

`**v0.5**` Same declaration with an explicit `grain` field.

```python
isin = registry.concept("isin", "ISO 6166 identifier. Identifies an issue …", grain="issue")
ric  = registry.concept("ric",  "Refinitiv Instrument Code …", grain="listing", distinct_from=isin)
```

The Markdown an agent receives in its context has a structured line rather than prose with capitals and negations.

```
### \`isin\` — isin
  - **Definition**: ISO 6166 International Securities Identification Number …
+ - **Grain**: issue
  - **Realized by**: bloomberg_feed.isin, refinitiv_feed.isin
  - **Relation**: distinct from → \`figi\`
```

`grain` defaults to `None` so nothing breaks if you choose not to use it. Concepts without a declared grain are invisible to the grain check.

### Groundings

`v0.4` did not have any grounding artifact. Granted concept-to-column binding existed the `concept=` decorator produced them, but they were rendered together with definitions in the Markdown via the `Realized by`, thus a schema migration would produce a diff in an ontology document.

`v0.5` produces a standalone document generated on demand.

```python
to_groundings_file(layer, "groundings.yaml")
```

The Markdown context still carries the `Realized by`, as an agent will still require it. The split is at the **governance** level, `concepts` and `groundings` have now their own separate files with separate review and change cadence paths. This will let a Calypso-to-Murex migration rewrite every binding without touching a single definition.

### Enforcement

`v0.4` nothing of the kind. `semantido.lint` does not exist.

`v0.5` the layer went from a document to an artifact failing a release.

```
SL008 error   relationships[0]     grain-mismatched join …
SL007 error   groundings.ric       definition_checksum drift …
```

## The semantic layer gates in semantido.

A realization in experimenting with v0.5 came from observing how an agent interacts with the layer and brought a final guardrail in place. Each subsystem validates itself, SQLAlchemy checks the schema, the registry checks its graph, the exporters check their formats. But nothing actually validated the cross-reference between them.

![Three tiers, three gates — two of them ship in v0.5](https://dragoscrintea.me/articles/06-the-semantic-layer-can-now-fail-your-build/gates.svg)

Two guardrails are shipped now. `definition_checksum` guards the meaning: a concept definition moved while its grounding still claims the old one. `semantido.lint` guards the model internal consistency: every claim the layer makes about itself has to hold (see SL008).

The third guardrail is a part of `v0.6` release. Detecting that an *external* structure source has changed under you, a schema registry is evolving; a vendor adding a new column would require the library to have a notion of an external source authority.

## Outro

The measurements show that curated semantics beat a raw DDL hold. Now semantido can safely detect and prevent a layer from silently degrading between the day it's written and the day someone queries it. This is by far one of the main causes of drift in current systems which would be exacerbated n-fold in agentic ones.

`pip install semantido` and give it a try and... a GitHub star.

Hikari Labs helps data and AI leadership teams evaluate and implement semantic layer architecture for GenAI applications. If you are planning this decision for 2026, the advisory workshop is a two-hour structured conversation that produces a vendor shortlist and a decision framework tailored to your existing stack. [Book here.](https://dragoscrintea.me/intake-workshop)

[Subscribe to my newsletter](#newsletter-form) to stay up to date with the latest articles and open-source projects.

**Disclaimer:**

- This article is a personal reflection of my own experiences and opinions and does not represent any of my employer(s) views.
- AI was used in structuring and grammar correcting this article. I care about my readers and respect their time and keep token usage to a minimum.
- Some of the images used in this article have been generated with Gemini 3 Pro, based on the article text given in the prompt. Others are made with Excalidraw by yours truly.
- [semantido](https://pypi.org/project/semantido/) , the open-source semantic layer built for GenAI applications, is available on GitHub.