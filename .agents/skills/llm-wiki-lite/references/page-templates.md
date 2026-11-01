# Page templates

This wiki page templates for each page type.

## Source

```markdown

---
type: Source
title: "<Article / Paper Title>"
description: "<One sentence summary of what this source is about.>"
tags: ["<topic>", "<domain>"]
generated: { by: "llm-wiki-lite/1.0", at: YYYY-MM-DDTHH:MM:SSZ }
resource: "<canonical URL or DOI>"
sources:
  - id: "raw"
    resource: "../../raw/<raw-filename.ext>"
    title: "<Article / Paper Title>"
    author: "human:<author-slug>"
    last_modified: YYYY-MM-DDTHH:MM:SSZ
---

# <Article / Paper Title>

## Summary
[2-3 paragraph synthesis of the source's argument, findings, or narrative.]

## Key Claims
- <Specific claim with numbers, dates, and attribution.>[^raw]
- <Specific claim.>[^raw]

## Entities Mentioned
- [<Entity Name>](../entities/<slug>.md) — <role in this source>
- [<Entity Name>](../entities/<slug>.md) — <role in this source>

## Concepts Covered
- [<Concept Name>](../concepts/<slug>.md) — <how this source relates>
- [<Concept Name>](../concepts/<slug>.md) — <how this source relates>

## Notable Quotes
> "<Verbatim quote.>"
> — <Who said it / where in the source>

## Notes
- Connects to [<existing concept>](../concepts/<slug>.md) — <reason>

[^raw]: <Article / Paper Title>. <Author>. <Date>.

```

---

## Entity

```markdown

---
type: Entity
title: "<Entity Display Name>"
description: "<One sentence: what this entity is and why it matters.>"
tags: ["<subtype: person|company|project|tool>", "<domain>"]
generated: { by: "llm-wiki-lite/1.0", at: YYYY-MM-DDTHH:MM:SSZ }
sources:
  - id: "<source-slug>"
    resource: "../sources/<source-slug>.md"
    title: "<Source title>"
    author: "human:<author-slug>"
    last_modified: YYYY-MM-DDTHH:MM:SSZ
---

# <Entity Display Name>

## Overview
[1-2 paragraphs covering what this entity is, its background, and its significance.
Cite claims with footnotes.][^source-slug]

## Key Facts
- **Type:** person | company | project | tool
- **Founded / Created:** <date or context>[^source-slug]
- **Domain:** <what they work on>[^source-slug]
- **Affiliation / Parent:** [<Parent Entity>](../entities/<slug>.md)
- **Status:** active | inactive | acquired | deprecated
- **Notable for:** <key contributions or achievements>[^source-slug]
- **Key people:** [<Person>](../entities/<slug>.md) — <role>

## Relevance
[Why this entity matters to the topics tracked in this wiki. What role does it play
in the broader landscape? Cite evidence.][^source-slug]

## Related
- [<Related Entity>](../entities/<slug>.md) — <nature of relationship>
- [<Related Concept>](../concepts/<slug>.md) — <how this entity connects>
- [<Relationship Page>](../relationships/<slug>.md) — <what it covers>

## Source History
- [<source-slug>](../sources/<source-slug>.md) — <what this source contributed about this entity>

[^source-slug]: <Source title>. <Author>. <Date>.

```

---

## Concept

```markdown

---
type: Concept
title: "<Concept Display Name>"
description: "<One sentence definition.>"
tags: ["<domain>", "<technique|pattern|idea>"]
generated: { by: "llm-wiki-lite/1.0", at: YYYY-MM-DDTHH:MM:SSZ }
sources:
  - id: "<source-slug>"
    resource: "../sources/<source-slug>.md"
    title: "<Source title>"
    author: "human:<author-slug>"
    last_modified: YYYY-MM-DDTHH:MM:SSZ
---

# <Concept Display Name>

## Definition
[Clear, concise definition. What is this concept? Where does it come from?
Include origin or coinage if notable.][^source-slug]

## How It Works
[Explanation of the mechanism, pattern, or process. Step-by-step if applicable.
Describe inputs, outputs, and the core logic.][^source-slug]

## Key Points
- <Atomic, self-contained insight.>[^source-slug]
- <Distinguishing property or constraint.>[^source-slug]
- <Common misconception or nuance.>[^source-slug]

## Applications
[Where and how this concept is used in practice. Which entities apply it?
What problems does it solve?][^source-slug]

## Related Concepts
- [<Related Concept>](../concepts/<slug>.md) — <contrast or connection>
- [<Parent Concept>](../concepts/<slug>.md) — <this is a specialisation of>
- [<Relationship Page>](../relationships/<slug>.md) — <what it covers>

## Source History
- [<source-slug>](../sources/<source-slug>.md) — <what this source contributed>

[^source-slug]: <Source title>. <Author>. <Date>.

```

---

## Relationship

```markdown

---
type: Relationship
title: "<A Name> vs <B Name>"
description: "<One sentence stating what the relationship is and why it matters.>"
tags: ["<domain>"]
relation: compares | builds-on | uses | competes-with | part-of | acquires | supersedes | other
between: ["<id-a>", "<id-b>"]
generated: { by: "llm-wiki-lite/1.0", at: YYYY-MM-DDTHH:MM:SSZ }
sources:
  - id: "<source-slug>"
    resource: "../sources/<source-slug>.md"
    title: "<Source title>"
    author: "human:<author-slug>"
    last_modified: YYYY-MM-DDTHH:MM:SSZ
---

# <A Name> vs <B Name>

## Summary
[1-2 paragraphs explaining how these two entities or concepts relate. State the
core claim the sources make about this relationship.][^source-slug]

## Key Differences

| Dimension | [<A Name>](../entities/<a-slug>.md) | [<B Name>](../entities/<b-slug>.md) |
|---|---|---|
| <dimension, e.g. Scope> | <A's value>[^source-slug] | <B's value>[^source-slug] |
| <dimension, e.g. Approach> | <A's value>[^source-slug] | <B's value>[^source-slug] |
| <dimension, e.g. Scale> | <A's value>[^source-slug] | <B's value>[^source-slug] |

## When to Use Each

**Use <A Name> when:**
- <condition>[^source-slug]

**Use <B Name> when:**
- <condition>[^source-slug]

## Tradeoffs
- <Tradeoff or tension between A and B.>[^source-slug]
- <What choosing one over the other implies.>[^source-slug]

## Evidence
- <Explicit claim from a source about how A and B relate.>[^source-slug]

## Related
- [<Related Relationship>](../relationships/<slug>.md) — <how it connects>
- [<Related Concept>](../concepts/<slug>.md) — <relevance>

## Source History
- [<source-slug>](../sources/<source-slug>.md) — <what this source contributed to this relationship>

[^source-slug]: <Source title>. <Author>. <Date>.

```