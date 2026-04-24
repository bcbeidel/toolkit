---
name: Hook Best Practices
description: Authoring guide for Claude Code hooks — event-driven handlers registered in settings.json that fire at lifecycle moments to enforce quality gates deterministically. Referenced by build-hook and check-hook.
---

# Hook Best Practices

## What a Good Hook Does

A hook is a deterministic gate. It runs because a lifecycle event happened —
a tool is about to execute, a session started, a file changed — not because
Claude judged the situation to warrant it. That determinism is the entire
value proposition: when "usually" is not good enough, a hook is the primitive
that ships guaranteed enforcement.

A hook earns its place when three conditions hold: (1) the goal is an
*invariant*, not a preference — one false positive per session is enough to
generate bypass culture and nullify the gate; (2) the enforcement point maps
to a specific lifecycle event; (3) the check can be expressed in a shell
one-liner or a lean script. If any of those three fails — advisory guidance,
no lifecycle hook, semantic judgment required — the goal belongs to a
different primitive (CLAUDE.md, a rule, a skill).

**What a hook is not.** Not an unconditional static block (that is
`permissions.deny`). Not a preference (that is CLAUDE.md). Not semantic
evaluation of file content (that is a rule). Not a procedure invoked by Claude
(that is a skill).

## Anatomy

### Event selection

Hooks fire on named lifecycle events. The event determines what the hook can
do — PreToolUse can block, PostToolUse cannot; Stop and SubagentStop have
loop-protection obligations; non-tool events have different payload shapes.

| Category | Events | Blockable? |
|----------|--------|------------|
| Tool execution | `PreToolUse`, `PostToolUse`, `PostToolUseFailure` | PreToolUse only |
| Session lifecycle | `SessionStart`, `SessionEnd`, `UserPromptSubmit`, `PreCompact`, `PostCompact`, `InstructionsLoaded`, `ConfigChange`, `CwdChanged`, `FileChanged` | UserPromptSubmit / PreCompact / ConfigChange |
| Agent coordination | `Stop`, `StopFailure`, `SubagentStart`, `SubagentStop`, `TeammateIdle` | Stop / SubagentStop / TeammateIdle |
| Tasks & worktrees | `TaskCreated`, `TaskCompleted`, `WorktreeCreate`, `WorktreeRemove` | TaskCreated / TaskCompleted / WorktreeCreate (any non-zero) |
| Permission & MCP | `Notification`, `PermissionRequest`, `PermissionDenied`, `Elicitation`, `ElicitationResult` | PermissionRequest / Elicitation / ElicitationResult |

The single most common misconfiguration is routing a blocking intent through
`PostToolUse`: the tool has already run, the exit code is ignored, the gate
silently fails.

### Handler types

| Type | When | Cost |
|------|------|------|
| `command` | Most enforcement goals | None beyond subprocess |
| `http` | POST to external endpoint | Network |
| `prompt` | Single-turn LLM evaluation | API cost + latency |
| `agent` | Multi-turn subagent with tools | Full Claude session |

Default to `command`. Reach for `prompt`/`agent` only when the judgment
genuinely needs an LLM — on a high-frequency event like `PreToolUse`, the
per-call cost accumulates into session sluggishness.

### Matcher syntax

Matchers select which tool invocations fire the hook. The matcher is a field
on each hook entry in `settings.json` and follows a three-tier evaluation
determined by the pattern content (not a flag):

1. `"*"`, `""`, or omitted → wildcard: fires on every tool call for this event
2. Alphanumeric + pipe only (`"Write|Edit|MultiEdit"`) → exact match or list
3. Any other character (`"mcp__memory__.*"`, `"^Notebook"`) → JavaScript regex (not POSIX; case-sensitive)

Canonical tool names: `Bash`, `Write`, `Edit`, `MultiEdit`, `Read`, `Glob`,
`Grep`, `WebFetch`, `WebSearch`, `Agent`, `NotebookEdit`, `NotebookRead`. A
matcher of `bash` or `write` silently matches nothing.

