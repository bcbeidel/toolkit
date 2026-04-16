---
name: hanlons-razor
description: Interpret behavior charitably — attribute to mistakes before malice; use when behavior seems hostile or frustrating and an adversarial interpretation is forming
argument-hint: "[situation where someone's behavior seems problematic]"
user-invocable: true
---

<objective>
When faced with behavior that seems hostile, incompetent, or deliberately
harmful, consider simpler explanations first. Most apparent malice is
actually miscommunication, different priorities, lack of context, or honest
mistakes. Prevents adversarial framing from poisoning collaboration.
</objective>

<process>
1. Describe the behavior or situation that seems problematic
2. State the uncharitable interpretation (the "malice" reading)
3. Generate 3+ charitable alternative explanations
4. For each alternative, assess: is this plausible given available evidence?
5. Identify what information would distinguish between interpretations
6. Choose the most likely explanation given available evidence
7. Define the appropriate response based on the chosen interpretation
</process>

<output_format>
## Hanlon's Razor: [Topic]

### Situation
[The behavior or event that seems problematic]

### Uncharitable Interpretation
[The "malice" or "incompetence" reading]

### Charitable Alternatives
1. [Alternative explanation] — plausibility: high/medium/low
2. [Alternative explanation] — plausibility: high/medium/low
3. [Alternative explanation] — plausibility: high/medium/low

### Distinguishing Evidence
[What would you need to know to determine which interpretation is correct?]

### Most Likely Explanation
[The interpretation best supported by available evidence]

### Appropriate Response
[How to respond given the most likely explanation]
</output_format>

<example>
## Hanlon's Razor: PR Sitting Unreviewed for a Week

### Situation
You submitted a PR 7 days ago, pinged the assigned reviewer twice, and got no response. The reviewer has been merging other PRs during this time.

### Uncharitable Interpretation
The reviewer is deliberately ignoring your PR because they disagree with your approach and want to passively block it rather than give direct feedback.

### Charitable Alternatives
1. They're prioritizing PRs for the release deadline this week and yours isn't on the critical path — plausibility: high
2. They saw the PR, noted it was large (400+ lines), and keep deferring it for a time block they haven't found — plausibility: high
3. Your notification got buried — Slack/email volume means pings are easily missed — plausibility: medium

### Distinguishing Evidence
Check whether the PRs they've been reviewing are smaller or release-critical. Ask directly: "Is this a good time, or should I find another reviewer?" Their response will distinguish between "busy" and "avoiding."

### Most Likely Explanation
PR size + competing priorities. A 400-line PR requires 30-60 minutes of focused review. During a release crunch, that time block doesn't exist. The other merged PRs were likely small and fast.

### Appropriate Response
Break the PR into 2-3 smaller PRs if possible. Message the reviewer offering to walk through the changes in 15 minutes to reduce their review burden. If still no response after the offer, reassign to a different reviewer without resentment.
</example>

## Key Instructions

- Charitable interpretation does not mean ignoring evidence of genuine malice; it means exhausting more likely explanations first.
- Does not resolve the situation; produces a clearer interpretation framework and a recommended response approach.

## Anti-Pattern Guards

1. **Overriding clear evidence** — Hanlon's Razor applies before evidence, not against it; if malice is demonstrated, the razor doesn't apply.
2. **Using charity to avoid addressing patterns** — a repeated pattern of the same "mistake" may indicate intent; acknowledge when the charitable explanation stops being the most likely one.

## Handoff

**Receives:** A situation where someone's behavior seems problematic, hostile, or deliberately harmful
**Produces:** A structured alternatives analysis with distinguishing evidence and a recommended response
**Chainable to:** `consider` (to apply additional models), `map-vs-territory` (to check what assumptions are driving the uncharitable interpretation)

