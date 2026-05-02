---
name: check-help-skill
description: >-
  Use when the user wants to "audit a help skill", "check the
  /<plugin>:help command", "review my plugin index", "verify my
  help-skill is up to date", or "is the skill table in this help-skill
  current". Audits a plugins/<plugin>/skills/help/SKILL.md against the
  help-skill rubric — coverage, freshness, frontmatter fidelity, plus
  five judgment dimensions.
argument-hint: "[path to help-skill SKILL.md, or plugin name]"
user-invocable: true
version: 1.0.0
owner: build-plugin
license: MIT
references:
  - ../../_shared/references/help-skill-best-practices.md
  - ../../_shared/references/skill-best-practices.md
  - references/audit-dimensions.md
  - references/repair-playbook.md
  - scripts/check_help_skill.py
---

# /build:check-help-skill

Audit a help-skill — the SKILL.md at
`plugins/<plugin>/skills/help/SKILL.md` — against the rubric. The
audit runs in three tiers: deterministic checks (skill-index
coverage, freshness, frontmatter fidelity, line count, slug, secret
patterns); judgment checks (workflow curation, triage scaffolding,
dual audience, scope discipline, trigger quality); and a cross-
entity check (trigger collision against sibling skills).

The full check inventory lives in
[audit-dimensions.md](references/audit-dimensions.md). Repair
recipes live in [repair-playbook.md](references/repair-playbook.md).
The principles audited come from
[help-skill-best-practices.md](../../_shared/references/help-skill-best-practices.md).

## When to use

- The user says "audit / check / review / lint a help-skill"
- The user passes a path to a help-skill SKILL.md or names a plugin
  whose help-skill should be audited
- After `/build:build-help-skill` writes a new help-skill (the build
  step chains to this skill automatically)
- A sibling skill in the plugin was added, removed, or renamed —
  drift check
- A plugin version bump — confirm the help-skill still reflects the
  plugin's shape

## Prerequisites

- Working directory contains a checkout with the target plugin
- Read access to `plugins/<plugin>/skills/help/SKILL.md` and to
  every sibling `plugins/<plugin>/skills/*/SKILL.md`
- `$ARGUMENTS` either names the help-skill path or names the plugin
  (resolves to `plugins/<plugin>/skills/help/SKILL.md`)

## Steps

1. **Resolve the target.** Read `$ARGUMENTS`. If it ends in
   `SKILL.md`, treat as the path. If it names a plugin (e.g.,
   `work`), resolve to `plugins/<plugin>/skills/help/SKILL.md`. If
   the file does not exist, stop — there is nothing to audit. If
   the path resolves to a SKILL.md whose `name` is not `help`, stop
   and route to `/build:check-skill` — this auditor is for help-
   skills only.

2. **Run Tier-1 deterministic checks.** Invoke
   `scripts/check_help_skill.py <plugin-or-path>` and capture
   stdout. The script enforces the audit-dimensions.md Tier-1
   inventory — slug fidelity, frontmatter shape, line count,
   secret/TLS/pipe-to-shell patterns, synopsis presence,
   managed-region presence, skill-index coverage and
   no-self-listing, description fidelity, workflow section
   presence and freshness, pointer resolution — and emits findings
   in lint format with severities (FAIL / WARN / INFO). The LLM
   reasons over the script's output, not the raw SKILL.md. Exit 0
   indicates clean / WARN-only / INFO-only; exit 1 indicates at
   least one FAIL.

3. **FAIL gate.** Any FAIL finding excludes the file from Tier-2
   judgment — fix the structural issue before evaluating quality.
   The exclusion list: `slug-mismatch`, `secret`, `managed-region-
   missing`, `skill-index-coverage` (rows for skills that don't
   exist on disk), `pointer-broken-fail` (broken pointer to
   AGENTS.md / RESOLVER.md / plugin README, which are load-bearing
   navigation). Other FAILs may be present at this point but are
   surfaced and continue.

4. **Run Tier-2 judgment checks.** One LLM evaluation per file
   covering all five dimensions: workflow curation (at least one
   composed chain, not just a flat list); triage scaffolding (task
   → skill mapping is actionable, not just a description echo);
   dual audience (readable for both human typing `/<plugin>:help`
   and agent looking up routing); scope discipline (does not
   duplicate AGENTS.md or README content); trigger quality
   (description fires on meta-questions about the plugin, not on
   the plugin's own workflows). Each dimension returns
   PASS / WARN / FAIL with one-sentence rationale, citing the
   source principle.

5. **Run Tier-3 cross-entity check.** For each sibling skill in the
   plugin, compare its `description` against the help-skill's
   `description` for trigger collision. Heuristic: shared
   trigger-phrase tokens above a threshold flag as INFO; an
   identical "Use when the user/caller asks…" phrasing across two
   skills flags as WARN. The router cannot disambiguate two skills
   that match the same trigger — surface every collision so the
   user can narrow either side.

6. **Report.** Emit findings in the lint-style format used across
   the toolkit's check-* skills: severity, ID, location (line:col
   when applicable), one-line message, source principle. Group by
   tier. End with a summary count and the `/build:check-help-skill
   --repair` invitation.

