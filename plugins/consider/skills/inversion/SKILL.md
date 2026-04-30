---
name: inversion
description: Solve problems backwards by identifying what would guarantee failure — use when direct optimization feels stuck or failure modes are unclear
argument-hint: "[goal or outcome to achieve]"
user-invocable: true
license: MIT
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

<example>
## Inversion Analysis: Developer Platform Launch

### Desired Outcome
Launch an internal developer platform adopted by 80% of engineering teams within 6 months.

### Guaranteed Failure Modes
1. Build without talking to teams about their actual pain points — likelihood: high, severity: high
2. Require migration from existing tools on day one — likelihood: medium, severity: high
3. No documentation or onboarding path — likelihood: medium, severity: medium
4. Platform team operates in isolation, slow to fix bugs — likelihood: medium, severity: high
5. Mandate adoption top-down without demonstrating value — likelihood: high, severity: medium
6. Over-engineer for future scale instead of solving current problems — likelihood: medium, severity: medium

### Avoidance Strategies
| Failure Mode | Avoidance Strategy |
|-------------|-------------------|
| Build without input | Interview 5 teams before writing code; co-design with 2 pilot teams |
| Forced migration | Run alongside existing tools; migrate incrementally when platform proves faster |
| No docs | Onboarding guide ships with v1; pilot teams write the first tutorials |
| Slow bug response | Dedicated on-call rotation; SLA of 1 business day for blocking issues |
| Top-down mandate | Demo wins from pilot teams; let adoption spread organically before any mandates |
| Over-engineering | Ship MVP for the top 3 pain points only; add capabilities based on demand |

### Positive Plan
Start with pilot teams, solve their top 3 pain points, ship fast bug fixes, let results drive adoption. Documentation and incremental migration from day one.

### Blind Spots
We haven't considered what happens if pilot teams' pain points diverge significantly — the platform might fragment into team-specific solutions rather than a shared one.
</example>

## Key Instructions

- If all failure modes seem low-likelihood, explicitly ask what would have to be true for the plan to fail — most teams systematically underestimate operational risks.
- Does not substitute for direct planning; produces a failure-mode inventory to inform a positive plan.

## Anti-Pattern Guards

1. **Listing generic risks** — failure modes must be specific to the stated goal and context; "poor communication" is noise unless it maps to a concrete scenario.
2. **Stopping at failure identification** — inversion's value is the avoidance strategies and synthesized positive plan; always complete steps 5–7.

## Handoff

**Receives:** A goal or desired outcome the user wants to achieve
**Produces:** A ranked failure-mode inventory with avoidance strategies and a synthesized positive plan
**Chainable to:** `second-order` (to trace consequences of each failure mode), `first-principles` (to challenge whether the goal's assumptions are sound)

