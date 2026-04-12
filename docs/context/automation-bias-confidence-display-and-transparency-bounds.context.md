---
name: "Automation Bias, Confidence Display, and Transparency Bounds"
description: "Silent auto-routing causes ~60% degradation when assumptions compound; displaying dynamic confidence reduces automation bias (erroneous auto-advice inflates error rates 26%); optimal transparency is a narrow band — routing label, not reformulation or model internals"
type: context
sources:
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC3240751/
  - https://dl.acm.org/doi/10.1145/2858036.2858402
  - https://arxiv.org/abs/2602.07338
  - https://arxiv.org/abs/2402.02136
  - https://www.sciencedirect.com/science/article/pii/S0749597825000172
  - https://arxiv.org/abs/2511.00230
  - https://sjdm.org/journal/17/17411/new.html
related:
  - docs/research/2026-04-11-ux-patterns-primitive-routing.research.md
  - docs/context/intent-based-vs-model-routing-articulatory-distance.context.md
  - docs/context/intake-acceptance-before-routing-commitment.context.md
  - docs/context/wizard-vs-recommendation-routing-onboarding.context.md
  - docs/context/intent-routing-convergent-pattern-five-steps.context.md
---

Silent auto-routing — inferring a primitive and acting without surfacing the routing decision — carries a specific failure cost: when automated advice is wrong and unexplained, erroneous decisions increase by 26%. Displaying dynamic confidence levels measurably reduces this automation bias. But transparency is not uniformly beneficial — showing too much (model internals, explicit reformulations of user intent) can be as harmful as showing nothing. The calibrated middle ground is a brief routing label that confirms the action without replacing the user's vocabulary.

**Automation bias: the quantified cost of silent routing**

Parasuraman & Manzey (Human Factors 2010, systematic review) found that erroneous automated advice increases incorrect decision rates by 26% compared to no automation (risk ratio 1.26, 95% CI 1.11–1.44). Critically, displaying dynamic confidence levels — indicating when the system is uncertain versus confident — reduced automation bias. "Updating the confidence level of the DSS alongside pieces of advice improved the appropriateness of user reliance, decreasing AB."

This directly constrains WOS routing design: when routing confidence is low, showing confidence state is not just good UX — it measurably reduces incorrect decisions. Silent routing that presents confident output for low-confidence decisions increases the probability of the user accepting a wrong routing without questioning it.

**The intent mismatch degradation**

Liu et al. (2026, arXiv:2602.07338) found approximately 60% relative performance degradation when systems committed to routing decisions without surfacing their interpretation (Figure 2: "the relative performance degradation between fully specified and underspecified settings remains remarkably constant (~60%) across diverse model sizes and families"). The structural cause: early tentative assumptions get locked in, and subsequent user inputs are interpreted as confirmations rather than corrections.

Silent auto-routing is the mechanism that enables this degradation. If the routing decision is never surfaced, users have no opportunity to catch and correct wrong assumptions before they compound.

**The transparency inverted-U**

Kizilcec (CHI 2016, n=103 field experiment on peer assessment grading) found that both too-little and too-much transparency reduced trust calibration equally, compared to medium transparency. In low and high transparency conditions, expectation violation was negatively correlated with trust. In the medium transparency condition, trust was uncorrelated with expectation violation. The finding: some transparency is necessary for trust calibration, but more transparency is not uniformly better.

Schilke & Reimann (2025, 13 pre-registered experiments, n>3,000) found that AI disclosure — surfacing AI involvement or decision-making — consistently reduced trust across domains. While this study addresses AI authorship disclosure specifically, it establishes that surfacing AI decision-making can systematically reduce user acceptance when framing is not carefully managed.

**What too much transparency costs**

Bodonhelyi et al. (2024) found users preferred responses to their original stated intent 56.61%/53.50% of the time over correctly-reformulated versions — users resist having their words replaced by the system's vocabulary even when the replacement is accurate. Shi et al. (arXiv:2511.00230, 2025) found that exposing model internals increased trust but caused systematic miscalibration: users misjudged 11 of 15 behavioral traits, and correct behavior did not improve. Hoffmann, Gaissmaier, & von Helversen (JDM 2017, n=144 + n=110) found process accountability — requiring users to justify routing choices before acting — reduced confidence without improving accuracy or changing judgment strategies.

**The calibrated middle ground**

The evidence converges on a narrow effective band for routing transparency:
- **Too little:** Silent routing — no routing label shown, no confidence signal — causes automation bias (+26% error rate) and ~60% degradation when assumptions compound
- **Too much:** Reformulating user intent in system vocabulary, exposing model internals, or requiring justification — reduces satisfaction, creates miscalibration, reduces confidence without improving accuracy
- **The effective band:** A brief routing label in user-goal vocabulary that confirms what action will be taken, combined with a confidence signal when routing certainty is low

Example of the effective band: "Building this as a hook — a check that runs before each push. [Confident]" vs. "I'm not sure if this should be a hook or a rule — which fits better? [Uncertain]"

**Takeaway**

Surface routing decisions as brief goal-vocabulary labels — not reformulations of user intent, not explanations of model internals. Show confidence state when routing certainty is low; erroneous silent routing inflates error rates 26% and degrades performance ~60% when wrong assumptions compound. The transparency optimum is narrow: a routing label confirms the decision without replacing the user's vocabulary. Anything beyond this label consistently reduces user satisfaction without improving routing accuracy.
