---
description: Assess decision risk by classifying as one-way or two-way door
argument-hint: "[decision to evaluate for reversibility]"
---

<objective>
Not all decisions carry equal risk. Two-way doors (easily reversible) should
be made quickly with less analysis. One-way doors (hard to reverse) deserve
careful deliberation. Classify the decision to calibrate the right amount
of analysis.
</objective>

<process>
1. State the decision being considered
2. Assess: if this goes wrong, can we undo it? At what cost?
3. Classify as one-way door (irreversible) or two-way door (reversible)
4. If two-way: identify the rollback path and its cost
5. If one-way: identify what makes it irreversible and the blast radius
6. Calibrate analysis effort to the door type
7. If one-way, identify partial reversibility or ways to reduce commitment
</process>

<output_format>
## Reversibility Analysis: [Topic]

### Decision
[What's being decided]

### Classification: [One-Way Door / Two-Way Door]

### Reversibility Assessment
- **Can it be undone?** [Yes/Partially/No]
- **Cost to reverse:** [Low/Medium/High/Impossible]
- **Time to reverse:** [Minutes/Days/Months/Never]
- **Blast radius:** [Self/Team/Organization/Public]

### If Two-Way Door
- **Rollback path:** [How to undo]
- **Recommendation:** Decide quickly, course-correct later

### If One-Way Door
- **What makes it irreversible:** [Specific factors]
- **Ways to reduce commitment:** [Pilot, phase, or partial approach]
- **Recommendation:** Analyze thoroughly before committing
</output_format>

<success_criteria>
- Classification is justified with specific reasoning, not gut feel
- Cost, time, and blast radius of reversal are all assessed
- Two-way doors get a bias toward action (not over-analysis)
- One-way doors get suggestions for reducing irreversibility
- Recommendation matches the classification (fast for 2-way, careful for 1-way)
</success_criteria>
