---
description: Prioritize tasks and decisions by mapping urgency against importance
argument-hint: "[list of tasks, decisions, or competing priorities]"
---

<objective>
Sort competing demands into four quadrants based on urgency and importance.
Clarify what to do now, schedule, delegate, or eliminate. Prevents urgency
from crowding out what actually matters.
</objective>

<process>
1. List all tasks, decisions, or demands competing for attention
2. For each item, assess: Is it urgent? (time-sensitive, external deadline)
3. For each item, assess: Is it important? (contributes to goals, high impact)
4. Place each item in the appropriate quadrant
5. Define action for each quadrant (do/schedule/delegate/eliminate)
6. Identify items that feel urgent but aren't important (the trap)
7. Commit to specific next actions for quadrant 1 and 2 items
</process>

<output_format>
## Eisenhower Matrix: [Topic]

### Items to Prioritize
[Numbered list of all items]

### Matrix

|  | Urgent | Not Urgent |
|--|--------|-----------|
| **Important** | Q1: DO NOW | Q2: SCHEDULE |
| **Not Important** | Q3: DELEGATE | Q4: ELIMINATE |

### Quadrant Assignments
- **Q1 (Do Now):** [items]
- **Q2 (Schedule):** [items]
- **Q3 (Delegate):** [items]
- **Q4 (Eliminate):** [items]

### Key Insight
[What's crowding out the important-not-urgent work?]
</output_format>

<example>
## Eisenhower Matrix: Sprint Planning Priorities

### Items to Prioritize
1. Fix production login bug (users locked out)
2. Write Q2 architecture proposal (due in 3 weeks)
3. Review 4 pending pull requests
4. Update team wiki with onboarding docs
5. Respond to vendor demo scheduling emails
6. Refactor auth module (tech debt)

### Matrix

|  | Urgent | Not Urgent |
|--|--------|-----------|
| **Important** | Q1: Fix login bug | Q2: Architecture proposal, Refactor auth |
| **Not Important** | Q3: Vendor emails, PR reviews | Q4: Wiki updates |

### Quadrant Assignments
- **Q1 (Do Now):** Fix production login bug — users are blocked, revenue impact
- **Q2 (Schedule):** Architecture proposal (block 2hrs Thursday), Auth refactor (next sprint)
- **Q3 (Delegate):** Vendor emails (admin can schedule), PR reviews (assign to senior dev)
- **Q4 (Eliminate):** Wiki updates — onboarding isn't happening this quarter

### Key Insight
PR reviews feel urgent because notifications pile up, but they're not important enough to displace the architecture proposal. Batching reviews to end-of-day prevents them from fragmenting deep work on Q2 items.
</example>

<success_criteria>
- All items explicitly placed in exactly one quadrant
- Urgency and importance assessments are justified, not arbitrary
- Q2 items identified (these are most commonly neglected)
- At least one "urgency trap" identified (feels urgent, isn't important)
- Next actions are specific and time-bound for Q1 and Q2
</success_criteria>
