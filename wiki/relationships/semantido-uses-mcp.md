---
type: Relationship
title: "semantido uses MCP"
description: "semantido serializes its semantic layer into an MCP-compatible format so agents query governed schema meaning live at plan time — the third of its three consumption paths."
tags: ["semantido", "agentic"]
relation: uses
between: ["entities/semantido", "entities/mcp"]
generated: { by: "llm-wiki-dci/claude-opus-4-8", at: 2026-10-24T00:00:00Z }
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
  - id: "two-agents-walk-into-an-mcp-the-concept-registry-an-ontology-grade-rigor-at-sqlalchemy-decorator-cost-semantido-v0-4-1-release"
    resource: "../sources/two-agents-walk-into-an-mcp-the-concept-registry-an-ontology-grade-rigor-at-sqlalchemy-decorator-cost-semantido-v0-4-1-release.md"
    title: "Two agents walk into an mcp: the Concept Registry. Semantido v0.4.1 release."
    author: "human:dragos-crintea"
    last_modified: 2026-07-22T00:00:00Z
---

# semantido uses MCP

## Summary
[MCP](../entities/mcp.md) is semantido's live-tools consumption path. semantido serializes its
definitions into an MCP-compatible format so an agent can query the governed layer at plan time —
asking, for example, which column is a table's time dimension — rather than relying only on a static
snapshot in its prompt.[^the-semantic-layer-landscape-what-you-need-to-know-before-choosing-one][^semantics-where-the-code-lives-interchange-where-the-stack-lives-semantido-v0-3-0-release]
semantido states it was built for the MCP and agentic world.[^the-semantic-layer-landscape-what-you-need-to-know-before-choosing-one]

## Evidence
- semantido can serialize its definitions into an MCP-compatible format, giving agents contextualised schemas rather than raw table structure.[^the-semantic-layer-landscape-what-you-need-to-know-before-choosing-one]
- An MCP server over the layer is the third of three agent consumption paths (context, interchange, live tools), answering plan-time questions and paying tokens only for what the current question needs.[^semantics-where-the-code-lives-interchange-where-the-stack-lives-semantido-v0-3-0-release]
- In the federated-agents experiment, every claim an agent needs about a concept is one MCP call away.[^two-agents-walk-into-an-mcp-the-concept-registry-an-ontology-grade-rigor-at-sqlalchemy-decorator-cost-semantido-v0-4-1-release]

## Related
- [semantido](../entities/semantido.md) — the semantic layer serialized to MCP
- [MCP](../entities/mcp.md) — the protocol it targets
- [Semantic layer](../concepts/semantic-layer.md) — what MCP exposes to agents

## Source History
- [the-semantic-layer-landscape-what-you-need-to-know-before-choosing-one](../sources/the-semantic-layer-landscape-what-you-need-to-know-before-choosing-one.md) — semantido is MCP-ready
- [semantics-where-the-code-lives-interchange-where-the-stack-lives-semantido-v0-3-0-release](../sources/semantics-where-the-code-lives-interchange-where-the-stack-lives-semantido-v0-3-0-release.md) — MCP as the live-tools path
- [two-agents-walk-into-an-mcp-the-concept-registry-an-ontology-grade-rigor-at-sqlalchemy-decorator-cost-semantido-v0-4-1-release](../sources/two-agents-walk-into-an-mcp-the-concept-registry-an-ontology-grade-rigor-at-sqlalchemy-decorator-cost-semantido-v0-4-1-release.md) — one MCP call away

[^the-semantic-layer-landscape-what-you-need-to-know-before-choosing-one]: The Semantic Layer landscape, what you need to know before choosing one.. Dragos Crintea. 2026-05-17.
[^semantics-where-the-code-lives-interchange-where-the-stack-lives-semantido-v0-3-0-release]: Semantics where the code lives. Interchange where the stack lives. Semantido v0.3.0 release.. Dragos Crintea. 2026-07-10.
[^two-agents-walk-into-an-mcp-the-concept-registry-an-ontology-grade-rigor-at-sqlalchemy-decorator-cost-semantido-v0-4-1-release]: Two agents walk into an mcp: the Concept Registry, an ontology-grade rigor at SQLAlchemy-decorator cost. Semantido v0.4.1 release.. Dragos Crintea. 2026-07-22.
