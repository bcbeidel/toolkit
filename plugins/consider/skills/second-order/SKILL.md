---
name: second-order
description: Think through the consequences of consequences before acting — use when an action has obvious immediate effects but the downstream consequences haven't been traced
argument-hint: "[decision or action to evaluate]"
user-invocable: true
license: MIT
---

<objective>
Go beyond immediate effects to trace second and third-order consequences.
Most people stop at "what happens next?" — this model asks "and then what?"
repeatedly to uncover hidden costs, feedback loops, and unintended effects.
</objective>

<process>
1. State the proposed action or decision
2. List all immediate (first-order) effects
3. For each first-order effect, ask "and then what?" — list second-order effects
4. For significant second-order effects, push to third-order
5. Identify feedback loops (where effects amplify or dampen themselves)
6. Map unintended consequences that only appear at higher orders
7. Reassess the original decision with full consequence chain visible
</process>

<output_format>
## Second-Order Analysis: [Topic]

### Proposed Action
[The decision being evaluated]

### Consequence Chain
- **1st order:** [Immediate effect]
  - **2nd order:** [Consequence of that effect]
    - **3rd order:** [Consequence of the consequence]

### Feedback Loops
- [Loop description: A causes B which amplifies/dampens A]

### Unintended Consequences
- [Effect that only becomes visible at 2nd/3rd order]

### Revised Assessment
[Should we proceed, modify, or abandon given full consequence chain?]
</output_format>

<example>
## Second-Order Analysis: Mandatory Code Review Policy

### Proposed Action
Require two approvals on every pull request before merge.

### Consequence Chain
- **1st order:** PRs take longer to merge (reviewers must be available)
  - **2nd order:** Developers batch smaller changes into larger PRs to reduce review overhead
    - **3rd order:** Larger PRs get superficial reviews — reviewers skim instead of reading carefully
- **1st order:** More eyes on code catches bugs earlier
  - **2nd order:** Developers rely on reviewers as a safety net, writing less carefully
- **1st order:** Junior developers get feedback and learn faster
  - **2nd order:** Senior developers spend significant time reviewing, reducing their own output
    - **3rd order:** Seniors become bottlenecks; review queues grow; teams start rubber-stamping

### Feedback Loops
- Larger PRs → worse reviews → more bugs slip through → pressure to add more reviewers → even longer queues (amplifying)
- Junior learning → better code quality over time → reviews get faster (dampening, but slow)

### Unintended Consequences
- Review bottlenecks create a two-class system: people who review and people who wait. Resentment builds.
- Two-approval rule optimizes for risk avoidance but penalizes the 90% of changes that are low-risk.

### Revised Assessment
Keep mandatory review but with one approval, not two. Add a "trivial" label for changes under 20 lines that need only one reviewer. This preserves the learning and bug-catching benefits while avoiding the bottleneck spiral.
</example>

## Key Instructions

- Stop at third-order effects for most decisions — deeper chains multiply uncertainty without adding insight.
- If a feedback loop identified in step 5 is reinforcing (amplifying), treat it as high severity regardless of the original decision's apparent scale.
- Does not recommend actions; produces a consequence map so the user can make an informed decision.

## Anti-Pattern Guards

1. **Stopping at first-order effects** — the model's value is specifically the second and third-order consequences; if the analysis doesn't go deeper than "this will happen," it hasn't been applied.
2. **Over-extending the chain** — fourth-order and beyond typically degrade into noise; flag when the analysis stops at third order and why that's sufficient.

## Handoff

**Receives:** A proposed action or decision the user wants to evaluate for downstream consequences
**Produces:** A consequence chain to third order with feedback loops and a revised assessment of whether to proceed
**Chainable to:** `inversion` (to identify which second-order effects become failure modes), `reversibility` (to assess how locked in the decision becomes once second-order effects activate)

