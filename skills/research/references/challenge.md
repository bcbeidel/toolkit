# Challenge Reference

Used during Phase 6 (Challenge). Three sub-steps applied based on
research mode:

| Mode | Assumptions | ACH | Premortem |
|------|-------------|-----|----------|
| deep-dive, feasibility, competitive, options | Yes | Yes | Yes |
| landscape, technical, historical, open-source | Yes | No | Yes |

## Assumptions Check (All Modes)

1. List 3-5 key assumptions underlying emerging findings
2. For each: what evidence supports it? contradicts it? impact if false?
3. Flag assumptions with weak or no supporting evidence

Output format:

| Assumption | Supporting Evidence | Counter-Evidence | Impact if False |
|------------|-------------------|------------------|-----------------|
| [assumption] | [evidence for] | [evidence against] | [impact] |

## Analysis of Competing Hypotheses (Mode-Conditional)

Triggered for: deep-dive, options, competitive, feasibility.

1. Generate 3+ hypotheses including at least one contradicting your emerging finding. Anti-anchoring: ask "What would someone who disagrees propose?" and add it.
2. Rate each evidence item against each hypothesis: **C** (consistent), **I** (inconsistent), **N** (neutral).
3. Select the hypothesis with fewest inconsistencies (not most consistencies).

Output format:

| Evidence | Hypothesis A | Hypothesis B | Hypothesis C |
|----------|-------------|-------------|-------------|
| [evidence] | C | I | N |
| Inconsistencies | 1 | 1 | 0 |

Selected: [Hypothesis] — fewest inconsistencies. Rationale: [why].

## Premortem (All Modes)

1. Assume the main conclusion is wrong
2. Generate 3 reasons why: overweighted evidence? missing perspective? what could change?
3. Assess plausibility (high/medium/low) and whether conclusion needs qualifying

Output format:

| Failure Reason | Plausibility | Impact on Conclusion |
|----------------|-------------|---------------------|
| [reason] | medium | Qualifies finding #2 |
