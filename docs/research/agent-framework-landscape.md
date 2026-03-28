---
name: "Agent Framework Landscape"
description: "Landscape survey of how nine major agent frameworks handle tool registration, memory, planning, and orchestration — identifying universal patterns vs. framework-specific abstractions and implications for plugin portability"
metadata:
  type: research
  sources:
    - https://langfuse.com/blog/2025-03-19-ai-agent-comparison
    - https://dspy.ai/learn/programming/tools/
    - https://docs.haystack.deepset.ai/docs/agents
    - https://docs.crewai.com/
    - https://learn.microsoft.com/en-us/semantic-kernel/frameworks/agent/agent-architecture
    - https://openai.github.io/openai-agents-python/tools/
    - https://platform.claude.com/docs/en/agent-sdk/overview
    - https://github.com/ag2ai/ag2
    - https://modelcontextprotocol.io/specification/2025-11-25
    - https://developers.llamaindex.ai/python/framework/module_guides/deploying/agents/memory/
    - https://blog.langchain.com/langchain-langgraph-1dot0/
    - https://arxiv.org/html/2510.04173v1
  related:
    - docs/research/multi-agent-coordination.md
    - docs/research/agentic-planning-execution.md
    - docs/research/tool-design-for-llms.md
    - docs/context/tool-registration-convergence.md
    - docs/context/agent-memory-tiers.md
    - docs/context/agent-framework-portability.md
---

## Summary

Nine agent frameworks (LangChain/LangGraph, CrewAI, AutoGen/AG2, Semantic Kernel, DSPy, Haystack, LlamaIndex, Claude Agent SDK, OpenAI Agents SDK) have converged on a small set of universal patterns for tool registration and memory, while diverging significantly on orchestration topology and planning strategy. MCP (Model Context Protocol) is accelerating convergence on the tool interface layer, with all major frameworks now supporting or integrating it. A plugin system that targets portability must align with the universal patterns (function-as-tool with JSON Schema, tiered memory, structured output) while remaining agnostic to framework-specific orchestration decisions.

**Key findings:**

- **Tool registration is converging.** All nine frameworks use function-as-tool with automatic JSON Schema generation from type hints and docstrings. The `@tool` decorator pattern is nearly universal. MCP provides a cross-framework interop layer adopted by every major player.
- **Memory splits into three tiers everywhere.** Short-term (conversation buffer), long-term (persistent cross-session), and semantic (vector-indexed retrieval) appear in every framework, though the abstraction level varies.
- **Planning strategy is framework-specific.** ReAct is the default in most frameworks, but plan-and-execute, ReWOO, and tree-of-thought are available as alternatives. No framework locks you into one strategy.
- **Orchestration topology is the primary differentiator.** LangGraph uses directed graphs, CrewAI uses role-based crews, AutoGen uses conversation-based patterns, OpenAI uses handoffs, Claude uses subagents. This is where frameworks diverge most.
- **A plugin must be tool-layer portable, orchestration-layer agnostic.** Define tools as decorated functions with schemas. Let the host framework handle orchestration.

## Findings

### 1. Tool Registration Patterns

Every framework surveyed converges on the same core abstraction: a Python function decorated with metadata becomes a callable tool for an LLM. The differences are surface-level syntax, not architectural.

**Universal pattern: function + decorator + schema**

| Framework | Decorator | Schema Source | MCP Support |
|-----------|-----------|---------------|-------------|
| LangChain/LangGraph | `@tool` | Type hints + docstring, optional Pydantic `args_schema` | Yes (adapter) |
| CrewAI | `@tool` | Type hints + docstring | Yes |
| AutoGen/AG2 | `register_function()` | Type hints | Yes (extension) |
| Semantic Kernel | `@kernel_function` | `[KernelFunction]` attribute + `[Description]` | Yes |
| DSPy | `dspy.Tool(fn)` | Type hints + docstring, converted to LiteLLM format | No native |
| Haystack | `@tool` or `Tool()` class | Type hints + docstring | Yes |
| LlamaIndex | `FunctionTool.from_defaults()` | Type hints + docstring | Yes |
| Claude Agent SDK | `@tool` | In-process MCP server via `create_sdk_mcp_server` | Native |
| OpenAI Agents SDK | `@function_tool` | `inspect` + `griffe` + Pydantic | Yes |

**What is universal:**
- JSON Schema as the wire format for tool parameter definitions
- Natural language descriptions drive tool selection (models choose tools from descriptions, not code)
- Type hints provide the schema source in every Python framework
- Docstrings supplement descriptions automatically
- Return values are typically serialized to strings for the LLM

