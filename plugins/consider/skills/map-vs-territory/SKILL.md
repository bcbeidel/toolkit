---
name: map-vs-territory
description: Recognize where your mental model diverges from reality — use when a plan or model is driving decisions and its assumptions haven't been stress-tested
argument-hint: "[situation where assumptions may not match reality]"
user-invocable: true
license: MIT
---

<objective>
Every mental model, plan, or abstraction is a map — a simplified
representation. The territory is reality. Identify where your map
diverges from the territory, what it leaves out, and where those
gaps could cause problems.
</objective>

<process>
1. State the mental model, plan, or abstraction being used
2. List what the model captures well (where map matches territory)
3. List what the model simplifies or abstracts away
4. List what the model ignores entirely
5. For each simplification and omission, assess: could this matter?
6. Identify the highest-risk gap between map and territory
7. Propose a way to verify the map against actual territory
</process>

<output_format>
## Map vs Territory: [Topic]

### The Map (current model)
[The mental model, plan, or abstraction in use]

### Where Map Matches Territory
- [Aspect that the model captures accurately]

### Where Map Simplifies
- [Aspect that's simplified] — risk: high/medium/low

### Where Map Is Blank
- [Aspect the model ignores entirely] — risk: high/medium/low

### Highest-Risk Gap
[The divergence most likely to cause problems]

### Reality Check
[How to verify the map against actual conditions]
</output_format>

<example>
## Map vs Territory: Sprint Velocity Predictions

### The Map (current model)
"Our team velocity is 40 story points per sprint, so this 120-point epic will take 3 sprints."

### Where Map Matches Territory
- Average velocity over the last 6 sprints is genuinely ~40 points
- Team composition hasn't changed recently
- The work is in a familiar domain (same service, similar features)

### Where Map Simplifies
- Velocity averages hide variance (actual range: 28-52 points) — risk: medium
- Story points assume uniform complexity, but this epic has an unfamiliar integration — risk: high
- "3 sprints" assumes no interruptions (production incidents, unplanned work) — risk: medium

### Where Map Is Blank
- The epic depends on an external team's API that isn't built yet — risk: high
- Two engineers have PTO overlapping in sprint 2 — risk: medium
- We've never estimated an epic this large as a single block before — risk: low

### Highest-Risk Gap
The external API dependency. Our velocity model assumes all work is within our control. If the external team delivers late, sprint 2 stalls regardless of our capacity.

### Reality Check
Ask the external team for their delivery date and confidence level. If they can't commit, re-sequence the epic to pull forward work that doesn't depend on their API. Adjust the estimate to 4-5 sprints to account for the dependency and PTO gaps.
</example>

## Key Instructions

- The goal is to find gaps before they cause failures, not to invalidate the model — a well-calibrated map with known limits is still useful.
- Does not update the model; produces a gap audit and a verification plan the user acts on.

## Anti-Pattern Guards

1. **Treating simplifications as failures** — all maps simplify; the question is whether the simplification matters for the decision at hand.
2. **Generating abstract gaps** — every gap must have a concrete risk statement ("if this gap is real, X could happen"), not just "this isn't modeled."

## Handoff

**Receives:** A mental model, plan, or abstraction the user is relying on for a decision
**Produces:** A three-zone gap audit (matches / simplifies / ignores) with the highest-risk divergence and a reality-check approach
**Chainable to:** `first-principles` (to rebuild from verified fundamentals), `second-order` (to trace consequences of the highest-risk gap)

