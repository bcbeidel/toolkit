---
name: Hook Output and Decision Control
description: "How Claude Code hooks influence Claude via JSON stdout: universal output fields, per-event hookSpecificOutput schemas, handler types (command/http/prompt/agent), and exit code semantics per event"
type: reference
confidence: high
created: 2026-04-13
updated: 2026-04-13
sources:
  - https://code.claude.com/docs/en/hooks
related:
  - docs/context/hooks-deterministic-enforcement-vs-advisory.context.md
  - docs/context/hook-event-payload-schemas.context.md
  - docs/context/hook-matcher-syntax.context.md
---
Hooks influence Claude through two mechanisms: exit code (binary block/pass) and JSON stdout (rich decision control). JSON output is only parsed on exit code 0 — exit code 2 ignores stdout entirely.

## Exit Code Semantics

| Exit Code | Meaning | Blocking behavior |
|-----------|---------|-------------------|
| 0 | Success | Parses stdout for JSON; stdout added to context for UserPromptSubmit and SessionStart |
| 2 | Blocking error | Ignores stdout; feeds stderr to Claude (or user); blocks per-event (see table) |
| Other | Non-blocking error | Shows first line of stderr to user; full stderr in debug log |

**Which events can block via exit code 2:**

| Blocks | Does not block |
|--------|---------------|
| PreToolUse, PermissionRequest, UserPromptSubmit, Stop, SubagentStop, TaskCreated, TaskCompleted, ConfigChange, Elicitation, ElicitationResult | PostToolUse, PostToolUseFailure, PermissionDenied, Notification, SubagentStart, SessionStart, SessionEnd, FileChanged, PreCompact, PostCompact, WorktreeRemove, InstructionsLoaded |

**WorktreeCreate:** Any non-zero exit code fails creation (not just 2).

## Universal JSON Output Fields (Exit Code 0)

```json
{
  "continue": false,           // false stops Claude entirely (shows stopReason to user)
  "stopReason": "string",      // shown to user when continue=false
  "suppressOutput": true,      // omits stdout from debug log
  "systemMessage": "string",   // warning message shown to user
  "hookSpecificOutput": { }    // event-specific decision control (see below)
}
```

## hookSpecificOutput Per Event

**PreToolUse** — richest decision surface:
```json
{
  "hookEventName": "PreToolUse",
  "permissionDecision": "allow|deny|ask|defer",
  "permissionDecisionReason": "string",
  "updatedInput": { },          // replaces entire tool input before execution
  "additionalContext": "string" // injected into Claude's context
}
```
`updatedInput` is the correct way to sanitize or transform tool inputs (e.g., strip dangerous flags from a Bash command).

**PostToolUse** — can signal block after execution:
```json
{
  "decision": "block",
  "reason": "string",
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": "string",
    "updatedMCPToolOutput": "any"  // replaces MCP tool output (MCP tools only)
  }
}
```
PostToolUse runs after execution — it cannot undo the tool call. `decision: block` communicates failure to Claude for self-correction, not prevention.

**UserPromptSubmit:**
```json
{
  "hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit",
    "additionalContext": "string",
    "sessionTitle": "string"     // auto-renames the session
  }
}
```

**SessionStart:**
```json
{ "hookSpecificOutput": { "hookEventName": "SessionStart", "additionalContext": "string" } }
```

**PermissionRequest:**
```json
{
  "hookSpecificOutput": {
    "hookEventName": "PermissionRequest",
    "decision": { "behavior": "allow|deny", "updatedInput": { }, "message": "string" }
  }
}
```

**Output size cap:** hookSpecificOutput, systemMessage, and plain stdout injected into context are capped at 10,000 characters; excess is saved to a file with a preview path returned.

## Handler Types

All handlers share: `type`, `if` (conditional expression), `timeout` (seconds), `statusMessage`, `once` (skills only).

**command** — shell script (default; use for all deterministic enforcement):
```json
{ "type": "command", "command": "string", "async": false, "shell": "bash|powershell" }
```

**http** — POST to external endpoint (30s default timeout; lower than 600s command default):
```json
{ "type": "http", "url": "string", "headers": { }, "allowedEnvVars": ["string"] }
```
2xx = success; non-2xx = non-blocking error; connection failures are non-blocking.

**prompt** — single-turn LLM evaluation (no tool access, no file reads):
```json
{ "type": "prompt", "prompt": "string", "model": "string (optional, defaults to fast model)" }
```
Use for semantic classification where a rule is too nuanced for shell logic. Slower and costlier than command.

**agent** — multi-turn subagent with full tool access:
```json
{ "type": "agent", "prompt": "string", "model": "string (optional)" }
```
Use for deep verification requiring file reads or code analysis. Significant API cost — reserve for high-value completion gates, not per-file operations.

## Handler Selection Rule

Default to `command`. Use `prompt` when the enforcement criterion requires semantic judgment (e.g., "does this response stay on task?"). Use `agent` when the check requires file access beyond the current tool input. Use `http` when integrating with an external webhook or policy service.
