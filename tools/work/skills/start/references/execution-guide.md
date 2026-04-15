---
name: Execution Guide
description: Core execution loop guidance — task protocol, commit discipline, three-tier verification model
---

# Execution Guide

Detailed guidance for the task execution loop in Step 4 of the workflow.

## Task Execution Protocol

For each task, follow this sequence:

1. **Implement** — build what the task describes
2. **Verify** — confirm the task is done correctly (see verification model)
3. **Commit** — `git commit` with message `feat(plan): task N — title`
4. **Update checkbox** — `- [ ]` → `- [x]` with the SHA from step 3:
   `- [x] Task N: title <!-- sha:abc1234 -->`
5. **Commit plan update** — fold into the next task's commit, or commit
   separately if this is the last task

The implementation commit (step 3) must happen before the SHA annotation
(step 4) — you can't reference a commit that doesn't exist yet.

## Commit Discipline

**One commit per task.** This creates rollback boundaries — if task N+1
fails, you can diff against the SHA from task N to see exactly what
changed and revert cleanly.

Commit message format:

```
feat(plan): task N — short task title

Plan: docs/plans/YYYY-MM-DD-feature-name.plan.md
```

**Chunk boundaries.** For plans with 10+ tasks organized into chunks
(`## Chunk N: name`), also commit at chunk transitions. Chunk commits
are supplementary — they don't replace per-task commits.

## Three-Tier Verification Model

Not all verification is running tests. Identify which type applies to
each task and use the matching protocol.

| Type | Signal | Example | Protocol |
|------|--------|---------|----------|
| **Automated** | Command exit code + output | `pytest tests/test_foo.py -v` | Run the command. Confirm expected output. If it fails, the task isn't done. |
| **Structural** | Observable file/code state | "Function `assess_file` exists in module" | Read the file. Confirm the observable fact. No command needed. |
| **Reasoning** | Intent alignment | "The gate refuses draft plans" | Trace the implementation against the plan's Goal and Approach. Confirm the logic satisfies the intent, not just a test. |

**Mixed verification.** Many tasks require more than one type. A task
might need automated verification (tests pass) AND reasoning verification
(the implementation actually solves the problem, not just the test case).
Apply all applicable types.

**Verification is not optional.** If you cannot verify a task, you cannot
mark it complete. Ask the user for help defining verification criteria
rather than checking a box without proof.

## Scope Discipline

Execute the plan as written. During execution, you may discover:

- Edge cases the plan didn't anticipate
- Adjacent code that could be improved
- Features that would be nice to add

**Do not act on these.** Write them down in the plan file or a companion
notes file, then continue with the current task. Scope changes require
pausing execution and discussing with the user.

## When to Stop and Ask

Stop executing immediately when:

- **Unclear instructions** — the task description is ambiguous
- **Missing dependencies** — a required file, API, or service doesn't exist
- **Repeated verification failures** — after 2 retries (3 total attempts),
  escalate rather than continuing to loop
- **Scope uncertainty** — the task seems to require changes beyond what
  the plan described

Ask for clarification rather than guessing. Wrong guesses compound —
each incorrect step makes recovery harder.
