---
name: "A/B Testing Statistical Rigor and the Peeking Problem"
description: "α=0.05 and 80% power are operational defaults, not universal mandates; peeking at results 20 times inflates false positive rate to ~40%; mSPRT solves peeking but trades statistical power; CUPED 65% speedup is best-case under high correlation"
type: concept
confidence: high
created: 2026-04-10
updated: 2026-04-10
sources:
  - https://www.abtasty.com/blog/sample-size-calculation/
  - https://docs.statsig.com/experiments/advanced-setup/sequential-testing
  - https://docs.growthbook.io/statistics/multiple-corrections
  - https://www.geteppo.com/blog/the-cult-of-stat-sig
  - https://www.geteppo.com/blog/cuped-bending-time-in-experimentation
related:
  - docs/context/experimentation-culture-incentive-misalignment.context.md
---
The industry standard for A/B testing — α=0.05 (Z=1.96) significance level and 80% statistical power (Z=0.84) — is an operational default, not a universal mandate. These thresholds minimize false positives while preserving reasonable sensitivity to detect true effects. They emerged from frequentist statistics as practical starting points, not from rigorous analysis of what is appropriate for marketing decisions specifically. Context-sensitive thresholds are better practice: 80-90% confidence for low-stakes UI tests where false positives are cheap to reverse, 99% for high-stakes decisions with expensive rollback costs. The binary treatment of significance — "significant" vs. "not significant" — is described by practitioners as "especially problematic" because it discards information about effect size and uncertainty.

Minimum experiment duration of 14 days is well-supported for capturing behavioral variation across weekdays and weekends. Running experiments for less time introduces systematic bias from day-of-week effects — Monday conversion rates differ from Friday rates, and users exhibit different behaviors on their first session of the week versus mid-week sessions.

The peeking problem is the most common statistical error in practice. Checking experiment results before the predetermined end date and making decisions based on early results inflates the false positive rate substantially. Checking results 20 times instead of once can inflate the false positive rate from the intended 5% to approximately 40% or higher. The mechanism: each check is effectively an independent statistical test, and the probability of at least one false positive accumulates with each check. The solution is either strict pre-commitment to check only at the predetermined end date, or sequential testing methods that explicitly account for interim looks.

The modified Sequential Probability Ratio Test (mSPRT), implemented by Statsig, addresses the peeking problem by continuously adjusting p-values and confidence intervals to compensate for the increased false positive rate from continuous monitoring. The critical tradeoff Statsig's documentation states directly: "If making the right decision is important, use statistically-significant sequential testing results. If accurate measurement is important, wait for full power." mSPRT reduces statistical power compared to fixed-horizon tests and overestimates effect sizes on early stopping — it is best suited for rapid decisions and regression detection during launches, not for careful causal measurement. Spotify Engineering identified a "Peeking Problem 2.0" for longitudinal experiments where the same user contributes multiple observations over time, requiring additional methodological care beyond standard mSPRT.

Multiple testing correction is required when running experiments with multiple metrics or multiple hypothesis tests simultaneously. Running 10 experiments with 2 variations and 10 metrics each means 100 simultaneous hypothesis tests — at α=0.05, false positives accumulate dramatically without correction. Two primary strategies: Holm-Bonferroni (FWER control) for conservative analysis requiring high reliability in primary metrics, and Benjamini-Hochberg (FDR control) for exploratory analysis tolerating modest false positive rates while preserving more statistical power.

CUPED (Controlled-experiment using pre-experiment data) reduces experiment variance by leveraging historical user data, enabling faster statistical significance. Microsoft's original implementation reduced 8-week experiments to 5-6 weeks — a 65% speedup under favorable conditions. The 65% figure is best-case, not typical: it applies under high pre-post correlation between the covariate (pre-experiment metric) and the outcome variable. Under low correlation — new product surfaces, first-time user flows, high-variance behavioral metrics — the benefit is under 5%. CUPED also assumes linearity in the relationship between covariate and outcome, and clean baselines; imperfect randomization or holdover exposure from prior experiments invalidates the variance reduction.
