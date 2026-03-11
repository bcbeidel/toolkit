---
name: Validate Plan Skill Design
description: Design spec for wos:validate-plan skill — plan-level validation with automated/human criteria, failure diagnosis, and recovery
type: plan
status: approved
related:
  - docs/plans/2026-03-11-execute-plan-skill-design.md
  - docs/plans/2026-03-11-plan-document-format-design.md
  - skills/_shared/references/plan-format.md
branch: feat/161-validate-plan-skill
pull-request: TBD
---

# Validate Plan Skill Design

## Purpose

WOS-native skill for verifying that a plan succeeded end-to-end. Catches
the task-pass / plan-fail gap where agents achieve 100% task completion
but miss cross-task synthesis (13% recall per Akshathala et al., 2025).
Works standalone — recommended as follow-up after completing all tasks
in a plan.

## Scope

Must have:
- `skills/validate-plan/SKILL.md` under 500 lines
- Three reference files: `automated-validation.md`, `human-validation.md`, `failure-diagnosis.md`
- Skill triggers on "validate", "verify the plan", "check if done", "are we done"
- Precondition check via existing `assess_plan.py` (all tasks checked)
- Automated validation: run commands, check exit codes, capture output
- Human validation: present criteria, collect confirmation (full list default, one-by-one option)
- Mixed validation: automated + human in same criterion
- Task-pass/plan-fail diagnosis with three gap types and recovery
- Structured output: per-criterion results, diagnosis on failure
- Update to execute-plan SKILL.md: recommend validate-plan with confirmation gate

Won't have:
- New Python code or validation scripts (LLM handles criteria classification and execution)
- Plan-specific audit validators in `wos/validators.py` (separate concern)
- Code-enforced validation section format (convention, not enforcement)
- Automatic invocation from execute-plan (user confirms)

## Skill Directory Structure

```
skills/validate-plan/
├── SKILL.md                          (~150-200 lines)
└── references/
    ├── automated-validation.md       (~70-80 lines)
    ├── human-validation.md           (~60-70 lines)
    └── failure-diagnosis.md          (~80-90 lines)
```

No new Python code. Uses existing `assess_plan.py` for precondition
checks via preflight pattern. Validation criteria extraction (parsing
the Validation section, classifying items, interpreting results) is
LLM work guided by SKILL.md instructions and reference files.

## SKILL.md Workflow

### Metadata

```yaml
---
name: validate-plan
description: >
  Verifies a plan succeeded end-to-end by running validation criteria.
  Use when the user wants to "validate the plan", "verify the plan",
  "check if done", "run validation", "are we done", "did the plan work",
  or after completing all tasks in a plan. Handles both automated
  (command) and human (judgment) validation criteria.
user-invocable: true
argument-hint: "[plan file path]"
references:
  - references/automated-validation.md
  - references/human-validation.md
  - references/failure-diagnosis.md
  - ../_shared/references/preflight.md
  - ../_shared/references/plan-format.md
---
```

### Steps

**Step 1: Load plan** — read plan file, locate Validation section. Validation
criteria are a numbered list, prioritized, with embedded code blocks for
runnable commands.

**Step 2: Check preconditions** — run `assess_plan.py --file <plan>` via
preflight pattern. All task checkboxes must be checked. If unchecked tasks
remain, report them and stop. Do not proceed with partial validation.

**Step 3: Classify criteria** — tag each numbered item in the Validation
section. Classification lives in SKILL.md body (straightforward rules):
- **Automated** — item contains a runnable command in a code block
- **Human** — item describes an observable condition requiring judgment
- **Mixed** — item has both an automated command and a judgment component

**Step 4: Run automated checks** — execute commands from automated and
mixed criteria. Capture exit code + output per criterion. Exit code 0 = pass,
non-zero = fail. Load `automated-validation.md` for execution patterns,
output interpretation, and environment handling.

