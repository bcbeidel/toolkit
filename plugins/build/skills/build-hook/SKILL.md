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
  - ../../_shared/references/hook-best-practices.md
  - ../../_shared/references/primitive-routing.md
  - references/hook-testing.md
---

# Build Hook

Scaffold a Claude Code hook — an event-driven handler that enforces a quality
gate deterministically, bypassing LLM judgment. See
[hook-best-practices.md](../../_shared/references/hook-best-practices.md) for the
rubric both halves of the pair share.

**Workflow sequence:** 1. Route → 2. Scope Gate → 3. Elicit → 4. Draft →
5. Safety Check → 6. Stop Hook Guard (conditional) → 7. Rule Overlap →
8. Review Gate → 9. Save → 10. Test

## 1. Route

Confirm a hook is the right primitive. Full framework:
[primitive-routing.md](../../_shared/references/primitive-routing.md).

- **Unconditional permanent block** (never allow tool X, no exceptions ever) → route to `settings.json` `permissions.deny`.
- **Advisory guidance or preference** (prefer X, follow this convention) → route to CLAUDE.md or `/build:build-skill`.
- **Semantic judgment on file content** (convention too nuanced for grep) → route to `/build:build-rule`.
- **Specific lifecycle trigger + must fire regardless of LLM judgment** → proceed.

## 2. Scope Gate

Refuse — and recommend an alternative — when any of these signal:

1. **The goal is a preference, not an invariant.** Hooks spend their authority on false positives. If the user is unsure whether they'd want a bypass path, the goal is advisory — route to CLAUDE.md or a skill.
2. **The check needs semantic judgment.** If the criterion cannot be expressed as a shell one-liner or a lean script (format, naming pattern, file existence, command shape), route to `/build:build-rule`.
3. **No lifecycle event maps to the goal.** If the trigger is "after the user thinks about X," there is no hook to write.

## 3. Elicit

If `$ARGUMENTS` is non-empty, parse as `[hook-event] [enforcement-goal]` —
pre-fill the first two fields, confirm with the user, then ask only the
handler-type question. Otherwise ask one at a time:

1. **Hook event** — which lifecycle moment? See the event table in
   [hook-best-practices.md §Anatomy §Event selection](../../_shared/references/hook-best-practices.md).
   If the goal is to block, the event must be PreToolUse or another blockable event.
2. **Handler type** — `command` (default), `http`, `prompt`, or `agent`. Default
   to `command` unless the enforcement genuinely needs an LLM.
3. **Enforcement goal** — one sentence. Confirm before drafting.

## 4. Draft

Produce two artifacts, referencing the Anatomy section of the principles
doc for every shape decision (skeleton, matcher syntax, JSON output contract,
settings.json entry, path-expansion variables).

**Artifact 1 — Hook script.** Start from the skeleton in
[hook-best-practices.md §Anatomy §Script skeleton](../../_shared/references/hook-best-practices.md).
Fill in the enforcement logic.

**Artifact 2 — settings.json entry.** Start from the entry shape in
[hook-best-practices.md §Anatomy §Settings.json entry shape](../../_shared/references/hook-best-practices.md).
Pick a `timeout` appropriate for the gate (10–60 s typical).

Present both artifacts to the user before the Safety Check.

## 5. Safety Check

Review the draft against the audit rubric in
[audit-dimensions.md](../check-hook/references/audit-dimensions.md) —
the same dimensions `/build:check-hook` uses. Revise until each applicable
dimension passes. High-leverage checks for a fresh scaffold:

- `exit-code-contract` — blocking intent uses `exit 2`, not `exit 1` or an unthrown exception.
- `async-blocking-coherence` — `async: true` and `exit 2` are mutually exclusive.
- `stdin-consumption` — `INPUT=$(cat)` is present; the script is executable.
- `command-path-expansion` — `$CLAUDE_PROJECT_DIR` or absolute path; never `$HOME` / `~`.
- `injection-safety` — no `eval` on payload values; all expansions quoted; `jq --arg` for variable injection.
- `jq-handling` — availability check present; field paths match the matcher's tool.
- `shell-hygiene` — `set -Eeuo pipefail`; errors to stderr; `[[` over `[`; `#!/usr/bin/env bash`.
- `destructive-operations` — no `rm -rf`, `git reset --hard`, `git push --force`, `git checkout .`.

## 6. Stop Hook Guard

**Only for `Stop` and `SubagentStop` events.** Skip otherwise.

A Stop hook that exits 2 without a re-entry guard creates an infinite loop.
Apply the belt-and-suspenders pattern from
[hook-best-practices.md §Patterns That Work](../../_shared/references/hook-best-practices.md):

- **SubagentStop:** inspect `stop_hook_active` and `last_assistant_message`.
- **Stop:** use a session-scoped guard file keyed to `session_id` (the `Stop` payload lacks `stop_hook_active`).

## 7. Rule Overlap

Scan `CLAUDE.md` for instructions that express the same enforcement goal.
If found, note the overlap and ask:

> "CLAUDE.md already says [X]. A hook enforces this deterministically
> (CLAUDE.md is advisory). Do you want both (belt-and-suspenders), only
> the hook (deterministic), or is CLAUDE.md sufficient?"

The user decides — overlap is often intentional.

## 8. Review Gate

Present both artifacts — script and settings.json entry — and wait for
explicit user approval before writing. If the user requests changes, revise
and re-present. Proceed only on explicit approval.

## 9. Save

Write the approved script to `.claude/hooks/<name>.sh` (or a path the user
specifies). Make it executable: `chmod +x .claude/hooks/<name>.sh`.

Show the settings.json patch for the user to apply manually. Do not
auto-patch `settings.json` — it may contain permission entries and other
hook arrays that should not be overwritten.

## 10. Test

Follow the three-layer verification in
[hook-testing.md](references/hook-testing.md) — configuration, logic
isolation, execution trace — before activating the hook.

Then offer:

> "Run `/build:check-hook` to audit the configuration for coverage gaps,
> misconfigurations, and safety issues?"

## Anti-Pattern Guards

1. **Skipping Route/Scope Gate.** A goal that fits `permissions.deny` or CLAUDE.md should never reach the Draft step.
2. **Blocking via PostToolUse.** PostToolUse cannot prevent execution; presenting a PostToolUse draft for a blocking goal is a misconfiguration that silently fails to enforce.
3. **`async: true` with `exit 2`.** Async hooks run after execution regardless of exit code.
4. **Writing files before the Review Gate.** Skipping the gate bypasses the only safety checkpoint.
5. **Auto-patching `settings.json`.** Always show the snippet; let the user apply.

## Key Instructions

- Do not write any file to disk before the Review Gate passes.
- Do not auto-patch `settings.json`; always show the snippet for manual application.
- Won't build a hook when `permissions.deny` covers the goal — unconditional blocks need no script.
- Won't build a hook for advisory guidance — suggest CLAUDE.md or a skill instead.
- Won't skip the Safety Check against `audit-dimensions.md`.
- Recovery if a hook is written in error: `chmod -x .claude/hooks/<name>.sh` (disables without deleting) or remove the file and its `settings.json` entry. A configured hook whose script is missing or non-executable silently fails and leaves normal tool flow intact.

## Handoff

**Receives:** Hook event, handler type, enforcement goal.
**Produces:** Hook script at `.claude/hooks/<name>.sh` + settings.json entry snippet.
**Chainable to:** `/build:check-hook` (audit the hook against `audit-dimensions.md`).
