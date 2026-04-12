---
name: "Wizard vs. Recommendation Routing in Developer Onboarding"
description: "Recommendation-based routing (infer intent, propose, confirm) has 23× more research support than wizard-based routing in developer onboarding; a single targeted clarification question when ambiguity is high improves routing accuracy ~20%"
type: context
sources:
  - https://arxiv.org/abs/2408.15989
  - https://www.amazon.science/publications/ask-aspects-and-retrieval-based-hybrid-clarification-in-task-oriented-dialogue-systems
  - https://www.nngroup.com/articles/wizards/
  - https://arxiv.org/abs/2502.02194
related:
  - docs/research/2026-04-11-ux-patterns-primitive-routing.research.md
  - docs/context/intake-acceptance-before-routing-commitment.context.md
  - docs/context/automation-bias-confidence-display-and-transparency-bounds.context.md
  - docs/context/intent-routing-convergent-pattern-five-steps.context.md
---

The most evidence-backed onboarding routing pattern is recommendation-based (infer need from stated goal, propose a route, allow confirmation), not wizard-based (sequential question-and-answer). A systematic literature review of 32 onboarding studies found recommendation systems in 23 of 32 studies — wizard-style routing received minimal research attention. This is primarily an absence-of-evidence finding for wizards rather than evidence of wizard failure, but the asymmetry in research support is significant: when selecting a routing pattern, the recommendation approach has substantially more backing.

**The SLR evidence**

Santos et al. (2024, arXiv:2408.15989) conducted a systematic literature review of 32 studies on software onboarding solutions. Key findings:
- Recommendation systems were the "most prevalent strategy": 23 of 32 studies examined recommendation-based approaches — proactive, personalized suggestions based on inferred need
- Wizard-style sequential routing received minimal research attention (fewer than 2 of 32 studies)
- 71% of studies used laboratory experiments; 50% used quantitative metrics (success rates, completion times, satisfaction)
- Only 18 of 58 identified newcomer barriers are addressed by existing software solutions

The recommendation pattern in onboarding research has a consistent structural form: the system infers what the user needs from behavioral signals or stated goals, proposes an action or resource, and allows the user to confirm or redirect. This is structurally identical to intent-based routing: accept goal, infer primitive, show routing label, confirm.

**The CRA counter-evidence that doesn't indict wizards**

Create React App is frequently cited as evidence that wizard-based CLI routing fails. The React team's official deprecation post-mortem (react.dev, 2025) directly contradicts this: CRA was deprecated due to "missing architectural capabilities in the generated artifact" — missing routing, data fetching, and code splitting features in what CRA produced. The wizard intake flow itself was not the failure point. Wizard flows that ask "create a new project?" and scaffold correctly are not indicted by CRA's deprecation. This removes CRA as evidence against wizard patterns.

**The expert-user failure case**

Where wizard-based routing does have documented failure evidence, it is expertise-specific. NN/g's wizard design article identifies expert users as the canonical wizard failure case: "power users often find wizards frustratingly rigid and limiting since wizards don't show users what their actions really do." Koenemann et al. (IJHCS 2025, n=56 developers, 8 co-design workshops) confirmed empirically that expert developers found mandatory explanation flows "obnoxious or even 'outrageous.'" Forced sequential clarification flows harm expert users who can specify intent clearly on the first turn.

This creates a practical design constraint: if the user population includes expert developers, a mandatory multi-step wizard will generate resistance from the users who need it least and may benefit the users who need it most (novices). A confidence-triggered single clarification step avoids this tradeoff.

**The single clarification question**

Amazon's ASK system (ACL 2025) provides the most direct empirical evidence for bounded clarification: asking one targeted clarifying question when routing ambiguity is detected improved retrieval recall@5 by approximately 20% versus direct routing. The key structural feature: the clarification question is triggered by ambiguity detection, not asked unconditionally for every routing request. Users with high-clarity intent statements are not forced through an unnecessary clarification step; only ambiguous requests trigger the additional question.

This pattern bridges the wizard vs. recommendation divide: it is recommendation-based (infer, propose) but uses a single wizard-style clarification step as an ambiguity escape valve.

**Design implications**

The evidence supports a routing design with these characteristics:
- Default to recommendation-based routing: accept goal statement, infer primitive, show routing label
- Trigger a single clarification question when intent ambiguity is detected — not for all requests
- Do not implement a mandatory multi-step sequential wizard for all routing requests
- Provide expert users an escape from guided flows once they are familiar with the primitive vocabulary
- Do not use wizard flows to ask users to justify their choice — the routing decision belongs to the system's inference, with user confirmation as the checkpoint

**Takeaway**

Recommendation-based routing (infer then propose) has 23 of 32 studies in its favor for developer onboarding contexts; wizard-based routing has minimal direct research support. But this is not "wizards fail" — it is "wizards are understudied." The practical synthesis: default to recommendation-based routing with confidence-triggered single clarification. Reserve multi-step wizard flows for genuinely high-complexity decisions where the user actively benefits from guided structure — not for routine primitive routing.
