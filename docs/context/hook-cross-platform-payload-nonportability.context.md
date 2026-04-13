---
name: "Hook Cross-Platform Payload Non-Portability"
description: "Hook payload schemas are fully non-interoperable across platforms: field names, naming conventions, blocking mechanisms, and data types all differ; scripts are not portable"
type: context
sources:
  - https://code.claude.com/docs/en/hooks
  - https://cursor.com/docs/hooks
  - https://docs.windsurf.com/windsurf/cascade/hooks
  - https://docs.github.com/en/copilot/reference/hooks-configuration
  - https://developers.openai.com/codex/hooks
  - https://docs.cline.bot/customization/hooks
related:
  - docs/research/2026-04-13-hooks-platform-comparison.research.md
  - docs/context/hook-handler-type-comparison.context.md
  - docs/context/hook-copilot-toolargs-serialization.context.md
  - docs/context/hook-platform-event-coverage-comparison.context.md
---

There is no cross-platform hook portability. Payload field naming conventions, event names, blocking mechanisms, data types, and output field schemas all differ across every platform. A script written for one platform will silently fail on another.

**Naming convention divergence**

| Platform | Event name convention | Field convention | Example |
|----------|-----------------------|-----------------|---------|
| Claude Code | PascalCase | snake_case | `PreToolUse`, `tool_name` |
| Cursor | camelCase | snake_case | `preToolUse`, `tool_name` |
| Windsurf | snake_case | snake_case | `pre_read_code`, `agent_action_name` |
| Copilot cloud | camelCase | camelCase | `preToolUse`, `toolName`, `toolArgs` |
| Copilot VS Code | PascalCase | snake_case | `PreToolUse`, `hook_event_name` |
| Codex CLI | PascalCase | snake_case | `PreToolUse`, `tool_name` |
| Cline | PascalCase | camelCase | `PreToolUse`, `taskId`, `clineVersion` |

**Platform-specific fields**

Each platform adds fields that are meaningless or absent on others:

- Cursor: `conversation_id`, `generation_id`, `cursor_version`, `user_email`, `workspace_roots`, `transcript_path`
- Windsurf: `trajectory_id`, `execution_id`, `agent_action_name`
- Codex: `turn_id` (turn-scoped events only)
- Cline: `taskId`, `hookName`, `clineVersion`, `userId`, `model.provider`, `model.slug`

**Blocking mechanism divergence**

| Platform | Block signal |
|----------|-------------|
| Claude Code | Exit code 2 |
| Cursor | Exit code 2 or `permission: 'deny'` in JSON |
| Windsurf | Exit code 2 (pre-hooks only) |
| Copilot | Non-zero exit (preToolUse) |
| Codex | Exit code 2 or `{"decision": "block"}` in JSON |
| Cline | `{"cancel": true}` in JSON stdout |

**Silent failures are the risk**

A script using `permissionDecision` (Claude Code output field) will compile and run on Codex — but Codex silently ignores the field. A script using `toolArgs` as a string (Copilot format) will fail with a parse error on Claude Code, which delivers `tool_input` as a parsed object. There are no cross-platform validation tools; divergence is always silent at runtime.

The only safe approach for cross-platform use: write platform-specific scripts for each target and do not attempt to share hook script logic across platforms.
