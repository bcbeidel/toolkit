---
name: Recovery Patterns
description: Failure handling — task splitting, retry protocol, escalation, git rollback, task-pass/plan-fail
---

# Recovery Patterns

What to do when things go wrong during plan execution.

## Task Splitting on Partial Completion

When a task is partially done (some steps completed, others not):

1. **Identify the boundary** — what work is done and committed?
2. **Split the task** in the plan file:
   - Mark the done portion `[x]` with its commit SHA
   - Create a new checkbox for the remaining work
3. **Continue** from the new task

Example:

```markdown
- [x] Task 3a: Add validation logic (partial) <!-- sha:abc1234 -->
- [ ] Task 3b: Add validation error messages (remaining)
```

This preserves the work already done and gives the remaining portion
a clean starting point.

## Retry Protocol

When verification fails:

1. **First attempt** — implement and verify as planned
2. **First retry** — read the error output, diagnose the issue,
   fix it, re-verify
3. **Second retry** — read the error output again, try a different
   approach, re-verify
4. **Escalate** — after 2 retries (3 total attempts), stop and
   escalate to the user

**Feed failure output back.** On each retry, include the full error
output from the previous attempt. This gives the agent context for
self-correction.

## Escalation Format

When escalating to the user, provide:

- **What was tried** — the approaches attempted (all 3)
- **Evidence** — error output, logs, diffs
- **Options** — 2-3 possible paths forward with tradeoffs
- **Recommendation** — your best judgment with confidence level

Do not just say "it doesn't work." Provide enough context for the
user to make an informed decision.

## Git-Based Rollback

Each completed task's checkbox has a commit SHA annotation. Use these
for targeted rollback:

```bash
# See what changed in a specific task
git diff <prev-sha>..<task-sha>

# Revert a specific task's changes
git revert <task-sha>
```

**Prefer revert over reset.** Revert creates a new commit that undoes
the changes, preserving history. Reset discards history and can lose
work.

## Task-Pass / Plan-Fail

When all tasks pass individually but plan-level validation fails:

1. **Do NOT mark the plan as failed** — the tasks are done correctly
2. **Identify the gap** — which integration or cross-cutting
   requirement is unmet?
3. **Add new tasks** — append new checkboxes to the plan addressing
   the gaps
4. **Continue execution** — the plan stays in `executing` state
   with the additional tasks

This is a known failure mode: agents can achieve 100% task completion
but miss cross-cutting concerns. The plan-level Validation section
exists to catch exactly this.

## Transient vs. Non-Transient Failures

**Transient** — retry is likely to help:
- Flaky tests
- Network timeouts
- Rate limits
- Temporary resource unavailability

**Non-transient** — retry will not help, escalate immediately:
- Missing APIs or endpoints
- Wrong architecture or approach
- Missing dependencies not in the plan
- Permission or access issues

Distinguish between these before retrying. Retrying a non-transient
failure wastes attempts and delays escalation.
