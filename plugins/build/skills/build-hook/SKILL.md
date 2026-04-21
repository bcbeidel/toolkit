---
name: build-hook
description: >
  Builds a Claude Code hook (event-driven quality gate) with a script and
  the corresponding settings.json hooks entry. Use when the user wants to
  "create a hook", "add a PostToolUse hook", "build a hook", "enforce
  quality on tool use", "set up automated quality gates", "run a script
  after tool use", or "block dangerous operations automatically".
argument-hint: "[hook event] [enforcement goal]"
user-invocable: true
references:
  - ../../_shared/references/primitive-routing.md
---

# Build Hook

Scaffold a Claude Code hook: an event-driven script that enforces quality
gates deterministically, bypassing LLM interpretation.

**Workflow sequence:** 1. Route → 2. Elicit → 3. Draft → 4. Safety Check → (5. Stop Hook Guard if Stop/SubagentStop) → 6. Rule Overlap → 7. Review Gate → 8. Save → 9. Test

## 1. Route

Determine whether a hook is the right primitive before asking hook-specific questions. Full decision matrix: [primitive-routing.md](../../_shared/references/primitive-routing.md).

- **Goal is an unconditional permanent block** (never allow tool X, no conditions, ever) →
  suggest `settings.json` `permissions.deny` instead. No logic, no script, cannot be bypassed by exit codes.
- **Goal is advisory guidance or procedural instruction** (prefer X, follow this convention) →
  suggest CLAUDE.md or `/build:build-skill` instead. Hooks enforce mandatory behavior regardless of LLM judgment — not preferences.
- **Goal is a semantic judgment on file content** (convention too nuanced for grep) →
  suggest `/build:build-rule` instead. Rules use LLM evaluation; hooks use shell scripts.
- **Goal has a specific lifecycle trigger and must fire regardless of LLM judgment** →
  proceed to Elicit.

## 2. Elicit

If `$ARGUMENTS` is non-empty, parse it as `[hook-event] [enforcement-goal]` —
pre-fill the two fields below from the tokens, confirm them with the user, and
only ask the handler-type question. Otherwise:

Ask three things, one question at a time:

**1. Hook event** — which lifecycle moment should trigger this hook?

| Category | Events |
|----------|--------|
| Tool execution | `PreToolUse` (blockable), `PostToolUse` (cannot prevent), `PostToolUseFailure` |
| Session lifecycle | `SessionStart`, `SessionEnd`, `UserPromptSubmit` (blockable), `PreCompact` (blockable), `PostCompact`, `InstructionsLoaded`, `ConfigChange` (blockable), `CwdChanged`, `FileChanged` |
| Agent coordination | `Stop` (blockable), `StopFailure`, `SubagentStart`, `SubagentStop` (blockable), `TeammateIdle` (blockable) |
| Tasks & worktrees | `TaskCreated` (blockable), `TaskCompleted` (blockable), `WorktreeCreate` (**any** non-zero exit fails creation), `WorktreeRemove` |
| Permission & MCP | `Notification` (observability only), `PermissionRequest` (blockable), `PermissionDenied`, `Elicitation` (blockable), `ElicitationResult` (blockable) |

If the goal is to *block* or *prevent* something, the event must be
`PreToolUse` — `PostToolUse` fires after execution and cannot prevent it.

**2. Handler type** — how should the hook execute?
- `command` — shell script (default; use for most enforcement goals)
- `http` — POST to an external endpoint
- `prompt` — single-turn LLM evaluation (adds per-call API cost and latency; avoid on high-frequency events like `PreToolUse`)
- `agent` — multi-turn subagent with file and command access (spawns a full Claude session per invocation; significant cost; use only for complex multi-step judgment)

Default to `command` unless the user has a specific reason otherwise.

**3. Enforcement goal** — one sentence: what should this hook enforce or
detect? Confirm the goal before drafting.

## 3. Draft

Produce two artifacts.

**Artifact 1: Hook script** (for `command` type — adapt for other types)

```bash
#!/usr/bin/env bash
# Hook: [enforcement goal]
# Event: [hook event]

set -Eeuo pipefail

INPUT=$(cat)

# [enforcement logic here]

exit 0
```

