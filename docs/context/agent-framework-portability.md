---
name: "Agent Framework Portability"
description: "Five rules for building agent tools and plugins that work across frameworks: target the tool layer, use MCP, stay out of orchestration, manage own state, and plan for churn"
metadata:
  type: reference
  sources:
    - https://langfuse.com/blog/2025-03-19-ai-agent-comparison
    - https://modelcontextprotocol.io/specification/2025-11-25
    - https://arxiv.org/html/2510.04173v1
  related:
    - docs/research/agent-framework-landscape.md
    - docs/context/plugin-extension-architecture.md
    - docs/context/tool-design-for-llms.md
    - docs/context/tool-registration-convergence.md
    - docs/context/agent-memory-tiers.md
---

## The Portability Problem

The agent framework ecosystem is fragmented across nine major players (LangChain/LangGraph, CrewAI, AutoGen/AG2, Semantic Kernel, DSPy, Haystack, LlamaIndex, Claude Agent SDK, OpenAI Agents SDK), each with its own orchestration model, memory API, and agent lifecycle. Building a tool or plugin that works in only one framework is a bet on that framework surviving the next consolidation cycle — a bet that has already failed for projects tightly coupled to pre-fork AutoGen or pre-1.0 LangChain.

The good news: beneath the framework-specific surface, universal patterns exist. They define the safe abstraction boundary for portable tools.

## Five Portability Rules

### 1. Target the Tool Layer

The tool interface is the one layer where all nine frameworks agree. Every framework wraps Python functions as tools with JSON Schema parameters and natural language descriptions. A plugin that exposes tools this way works everywhere.

**Safe to depend on (universal):**
- Function + schema + description as the tool contract
- JSON Schema as the wire format for parameter definitions
- Type hints as the schema source
- Natural language descriptions driving tool selection
- Structured output (constraining LLM responses to match a schema)

**Not safe to depend on (framework-specific):**
- Specific decorator syntax (`@tool` vs. `@kernel_function` vs. `@function_tool`)
- Whether tools bind to agents or to a global registry
- Pydantic integration depth
- Agent lifecycle hooks (pre/post-execution, middleware)

### 2. Use MCP for Cross-Framework Distribution

The Model Context Protocol is the only tool interop standard with adoption from all major LLM providers (Anthropic, OpenAI, Google, Microsoft) and most agent frameworks. Packaging tools as MCP servers decouples implementation from any specific framework.

MCP is not perfect — enterprise adoption is early, implementations vary in maturity, and DSPy lacks native support. But it is the closest thing to a universal tool distribution mechanism that exists. The November 2025 spec update and December 2025 donation to the Linux Foundation signal long-term commitment.

### 3. Stay Out of Orchestration

How agents coordinate is the most framework-specific layer:

- **LangGraph:** Directed graphs with explicit edges and shared state
- **CrewAI:** Role-based crews with manager delegation
- **AutoGen/AG2:** Asynchronous conversation routing
- **OpenAI Agents SDK:** Handoff-based delegation (agents as tools)
- **Claude Agent SDK:** Subagent spawning with isolated context

A plugin should provide tools and context, not orchestration logic. Let the host framework decide how to compose, sequence, and parallelize agent work. If a plugin needs multi-step workflows, expose each step as a separate tool and let the agent (or framework) decide the execution order.

### 4. Manage Your Own State

Every framework has three-tier memory (short-term, long-term, semantic), but the APIs are completely incompatible. A plugin cannot portably read from or write to framework memory.

Instead:
- Use files, databases, or other storage the plugin controls
- Accept context as tool input parameters rather than reading from agent memory
- Return structured results and let the framework decide what to persist
- Do not assume tool outputs will be stored in any particular memory tier

### 5. Plan for Framework Churn

The 2025-2026 period demonstrated that framework stability cannot be assumed:
- Microsoft merged AutoGen and Semantic Kernel into Microsoft Agent Framework (October 2025)
- AutoGen forked to AG2 under independent governance
- CrewAI rebuilt without LangChain dependency
- LangChain and LangGraph reached 1.0 with breaking changes from earlier versions

Tight coupling to any single framework's abstractions is a liability. The universal patterns — function-as-tool, JSON Schema, MCP — are the stable ground. Framework-specific adapters should be thin wrappers that can be updated or replaced independently.

## What Could Invalidate These Rules

- A dominant framework emerges that forces its orchestration model as a de facto standard (reducing the need for portability)
- MCP evolution breaks backward compatibility, fragmenting the tool interop layer
- LLM providers embed orchestration directly into their APIs, making frameworks less relevant
- Agent-to-agent protocols (like Google's A2A) create a new interop layer that supersedes framework-level coordination

## Bottom Line

Portable plugins live at the tool layer: plain functions with typed parameters, clear descriptions, JSON Schema contracts, and optional MCP packaging. Everything above that — orchestration, memory, planning strategy — belongs to the host framework. The boundary between "what the plugin provides" and "what the framework decides" is the tool interface.
