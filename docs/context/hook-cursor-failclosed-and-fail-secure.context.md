---
name: "Cursor failClosed and Fail-Secure Behavior"
description: "Cursor's failClosed: true reverses default fail-open behavior for hook crashes; no other platform documents an equivalent mechanism"
type: context
sources:
  - https://cursor.com/docs/hooks
related:
  - docs/research/2026-04-13-hooks-platform-comparison.research.md
  - docs/context/hook-cursor-unique-capabilities.context.md
  - docs/context/hook-blocking-reliability-cross-platform.context.md
---

When a hook crashes, times out, or returns invalid JSON, the default behavior across all surveyed platforms is fail-open: the triggering action proceeds as if the hook had not run. Cursor is the only platform that documents a mechanism to reverse this.

**The `failClosed` property**

Setting `failClosed: true` on a hook definition causes hook failures (crash, timeout, invalid JSON output) to block the action rather than allow it through. This is fail-secure behavior: if the safety check cannot complete, the action does not proceed.

Default (omitting `failClosed` or setting `failClosed: false`): hook crashes → action proceeds.
With `failClosed: true`: hook crashes → action is blocked.

The official Cursor documentation recommends `failClosed: true` specifically for security-critical hooks: `beforeMCPExecution` and `beforeReadFile` are cited as the primary use cases.

**Why this matters**

A hook that crashes silently allows every action it was meant to gate. If a security hook depends on an external binary that is missing in a CI environment, or times out when the network is slow, the default fail-open behavior means the gate is gone without any visible signal. `failClosed: true` converts this silent bypass into a hard block.

No other platform in the survey — Claude Code, Windsurf, Copilot, Codex, or Cline — documents an equivalent option.

**Practical caveat**

`failClosed: true` is only meaningful if enforcement actually works. As of Q1 2026, Cursor's `preToolUse` `deny` is confirmed non-enforcing for file reads. `failClosed` governs crash behavior, not enforcement correctness — a hook that does not crash but whose deny decision is ignored provides no additional protection. Verify enforcement per tool type independently before relying on `failClosed: true` for security guarantees.
