---
name: "LangChain and LlamaIndex Do Not Abstract Skill File Concerns"
description: "LangChain and LlamaIndex normalize tool API calls across cloud providers but do not address SKILL.md-level concerns: file loading, progressive disclosure, description routing, or subagent dispatch"
type: context
sources:
  - https://blog.langchain.com/tool-calling-with-langchain/
  - https://developers.llamaindex.ai/python/framework/module_guides/deploying/agents/tools/
  - https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
related:
  - docs/research/2026-04-11-wos-skill-portability-runtime-comparison.research.md
  - docs/context/langchain-tool-abstraction-gaps.context.md
  - docs/context/skill-loading-architecture-claude-specific.context.md
  - docs/context/mcp-vs-skill-format-abstraction-layers.context.md
  - docs/context/skill-format-portability-floor-vs-wos-extensions.context.md
---

# LangChain and LlamaIndex Do Not Abstract Skill File Concerns

LangChain and LlamaIndex operate at the function-calling API layer — they normalize how tool schemas are transmitted to providers and how responses are parsed. They do not address the skill file layer: how instructions are loaded progressively, how description text routes user intent to a skill, or how subagent isolation is managed. These are WOS-level concerns that neither framework abstracts.

## What the Frameworks Do

**LangChain:** `bind_tools()` normalizes tool definitions across OpenAI, Anthropic, and Gemini. `AIMessage.tool_calls` provides consistent response parsing. Provider substitution requires changing one class. The framework handles wire format translation internally.

**LlamaIndex:** `FunctionTool` wraps Python functions with auto-inferred or custom schemas. `ToolSpec` bundles related tools. The same cross-provider abstraction pattern applies. LlamaIndex additionally supports MCP tools via LlamaHub, creating an MCP-to-tool-framework bridge.

Both frameworks reduce tool portability to a data format translation problem, handled once in the framework rather than in every application.

## What Neither Framework Addresses

The WOS skill model involves concerns at a layer above tool API calls:

- **Progressive loading:** L1 metadata injected at startup, L2 instructions loaded on-demand via Bash reads, L3 resources fetched only when referenced. Neither LangChain nor LlamaIndex has a mechanism for this — they assume tool definitions are pre-compiled and passed at session initialization.

- **Description-based intent routing:** How a user's natural language triggers a specific skill from a catalog. The frameworks assume the application selects which tool to call; they do not provide a routing layer that maps freeform user input to a skill based on description semantics.

- **Subagent dispatch and fork isolation:** `context: fork` in WOS creates an isolated subagent context for a skill invocation. Neither framework abstracts this pattern — subagent orchestration remains application-level.

- **Frontmatter conventions:** `name`, `description`, `related`, `sources`, `allowed-tools`, and the rest of the SKILL.md schema are WOS conventions. Neither framework parses or respects them.

## What Porting a WOS Skill via LangChain Looks Like

A WOS skill ported through LangChain would reduce to:
- A Python function (the skill's executable logic)
- A `name` and `description` passed to `FunctionTool`
- Optional parameter schema

Everything else — reference files, progressive loading, dynamic injection, context fork isolation, the SKILL.md frontmatter — has no representation in the framework's model. The ported skill is a single flat function definition. It retains the skill's name and description but loses the structural architecture WOS skills are designed around.

This is not a framework failure; it is a scope mismatch. LangChain and LlamaIndex solve tool API portability. WOS skills solve prompt-layer instruction management with progressive loading and catalog-driven routing. These are different problems at different layers.

---

**Takeaway:** LangChain and LlamaIndex abstract tool API calls across cloud providers but do not address skill file loading, progressive disclosure, description routing, or subagent dispatch. Porting a WOS skill through these frameworks loses its structural architecture. The framework portability layer and the skill file portability layer are separate problems requiring separate solutions.
