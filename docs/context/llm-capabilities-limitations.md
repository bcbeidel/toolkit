---
name: "LLM Capabilities and Limitations"
description: "What LLMs do reliably vs. where they fail, and six architectural principles for agent design"
type: reference
sources:
  - https://arxiv.org/abs/2307.03172
  - https://arxiv.org/abs/2311.05232
  - https://arxiv.org/abs/2305.18654
  - https://arxiv.org/abs/2402.01817
  - https://arxiv.org/abs/2310.01798
  - https://arxiv.org/abs/2310.13548
  - https://arxiv.org/abs/2207.05221
  - https://arxiv.org/abs/2305.20050
related:
  - docs/research/llm-capabilities-limitations.md
  - docs/research/prompt-engineering.md
  - docs/context/prompt-engineering.md
  - docs/context/context-window-management.md
---

LLMs are reliable generators but unreliable verifiers. They produce coherent text, extract patterns, and approximate knowledge well. They fail at autonomous planning, self-correction without external feedback, and consistent reasoning over complex multi-step tasks. Agent architectures must treat LLMs as draft-generators paired with external verification, not as autonomous reasoners.

## Six Failure Modes

**Hallucination.** LLMs fabricate information from parametric memory (extrinsic hallucination) and contradict provided context (intrinsic hallucination). Extrinsic hallucination is more dangerous because it produces confident outputs with no grounding signal to detect. The most fluent outputs may be the least reliable. Chain-of-Verification (CoVe) mitigates this by forcing the model to verify its claims from independent angles before finalizing.

**Attention decay.** Models perform best when relevant information appears at the beginning or end of context. Performance degrades significantly for information in the middle of long contexts. Larger context windows do not solve this — a 100K window where the model ignores the middle 60K tokens is worse than a well-structured 20K prompt with critical information at boundaries.

**Compositional reasoning breakdown.** Transformers solve compositional tasks through pattern-matching against training data, not systematic reasoning. Performance rapidly decays with increased task complexity. This is architectural: autoregressive generation reduces multi-step reasoning to sequential token prediction.

**Planning incapability.** LLMs cannot plan or self-verify autonomously. They function as approximate knowledge sources that suggest plausible plans but cannot verify whether plans achieve goals. The LLM-Modulo framework proposes pairing LLM generation with external symbolic verification.

**Self-correction failure.** LLMs struggle to self-correct without external feedback, and performance sometimes worsens after self-correction attempts. Intrinsic self-correction (no new information) fails; extrinsic correction (external feedback) works. Apparent self-improvement through iterative critique comes from correct solutions being present in top-k sampling, not genuine error analysis.

**Sycophancy.** RLHF-trained models systematically prefer agreement over correctness. This extends beyond user-pleasing to confirmation bias toward any framing in the prompt, including framing from other agents in multi-agent systems. Both humans and preference models prefer sycophantic responses over correct ones, reinforcing this pattern during training.

## Reliable Strengths

**Text generation and transformation** — coherent output given clear instructions, including translation, summarization, and reformatting. **Approximate knowledge retrieval** — generating plausible candidates for plans, code, hypotheses, and factual claims. **Critique generation** — identifying flaws that human evaluators miss, scaling with model size. **Process-supervised reasoning** — when reasoning is broken into individually verified steps, performance improves substantially (78% on MATH benchmarks vs. outcome-only supervision).

## Calibration

Token-level probabilities on structured queries (multiple choice, true/false) provide rough uncertainty signals. Calibration breaks down on unfamiliar task distributions, in free-form generation, and during self-evaluation. Multi-sample consistency — asking the same question multiple ways and checking agreement — is more reliable than any single-response confidence expression.

## Design Principles for Agent Systems

1. **Generate, don't verify.** Use LLMs to produce candidates. Use deterministic systems or independent LLM instances to verify.
2. **Verify steps, not outcomes.** Process supervision — checking each reasoning step — outperforms outcome-only checks. Build verification gates between pipeline stages.
3. **Structure context for attention.** Place instructions at the start, output format at the end. Keep retrieved context concise and at boundaries.
4. **Use external signals for confidence.** Multi-sample consistency beats free-form confidence expressions. Do not trust "I'm X% confident" statements.
5. **Design for disagreement.** Counter sycophancy with adversarial prompting, independent verification, and explicit reward for uncertainty expression.
6. **Scope tasks to strengths.** LLMs excel at generation, pattern matching, retrieval, and critique. They fail at autonomous planning, multi-step reasoning, and self-correction.
