---
name: Agent Memory Tier Taxonomy and Implementation Gaps
description: "Five memory tiers (short-term through procedural) are taxonomically stable, but production implementations vary significantly across frameworks and memory beyond short-term/long-term remains experimental."
type: concept
confidence: high
created: 2026-04-10
updated: 2026-04-10
sources:
  - https://redis.io/blog/ai-agent-memory-stateful-systems/
  - https://dev.to/foxgem/ai-agent-memory-a-comparative-analysis-of-langgraph-crewai-and-autogen-31dp
  - https://platform.claude.com/docs/en/managed-agents/overview
  - https://www.anthropic.com/engineering/managed-agents
related:
  - docs/context/agent-tool-portability-and-mcp-as-transport-layer.context.md
  - docs/context/multi-agent-shared-state-failure-mechanisms.context.md
  - docs/context/agentic-planning-hybrid-global-plan-local-react.context.md
---
# Agent Memory Tier Taxonomy and Implementation Gaps

**The standard taxonomy is stable; production implementations are not.** Five memory types are well-defined and widely cited, but frameworks implement them heterogeneously, and tiers beyond short-term and long-term remain experimental or framework-specific in production as of 2026.

## The Five-Tier Taxonomy

| Type | Purpose | Persistence | Primary Storage |
|------|---------|-------------|-----------------|
| Short-term | Immediate context, current session | In-context; resets at session end | In-process / context window |
| Long-term | Cross-session history, user preferences | External persistent store | Database / vector DB |
| Episodic | Specific past experiences with temporal context | Semantic search + ground truth | Vector DB + event logs |
| Semantic | Factual knowledge independent of experience | Structured facts + concept embeddings | Structured DB + vector DB |
| Procedural | How-to knowledge, workflow steps, decision logic | Workflow DB + similarity retrieval | Workflow DB + vector DB |

**Start with short-term and long-term memory. Add other types only as operational value justifies the added complexity.** This is the practical default from framework documentation.

## Framework-Specific Implementations

Frameworks converge on taxonomy vocabulary but diverge on implementation:

- **LangGraph**: external vector DB for long-term; LangMem toolkit for episodic, semantic, and procedural memory. Persistent checkpointing is a core platform feature.
- **CrewAI**: RAG-based short-term memory; SQLite3 for long-term; RAG-based entity memory.
- **AutoGen**: conversation message list for short-term; custom external integrations for long-term with no built-in persistence.
- **Anthropic Managed Agents**: memory is listed as "research preview" — production patterns still evolving.

## The Four-Stage Architecture for Persistent Memory

When implementing long-term or episodic memory with vector storage:

1. **Encoding** — convert content to vector embeddings using transformer models
2. **Storage** — index choice: HNSW (graph-based, high recall, higher memory cost) for precision-critical small-to-mid datasets; IVF (cluster-based, memory-efficient) for large-scale
3. **Retrieval** — approximate k-NN search to surface relevant context
4. **Integration** — format and inject retrieved context into the model's prompt

Advanced retrieval stacks combine semantic similarity, BM25 keyword search, graph traversal, and temporal signals, with cross-encoder reranking. These are available in toolkits like LangMem (LangGraph), Hindsight (AutoGen), and MemMachine, but are not standard out of the box.

## Key Implementation Gap

**Memory portability does not exist.** LangGraph's checkpointing format, CrewAI's SQLite schema, and AutoGen's custom integrations are incompatible. If an agent needs to be migrated between frameworks, memory stores must be rebuilt.

**Anthropic Managed Agents explicitly labels memory as "research preview"** — meaning even the vendor-native memory system lacks production stability guarantees.

## Takeaway

Use the five-tier taxonomy as a design vocabulary and planning tool. In production, implement short-term memory via context window management and long-term memory via an external persistent store with vector retrieval. Defer episodic, semantic, and procedural tiers until the use case demonstrably requires them. Do not assume memory portability across frameworks.
