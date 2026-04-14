---
name: "Claude Code Subagent Tool Selection Strategy"
description: "How to choose which tools to grant a subagent — tool restrictions are hard constraints, omitting tools is the dangerous over-grant default"
type: context
sources:
  - https://code.claude.com/docs/en/sub-agents
  - https://www.pubnub.com/blog/best-practices-for-claude-code-sub-agents/
  - https://www.ksred.com/claude-code-agents-and-subagents-what-they-actually-unlock/
  - https://github.com/VoltAgent/awesome-claude-code-subagents
related:
  - docs/research/2026-04-14-subagent-authoring-best-practices.research.md
  - docs/context/claude-code-subagent-permission-and-security-model.context.md
  - docs/context/claude-code-subagent-definition-format.context.md
---

# Claude Code Subagent Tool Selection Strategy

Tool restrictions are hard constraints, not prompt instructions. A subagent defined with only `Read, Grep, Glob` cannot write files regardless of what the body says. Body instructions saying "do not modify files" without tool restrictions can be violated — natural language constraints are soft; the `tools` field is enforced at the runtime level.

## The Dangerous Default

Omitting the `tools` field means the subagent inherits ALL tools from the main conversation, including any MCP tools. This is the over-grant default. For any role-scoped agent — a reviewer, auditor, researcher — omitting `tools` gives capabilities that undermine the agent's purpose and create unintended risk.

Official docs: "If you keep all tools selected, the subagent inherits all tools available to the main conversation."

Default to restriction for any agent with a defined role. Omit `tools` only for fully general-purpose agents where you explicitly want the full tool set.

## allowlist vs. denylist

Two mechanisms control tool access:

- **`tools` (allowlist)** — the subagent can only use the tools in this list
- **`disallowedTools` (denylist)** — these tools are removed from whatever the subagent would otherwise have

If both are set, `disallowedTools` is applied first. A tool listed in both is removed. Anthropic's own Explore and Plan built-ins use `disallowedTools` to strip `Write`, `Edit`, and `NotebookEdit` from an otherwise full tool set. The code-reviewer example uses an explicit `tools` allowlist: `Read, Grep, Glob, Bash`.

## Three-Tier Taxonomy

Community practice (consistent with official examples) has codified three tiers:

| Tier | Tools | Use for |
|------|-------|---------|
| Read-only | `Read, Grep, Glob` | Reviewers, auditors, analysis agents |
| Research | `Read, Grep, Glob, WebFetch, WebSearch` | Documentation lookup, research agents |
| Implementation | `Read, Write, Edit, Bash, Glob, Grep` | Agents that write or modify files |

Official built-in assignments align with these tiers: Explore and Plan use read-only patterns via `disallowedTools`; the debugger example uses implementation-tier tools; the data-scientist example uses `Bash, Read, Write`.

## Conditional Gating Within a Tool

When you need operation-level control — not just tool-level — use `PreToolUse` hooks. Example: allow `Bash` for the agent but configure a hook to validate SQL and permit only SELECT queries. This is the recommended approach when a tool is needed but specific operations within it should be blocked.

## Permission Inheritance

`bypassPermissions: true` in the parent conversation propagates to all subagents and cannot be overridden by `permissionMode` in the subagent definition. If a parent runs with elevated permissions, subagents inherit those elevations. Design permission scope at the invocation level, not just at the agent definition level.

**Takeaway:** Default to restriction — start from the read-only tier and add tools only as the agent's task requires. Tool restrictions enforce constraints that body instructions cannot. Use `PreToolUse` hooks for operation-level gating within a single tool.
