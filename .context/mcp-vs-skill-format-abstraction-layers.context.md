---
name: "MCP and SKILL.md Are Different Abstraction Layers"
description: "MCP solves tool invocation protocol via JSON-RPC; it does not address SKILL.md file format, L1/L2/L3 loading, or intent routing — treating MCP adoption as evidence of skill format portability conflates two unrelated layers"
type: context
sources:
  - https://modelcontextprotocol.io/docs/concepts/tools
  - https://blog.langchain.com/tool-calling-with-langchain/
  - https://developers.llamaindex.ai/python/framework/module_guides/deploying/agents/tools/
  - https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
related:
  - docs/research/2026-04-11-wos-skill-portability-runtime-comparison.research.md
  - docs/context/tool-api-incompatibility-cloud-providers.context.md
  - docs/context/agent-skills-governance-gap.context.md
  - docs/context/skill-loading-architecture-claude-specific.context.md
  - docs/context/mcp-vs-function-calling-tradeoffs.context.md
  - docs/context/skill-mcp-tool-subagent-taxonomy.context.md
---

# MCP and SKILL.md Are Different Abstraction Layers

MCP (Model Context Protocol) is a JSON-RPC server protocol for tool invocation. SKILL.md is a file format for defining prompt-level skills with progressive loading and intent-routing conventions. These solve different problems at different layers of the stack. High MCP adoption does not validate SKILL.md portability, and MCP cannot substitute for the SKILL.md concerns it does not address.

## What MCP Defines

MCP's tool definition format includes: `name`, `description`, `inputSchema` (JSON Schema), optional `outputSchema`, and `annotations`. It specifies how a server exposes callable tools to a client via JSON-RPC. Servers that support tools must declare the `tools` capability. Clients must treat tool annotations as untrusted unless the server is trusted.

MCP has seen substantial adoption: Anthropic donated MCP to the Linux Foundation/AAIF, with OpenAI, Google, and Microsoft joining. MCP is available as a `ToolSpec` in LlamaHub, enabling framework-level integration between MCP servers and LlamaIndex agents.

## What MCP Does Not Address

MCP is a runtime-to-server invocation protocol. It does not address:

- **File format loading:** How skill instructions are discovered on disk, parsed, and loaded into context (L1/L2/L3)
- **Progressive disclosure:** Loading only the relevant portion of skill instructions on-demand
- **Description-based intent routing:** How a user's natural language request maps to a skill at the prompt layer
- **Subagent dispatch:** How `context: fork` isolation or similar subagent patterns are orchestrated
- **Frontmatter conventions:** `name`, `description`, `related`, `sources`, and the rest of the SKILL.md frontmatter schema

A WOS skill could theoretically expose its underlying scripts as an MCP server, but this is additive — it does not make the skill's SKILL.md file format portable, nor does it provide the routing, loading, or context management behaviors WOS skills depend on.

## The Conflation Risk

MCP's adoption curve is often cited as evidence that "tool calling is standardized." This is true for the invocation protocol layer. It does not extend to the skill file format layer. Conflating these is a common reasoning error:

- MCP = how tools are called once discovered
- SKILL.md = how skills are authored, discovered, loaded, and routed to

Both layers need solutions for cross-runtime portability. MCP provides one. The skill file format layer has no equivalent independent standard.

The Agent Skills spec (`agentskills.io`) defines a minimum for the file format layer, but it remains Anthropic-controlled (see: agent-skills-governance-gap). MCP's governance maturity (Linux Foundation/AAIF) is not shared by Agent Skills.

---

**Takeaway:** MCP addresses tool invocation protocol (JSON-RPC), not skill file format, loading, or routing. MCP adoption statistics do not validate SKILL.md portability. They are separate abstraction layers requiring separate portability solutions.
