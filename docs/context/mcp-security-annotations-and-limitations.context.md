---
name: "MCP Security: Annotations and Protocol Limitations"
description: "MCP tool annotations are hints not guarantees — tool poisoning and prompt injection are unmitigated at the protocol level; enterprise deployments require network controls and sandboxing"
type: context
sources:
  - https://modelcontextprotocol.io/specification/2025-11-25/server/tools
  - https://blog.modelcontextprotocol.io/posts/2026-03-16-tool-annotations/
  - https://simonwillison.net/2025/Apr/9/mcp-prompt-injection/
  - https://prompt.security/blog/top-10-mcp-security-risks
  - https://research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files-cve-2025-59536/
related:
  - docs/context/mcp-vs-function-calling-tradeoffs.context.md
  - docs/context/hooks-deterministic-enforcement-vs-advisory.context.md
  - docs/context/llm-failure-modes-and-mitigations.context.md
  - docs/context/production-reliability-gap-and-multi-agent-failures.context.md
---

MCP tool annotations communicate behavioral intent to clients, but they provide no security guarantee. A tool with `readOnlyHint: true` from an untrusted server can still perform writes. The protocol cannot enforce consent at the wire level — it relies on implementers to follow "SHOULD" requirements for user oversight.

**The four annotation hints (added March 2025):**

| Hint | Default | Intended meaning |
|---|---|---|
| `readOnlyHint` | false | Tool does not modify its environment |
| `destructiveHint` | true | Modifications are irreversible or destructive |
| `idempotentHint` | false | Repeated calls with same args are safe |
| `openWorldHint` | true | Tool interacts with external entities |

Conservative defaults: a tool with no annotations is assumed non-read-only, potentially destructive, non-idempotent, and open-world. Clients can use these hints for UX: `readOnlyHint: true` from a trusted server is a candidate for auto-approval; `destructiveHint: true` triggers a confirmation dialog. The key qualifier is "trusted server."

**Annotations are not trusted from untrusted servers.** A malicious server can set `readOnlyHint: true` on a tool that exfiltrates data. Annotations describe intent in cooperative scenarios — they do not constrain capability in adversarial ones.

**Named attack classes that remain unmitigated at the protocol level:**

- **Tool poisoning** — malicious instructions embedded in tool `description` fields, visible to the LLM but not displayed to users in most clients; can direct the model to exfiltrate data or take unintended actions
- **Indirect prompt injection** — malicious instructions in data accessed through MCP servers (file contents, email bodies, web pages returned by tools)
- **Rug pull attacks** — tools that appear legitimate initially become malicious after gaining user trust; `notifications/tools/list_changed` enables tool definitions to mutate post-installation
- **Tool shadowing** — malicious servers override or mimic tools from trusted servers when multiple MCP servers are connected
- **CVE-2025-6514** (CVSS 9.6, July 2025) — OS command injection in `mcp-remote` versions 0.0.5–0.1.16 via malicious `authorization_endpoint` values; fixed in 0.1.16; enabled RCE on client machines

**CVE-2025-59536** (Claude Code hooks, Check Point Research, 2026): While not MCP-specific, the same threat model applies — repository files that execute code (`hooks.json`, MCP server configs) are attack surface reachable via supply chain or malicious collaborator. Hook configs and MCP server definitions should receive the same code review scrutiny as source files.

**What the protocol cannot fix.** Simon Willison's framing: "Mixing tools with untrusted instructions is inherently dangerous." The problem is architectural — the LLM processes tool descriptions and returned data in the same context as user instructions. There is no sandboxed channel for untrusted content.

**Enterprise mitigations required beyond the protocol:**
- Network controls: restrict which external services MCP servers can reach
- Sandboxing: run MCP servers in isolated environments with limited filesystem and network access
- Display tool descriptions to users initially and alert when they change (Willison's prescriptions)
- Treat the `notifications/tools/list_changed` event as a trust boundary: re-present tool definitions to users before accepting mutated ones
- Audit trails: log all `tools/call` invocations with inputs and outputs; no standard exists yet (on the 2026 roadmap)
