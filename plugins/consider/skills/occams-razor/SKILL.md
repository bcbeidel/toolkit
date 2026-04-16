---
name: occams-razor
description: Find the simplest explanation or solution that accounts for all known facts — use when there are multiple competing explanations and the simplest hasn't been tried first
argument-hint: "[phenomenon or problem with multiple possible explanations]"
user-invocable: true
---

<objective>
Among competing explanations, identify the one that makes the fewest
assumptions while still accounting for all observed evidence. Prefer
simplicity, but not at the cost of explanatory power.
</objective>

<process>
1. State the phenomenon or problem requiring explanation
2. List all known facts and observations that must be explained
3. Generate 3-5 candidate explanations of varying complexity
4. For each candidate, count the assumptions required
5. Check each candidate against all known facts — does it account for everything?
6. Select the simplest explanation that fits all facts
7. Identify what new evidence would distinguish between candidates
</process>

<output_format>
## Occam's Razor Analysis: [Topic]

### Observations to Explain
- [Fact 1]
- [Fact 2]

### Candidate Explanations
| Explanation | Assumptions | Fits all facts? |
|-------------|------------|----------------|
| [Simple] | N | Yes/No |
| [Complex] | N | Yes/No |

### Simplest Sufficient Explanation
[The winner and why]

### Distinguishing Evidence
[What would confirm or rule out alternatives]
</output_format>

<example>
## Occam's Razor Analysis: API Response Time Increase

### Observations to Explain
- P95 latency increased from 200ms to 800ms last Tuesday
- No code deployments that day
- Database CPU is normal
- Only affects the /search endpoint
- Traffic volume unchanged

### Candidate Explanations
| Explanation | Assumptions | Fits all facts? |
|-------------|------------|----------------|
| Search index corrupted | 1 (index can silently corrupt) | Yes |
| Upstream provider slowed down | 1 (provider had an incident) | Yes — /search calls external API |
| DNS resolution intermittent | 2 (DNS issue + only affects one endpoint) | Partial — why only /search? |
| Memory leak in search service | 2 (leak exists + triggered Tuesday) | Partial — would worsen over time |

### Simplest Sufficient Explanation
Upstream search provider experienced degradation. This requires only one assumption (provider incident), explains why only /search is affected (it's the only endpoint calling that provider), and fits the Tuesday timing without needing a code change.

### Distinguishing Evidence
Check the provider's status page for Tuesday incidents. If clean, run `curl` directly against the provider API to measure current latency. If provider is fast, re-examine the search index.
</example>

## Key Instructions

- A simpler explanation that doesn't account for all known facts is not Occam's Razor — it's an incomplete explanation; simplicity cannot come at the cost of explanatory coverage.
- Does not prescribe investigation steps; identifies the most parsimonious explanation to test first.

## Anti-Pattern Guards

1. **Discarding evidence to achieve simplicity** — the simplest explanation must fit all known facts; simplifying by ignoring inconvenient observations is not Occam's Razor.
2. **Conflating common with simple** — a common explanation requires fewer assumptions only if its commonness doesn't itself require additional assumptions to explain.

## Handoff

**Receives:** A phenomenon or problem with multiple possible explanations and a set of known observations
**Produces:** A ranked candidate explanation table with the simplest sufficient explanation and distinguishing evidence
**Chainable to:** `5-whys` (to drill into the chosen explanation's root cause), `map-vs-territory` (to check whether the observations themselves are accurate)

