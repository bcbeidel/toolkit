# Failure Diagnosis

How to diagnose and recover when plan-level validation fails after all
tasks pass individually.

## The Task-Pass / Plan-Fail Problem

All task checkboxes are checked. Each task was verified individually.
But end-to-end validation fails. This is not a bug — it is the primary
failure mode that plan-level validation exists to catch.

Research evidence: agents achieve 100% task completion but only 13%
recall on cross-task synthesis (Akshathala et al., 2025). Individual
tasks are correct; the composition is not.

## Three Gap Types

When validation fails after all tasks pass, classify the gap:

| Gap Type | Signal | Example |
|----------|--------|---------|
| **Integration gap** | Files correct individually, composition broken | Module A exports `UserDTO`, Module B imports `UserDTO`, but A returns `{id, name}` and B expects `{id, name, email}` |
| **Specification drift** | Implementation works but doesn't match the plan's Goal | Plan says "paginated API with cursor-based navigation" but implementation returns all results in a single response |
| **Missing cross-cutting concern** | No task addressed a quality that only manifests at plan level | Each endpoint validates input independently, but there is no consistent error response format across the API |

## Diagnostic Protocol

When a validation criterion fails:

1. **Identify** — which specific criterion failed and what evidence
   shows the failure (command output, user observation)
2. **Re-read Goal and Scope** — compare the failed criterion against
   what the plan intended to achieve. Is the criterion testing
   something in scope?
3. **Trace the gap** — compare the failed criterion against individual
   task verifications. Each task passed its own check — where does
   the gap between "tasks correct" and "plan incorrect" emerge?
4. **Classify** — assign one of the three gap types above. The
   classification determines the recovery approach.
5. **Write diagnosis** — structured output:

```
## Validation Failure Diagnosis

**Failed criterion:** [number and text]
**Evidence:** [command output or observation]
**Gap type:** [integration / specification drift / cross-cutting]
**Analysis:** [1-2 sentences explaining where the gap emerged]
**Suggested tasks:** [see Recovery below]
```

## Recovery: Suggest New Tasks

For each failure, propose 1-3 concrete tasks that close the gap.
Format tasks to match the plan's existing style (checkbox items with
verification commands).

**Integration gap example:**
```markdown
- [ ] Task N+1: Align UserDTO shape between auth and profile modules
  Modify `src/auth/dto.py` to include `email` field.
  Verify: `pytest tests/integration/ -v` passes with cross-module test.
```

**Specification drift example:**
```markdown
- [ ] Task N+1: Add cursor-based pagination to /api/users endpoint
  Modify `src/api/users.py` to accept `cursor` parameter and return
  `next_cursor` in response.
  Verify: `curl '/api/users?limit=10'` returns `next_cursor` field.
```

**Cross-cutting concern example:**
```markdown
- [ ] Task N+1: Standardize error response format across all endpoints
  Create `src/api/errors.py` with `ErrorResponse` schema. Update all
  endpoint error handlers to use it.
  Verify: `pytest tests/test_error_format.py -v` checks 3+ endpoints
  return consistent `{error, message, status}` shape.
```

Present suggested tasks to the user:

> "Validation found [N] failing criteria. I've diagnosed the gaps and
> suggest [M] new tasks to address them. Add these tasks to the plan
> (keeps status: executing), or abandon the plan?"

If the user adds tasks, insert them into the plan's **Tasks section**
(before the Validation heading). Tasks placed after the Validation
heading are invisible to `assess_plan.py`. Update the plan file on disk.

## When NOT to Add Tasks

Adding tasks addresses gaps in execution. But if the failure reveals
a **fundamental design flaw** — wrong architecture, wrong technology
choice, incorrect assumptions about the problem — additional tasks
will not fix it.

Signs of a design flaw:
- Multiple criteria fail for different reasons
- The suggested fix would contradict the plan's Approach section
- The gap affects the plan's Goal, not just its implementation

In this case, recommend abandoning the plan and creating a new one:

> "This failure suggests a design-level issue, not an execution gap.
> I recommend setting this plan to `abandoned` and revising the
> design before creating a new plan."

Provide structured feedback for the design revision:
- **What failed:** specific criteria and evidence
- **Why tasks won't fix it:** explain the design-level issue
- **Impact:** which parts of the design are affected
- **Alternatives:** 1-2 design directions that might address the issue
