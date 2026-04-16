---
name: Hook Matcher Syntax
description: "Exact rules for Claude Code hook matcher evaluation: three-tier syntax (wildcard, exact/pipe, JavaScript regex), per-event matcher targets, argument filtering, and MCP tool patterns"
type: reference
confidence: high
created: 2026-04-13
updated: 2026-04-13
sources:
  - https://code.claude.com/docs/en/hooks
related:
  - docs/context/hooks-deterministic-enforcement-vs-advisory.context.md
  - docs/context/hook-event-payload-schemas.context.md
  - docs/research/2026-04-13-hook-quality-and-evaluation.research.md
---
Matchers control which events trigger a hook. The evaluation rule uses three tiers based on pattern content — not a flag or syntax prefix.

## Three-Tier Evaluation Rule

| Pattern | Condition | Behavior |
|---------|-----------|----------|
| `"*"`, `""`, or omitted | — | Match all (wildcard) |
| Only `[a-zA-Z0-9_\|]` | alphanumeric + pipe only | Exact string match or `\|`-separated list |
| Any other characters | contains `.`, `^`, `*`, `(`, etc. | Treated as **JavaScript regex** |

Examples:
- `"Bash"` — exact match on tool name Bash
- `"Write\|Edit\|MultiEdit"` — matches any of the three
- `"mcp__memory__.*"` — JS regex: all tools from the memory MCP server
- `"^Notebook"` — JS regex: tools whose names start with "Notebook"
- `"Bash(npm test*)"` — argument filter (see below)

**Regex flavor is JavaScript (case-sensitive).** POSIX regex syntax will not work. `\d`, `\w`, lookaheads are valid; POSIX character classes (`[:alpha:]`) are not.

## Per-Event Matcher Targets

The matcher field filters on a different property depending on the event:

| Event | Matcher filters on |
|-------|--------------------|
| PreToolUse, PostToolUse, PostToolUseFailure, PermissionRequest, PermissionDenied | `tool_name` |
| SessionStart | `source` (`startup`, `resume`, `clear`, `compact`) |
| SessionEnd | `reason` (`clear`, `resume`, `logout`, `prompt_input_exit`, `other`) |
| Notification | `notification_type` |
| SubagentStart, SubagentStop | `agent_type` |
| PreCompact, PostCompact | `trigger` (`manual`, `auto`) |
| FileChanged | Literal filenames only (no regex) |
| UserPromptSubmit, Stop, TeammateIdle, TaskCreated, TaskCompleted, WorktreeCreate, WorktreeRemove, CwdChanged | **No matcher support** — always fire |

## Argument Filtering

For `Bash` hooks, append the argument pattern in parentheses to filter on the command string:

```
"Bash(npm test*)"   — matches Bash calls whose command starts with "npm test"
"Bash(git commit*)" — matches git commit operations specifically
"Bash(rm *)"        — matches any rm command
```

This is the correct way to gate on specific shell commands without running the hook on every Bash call.

## The `if` Field: Argument-Level Filtering (v2.1.85+)

The `matcher` field filters at the hook *group* level by tool name. The `if` field filters individual *handlers* by tool name and arguments together, using permission rule syntax. The hook process does not spawn at all when `if` doesn't match — reducing per-call latency beyond what matcher alone provides.

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Bash",
      "hooks": [
        { "if": "Bash(git *)", "command": "check-git-policy.sh" },
        { "if": "Bash(npm *)", "command": "check-npm-policy.sh" }
      ]
    }]
  }
}
```

Without `if`, both handlers spawn for every Bash call. With `if`, each handler spawns only for its matching command prefix.

**`if` field rules:**
- Only works on tool events: `PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `PermissionRequest`, `PermissionDenied`
- Adding it to non-tool events (Stop, SessionStart, etc.) prevents the hook from running entirely
- Uses permission rule syntax: `"Bash(git *)"`, `"Edit(*.ts)"`, `"Write(src/*)"` are all valid
- Requires Claude Code v2.1.85 or later; earlier versions ignore the field and run the hook on every matched call

**`if` vs. argument filtering in `matcher`:** `"Bash(npm test*)"` in the `matcher` field filters the entire group; `"if": "Bash(npm test*)"` on a handler filters that handler only. Use `matcher` when all handlers in a group share the same scope; use `if` for per-handler scoping within a shared group.

## MCP Tool Naming and Matching

MCP tools follow the pattern `mcp__<server>__<tool>`:
- `mcp__memory__create_entities`
- `mcp__filesystem__read_file`
- `mcp__github__search_repositories`

Useful matcher patterns:
```
mcp__memory__.*        — all tools from the memory server
mcp__.*__write.*       — any write-prefixed tool from any server
mcp__github__.*        — all GitHub MCP tools
```

## Deduplication

Identical command strings or URLs run only once even if matched by multiple hook rules. A hook that appears twice (e.g., in user settings and project settings) with the same command will execute once, not twice.

Matchers with `"permissionDecision": "defer"` in their JSON output pause execution for integrations using the `-p` flag (non-interactive mode).

## Tool Name Case Sensitivity

Tool names are case-sensitive. `Bash` ≠ `bash`. The canonical names as of 2026:
`Bash`, `Write`, `Edit`, `MultiEdit`, `Read`, `Glob`, `Grep`, `WebFetch`, `WebSearch`, `Agent`, `AskUserQuestion`, `ExitPlanMode`, `NotebookEdit`, `NotebookRead`.

A matcher on `bash` matches nothing. Verify with exact casing from the hooks reference.
