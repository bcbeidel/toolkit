---
name: "Bayesian A/B Testing: Interpretability Advantage, Not Sample Efficiency"
description: "Bayesian A/B testing's defensible advantage is interpretability — probability to be best (P2BB) gives intuitive decision support. The '75% fewer samples' figure is unsubstantiated vendor marketing."
type: concept
confidence: high
created: 2026-04-10
updated: 2026-04-10
sources:
  - https://www.dynamicyield.com/lesson/running-effective-bayesian-ab-tests/
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC8526359/
  - https://engineering.atspotify.com/2023/03/choosing-sequential-testing-framework-comparisons-and-discussions
related:
  - docs/context/causal-inference-twfe-did-and-dag-discipline.context.md
  - docs/context/ml-vs-statistical-methods-sample-size-tradeoff.context.md
---
# Bayesian A/B Testing: Interpretability Advantage, Not Sample Efficiency

The defensible advantage of Bayesian A/B testing is interpretability: probability to be best (P2BB) expresses evidence as a probability statement, which is what business decision-makers actually want. The widely cited "75% sample-size reduction" claim is unsubstantiated vendor marketing, not a replicable finding.

## The Interpretability Advantage

Frequentist p-values answer a question practitioners do not ask: "What is the probability of observing results this extreme if the null hypothesis were true?" P2BB answers the question they do ask: "What is the probability that variant A outperforms variant B?" This directness reduces decision errors from p-value misinterpretation, which is endemic in business experimentation.

Bayesian credible intervals are also directly interpretable: a 95% credible interval means there is a 95% posterior probability that the parameter lies within that range. Frequentist confidence intervals carry no such interpretation.

## What Bayesian Testing Does Not Fix

**Sample efficiency is not reliably higher.** The "75% fewer samples" figure appears in vendor marketing (notably Dynamic Yield) but has no cited primary source. Bayesian A/B testing does not reduce required sample size in any general sense — the posterior concentrates as data accumulates just as frequentist power grows. Sequential testing under both frameworks can reduce expected sample size, but the comparison is method-specific and depends heavily on prior strength and stopping rules.

**Early stopping is dangerous under Bayesian A/B testing too.** P2BB fluctuates during testing. The correct practice is to set strict stopping thresholds (0.999 or 0.001) before starting, not to stop when P2BB looks good mid-experiment. The peeking problem is not automatically solved by switching from frequentist to Bayesian methods.

**Priors require reporting and sensitivity analysis.** A 2021 PMC review of Bayesian analysis reporting found only 24% of studies fully reported the prior, and only 18% conducted a sensitivity analysis — even in academic work. In business experimentation, prior choices typically go undocumented entirely. A Bayesian test using an aggressive informative prior can reach high P2BB with fewer samples not because of statistical efficiency but because prior beliefs are doing most of the work.

## Practical Guidance

- Use Bayesian A/B testing when the P2BB framing will improve decision quality for stakeholders who struggle with p-values.
- Run experiments through complete weekly cycles; avoid stopping on partial cycles regardless of P2BB.
- If sample-size reduction is a genuine goal, use sequential testing (Group Sequential Testing is preferred over mSPRT per Spotify's 2023 analysis) rather than switching frameworks.
- Document the prior, report the prior's effect on conclusions, and conduct at least a basic sensitivity analysis.

## Bottom Line

Bayesian A/B testing is not more sample-efficient than frequentist testing in any well-supported general sense. Its real advantage is that P2BB is the decision metric stakeholders actually understand. That advantage is real and worth having — but overselling it as a route to shorter tests will create misaligned expectations and early stopping errors.
