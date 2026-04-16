---
name: "Intake: Accept-Then-Interpret Before Routing Commitment"
description: "Accept the user's goal statement before committing to a routing decision; delaying commitment prevents compounding errors from early wrong assumptions, and showing the interpretation before acting improves mental model formation"
type: context
sources:
  - https://arxiv.org/abs/2602.07338
  - https://arxiv.org/abs/2304.06597
  - https://arxiv.org/abs/2401.14484
  - https://www.amazon.science/publications/ask-aspects-and-retrieval-based-hybrid-clarification-in-task-oriented-dialogue-systems
related:
  - docs/research/2026-04-11-ux-patterns-primitive-routing.research.md
  - docs/context/abstraction-gap-and-goal-vocabulary-scent.context.md
  - docs/context/intent-based-vs-model-routing-articulatory-distance.context.md
  - docs/context/wizard-vs-recommendation-routing-onboarding.context.md
  - docs/context/automation-bias-confidence-display-and-transparency-bounds.context.md
  - docs/context/intent-routing-convergent-pattern-five-steps.context.md
---

Two independent research lines converge on the same intake sequence: accept the user's free-text goal statement first, then surface the system's interpretation of it before routing commits. Systems that commit to a routing decision before surfacing their interpretation — "early tentative assumptions" — cause compounding errors that degrade performance by approximately 60%. Systems that show interpretation after accepting intent improve user mental model formation. The intervention that resolves both problems is identical: delay routing commitment, show interpretation, then act.

**Early routing commitment is the primary failure mode**

Liu et al. (2026, arXiv:2602.07338) studied intent mismatch in multi-turn LLM conversations. The paper identifies three triggering patterns for mismatch:
1. Users provide "underspecified, fragmented utterances relying on contextual pronouns and vague directives"
2. Systems make "early tentative assumptions" and lock in these interpretations across turns
3. Systems interpret user clarifications as confirmations rather than corrections

Figure 2 of the paper shows approximately 60% relative performance degradation between fully-specified and underspecified settings across diverse model sizes and families. A Mediator-Assistant framework that reconstructed ambiguous multi-turn inputs into explicit single-turn instructions before acting achieved approximately 20 percentage points of performance recovery (GPT-4o-mini: +20.3pp; average across models: ~20–24pp).

This maps directly to single-turn routing problems: a user states a vague goal ("I want to make sure nobody pushes to main without a review"), the system must reconstruct it into a clear primitive specification ("a hook that enforces a branch protection rule") without locking in wrong assumptions before the interpretation is confirmed.

**Accept-then-interpret improves mental models**

The CHI 2023 "What It Wants Me To Say" study (Liu & Sarkar et al., n=24) found that grounded abstraction matching — showing users how the system interprets their request in user-comprehensible terms — improved "end-users' understanding of the scope and capabilities of the code-generating model, helping users develop better mental models for crafting effective prompts." The mechanism: making the system's vocabulary legible to the user after an initial natural-language attempt, rather than requiring vocabulary knowledge as a precondition.

The intake sequence this implies:
1. Accept free-text goal description — no taxonomy knowledge required from the user
2. Construct the routing interpretation internally
3. Show the interpretation in user-goal vocabulary before acting ("Building this as a hook — a check that runs before each push")
4. Allow confirmation or correction
5. Route

**The single clarification question**

Amazon's ASK system (ACL 2025) provides empirical support for a bounded version of the clarification step: asking one targeted clarifying question when routing ambiguity is detected improved retrieval recall@5 by approximately 20% compared to direct routing without clarification. This is a narrower pattern than a full wizard — one question, triggered only when ambiguity is high, not a mandatory sequential flow. It is structurally the same as showing a routing interpretation and asking "is this right?" — a single checkpoint with low friction.

**The user-vocabulary constraint**

The accept-then-interpret pattern has a critical constraint: the interpretation shown to the user must use the user's goal vocabulary, not the system's primitive vocabulary. Bodonhelyi et al. (2024) found users preferred responses to their original stated intent 56.61% (GPT-3.5) and 53.50% (GPT-4) of the time, even when the system's reformulation was technically more accurate. Users resist having their words replaced by the system's vocabulary.

This means the interpretation step should show a routing label and brief description in goal terms — not restate the user's goal in different words. "Building this as a hook: a check that runs before each push" bridges system vocabulary to goal vocabulary. "You want to enforce branch protection by intercepting the push event" replaces the user's vocabulary — and based on the evidence, this reduces satisfaction even when it is correct.

**IBM Design Principles corroboration**

Weisz et al. (CHI 2024) articulate the same principle from the design side: "help the user craft effective outcome specifications" and "orient the user to generative variability." The IBM framework explicitly notes that trial-and-error dominates user behavior when vocabulary scaffolding is absent — confirming that unscaffolded intent intake, without showing interpretation, produces the same failure mode as early commitment.

**Takeaway**

Do not commit to a routing decision before surfacing the interpretation to the user. Early commitment without showing interpretation is the primary documented source of routing failure — it degrades performance ~60% when wrong assumptions compound. Show the routing interpretation as a brief goal-vocabulary label before acting. Allow correction at this point, not through a forced justification gate before the routing decision is made. A single targeted clarification question when ambiguity is high (not a multi-step wizard) is the evidence-backed clarification pattern.
