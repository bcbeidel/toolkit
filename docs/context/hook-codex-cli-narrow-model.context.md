---
name: "Codex CLI Hook Narrow Model"
description: "Codex CLI provides only 5 hook events, and PreToolUse only intercepts the Bash tool; output fields from other platforms are silently ignored"
type: context
sources:
  - https://developers.openai.com/codex/hooks
related:
  - docs/research/2026-04-13-hooks-platform-comparison.research.md
  - docs/context/hook-platform-event-coverage-comparison.context.md
  - docs/context/hook-cross-platform-payload-nonportability.context.md
  - docs/context/hook-blocking-reliability-cross-platform.context.md
---

Codex CLI has the narrowest hook implementation of any platform surveyed. Five events, Bash-only interception, and silent discard of output fields from other platforms make Codex the most constrained scripting target as of Q1 2026.

**Event surface**

SessionStart, PreToolUse, PostToolUse, UserPromptSubmit, Stop. No subagent events, no compaction events, no file-change events, no permission events.

**Bash-only PreToolUse**

The critical constraint: Codex's PreToolUse only intercepts the Bash tool. MCP tools, Write, WebSearch, and non-shell tools are not interceptable. A hook designed to gate all file writes will not fire on file-write operations in Codex — only shell-executed writes would trigger it. This is documented explicitly: "Currently PreToolUse only supports Bash tool interception."

**Silent discard of cross-platform fields**

Scripts that emit Claude Code output fields will silently fail to influence Codex behavior:

- `permissionDecision` — recognized by Claude Code, ignored by Codex
- `updatedInput` — recognized by Claude Code and Cursor, ignored by Codex
- `additionalContext` — recognized by Claude Code, ignored by Codex

Codex's own blocking shape for PreToolUse is `{"decision": "block", "reason": "..."}` (JSON) or exit code 2 with reason in stderr. These are not the same as Claude Code's exit code 2 plus JSON output contract.

**PostToolUse semantics**

PostToolUse cannot undo an already-executed Bash command. Codex records feedback from the hook, replaces the tool result with that feedback, and continues. This is a continuation mechanism, not a rollback.

**Stop behavior**

`decision: 'block'` in Stop hook output tells Codex to continue the agent loop automatically. If any matching hook returns `continue: false`, that takes precedence. `suppressOutput` is parsed but not implemented for most events.

**Status and availability**

Feature status: Experimental. Windows support temporarily disabled. Hook configuration at `~/.codex/hooks.json` (user-level) and `<repo>/.codex/hooks.json` (repository-level); both coexist and all matching hooks run. Default timeout: 600 seconds (matches Claude Code command handler default).
