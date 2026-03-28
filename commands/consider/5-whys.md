---
description: Drill to root cause by asking why repeatedly until fundamentals emerge
metadata:
  argument-hint: "[problem or symptom to trace to its root cause]"
---

<objective>
Move past symptoms to find the root cause of a problem. Each "why" peels
back a layer of causation. Usually 5 iterations reach the systemic cause
that, if addressed, prevents recurrence.
</objective>

<process>
1. State the problem or symptom clearly
2. Ask "Why does this happen?" — record the answer
3. Take that answer and ask "Why?" again
4. Repeat until you reach a root cause (typically 5 levels)
5. Verify: does addressing the root cause prevent the original symptom?
6. Check for multiple causal chains (problems often have more than one root)
7. Identify the most actionable root cause to address first
</process>

<output_format>
## 5 Whys Analysis: [Topic]

### Problem Statement
[The symptom or issue observed]

### Why Chain
1. Why? [Answer 1]
2. Why? [Answer 2]
3. Why? [Answer 3]
4. Why? [Answer 4]
5. Why? [Root cause]

### Root Cause
[The fundamental issue identified]

### Verification
[Would fixing this root cause prevent the original problem?]

### Action
[Specific step to address the root cause]
</output_format>

<example>
## 5 Whys Analysis: CI Builds Failing Intermittently

### Problem Statement
Integration tests fail roughly 20% of the time on CI but pass locally.

### Why Chain
1. Why? Tests depend on a shared database that sometimes has stale data from previous runs.
2. Why? Test teardown doesn't reset the database — it relies on transactions that sometimes don't roll back.
3. Why? Two test suites run in parallel and share a single test database instance.
4. Why? The CI config was copied from a project that ran tests sequentially.
5. Why? No one reviewed the CI config when we added the second test suite six months ago.

### Root Cause
CI infrastructure was never updated when test parallelism was introduced. The shared database assumption held for sequential runs but breaks under concurrency.

### Verification
Giving each parallel suite its own database instance would eliminate the shared-state race condition, preventing the intermittent failures.

### Action
Create per-suite database instances in CI using a template database that's cloned at suite start and destroyed at suite end.
</example>

