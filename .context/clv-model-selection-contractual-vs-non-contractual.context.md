---
name: "CLV Model Selection: Contractual vs. Non-Contractual"
description: "CLV model selection depends on business model. BG/NBD + Gamma-Gamma for non-contractual (retail/e-commerce); survival models (Weibull/Cox) for contractual (subscriptions). The contractual/non-contractual distinction is the fundamental fork."
type: comparison
confidence: high
created: 2026-04-10
updated: 2026-04-10
sources:
  - https://www.pymc-marketing.io/en/stable/guide/clv/clv_intro.html
  - https://www.aliz.ai/en/blog/part-1-customer-lifetime-value-estimation-via-probabilistic-modeling
  - https://www.pymc-labs.com/blog-posts/hierarchical_clv
  - https://towardsdatascience.com/from-probabilistic-to-predictive-methods-for-mastering-customer-lifetime-value-72f090ebcde2/
  - https://www.statology.org/customer-lifetime-value-with-python-beyond-simple-averages/
related:
  - docs/context/churn-prediction-vs-uplift-modeling.context.md
---
# CLV Model Selection: Contractual vs. Non-Contractual

The fundamental decision in CLV modeling is not algorithm choice — it is business model type. Contractual settings (subscriptions) use survival models (Weibull, Cox). Non-contractual settings (retail, e-commerce) use BG/NBD + Gamma-Gamma. "We cannot use the same approaches to compute lifetime value" across these two contexts (PyMC-Marketing documentation).

## The Fundamental Fork

**Contractual settings** (subscriptions, insurance, memberships): churn is directly observed. The customer either renews or cancels. Relationship status is always known. Survival analysis models the time to cancellation event.
- Primary models: Weibull AFT (accelerated failure time), Cox proportional hazards
- Inputs: tenure, subscription tier, engagement metrics, billing history
- Interpretable output: survival curves showing probability of retention at each time horizon

**Non-contractual settings** (retail, e-commerce, hotel bookings): churn is never directly observed. A customer who has not purchased may be in a natural inter-purchase gap or may have permanently defected. The distinction is always uncertain.
- Primary model: BG/NBD (Beta Geometric Negative Binomial Distribution) for transaction count + Gamma-Gamma for transaction value
- Inputs: recency (time since last purchase), frequency (number of repeat purchases), observation period T
- Interpretable output: probability customer is still "alive" + expected future transactions over a forecast horizon

## BG/NBD Model Details and Limitations

BG/NBD (Fader, Hardie & Lee, 2005) models two parallel processes: heterogeneous Poisson purchase rates across customers, and probabilistic latent churn after any transaction. It requires only RFM data (recency, frequency, monetary value is handled by Gamma-Gamma separately).

Known limitations:
- **Single-purchase customers receive p(alive) = 1** — structurally unrealistic for first-time buyers who may never return
- **Independence assumption**: dropout probability and purchase frequency are modeled as independent — likely violated in practice (high-frequency buyers may be harder to churn)
- **Stationarity assumption**: purchase rates assumed stable over time — fails for businesses with strong seasonality or promotional cadences
- The Poisson purchase-rate assumption is frequently violated; a COM-Poisson variant has been proposed for overdispersed purchase distributions

## Gamma-Gamma Extension

Gamma-Gamma models expected transaction value among repeat purchasers. It is fit only on customers with frequency > 0 (at least one repeat purchase) and assumes monetary value is independent of purchase frequency. The independence assumption frequently fails: high-frequency buyers often purchase lower-value items. Validate this assumption before applying.

Combined BG/NBD + Gamma-Gamma: a practitioner analysis on a publicly available dataset found simple average CLV of $11.67 vs. probabilistic CLV median of $21.32 over 26 weeks — the probabilistic model captures value concentration among high-value customers that averages hide.

## Hierarchical Bayesian Extensions

For organizations with multiple customer cohorts or product lines, hierarchical Bayesian extensions via PyMC-Marketing address two BG/NBD failure modes: small-cohort instability (pooling information across cohorts) and seasonality (allowing time-varying parameters). On the CDNOW benchmark dataset, unpooled models showed high volatility and wide credible intervals for small cohorts (n=124); hierarchical estimates were substantially more stable.

## When Simpler Models Are Sufficient

For small-to-mid-market organizations without data science capacity, recency-tiered cohort LTV (simple average CLV by acquisition channel and recency bucket) delivers approximately 80% of the decision value at a fraction of the modeling complexity. The BG/NBD improvement over averages is real but requires clean transactional data, statistical expertise, and ongoing model validation to maintain.

## Bottom Line

Identify your business model type first — contractual or non-contractual. This determines the model family. For non-contractual businesses with sufficient transaction history, BG/NBD + Gamma-Gamma is the standard probabilistic baseline. Validate BG/NBD assumptions (Poisson purchase rates, independence of dropout and frequency) before deployment; violations are common in real retail data.
