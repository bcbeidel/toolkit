---
name: "Windsurf Hook Model and Constraints"
description: "Windsurf Cascade provides 12 hooks on a simple pre/post split across six operation types; no confirmed blocking failures; no input transformation; actively expanding as of Q1 2026"
type: context
sources:
  - https://docs.windsurf.com/windsurf/cascade/hooks
  - https://www.digitalapplied.com/blog/windsurf-swe-1-5-cascade-hooks-november-2025
related:
  - docs/research/2026-04-13-hooks-platform-comparison.research.md
  - docs/context/hook-platform-event-coverage-comparison.context.md
  - docs/context/hook-blocking-reliability-cross-platform.context.md
  - docs/context/hook-windsurf-transcript-security-constraints.context.md
  - docs/context/hook-path-expansion-platform-quirks.context.md
---

Windsurf Cascade's hook model is the simplest of the six platforms surveyed. Twelve events map to a strict pre/post split across six operation types, the blocking semantics are unambiguous, and no confirmed enforcement failures have been reported — a meaningful distinction given that Claude Code, Cursor, and GitHub Copilot VS Code all have documented blocking gaps as of Q1 2026.

**The pre/post model**

Six operation types, each with a `pre_` and `post_` variant:

| Operation | Pre | Post |
|-----------|-----|------|
| Read code | `pre_read_code` | `post_read_code` |
| Write code | `pre_write_code` | `post_write_code` |
| Run command | `pre_run_command` | `post_run_command` |
| MCP tool | `pre_mcp_tool_use` | `post_mcp_tool_use` |
| User prompt | `pre_user_prompt` | `post_cascade_response` |
| Worktree | _(none)_ | `post_setup_worktree` |

Additionally, `post_cascade_response_with_transcript` provides a full-session conversation transcript at response completion.

**Blocking semantics**

Only pre-hooks can block; post-hooks cannot (the action has already occurred). Exit code 0 = proceed; exit code 2 = block (user sees stderr message); any other exit code = error (action proceeds). There is no `ask`, `defer`, or `updatedInput` equivalent — Windsurf pre-hooks are block/allow only, with no input transformation capability. This simplicity is both the strength (clear semantics) and the limitation (less expressive than Claude Code or Cursor).

**Confirmed expansion**

- `pre_user_prompt` blocking added version 1.13.5, December 27, 2025
- `post_setup_worktree` hook added January 16, 2026

Windsurf is actively adding coverage. The current surface is the floor, not the ceiling.

**Architectural constraints**

- No `updatedInput` — hooks cannot mutate tool input before execution
- `show_output` does not apply to `pre_user_prompt` or `post_cascade_response` hooks
- `~` is not expanded in `working_directory`; absolute paths required (silent failure otherwise)
- Configuration files merge across three tiers (system → user → workspace); see platform-specific config paths for macOS, Linux/WSL, Windows, and JetBrains
- Transcript files from `post_cascade_response_with_transcript` are capped at 100 and have security implications (see `hook-windsurf-transcript-security-constraints.context.md`)

**Reliability posture**

No independent reports of Windsurf pre-hook exit code 2 failing to block were found in the research. The simpler model may be the reason: fewer edge cases, fewer tool-type-specific code paths to get wrong. However, the absence of disconfirming reports is not a guarantee — Windsurf is also pre-stable (no official stability designation as of Q1 2026).