**Step 5: Present human criteria** — show full numbered list with automated
results already filled in. Each item gets a status: pass (automated confirmed),
fail (automated failed), or pending (needs human judgment). Ask user to
confirm each pending criterion. Offer one-by-one mode if user prefers. Load
`human-validation.md` for presentation patterns and escalation.

**Step 6: Handle failures** — if any criterion fails, load
`failure-diagnosis.md`. Classify gap type (integration gap, specification
drift, or missing cross-cutting concern). Suggest 1-3 new tasks to close the
gap. Keep plan in `executing` state. Ask user: add suggested tasks, or
abandon?

**Step 7: On success** — update plan frontmatter `status: completed`. Output
structured summary: total criteria count, pass/fail per item, any
human-confirmed items with user notes.

## Reference File Design

### `automated-validation.md` (~70-80 lines)

Serves workflow step 4 (run automated checks). Classification logic is
inline in SKILL.md; this reference covers execution and interpretation.

**Content:**

- **Command execution protocol** — run each code block from the Validation
  section in priority order. Capture exit code, stdout, stderr. Exit code
  0 = pass, non-zero = fail.
- **Structural vs. semantic checks** — structural checks confirm observable
  state (file exists, function exported, endpoint returns 200). Semantic
  checks confirm behavior (test suite passes, migration runs clean). Both
  can be automated.
- **Output interpretation** — not all non-zero exits are failures. Test
  runners report failure counts, linters distinguish warning vs. error,
  build tools may warn without failing. Read output, don't just check exit
  code.
- **Environment sensitivity** — commands may depend on project setup (running
  server, database, env vars). If a command fails with an environment error
  (not found, connection refused), report as "blocked" not "failed." Suggest
  what the user needs to set up.
- **Idempotency** — validation commands should be safe to re-run. If a
  command has side effects, flag to user before running.
- **Examples** — 3-4 by plan type:
  - Code implementation: `pytest tests/ -v` → check exit code + "N passed"
  - Refactoring: `ruff check src/` → zero errors + `pytest` → no regressions
  - Migration: `python manage.py migrate --check` → "No migrations to apply"

**Research support:** Plan Execution research (3-level verification, exit code
patterns). Input Validation research (eager/lazy timing, structural vs.
semantic tiers).

### `human-validation.md` (~60-70 lines)

Serves workflow step 5 (present human criteria). Classification logic is
inline in SKILL.md; this reference covers presentation and confirmation.

**Content:**

- **Presentation format** — show full numbered list with automated results
  filled in. Each item: pass, fail, or pending. Full context before user
  starts confirming.
- **Default mode: full list** — present all pending criteria at once. Faster
  for experienced users, gives the big picture.
- **One-by-one mode** — if user requests, present each criterion individually
  with context from the plan's Goal section. Wait for confirmation before
  next.