7. **Opt-in repair loop.** If the user opts in (`y` / specific
   finding IDs), apply canonical repairs from
   [repair-playbook.md](references/repair-playbook.md) one finding
   at a time, with explicit confirmation per fix. Re-run Tier-1
   after each fix to verify it landed cleanly. Tier-2 dimensions
   are coaching — surface them but do not auto-repair without
   explicit per-finding approval.

## Failure modes

- **Target file missing.** Step 1 stops the workflow. Recovery:
  scaffold via `/build:build-help-skill <plugin>` first, or correct
  the path argument.
- **Target is not a help-skill.** Step 1 routes to
  `/build:check-skill`. Recovery: re-invoke the appropriate
  auditor.
- **Sibling skills unreadable.** If `plugins/<plugin>/skills/*/
  SKILL.md` cannot be parsed (malformed frontmatter), Tier-1
  coverage and fidelity checks emit `tool-degraded` INFO findings
  and continue. Recovery: fix the malformed sibling first; the
  help-skill audit is downstream.
- **Tier-2 LLM call fails.** Surface the failure as an INFO
  finding; Tier-1 results stand. Recovery: re-run the audit; do not
  block on transient model failures.
- **Repair playbook lacks a recipe for a finding.** A
  finding-without-recipe is a gap in the playbook itself, not a
  failure of the auditor. Surface to the user; the recipe should be
  added to `repair-playbook.md` in a follow-up.

## Examples

<example>
Invocation:

```bash
/build:check-help-skill work
```

Step 1 — Resolves to `plugins/work/skills/help/SKILL.md`. File
exists. `name: help`. Proceed.

Step 2 — Tier-1: 0 FAIL, 1 WARN, 0 INFO.
- WARN `description-fidelity` — table row for `plan-work` reads
  *"Plan a multi-step task"* but the current
  `plugins/work/skills/plan-work/SKILL.md` description starts *"Use
  when the user has a spec or requirements for a multi-step
  task…"*. Source: *Description fidelity — entries reflect actual
  frontmatter*.

Step 3 — No FAIL exclusion; proceed to Tier-2.

Step 4 — Tier-2: 5 PASS.

Step 5 — Tier-3: no trigger collisions.

Step 6 — Reports 1 WARN. Invites repair.

Step 7 — User accepts the repair. Playbook recipe regenerates the
managed region from sibling frontmatter; re-runs Tier-1; finding
clears. Reports clean.
</example>

## Key Instructions

- Run Tier-1 before Tier-2; FAIL findings exclude the file from
  judgment evaluation. Audit cleanly is the contract.
- Cite the source principle for every finding — every dimension in
  `audit-dimensions.md` names the
  `help-skill-best-practices.md` section it enforces.
- Tier-3 trigger-collision check is what makes this auditor
  load-bearing — a help-skill in isolation looks fine; a help-skill
  that fights its siblings only fails when the router has to choose.
- Repair is opt-in and per-finding; never apply playbook recipes
  without explicit user confirmation.

## Anti-Pattern Guards

1. **Skipping the trigger-collision check.** A help-skill that
   parses cleanly but collides with siblings will misroute callers
   silently. Tier-3 is the load-bearing dimension; running only
   Tier-1 + Tier-2 leaves the highest-value defect undetected.
2. **Auto-repairing Tier-2 findings.** Judgment dimensions (workflow
   curation, dual audience, scope discipline) need user input.
   Auto-applying playbook recipes without confirmation produces
   plausible but wrong rewrites.
3. **Treating description-fidelity as deterministic-equivalent.**
   The check compares the table's trigger column to the sibling's
   current description; minor wording differences are expected
   (truncation to ~12 words). The check fires on *substantive*
   drift (a sibling description changed and the table did not).
   Reporting trivial wording deltas as FAIL produces noise.
4. **Inlining a chained skill instead of invoking it.** MUST invoke
   `/build:check-skill` via the Skill tool when Step 1 routes off-
   target. MUST NOT inline a partial check-skill audit. The
   shortcut bypasses the chained skill's rubric.

## Handoff

**Receives:** Path to a help-skill SKILL.md or a plugin name.

**Produces:** A finding report (FAIL / WARN / INFO with source
principle citations) and an opt-in repair loop. Does not write to
disk unless the user opts in to repair.

**Chainable to:** `/build:check-skill <path>` (catches generic
SKILL.md structural issues outside the help-skill rubric);
`/build:check-skill-pair help-skill` (audits pair-level integrity —
principles doc present, audit/playbook coverage, routing
registration); `/build:build-help-skill <plugin>` (when the target
file does not exist).