The script receives a JSON payload on stdin with fields:
`session_id`, `transcript_path`, `cwd`, `hook_event_name`, `tool_name`,
`tool_input`, `tool_use_id`, `permission_mode`.

`tool_input` structure is tool-specific — extracting the wrong field returns `null` silently:

| Tool(s) | jq path |
|---------|---------|
| `Bash` | `.tool_input.command` |
| `Write` | `.tool_input.file_path`, `.tool_input.content` |
| `Edit`, `MultiEdit` | `.tool_input.path` |
| `Read`, `Glob`, `Grep` | `.tool_input.path` or `.tool_input.pattern` |
| `WebFetch`, `WebSearch` | `.tool_input.url` |

Adapt jq field paths when repurposing a hook across tool types.

**Safe payload extraction:** Always quote extracted values. Use `jq -r` and
store results in variables before use. Never interpolate payload fields directly
into jq filter strings — use `--arg` for shell variable injection:

```bash
TOOL_NAME="$(echo "${INPUT}" | jq -r '.tool_name')"
CMD="$(echo "${INPUT}" | jq -r '.tool_input.command // empty')"

# Passing a shell variable into a jq filter safely
RESULT="$(echo "${INPUT}" | jq --arg key "${TOOL_NAME}" '.fields[$key]')"
```

`tool_input.command` in Bash hooks reflects what the user asked Claude to run —
treat it as untrusted input. Use `[[` over `[` for conditionals. Send error
messages to STDERR (`>&2`). Guard `grep`, `diff`, and similar commands with
`|| true` when a non-zero exit is expected behavior.

**ERR/EXIT traps (optional):** Add structured error context and cleanup:

```bash
trap 'echo "Error on line ${LINENO}: ${BASH_COMMAND}" >&2' ERR
trap 'rm -f "${TMPFILE:-}"' EXIT
```

Use `set -x` only during local debugging — in production it floods stderr and
can leak payload values from the JSON input in traces.

**Style:** Use `lower_case_with_underscores` for local variables and functions;
`UPPER_CASE_WITH_UNDERSCORES` for exported variables and constants. When the
script contains named functions, add a `main()` function and call it at the end:
`main "$@"`.

