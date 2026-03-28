---
name: "Tool Registration Convergence"
description: "How nine major agent frameworks converged on function-as-tool with JSON Schema, the decorator registration pattern, and MCP as the cross-framework interop layer"
metadata:
  type: reference
  sources:
    - https://langfuse.com/blog/2025-03-19-ai-agent-comparison
    - https://modelcontextprotocol.io/specification/2025-11-25
    - https://dspy.ai/learn/programming/tools/
    - https://openai.github.io/openai-agents-python/tools/
    - https://platform.claude.com/docs/en/agent-sdk/overview
  related:
    - docs/research/agent-framework-landscape.md
    - docs/context/tool-design-for-llms.md
    - docs/context/plugin-extension-architecture.md
    - docs/context/agent-memory-tiers.md
    - docs/context/agent-framework-portability.md
---

## The Universal Tool Pattern

Every major Python agent framework — LangChain/LangGraph, CrewAI, AutoGen/AG2, Semantic Kernel, DSPy, Haystack, LlamaIndex, Claude Agent SDK, and OpenAI Agents SDK — has converged on the same core abstraction: a Python function decorated with metadata becomes a callable tool for an LLM.

The registration ceremony varies (decorator vs. class wrapper vs. explicit call), but the architecture is identical:

1. **Function** — a standard Python function with typed parameters
2. **Decorator/wrapper** — `@tool`, `@kernel_function`, `@function_tool`, `dspy.Tool(fn)`, or `FunctionTool.from_defaults()`
3. **Schema** — JSON Schema generated automatically from type hints and docstrings
4. **Description** — natural language text that the LLM uses for tool selection

This is not coincidence. LLM providers (Anthropic, OpenAI, Google) all accept tool definitions as JSON Schema, so frameworks that want to work with any model must produce JSON Schema. Type hints are Python's native schema source. The decorator is the idiomatic way to attach metadata to a function.

## What Is Universal

- **JSON Schema as the wire format.** Every framework and every LLM provider uses JSON Schema for tool parameter definitions. This is the single most stable interface in the ecosystem.
- **Natural language descriptions drive selection.** Models choose which tool to call based on the description string, not the code. Description quality directly affects tool selection accuracy.
- **Type hints provide the schema source.** In every Python framework, parameter types and return types are introspected to generate the schema automatically.
- **Docstrings supplement descriptions.** Most frameworks extract tool descriptions from docstrings when no explicit description is provided.
- **Return values serialize to strings.** Tool outputs are typically converted to strings before being passed back to the LLM.

## What Varies

- **Registration binding.** Some frameworks bind tools to individual agents (CrewAI, Claude Agent SDK); others bind to a global kernel or registry (Semantic Kernel). This affects how tools are shared across multi-agent systems.
- **Pydantic depth.** OpenAI Agents SDK and LangChain deeply integrate Pydantic for schema validation. DSPy and AutoGen use lighter approaches. This affects how complex nested parameter types are handled.
- **MCP maturity.** Claude Agent SDK treats MCP as native (tools are MCP servers). Others use adapters of varying completeness. DSPy has no native MCP support as of early 2026.

## MCP as the Convergence Layer

The Model Context Protocol (MCP), released by Anthropic in November 2024 and donated to the Linux Foundation's Agentic AI Foundation in December 2025, has become the standard cross-framework tool interop protocol. Adopted by OpenAI, Google, Microsoft, LangChain, Haystack, and others, MCP decouples tool implementation from agent reasoning.

MCP tools follow a `mcp__<server>__<tool>` naming convention. A tool packaged as an MCP server can be consumed by any framework with an MCP adapter — no framework-specific wrapper code needed.

The November 2025 spec update added async operations, statelessness options, and a community registry, addressing early criticism about statefulness requirements.

**Caveat:** MCP adoption breadth does not equal depth. Enterprise adoption remains early, implementations vary in completeness, and the protocol is still evolving. DSPy lacks native support entirely. But as of early 2026, MCP is the only protocol with adoption from all major LLM providers.

## Practical Implications

A plugin or tool library that wants maximum framework reach should:

1. Define tools as plain Python functions with complete type annotations
2. Write clear docstrings (these become the LLM-facing descriptions)
3. Accept and return JSON-serializable types
4. Optionally package as an MCP server for zero-integration consumption
5. Avoid framework-specific decorators in the core implementation — add thin adapter layers per framework if needed