**FileChanged exception.** `FileChanged` treats `matcher` as a `|`-separated
list of *literal filenames*, not a regex. `".envrc|.env"` watches those two
files; regex syntax is not interpreted there.

**The `if` field (v2.1.85+).** Filters individual handlers by tool name and
arguments — tighter than `matcher` alone, because the hook process does not
spawn at all when `if` doesn't match. Example: `"if": "Bash(git *)"` fires
only for `git` subcommands. Only works on tool events; on non-tool events
it prevents the hook from running entirely.

### Payload schema and extraction

The command handler receives a JSON payload on stdin with fields: `session_id`,
`transcript_path`, `cwd`, `hook_event_name`, `tool_name`, `tool_input`,
`tool_use_id`, `permission_mode`.

`tool_input` structure is tool-specific — extracting the wrong field returns
`null` silently:

| Tool(s) | jq path |
|---------|---------|
| `Bash` | `.tool_input.command` |
| `Write` | `.tool_input.file_path`, `.tool_input.content` |
| `Edit`, `MultiEdit` | `.tool_input.path` |
| `Read`, `Glob`, `Grep` | `.tool_input.path` or `.tool_input.pattern` |
| `WebFetch`, `WebSearch` | `.tool_input.url` |

**Safe extraction:** Always `jq -r`, store in a variable, then use. Never
interpolate payload fields directly into a jq filter — use `--arg`:

```bash
TOOL_NAME="$(echo "${INPUT}" | jq -r '.tool_name')"
CMD="$(echo "${INPUT}" | jq -r '.tool_input.command // empty')"
RESULT="$(echo "${INPUT}" | jq --arg key "${TOOL_NAME}" '.fields[$key]')"
```

Treat all `tool_input` fields as untrusted: they reflect what the user asked
Claude to do.

### Exit codes and the JSON output contract

Command hooks signal outcome through exit code plus optional stdout JSON.

| Exit | Meaning | stdout parsed? |
|------|---------|----------------|
| 0 | Pass (or structured response) | Yes, as JSON |
| 1 | Warn — error in transcript, execution proceeds | No |
| 2 | Block (PreToolUse / blockable events only) | No |
| other | Treated as 1 | No |

**JSON output contract (exit 0 only).** stdout must be a single JSON object
with no leading text. Fields:

- `hookSpecificOutput.hookEventName` — **required**, echo the event name
- `permissionDecision: "allow" | "deny" | "ask" | "defer"` + `permissionDecisionReason` — PreToolUse / PermissionRequest block-or-allow channel; precedence `deny > defer > ask > allow`
- `decision: "block"` + `reason` — top-level block for UserPromptSubmit, PostToolUse, Stop, SubagentStop, PreCompact, ConfigChange, TaskCreated, TaskCompleted
- `additionalContext` — injected into Claude's view; capped at 10,000 characters
- `continue: false` + `stopReason` — halts entire conversation
- `systemMessage` — user-visible message
- `suppressOutput: true` — omits hook output from debug log
- `sessionTitle` (UserPromptSubmit only) — auto-names session
- `retry: true` (PermissionDenied only) — tells Claude it may retry
- `worktreePath` (WorktreeCreate) — required return for HTTP handler; command handler prints to stdout instead
- `hookSpecificOutput.updatedInput` (PreToolUse only) — replaces `tool_input` entirely before execution; use to sanitize/transform rather than refuse

Hook stdout is **truncated silently at 10,000 characters** — large
`additionalContext` or `systemMessage` payloads get cut mid-JSON and surface
as "JSON validation failed" in the transcript.

