---
name: Plan Format Guide
description: How to write effective plan sections — goals, scope, tasks, and verification
---

# Plan Format Guide

Guidance for writing each of the 6 required plan sections. For the structural
reference (frontmatter schema, lifecycle states, task decomposition rules),
see [Plan Document Format](../../_shared/references/plan-format.md).

## Writing the Goal

State the user-visible outcome in 2-3 sentences. Lead with what changes,
then why it matters. Avoid implementation language.

| Quality | Example |
|---------|---------|
| Good | "Users can filter audit results by severity and file type. This reduces noise when investigating specific issues." |
| Bad | "Add --severity and --type flags to the audit CLI and wire them through validators.py" |
| Bad | "Improve the audit experience." |

The goal should be verifiable from outside the codebase. If someone unfamiliar
with the project reads it, they should understand what success looks like.

## Scoping with Must / Won't

Must-have items define the minimum viable delivery. Won't-have items are
equally important — they prevent scope creep by making exclusions explicit.

Include anything the user might reasonably expect but that's excluded. If
a feature is adjacent but not part of this plan, put it in Won't.

**Signals you need Won't items:**
- The design mentions future work
- The feature has obvious extensions you're not building yet
- The plan touches shared code that other features also use

## Writing the Approach

High-level technical strategy. 2-4 sentences describing how the goal will
be achieved. Name the key architectural decisions.

This is "middle altitude" — enough detail to orient the implementer, not
enough to prescribe every line of code. If the approach reads like
pseudo-code, it's too detailed. If it reads like a goal restated, it's
too abstract.

## File Changes

List every file created, modified, or deleted. For modifications, include
what changes (not just the file path).

    - Create: `wos/new_module.py`
    - Modify: `wos/validators.py` (add severity filter to validate_project)
    - Modify: `tests/test_validators.py` (add filter tests)
    - Delete: `wos/old_module.py`

Include line references for targeted modifications when the file is large.

## Writing Tasks

Tasks are the plan's core. Each task is a deliverable with verification.

**Middle altitude:**

| Level | Example | Problem |
|-------|---------|---------|
| Too abstract | "Implement authentication" | No verification possible |
| Right | "Add login endpoint that returns JWT. Verify: `curl -X POST /login` returns 200" | Observable outcome with command |
| Too granular | "Add `import jwt` on line 3 of auth.py" | Prescribes implementation |

**Verification patterns:**

Every task ends with a verification step. Types:
- Test command: `python python -m pytest tests/test_foo.py::test_name -v`
- CLI invocation: `python scripts/lint.py --root . | grep "0 failures"`
- Manual check: `wc -l skills/foo/SKILL.md` (expected: under 500)
- Read verification: confirm file exists and contains expected content
- Human confirmation: present summary to user, confirm scope matches intent
- Content verification: "Verify file contains [section/keyword]"
- Structural check: "Confirm frontmatter has required fields: name, description, type"

**Task naming:** Name tasks as deliverables, not activities.
- Good: "Login endpoint with JWT response"
- Bad: "Work on authentication"

## Writing Validation

End-to-end criteria that prove the plan succeeded. These are higher-level
than task verification — they test the whole feature, not individual pieces.

At least one criterion required. Each must be concrete:

| Quality | Example |
|---------|---------|
| Good | "`python python -m pytest tests/ -v` — all tests pass" |
| Good | "`python scripts/lint.py --root .` — no failures for new skill" |
| Bad | "Verify the feature works correctly" |
| Bad | "Everything should be tested" |

## Chunking Large Plans

Group tasks into chunks of 3-5 by logical dependency — tasks within a
chunk share files or build on each other. Each chunk should produce
a verifiable intermediate state. Name chunks by outcome, not sequence:
"Authentication endpoints" not "Chunk 1."
