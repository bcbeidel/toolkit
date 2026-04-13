---
name: "Hook Platform Event Coverage Comparison"
description: "Event depth ranking across six AI coding platforms: Claude Code (24+) > Cursor (20+) > Windsurf (12) > Copilot/Cline (8 each) > Codex CLI (5)"
type: context
sources:
  - https://code.claude.com/docs/en/hooks
  - https://cursor.com/docs/hooks
  - https://cursor.com/changelog/1-7
  - https://docs.windsurf.com/windsurf/cascade/hooks
  - https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-hooks
  - https://code.visualstudio.com/docs/copilot/customization/hooks
  - https://developers.openai.com/codex/hooks
  - https://docs.cline.bot/customization/hooks
related:
  - docs/research/2026-04-13-hooks-platform-comparison.research.md
  - docs/context/hook-cursor-unique-capabilities.context.md
  - docs/context/hook-windsurf-model-and-constraints.context.md
  - docs/context/hook-cline-task-lifecycle-model.context.md
  - docs/context/hook-platform-stability-status-q1-2026.context.md
---

Event coverage is the most direct measure of how much of the agent lifecycle each platform exposes to automation. As of Q1 2026: Claude Code (24+) > Cursor (20+) > Windsurf (12) > GitHub Copilot cloud agent (8) = Cline (8) > Codex CLI (5).

**Claude Code — broadest surface (24+ events)**

Events span every lifecycle dimension: tool execution (PreToolUse, PostToolUse, PostToolUseFailure), session (SessionStart, SessionEnd, UserPromptSubmit), subagent coordination (SubagentStart, SubagentStop, Stop), permission (PermissionRequest, PermissionDenied, Notification), compaction (PreCompact, PostCompact), filesystem state (FileChanged, CwdChanged), worktree lifecycle (WorktreeCreate, WorktreeRemove), and agent tasks (TaskCreated, TaskCompleted, InstructionsLoaded, ConfigChange, Elicitation, ElicitationResult). No other platform covers all these dimensions simultaneously.

**Cursor — deepest per-event granularity (20+ events)**

Cursor separates tool-type-specific hooks from the generic PreToolUse/PostToolUse pair: `beforeShellExecution`, `afterShellExecution`, `beforeMCPExecution`, `afterMCPExecution`, `beforeReadFile`, `afterFileEdit`. Additionally, Cursor is the only platform with agent reasoning hooks (`afterAgentThought`, `afterAgentResponse`) and inline-completion hooks (`beforeTabFileRead`, `afterTabFileEdit`). These fire on events other platforms do not expose at all.

**Windsurf — 12 events, clean pre/post split**

Events map to six operation types: read_code, write_code, run_command, mcp_tool_use, user_prompt, and cascade_response. The model is consistent: every operation has a `pre_` and `post_` variant, with `post_cascade_response_with_transcript` added for full-session transcript access. Coverage has been actively expanding: `pre_user_prompt` blocking was added December 2025, and `post_setup_worktree` was added January 2026.

**GitHub Copilot — 8 events each, cloud agent and VS Code diverge**

The cloud agent and VS Code implementations share most events but differ in exactly one: the cloud agent has `errorOccurred` (the only platform to expose this event), while VS Code has `PreCompact` (context management). Neither provides reasoning-step or file-type-specific events. Matcher values in the VS Code format are parsed but not applied.

**Codex CLI — 5 events, narrowest of all platforms**

SessionStart, PreToolUse, PostToolUse, UserPromptSubmit, Stop. PreToolUse only intercepts the Bash tool; MCP, Write, WebSearch, and non-shell tools are not interceptable. The feature is marked "Experimental" as of Q1 2026, and Windows support is temporarily disabled.

**Cline — 8 events, unique task-lifecycle focus**

Cline's hook model centers on task lifecycle rather than tool execution: TaskStart, TaskResume, TaskCancel, TaskComplete. These four events have no equivalent in any other platform. The remaining four (PreToolUse, PostToolUse, UserPromptSubmit, PreCompact) mirror common patterns. Windows support requires PowerShell scripts; global toggle via `cline config` is not yet supported on Windows.

**What event count tells you — and what it doesn't**

A higher event count means more observability and automation surface, but does not guarantee enforcement fidelity. Event coverage rankings will shift as platforms develop rapidly. Any comparison is valid for Q1 2026 only; reassess before making architecture decisions tied to specific event availability.