**`updatedInput` (PreToolUse only):** To sanitize or transform tool input instead
of blocking, print JSON to stdout on exit 0:

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "updatedInput": { "command": "<sanitized-command>" }
  }
}
```

This replaces the entire `tool_input` before execution. Use this when the goal is
to strip dangerous flags rather than refuse the operation entirely.

**Broader JSON output contract.** stdout on exit 0 may carry these fields; stdout
on any non-zero exit is ignored. stdout must be **only** the JSON object — any
leading text triggers "JSON validation failed."

- `hookSpecificOutput.hookEventName` (required) — echo the event name.
- `permissionDecision: "allow" | "deny" | "ask" | "defer"` plus
  `permissionDecisionReason` — PreToolUse / PermissionRequest block-or-allow
  channel. Precedence across hooks: `deny > defer > ask > allow`.
- `decision: "block"` + `reason` — top-level field for UserPromptSubmit,
  PostToolUse, Stop, SubagentStop, PreCompact, ConfigChange, TaskCreated,
  TaskCompleted.
- `additionalContext` — extra text injected into Claude's view; capped at
  10,000 characters (spec-wide truncation rule).
- `continue: false` + `stopReason` — halts the entire conversation.
- `systemMessage` — user-visible message.
- `suppressOutput: true` — omits hook output from the debug log (keeps
  functional effects like `additionalContext` / `decision` intact).
- `sessionTitle` (UserPromptSubmit only) — auto-names the session.
- `retry: true` (PermissionDenied only) — tells Claude it may retry the
  denied tool call.
- `worktreePath` (WorktreeCreate, HTTP handlers) — required return field;
  command handlers print the path to stdout instead.

**Artifact 2: settings.json entry**

```json
{
  "hooks": {
    "[EventName]": [
      {
        "matcher": "[tool name, pipe-separated, or * for all]",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/[name].sh",
            "timeout": 60
          }
        ]
      }
    ]
  }
}
```

Spec defaults: 600 s for command hooks, 30 s for prompt, 60 s for agent.
Lower `"timeout"` for tight gates (10–60 s typical) so a stuck hook fails
fast; raise only when the enforcement step genuinely needs it. A hook that
exceeds its timeout is treated as non-blocking — the operation proceeds
and a hook error appears in the transcript. Slow synchronous hooks
accumulate session sluggishness and create pressure to bypass enforcement.

Optional command-handler fields: `"shell": "bash" | "powershell"` (explicit
shell selection for cross-platform hooks); `"statusMessage": "..."` (spinner
text shown while the hook runs); `"asyncRewake": true` (async hook that wakes
Claude on exit 2 with stderr/stdout, implies `async: true`). HTTP handlers
accept `"headers"` and `"allowedEnvVars"`; prompt/agent handlers accept
`"model"` (defaults to the fast model for prompt).

Include `matcher` when the event is tool-scoped (PreToolUse, PostToolUse).
Matcher syntax: simple name (`"Bash"`), pipe-separated (`"Write|Edit|MultiEdit"`),
wildcard (`"*"`), or regex (`"mcp__memory__.*"`).

**Three-tier matcher evaluation** (determined by pattern content, not a flag):
- `"*"`, `""`, or omitted → wildcard: fires on every tool call for this event
- Alphanumeric + pipe only (e.g., `"Write|Edit|MultiEdit"`) → exact match or pipe-separated list
- Any other character (e.g., `"mcp__memory__.*"`, `"^Notebook"`) → JavaScript regex (not POSIX; case-sensitive)

**FileChanged matcher exception.** `FileChanged` treats `matcher` as a
`|`-separated list of literal filenames, not a regex. `".envrc|.env"` watches
those two files; regex syntax there is not interpreted. An MCP matcher like
`"mcp__memory"` (no trailing `.*`) is exact-match and matches nothing — use
`"mcp__memory__.*"` for regex scope.

**`if` field** (v2.1.85+): filters individual handlers by tool name and arguments. The hook
process does not spawn at all when `if` doesn't match — tighter than `matcher` alone and
reduces per-call latency. Example: `"if": "Bash(git *)"` fires only for `git` subcommands.
Only works on tool events (`PreToolUse`, `PostToolUse`, etc.); on non-tool events it prevents
the hook from running entirely.

Present both artifacts to the user before any safety checks.

## 4. Safety Check

With the draft script from the preceding step in hand, review it against eleven criteria. Revise before proceeding if
any fail.

1. **No destructive operations** — flag `rm -rf`, `git reset --hard`,
   `git checkout .`, `git push --force`. A hook should never delete or
   overwrite work without explicit user action.

2. **Idempotent** — running the hook twice must produce the same outcome.
   No unbounded log appending, no counter incrementing, no side effects
   that accumulate across invocations.

3. **No unintended side effects** — the hook should do exactly what the
   enforcement goal specifies. Flag anything beyond that scope.

4. **Exit code correctness** — blocking hooks must use `exit 2`. `exit 1`
   is non-blocking: the error appears in the transcript but execution
   continues. A hook configured with `"async": true` can never block
   regardless of exit code — flag this combination as a misconfiguration.
   For Python hooks: uncaught exceptions exit 1 (non-blocking). All
   blocking paths must call `sys.exit(2)` explicitly; all pass paths must
   call `sys.exit(0)` — do not rely on interpreter fall-through.

5. **Stdin correctness** — the script must contain `INPUT=$(cat)` at or near
   the top. Scripts that don't consume stdin will hang or fail silently when
   the JSON payload exceeds the OS pipe buffer. Flag and add the line if missing.

6. **Tool name case sensitivity** — verify the matcher uses exact canonical
   casing: `Bash`, `Write`, `Edit`, `MultiEdit`, `Read`, `Glob`, `Grep`. A
   matcher on `bash` or `write` silently matches nothing and disables the hook.

7. **Injection safety** — `tool_input` fields are user-influenced. Three
   checks: (a) no `eval` on any payload-derived value; (b) all variable
   expansions quoted as `"${var}"`; (c) external commands invoked by absolute
   path (`/usr/bin/jq`) or guarded with `command -v` availability check.

8. **ShellCheck + shfmt** — run `shellcheck .claude/hooks/<name>.sh` and fix all
   warnings. ShellCheck catches quoting issues, deprecated syntax, and command
   misuse. It does not catch wrong exit code intent or incorrect jq field
   paths — those require testing with real payloads (see Test section).
   Also run `shfmt -i 2 -w .claude/hooks/<name>.sh` for consistent formatting.
   If ShellCheck produces false positives specific to hook patterns (e.g., SC2034
   for jq-assigned variables, SC2016 for intentionally single-quoted JSON strings),
   suppress them inline or via a `.shellcheckrc` rather than disabling ShellCheck
   wholesale.

9. **jq availability** — `jq` is not guaranteed to be in Claude Code's
   restricted PATH. Add an availability check at the top of any hook that
   depends on it:
   ```bash
   command -v jq &>/dev/null || { echo "jq required but not installed" >&2; exit 2; }
   ```
   For portability, fall back to `python3 -c "import json,sys; ..."` when `jq`
   cannot be guaranteed.

10. **Latency** — Synchronous hooks block Claude while they run. Flag hooks
    that spawn LLM calls, network requests, or recursive scans — target under
    1 second. Move non-critical work to `async: true`.

11. **Non-deterministic `updatedInput`** — If more than one PreToolUse hook
    returns `updatedInput` for the same tool, the last to finish wins (hooks
    run in parallel). Flag this as a misconfiguration; consolidate all input
    modifications for a given tool into one hook.

## 5. Stop Hook Guard

**Only for `Stop` and `SubagentStop` events.** Skip this section for all
other events.

A Stop hook that exits 2 (blocking) without checking `stop_hook_active`
traps Claude in an infinite loop. Add this guard at the top of the script:

```bash
STOP_ACTIVE=$(echo "$INPUT" | python3 -c \
  "import sys, json; d=json.load(sys.stdin); print(d.get('stop_hook_active', False))")
