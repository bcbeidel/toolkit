---
name: "Claude Code Subagent Permission and Security Model"
description: "Two distinct inheritance paths for tool permissions in Claude Code subagents — tool registry vs runtime allowlist, bypassPermissions propagation, plugin restrictions, and the nesting enforcement boundary"
type: context
sources:
  - https://code.claude.com/docs/en/sub-agents
  - https://github.com/anthropics/claude-code/issues/14714
  - https://github.com/anthropics/claude-code/issues/22665
  - https://github.com/anthropics/claude-code/issues/20264
  - https://github.com/anthropics/claude-code/issues/25000
related:
  - docs/research/2026-04-13-claude-code-subagent-mechanics-cross-platform.research.md
  - docs/context/claude-code-subagent-definition-format.context.md
  - docs/context/claude-code-subagent-context-isolation-model.context.md
  - docs/context/claude-code-subagent-invocation-and-routing.context.md
  - docs/context/subagent-cross-platform-format-comparison.context.md
---

# Claude Code Subagent Permission and Security Model

Two separate concepts govern tool access in subagents, and they inherit differently. Conflating them is the source of most permission confusion.

## Tool Registry vs Runtime Permission Allowlist

**Tool registry** (which tools are available): Subagents inherit all tools from the global tool registry by default. Restrict with `tools` (allowlist) or `disallowedTools` (denylist). If both are set, `disallowedTools` is applied first; a tool listed in both is removed.

**Session-runtime permission allowlist** (which tool calls the user has pre-approved): NOT inherited by subagents. This is intentional design, not a bug. Four GitHub issues (#14714, #22665, #20264, #25000) reported this as a bug — all are now closed. Root issue #5465 was closed NOT_PLANNED, confirming the design choice: pre-approved tool calls in the parent session require re-prompting in subagents.

MCP tool inheritance fix shipped in v2.1.101: subagents now properly inherit MCP tools from dynamically-injected servers (a separate gap from the allowlist issue).

## `bypassPermissions` Propagates and Cannot Be Overridden

If the parent uses `bypassPermissions` mode, this takes precedence over the subagent's `permissionMode` frontmatter — the subagent cannot restrict its own permissions below the parent's level. Same for `auto` mode: if the parent uses auto mode, the subagent inherits auto mode and its `permissionMode` frontmatter is ignored.

The subagent's `permissionMode` field can only restrict permissions relative to a `default`-mode parent. It cannot sandbox itself below what the parent has already granted.

## Tool Configuration

```yaml
# Allowlist — only these tools available
tools: Read, Grep, Glob, Bash

# Denylist — all tools except these
disallowedTools: Write, Edit

# Both — denylist applied first, then allowlist resolved against remainder
```

## Plugin Security Restrictions

Agents loaded from a plugin's `agents/` directory cannot use `hooks`, `mcpServers`, or `permissionMode`. These fields are silently ignored. This is a documented security boundary: plugins cannot configure lifecycle hooks, inject MCP servers, or escalate permissions.

## Agent Spawning Restriction

The `Agent(agent_type)` syntax in the `tools` field of a main-session agent restricts which subagent types it can spawn (allowlist). Example:

```yaml
tools: Read, Glob, Agent(code-reviewer), Agent(security-scanner)
```

This syntax has no effect inside subagent definitions. Subagents cannot spawn other subagents — enforced at the tool level by filtering the Agent tool out of subagent tool sets.

Workaround: a subagent can call `claude -p` via the Bash tool to spawn a headless Claude subprocess. This bypasses the restriction but loses orchestration visibility and complicates error handling — it runs outside Claude Code's coordination layer.

## Takeaway

Design with these constraints explicitly in mind:
- Pre-approve tools at the subagent level, not just the parent level — runtime allowlists do not carry over.
- `bypassPermissions` in the parent propagates unconditionally — subagents cannot sandbox themselves below the parent's permission level.
- Nesting is blocked by design; plan orchestration accordingly.
