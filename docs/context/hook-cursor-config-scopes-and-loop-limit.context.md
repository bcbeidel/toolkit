---
name: "Cursor Hook Config Scopes and Loop Limit"
description: "Cursor provides four configuration scope tiers (enterprise > team > project > user) and a loop_limit to prevent stop-hook feedback loops; most platforms support two tiers at most"
type: context
sources:
  - https://cursor.com/docs/hooks
related:
  - docs/research/2026-04-13-hooks-platform-comparison.research.md
  - docs/context/hook-cursor-unique-capabilities.context.md
  - docs/context/hook-platform-event-coverage-comparison.context.md
---

Cursor's hook configuration system supports four scope tiers, more than any other platform in the survey. It also provides `loop_limit` for controlling stop-hook feedback loops — a problem that has caused CI infinite loops in other platforms.

**Four configuration scope tiers**

Priority order (highest to lowest):

1. **Enterprise** — MDM-managed (mobile device management). Deployed organization-wide and cannot be overridden by lower scopes.
2. **Team** — Cloud-distributed by the Cursor team account. Applies to all team members across all projects.
3. **Project** — `.cursor/hooks.json` in the repository root. Repository-specific hooks.
4. **User** — `~/.cursor/hooks.json`. Personal hooks applying to all projects.

By comparison: Claude Code supports project (`.claude/settings.json`) and user (`~/.claude/settings.json`). Codex supports user (`~/.codex/hooks.json`) and repository (`<repo>/.codex/hooks.json`). Windsurf supports system, user, and workspace (three tiers). No other platform documents an enterprise MDM tier.

Cursor automatically reloads `hooks.json` on file save, without requiring a restart.

**loop_limit**

For `stop` and `subagentStop` hooks, Cursor sets a default `loop_limit` of 5. This caps the number of automatic follow-up iterations triggered by a stop hook before the loop is terminated. Setting `loop_limit: null` removes the cap.

This prevents the category of problem documented in Claude Code's CI integration (GitHub issue #3573): a Stop hook script with a syntax error looping indefinitely in GitHub Actions. Cursor's `loop_limit` builds loop prevention into the configuration schema rather than requiring the script author to implement re-entry detection. Claude Code addresses the same problem via the `stop_hook_active` field in the SubagentStop payload (SubagentStop only; Stop events do not include this field).

**Session-scoped environment variables**

Environment variables set in a `sessionStart` hook propagate to all subsequent hooks in the session. This enables session-level context (e.g., project identifiers, auth tokens) to be established once at session open and consumed throughout.