[ "$STOP_ACTIVE" = "True" ] && exit 0
```

This check is mandatory for any Stop/SubagentStop hook that may exit 2.

**Important:** `stop_hook_active` is a **SubagentStop-only** field — it is
absent from `Stop` event payloads (which include `stop_reason` instead). The
guard above works for SubagentStop. For `Stop` hooks, use one of three
loop-break layers (all three is belt-and-suspenders for production gates):

1. **`stop_hook_active` field** — SubagentStop only; exits 0 on re-entry.
2. **Progress-indicator check on `last_assistant_message`** (SubagentStop
   payload field) — exit 0 if the subagent is making progress toward the
   hook's requirement, so the block resolves when the subagent completes
   the work.
3. **Session-scoped guard file** keyed to `session_id` — touch a temp file
   on first block; exit 0 if it already exists. Necessary for `Stop` hooks
   since its payload lacks `stop_hook_active`.

Without at least one layer, a blocking Stop/SubagentStop hook loops until the
session is killed.

## Security Note

`.claude/settings.json` is a repository file. Any collaborator with commit
access can inject hooks that execute arbitrary commands on the machine of
anyone who opens the project (CVE-2025-59536). This is not a hypothetical
— hooks run automatically without prompting when trusted.

Operational implication: treat hook additions to `settings.json` with the
same code-review scrutiny as executable source files. The enhanced warning
dialog Anthropic added after the CVE is the last line of defense.

**Recursive-loop safety (spec warning).** Avoid invoking `claude` or
`claude-code` from inside a hook command — each spawn re-fires hooks on the
nested session and compounds exponentially. This is distinct from the
Stop-hook infinite-loop case (§5): even non-Stop hooks that shell out to
Claude can cause runaway spawning. If LLM-mediated decisions genuinely need
to run inside a hook, use `type: "prompt"` or `type: "agent"` handlers
instead of a shell-out to `claude`.

## Known Limitations

Three permanent limitations that affect hook design decisions:

- **Path expansion:** Use `$CLAUDE_PROJECT_DIR` (or an absolute path) in
  `settings.json` `"command"` values. `$CLAUDE_PROJECT_DIR` is guaranteed
  to resolve to the project root regardless of cwd; `$HOME` and `~` have
  been observed to expand inconsistently across versions and silently fail
  to load the script. Verify the hook appears in `/hooks` after any path
  change. Plugin-bundled hooks additionally get `${CLAUDE_PLUGIN_ROOT}`
  (install dir, changes on update) and `${CLAUDE_PLUGIN_DATA}` (persistent
  data dir, survives updates). `$CLAUDE_ENV_FILE` is available inside
  `SessionStart`, `CwdChanged`, and `FileChanged` hook scripts for
  persisting environment variables into the session.
- **Non-interactive mode:** Under `claude -p` (non-interactive / CI), the
  `AskUserQuestion` and `ExitPlanMode` tools block because there is no user to
  answer them. The documented workaround is a `PreToolUse` hook that returns
  `permissionDecision: "allow"` with an `updatedInput` supplying the answer.
  Anchor CI-critical enforcement on `PreToolUse`, not on interactive-only
  events.
- **Shell profile pollution:** `~/.bashrc` or `~/.zshrc` statements that emit
  output unconditionally corrupt the stdin JSON pipe and cause hook parse
  failures. Fix by guarding interactive-only output:
  ```bash
  if [[ $- == *i* ]]; then echo "Shell ready"; fi
  ```
  Claude Code spawns hooks in non-interactive shells, so the `i` flag is absent
  and the guarded block is skipped.

## 6. Rule Overlap

Check `CLAUDE.md` for instructions that already express the same enforcement
goal.

If overlap is found, note it and ask:
> "There's already a CLAUDE.md instruction that says [X]. A hook enforces
> this deterministically (CLAUDE.md is advisory; hooks aren't). Do you
> want the hook for guaranteed enforcement, or is the instruction sufficient?"

Both can be intentional (belt-and-suspenders); one may be stale. The user
decides.

## 7. Review Gate

Present both artifacts — the complete hook script and the settings.json
snippet — and wait for explicit user approval before writing any file to
disk. Write only after this gate passes.

If the user requests changes, revise and re-present. Continue this loop
until the user explicitly approves the artifacts or cancels. Proceed to
Save only on explicit approval.

## 8. Save

Write the approved hook to `.claude/hooks/<name>.sh` (or a path the user
specifies). Make it executable:

```bash
chmod +x .claude/hooks/<name>.sh
```

Show the settings.json patch for the user to apply manually. Do not
auto-patch `settings.json` — it may contain permission entries that
should not be overwritten.

> "Hook script written to `.claude/hooks/<name>.sh`. Add the settings
> entry shown above to `.claude/settings.json` (or settings.local.json
> for local-only enforcement) to activate it."

## 9. Test

Read `references/hook-testing.md` and follow the three-layer verification
procedure (configuration, logic isolation, execution trace) before activating
the hook.

After testing, offer:

> "Run `/build:check-hook` to audit the configuration for coverage gaps,
> misconfigurations, and safety issues?"

## Anti-Pattern Guards

1. **Skipping primitive routing** — always run Route before Elicit; a goal that fits `permissions.deny` or CLAUDE.md should never reach the Draft step
2. **Blocking via PostToolUse** — PostToolUse cannot prevent execution; presenting a PostToolUse draft for a blocking goal is a misconfiguration that silently fails to enforce
3. **Using `async: true` with exit 2** — async hooks run after execution proceeds regardless of exit code; a hook that needs to block must be synchronous
4. **Writing files before the Review Gate** — presenting the artifacts and proceeding immediately without waiting for explicit approval bypasses the only safety checkpoint
5. **Auto-patching `settings.json`** — the settings file may contain permission entries and hook arrays that should not be overwritten; always show the snippet and let the user apply it

## Key Instructions

- Do not write any file to disk before the Review Gate passes — present both artifacts first, wait for explicit user approval
- Do not auto-patch `settings.json`; always show the snippet for the user to apply manually
- Won't build a hook when `permissions.deny` covers the goal — unconditional permanent blocks don't need logic or a script
- Won't build a hook for advisory guidance or preferences — suggest CLAUDE.md or a skill instead
- Won't skip the Safety Check — run all eleven criteria before declaring the draft ready
- Recovery if a hook is written in error: run `chmod -x .claude/hooks/<name>.sh` to disable without deleting, or remove the file and the matching `settings.json` entry; a configured hook whose script is missing or non-executable silently fails and leaves normal tool flow intact

## Handoff

**Receives:** Hook event, handler type, enforcement goal
**Produces:** Hook script at `.claude/hooks/<name>.sh` and a settings.json entry snippet
**Chainable to:** check-hook (to verify the hook configuration after creation)
