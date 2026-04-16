---
name: "Measurement Triangulation: Attribution, Incrementality, and MMM"
description: "Each measurement method answers a different question; triangulating all three is the consensus framework, but platform attribution systematically overcounts and no single method is causally valid"
type: concept
confidence: high
created: 2026-04-10
updated: 2026-04-10
sources:
  - https://www.adjust.com/blog/attribution-incrementality-mmm/
  - https://www.deducive.com/blog/2025/12/12/our-guide-to-marketing-attribution-incrementality-and-mmm-for-2026
  - https://www.measured.com/faq/incrementality-attribution-mmm-decision-tree/
  - https://www.emarketer.com/content/faq-on-incrementality-how-prove-your-ads-actually-work-2026
  - https://www.haus.io/blog/incrementality-testing-vs-traditional-mmm-whats-the-difference
related:
  - docs/context/bayesian-mmm-tool-selection-meridian-robyn.context.md
  - docs/context/paid-automation-data-sufficiency-gates.context.md
---
The three core measurement methods in digital marketing answer fundamentally different questions and are not interchangeable: attribution answers "which" (which ad, which keyword, which creative drove this conversion), incrementality answers "did it cause" (would this conversion have happened without the marketing exposure), and MMM answers "how much" (how should budget be allocated across channels, and what are diminishing returns). Using any one method alone produces a systematically incomplete picture.

Attribution — including multi-touch attribution built on Shapley values or Markov chains — distributes credit mathematically across touchpoints. It satisfies fairness axioms, but it cannot establish causality. It cannot answer whether conversions would have occurred without a given channel. Real-world divergence between Shapley-based attribution and other methods can reach 80%, which means tactical optimization decisions made on attribution data can be directionally wrong. GA4's data-driven attribution has additional limitations: it is scoped to Google's ecosystem, requires a 400-conversion/28-day threshold before activating, and is opaque about model inputs.

Platform-reported attribution systematically overcounts. Walled-garden platforms (Google, Meta) attribute conversions within their own ecosystems and share only aggregated signals. A documented example: Meta reports 500 conversions for a campaign while an independent incrementality test shows only 140 incremental conversions. Last-click models compound this by assigning 100% credit to the final touchpoint, overrepresenting bottom-funnel retargeting and underrepresenting assist channels. Platform-run conversion lift tests (Facebook Conversion Lift, Google Brand Lift) have structural bias toward confirming platform value and are not neutral arbiters.

Incrementality testing is the only method that answers causality questions directly. Geo-based experiments with matched markets establish a counterfactual: what would have happened without the marketing exposure. The eMarketer July 2025 survey found 52% of US brand and agency marketers now use incrementality testing. Google reduced minimum budgets for experiments to $5,000 using Bayesian models, democratizing access for mid-market brands. The operational barriers — 6-12 months of geographic sales history, 10-15 matched markets, minimum test duration of 3-4 weeks — remain real. Self-reported benchmarks from vendors (e.g., Stella's 2.31x iROAS across 225 geo tests) have survivorship bias and no independent audit.

MMM operates at the strategic layer. It answers budget allocation questions using aggregated, channel-level historical data — no individual tracking required. MMM cannot answer whether last week's campaign caused conversions; it models long-run relationships and diminishing returns. It requires 2+ years of clean historical data with meaningful spend variation across channels, significant analytical investment, and expert calibration of transformation specifications (adstock decay, saturation curves). Without expertise, MMM produces plausible-looking but miscalibrated outputs.

The triangulation framework routes decisions to the right method by question type: use attribution for real-time tactical optimization (bid changes, creative decisions, keyword management), use incrementality for channel validation and finance reporting (is this channel adding incremental value?), and use MMM for annual budget strategy (where should we shift investment across channels?). Integrating the three requires resolving systematic conflicts between their outputs — a problem with no algorithmic solution today. MMM is a mature-team capability, not a starting point. For teams without MMM infrastructure, the practical standard is incrementality testing as a complement to, not replacement for, platform-reported attribution.
