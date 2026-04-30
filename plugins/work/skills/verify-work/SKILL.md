---
name: verify-work
description: >
  Verifies completed work against validation criteria. Works in two
  modes: with a plan (runs the plan's Validation section) or ad-hoc
  (builds checks from git diff, project config, and project docs).
  Use when the user wants to "validate the work", "verify the work",
  "check my work", "verify my changes", "does this look right",
  "run checks", "check if done", "are we done", "did it work",
  or after completing all tasks in a plan.
argument-hint: "[plan file path (optional)]"
user-invocable: true
references:
  - references/automated-validation.md
  - references/human-validation.md
  - references/adhoc-validation.md
  - references/failure-diagnosis.md
  - ../../_shared/references/plan-format.md
license: MIT
---

# Verify Work

Verify that completed work meets validation criteria — either from a plan's
Validation section or from a hypothesis built from git diff, project
conventions, and project docs.

**Announce at start:** "I'm using the verify-work skill to verify this work."

## Workflow

### 1. Determine Mode

**Plan mode:** A plan file path was provided, or the user references a
plan. Read the plan file. Locate the **Validation** section. If it
contains criteria, proceed to Step 2 (Plan Preconditions).

If the Validation section is missing or empty, stop and report: "This
plan has no validation criteria. Add concrete criteria to the Validation
section before running validation."

**Ad-hoc mode:** No plan provided or referenced. Proceed to Step 1b
(Build Hypothesis).

### 1b. Build Hypothesis (ad-hoc mode)

Gather signals from three sources. See
[adhoc-validation](references/adhoc-validation.md) for the full protocol.

**Git diff:** Run `git diff main...HEAD --stat`, `git diff --stat`, and
`git diff --cached --stat`. Categorize changed files (source, tests,
config, docs).

**Config files:** Scan for project config files to discover available
checks (test runners, linters, type checkers, build tools). Only propose
checks for tools actually configured.

**Project docs:** Read `CLAUDE.md`, `AGENTS.md`, `README.md`, and
`CONTRIBUTING.md` for explicit test/lint/build commands and conventions.

### 1c. Present and Confirm (ad-hoc mode)

Present the hypothesis:

```
Based on your changes and project setup, here's what I'd validate:

Changes detected:
- [N] source files modified ([list key files])
- [N] test files modified
- [N] doc files modified

Proposed checks:
1. [auto] `command` — description
2. [auto] `command` — description
3. [human] Description of qualitative check

Add, remove, or modify any of these? Or confirm to run.
```

Every proposed check must cite its signal source (git diff, config file,
or project doc). Wait for user confirmation before executing.

### 2. Plan Preconditions (plan mode only)

Check that all task checkboxes are complete:

```bash
bash <plugin-skills-dir>/start-work/scripts/check_tasks_complete.sh <path>
```

The script exits 0 with "OK: all tasks complete" if all boxes are checked.
It exits 1 and prints the open task lines if any remain. If tasks remain,
report them and stop:

> "[N] task(s) incomplete. Complete all tasks before validating."

Do not proceed with partial validation.

### 3. Classify Criteria

Tag each numbered item in the Validation section:

- **Automated** — item contains a runnable command in a code block
- **Human** — item describes an observable condition requiring judgment
- **Mixed** — item has both a runnable command and a judgment component

### 4. Run Automated Checks

Execute commands from automated and mixed criteria in priority order
(numbered list order). Capture exit code and output per criterion.

- Exit code 0 = **pass**
- Non-zero exit code = **fail** (but read output — see
  [automated-validation](references/automated-validation.md) for
  interpretation nuance)

For mixed criteria, run the automated part first. If it fails, mark the
criterion as failed without proceeding to the human component.

### 5. Present Human Criteria

Show the full numbered list with results:

```
Validation Results:
1. [PASS] `python python -m pytest tests/ -v` — 42 passed
2. [FAIL] `ruff check src/` — 3 errors found
3. [PENDING] All API responses use consistent error format
4. [PENDING] Documentation covers all new endpoints
```

Ask the user to confirm each pending (human) criterion. Default: present
the full list and ask for confirmation on all pending items at once. If
the user prefers one-by-one, switch to that mode.

See [human-validation](references/human-validation.md) for presentation
patterns, judgment vs. confirmation criteria, and escalation.

### 6. Handle Failures

If any criterion failed:

1. Report which criteria failed with evidence (command output, user
   rejection reason)
2. Load [failure-diagnosis](references/failure-diagnosis.md)
3. Classify the gap type: integration gap, specification drift, or
   missing cross-cutting concern

**Plan mode:**

4. Suggest 1-3 new tasks to close the gap, formatted to match the
   plan's existing task style
5. Keep plan in `executing` state
6. Ask user: add suggested tasks to plan, or abandon?

If the user adds tasks, insert them into the plan's **Tasks section**
(before the Validation heading, not after it). This is critical —
`assess_plan.py` only parses tasks under task-related headings. Tasks
appended after the Validation heading will be invisible to the execution
tooling. Update the plan file and save. The plan returns to active
execution.

**Ad-hoc mode:**

4. Present specific, actionable suggestions to fix each failure
5. Offer to re-run validation after fixes are applied

No plan file to update — suggestions are conversational.

### 7. On Success

When all criteria pass (automated + human confirmed) and none are
marked uncertain:

**Plan mode:**

1. Update plan frontmatter: `status: completed`
2. Output structured summary:

```
Validation Complete — ALL PASSED

Plan: [plan name]
Criteria: [N] total ([A] automated, [H] human, [M] mixed)

Results:
1. [PASS] criterion description
2. [PASS] criterion description (human-confirmed)
...

Status updated: executing → completed
```

**Ad-hoc mode:**

1. Output results summary:

```
Validation Complete — ALL PASSED

Criteria: [N] total ([A] automated, [H] human)

Results:
1. [PASS] criterion description
2. [PASS] criterion description (human-confirmed)
...
```

## Key Instructions

- **All tasks must be complete before validating (plan mode).** The
  precondition check (Step 2) enforces this. Partial validation produces
  misleading results.
- **Run automated checks before human checks.** Automated results
  inform human judgment. If tests fail, asking the user to judge code
  quality is premature.
- **Read command output, not just exit codes.** A passing exit code
  with warning output may still indicate problems. A failing exit code
  from a missing environment is "blocked," not "failed."
- **Plan stays in `executing` on failure (plan mode).** Never mark a
  plan as failed or completed when validation criteria fail. Add tasks
  to address gaps or abandon with a reason.
- **Run the criteria as given, not your own.** In plan mode, run what
  the plan author wrote. In ad-hoc mode, run what the user confirmed.
  Do not invent additional criteria or skip criteria you consider
  redundant.

## Anti-Pattern Guards

1. **Validating with unchecked tasks** — partial validation is unreliable.
   The precondition check prevents this, but if you notice unchecked tasks
   after loading the plan, stop and report them.
2. **Marking completed on failure** — failed validation means the plan
   needs more work. Add tasks or abandon; never mark completed.
3. **Inventing criteria** — the Validation section is the contract. Adding
   criteria the plan author didn't write changes the success bar without
   consent.
4. **Skipping human criteria** — automated-only validation misses
   qualitative concerns. Present human criteria even when all automated
   checks pass.
5. **Diagnosing without evidence** — when reporting failures, include
   command output, error messages, or specific observations. "It didn't
   work" is not a diagnosis.
6. **Running quality judgment before structural checks pass** — if plan structure is malformed (missing status, wrong task count), quality checks produce meaningless results. Structural preconditions (Step 2) must pass before any judgment-based criterion runs. A malformed plan is not "mostly validated."

## Handoff

**Receives:** Plan file path (optional); validates current working state against plan criteria
**Produces:** Validation report with pass/fail verdict per criterion
**Chainable to:** finish-work (on pass), start-work (on fail)
