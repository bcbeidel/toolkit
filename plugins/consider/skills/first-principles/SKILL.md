---
name: first-principles
description: Break down assumptions and rebuild reasoning from fundamental truths — use when a standard approach feels wrong or produces diminishing returns but no one has questioned its underlying assumptions
argument-hint: "[problem or system to deconstruct]"
user-invocable: true
license: MIT
---

<objective>
Deconstruct a problem into its most basic, foundational elements. Strip away
assumptions, conventions, and analogies. Rebuild understanding from verified
fundamentals to find novel solutions.
</objective>

<process>
1. State the problem or system clearly in one sentence
2. List every assumption embedded in the current approach
3. Challenge each assumption — is it a fundamental truth or a convention?
4. Identify the bedrock truths that remain after challenges
5. Rebuild a solution from only those verified fundamentals
6. Compare the rebuilt solution to the conventional approach
7. Identify what the conventional approach gets wrong or misses
</process>

<output_format>
## First-Principles Analysis: [Topic]

### Problem Statement
[One clear sentence]

### Assumptions Identified
- [Assumption 1] — fundamental / convention / unverified
- [Assumption 2] — ...

### Fundamental Truths
1. [Verified truth that survived challenge]
2. ...

### Rebuilt Reasoning
[Solution constructed from fundamentals only]

### Key Insight
[What changes when you reason from fundamentals vs convention]
</output_format>

<example>
## First-Principles Analysis: Monolith vs Microservices

### Problem Statement
Our team assumes we need microservices because we're scaling, but deploys are slow and coordination costs are high.

### Assumptions Identified
- Microservices improve scalability — convention (monoliths scale vertically too)
- Independent deploys are faster — convention (coordination overhead can negate this)
- Our team is big enough to own separate services — unverified (we have 4 engineers)
- Network calls between services are negligible — unverified (latency adds up)

### Fundamental Truths
1. We need to deploy changes without breaking unrelated features
2. Our current bottleneck is deploy pipeline speed, not runtime scaling
3. Four engineers cannot maintain more than 2-3 independent services effectively

### Rebuilt Reasoning
A modular monolith with clear internal boundaries gives us deploy isolation (via feature flags and targeted rollouts) without the coordination cost of service boundaries. Split only when a module's scaling needs diverge measurably from the rest.

### Key Insight
The assumption "scaling = microservices" skipped the question "what are we actually scaling?" Our bottleneck is deploy speed, not request throughput — a problem microservices make worse, not better.
</example>

## Key Instructions

- If all assumptions survive challenge, note that the conventional approach may already be optimal — first-principles doesn't always produce a novel solution.
- Does not generate solutions from scratch; produces a framework for rebuilding reasoning once fundamentals are verified.

## Anti-Pattern Guards

1. **Rebuilding from convention** — stripping away a convention only to rebuild the same approach is the common failure; the rebuilt solution must trace to verified fundamentals, not intuition.
2. **Mistaking "feels fundamental" for "is fundamental"** — a fundamental truth is verifiable, not just hard to argue with; apply the same skepticism to proposed fundamentals as to assumptions.

## Handoff

**Receives:** A problem or system the user wants to deconstruct and reason about from fundamentals
**Produces:** An assumptions audit, verified fundamentals, and a rebuilt solution compared against the conventional approach
**Chainable to:** `inversion` (to stress-test the rebuilt solution), `consider` (to apply additional mental models)

