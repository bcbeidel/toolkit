---
name: "Abstraction Gap and Goal-Vocabulary Scent"
description: "Users describe goals in different vocabulary than system primitives; surfacing the system's interpretation in user-goal language — not asking users to name a primitive — is the intervention that closes the gap"
type: context
sources:
  - https://arxiv.org/abs/2304.06597
  - https://arxiv.org/abs/2401.14484
  - https://ixdf.org/literature/book/the-glossary-of-human-computer-interaction/information-foraging-theory
  - https://dl.acm.org/doi/10.1145/2430545.2430551
  - https://www.nngroup.com/articles/progressive-disclosure/
related:
  - docs/research/2026-04-11-ux-patterns-primitive-routing.research.md
  - docs/context/intent-based-vs-model-routing-articulatory-distance.context.md
  - docs/context/intake-acceptance-before-routing-commitment.context.md
  - docs/context/intent-routing-convergent-pattern-five-steps.context.md
---

The abstraction gap is the structural vocabulary mismatch between how users describe their goals and the vocabulary the system requires to act on them. The CHI 2023 study "What It Wants Me To Say" (Liu et al., n=24 between-subjects) established this as a named phenomenon: "only a small portion of the infinite space of naturalistic utterances is effective at guiding code generation." This is not a user skill problem — it is a predictable structural divergence between goal language ("prevent pushes to main without review") and primitive vocabulary ("hook," "rule," "workflow"). The gap applies directly to any developer tool with a primitive taxonomy users must learn before they can select correctly.

**Why vocabulary mismatch causes routing failure**

Information Foraging Theory (Pirolli & Card; applied to SE tools by Fleming et al., TOSEM) provides the causal model: users evaluate information paths before committing effort based on "information scent" — the degree to which visible labels and cues predict whether a path leads to their goal. When intake labels use system-abstraction vocabulary rather than user-goal vocabulary, scent is absent. Users cannot predict which primitive path leads to what they want without already knowing the answer. The result is exploratory browsing — trial-and-error navigation — rather than targeted selection.

Concrete application: an intake screen showing "Select a primitive: skill / command / hook / rule / subagent" provides zero information scent to a user who does not know these terms. The same five options presented as "Add new behavior to Claude / Create a reusable command / Enforce a check automatically / Set a persistent rule / Delegate a background task" provide scent — users can match their goal vocabulary against the option vocabulary without knowing the underlying taxonomy.

**The grounded abstraction matching intervention**

The CHI 2023 paper's proposed solution was "grounded abstraction matching": translating the system's output back into systematic, predictable naturalistic utterance — showing users how the system interprets their request in terms they can evaluate. In the study, this approach "improved end-users' understanding of the scope and capabilities of the code-generating model, helping users develop better mental models for crafting effective prompts."

This establishes a specific intake sequence that outperforms both silent routing and upfront option lists:
1. Accept free-text goal description from the user
2. Show the system's interpretation of the goal mapped to its taxonomy ("Building this as a hook — a check that runs before each push")
3. Allow the user to confirm or correct before acting

The IBM Design Principles for Generative AI (Weisz et al., CHI 2024) corroborate: systems must "help the user craft effective outcome specifications" and "build upon the user's existing mental models" — not require users to learn system vocabulary before they can express intent. Trial-and-error becomes the dominant behavior pattern when vocabulary scaffolding is absent.

**The progressive disclosure constraint**

NN/g's progressive disclosure synthesis identifies a hard constraint: systems with three or more abstraction levels "typically create usability problems." Hick-Hyman Law applies at maximum strength when users lack a mental model — decision time increases logarithmically with option count. A user who does not know what "hook," "rule," and "subagent" mean faces maximum cognitive friction when presented with all five primitives simultaneously. Hiding lower-frequency primitives and surfacing only the most common ones at intake reduces this friction; progressive disclosure is effective for this initial exposure.

**The expert-user boundary condition**

The abstraction gap intervention is scoped to users without an existing mental model of the system's primitive vocabulary. Expert developers face an inverse problem: fully opaque intent routing removes their ability to validate routing decisions or debug unexpected behavior. A 2025 elicitation study (Koenemann et al., IJHCS, n=56 developers, 8 workshops) found experts needed on-demand access to model internals, not progressive-reveal flows designed for novices. Experts found automatic explanation generation "obnoxious or even 'outrageous.'"

The design implication: the abstraction gap pattern applies at intake for all users, but expert users need an escape valve — on-demand access to the routing decision and model vocabulary — rather than being forced through a vocabulary-bridging flow once they already know the primitives.

**Takeaway**

Use user-goal vocabulary in intake labels to provide information scent. When routing, show the system's interpretation as a brief routing label in user-goal language — not a prompt reformulation, not a primitive name alone. Close the vocabulary gap at interpretation time, not at selection time. Forcing users to select from a primitive list before routing is the highest-friction design available to a system whose users don't know the taxonomy.
