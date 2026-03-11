---
name: validate-plan
description: >
  Verifies a plan succeeded end-to-end by running validation criteria.
  Use when the user wants to "validate the plan", "verify the plan",
  "check if done", "run validation", "are we done", "did the plan work",
  or after completing all tasks in a plan. Handles both automated
  (command) and human (judgment) validation criteria.
argument-hint: "[plan file path]"
user-invocable: true
references:
  - references/automated-validation.md
  - references/human-validation.md
  - references/failure-diagnosis.md
  - ../_shared/references/preflight.md
  - ../_shared/references/plan-format.md
---

# Validate Plan

Verify that a plan succeeded end-to-end — not just that every task was
checked off, but that the combined result meets the plan's validation
criteria.

**Announce at start:** "I'm using the validate-plan skill to verify this plan."

## Workflow

### 1. Load Plan

Read the plan file. If no path was provided, ask the user which plan to
validate.

Locate the **Validation** section. It contains a numbered list of criteria,
prioritized, with embedded code blocks for runnable commands. If the
Validation section is missing or empty, stop and report: "This plan has
no validation criteria. Add concrete criteria to the Validation section
before running validation."

### 2. Check Preconditions

Run the preflight check (per `preflight.md`), then the entry script:

```bash
uv run <plugin-scripts-dir>/check_runtime.py
uv run <plugin-skills-dir>/execute-plan/scripts/plan_assess.py --file <path>
```

Parse the JSON output. All task checkboxes must be checked
(`tasks.completed == tasks.total`). If unchecked tasks remain, report
them and stop:

> "[N] of [total] tasks incomplete. Complete all tasks before validating.
> Remaining: [list unchecked tasks]"

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
1. [PASS] `uv run python -m pytest tests/ -v` — 42 passed
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

### 7. On Success

When all criteria pass (automated + human confirmed) and none are
marked uncertain:

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

## Key Instructions

- **All tasks must be complete before validating.** The precondition
  check (Step 2) enforces this. Partial validation produces misleading
  results.
- **Run automated checks before human checks.** Automated results
  inform human judgment. If tests fail, asking the user to judge code
  quality is premature.
- **Read command output, not just exit codes.** A passing exit code
  with warning output may still indicate problems. A failing exit code
  from a missing environment is "blocked," not "failed."
- **Plan stays in `executing` on failure.** Never mark a plan as failed
  or completed when validation criteria fail. Add tasks to address gaps
  or abandon with a reason.
- **Validation criteria come from the plan, not from you.** Run the
  criteria the plan author wrote. Do not invent additional criteria or
  skip criteria you consider redundant.

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
