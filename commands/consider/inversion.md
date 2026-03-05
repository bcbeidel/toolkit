---
description: Solve problems backwards by identifying what would guarantee failure
argument-hint: "[goal or outcome to achieve]"
---

<objective>
Instead of asking "how do I succeed?", ask "what would guarantee failure?"
Identify the most likely failure modes, then design around avoiding them.
Often clearer than direct optimization.
</objective>

<process>
1. State the desired outcome clearly
2. Invert: "What would guarantee we fail at this?"
3. List 5-7 specific failure modes or anti-patterns
4. Rank failure modes by likelihood and severity
5. For each top failure mode, define an avoidance strategy
6. Synthesize avoidance strategies into a positive plan
7. Check: does the inverted plan cover the most dangerous scenarios?
</process>

<output_format>
## Inversion Analysis: [Topic]

### Desired Outcome
[What success looks like]

### Guaranteed Failure Modes
1. [Failure mode] — likelihood: high/medium/low, severity: high/medium/low
2. ...

### Avoidance Strategies
| Failure Mode | Avoidance Strategy |
|-------------|-------------------|
| [Mode 1] | [Strategy] |

### Positive Plan (from inversion)
[Synthesized plan that avoids all major failure modes]

### Blind Spots
[What failure modes might we be missing?]
</output_format>

<success_criteria>
- At least 5 specific failure modes identified (not generic)
- Failure modes ranked by both likelihood and severity
- Each avoidance strategy is concrete and actionable
- Positive plan follows logically from the avoidance strategies
- Blind spots section demonstrates intellectual honesty
</success_criteria>
