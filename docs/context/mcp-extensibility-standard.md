---
name: "MCP as the Universal Extensibility Protocol"
description: "How the Model Context Protocol became the industry standard for connecting AI coding tools to external systems — adoption, specification maturity, and remaining gaps"
metadata:
  type: reference
  sources:
    - https://modelcontextprotocol.io/specification/2025-11-25
    - https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation
    - https://code.claude.com/docs/en/overview
    - https://docs.cursor.com/context/rules
    - https://developers.openai.com/codex/skills/
  related:
    - docs/research/ai-coding-assistant-conventions.md
    - docs/context/plugin-extension-architecture.md
    - docs/context/tool-design-for-llms.md
    - docs/context/skill-command-system-landscape.md
---

MCP (Model Context Protocol) has become the universal standard for extending AI coding tools with external capabilities. Created by Anthropic and donated to the Linux Foundation's Agentic AI Foundation in December 2025, MCP crossed 97 million monthly SDK downloads by February 2026.

## Adoption Across Tools

Every major AI coding tool except Aider supports MCP natively:

| Tool | Config Location | Notes |
|------|----------------|-------|
| Claude Code | `.mcp.json` | First-class support; Anthropic created MCP |
| GitHub Copilot | `.vscode/mcp.json`, `.github/copilot/` | Agent mode + coding agent |
| Cursor | `.cursor/mcp.json` | One-click setup, OAuth support |
| Windsurf | Settings UI or config file | Integrated with Cascade |
| Codex CLI | `agents/openai.yaml` dependencies | Skills can declare MCP dependencies |
| Cline | `cline_mcp_settings.json` | Can create MCP servers on the fly |
| Aider | N/A | No native support; model-agnostic approach |

Aider's absence is deliberate — its model-agnostic design philosophy avoids tool-specific protocols. For all other tools, MCP is the primary mechanism for connecting to external services, databases, APIs, and development tools.

## Protocol Maturity

The November 2025 specification update added three significant capabilities:

1. **Server identity verification.** Cryptographic verification of MCP server identity, addressing supply-chain security concerns.
2. **Async operations.** Support for long-running tool calls that don't block the conversation.
3. **Statelessness by default.** Servers no longer need to maintain session state, simplifying deployment and scaling.

These additions moved MCP from an early-stage protocol to a production-ready standard. The Linux Foundation governance ensures that evolution happens through an open process with multi-vendor input.

## What MCP Provides

MCP standardizes three interaction primitives:

- **Tools.** Functions that the AI can invoke (e.g., query a database, create a ticket, run a test).
- **Resources.** Data sources the AI can read (e.g., documentation, configuration, logs).
- **Prompts.** Pre-built instruction templates that servers can offer to clients.

This maps cleanly to how AI coding tools already work: tools extend the action space, resources extend the knowledge space, and prompts provide structured starting points for common tasks.

## Remaining Gaps

MCP universality has limits:

- **Implementation variance.** Tools implement different subsets of the specification. A server that works perfectly with Claude Code may behave differently in Cursor or Copilot.
- **Security concerns persist.** Despite the November 2025 improvements, running arbitrary MCP servers introduces supply-chain risk. Server identity verification helps, but the ecosystem lacks a trust registry.
- **Orchestration limitations.** MCP's tool-call model handles individual operations well but lacks primitives for multi-step workflows, transactions, or coordinated tool use. Complex workflows still need application-level orchestration.
- **No native Aider support.** Teams using Aider alongside MCP-supporting tools cannot share extensibility configurations.

## Relevance to WOS

WOS operates as a Claude Code plugin, which means its scripts and skills run within Claude Code's MCP-aware environment. While WOS itself uses the simpler skill/script model rather than MCP servers, it coexists with MCP-provided tools. As the ecosystem matures, WOS may benefit from MCP for cross-tool compatibility — a WOS MCP server could provide context navigation to any supporting tool, not just Claude Code.
