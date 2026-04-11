---
name: check-hook
description: >
  Audits Claude Code hooks configuration for event coverage, script safety,
  async and blocking contradictions, Stop hook loop risks, rule overlap,
  and idempotency. Use when the user wants to "audit hooks", "check hooks",
  "review hooks", "check my hooks", "what quality gates are missing", or
  "are my hooks safe".
argument-hint: "[settings.json path]"
user-invocable: true
---

# Check Hook

Inspect a project's Claude Code hooks configuration for coverage gaps,
misconfigurations, unsafe patterns, and redundancy. Read-only — reports
findings but does not modify any files.

## Input

Read hooks from both of these locations (use whichever exist):
- `.claude/settings.json`
- `.claude/settings.local.json`

If a file path argument was provided, read that file instead.

If neither location exists, or neither contains a `hooks:` key, report
this as the first finding before running any checks:

> **No hooks configured** (warn) — No hooks found in `.claude/settings.json`
> or `.claude/settings.local.json`. PreToolUse hooks provide deterministic
> enforcement that CLAUDE.md instructions cannot guarantee.

Then continue to the Event coverage check, which will also fire.

## Checks

Run six checks. For each configured hook, apply all relevant checks.

### 1. Event coverage

Is a `PreToolUse` hook present?

`PreToolUse` is the only event that can block tool execution (via exit
code 2). `PostToolUse` fires after execution and cannot prevent it — a
`PostToolUse` hook intended to block is a misconfiguration that silently
fails to enforce.

Flag as `warn` if no `PreToolUse` hook is present, with a note that
quality-gate enforcement requires PreToolUse.

### 2. Script safety

For each hook using `"type": "command"`, read the command string. Flag
as `fail` if it contains:
- `rm -rf`
- `git reset --hard`
- `git checkout .`
- `git push --force` or `git push -f`

These operations are irreversible and should never run automatically
without explicit user intent.

### 3. Async + blocking contradiction

For each hook, check whether `"async": true` is set alongside a script
that contains `exit 2` logic, or is described as a gate or blocker.

Async hooks run in the background after execution proceeds — they can
never block regardless of exit code. A hook that needs to block must be
synchronous (the default; `async` omitted or `false`).

Flag as `fail` if `async: true` is paired with blocking intent.

### 4. Stop hook loop risk

For any `Stop` or `SubagentStop` hook: check whether the hook script
reads the `stop_hook_active` field from its stdin JSON and exits 0 when
it is `True`.

A Stop hook that returns exit code 2 without this guard forces Claude to
keep responding indefinitely — it cannot stop. This is an infinite loop.

Flag as `fail` if a Stop/SubagentStop hook appears to exit 2 under any
condition but does not contain a `stop_hook_active` guard.

### 5. Rule overlap

Read `CLAUDE.md` (if it exists) and check whether any hook duplicates an
instruction already expressed there.

Overlap is not always wrong — a hook that enforces a CLAUDE.md rule
deterministically is intentional belt-and-suspenders. But one of the two
may be stale, or the hook may have been added without knowing the rule
already exists.

Flag as `warn` for each overlap found, noting which CLAUDE.md instruction
the hook may duplicate.

### 6. Idempotency

For each hook script, check for patterns that accumulate state across
invocations:
- Unbounded appending to a log file without rotation
- Incrementing a counter without a reset mechanism
- Creating files that are never cleaned up

Running a hook twice should produce the same result. State accumulation
is a sign the hook will degrade over time.

Flag as `warn` per pattern found.

## Report

Present findings as a table with a summary count at the top:

```
N issues across M hooks (X fail, Y warn)

event          | hook command          | check             | finding
---------------+-----------------------+-------------------+---------------------------
PostToolUse    | .claude/hooks/gate.sh | Event coverage    | PostToolUse cannot block; use PreToolUse for enforcement
Stop           | .claude/hooks/stop.sh | Stop hook loop    | No stop_hook_active guard — infinite loop risk
PostToolUse    | lint-after-write.sh   | Async + blocking  | async:true with exit 2 — hook will never block
```

If no issues are found, confirm:
> "Hooks look well-configured."

## Handoff

**Receives:** Settings file path (optional); reads `.claude/settings.json` and `.claude/settings.local.json` by default
**Produces:** Findings table per hook; read-only — no files modified
**Chainable to:** build-hook (to create or fix a hook based on findings)
