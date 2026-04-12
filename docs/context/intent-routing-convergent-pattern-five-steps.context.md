---
name: "Intent Routing: Convergent Five-Step Pattern"
description: "Evidence across five sub-questions converges on a single actionable intake pattern: accept natural language, infer primitive, show routing label (not reformulation), display confidence when uncertain, provide easy correction — not a justification gate"
type: context
sources:
  - https://arxiv.org/abs/2304.06597
  - https://arxiv.org/abs/2310.03691
  - https://arxiv.org/abs/2602.07338
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC3240751/
  - https://dl.acm.org/doi/10.1145/2858036.2858402
  - https://arxiv.org/abs/2408.15989
  - https://arxiv.org/abs/2402.02136
  - https://sjdm.org/journal/17/17411/new.html
  - https://www.amazon.science/publications/ask-aspects-and-retrieval-based-hybrid-clarification-in-task-oriented-dialogue-systems
related:
  - docs/research/2026-04-11-ux-patterns-primitive-routing.research.md
  - docs/context/abstraction-gap-and-goal-vocabulary-scent.context.md
  - docs/context/intent-based-vs-model-routing-articulatory-distance.context.md
  - docs/context/intake-acceptance-before-routing-commitment.context.md
  - docs/context/wizard-vs-recommendation-routing-onboarding.context.md
  - docs/context/automation-bias-confidence-display-and-transparency-bounds.context.md
---

Across five research sub-questions — abstraction gap, intent vs. model routing, intake patterns, wizard vs. recommendation evidence, and justification gates — the findings converge on one actionable intake pattern. Each step is independently supported by empirical evidence; each anti-pattern has documented failure costs.

**The five-step pattern**

**Step 1: Accept the user's goal in natural language**
Do not ask users to name or select a primitive at intake. Requiring users to match their goal to a taxonomy they don't know imposes maximum Hick's Law friction and provides zero information scent (IFT framework; CHI 2023 abstraction gap study, n=24). Goal-vocabulary labels provide scent; primitive-vocabulary labels do not.

**Step 2: Infer the routing from intent**
Use intent-based classification rather than model-based option selection. Accepting natural language goal statements and classifying them internally reduces articulatory distance — the burden of expressing intent. DirectGPT (CHI 2024, n=12, within-subject): reducing articulatory distance produced 50% faster task completion, ~25% higher success rates, 72% fewer words (p<0.001). This is the strongest empirical argument for intent-based intake.

**Step 3: Show a routing label before acting**
Surface the routing interpretation as a brief label in user-goal vocabulary before taking action. Do not reformulate the user's words. Do not expose model internals. A short label that confirms the action — "Building this as a hook — a check that runs before each push" — is the calibrated middle ground. Too little (silent routing) causes automation bias: erroneous automated advice increases incorrect decisions by 26% (Parasuraman & Manzey, Human Factors 2010 systematic review, risk ratio 1.26, 95% CI 1.11–1.44). Too much (visible reformulation) reduces satisfaction: users preferred responses to their original intent 56.61%/53.50% of the time over correctly-reformulated versions (Bodonhelyi et al. 2024). Kizilcec (CHI 2016, n=103) confirmed the inverted-U: both extremes of transparency reduce trust calibration equally.

**Step 4: Display confidence state when routing certainty is low**
When automatic classification is uncertain, surface that uncertainty — do not present a confident routing label for a low-confidence decision. Dynamic confidence display reduces automation bias (Parasuraman & Manzey 2010). Automatic intent classification has a measurable ~10% failure ceiling at GPT-4 performance, with systematic blind spots for rare categories (Bodonhelyi et al. 2024: "learning support" — 0% for GPT-4; "curricular planning" — 0% for GPT-4). The rarest primitive in a system is the most likely to be systematically misclassified. When confidence is low, surface it and offer a single targeted clarification question. Amazon's ASK system (ACL 2025) found one targeted clarifying question when ambiguity is high improved recall@5 by ~20%.

**Step 5: Provide easy correction, not a justification gate**
After showing the routing label, provide one low-friction path to redirect — not a gate requiring users to explain their choice before routing proceeds. Hoffmann, Gaissmaier, & von Helversen (JDM 2017, two controlled experiments, n=144 + n=110): process accountability (forced justification before judgment) reduced confidence without improving accuracy or changing judgment strategies. There is no direct empirical evidence that justification gates improve intake routing accuracy. Justification gates shift friction from the system (which should bear the inference cost) to the user (who should confirm or redirect).

**Binding constraints**

Three findings qualify where the pattern applies:

1. **~10% failure ceiling:** Even at GPT-4 performance, ~1 in 10 users is misrouted. Rare primitives (e.g., "subagent") are the most likely to be systematically misclassified. The intake design must account specifically for rare-primitive failure modes, not just optimize the common case.

2. **Expert-user escape valves:** Expert developers find mandatory guided flows "obnoxious or even 'outrageous'" (Koenemann et al. 2025, n=56, IJHCS). They need on-demand access to the routing decision and model vocabulary. The five-step pattern applies at intake for all users; experts need a path to bypass or inspect the interpretation step once they know the vocabulary.

3. **Visible reformulation consistently reduces satisfaction:** Users who see their intent replaced by the system's vocabulary resist it even when the replacement is correct (56%+ prefer original phrasing). The routing label in Step 3 must use goal vocabulary, not rephrase the user's words.

**Anti-patterns this rules out:** presenting all primitives simultaneously (highest-friction design); silent auto-routing (+26% error rate); showing a reformulation (consistent satisfaction reduction); mandatory multi-step wizard (harms experts); justification gates (reduces confidence, no accuracy gain).

**Takeaway**

The five steps are not a preference — they are each independently supported by empirical findings with documented failure costs for the alternatives. The pattern accepts that automatic classification fails ~10% of cases, and routes around that by showing confidence state and providing low-friction correction. The goal-vocabulary label at Step 3 is the linchpin: it closes the automation bias gap without triggering reformulation resistance.
