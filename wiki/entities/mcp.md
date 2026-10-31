---
type: Entity
title: "MCP (Model Context Protocol)"
description: "The protocol for exposing tools and context to AI agents; semantido serializes its semantic layer to MCP so agents query governed schema meaning at plan time."
tags: ["tool", "agentic"]
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

# MCP (Model Context Protocol)

## Overview
MCP is the protocol over which agents access tools and context. In this series it is the live-tools
consumption path for a semantic layer: [semantido](semantido.md) serializes its definitions into an
MCP-compatible format so an agent can ask the layer a question — "what is the time dimension of this
table?" — at plan time and get a governed answer, paying tokens only for what the current question
needs.[^the-semantic-layer-landscape-what-you-need-to-know-before-choosing-one][^semantics-where-the-code-lives-interchange-where-the-stack-lives-semantido-v0-3-0-release]

## Key Facts
- **Type:** tool / protocol (agent–tool interface)
- semantido can serialize its definitions into an MCP-compatible format, giving agents contextualised schemas rather than raw table structure.[^the-semantic-layer-landscape-what-you-need-to-know-before-choosing-one]
- semantido states it was "built for the MCP and agentic world."[^the-semantic-layer-landscape-what-you-need-to-know-before-choosing-one]
- An MCP server over the layer is the third of three agent consumption paths (context, interchange, live tools).[^semantics-where-the-code-lives-interchange-where-the-stack-lives-semantido-v0-3-0-release]
- In the federated-agents experiment, every claim an agent needs about a concept is "one hop (one MCP call) away."[^two-agents-walk-into-an-mcp-the-concept-registry-an-ontology-grade-rigor-at-sqlalchemy-decorator-cost-semantido-v0-4-1-release]

## Relevance
MCP is why semantido's governed metadata matters to agents in practice: it is the interface that lets
a running agent consult the layer live instead of relying only on a static snapshot in its prompt,
which is central to the "two agents walk into an MCP" interop experiment.[^two-agents-walk-into-an-mcp-the-concept-registry-an-ontology-grade-rigor-at-sqlalchemy-decorator-cost-semantido-v0-4-1-release]

## Related
- [semantido](semantido.md) — serializes to MCP ([semantido uses MCP](../relationships/semantido-uses-mcp.md))
- [Semantic layer](../concepts/semantic-layer.md) — what MCP exposes to agents

## Source History
- [the-semantic-layer-landscape-what-you-need-to-know-before-choosing-one](../sources/the-semantic-layer-landscape-what-you-need-to-know-before-choosing-one.md) — semantido is MCP-ready
- [semantics-where-the-code-lives-interchange-where-the-stack-lives-semantido-v0-3-0-release](../sources/semantics-where-the-code-lives-interchange-where-the-stack-lives-semantido-v0-3-0-release.md) — MCP as the live-tools path
- [two-agents-walk-into-an-mcp-the-concept-registry-an-ontology-grade-rigor-at-sqlalchemy-decorator-cost-semantido-v0-4-1-release](../sources/two-agents-walk-into-an-mcp-the-concept-registry-an-ontology-grade-rigor-at-sqlalchemy-decorator-cost-semantido-v0-4-1-release.md) — claims one MCP call away

[^the-semantic-layer-landscape-what-you-need-to-know-before-choosing-one]: The Semantic Layer landscape, what you need to know before choosing one.. Dragos Crintea. 2026-05-17.
[^semantics-where-the-code-lives-interchange-where-the-stack-lives-semantido-v0-3-0-release]: Semantics where the code lives. Interchange where the stack lives. Semantido v0.3.0 release.. Dragos Crintea. 2026-07-10.
[^two-agents-walk-into-an-mcp-the-concept-registry-an-ontology-grade-rigor-at-sqlalchemy-decorator-cost-semantido-v0-4-1-release]: Two agents walk into an mcp: the Concept Registry, an ontology-grade rigor at SQLAlchemy-decorator cost. Semantido v0.4.1 release.. Dragos Crintea. 2026-07-22.
