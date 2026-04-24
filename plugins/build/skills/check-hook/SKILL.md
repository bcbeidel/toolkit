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
references:
  - ../../_shared/references/hook-best-practices.md
  - references/audit-dimensions.md
  - references/repair-playbook.md
  - references/platform-limitations.md
---

# Check Hook

Audit a project's Claude Code hooks configuration against the rubric in
[hook-best-practices.md](../../_shared/references/hook-best-practices.md).
Read-only until the opt-in Repair Loop.

**Workflow sequence:** 1. Scope → 2. Primitive Routing Scan → 3. Judgment Checks → 4. Platform Scope → 5. Report → 6. Opt-In Repair Loop

## 1. Scope

If `$ARGUMENTS` is non-empty, read the settings file at that path. Otherwise,
read from both default locations (use whichever exist):

- `.claude/settings.json`
- `.claude/settings.local.json`

If neither exists, or neither has a `hooks:` key, the first finding is:

> **No hooks configured** (warn) — PreToolUse hooks provide deterministic
> enforcement CLAUDE.md instructions cannot guarantee.

Continue to the Primitive Routing scan, which will also fire.

## 2. Primitive Routing Scan

Before judgment checks, scan `CLAUDE.md` (if present) for rules that match
any of three conversion signals — advisory instructions that belong in a hook:

1. The rule is one Claude keeps violating under normal conditions.
2. The rule can be expressed as a shell one-liner (format, test gate, naming pattern).
3. The rule requires enforcement at a specific lifecycle moment.

For each matching rule, flag as `warn`, quote the rule, note the signal,
and recommend converting to a PreToolUse hook.

## 3. Judgment Checks

Evaluate each configured hook against every dimension in
[audit-dimensions.md](references/audit-dimensions.md). Each dimension
entry carries pass/fail criteria, severity, and the principles-doc section
it enforces. Do not repeat the dimension bodies here — the rubric is
authoritative.

For each finding, capture: dimension name, offending hook / command / file,
specific issue, severity (`fail` / `warn`).

## 4. Platform Scope

These checks target Claude Code (`settings.json` / `settings.local.json`).
If the project's hooks may run on additional platforms (Copilot, etc.),
read [platform-limitations.md](references/platform-limitations.md) and
append platform-specific findings as a separate report section.

## 5. Report

Present findings as a summary count plus a table, severity-sorted
(`fail` → `warn` → `info`):

```
N issues across M hooks (X fail, Y warn)

event          | hook command          | dimension                 | finding
---------------+-----------------------+---------------------------+---------------------------
PostToolUse    | .claude/hooks/gate.sh | event-matcher-fit         | PostToolUse cannot block; use PreToolUse
Stop           | .claude/hooks/stop.sh | stop-loop-guard           | No re-entry guard — infinite loop risk
PostToolUse    | lint-after-write.sh   | async-blocking-coherence  | async:true + exit 2 — never blocks
```

If Platform Scope added findings, append:

```
**Cross-platform limitations:** [list per platform]
```

If no issues: "Hooks look well-configured."

## 6. Opt-In Repair Loop

Ask exactly once:

> "Apply fixes? Enter `y` (all), `n` (skip), or comma-separated numbers."

For each selected finding, route per
[repair-playbook.md](references/repair-playbook.md) — each dimension has a
recipe: direct edit (add `INPUT=$(cat)`, fix matcher casing, swap `$HOME`
for `$CLAUDE_PROJECT_DIR`), or routed to `/build:build-hook` for substantive
rewrites, or requires user judgment (CLAUDE.md overlap).

Show the diff before writing. Terminate when the user selects no further
findings, enters `n`, or confirms `done`.

## Anti-Pattern Guards

1. **Treating rule overlap as always wrong.** CLAUDE.md + hook duplication can be intentional belt-and-suspenders; flag for user decision, do not auto-remove.
2. **Skipping Primitive Routing Scan when no hooks exist.** Absence of hooks is itself a coverage gap worth surfacing.
3. **Reading settings outside the project.** Only `.claude/settings.json` and `.claude/settings.local.json` under the current project root, unless the user passes an explicit path.
4. **Bulk-applying fixes.** Per-finding confirmation required. Some findings (CLAUDE.md overlap, blocking-before-warn graduation) are intentional mid-deployment states.

## Key Instructions

- Read-only until the Repair Loop; no writes without per-finding confirmation.
- Always run Primitive Routing Scan before the judgment pass — even with zero hooks configured.
- `stop-loop-guard` findings are `fail`, not `warn` — unguarded blocking Stop hooks require a session kill to recover.
- Recovery: outside the Repair Loop this skill modifies nothing; any edits it produces can be reverted with `git diff` / `git checkout`.

## Handoff

**Receives:** Settings file path (optional); defaults to `.claude/settings.json` and `.claude/settings.local.json`.
**Produces:** Findings table per hook; optional targeted edits gated by per-finding user confirmation in the Repair Loop.
**Chainable to:** `/build:build-hook` (create a new hook or substantially rewrite one flagged by the audit); `/build:check-skill-pair hook` (audit pair-level integrity).
