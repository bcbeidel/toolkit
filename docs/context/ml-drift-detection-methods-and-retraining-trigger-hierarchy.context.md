---
name: ML Drift Detection Methods and Retraining Trigger Hierarchy
description: "Performance degradation is the most reliable retraining trigger — distribution drift statistics produce false positives; KS, PSI, and Wasserstein each fit different dataset sizes and sensitivity requirements."
type: concept
confidence: high
created: 2026-04-10
updated: 2026-04-10
sources:
  - https://www.evidentlyai.com/ml-in-production/data-drift
  - https://www.evidentlyai.com/blog/data-drift-detection-large-datasets
  - https://smartdev.com/ai-model-drift-retraining-a-guide-for-ml-system-maintenance/
related:
  - docs/context/mlops-maturity-levels-and-organizational-prerequisites.context.md
  - docs/context/feature-store-dual-store-pattern-and-scale-threshold.context.md
---
# ML Drift Detection Methods and Retraining Trigger Hierarchy

Drift detection is essential for production ML, but statistical drift signals are unreliable retraining triggers on their own. Business metric degradation — model performance declining on actual outcomes — is the more reliable and actionable signal.

## Four Types of Drift

Understanding which type of drift is occurring determines the remediation:

- **Data drift (covariate shift)**: Input feature distributions change relative to training data. The model's learned function may still be valid, but it's being applied to inputs it hasn't seen. May or may not cause performance degradation.
- **Concept drift**: The relationship between input features and target variables fundamentally changes. The model's learned function is now wrong. Will cause performance degradation.
- **Prediction drift**: Model output distribution shifts without obvious input changes. Can indicate concept drift or data quality issues upstream.
- **Training-serving skew**: Distribution mismatch between training data and production inputs at deployment time. This is a preventable, one-time issue (not ongoing drift) — best addressed with a feature store.

Concept drift is more damaging than data drift because the model's fundamental assumption about the world is incorrect.

## Statistical Detection Methods

No single best test exists — method selection depends on dataset size and desired sensitivity:

| Method | Sensitivity | Best Use Case |
|--------|-------------|---------------|
| Kolmogorov-Smirnov (KS) | High — flags 0.5% changes on large datasets | Small samples (<1,000 observations) |
| Population Stability Index (PSI) | Low — stable across sample sizes | Large datasets; react only to major changes |
| Wasserstein Distance | Medium — between KS and PSI | Compromise when neither extreme fits |
| Jensen-Shannon Divergence | Medium — stable for large datasets | Slight sensitivity advantage over KL divergence |

KS test caution: on large datasets (>10,000 observations), KS flags statistically significant changes that have no practical impact on model performance. This produces alert fatigue. Use PSI or Wasserstein for large-dataset monitoring.

Categorical features use Chi-square tests rather than KS.

## The Retraining Trigger Hierarchy

**Primary trigger — performance metrics**: "The most important signal: your model's performance metrics have declined." When labeled data is available and model accuracy, precision/recall, RMSE, or other business-relevant metrics degrade, this is a direct and unambiguous retraining signal. Act on it.

**Secondary trigger — distribution drift**: When labeled data is unavailable or delayed (common in production), distribution changes provide early warning. Use drift statistics to flag potential issues for investigation, not as automatic retraining triggers. Statistical drift does not always mean performance drift.

**Fallback — time-based retraining**: Fixed schedule (daily, weekly, monthly) is the simplest approach. May retrain unnecessarily when nothing has changed; may retrain too late if drift occurs rapidly. Use as a floor, not a primary strategy.

## Retraining Data Strategy

When retraining, use recent historical data (typically 1–2 years) rather than the entire historical dataset. Older data may contain patterns that no longer reflect current behavior, contaminating the model with stale signals. Full retrains on complete history risk learning from outdated distributions.

## Confidence Note

Drift detection sources are dominated by Evidently AI (3 of 3 sources) — they sell drift monitoring tooling. Technical comparisons are detailed and widely cited externally, but tool-specific recommendations reflect vendor interest. The statistical method comparison (KS/PSI/Wasserstein) is directionally consistent with independent statistical literature. Treat tooling recommendations skeptically; treat method characteristics as reliable.

**Takeaway**: Monitor business performance metrics as the primary retraining trigger. Use distribution drift statistics as early-warning indicators, not automatic retraining gates. Match statistical method to dataset size: KS for small datasets, PSI for large datasets, Wasserstein as the middle ground.