### Settings.json entry shape

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/gate.sh",
            "timeout": 60
          }
        ]
      }
    ]
  }
}
```

Spec timeout defaults: 600 s for command, 30 s for prompt, 60 s for agent.
Tight gates should be 10–60 s so a stuck hook fails fast; a hook that
exceeds its timeout is treated as non-blocking (operation proceeds, error
in transcript).

Optional fields: `"shell": "bash" | "powershell"`, `"statusMessage"`,
`"asyncRewake": true` (implies `async: true`), `"headers"` and
`"allowedEnvVars"` (HTTP), `"model"` (prompt/agent; defaults to fast model
for prompt).

### Path expansion variables

- `$CLAUDE_PROJECT_DIR` — project root, resolves regardless of cwd; use this
- Absolute paths — also fine
- `$HOME` / `~` — expand inconsistently across versions; **silently fail** to load the script
- `$CLAUDE_PLUGIN_ROOT` — plugin install dir (changes on update)
- `$CLAUDE_PLUGIN_DATA` — plugin persistent data dir (survives updates)
- `$CLAUDE_ENV_FILE` — available inside `SessionStart`, `CwdChanged`, `FileChanged` for persisting env vars

### Script skeleton

```bash
#!/usr/bin/env bash
# Hook: <enforcement goal>
# Event: <hook event>

set -Eeuo pipefail

INPUT=$(cat)

command -v jq &>/dev/null || { echo "jq required" >&2; exit 2; }

# <enforcement logic>

