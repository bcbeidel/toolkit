---
name: "Cline Hook Enforcement Anomalies"
description: "Cline's PostToolUse exit code 1 erroneously blocks execution despite non-blocking documentation; hooks fire even when tool permissions are disabled"
type: context
sources:
  - https://docs.cline.bot/customization/hooks
  - https://deepwiki.com/cline/cline/7.3-hooks-system
related:
  - docs/research/2026-04-13-hooks-platform-comparison.research.md
  - docs/context/hook-cline-task-lifecycle-model.context.md
  - docs/context/hook-blocking-reliability-cross-platform.context.md
---

Cline has two documented enforcement anomalies: PostToolUse exit code 1 erroneously blocks execution despite documentation saying it should not, and hooks fire for tool types that have been permission-disabled.

**PostToolUse exit code 1 blocks unexpectedly**

Cline's official documentation describes PostToolUse as non-blocking: execution continues after PostToolUse fires, regardless of hook output. Community reports (MODERATE confidence — T5 source, auto-generated DeepWiki) contradict this: exit code 1 from PostToolUse actually halts the agent loop in practice.

If you are using PostToolUse for logging, metrics, or notification (all use cases where non-blocking behavior is expected and required), test exit code behavior explicitly. A PostToolUse hook that exits 1 on logging failures would unexpectedly stop the agent rather than silently failing the log write.

The primary blocking contract for Cline is `cancel: true` in JSON stdout. Exit code behavior outside of this is not explicitly documented, which creates ambiguity.

**Hooks fire when per-tool permissions are disabled**

When a developer disables Read or Edit tool permissions in Cline's configuration, the agent cannot use those tools. However, PostToolUse hooks for those tool types — e.g., `PostToolUse (write_to_file)` — still execute without user confirmation (GitHub issue #7334, referenced in the DeepWiki source). Note: this specific issue number requires independent verification before use in architecture decisions.

This creates two problems:

1. **Unexpected hook execution:** Hooks run for tools the user has explicitly restricted. Developers may not expect hook side effects (e.g., logging a write operation, triggering a notification) when they believe writes are disabled.

2. **Policy enforcement bypass path:** A hook that was intended to gate or monitor a disabled tool type still fires. Depending on the hook's behavior, this could mean audit logs show tool activity that the user believed was prevented, or enforcement hooks attempt to gate actions that should not be occurring at all.

**Deprecated fields**

Hooks that emit deprecated fields (such as `shouldContinue`, superseded by `cancel`) are validated against and rejected. Deprecated fields cause silent failures — the hook runs, output is parsed, and the deprecated field is discarded without warning. Audit hook output schemas when upgrading Cline versions.
