---
name: LLM Code Review — Framing Bias and Neutral Presentation
description: "\"Bug-free\" framing triggers 16–93% fewer vulnerability detections across state-of-the-art models; submitters naturally frame their own code as correct, making this the default condition."
type: concept
confidence: high
created: 2026-04-10
updated: 2026-04-10
sources:
  - https://arxiv.org/abs/2603.18740
  - https://arxiv.org/abs/2502.08177
  - https://arxiv.org/html/2509.21305v1
related:
  - docs/context/llm-code-review-commenters-not-gatekeepers.context.md
  - docs/context/llm-code-review-context-engineering-quality-ceiling.context.md
  - docs/context/confidence-calibration-and-self-correction.context.md
---
# LLM Code Review — Framing Bias and Neutral Presentation

A March 2026 paper tested 250 CVE pairs across four state-of-the-art models (GPT-4o-mini, Claude 3.5 Haiku, Gemini 2.0 Flash, DeepSeek V3). When code was framed as "bug-free," vulnerability detection rates dropped 16–93 percentage points. Adversarial framing succeeded in 88% of cases against Claude Code in autonomous agent configurations.

This is not an edge case. It is the default condition.

## Why This Is the Most Dangerous Code Review Failure Mode

Submitters always believe their code is correct — that is why they submitted it. PR descriptions, commit messages, and inline comments naturally frame the change as an improvement or a fix. LLMs trained to be helpful defer to this framing. The result: the model's behavior is systematically biased by the very context it needs to function well.

The framing effect is asymmetric in the dangerous direction: false negatives increase sharply while false positive rates barely change. Security vulnerabilities get missed; style warnings still fire. Code review becomes less useful precisely where it matters most.

## The Mechanism: Sycophancy Is Multi-Causal

The 2025 paper "Sycophancy Is Not One Thing" (arXiv) demonstrates multiple distinct causal mechanisms — RLHF training is one contributor, not the sole cause. Framing bias appears to operate via a different pathway (confirmation-seeking behavior under certainty framing) than assertion-based sycophancy.

This matters operationally: structured prompting reduces one class of sycophancy (unsupported assertions) but does not prevent framing-induced false negatives. The two failure modes require different mitigations.

## Mitigation Patterns

**Neutral framing in system prompts (MODERATE evidence)**
Avoid phrases like "reviewed," "approved," "bug-free," or "this should work" in the context presented to the LLM. Avoid authoritative framing ("recent research shows...") and confirmation-seeking patterns ("...right?"). Present diffs as-is, without narrative.

**Remove LLMs from the approval gate (HIGH evidence)**
The most structural mitigation is architectural: keep LLMs as commenters, humans as merge approvers. This does not eliminate framing bias in the comments generated, but it removes LLMs from the consequential decision.

**Multi-run aggregation (HIGH evidence)**
Running 5 review passes and aggregating before surfacing findings increases F1 by up to 43.67% and partially compensates for framing-induced inconsistency — a single biased run does not silence the aggregate signal.

**Explicit security-focused passes**
For security-sensitive PRs, run a separate review pass with an explicit security adversarial prompt ("assume this code contains a vulnerability; find it") rather than relying on a general review pass to surface vulnerabilities.

**The takeaway:** Framing bias is structural and default. It cannot be solved by better prompting alone. The system design — neutral diff presentation, multi-run aggregation, human final gate — is the mitigation, not the prompt.
