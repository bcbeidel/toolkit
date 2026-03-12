---
name: "Validate Work Ad-Hoc Mode Design"
description: "Design for plan-free validation path in validate-work — git diff + project conventions build a hypothesis, user confirms, then execute"
type: design
status: draft
related:
  - skills/validate-work/SKILL.md
  - skills/validate-work/references/automated-validation.md
  - skills/validate-work/references/human-validation.md
---

## Goal

Let users call `/wos:validate-work` without a plan. The skill inspects
git diff, project conventions, and project docs to build a validation
hypothesis — a prioritized list of criteria. The user confirms, edits,
or supplements the list before execution begins.

## Behavior

### Entry Branching

Step 1 of the existing workflow changes from "Load Plan" to "Determine
Mode":

- **Plan path:** User provides a plan file, or a plan is found in
  context. Existing behavior — no changes.
- **Ad-hoc path:** No plan provided or found. Skill announces it will
  build a validation hypothesis from the project state.

The rest of the workflow (classify criteria, run automated, present
human, handle failures) is identical for both paths. The only
difference is where the criteria list comes from.

### Ad-Hoc Hypothesis Building

Three signal sources, checked in order:

**1. Git diff analysis**

Inspect changes to understand what was modified:
- `git diff main...HEAD` — committed changes on the branch
- `git diff` + `git diff --cached` — unstaged and staged work
- Categorize changed files: source code, tests, config, docs, other

This tells the skill *what changed* — which modules, which layers,
whether tests were added/modified.

**2. Project convention detection**

Scan for config files to infer available checks:

| Config file | Inferred check |
|------------|---------------|
| `pyproject.toml` (has `[tool.pytest]` or `pytest` dep) | `pytest` |
| `pyproject.toml` (has `[tool.ruff]`) | `ruff check` |
| `pyproject.toml` (has `[tool.mypy]`) | `mypy` |
| `package.json` (has `test` script) | `npm test` |
| `package.json` (has `lint` script) | `npm run lint` |
| `tsconfig.json` | `npx tsc --noEmit` |
| `.eslintrc*` / `eslint.config.*` | `npx eslint` |
| `Makefile` (has `test` target) | `make test` |
| `Cargo.toml` | `cargo test`, `cargo clippy` |
| `go.mod` | `go test ./...`, `go vet ./...` |

Only include checks for tools that are actually configured in the
project. Don't guess.

**3. Project documentation signals**

Read project docs for additional validation cues:
- `CLAUDE.md` / `AGENTS.md` — build/test commands, conventions, lint rules
- `README.md` — setup instructions, documented test commands
- `CONTRIBUTING.md` — CI expectations, quality gates

Extract any explicit test/lint/build commands mentioned in these files.

### Hypothesis Presentation

Present the synthesized criteria list to the user:

```
Based on your changes and project setup, here's what I'd validate:

Changes detected:
- 3 source files modified (wos/skill_audit.py, scripts/audit.py, ...)
- 1 test file modified (tests/test_skill_audit.py)
- 1 doc file modified (CLAUDE.md)

Proposed checks:
1. [auto] `uv run python -m pytest tests/ -v` — test suite passes
2. [auto] `ruff check wos/ tests/ scripts/` — no lint violations
3. [human] Changed behavior matches intent (CLAUDE.md updated to reflect new defaults)

Add, remove, or modify any of these? Or confirm to run.
```

Key rules for hypothesis building:
- **Scope checks to what changed.** If only `wos/skill_audit.py` changed,
  don't propose running the entire project's integration suite.
- **Tests first.** If tests exist for changed code, they're always the
  first criterion.
- **Lint if configured.** Only propose linting if a linter config exists.
- **Human criteria for doc/behavior changes.** If docs or config changed,
  add a human criterion for intent alignment.
- **No invented criteria.** Every proposed check must be grounded in a
  signal (git diff showed it, config file enables it, project docs
  mention it). State the signal source.

### User Confirmation Gate

The user can:
- **Confirm** — run the checks as proposed
- **Add** — append criteria (automated or human)
- **Remove** — drop criteria they don't want
- **Modify** — change commands or descriptions

Execution only begins after explicit confirmation. This is the gate
that prevents false-positive checks from wasting time.

### Execution

Once confirmed, the criteria list feeds into the existing Steps 4-7:
- Step 4: Run automated checks (per automated-validation.md)
- Step 5: Present human criteria (per human-validation.md)
- Step 6: Handle failures — in ad-hoc mode, suggest fixes rather than
  plan tasks. No plan to update, so present findings and ask the user
  what to do next.
- Step 7: On success, report results. No plan status to update.

### Failure Handling Difference

In plan mode, failures produce new tasks added to the plan. In ad-hoc
mode, failures produce:
- The diagnosis (what failed, evidence)
- Suggested actions (not plan tasks — just "here's what to fix")
- Offer to re-run validation after fixes

The failure-diagnosis reference (gap types, diagnostic protocol) still
applies conceptually but the recovery mechanism is lighter — no plan
file to modify.

## Components

### Modified

- `skills/validate-work/SKILL.md` — Add mode branching at Step 1,
  ad-hoc hypothesis building steps, modified failure handling for
  ad-hoc mode

### New

- `skills/validate-work/references/adhoc-validation.md` — Convention
  detection table, hypothesis building protocol, config-file-to-check
  mapping, project doc scanning guidance

### Unchanged

- `skills/validate-work/references/automated-validation.md` — works as-is
- `skills/validate-work/references/human-validation.md` — works as-is
- `skills/validate-work/references/failure-diagnosis.md` — works as-is
  (gap types apply conceptually; plan-specific recovery language can be
  conditioned on mode)

## Constraints

- No new Python scripts. This is pure skill logic — the model reads
  git diff, scans for config files, and builds the hypothesis.
- The plan path must remain unchanged. Ad-hoc is additive.
- Hypothesis must be grounded in signals, not invented. Every proposed
  check traces to a git diff finding, config file, or project doc.

## Acceptance Criteria

1. User can call `/wos:validate-work` with no plan and get a useful
   validation hypothesis based on their actual changes and project setup
2. User can confirm, add, remove, or modify proposed criteria before
   execution
3. Existing plan-based workflow is unaffected
4. Skill stays under 500 instruction lines (current: 281)
