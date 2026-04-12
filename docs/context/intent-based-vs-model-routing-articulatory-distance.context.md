---
name: "Intent-Based vs. Model-Based Routing and Articulatory Distance"
description: "Reducing articulatory distance — the burden of expressing intent — measurably improves routing success; automatic intent classification has a ~10% failure ceiling with systematic blind spots for rare primitives"
type: context
sources:
  - https://arxiv.org/abs/2310.03691
  - https://arxiv.org/abs/2402.02136
  - https://arxiv.org/abs/2401.14484
  - https://docs.github.com/en/actions/get-started/actions-vs-apps
  - https://www.sciencedirect.com/science/article/abs/pii/S1045926X16300982
related:
  - docs/research/2026-04-11-ux-patterns-primitive-routing.research.md
  - docs/context/abstraction-gap-and-goal-vocabulary-scent.context.md
  - docs/context/automation-bias-confidence-display-and-transparency-bounds.context.md
  - docs/context/intake-acceptance-before-routing-commitment.context.md
  - docs/context/intent-routing-convergent-pattern-five-steps.context.md
---

Intent-based routing accepts a user's goal in natural language and infers the correct primitive. Model-based routing presents the system's primitive model and asks users to self-match. The empirical case for preferring intent-based intake is strongest for novice users through articulatory distance: any design that reduces the burden of expressing intent improves task success. The failure mode of intent-based routing — silent misclassification of ~10% of cases with systematic blind spots for rare primitives — constrains how it should be implemented.

**Articulatory distance is the empirical anchor**

DirectGPT (Masson et al., CHI 2024, n=12 within-subject) provides the most rigorous empirical comparison of intent specification modes. Users who could express intent through direct manipulation (selecting objects + applying operations from a toolbar) versus free-text natural language prompts showed:
- 50% faster task completion (56s vs. 117s)
- ~25% higher success rate (M=4.84 vs. M=3.89 on a 5-point scale, p<0.001)
- 72% fewer words per prompt (5.83 vs. 19.98 words)
- 50% fewer prompts required (M=1.90 vs. M=3.67)

The authors attribute the gains to reduced "articulatory distance" — the gap between intended action and how it must be expressed — and reduced "semantic distance" — the verbosity required to convey intent. Model-based routing that asks users to match their goals against technical primitive descriptions imposes articulatory distance: users must translate their internal goal into the system's vocabulary before they can express it. Intent-based intake that accepts goal descriptions in natural language eliminates this translation step.

Participant P5: "[DirectGPT] was more like a tool. I did not need to make it comprehend anything."

**The ~10% failure ceiling**

Automatic intent classification cannot be assumed to work correctly for all users. Bodonhelyi et al. (2024, user study examining GPT-3.5 and GPT-4) measured:
- GPT-4 intent recognition accuracy: 89.64% (F1: 88.84%)
- GPT-3.5 intent recognition accuracy: 75.28% (F1: 74.28%)

Even at GPT-4 performance, ~1 in 10 users is misrouted. The failure distribution is not uniform: systematic blind spots exist for rare or ambiguous categories. "Learning support" intent had 0% recognition by GPT-4 (GPT-3.5: 36.84%). "Curricular planning" intent had 0% recognition by GPT-4 (GPT-3.5: 50%). The categories with worst performance are exactly the rare categories — the primitives used least frequently in a system are the most likely to be systematically misclassified.

For a developer tool with five primitives where one ("subagent") is used far less frequently than others, intent classification will fail most often precisely for subagent requests. Silent auto-routing without confidence signaling will misroute these users invisibly.

**Industry default is model-based, but not by design validation**

GitHub's documentation for the Actions/Apps routing problem — one of the most referenced real-world two-primitive routing decisions — uses model-based routing: it explains technical characteristics ("Apps run persistently; Actions don't require persistent infrastructure") and asks users to self-match. No intake question, no decision tree, no wizard flow.

This is the dominant industry pattern, but not because it has been validated against intent-based alternatives. It reflects historical default — model-based routing requires no AI classification. The absence of intent-based routing in existing developer tool documentation is not evidence of efficacy.

**The expert-user counter-evidence**

Pot et al. (JVLC 2016, iterative design + user study on social robot APIs) found empirically that an initial high-abstraction API — which hid model details to reduce user burden — had to be revised to a *lower* abstraction level after user study found it "took away too much control from programmers." This is a direct case where exposing more of the model outperformed hiding it, for expert-level users who needed to validate and debug their configurations.

The IBM Design Principles for Generative AI (Weisz et al., CHI 2024) note that "orient the user to generative variability" — making system capability boundaries visible — is a necessary design principle. Pure intent-based routing that exposes no model internals leaves users unable to form accurate expectations about what the system can and cannot do.

**Takeaway**

Accept natural language goal statements at intake — this reduces articulatory distance and is the strongest argument for intent-based routing. But plan for the ~10% failure ceiling: rare primitives will be systematically misclassified, and silent auto-routing will fail these users invisibly. Surface confidence state when routing certainty is low, and ensure the rare primitives in the system receive extra handling, not less. Model-based routing is the historical default, not the validated optimum.