**What varies:**
- Registration ceremony (decorator vs. class wrapper vs. explicit registration call)
- Whether tools are bound to agents or to a global kernel/registry
- Pydantic integration depth (OpenAI SDK and LangChain are deepest; DSPy and AutoGen are lightest)
- MCP integration maturity (Claude Agent SDK is native; others use adapters)

**MCP as the convergence layer.** Anthropic's Model Context Protocol, released November 2024, has been adopted by OpenAI, Google, LangChain, Haystack, and Microsoft. As of late 2025, there are tens of thousands of MCP servers available. The November 2025 spec update added async operations, statelessness, and a community registry. In December 2025, Anthropic donated MCP to the Linux Foundation's Agentic AI Foundation. MCP tools follow a `mcp__<server>__<tool>` naming convention and decouple tool implementation from agent reasoning.

### 2. Memory Approaches

All frameworks implement a tiered memory architecture, though they vary in how explicit or automatic the tiers are.

**Tier 1: Short-term (conversation/working memory)**
Every framework maintains a conversation buffer — the recent messages within a session. This is the minimum viable memory. LlamaIndex's `ChatMemoryBuffer` stores the last N messages fitting a token limit. LangGraph uses thread-scoped checkpointers. CrewAI maintains per-agent short-term buffers. The Claude Agent SDK scopes memory to the agent run (subagents get isolated context windows).

**Tier 2: Long-term (cross-session persistence)**
Stores information across sessions, surviving restarts. LangGraph uses MongoDB-backed checkpointers. CrewAI provides a long-term vector index per agent. LlamaIndex offers `ChatSummaryMemoryBuffer` that summarizes when conversations get too long. Semantic Kernel/Microsoft Agent Framework provides session-based state management with pluggable backends. The OpenAI Agents SDK documents a pattern using external stores for cross-session context.

**Tier 3: Semantic (vector-indexed retrieval)**
Vector-based memory for retrieving relevant past information by similarity rather than recency. LlamaIndex's `VectorMemory` stores and retrieves via a vector database. CrewAI's entity memory indexes facts about entities. LangGraph supports vector store integrations for long-term semantic retrieval. The pattern is consistent: embed memories as vectors, retrieve by similarity at query time.

**What is universal:**
- Three-tier split (short-term buffer, long-term persistent, semantic retrieval)
- Token-limited conversation windows with overflow strategies (truncation or summarization)
- Memory is per-agent in multi-agent systems (isolation by default)

**What varies:**
- Whether memory management is automatic or manual
- Backend pluggability (some frameworks are opinionated about storage; others are fully pluggable)
- Whether entity extraction is a first-class feature (CrewAI yes, most others no)
- Summarization strategies for overflow (LlamaIndex provides this built-in; others require custom logic)

### 3. Planning Strategies

Planning determines how an agent decomposes a goal into actions. Three paradigms dominate.

**ReAct (Reasoning + Acting)** — The default in most frameworks. The agent iterates through Thought, Action, Observation cycles. Each step involves an LLM call that decides the next tool to use based on accumulated observations. LangChain, DSPy (`dspy.ReAct`), LlamaIndex (`ReActAgent`), and Haystack all implement this pattern. Strengths: grounded reasoning, reduced hallucination vs. pure chain-of-thought. Weakness: requires an LLM call per tool invocation, plans only one step ahead.

**Plan-and-Execute** — Separates planning from execution. A planner LLM produces a full task decomposition upfront, then an executor carries out each step. LangGraph documents this as a first-class pattern. Strengths: more goal-directed, better for multi-step tasks. Weakness: the plan may become stale if intermediate results change the problem.

**ReWOO (Reasoning Without Observation)** — Plans the entire tool sequence upfront without waiting for intermediate observations. More token-efficient than ReAct. Available in LangGraph. Strength: faster, fewer LLM calls. Weakness: cannot adapt to unexpected intermediate results.

**Tool-calling (native function calling)** — Not a planning strategy per se, but modern LLMs (Claude, GPT-4, Gemini) support native function calling that bypasses the ReAct text-parsing loop. DSPy and LlamaIndex's `FunctionAgent` leverage this directly. The trend is away from ReAct's text-based tool parsing toward native function calling APIs.

**What is universal:**
- ReAct is available everywhere as the baseline
- Plan-and-execute is available as an alternative in graph-based frameworks
- Native function calling is replacing text-based tool parsing

