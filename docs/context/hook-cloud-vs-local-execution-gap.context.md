---
name: "Hook Cloud vs Local Execution Gap"
description: "Cursor cloud agent hooks silently do not fire as of December 2025 (confirmed bug, no ETA); hooks designed for local enforcement are absent in cloud/CI contexts without warning"
type: context
sources:
  - https://forum.cursor.com/t/project-level-hooks-and-root-level-hooks-no-longer-work-in-cloud-agents/144932
  - https://cursor.com/docs/hooks
related:
  - docs/research/2026-04-13-hooks-platform-comparison.research.md
  - docs/context/hook-cursor-unique-capabilities.context.md
  - docs/context/hook-cursor-config-scopes-and-loop-limit.context.md
  - docs/context/hook-blocking-reliability-cross-platform.context.md
---

Hooks configured for local Cursor execution silently do not fire when the same project runs in Cursor's Cloud Agent mode. This is a confirmed bug with no ETA for a fix as of December 2025.

**The bug**

When running a Cloud Agent task in Cursor — a hosted, cloud-executed agent run rather than a local IDE session — project-level and root-level hooks are never executed. The hooks are present in `.cursor/hooks.json`, they work correctly in local Cursor sessions, and no error is surfaced. The agent runs, tools execute, and hook scripts are simply never invoked.

The Cursor team confirmed this bug on December 13, 2025, in the Cursor Forum thread: "The bug is confirmed and the team is investigating it. Unfortunately, there's no ETA yet."

**Why this matters**

Any security or quality enforcement deployed via Cursor hooks is silently absent for Cloud Agent runs. If hooks gate dangerous commands, prevent file writes to protected paths, or log tool usage for audit — none of that executes in cloud context. The absence is invisible: there are no error messages, no hook failure events, no indication that the enforcement layer is missing.

**Broader pattern: local vs cloud execution gaps**

Cursor is the clearest example, but the pattern appears elsewhere:

- GitHub Copilot has no global hook configuration at all — hooks must be configured per-repository via `.github/hooks/*.json`. There is no way to apply consistent personal or organization-wide policies across all projects, and no hooks fire without a repository-level config.
- Claude Code Stop hooks have caused CI infinite loops (GitHub issue #3573) when user-level hooks were applied in GitHub Actions contexts where they were not appropriate — a scoping mismatch, not a silent no-op, but another form of local-vs-CI behavioral divergence.

**Practical guidance**

Before deploying hooks as part of a security or quality enforcement strategy, verify that hook execution is confirmed in all execution contexts you rely on: local IDE, cloud agent, CI pipeline. For Cursor specifically, do not assume local hook behavior transfers to Cloud Agent runs until the bug is resolved and confirmed fixed.
