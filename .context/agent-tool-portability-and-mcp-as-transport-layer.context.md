---
name: Agent Tool Portability and MCP as Transport Layer
description: "MCP is a stateless transport layer for tool invocation, not an orchestration environment; portability lives at the tool layer, not the orchestration layer."
type: concept
confidence: high
created: 2026-04-10
updated: 2026-04-10
sources:
  - https://www.scalekit.com/blog/unified-tool-calling-architecture-langchain-crewai-mcp
  - https://arxiv.org/html/2505.02279v1
  - https://arxiv.org/pdf/2505.06817
  - https://blog.modelcontextprotocol.io/posts/2026-mcp-roadmap/
  - https://clickhouse.com/blog/how-to-build-ai-agents-mcp-12-frameworks
related:
  - docs/context/agent-memory-tier-taxonomy-and-implementation-gaps.context.md
  - docs/context/multi-agent-orchestration-patterns-and-selection-criteria.context.md
  - docs/context/agentic-resilience-infrastructure-primitives.context.md
---
# Agent Tool Portability and MCP as Transport Layer

**Portability lives at the tool layer, not the orchestration layer.** Tools implemented against MCP are callable from LangChain, CrewAI, Claude Agent SDK, AutoGen, or any other framework without bespoke adapters. Orchestration topology — state management, agent identity, access control — remains framework-specific and cannot be abstracted to the tool layer.

## What MCP Is

MCP is a JSON-RPC client-server interface for tool invocation and context ingestion. Each invocation is **atomic and stateless**. "MCP is not an orchestration environment, it's a transport layer." The same callable can run under LangChain, CrewAI, or directly via MCP with identical behavior.

This is the architectural separation that enables portability: reasoning and coordination logic live in the framework; tool definitions live below it, exposed via MCP. Changing the tool implementation updates the interface immediately — no version sync required across frameworks.

## Parallel Protocol Layers

MCP handles tool and data access. Two complementary protocols handle coordination above it:

- **A2A** — peer-to-peer task outsourcing between agents via HTTP and Server-Sent Events; launched by Google (April 2025), now under Linux Foundation with v0.3 spec and 50+ partners. This is the only agent-to-agent protocol mature enough to build against in 2025–2026.
- **ACP** — RESTful messaging for local multi-agent systems; merged into A2A under Linux Foundation in August 2025.

ANP (decentralized open-internet discovery via DIDs/JSON-LD) is a July 2025 arXiv proposal — experimental, not production-ready.

## Practical Portability Patterns

**Schema-first, framework-agnostic tool definitions** prevent version drift when logic is embedded in framework-specific layers. Define tools by their interface contract, not their runtime host.

**Dynamic tool discovery** is preferable for large tool sets: agents maintain brief availability lists and retrieve full specifications on demand via help flags or search, rather than loading all definitions upfront. This keeps context window overhead manageable.

**MCP security posture varies across frameworks.** Claude Agent SDK requires explicit allowlisting — it blocks all tools unless the `allowed_tools` property explicitly permits them. Other frameworks (Upsonic) auto-discover and enable everything by default. "MCP support" does not imply uniform behavior; portability claims require auditing the security model of each consuming framework.

## What MCP Does Not Cover

MCP cannot abstract away orchestration concerns. Agent-to-agent coordination — assigning tasks, tracking state across agents, communicating results between cooperating agents — requires A2A or equivalent protocols. Teams that equate MCP support with full portability will encounter this gap when building multi-agent workflows.

The 2026 MCP roadmap identifies remaining enterprise gaps: stateful sessions conflict with load balancers, horizontal scaling requires workarounds, audit trails and SSO integration are still maturing.

## Takeaway

Use MCP to define tools once and consume them across frameworks. Use A2A for agent-to-agent task delegation. Do not attempt to push coordination concerns into MCP — it is a tool transport, not an agent runtime.
