---
name: "Cursor Hook Unique Capabilities"
description: "Cursor exposes reasoning-step hooks and rich subagentStop telemetry unavailable on any other platform, plus failClosed fail-secure behavior and four configuration scope tiers"
type: context
sources:
  - https://cursor.com/docs/hooks
  - https://cursor.com/changelog/1-7
  - https://blog.gitbutler.com/cursor-hooks-deep-dive
  - https://infoq.com/news/2025/10/cursor-hooks/
related:
  - docs/research/2026-04-13-hooks-platform-comparison.research.md
  - docs/context/hook-platform-event-coverage-comparison.context.md
  - docs/context/hook-cursor-config-scopes-and-loop-limit.context.md
  - docs/context/hook-cursor-failclosed-and-fail-secure.context.md
  - docs/context/hook-cloud-vs-local-execution-gap.context.md
---

Cursor's hook system (launched v1.7, September 29, 2025) adds two capabilities that no other platform provides: visibility into the agent's internal reasoning steps, and rich structured telemetry at subagent completion. These, combined with `failClosed` fail-secure configuration, distinguish Cursor's hook surface from Claude Code's breadth-first model.

**Reasoning-step hooks**

Two hooks expose the agent's intermediate reasoning:

- `afterAgentThought` — fires after each thinking block the agent completes
- `afterAgentResponse` — fires after the agent produces a complete assistant message

These are distinct from tool execution hooks. They allow hooks to observe what the agent was "thinking" and respond to reasoning patterns, not just to tool calls. No other platform in the survey (Claude Code, Windsurf, Copilot, Codex, Cline) exposes this level of agent-internal observability.

A third reasoning-adjacent hook, `beforeSubmitPrompt`, fires immediately after the user hits send but before the backend request. The GitButler deep-dive notes it is currently "informational only — you cannot communicate to the user, agent or stop the agent with json output," meaning its blocking potential is constrained in practice despite schema suggestions otherwise.

**Rich subagentStop telemetry**

The `subagentStop` payload includes fields not present on any other platform:

- `status` — `completed`, `error`, or `aborted`
- `task` and `summary` — description and outcome
- `duration_ms` — wall-clock time for the subagent run
- `message_count` and `tool_call_count` — interaction counts
- `loop_count` — how many loops the subagent executed
- `modified_files` — list of files changed during the run
- `agent_transcript_path` — path to the subagent's conversation transcript

This makes `subagentStop` the richest event payload in the cross-platform survey. Claude Code's SubagentStop includes `stop_hook_active` for loop prevention but provides no analogous telemetry fields.

**Inline completion hooks**

Cursor also exposes hooks for Tab (inline completion) behavior: `beforeTabFileRead` and `afterTabFileEdit`. These fire on completions, not agent tool calls — a separate execution surface that other platforms do not instrument.

**Caveats**

Evidence for most of these capabilities is HIGH (T1 official docs). However, several enforcement behaviors are confirmed broken or unimplemented: `ask` is schema-accepted but not enforced for `preToolUse`; `beforeSubmitPrompt` and `afterFileEdit` are described as informational-only in practice. Additionally, Cursor cloud agent hooks silently do not fire as of December 2025 (confirmed bug, no ETA) — meaning reasoning-step hooks and telemetry are local-only.
