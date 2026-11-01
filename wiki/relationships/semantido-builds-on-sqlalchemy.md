---
type: Relationship
title: "semantido builds on SQLAlchemy"
description: "semantido is implemented as semantic decorators on SQLAlchemy models, which is what makes it application-native: meaning lives in the same file and deployment as the schema."
tags: ["semantido", "python"]
relation: builds-on
between: ["entities/semantido", "entities/sqlalchemy"]
generated: { by: "llm-wiki-lite/1.0", at: 2026-10-24T00:00:00Z }
sources:
  - id: "the-semantic-layer-landscape-what-you-need-to-know-before-choosing-one"
    resource: "../sources/the-semantic-layer-landscape-what-you-need-to-know-before-choosing-one.md"
    title: "The Semantic Layer landscape, what you need to know before choosing one."
    author: "human:dragos-crintea"
    last_modified: 2026-05-17T00:00:00Z
  - id: "semantics-where-the-code-lives-interchange-where-the-stack-lives-semantido-v0-3-0-release"
    resource: "../sources/semantics-where-the-code-lives-interchange-where-the-stack-lives-semantido-v0-3-0-release.md"
    title: "Semantics where the code lives. Interchange where the stack lives. Semantido v0.3.0 release."
    author: "human:dragos-crintea"
    last_modified: 2026-07-10T00:00:00Z
---

# semantido builds on SQLAlchemy

## Summary
semantido does not run as a separate service; it extends the [SQLAlchemy](../entities/sqlalchemy.md)
models a Python application already has with semantic decorators, so a table's definition and its
meaning live in the same file.[^the-semantic-layer-landscape-what-you-need-to-know-before-choosing-one]
This is the design choice that makes semantido "application-native" — the semantic definitions deploy
with the application and inherit its code review, branch protections and CI/CD refresh.[^the-semantic-layer-landscape-what-you-need-to-know-before-choosing-one]

## Evidence
- semantido extends SQLAlchemy models, the ORM most Python data applications already use, with semantic decorators rather than introducing a new service.[^the-semantic-layer-landscape-what-you-need-to-know-before-choosing-one]
- A metric is a decorated Python method on the SQLAlchemy class it belongs to, not a separate YAML file in another repository.[^the-semantic-layer-landscape-what-you-need-to-know-before-choosing-one]
- The `@semantic_table(...)` decorator and column attributes are declared on SQLAlchemy models and validated against the physical schema at sync time.[^semantics-where-the-code-lives-interchange-where-the-stack-lives-semantido-v0-3-0-release]

## Related
- [semantido](../entities/semantido.md) — the semantic layer
- [SQLAlchemy](../entities/sqlalchemy.md) — the ORM it builds on
- [Semantic drift](../concepts/semantic-drift.md) — what this coupling prevents

## Source History
- [the-semantic-layer-landscape-what-you-need-to-know-before-choosing-one](../sources/the-semantic-layer-landscape-what-you-need-to-know-before-choosing-one.md) — application-native design on SQLAlchemy
- [semantics-where-the-code-lives-interchange-where-the-stack-lives-semantido-v0-3-0-release](../sources/semantics-where-the-code-lives-interchange-where-the-stack-lives-semantido-v0-3-0-release.md) — decorators validated at sync time

[^the-semantic-layer-landscape-what-you-need-to-know-before-choosing-one]: The Semantic Layer landscape, what you need to know before choosing one.. Dragos Crintea. 2026-05-17.
[^semantics-where-the-code-lives-interchange-where-the-stack-lives-semantido-v0-3-0-release]: Semantics where the code lives. Interchange where the stack lives. Semantido v0.3.0 release.. Dragos Crintea. 2026-07-10.
