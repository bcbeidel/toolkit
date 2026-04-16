---
name: "Claude Code Subagent Definition Format"
description: "The complete .claude/agents/*.md file format — 16 frontmatter fields, 5-tier discovery hierarchy, plugin security restrictions, and model resolution order for Claude Code subagents"
type: context
sources:
  - https://code.claude.com/docs/en/sub-agents
related:
  - docs/research/2026-04-13-claude-code-subagent-mechanics-cross-platform.research.md
  - docs/context/claude-code-subagent-context-isolation-model.context.md
  - docs/context/claude-code-subagent-permission-and-security-model.context.md
  - docs/context/claude-code-subagent-invocation-and-routing.context.md
  - docs/context/subagent-cross-platform-format-comparison.context.md
---

# Claude Code Subagent Definition Format

A subagent file is Markdown with YAML frontmatter. The body becomes the system prompt. Only `name` and `description` are required. Sixteen fields are supported.

## Complete Field Reference

| Field | Default | Key semantic |
|---|---|---|
| `name` | required | Unique slug (lowercase, hyphen-separated) |
| `description` | required | Routing signal — when Claude should delegate to this agent |
| `tools` | inherit all | Allowlist of tools the subagent can use |
| `disallowedTools` | none | Denylist; applied before `tools`; a tool in both is removed |
| `model` | `inherit` | `sonnet`, `opus`, `haiku`, full model ID (e.g., `claude-opus-4-6`), or `inherit` |
| `permissionMode` | `default` | `default`, `acceptEdits`, `auto`, `dontAsk`, `bypassPermissions`, `plan` |
| `maxTurns` | unbounded | Stops the subagent after N agentic turns |
| `skills` | none | Skills to inject into subagent context at startup (not inherited from parent) |
| `mcpServers` | inherit | MCP servers available to this subagent |
| `hooks` | none | Lifecycle hooks scoped to this subagent |
| `memory` | none | Persistent memory scope: `user`, `project`, or `local` |
| `background` | `false` | `true` runs concurrently; `false` blocks parent |
| `effort` | inherit | `low`, `medium`, `high`, `max` (`max` is Opus 4.6 only) |
| `isolation` | none | `worktree` runs in a temporary git worktree |
| `color` | system default | Display color in the agents panel |
| `initialPrompt` | none | Auto-submitted as first user turn in `--agent` session-wide mode only |

## Discovery — 5-Tier Priority Hierarchy

Subagents are loaded at session start (not on demand). Higher priority wins on name conflict. `/agents` reloads without restart.

| Priority | Location | Scope |
|---|---|---|
| 1 (highest) | Managed settings | Organization-wide |
| 2 | `--agents` CLI flag | Current session |
| 3 | `.claude/agents/` | Current project |
| 4 | `~/.claude/agents/` | All your projects |
| 5 (lowest) | Plugin's `agents/` directory | Where plugin is enabled |

Project discovery walks upward from CWD. Directories added via `--add-dir` grant file access only — not scanned for agents.

## Plugin Security Restrictions

Plugin subagents (agents loaded from a plugin's `agents/` directory) cannot use `hooks`, `mcpServers`, or `permissionMode`. These fields are silently ignored when loading agents from a plugin. This is a documented security boundary, not a bug.

## Model Resolution Order

When a subagent is invoked, the model is resolved in this order (highest priority first):

1. `CLAUDE_CODE_SUBAGENT_MODEL` environment variable
2. Per-invocation `model` parameter from the parent's Agent tool call
3. Subagent definition's `model` frontmatter field
4. Main conversation's model

`effort: max` is only available for Opus 4.6. `initialPrompt` only fires when the agent runs as the full session via `--agent` flag or `agent` setting — it does not fire for Agent-tool-spawned subagents.

## Minimal Valid Example

```markdown
---
name: code-reviewer
description: Reviews code for quality and best practices. Use proactively when code changes are ready for review.
tools: Read, Glob, Grep
model: sonnet
---

You are a code reviewer. Analyze the provided code and return specific,
actionable feedback on quality, security, and best practices.
```

## Takeaway

The format is simple by design: 2 required fields, the rest optional with sensible defaults. The critical non-obvious behaviors are: `initialPrompt` only works in session-wide mode; plugin agents lose 3 fields silently; model resolution has 4 levels with env var at top.