**What varies:**
- Whether planning is a separate, configurable module (LangGraph, DSPy) or baked into the agent loop
- Support for plan revision (replanning after partial execution)
- Optimization — DSPy uniquely compiles and optimizes prompts for tool-calling performance

### 4. Orchestration Models

This is where frameworks diverge most. Orchestration determines how agents coordinate, delegate, and share state.

**Graph-based (LangGraph):** Agents are nodes in a directed graph. Edges define data flow. A central `StateGraph` maintains shared state. Supports conditional branching, parallel execution, and cycles. The most explicit orchestration model — every transition is defined in code.

**Role-based crews (CrewAI):** Agents have roles (researcher, writer, reviewer). A Crew groups agents and tasks, executing them sequentially or hierarchically. A manager agent can supervise, delegate, and quality-check. Flows add event-driven orchestration with conditional branching and looping.

**Conversation-based (AutoGen/AG2):** Everything is an asynchronous conversation among agents. Orchestration patterns include group chat, sequential chat, nested chat, and swarms. Custom reply methods allow arbitrary routing. Less structured than graphs but more natural for dialogue-heavy tasks.

**Handoff-based (OpenAI Agents SDK):** Agents delegate to other agents via handoffs, which are represented as tools to the LLM (e.g., `transfer_to_refund_agent`). Lightweight — no explicit graph definition needed. Agents can also be composed as tools via `Agent.as_tool()`.

**Subagent-based (Claude Agent SDK):** The parent agent spawns subagents with isolated context windows. Subagents run in parallel and return results to the orchestrator. Built-in tool allowlisting controls what each subagent can do.

**Plugin-based (Semantic Kernel):** A central Kernel manages plugins. Agents consume plugins from the kernel. The Microsoft Agent Framework (October 2025) merges this with AutoGen's patterns, adding graph-based workflows.

**Pipeline-based (Haystack):** Components connect into Pipelines with explicit data flow. The `Agent` class wraps a pipeline with a reasoning loop. Serializable and Kubernetes-ready.

**Signature-based (DSPy):** Modules compose into programs via declarative signatures. Orchestration is implicit in module composition. The compiler optimizes the whole program. Unique in treating orchestration as a compilation target.

**What is universal:**
- Supervisor/manager pattern (one agent routes to specialists) exists in every multi-agent framework
- Agent-as-tool composition (wrapping one agent as a callable tool for another)
- State isolation between agents (each agent gets its own context)

**What varies:**
- Topology (graph vs. conversation vs. crew vs. handoff vs. pipeline)
- Explicitness (LangGraph requires defining every edge; handoffs are implicit)
- State sharing mechanism (shared graph state vs. message passing vs. result aggregation)
- Whether orchestration is code-defined or LLM-decided

### 5. Universal vs. Framework-Specific Patterns

**Universal (safe to depend on):**

1. **Tool = function + schema + description.** Every framework wraps Python functions as tools with JSON Schema parameters and natural language descriptions. A plugin that exposes tools this way works everywhere.
2. **JSON Schema as the type contract.** The wire format for tool parameters is JSON Schema across all frameworks and all LLM providers.
3. **MCP as the interop protocol.** With adoption by Anthropic, OpenAI, Google, Microsoft, LangChain, and Haystack, MCP is the standard way to expose tools across framework boundaries.
4. **Conversation history as base memory.** Every framework maintains a message-based conversation buffer. Plugins can assume this exists.
5. **Structured output.** All frameworks support constraining LLM output to match a schema (via function calling, JSON mode, or grammar-based generation).

**Framework-specific (do not depend on):**

1. **Orchestration topology.** Graph edges, crew assignments, handoff declarations, and conversation routing are all framework-specific. A plugin must not assume any particular orchestration model.
2. **State management mechanism.** LangGraph's checkpointers, CrewAI's shared memory bus, Semantic Kernel's session state — these are incompatible abstractions.
3. **Planning strategy selection.** Whether an agent uses ReAct, plan-and-execute, or ReWOO is a runtime decision. Plugins should not assume a planning strategy.
4. **Agent lifecycle hooks.** Pre/post-execution hooks, middleware, and telemetry integration vary by framework.
5. **Multi-agent communication protocol.** Message passing, shared state mutation, and result aggregation work differently in every framework.

## Challenges

**Counter-evidence and tensions:**

