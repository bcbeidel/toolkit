---
description: Assess decision risk by classifying as one-way or two-way door
metadata:
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

<example>
## Reversibility Analysis: Choosing a Database for the Events Service

### Decision
Use PostgreSQL vs DynamoDB for a new event-sourcing service.

### Classification: One-Way Door

### Reversibility Assessment
- **Can it be undone?** Partially — data can be migrated, but schema design and query patterns are deeply coupled
- **Cost to reverse:** High — rewriting data access layer, migrating data, revalidating correctness
- **Time to reverse:** Months (data migration + regression testing + gradual cutover)
- **Blast radius:** Team — affects the events team and all downstream consumers of the event stream

### If One-Way Door
- **What makes it irreversible:** Query patterns, schema design, and operational tooling all become database-specific within weeks. After 6 months of production data, migration becomes a project in itself.
- **Ways to reduce commitment:** Start with a repository abstraction layer so business logic doesn't call database APIs directly. Build for PostgreSQL first (team knows it), but keep the option to swap the storage backend if DynamoDB's scaling becomes necessary.
- **Recommendation:** Analyze thoroughly. Default to PostgreSQL (known quantity, team expertise, adequate for projected scale). Revisit DynamoDB only if event volume exceeds 50K/sec — a threshold we're unlikely to hit in year one.
</example>

