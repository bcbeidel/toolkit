---
name: "Cline Task Lifecycle Hook Model"
description: "Cline exposes TaskStart/Resume/Cancel/Complete events unique across all platforms; blocking uses cancel: true in JSON output rather than exit codes"
type: context
sources:
  - https://docs.cline.bot/customization/hooks
  - https://cline.ghost.io/cline-v3-36-hooks/
  - https://deepwiki.com/cline/cline/7.3-hooks-system
related:
  - docs/research/2026-04-13-hooks-platform-comparison.research.md
  - docs/context/hook-platform-event-coverage-comparison.context.md
  - docs/context/hook-cline-enforcement-anomalies.context.md
  - docs/context/hook-blocking-reliability-cross-platform.context.md
---

Cline's hook model is distinguished by task-lifecycle events that no other platform in the survey provides. Where every other platform focuses on tool execution (PreToolUse) and session boundaries (SessionStart/Stop), Cline exposes the full task lifecycle: start, resume, cancel, and completion.

**Unique task-lifecycle events**

Four events appear in no other platform:

- `TaskStart` — fires when a new task is initiated
- `TaskResume` — fires when an interrupted task is resumed
- `TaskCancel` — fires when the user cancels a running task
- `TaskComplete` — fires when a task finishes successfully

These enable hooks that track work across interruptions, validate task preconditions, audit completed tasks, or log cancellations. Auditing "what the agent accomplished" at task level — not just per tool call — is architecturally distinct from the other platforms' models.

**The four shared events**

The remaining four events align with common patterns: PreToolUse (before tool execution), PostToolUse (after tool completes, success or failure), UserPromptSubmit (user sends a message), PreCompact (before conversation history truncation).

**Blocking via `cancel: true`**

Cline does not rely on exit codes for blocking. The primary contract is JSON output on stdout:

```json
{
  "cancel": true,
  "errorMessage": "Reason displayed to user"
}
```

`cancel: true` stops the operation: blocks the tool, cancels a task start, or halts processing depending on which event fired it. When both global and workspace hooks are present, both run — global first, then workspace. If either returns `cancel: true`, the operation stops.

For informational additions without blocking: `contextModification` injects text into Claude's context. It is truncated above approximately 50KB.

**Storage and invocation**

Hooks are executables stored at `~/Documents/Cline/Hooks/` (global, macOS/Linux) or `.clinerules/hooks/` (project-scoped). On macOS/Linux: extensionless executable named by event (e.g., `PreToolUse`). On Windows: PowerShell `.ps1` script (e.g., `PreToolUse.ps1`). Toggle and enable via `cline config`; Windows does not yet support the toggle mechanism.

**PostToolUse semantics**

PostToolUse fires after both successful and failed tool executions. It can return `cancel: true` to stop the task but cannot undo the tool execution that already occurred. Evidence suggests (MODERATE — T5 source) that exit code 1 from PostToolUse erroneously blocks execution despite documentation stating it should not; see `hook-cline-enforcement-anomalies.context.md`.
