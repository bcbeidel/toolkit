---
name: "Confidence Calibration and Self-Correction"
description: "LLM confidence severely miscalibrated; self-correction without external feedback yields +1.8pp; structured external feedback yields 21-32pp"
type: concept
confidence: high
created: 2026-04-10
updated: 2026-04-10
sources:
  - https://arxiv.org/html/2503.15850v1
  - https://arxiv.org/html/2604.00445
  - https://direct.mit.edu/tacl/article/doi/10.1162/tacl_a_00713/125177/When-Can-LLMs-Actually-Correct-Their-Own-Mistakes
  - https://arxiv.org/abs/2308.00436
related:
  - docs/context/llm-failure-modes-and-mitigations.context.md
  - docs/context/llm-as-judge-biases-and-mitigations.context.md
---
LLM confidence estimates are severely miscalibrated, and self-correction without external feedback provides almost no improvement. The distinction between intrinsic self-correction (the model critiquing itself) and extrinsic self-correction (structured feedback from tests, tools, or execution) is the key design principle.

## Calibration Is Broken

Expected Calibration Errors (ECE) range from 0.108 to 0.427 across all tested LLM formats — well above acceptable thresholds for deployed systems. These errors mean the model's expressed confidence is a poor predictor of actual correctness. A model saying it is "90% confident" may be right only 60% of the time.

Most uncertainty metrics compound this problem by measuring "local continuation stability rather than semantic truth" — a fundamental proxy failure. High token probability does not mean the claim is factually correct; it means the model generates fluently. Fluency and accuracy are not correlated in the way confidence scores imply.

Reasoning uncertainty accounts for 58% of errors in multi-step QA tasks, making it the dominant failure mode category.

## Intrinsic Self-Correction: Almost Useless

Naive self-refinement ("Is there anything to refine?") yields only +1.8 percentage points improvement across five iterative attempts. The primary bottleneck is self-diagnosis — models systematically overrate their own generations during in-context critique, with monotonic amplification over multiple self-refinement steps.

Self-verification cannot detect errors the model lacks knowledge to identify. If the model doesn't know the correct answer, it cannot reliably detect that its answer is wrong. CoT chains compound this: reasoning steps can look coherent while being factually incorrect.

## Extrinsic Self-Correction: Substantial Gains

With structured external feedback — test suite results, tool output, execution traces — self-refinement yields 21-32 percentage point gains. The mechanism: external feedback provides ground truth signals the model cannot generate internally.

Design implications:
- Build feedback loops using executable verification where possible (tests, linters, static analysis)
- Treat "pass tests" as the primary self-correction signal, not "review your answer"
- Structure feedback as specific failure information, not general "try again" prompts

## Truth-Aligned Calibration (TAC)

TAC is a post-hoc calibration method using a lightweight neural mapper trained on correctness labels. It reduces ECE by 17-27 points across datasets and works with as few as 32 labeled examples or 30% corrupted training data. Raw confidence scores should not be trusted without calibration as a mandatory pipeline step.

## Detection Method Hierarchy

For cost-reliability tradeoffs in production:

1. **Single-pass** (cheapest): token entropy, perplexity, max log-probability — adequate for low-stakes use
2. **Multi-sample** (moderate cost): semantic entropy (clusters responses by meaning via NLI models), conformal prediction with formal statistical coverage guarantees
3. **Post-hoc calibration** (recommended for deployed systems): TAC or similar recalibration

Prompt-based mitigation can cut hallucination rates substantially (GPT-4o: 53% to 23% in one study), while temperature adjustments alone barely move the needle. Structural calibration approaches outperform prompt-based approaches for sustained reliability.

## Design Principle

"The model saying 'done' is not enough." Self-reported completion is not a verification signal. Build systems that check outputs against deterministic criteria — test execution, schema validation, factual cross-reference — rather than trusting model confidence as a proxy for correctness.
