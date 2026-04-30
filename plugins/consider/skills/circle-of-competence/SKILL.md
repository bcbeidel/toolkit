---
name: circle-of-competence
description: Scope decisions by distinguishing what you know well from what you don't — use when expertise boundaries are uncertain or a decision requires knowledge outside your direct experience
argument-hint: "[domain or decision where expertise boundaries matter]"
user-invocable: true
license: MIT
---

<objective>
Map the boundary between what you genuinely understand and what you only
think you understand. Make better decisions by staying within your circle
where possible, and explicitly flagging when you're operating outside it.
</objective>

<process>
1. Define the decision or domain being evaluated
2. List what you know well from direct experience (inside the circle)
3. List what you know about from reading but haven't practiced (the edge)
4. List what you don't know or are guessing about (outside the circle)
5. For the decision at hand, which zones does it require knowledge from?
6. For areas outside your circle, identify who has that competence
7. Decide: stay in circle, expand the circle, or bring in expertise
</process>

<output_format>
## Circle of Competence: [Topic]

### Domain
[The decision or area being evaluated]

### Inside (know well)
- [Area of genuine expertise — from direct experience]

### Edge (familiar but not deep)
- [Area where you have knowledge but not mastery]

### Outside (don't know)
- [Area where you're guessing or relying on assumptions]

### Decision Requirements
[Which zones does this decision touch?]

### Strategy
[Stay inside / expand the circle / bring in outside expertise]
</output_format>

<example>
## Circle of Competence: Should Our Backend Team Build the Mobile App?

### Domain
Deciding whether our team of 3 backend engineers should build the iOS/Android app ourselves or hire specialists.

### Inside (know well)
- REST API design and backend infrastructure
- PostgreSQL performance tuning and data modeling
- CI/CD pipelines and production monitoring
- Python and Go ecosystem

### Edge (familiar but not deep)
- React Native (one engineer did a tutorial project)
- Mobile app architecture patterns (read about MVVM, never shipped it)
- App Store submission process (know it exists, never done it)

### Outside (don't know)
- iOS/Android platform-specific performance optimization
- Mobile-specific UX patterns (gesture navigation, offline-first)
- App Store review guidelines and rejection recovery
- Push notification infrastructure at scale

### Decision Requirements
Building the mobile app requires deep knowledge in all three zones. API integration is inside our circle, but the entire frontend layer — UI, platform APIs, store submission — is outside it.

### Strategy
Bring in outside expertise. Hire or contract a mobile developer for the app shell and platform integration. Our team owns the API layer and backend (inside our circle). The mobile specialist handles what we'd spend months learning poorly. Review architecture decisions together so knowledge transfers over time.
</example>

## Key Instructions

- If the user has no relevant experience to assess, help them identify who does before mapping the circle.
- Does not evaluate whether a decision is worth making; only maps competence boundaries relative to it.
- Does not apply to pure preference questions where competence is irrelevant.

## Anti-Pattern Guards

1. **Confusing familiarity with competence** — reading about a topic places it on the edge, not inside the circle; direct practice is the threshold.
2. **Using the model to justify avoidance** — the goal is calibrated scope, not permission to stay comfortable; sometimes the right answer is to expand the circle.

## Handoff

**Receives:** A domain or decision where expertise boundaries affect the outcome
**Produces:** A three-zone competence map (inside / edge / outside) with a recommended strategy
**Chainable to:** `consider` (to apply additional mental models), `opportunity-cost` (to evaluate the cost of staying in vs. expanding the circle)

