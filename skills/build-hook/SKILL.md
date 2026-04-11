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
---

# Build Hook

Scaffold a Claude Code hook: an event-driven script that enforces quality
gates deterministically, bypassing LLM interpretation.

## Elicit

Ask three things, one question at a time:

**1. Hook event** — which lifecycle moment should trigger this hook?

| Category | Events |
|----------|--------|
| Tool execution | `PreToolUse` (fires before; can block), `PostToolUse` (fires after; cannot prevent), `PostToolUseFailure` |
| Session lifecycle | `SessionStart`, `SessionEnd`, `UserPromptSubmit`, `PreCompact`, `PostCompact` |
| Agent coordination | `Stop`, `SubagentStop`, `SubagentStart` |
| Permission | `Notification` (observability only), `PermissionRequest`, `PermissionDenied` |

If the goal is to *block* or *prevent* something, the event must be
`PreToolUse` — `PostToolUse` fires after execution and cannot prevent it.

**2. Handler type** — how should the hook execute?
- `command` — shell script (default; use for most enforcement goals)
- `http` — POST to an external endpoint
- `prompt` — single-turn LLM evaluation
- `agent` — multi-turn subagent with file and command access

Default to `command` unless the user has a specific reason otherwise.

**3. Enforcement goal** — one sentence: what should this hook enforce or
detect? Confirm the goal before drafting.

## Draft

Produce two artifacts.

**Artifact 1: Hook script** (for `command` type — adapt for other types)

```bash
#!/bin/bash
# Hook: [enforcement goal]
# Event: [hook event]

set -euo pipefail

INPUT=$(cat)

# [enforcement logic here]

exit 0
```

The script receives a JSON payload on stdin with fields:
`session_id`, `transcript_path`, `cwd`, `hook_event_name`, `tool_name`,
`tool_input`, `tool_use_id`, `permission_mode`.

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
            "command": ".claude/hooks/[name].sh",
            "timeout": 60
          }
        ]
      }
    ]
  }
}
```

Include `matcher` when the event is tool-scoped (PreToolUse, PostToolUse).
Matcher syntax: simple name (`"Bash"`), pipe-separated (`"Write|Edit|MultiEdit"`),
wildcard (`"*"`), or regex (`"mcp__memory__.*"`).

Present both artifacts to the user before any safety checks.

## Safety Check

Review the draft script against four criteria. Revise before proceeding if
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

## Stop Hook Guard

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

## Security Note

`.claude/settings.json` is a repository file. Any collaborator with commit
access can inject hooks that execute arbitrary commands on the machine of
anyone who opens the project (CVE-2025-59536). This is not a hypothetical
— hooks run automatically without prompting when trusted.

Operational implication: treat hook additions to `settings.json` with the
same code-review scrutiny as executable source files. The enhanced warning
dialog Anthropic added after the CVE is the last line of defense.

## Rule Overlap

Check `CLAUDE.md` for instructions that already express the same enforcement
goal.

If overlap is found, note it and ask:
> "There's already a CLAUDE.md instruction that says [X]. A hook enforces
> this deterministically (CLAUDE.md is advisory; hooks aren't). Do you
> want the hook for guaranteed enforcement, or is the instruction sufficient?"

Both can be intentional (belt-and-suspenders); one may be stale. The user
decides.

## Review Gate

Present both artifacts — the complete hook script and the settings.json
snippet — and wait for explicit user approval before writing any file to
disk. Do not write anything before this gate passes.

If the user requests changes, revise and re-present.

## Save

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

## Handoff

**Receives:** Hook event, handler type, enforcement goal
**Produces:** Hook script at `.claude/hooks/<name>.sh` and a settings.json entry snippet
**Chainable to:** audit-hook (to verify the hook configuration after creation)
