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
  - ../../_shared/references/brief-best-practices.md
  - references/audit-dimensions.md
  - references/repair-playbook.md
  - references/platform-limitations.md
license: MIT
---

# Check Hook

Audit a project's Claude Code hooks configuration against the rubric in
[hook-best-practices.md](../../_shared/references/hook-best-practices.md).
Read-only until the opt-in Repair Loop.

**Workflow sequence:** 1. Scope → 2. Primitive Routing Scan →
3. Judgment Checks → 3b. Brief-Quality Pass → 4. Platform Scope →
5. Report → 6. Opt-In Repair Loop

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

## 3b. Brief-Quality Pass

For each hook script audited, look for `.briefs/<hook-name>.brief.md`
at the repo root (the slug is the hook script's basename without
`.sh`). Apply the `brief-presence-and-content` dimension from
[audit-dimensions.md](references/audit-dimensions.md):

- **Presence.** File exists with the five required H2 sections
  (*User ask*, *So-what*, *Scope boundaries*, *Planned artifacts*,
  *Planned handoffs*).
- **Content quality.** *So-what* names a specific scenario the hook
  prevents — a real near-miss, a class of mistakes the team kept
  making — rather than reading as a category description.
- **Scope concreteness.** *In* / *Out* lists carry concrete items,
  not vague hedges.

Each shortfall is a `warn` finding under the
`brief-presence-and-content` dimension. Append to the findings set.
Hooks built before the brief pattern existed will trip this; the
repair playbook recommends a retroactive brief.

## 4. Platform Scope

These checks target Claude Code (`settings.json` / `settings.local.json`).
If the project's hooks may run on additional platforms beyond Claude Code,
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

## Example

Invocation: `/build:check-hook` (no argument; defaults to
`.claude/settings.json` and `.claude/settings.local.json`).

Scope finds `settings.json` with three hooks: a `PreToolUse` on `Bash`,
a `PostToolUse` on `Write` described as a "lint gate," and a blocking
`Stop` hook.

Primitive Routing Scan reads `CLAUDE.md` and finds one advisory rule —
"never commit files containing `TODO(ME)` markers" — that is shell-
expressible and has a lifecycle trigger. Flags as `warn`, recommends
converting to a `PreToolUse` hook.

Judgment Checks evaluate each hook against
[audit-dimensions.md](references/audit-dimensions.md):

- `PostToolUse` lint gate → `event-matcher-fit` fail: PostToolUse cannot
  block; move to PreToolUse.
- `PostToolUse` lint gate → `async-blocking-coherence` fail:
  `"async": true` with `exit 2` paths — cannot block regardless.
- `Stop` hook → `stop-loop-guard` fail: blocking `exit 2` with no
  `session_id`-keyed guard file.

Platform Scope skipped — no evidence the hooks run outside Claude Code.

Report:

```
4 issues across 3 hooks (3 fail, 1 warn)

event          | hook command          | dimension                | finding
---------------+-----------------------+--------------------------+---------------------------
PostToolUse    | lint-after-write.sh   | event-matcher-fit        | PostToolUse cannot block
PostToolUse    | lint-after-write.sh   | async-blocking-coherence | async:true + exit 2
Stop           | enforce-test-pass.sh  | stop-loop-guard          | No re-entry guard
—              | CLAUDE.md             | primitive-routing        | TODO(ME) rule — convert to PreToolUse
```

Repair Loop: user enters `1,3`. Finding 1 routes to `/build:build-hook`
(substantive rewrite; event must change). Finding 3 is a direct edit
from the `stop-loop-guard` entry in
[repair-playbook.md](references/repair-playbook.md) — add the
session-scoped guard snippet. User confirms the diff; file updated.

## Anti-Pattern Guards

1. **Treating rule overlap as always wrong.** CLAUDE.md + hook duplication
   can be intentional belt-and-suspenders; flag for user decision, do not
   auto-remove.
2. **Skipping Primitive Routing Scan when no hooks exist.** Absence of hooks
   is itself a coverage gap worth surfacing.
3. **Reading settings outside the project.** Only `.claude/settings.json`
   and `.claude/settings.local.json` under the current project root, unless
   the user passes an explicit path.
4. **Bulk-applying fixes.** Per-finding confirmation required. Some findings
   (CLAUDE.md overlap, blocking-before-warn graduation) are intentional
   mid-deployment states.

## Key Instructions

- Read-only until the Repair Loop; no writes without per-finding confirmation.
- Always run Primitive Routing Scan before the judgment pass — even with zero hooks configured.
- `stop-loop-guard` findings are `fail`, not `warn` — unguarded blocking Stop
  hooks require a session kill to recover.
- Recovery: outside the Repair Loop this skill modifies nothing; any edits
  it produces can be reverted with `git diff` / `git checkout`.

## Handoff

**Receives:** Settings file path (optional); defaults to `.claude/settings.json` and `.claude/settings.local.json`.
**Produces:** Findings table per hook; optional targeted edits gated by
per-finding user confirmation in the Repair Loop.
**Chainable to:** `/build:build-hook` (create a new hook or substantially
rewrite one flagged by the audit); `/build:check-skill-pair hook` (audit
pair-level integrity).
