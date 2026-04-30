---
name: via-negativa
description: Improve by removing problems rather than adding solutions — use when a system or process has accumulated complexity and improvement by addition has hit diminishing returns
argument-hint: "[system, process, or situation to improve]"
user-invocable: true
license: MIT
---

<objective>
Instead of asking "what should we add?", ask "what should we remove?"
Often the fastest path to improvement is eliminating what's harmful,
unnecessary, or creating friction. Subtraction before addition.
</objective>

<process>
1. Describe the current state of the system or situation
2. List everything currently present (features, steps, dependencies, rules)
3. For each element, ask: "Would things improve if this were removed?"
4. Identify the top 3-5 candidates for removal
5. For each candidate, assess: What breaks if we remove it? What improves?
6. Propose the removal plan (what to cut, in what order)
7. Check: does the simplified version still achieve the core purpose?
</process>

<output_format>
## Via Negativa Analysis: [Topic]

### Current State
[Brief description of what exists today]

### Removal Candidates
| Element | Remove? | What improves | What breaks |
|---------|---------|--------------|-------------|
| [Item] | Yes/No | ... | ... |

### Recommended Removals
1. [What to remove and why]
2. ...

### Simplified Version
[What remains after removals — does it still serve the core purpose?]

### What NOT to Remove
[Elements that seem removable but are load-bearing]
</output_format>

<example>
## Via Negativa Analysis: Deployment Pipeline

### Current State
Deployment pipeline has 12 steps: lint, unit test, integration test, build Docker image, push to registry, deploy to staging, run smoke tests, wait for manual approval, deploy to canary, monitor for 30 minutes, deploy to production, run production smoke tests.

### Removal Candidates
| Element | Remove? | What improves | What breaks |
|---------|---------|--------------|-------------|
| Manual approval gate | Yes | Deploy time drops 2-4 hours (waiting for approver) | Nothing — canary + smoke tests catch issues automatically |
| Separate lint step | Yes | 2 min saved — linting runs in IDE and pre-commit hooks already | Nothing — issues caught earlier in workflow |
| Staging environment | Yes | Eliminates a flaky environment that causes 30% of pipeline failures | Need canary to be reliable (it already is) |
| 30-min canary monitor | No | — | Removing loses the safety net for slow-burn issues |
| Integration tests | No | — | Only place we catch cross-service contract breaks |

### Recommended Removals
1. Manual approval gate — replaced by automated canary monitoring, which is more consistent than a human glancing at dashboards
2. Separate lint step — redundant with pre-commit hooks; lint errors haven't reached CI in 4 months
3. Staging environment — flaky environment causes more failed deploys than it prevents; canary on production traffic is a better signal

### Simplified Version
9 steps: unit test, integration test, build, push, deploy canary, monitor 30 min, deploy production, smoke test. Still catches regressions, still has gradual rollout, but 30% faster and no flaky staging.

### What NOT to Remove
The 30-minute canary monitor looks like wasted time but caught a memory leak last month that smoke tests missed. It's load-bearing.
</example>

## Key Instructions

- Always assess whether a removal candidate is load-bearing before proposing it; the "What NOT to Remove" section must be completed, not skipped.
- Does not implement removals; produces a removal plan the user executes.

## Anti-Pattern Guards

1. **Removing without checking dependencies** — an element may look unused but be load-bearing for edge cases; step 5 must assess what breaks, not just what improves.
2. **Using via negativa to justify rewrites** — subtraction should be incremental; removing everything at once and rebuilding is not via negativa, it's a rewrite.

## Handoff

**Receives:** A system, process, or situation where something currently present may be causing friction or unnecessary complexity
**Produces:** A ranked removal candidate analysis with a simplified version and explicit load-bearing elements to preserve
**Chainable to:** `occams-razor` (to confirm the simplified version is the most parsimonious one that still works), `first-principles` (to verify the core purpose before deciding what's essential)

