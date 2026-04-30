---
name: opportunity-cost
description: Evaluate what you give up by choosing one option over alternatives — use when a decision is being made without explicitly naming the best alternative foregone
argument-hint: "[decision with multiple options to compare]"
user-invocable: true
license: MIT
---

<objective>
Make the hidden cost of every choice explicit. When you choose option A,
the real cost isn't just what A costs — it's the best alternative you gave
up. Prevents tunnel vision on the chosen path.
</objective>

<process>
1. State the decision and the option currently favored
2. List all viable alternatives (including "do nothing")
3. For each alternative, estimate the value it would provide
4. Identify the best alternative — this is the opportunity cost
5. Compare: does the favored option exceed its opportunity cost?
6. Check for hidden costs not captured in the direct comparison
7. State the decision with opportunity cost made explicit
</process>

<output_format>
## Opportunity Cost Analysis: [Topic]

### Decision
[What's being decided]

### Options
| Option | Direct Value | Direct Cost | Key Tradeoff |
|--------|-------------|-------------|-------------|
| A (favored) | ... | ... | ... |
| B | ... | ... | ... |
| Do nothing | ... | ... | ... |

### Opportunity Cost
[Best alternative foregone and its estimated value]

### Hidden Costs
- [Cost not captured in direct comparison]

### Verdict
[Does the favored option justify its opportunity cost?]
</output_format>

<example>
## Opportunity Cost Analysis: Build vs Buy Authentication

### Decision
Whether to build a custom auth system or use Auth0.

### Options
| Option | Direct Value | Direct Cost | Key Tradeoff |
|--------|-------------|-------------|-------------|
| A: Build custom | Full control, no vendor dependency | 3 engineer-months, ongoing maintenance | Time to market vs control |
| B: Auth0 | Ships in 1 week, managed security patches | $1,200/month, vendor lock-in | Cost vs speed |
| Do nothing | No cost | Users can't log in — not viable | — |

### Opportunity Cost
If we build custom, we forgo 3 engineer-months of product work. At our current pace, that's the entire notifications feature our top 5 customers are waiting for. The opportunity cost isn't $0 — it's the revenue risk of delaying notifications by a quarter.

### Hidden Costs
- Custom auth requires ongoing security patching — not a one-time build
- Auth0 lock-in means switching later requires re-implementing session management
- Custom auth expertise leaves with the engineer who built it

### Verdict
Auth0 justified. The opportunity cost of building (delayed notifications = revenue risk) exceeds Auth0's dollar cost by roughly 10x. Revisit only if we outgrow Auth0's pricing tier or need auth behavior they can't support.
</example>

## Key Instructions

- Always include "do nothing" as an alternative — it is the most frequently overlooked option and often has the clearest opportunity cost.
- Does not make the decision; produces a comparison that makes the tradeoff explicit so the user can decide.

## Anti-Pattern Guards

1. **Comparing against only weak alternatives** — opportunity cost is the value of the best alternative, not a convenient one; include the strongest realistic option.
2. **Omitting hidden costs** — direct dollar or time comparisons miss ongoing costs (maintenance, lock-in, expertise loss); step 6 must be completed, not skipped.

## Handoff

**Receives:** A decision with a favored option and at least one realistic alternative
**Produces:** An option comparison table with opportunity cost named explicitly and a verdict
**Chainable to:** `reversibility` (to assess how locked in the favored choice is), `second-order` (to trace downstream effects of the foregone alternative)

