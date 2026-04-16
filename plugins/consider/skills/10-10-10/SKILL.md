---
name: 10-10-10
description: Evaluate decisions by considering impact across three time horizons
argument-hint: "[decision you're weighing or struggling with]"
user-invocable: true
---

<objective>
Break through short-term emotional reactions by evaluating how a decision
will feel and matter at three time scales: 10 minutes, 10 months, and
10 years from now. Separates fleeting discomfort from lasting impact.
</objective>

<process>
1. State the decision clearly, including the options
2. For each option, assess: How will I feel about this in 10 minutes?
3. For each option, assess: How will this matter in 10 months?
4. For each option, assess: How will this matter in 10 years?
5. Identify where short-term and long-term assessments diverge
6. Determine which time horizon should carry the most weight
7. Make the decision that optimizes for the right time horizon
</process>

<output_format>
## 10-10-10 Analysis: [Topic]

### Decision
[What's being decided, including options]

### Time Horizon Assessment
| Option | 10 Minutes | 10 Months | 10 Years |
|--------|-----------|-----------|---------|
| A | [feeling/impact] | [feeling/impact] | [feeling/impact] |
| B | [feeling/impact] | [feeling/impact] | [feeling/impact] |

### Divergence Points
[Where short-term and long-term assessments conflict]

### Dominant Time Horizon
[Which time frame matters most for this decision, and why]

### Decision
[The choice, justified by the appropriate time horizon]
</output_format>

<example>
## 10-10-10 Analysis: Rewrite Legacy Billing System

### Decision
Option A: Rewrite the billing system from scratch in a modern stack.
Option B: Incrementally refactor the existing system module by module.

### Time Horizon Assessment
| Option | 10 Minutes | 10 Months | 10 Years |
|--------|-----------|-----------|---------|
| A (Rewrite) | Exciting — fresh start, modern tools | Painful — 6 months in, still not shipped, maintaining two systems | Either transformative (if it ships) or a cautionary tale (if it stalls) |
| B (Refactor) | Frustrating — same old codebase | Steady progress — 3 modules modernized, billing still works | Fully modernized system, no big-bang risk, but took longer |

### Divergence Points
10-minute excitement for the rewrite masks the 10-month reality: rewrites routinely take 2-3x estimated time, and the team must maintain the old system in parallel. The refactor feels worse now but avoids the dual-maintenance trap.

### Dominant Time Horizon
10 months — this is a business-critical system. The risk of a stalled rewrite leaving the team maintaining two billing systems for a year outweighs the long-term elegance argument.

### Decision
Incremental refactor (Option B). The 10-month horizon reveals that the rewrite's main appeal is emotional (fresh start) rather than practical. Refactoring delivers value continuously without betting on a single high-risk cutover.
</example>

