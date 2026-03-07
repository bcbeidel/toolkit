---
description: Apply the 80/20 rule to find the highest-leverage inputs
argument-hint: "[area where effort and results feel misaligned]"
---

<objective>
Identify the vital few inputs that drive the majority of results. In most
systems, roughly 20% of causes produce 80% of effects. Find that 20% and
focus there for maximum leverage.
</objective>

<process>
1. Define the desired outcome or metric to optimize
2. List all inputs, activities, or factors that contribute to the outcome
3. Estimate each input's contribution to the total result
4. Rank inputs by contribution (highest first)
5. Identify the ~20% of inputs producing ~80% of results
6. For each high-leverage input, ask: can we do more of this?
7. For each low-leverage input, ask: can we reduce or eliminate this?
</process>

<output_format>
## Pareto Analysis: [Topic]

### Outcome to Optimize
[What we're trying to maximize or minimize]

### Input-to-Outcome Mapping
| Input | Est. Contribution | Cumulative |
|-------|------------------|-----------|
| [Top input] | X% | X% |
| [Next] | Y% | X+Y% |
| ... | ... | ... |

### Vital Few (the 20%)
- [High-leverage input 1]: amplify by [specific action]
- [High-leverage input 2]: amplify by [specific action]

### Trivial Many (candidates for reduction)
- [Low-leverage input]: reduce/eliminate because [reason]

### Recommended Focus Shift
[Where to redirect effort for maximum impact]
</output_format>

<example>
## Pareto Analysis: Reducing Support Ticket Volume

### Outcome to Optimize
Reduce monthly support tickets from 500 to under 200.

### Input-to-Outcome Mapping
| Input | Est. Contribution | Cumulative |
|-------|------------------|-----------|
| Password reset issues | 35% | 35% |
| Confusing billing page | 25% | 60% |
| API error messages unclear | 15% | 75% |
| Feature requests misfiled as bugs | 10% | 85% |
| Onboarding confusion | 8% | 93% |
| Account deletion requests | 4% | 97% |
| Other | 3% | 100% |

### Vital Few (the 20%)
- Password resets: add self-service reset flow (currently requires support ticket to trigger)
- Billing page: redesign the plan comparison table — 80% of billing tickets ask "what's the difference between plans?"

### Trivial Many (candidates for reduction)
- Feature requests as bugs: not worth building a routing system for 10% of volume
- Account deletion: low volume, legally required to handle manually anyway

### Recommended Focus Shift
Two changes (self-service password reset + billing page redesign) would eliminate ~60% of tickets. Everything else combined is less impactful than either of these alone. Start with password reset — it's a weekend project with the highest single-category impact.
</example>

<success_criteria>
- Inputs are specific and enumerable, not vague categories
- Contribution estimates are grounded in evidence or reasoning
- Clear separation between vital few and trivial many
- Amplification strategies are concrete and actionable
- Focus shift recommendation is specific to the situation
</success_criteria>