exit 0
```

## Patterns That Work

**Warn before block.** Deploy a new blocking PreToolUse hook with `exit 1`
(warning only) for at least a week before graduating to `exit 2` (block).
Rationale: one false positive per session is sufficient to establish bypass
culture (`--no-verify`, matcher tweaks), and once bypass is cultural the
hook provides no protection.

**Safe variable injection.** Use `jq --arg key "${TOOL_NAME}"` to pass shell
variables into jq filters rather than interpolating. Payload fields passed
through string interpolation become a parse-time injection vector.

**Belt-and-suspenders Stop loops.** For `Stop` and `SubagentStop` hooks that
exit 2, layer all three loop-break mechanisms: (1) `stop_hook_active` check
(SubagentStop only); (2) progress check on `last_assistant_message`; (3)
session-scoped guard file keyed to `session_id`. The first alone is enough
for SubagentStop; the third is required for Stop (its payload lacks
`stop_hook_active`); the second lets the block resolve naturally once the
subagent satisfies the requirement rather than remaining a hard gate.

**Lean synchronous, async for the rest.** Synchronous hooks block Claude
while they run. Target <1 second for synchronous gates; push anything that
calls an LLM, touches the network, or runs a slow subprocess to
`"async": true`. Remember: async hooks *cannot* block regardless of exit code.

**Local-only enforcement in `settings.local.json`.** The file is gitignored
and per-developer — appropriate for personal credential-protection or
ergonomics. Team-wide enforcement lives in `settings.json` but must be
treated as executable code in review.

## Anti-Patterns

**Blocking via PostToolUse.** The tool has already executed; the exit code
cannot undo it. Fails to enforce silently.

**`async: true` with `exit 2`.** Async hooks run after the operation
proceeds. Exit 2 is ignored. Looks like a blocker; is not one.

**Unguarded `Stop` / `SubagentStop` with `exit 2`.** Creates an infinite
loop. Requires a session kill to recover.

**`$HOME` or `~` in `command`.** Expansion is inconsistent across Claude Code
versions; the hook silently fails to load. `$CLAUDE_PROJECT_DIR` is the
spec's reference pattern.

**Missing `INPUT=$(cat)`.** Scripts that do not consume stdin hang or fail
silently when the payload exceeds the OS pipe buffer.

**`eval` on payload values.** `tool_input.command` reflects user input; feeding
it to `eval` is shell injection with no safe sanitization.

**Unquoted payload expansions.** `$var` (not `"${var}"`) undergoes
word-splitting and globbing; payload content can exploit that.

**Bare command names in adversarial environments.** `jq`, `grep` without
absolute paths are susceptible to PATH hijack. Matters most in
project-level `settings.json` (team commit access) and CI (runner-injected PATH).

**Wrong jq field paths for the matcher.** `jq -r '.tool_input.command'` on a
Write hook returns `null` silently. Field paths must match the tool's
`tool_input` schema.

**Blocking enforcement on interactive-only events under `claude -p`.** CI /
non-interactive mode cannot answer `AskUserQuestion` or `ExitPlanMode`.
Anchor CI-critical enforcement on `PreToolUse` with an `updatedInput` response.

**Multiple `PreToolUse` hooks returning `updatedInput` for the same tool.**
Hooks run in parallel; last to finish wins. Non-deterministic silently.

**User-level hooks (`~/.claude/settings.json`) alongside CI usage.** Fires in
every project including CI automation. Enforcement designed for local
ergonomics applies where it was never reviewed.

## Safety & Maintenance

**Static analysis.** Run ShellCheck and `shfmt -i 2` on every hook script.
ShellCheck catches quoting errors, deprecated syntax, conditional misuse;
`shfmt` enforces consistent formatting. Both are a floor — wrong exit-code
intent and incorrect jq field paths remain invisible to static analysis.
When ShellCheck false-positives on jq-assigned variables (SC2034) or
single-quoted JSON strings (SC2016), suppress *inline* or via
`.shellcheckrc`, never wholesale.

**Shell hygiene preamble.** `set -Eeuo pipefail` at the top. Wrap detection
commands (`grep`, `diff`, `test`, `[`) that legitimately exit non-zero
with `|| true` or inside `if`; otherwise `-e` aborts the hook and produces
false positives. Use `[[` over `[`; use `#!/usr/bin/env bash` over
`#!/bin/bash` for portability. Never commit `set -x`.

**Output routing.** Errors and block messages go to stderr (`>&2`). stdout is
for structured JSON on exit 0; anything else on stdout is either parsed as
JSON (and fails) or ignored (wasted work).

**Attack surface (CVE-2025-59536).** Any collaborator with commit access to
project `settings.json` can inject hooks that execute arbitrary commands on
every team member's machine when the project is opened. Treat hook additions
to project `settings.json` with the same scrutiny as executable source.
Personal-only enforcement belongs in `settings.local.json`.

**Recursive-loop safety.** Never invoke `claude` or `claude-code` from inside
a hook command. Each spawn re-fires hooks on the nested session and compounds
exponentially. If LLM-mediated decisions genuinely need to run inside a hook,
use `type: "prompt"` or `type: "agent"` instead of shelling out to `claude`.

**Shell profile pollution.** If `~/.bashrc` / `~/.zshrc` emits output
unconditionally, that output corrupts the stdin JSON pipe and causes parse
failures. Guard interactive-only output: `if [[ $- == *i* ]]; then ...; fi`.

**Idempotency.** A hook that runs twice must produce the same outcome. No
unbounded log appending, no counter increments, no files that are never
cleaned up.

**Latency budget.** <1 second for synchronous hooks. Move anything slower to
`async: true`. Session sluggishness from slow hooks generates bypass pressure.

**CLAUDE.md overlap.** A hook that duplicates a CLAUDE.md instruction may be
intentional (belt-and-suspenders: advisory layer + deterministic layer), or
it may be stale. Surface the overlap; let the human decide. Do not treat
duplication as always-wrong.

**Known limitations:**
- **Path expansion** — only `$CLAUDE_PROJECT_DIR` and absolute paths are guaranteed.
- **Non-interactive (`claude -p`)** — `AskUserQuestion` and `ExitPlanMode` block; use a PreToolUse hook with `permissionDecision: "allow"` + `updatedInput` to pre-answer.
- **Shell profile pollution** — non-interactive shells spawn hooks; guard interactive-only output.
- **Copilot compatibility** — Copilot serializes tool arguments as `toolArgs` (JSON string), not `tool_input` (object). Cross-platform hooks require a detection branch or separate configurations.