- **MCP convergence may be overstated.** While adopted broadly, MCP implementations vary in maturity. DSPy has no native MCP support. Enterprise adoption is still early (Gartner: under 5% of enterprise apps had task-specific agents in 2025). The protocol is still evolving (2026 roadmap includes transport scalability and governance).
- **"Universal" patterns may reflect Python-ecosystem bias.** The decorator-based tool registration pattern is a Python convention. TypeScript/JavaScript frameworks (Vercel AI SDK, OpenAI Agents TS) use different idioms. The "universal" label applies within the Python agent ecosystem.
- **Memory tiers are conceptually universal but practically incompatible.** Every framework has short-term, long-term, and semantic memory, but the APIs, storage backends, and retrieval mechanisms are completely different. A plugin cannot portably read from or write to memory across frameworks.
- **Framework churn is high.** Microsoft merged AutoGen and Semantic Kernel into Microsoft Agent Framework (October 2025). AutoGen forked to AG2. CrewAI rebuilt without LangChain dependency. Today's framework-specific patterns may not survive the next consolidation cycle.

**Premortem — what could invalidate these findings:**

- A dominant framework emerges that forces its orchestration model as a de facto standard
- MCP evolution breaks backward compatibility, fragmenting the tool interop layer
- LLM providers embed orchestration directly into their APIs, making frameworks less relevant
- Agent-to-agent protocols (like Google's A2A) create a new layer that supersedes framework-level coordination

## Sources

| # | URL | Title | Author/Org | Date | Status | Tier |
|---|-----|-------|------------|------|--------|------|
| 1 | https://langfuse.com/blog/2025-03-19-ai-agent-comparison | Comparing Open-Source AI Agent Frameworks | Langfuse | 2025-03 | Active | T2 |
| 2 | https://dspy.ai/learn/programming/tools/ | Tools - DSPy | Stanford NLP / DSPy | 2025 | Active | T1 |
| 3 | https://docs.haystack.deepset.ai/docs/agents | Agents - Haystack Documentation | deepset | 2025 | Active | T1 |
| 4 | https://docs.crewai.com/ | CrewAI Documentation | CrewAI Inc | 2025 | Active | T1 |
| 5 | https://learn.microsoft.com/en-us/semantic-kernel/frameworks/agent/agent-architecture | Semantic Kernel Agent Architecture | Microsoft | 2025 | Active | T1 |
| 6 | https://openai.github.io/openai-agents-python/tools/ | Tools - OpenAI Agents SDK | OpenAI | 2025 | Active | T1 |
| 7 | https://platform.claude.com/docs/en/agent-sdk/overview | Agent SDK Overview | Anthropic | 2025 | Active | T1 |
| 8 | https://github.com/ag2ai/ag2 | AG2 (formerly AutoGen) | AG2 AI | 2025 | Active | T1 |
| 9 | https://modelcontextprotocol.io/specification/2025-11-25 | MCP Specification | Anthropic / AAIF | 2025-11 | Active | T1 |
| 10 | https://developers.llamaindex.ai/python/framework/module_guides/deploying/agents/memory/ | Memory - LlamaIndex | LlamaIndex | 2025 | Active | T1 |
| 11 | https://blog.langchain.com/langchain-langgraph-1dot0/ | LangChain and LangGraph 1.0 | LangChain | 2025 | Active | T2 |
| 12 | https://arxiv.org/html/2510.04173v1 | Open Agent Specification Technical Report | ArXiv | 2025-10 | Active | T2 |

## Claims

| # | Claim | Type | Source | Status |
|---|-------|------|--------|--------|
| 1 | All nine frameworks use function-as-tool with JSON Schema generation from type hints | Pattern | 1, 2, 3, 4, 5, 6, 7, 8, 10 | Verified |
| 2 | MCP has been adopted by OpenAI, Google, Microsoft, LangChain, and Haystack | Fact | 9, 1 | Verified |
| 3 | MCP had 97M+ monthly SDK downloads by late 2025 | Metric | 9 | Reported |
| 4 | Three-tier memory (short-term, long-term, semantic) appears in all surveyed frameworks | Pattern | 1, 4, 5, 10 | Verified |
| 5 | ReAct is the default planning strategy in most frameworks | Pattern | 2, 3, 10, 11 | Verified |
| 6 | Orchestration topology is the primary differentiator between frameworks | Analysis | 1, 11, 12 | Assessed |
| 7 | Microsoft merged AutoGen and Semantic Kernel into Microsoft Agent Framework (Oct 2025) | Fact | 5, 8 | Verified |
| 8 | Anthropic donated MCP to Linux Foundation AAIF (Dec 2025) | Fact | 9 | Verified |
| 9 | Under 5% of enterprise apps had task-specific agents in 2025 (Gartner) | Metric | 1 | Reported |
| 10 | DSPy has no native MCP support | Gap | 2 | Verified |
| 11 | Agent Spec provides a framework-agnostic configuration language for agent portability | Proposal | 12 | Active |
| 12 | Native function calling is replacing ReAct text-based tool parsing | Trend | 2, 6, 10 | Assessed |

## Key Takeaways

1. **Target the tool layer for portability.** A plugin that exposes tools as decorated Python functions with type hints, docstrings, and JSON Schema parameters will work across all nine frameworks surveyed. This is the safe, universal abstraction layer.

2. **Use MCP for cross-framework tool distribution.** MCP is the only protocol with adoption from all major LLM providers and most agent frameworks. Packaging plugin tools as MCP servers maximizes reach without framework coupling.

3. **Stay out of orchestration.** How agents coordinate (graphs, crews, handoffs, conversations) is the most framework-specific layer. A plugin should provide tools and context, not orchestration logic. Let the host framework decide how to compose and sequence.

4. **Memory is portable in concept, not in implementation.** Every framework has the same three tiers, but the APIs are incompatible. A plugin should manage its own state (files, databases) rather than writing to framework memory abstractions.

5. **Plan for framework churn.** The 2025-2026 period saw major consolidation (Microsoft Agent Framework) and forks (AG2 from AutoGen). Tight coupling to any single framework's abstractions is a liability. The universal patterns (tool-as-function, JSON Schema, MCP) are the stable ground.

## Limitations

- This survey covers the Python ecosystem primarily. TypeScript/JavaScript agent frameworks (Vercel AI SDK, OpenAI Agents TS SDK) may have different patterns.
- Framework documentation and capabilities change rapidly. Specific API details may shift between the research date and reading date.
- Enterprise adoption data is limited. The Gartner projection is a single data point.
- The survey focuses on open-source frameworks. Proprietary platforms (AWS Bedrock Agents, Google Vertex AI Agent Builder) are not deeply covered.
- MCP adoption claims rely partly on download metrics, which may not reflect production usage.

## Search Protocol

| Query | Source | Date Range | Found | Used |
|-------|--------|------------|-------|------|
| LangChain LangGraph tool registration pattern architecture 2025 2026 | Web | 2025-2026 | 10 | 2 |
| CrewAI agent framework tool registration memory orchestration architecture | Web | 2024-2026 | 10 | 2 |
| AutoGen AG2 multi-agent framework tool registration orchestration patterns 2025 | Web | 2025 | 10 | 2 |
| Microsoft Semantic Kernel agent framework plugin tool registration architecture | Web | 2025-2026 | 10 | 2 |
| DSPy framework tool use module signature architecture 2025 | Web | 2025 | 10 | 2 |
| Claude Agent SDK Anthropic tool registration orchestration architecture | Web | 2025 | 10 | 2 |
| OpenAI Agents SDK tool registration orchestration handoffs 2025 | Web | 2025 | 10 | 2 |
| Haystack AI framework pipeline tool integration agent architecture 2025 | Web | 2025 | 10 | 2 |
| LlamaIndex agent framework tool registration memory architecture 2025 | Web | 2025 | 10 | 2 |
| agent framework comparison tool registration patterns universal abstractions 2025 2026 | Web | 2025-2026 | 10 | 3 |
| MCP Model Context Protocol tool registration standard agent frameworks adoption 2025 2026 | Web | 2025-2026 | 10 | 2 |
| agent framework memory patterns short-term long-term conversation state management comparison | Web | 2025 | 10 | 2 |
| agent framework planning strategies ReAct chain-of-thought tool calling patterns comparison | Web | 2025 | 10 | 2 |
| LangChain tool decorator schema JSON function calling structured output 2025 | Web | 2025 | 10 | 1 |
| agent framework orchestration topology patterns supervisor swarm graph pipeline 2025 | Web | 2025-2026 | 10 | 2 |
| DSPy tool registration dspy.Tool ReAct module function calling | Web | 2025 | 10 | 1 |
| Anthropic Claude Agent SDK tool definition MCP integration subagent architecture documentation | Web | 2025 | 10 | 1 |
| agent framework plugin portability tool abstraction layer interoperability design patterns | Web | 2025-2026 | 10 | 2 |
| Langfuse agent framework comparison 2025 tool patterns memory orchestration | Web | 2025 | 10 | 1 |
| OpenAI Agents SDK function tool automatic schema generation Pydantic agent as tool | Web | 2025 | 10 | 1 |
