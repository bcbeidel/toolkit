---
name: "ML vs. Statistical Methods: Sample Size Determines the Winner"
description: "Statistical forecasting methods (Theta, Comb, ARIMA) statistically dominate ML at small sample sizes. Gradient boosting is the sound tabular default for large datasets, but not universally dominant."
type: comparison
confidence: high
created: 2026-04-10
updated: 2026-04-10
sources:
  - https://www.mdpi.com/1099-4300/27/3/279
  - https://www.genpact.com/insight/the-evolution-of-forecasting-techniques-traditional-versus-machine-learning-methods
  - https://arxiv.org/pdf/2305.02997
related:
  - docs/context/rag-hallucination-and-retrieval-quality-gap.context.md
  - docs/context/agentic-ai-reliability-gap-and-agent-washing.context.md
  - docs/context/bayesian-ab-testing-interpretability-not-sample-efficiency.context.md
---
# ML vs. Statistical Methods: Sample Size Determines the Winner

At small sample sizes, statistical forecasting methods statistically dominate ML across horizons. Gradient boosting is the sound default for tabular business data when datasets are large, but neural networks can exceed it on smooth-feature, large-sample tasks. There is no universal winner — the right choice depends on dataset size, feature distribution, and nonlinearity.

## The Sample-Size Threshold

A 2025 peer-reviewed study in MDPI Entropy reviewing time-series forecasting found that Theta, Comb, and ARIMA statistically dominated ML methods across multiple forecasting horizons when sample sizes were small. A PLOS One meta-analysis (foundational) established the same pattern: ML only outperforms statistical methods as sample size grows. Below the threshold, simpler models win.

This directly challenges the "ML by default" instinct. A single published case study (Genpact, cereal sales: ML at 11.61% MAPE vs. traditional at 15.17%) does not generalize — it was conducted on a large, clean dataset in a domain where nonlinear patterns and many features are present.

**Decision rule for forecasting:**
- Small N, few features, strong seasonality → ARIMA, Theta, Exponential Smoothing
- Large N, many features, nonlinear patterns → gradient boosting (XGBoost, LightGBM, CatBoost)
- Large N, smooth feature distributions → benchmark neural networks against gradient boosting

## Gradient Boosting on Tabular Data

For structured business classification and regression tasks with large datasets, gradient boosting (XGBoost, LightGBM, CatBoost) is the most reliable baseline. It outperforms deep learning on heavy-tailed, skewed, or high-variance feature distributions — conditions that are common in business data. Consistent dominance in Kaggle competitions provides strong corroborating signal.

The qualification: neural networks show competitive or superior performance when feature distributions are smooth and datasets are large. A 2023 arXiv study found transformer models achieve approximately 8% higher recall on imbalanced classification tasks (fraud detection, medical diagnostics) — but the general finding from the same paper is that GBDTs are the safer default.

## Regulatory Context

In regulated industries (banking, insurance, healthcare), interpretability requirements push toward logistic regression and decision trees regardless of dataset size. A 2025 Springer systematic review of credit scoring found logistic regression preferred when regulators require explanations. Gradient boosting with SHAP post-hoc explanations is an acceptable middle ground in moderate-regulation contexts.

## Bottom Line

Do not default to ML for time series or forecasting tasks without first asking: how large is the dataset? At small N, ARIMA or Theta will likely outperform any ML approach with less engineering effort. For large-scale tabular data, gradient boosting is the sound default — but test empirically rather than assuming dominance.
