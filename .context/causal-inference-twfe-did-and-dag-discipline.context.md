---
name: "Causal Inference: TWFE DiD Bias and DAG Discipline"
description: "Standard two-way fixed effects DiD is biased under staggered treatment adoption; Callaway & Sant'Anna is the modern fix. DAGs are widely applied but only ~20% of studies report the implied adjustment set."
type: concept
confidence: high
created: 2026-04-10
updated: 2026-04-10
sources:
  - https://arxiv.org/html/2508.02310v1
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC11875439/
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC8275441/
  - https://github.com/py-why/dowhy
related:
  - docs/context/bayesian-ab-testing-interpretability-not-sample-efficiency.context.md
---
# Causal Inference: TWFE DiD Bias and DAG Discipline

Standard two-way fixed effects (TWFE) difference-in-differences is biased when treatment adoption is staggered across units over time. The modern fix is Callaway & Sant'Anna (2021) or equivalent methods. DAGs are necessary for identifying adjustment sets, but only ~20% of studies that use them actually report the implied set.

## TWFE and Staggered Adoption

TWFE DiD — regressing outcomes on unit and time fixed effects plus a treatment indicator — is the dominant panel estimator in applied social science and business analytics. The bias arises from a "negative weights problem": when different units adopt treatment at different times, TWFE uses already-treated units as controls for newly treated units. This produces contaminated comparisons.

Modern remedies with strong empirical support:
- **Callaway & Sant'Anna (2021)** — estimates group-time average treatment effects, then aggregates. The current default recommendation for staggered designs.
- **Borusyak, Jaravel & Spiess (2024)** — imputation-based approach; better precision in some settings.
- **Sun & Abraham (2021)** — interaction-weighted estimator; straightforward to implement.
- **Bacon Decomposition** — diagnostic tool; decomposes TWFE into weighted 2×2 comparisons to reveal where contamination is occurring.

The parallel trends assumption — that treated units would have followed control unit trajectories absent treatment — is unverifiable by definition. Pre-trend visualization is necessary but not sufficient: parallel pre-trends neither guarantee nor rule out valid post-treatment identification. Diagnostic tests often lack statistical power to detect meaningful violations.

## DAG Discipline in Practice

Directed Acyclic Graphs (DAGs) are the correct tool for formalizing causal assumptions before selecting an adjustment set. A 2024 PMC methodological review provides a six-step framework: (1) construct the DAG before study design, (2) define exposure and outcome, (3) add common causes, (4) consider selection procedures, (5) consider measurement error, (6) inform data analysis.

Key principles:
- **Absent arrows are the stronger assumption** — omitted edges encode independence claims; these require justification.
- **Mediators and colliders must not be adjusted for** — including mediators blocks the causal path; including colliders induces spurious associations.
- **Unmeasured variables belong in the DAG** — they affect causal pathway identification regardless of data availability.

The gap: only ~20% of studies applying DAGs report the adjustment set implied by their DAG. Researchers frequently draw the DAG, then select controls by statistical criteria rather than the graph's structural implications — defeating the purpose.

## Tooling

**DoWhy (Python/PyWhy)** is the best-in-class applied causal inference library. It implements a four-step methodology: model (specify causal graph), identify (derive estimand from graph), estimate (apply statistical methods), refute (test assumptions with falsification API). The refutation API — which includes placebo tests, subset tests, and data permutation — is the key differentiator; it makes causal inference more robust to assumption violations without requiring deep econometric expertise.

## Bottom Line

For any panel study with staggered rollout, default to Callaway & Sant'Anna rather than TWFE. Build the DAG first, report the implied adjustment set, and flag mediators and colliders explicitly. Use DoWhy's refutation API to test robustness. Do not treat pre-trend visualization as a sufficient identification check.