- **Confirmation vs. judgment** — binary criteria ("ADR has Alternatives with
  2+ options" — look and confirm) vs. judgment criteria ("documentation is
  clear"). For judgment, ask user to explain briefly — becomes evidence in
  output.
- **Mixed validation** — when a criterion has automated + human parts, run
  automated first. If automated fails, skip human part.
- **Escalation** — if user is unsure, mark as "uncertain" rather than forcing
  pass/fail. Uncertain items flagged in output for follow-up.
- **Examples** — 2-3:
  - Research: "All sub-questions answered with cited sources" → user reviews
  - Design: "ADR includes Alternatives section with 2+ options" → user checks
  - Mixed: "`pytest` passes AND error messages are user-friendly"

**Research support:** Document Lifecycle (consensus-based gates). LLM Output
Verification (4 HITL patterns: interrupt-resume, human-as-tool, approval,
escalation).

### `failure-diagnosis.md` (~80-90 lines)

Serves workflow step 6 (handle failures).

**Content:**

- **The task-pass / plan-fail problem** — all checkboxes checked, each task
  verified individually, but end-to-end validation fails. Agents achieve
  100% task completion but 13% recall on cross-task synthesis.
- **Three gap types:**

  | Gap Type | Signal | Example |
  |----------|--------|---------|
  | Integration gap | Files correct individually, composition broken | Module A exports correctly, Module B imports correctly, but A→B data shape mismatches |
  | Specification drift | Implementation works but doesn't match Goal | Plan says "paginated API" but implementation returns all results |
  | Missing cross-cutting concern | No task addressed plan-level quality | Each endpoint validates input, but no consistent error format across API |

- **Diagnostic protocol:**
  1. Identify which criterion failed
  2. Re-read plan's Goal and Scope sections
  3. Compare failed criterion against task verifications — where does gap emerge?
  4. Classify using three gap types
  5. Write diagnosis: what failed, gap type, evidence, suggested new tasks

- **Recovery: suggest new tasks** — for each failure, propose 1-3 concrete
  tasks matching plan's existing task format. Present to user: add tasks
  (plan stays `executing`), or abandon?
- **When NOT to add tasks** — fundamental design flaw means adding tasks
  won't help. Recommend abandoning plan and creating new one with revised
  design. Use structured feedback: what's wrong, why, impact, alternatives.
- **Examples** — one per gap type: failing criterion, diagnostic reasoning,
  suggested new tasks.

**Research support:** Plan Execution (task-pass/plan-fail, 100% completion /
13% cross-task recall). Plan Document Design (14-mode failure taxonomy).
Feedback Mechanisms (ECR-style structured feedback).

## Execute-Plan SKILL.md Update

Change Step 5 from auto-invoking validate-plan to a confirmation gate:

> After all tasks are checked, recommend running `wos:validate-plan` to
> verify the plan succeeded end-to-end. Ask the user for confirmation.
>
> - **User confirms** → invoke `wos:validate-plan`, which runs validation
>   and handles the `status: completed` transition on success.
> - **User declines** → execute-plan updates `status: completed` directly.
>   The user accepts responsibility for skipping plan-level validation.

This preserves the lifecycle gate as a recommended step while giving the
user control. The `executing → completed` transition always happens — the
question is whether it goes through validation first.

## Structured Output

**On success:**
- Update frontmatter: `status: executing` → `status: completed`
- Summary: total criteria, pass count, human-confirmed items with notes

**On failure:**
- Frontmatter stays: `status: executing`
- Summary: total criteria, pass/fail per item, diagnosis (gap type + evidence),
  suggested new tasks
- Prompt user: add tasks to plan, or abandon?

## Design Justification

| Decision | Source | Evidence |
|----------|--------|----------|
| 3-level verification (task/session/plan) | Codex PLANS.md (OpenAI, 2025); Best Practices (Anthropic, 2025) | Verification is "the single highest-leverage thing you can do"; Codex requires observable acceptance criteria |
| Validation as gate, not state | Quality Gates (SonarSource, 2025) | Gates "act as checkpoints... ensuring each stage meets specific criteria before code advances"; no AI tool implements "validating" state |
| Task-pass / plan-fail | Assessment Framework for Agentic AI (Akshathala et al., 2025) | 100% task completion but 13.1% recall on cross-task synthesis; 100% tool sequencing but 33% policy adherence |
| Dual validation (automated + human) | Comparative analysis across 6 AI tools | No tool addresses non-code validation; research/design plans need qualitative criteria |
| Standalone skill, recommended by execute-plan | Skill authoring conventions (WOS) | User-invocable skills with clear trigger phrases; execute-plan recommends, user confirms |
| Three reference files (domain-organized) | Research skill consolidation (WOS) | Each reference serves distinct phases, loads only when active; ~87 line average |
| assess_plan.py for preconditions | Execute-plan design (WOS) | Deterministic checks in Python, judgment in LLMs (P2); script already parses tasks and tracks completion |
