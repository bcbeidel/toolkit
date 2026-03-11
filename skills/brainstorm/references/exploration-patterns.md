---
name: Exploration Patterns
description: Divergent/convergent thinking scaffolds, question templates, and approach comparison format
---

# Exploration Patterns

Scaffolds for structured exploration. Use these patterns during the
Understand, Diverge, and Converge phases.

## Asking Questions

One question at a time. Prefer multiple-choice.

**Multiple-choice format:**
> How should [component] handle [scenario]?
> - **A)** [option] — [1-sentence tradeoff]
> - **B)** [option] — [1-sentence tradeoff]
> - **C)** Something else (describe)

**When open-ended is appropriate:**
- When the answer space is too large to enumerate
- When you need the user's domain expertise, not a design choice
- Keep it focused: "What does [term] mean in your context?" not
  "Tell me about your requirements"

## Exploring Approaches

Present 2-3 approaches with tradeoffs. Lead with your recommendation.

**Approach comparison format:**

| | Approach A: [Name] | Approach B: [Name] | Approach C: [Name] |
|---|---|---|---|
| **Summary** | 1-2 sentences | 1-2 sentences | 1-2 sentences |
| **Strengths** | Bullet list | Bullet list | Bullet list |
| **Weaknesses** | Bullet list | Bullet list | Bullet list |
| **Best when** | Condition | Condition | Condition |

> **Recommendation:** Approach [X] because [reason tied to user's
> stated constraints].

If you can only think of one approach, you haven't explored enough.
Push for at least two — even if one is "do nothing" or "simpler
alternative."

## Scope Decomposition

Flag oversized projects before deep-diving into details.

**Signals a project needs decomposition:**
- Request mentions 3+ independent subsystems
- Components have no runtime dependencies on each other
- Different teams or skills would own different pieces
- The spec would exceed ~2 pages if written as one document

**Decomposition response:**
> This looks like it has [N] independent pieces: [list]. I'd suggest
> brainstorming each one separately — they can be built in any order.
> Which should we start with?

## Convergence Checklist

Before moving from Converge to Write the Spec, confirm:

- [ ] User selected an approach (or a hybrid)
- [ ] Scope boundaries confirmed (must have / won't have)
- [ ] No open ambiguities about user intent
- [ ] Acceptance criteria are articulable (even if not yet written)
