---
name: "Agent Memory Tiers"
description: "The universal three-tier memory architecture (short-term, long-term, semantic) found in every major agent framework, why the tiers are conceptually portable but practically incompatible, and implications for plugin state management"
metadata:
  type: reference
  sources:
    - https://langfuse.com/blog/2025-03-19-ai-agent-comparison
    - https://developers.llamaindex.ai/python/framework/module_guides/deploying/agents/memory/
    - https://docs.crewai.com/
    - https://learn.microsoft.com/en-us/semantic-kernel/frameworks/agent/agent-architecture
  related:
    - docs/research/agent-framework-landscape.md
    - docs/context/agent-state-persistence.md
    - docs/context/context-window-management.md
    - docs/context/tool-registration-convergence.md
    - docs/context/agent-framework-portability.md
---

## The Three Tiers

Every major agent framework implements the same three-tier memory architecture. The taxonomy is universal even when the implementations are completely incompatible.

### Tier 1: Short-Term (Conversation/Working Memory)

The recent messages within a session — the minimum viable memory. Every framework maintains a conversation buffer, typically token-limited with overflow handling.

- **LlamaIndex:** `ChatMemoryBuffer` stores the last N messages fitting a token limit
- **LangGraph:** Thread-scoped checkpointers maintain per-conversation state
- **CrewAI:** Per-agent short-term buffers within a crew execution
- **Claude Agent SDK:** Memory scoped to the agent run; subagents get isolated context windows
- **OpenAI Agents SDK:** Conversation history passed through the agent loop

Short-term memory is always per-agent in multi-agent systems. Isolation is the default — agents do not share conversation buffers unless explicitly configured to do so.

### Tier 2: Long-Term (Cross-Session Persistence)

Information that survives restarts and spans multiple sessions. This is where frameworks diverge most in implementation.

- **LangGraph:** MongoDB-backed checkpointers for durable state
- **CrewAI:** Long-term vector index per agent, persisted across runs
- **LlamaIndex:** `ChatSummaryMemoryBuffer` summarizes when conversations grow too long
- **Semantic Kernel:** Session-based state management with pluggable backends
- **OpenAI Agents SDK:** Documented patterns using external stores (no built-in persistence)

The key tension: some frameworks auto-manage long-term memory (CrewAI), while others treat it as bring-your-own-storage (LangGraph, OpenAI). This affects how much control developers have over what gets persisted and how.

### Tier 3: Semantic (Vector-Indexed Retrieval)

Retrieving relevant past information by similarity rather than recency. This tier uses vector embeddings to find contextually relevant memories regardless of when they were created.

- **LlamaIndex:** `VectorMemory` stores and retrieves via a vector database
- **CrewAI:** Entity memory indexes facts about named entities for later retrieval
- **LangGraph:** Vector store integrations for long-term semantic retrieval

The pattern is consistent: embed memories as vectors, retrieve by cosine similarity at query time. But whether entity extraction is a first-class feature (CrewAI) or requires custom implementation (most others) varies significantly.

## Universal Properties

Three properties hold across all frameworks:

1. **Token-limited windows with overflow strategies.** Every framework handles the reality that conversation history eventually exceeds the context window. The strategies are truncation (drop oldest messages) or summarization (compress history into a summary). Most frameworks support both.

2. **Per-agent isolation in multi-agent systems.** Each agent gets its own memory by default. This prevents one agent's context from polluting another's reasoning. Sharing state between agents requires explicit mechanisms (shared graph state, message passing, or result aggregation).

3. **Recency bias in default behavior.** Without semantic memory, agents default to the most recent messages. This makes them effective at continuing a conversation but poor at recalling relevant information from earlier in a long session.

## The Portability Problem

The three tiers are conceptually universal but practically incompatible. A plugin cannot portably read from or write to memory across frameworks because:

- **APIs differ completely.** LangGraph checkpointers, CrewAI memory objects, and LlamaIndex memory buffers have no shared interface.
- **Storage backends are framework-chosen.** Some frameworks are opinionated (CrewAI picks the vector store); others are fully pluggable (LangGraph). A plugin cannot assume what backend exists.
- **Retrieval semantics vary.** What "retrieve relevant context" means — recency-weighted, similarity-scored, entity-filtered — depends on the framework's memory implementation.

## Implications for Plugins

Because framework memory is not portable, a plugin that needs to persist or retrieve state should:

1. **Manage its own state.** Use files, databases, or other storage the plugin controls directly. Do not write to framework memory abstractions.
2. **Accept context as input parameters.** Rather than reading from the agent's memory, accept relevant context as tool arguments that the agent passes explicitly.
3. **Return structured results.** Let the framework decide what to store in memory from the tool's output. The plugin should not assume its output will be persisted.

This aligns with the broader portability principle: plugins own their data; frameworks own their memory.
