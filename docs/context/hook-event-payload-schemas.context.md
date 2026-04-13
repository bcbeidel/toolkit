---
name: Hook Event Payload Schemas
description: "Per-event stdin JSON schemas for Claude Code hooks: common fields, event-specific fields, tool_input variants, and environment variables available at runtime"
type: reference
confidence: high
created: 2026-04-13
updated: 2026-04-13
sources:
  - https://code.claude.com/docs/en/hooks
related:
  - docs/context/hooks-deterministic-enforcement-vs-advisory.context.md
  - docs/context/hook-matcher-syntax.context.md
  - docs/context/hook-output-and-decision-control.context.md
---
Every hook receives a JSON payload on stdin. Misreading the schema is the most common cause of broken hooks — scripts that silently pass when they should block, or crash on unexpected field absence.

## Common Fields (All Events)

```json
{
  "session_id": "string",
  "transcript_path": "string",
  "cwd": "string",
  "hook_event_name": "string",
  "permission_mode": "default|plan|acceptEdits|auto|dontAsk|bypassPermissions",
  "agent_id": "string (subagent context only)",
  "agent_type": "string (subagent context only)"
}
```

## Event-Specific Fields

**PreToolUse / PostToolUse / PostToolUseFailure** add:
```json
{
  "tool_name": "Bash|Write|Edit|Read|Glob|Grep|Agent|WebFetch|mcp__server__tool|...",
  "tool_input": { ... },
  "tool_use_id": "string"
}
```
PostToolUse also adds `"tool_response": object`. PostToolUseFailure adds `"error": string` and optional `"is_interrupt": boolean`.

**tool_input structure varies by tool_name:**

| tool_name | Key fields in tool_input |
|-----------|--------------------------|
| Bash | `command`, `description`, `timeout`, `run_in_background` |
| Write | `file_path`, `content` |
| Edit | `file_path`, `old_string`, `new_string` |
| Read | `file_path`, `limit`, `offset` |
| WebFetch | `url`, `prompt` |
| Agent | `prompt`, `description` |

**Stop:** adds `"stop_reason": string`

**SubagentStop:** adds `"stop_hook_active": boolean`, `"agent_id"`, `"agent_type"`, `"agent_transcript_path"`, `"last_assistant_message"`

**UserPromptSubmit:** adds `"prompt": string`

**SessionStart:** adds `"source": startup|resume|clear|compact`, `"model": string`

**PermissionRequest:** adds `"tool_name"`, `"tool_input"`, `"permission_suggestions": array`

**PermissionDenied:** adds `"tool_name"`, `"tool_input"`, `"tool_use_id"`, `"reason": string`

## Environment Variables

Available to all hooks:
- `CLAUDE_PROJECT_DIR` — project root directory
- `CLAUDE_CODE_REMOTE` — `"true"` in remote web environments; unset in CLI

Available only to `SessionStart`, `CwdChanged`, `FileChanged`:
- `CLAUDE_ENV_FILE` — write `export VAR=value` lines here to persist env vars across subsequent Bash commands in the session

Plugin hooks also receive `CLAUDE_PLUGIN_ROOT` and `CLAUDE_PLUGIN_DATA`.

## Key Constraints

**stop_hook_active is SubagentStop only.** The Stop event payload does not include this field — Stop includes `stop_reason`. SubagentStop includes `stop_hook_active`. Both events can enter infinite loops if a blocking hook doesn't guard against repeated firing; read `stop_hook_active` from SubagentStop payloads, and implement equivalent guards for Stop hooks.

**tool_input is tool-specific.** A script that reads `tool_input.command` for Bash will fail silently for a Write hook — `command` is absent, `file_path` is the correct key. Parse defensively with `jq -r '.tool_input.file_path // empty'` rather than assuming fields are present.

**transcript_path is a JSONL file.** Readable in real time: `tail -f "$transcript_path" | jq`. Useful for debugging hooks that need session context beyond the current tool call.
