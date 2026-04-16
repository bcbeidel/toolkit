---
name: one-thing
description: Identify the single highest-leverage action that makes everything else easier
argument-hint: "[goal or area where focus is needed]"
user-invocable: true
---

<objective>
Cut through complexity to find the one action that, if done, would make
everything else easier or unnecessary. Based on the focusing question:
"What's the ONE thing I can do, such that by doing it, everything else
becomes easier or unnecessary?"
</objective>

<process>
1. State the goal or area of focus
2. List all possible actions that could advance this goal
3. For each action, assess: does this make other actions easier or unnecessary?
4. Identify domino effects — which action unlocks the most subsequent progress?
5. Test the candidate: if ONLY this one thing gets done, was it worthwhile?
6. Define what "done" looks like for this one thing
7. Identify what to say "no" to in order to protect focus on the one thing
</process>

<output_format>
## One Thing Analysis: [Topic]

### Goal
[What we're trying to achieve]

### Candidate Actions
| Action | Domino Effect | Makes others easier? |
|--------|-------------|---------------------|
| [Action 1] | [What it unlocks] | Yes/Partially/No |
| [Action 2] | [What it unlocks] | Yes/Partially/No |

### The One Thing
[The single highest-leverage action]

### Definition of Done
[What completion looks like — specific and measurable]

### Say No To
[What to deprioritize to protect focus on the one thing]
</output_format>

<example>
## One Thing Analysis: Improving Developer Onboarding

### Goal
Reduce time-to-first-commit for new engineers from 2 weeks to 3 days.

### Candidate Actions
| Action | Domino Effect | Makes others easier? |
|--------|-------------|---------------------|
| Write comprehensive onboarding docs | New hires self-serve answers | Partially — still need environment to work |
| Fix the dev environment setup script | New hires have working code on day 1 | Yes — unblocks everything downstream |
| Assign onboarding buddies | New hires get personalized help | Partially — buddies still fight the broken setup |
| Create a "first task" ticket template | Clear first contribution path | Partially — useless if environment isn't working |
| Record architecture walkthrough video | Context available on-demand | No — doesn't unblock the setup bottleneck |

### The One Thing
Fix the dev environment setup script. Every other onboarding improvement assumes the new hire has a working environment. A broken setup script means buddies spend their time debugging Docker instead of teaching architecture, docs describe a system the new hire can't run, and first tasks can't be attempted.

### Definition of Done
A new hire can run `make setup` on a fresh laptop and have all services running with seed data in under 30 minutes. Tested by having someone outside the team follow the instructions.

### Say No To
Pause the architecture video project and the onboarding doc rewrite until setup works. Both are wasted effort if people can't run the code.
</example>

