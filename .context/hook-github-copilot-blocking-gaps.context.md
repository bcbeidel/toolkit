---
name: "GitHub Copilot Hook Blocking Gaps"
description: "Copilot cloud agent short-circuits on the first deny; ask is unprocessed; VS Code matcher values are parsed but not applied — blocking is incomplete on both surfaces"
type: context
sources:
  - https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-hooks
  - https://docs.github.com/en/copilot/reference/hooks-configuration
  - https://code.visualstudio.com/docs/copilot/customization/hooks
related:
  - docs/research/2026-04-13-hooks-platform-comparison.research.md
  - docs/context/hook-github-copilot-surface-divergence.context.md
  - docs/context/hook-blocking-reliability-cross-platform.context.md
  - docs/context/hook-github-copilot-no-global-config.context.md
---

GitHub Copilot's blocking model has documented gaps on both the cloud agent and VS Code surfaces. Understanding these gaps is required before relying on Copilot hooks for enforcement.

**Cloud agent: first-deny short-circuits the chain**

If the first `preToolUse` hook returns `permissionDecision: deny`, subsequent hooks in the chain are skipped. The tool call is blocked, but later hooks — which might have logged the attempt, sent an alert, or applied additional checks — do not execute. This differs from Claude Code and Cursor, which run all matching hooks regardless of intermediate decisions.

The `ask` decision value is specified in the cloud agent schema but explicitly "not currently processed." A hook returning `ask` is functionally equivalent to returning nothing — the action proceeds.

**VS Code: matchers parsed but not applied**

VS Code hook definitions accept matcher values in Claude Code format (e.g., `Edit|Write` to filter by tool type). The VS Code documentation explicitly states: "Matcher values are parsed but not applied." This means every VS Code hook fires on every matching event regardless of any matcher restrictions you configure. A hook intended to run only on file writes will also run on file reads, shell commands, and all other tool events.

**VS Code enforcement status**

Evidence suggests (MODERATE — reporting from February–March 2026, SDK version claim requires independent verification) that deny decisions from VS Code hooks are ignored by the runtime. The hooks fire correctly and receive the right payloads, but the block decision does not prevent the agent from proceeding. If confirmed, this means VS Code Copilot hooks are effectively monitoring-only, not enforcement-capable, as of Q1 2026. Note: the specific SDK version claim requires independent verification before use in architecture decisions.

**What does reliably work**

Cloud agent `preToolUse` deny (non-zero exit code) is documented as functional for blocking individual tool calls. The `errorOccurred` event fires on agent errors. Session lifecycle events (start/end) fire reliably for logging purposes. Enforcement for other decision types and in VS Code context should be treated as unverified.
