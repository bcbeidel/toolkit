---
name: Validate Plan Skill Implementation
description: Create wos:validate-plan skill with SKILL.md and three reference files — issue #161
type: plan
status: executing
related:
  - docs/plans/2026-03-11-validate-plan-skill-design.md
  - skills/_shared/references/plan-format.md
branch: feat/161-validate-plan-skill
pull-request: https://github.com/bcbeidel/wos/pull/169
---

# Validate Plan Skill Implementation

## Goal

Ship the `wos:validate-plan` skill (#161) — a WOS-native skill that verifies
plans succeeded end-to-end by running automated and human validation criteria,
diagnosing task-pass/plan-fail gaps, and managing the executing→completed
lifecycle transition. Update execute-plan to recommend (not auto-invoke)
validate-plan with a user confirmation gate.

## Scope

Must have:
- `skills/validate-plan/SKILL.md` under 500 lines
- `skills/validate-plan/references/automated-validation.md`
- `skills/validate-plan/references/human-validation.md`
- `skills/validate-plan/references/failure-diagnosis.md`
- Skill triggers on "validate", "verify the plan", "check if done", "are we done"
- Precondition check via existing `assess_plan.py`
- Automated/human/mixed validation classification and execution
- Task-pass/plan-fail diagnosis with three gap types
- Structured output on success and failure
- Execute-plan SKILL.md Step 5 updated to confirmation gate pattern

Won't have:
- New Python code or scripts
- Plan-specific audit validators in `wos/validators.py`
- Code-enforced validation section format
- Automatic invocation from execute-plan

## Approach

Pure documentation skill following the brainstorm/write-plan pattern. SKILL.md
defines the 7-step workflow with inline classification rules. Three reference
files cover standalone concepts (automated execution, human presentation,
failure diagnosis), each serving distinct workflow steps. Uses existing
`assess_plan.py` via preflight pattern for precondition checks. A small update
to execute-plan SKILL.md changes Step 5 from auto-invoke to a confirmation
gate.

## File Changes

- Create: `skills/validate-plan/SKILL.md`
- Create: `skills/validate-plan/references/automated-validation.md`
- Create: `skills/validate-plan/references/human-validation.md`
- Create: `skills/validate-plan/references/failure-diagnosis.md`
- Modify: `skills/execute-plan/SKILL.md` (Step 5, lines 95-102)

## Tasks

### Task 1: Create SKILL.md

**Files:**
- Create: `skills/validate-plan/SKILL.md`

- [x] **Step 1: Create skill directory structure**

```bash
mkdir -p skills/validate-plan/references
```

- [x] **Step 2: Write SKILL.md**

Write `skills/validate-plan/SKILL.md` with:

Frontmatter:
```yaml
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
```

Body sections (following design spec workflow):
- Title + announce line
- 7-step workflow (Load plan, Check preconditions, Classify criteria,
  Run automated checks, Present human criteria, Handle failures, On success)
- Key Instructions (5-6 rules)
- Anti-Pattern Guards (4-5 items)
- Output Format section showing structured summary format

Classification rules inline in Step 3:
- Automated: item contains a runnable command in a code block
- Human: item describes an observable condition requiring judgment
- Mixed: item has both

Target: 150-200 lines. Must stay under 500 non-blank lines.

- [x] **Step 3: Verify SKILL.md is under 500 lines**

```bash
wc -l skills/validate-plan/SKILL.md
```

Expected: under 500 lines.

- [x] **Step 4: Commit**

```bash
git add skills/validate-plan/SKILL.md
git commit -m "feat(plan): task 1 — create validate-plan SKILL.md (#161)"
```

### Task 2: Create automated-validation.md

**Files:**
- Create: `skills/validate-plan/references/automated-validation.md`

- [x] **Step 1: Write automated-validation.md**

Write `skills/validate-plan/references/automated-validation.md` covering:

- Command execution protocol (run code blocks in priority order, capture
  exit code + stdout + stderr)
- Structural vs. semantic checks (observable state vs. behavior)
- Output interpretation (non-zero exits aren't always failures — test
  runners, linters, build tools differ)
- Environment sensitivity (distinguish "blocked" from "failed" when
  commands fail due to missing setup)
- Idempotency (flag commands with side effects before running)
- Examples section with 3-4 concrete examples by plan type:
  - Code implementation: `pytest tests/ -v`
  - Refactoring: `ruff check src/` + `pytest`
  - Migration: `python manage.py migrate --check`
  - Build: `npm run build` exit code + output check

Target: 70-80 lines.

- [x] **Step 2: Verify line count**

```bash
wc -l skills/validate-plan/references/automated-validation.md
```

Expected: 60-90 lines.

- [x] **Step 3: Commit**

```bash
git add skills/validate-plan/references/automated-validation.md
git commit -m "feat(plan): task 2 — create automated-validation reference (#161)"
```

### Task 3: Create human-validation.md

**Files:**
- Create: `skills/validate-plan/references/human-validation.md`

- [x] **Step 1: Write human-validation.md**

Write `skills/validate-plan/references/human-validation.md` covering:

- Presentation format (full numbered list with automated results filled in,
  each item shows pass/fail/pending status)
- Default mode: full list (present all pending criteria at once)
- One-by-one mode (if user requests, present individually with Goal context)
- Confirmation vs. judgment (binary criteria vs. judgment criteria —
  for judgment, ask user to explain briefly as evidence)
- Mixed validation (run automated part first, skip human if automated fails)
- Escalation (mark uncertain rather than forcing pass/fail, flag in output)
- Examples section with 2-3 examples:
  - Research: "All sub-questions answered with cited sources"
  - Design: "ADR includes Alternatives section with 2+ options"
  - Mixed: "`pytest` passes AND error messages are user-friendly"

Target: 60-70 lines.

- [x] **Step 2: Verify line count**

```bash
wc -l skills/validate-plan/references/human-validation.md
```

Expected: 50-80 lines.

- [x] **Step 3: Commit**

```bash
git add skills/validate-plan/references/human-validation.md
git commit -m "feat(plan): task 3 — create human-validation reference (#161)"
```

### Task 4: Create failure-diagnosis.md

**Files:**
- Create: `skills/validate-plan/references/failure-diagnosis.md`

- [x] **Step 1: Write failure-diagnosis.md**

Write `skills/validate-plan/references/failure-diagnosis.md` covering:

- The task-pass / plan-fail problem (100% task completion, 13% cross-task
  recall — this is what plan-level validation catches)
- Three gap types table:

  | Gap Type | Signal | Example |
  |----------|--------|---------|
  | Integration gap | Files correct individually, composition broken | Module A→B data shape mismatch |
  | Specification drift | Implementation works but doesn't match Goal | Plan says paginated, implementation returns all |
  | Missing cross-cutting | No task addressed plan-level quality | No consistent error format across API |

- Diagnostic protocol (5 steps: identify failure → re-read Goal/Scope →
  compare against task verifications → classify gap → write diagnosis)
- Recovery: suggest new tasks (1-3 concrete tasks matching plan's format,
  plan stays `executing`, ask user: add tasks or abandon?)
- When NOT to add tasks (fundamental design flaw → recommend abandon +
  new plan with revised design, structured feedback format)
- Examples section: one per gap type showing failing criterion, diagnostic
  reasoning, and suggested new tasks

Target: 80-90 lines.

- [x] **Step 2: Verify line count**

```bash
wc -l skills/validate-plan/references/failure-diagnosis.md
```

Expected: 70-100 lines.

- [x] **Step 3: Commit**

```bash
git add skills/validate-plan/references/failure-diagnosis.md
git commit -m "feat(plan): task 4 — create failure-diagnosis reference (#161)"
```

### Task 5: Update execute-plan SKILL.md

**Files:**
- Modify: `skills/execute-plan/SKILL.md` (lines 95-106)

- [x] **Step 1: Update Step 5 to confirmation gate**

In `skills/execute-plan/SKILL.md`, replace the current Step 5 (lines 95-102):

```markdown
### 5. Validate

When all tasks are checked:

1. Invoke `wos:validate-plan`
2. If validation passes, update frontmatter to `status: completed`
3. If validation fails, consult recovery patterns — add new tasks to
   address gaps, do NOT mark the plan as failed
```

With:

```markdown
### 5. Validate

When all tasks are checked, recommend running `wos:validate-plan` to
verify the plan succeeded end-to-end. Ask the user for confirmation.

- **User confirms** — invoke `wos:validate-plan`, which runs validation
  and handles the `status: completed` transition on success.
- **User declines** — update frontmatter to `status: completed` directly.
  The user accepts responsibility for skipping plan-level validation.
```

- [x] **Step 2: Verify the change reads correctly**

Read `skills/execute-plan/SKILL.md` and confirm Step 5 flows naturally
with Steps 4 and 6.

- [x] **Step 3: Commit**

```bash
git add skills/execute-plan/SKILL.md
git commit -m "feat(plan): task 5 — update execute-plan to recommend validate-plan (#161)"
```

### Task 6: Run validation

- [x] **Step 1: Run WOS audit**

```bash
uv run python -m pytest tests/ -v
uv run scripts/audit.py --root . --no-urls
```

Expected: all tests pass, no new audit failures. Check that the new
SKILL.md passes skill quality checks (name format, description length,
body under 500 lines).

- [x] **Step 2: Verify skill discovery**

Confirm the skill directory structure is correct:

```bash
ls -la skills/validate-plan/
ls -la skills/validate-plan/references/
```

Expected:
```
skills/validate-plan/SKILL.md
skills/validate-plan/references/automated-validation.md
skills/validate-plan/references/human-validation.md
skills/validate-plan/references/failure-diagnosis.md
```

- [x] **Step 3: Verify instruction density**

Check that total instruction lines across SKILL.md + all references
stays under 200:

```bash
uv run scripts/audit.py --root . --no-urls 2>&1 | grep -i "validate-plan"
```

Expected: no instruction density warnings for validate-plan.

- [x] **Step 4: Fix any issues found and commit**

If audit or tests surface issues, fix them and commit:

```bash
git add -A
git commit -m "fix: address validation issues in validate-plan skill (#161)"
```

## Validation

1. `uv run python -m pytest tests/ -v` passes with no failures
2. `uv run scripts/audit.py --root . --no-urls` reports no new failures
   for validate-plan skill files
3. `skills/validate-plan/SKILL.md` exists and is under 500 non-blank lines
4. Three reference files exist in `skills/validate-plan/references/`
5. `skills/execute-plan/SKILL.md` Step 5 uses confirmation gate pattern
   (no longer auto-invokes validate-plan)
6. Skill description includes trigger phrases: "validate", "verify the plan",
   "check if done", "are we done"
