---
name: Hook Testing and Debugging
description: "Three-layer debugging stack for Claude Code hooks: configuration verification → logic isolation → execution trace; performance profiling and payload capture strategies"
type: context
sources:
  - https://code.claude.com/docs/en/hooks-guide
  - https://blakecrosley.com/blog/claude-code-hooks-tutorial
  - https://stevekinney.com/courses/ai-development/claude-code-hook-control-flow
  - https://thinkingthroughcode.medium.com/the-silent-failure-mode-in-claude-code-hook-every-dev-should-know-about-0466f139c19f
related:
  - docs/research/2026-04-13-hook-quality-and-evaluation.research.md
  - docs/context/hook-quality-criteria.context.md
  - docs/context/hook-event-payload-schemas.context.md
  - docs/context/hooks-deterministic-enforcement-vs-advisory.context.md
---
Hook silent failures require three distinct verification layers — each catches a different class of failure. Skipping a layer leaves a gap that surfaces only in production.

## Three-Layer Debugging Stack

**Layer 1: Configuration verification (`/hooks` menu)**

Type `/hooks` in Claude Code to see all configured hooks grouped by event, with counts. Selecting a hook shows: event, matcher, type, source file, and command. This confirms the hook is loaded. What it does *not* validate: whether the script logic is correct, whether the exit code is right, or whether the matcher fires at the right time.

If the hook doesn't appear: check that the settings file has valid JSON (no trailing commas), that it's in the correct location (`.claude/settings.json` for project, `~/.claude/settings.json` for global), and restart the session if the file watcher missed the change.

**Layer 2: Script logic isolation (manual pipe test)**

Test the script independently before running inside Claude Code:

```bash
echo '{"tool_name":"Bash","tool_input":{"command":"rm -rf ~/"},"hook_event_name":"PreToolUse"}' \
  | .claude/hooks/safety-check.sh
echo "exit: $?"
```

This validates: script executability, stdin consumption, jq path correctness, exit code behavior, stderr output. Do this for every new hook before trusting it in a session. Most silent failures — wrong exit code, bad jq path, missing dependency — are caught here.

**Layer 3: End-to-end execution trace (debug log)**

Start Claude Code with a debug log target, then tail it in a parallel terminal:

```bash
# Terminal 1
claude --debug-file /tmp/claude.log

# Terminal 2
tail -f /tmp/claude.log
```

The debug log shows: which hooks matched, exit codes, full stdout and full stderr for every hook that fired. The in-session transcript view (`Ctrl+O`) shows only a one-line summary — success is silent, blocking errors show stderr, non-blocking errors show `<hook name> hook error` + first stderr line. The debug log is the full record.

If Claude Code was started without `--debug-file`, run `/debug` mid-session to enable logging and find the log path.

## Validating jq Paths Against Real Payloads

jq returns `null` silently when a field path is absent — it does not error. A blocking condition that reads `jq -r '.tool_input.command'` on a Write event (where the field is `.tool_input.file_path`) gets null, the condition doesn't match, and the hook passes everything through.

To validate against a real payload, add a capture line during development:

```bash
INPUT=$(cat)
echo "$INPUT" > /tmp/last-hook-input.json  # remove before production
```

Then inspect `/tmp/last-hook-input.json` to confirm the actual field names before writing extraction logic. This is particularly important when adapting a hook from one tool type to another.

## Performance Testing

Synchronous hooks block Claude while they run. Target under 200ms per hook; PostToolUse hooks adding 500ms+ create noticeable session sluggishness that accumulates across a refactor session.

Measure during development:

```bash
time echo '{"tool_name":"Bash","tool_input":{"command":"ls"}}' | .claude/hooks/my-hook.sh
```

If a hook exceeds the threshold, narrow its matcher with the `if` field or convert non-critical work to `async: true`.

## Auditing Exit Codes in Python Validators

Python scripts that use `sys.exit(1)` on failure are non-blocking — Claude Code logs a warning and continues execution. Any unhandled exception also exits with code 1 by default, creating a silent pass-through even when the validator detects a problem.

Audit pattern:

```bash
grep -n "sys.exit" ~/.claude/validators/*.py
# Every result must be sys.exit(0) or sys.exit(2) — nothing else
```

Wrap all validator logic in `try/except` with explicit `sys.exit(2)` in the exception handler.

## Takeaway

Run all three layers for every new hook. Layer 1 catches configuration problems. Layer 2 catches script logic and dependency problems. Layer 3 catches integration problems that only appear when Claude Code invokes the hook in a live session. A hook that appears correct at each prior layer rarely fails at the next.
