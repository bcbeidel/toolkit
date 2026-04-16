---
name: LLM Code Review — Commenters Not Gatekeepers
description: LLMs are unreliable standalone reviewers (best independent F1 19.38%); the correct architecture keeps them as first-pass commenters with human approval gates.
type: concept
confidence: high
created: 2026-04-10
updated: 2026-04-10
sources:
  - https://arxiv.org/html/2509.01494v1
  - https://arxiv.org/html/2505.20206v1
  - https://arxiv.org/html/2505.16339v1
  - https://docs.github.com/en/copilot/concepts/agents/code-review
  - https://arxiv.org/abs/2502.08177
related:
  - docs/context/llm-code-review-framing-bias-and-neutral-presentation.context.md
  - docs/context/llm-code-review-context-engineering-quality-ceiling.context.md
  - docs/context/approval-gate-trust-calibration-and-overconfidence.context.md
  - docs/context/hitl-oversight-as-tuned-policy-and-reversibility-gate.context.md
---
# LLM Code Review — Commenters Not Gatekeepers

The best independently validated F1 score for AI code review on real-world change-point detection is 19.38% — achieved with PR-Review + Gemini-2.5-Pro across 11 change types. Even with multi-run aggregation (5 passes), the ceiling is still below 20%. LLM approval accuracy reaches 44.44% inaccuracy under some conditions. These numbers make autonomous merge gating a direct reliability risk.

## The Human-in-the-Loop Architecture is Mandatory

GitHub Copilot enforces this architectural constraint at the product level: it can only leave "Comment" reviews, never "Approve" or "Request changes." Academic research independently converges on the same pattern — "Human-in-the-loop LLM Code Review" where LLMs generate initial findings but humans make final merge decisions.

The correct mental model is LLMs as contextual first-pass reviewers: they reduce ramp-up time on large or unfamiliar PRs, surface potential issues early, and free human reviewers from low-signal scanning. They do not replace the human approval decision.

## Where LLMs Add Value

LLMs are most reliable for functional defects: logic errors and resource issues reach 26.20% F1 on independent benchmarks, and GPT-4o corrects 67.83% of buggy code when given problem descriptions. A field study at WirelessCar found LLMs caught subtle defects like race conditions that humans might miss.

Two validated interaction modes:
- **Co-reviewer mode** — AI generates a summary and concerns before the human starts; reduces ramp-up time on large PRs but risks anchoring reviewers to AI framing
- **Interactive assistant mode** — reviewer queries AI on demand; preserves reviewer autonomy

The optimal mode is context-dependent. Neither dominates universally.

## Where LLMs Fail

- **Evolvability** (documentation, structural, visual changes): lowest F1, under 17%
- **Consistency**: only 27 identical findings across 5 runs of the same model on the same code — inconsistency is measurable and significant
- **Interprocedural analysis**: LLMs struggle with large codebases and cross-service breaking changes; no open-source tool detected cross-service breaking changes in a 450K-file monorepo
- **Security with framing bias**: 16–93% detection drop when code is framed as "bug-free" — the most operationally dangerous failure mode (see sibling file on framing bias)

SycEval (AAAI 2025) found sycophantic behavior in 58.19% of cases across GPT-4o, Claude Sonnet, and Gemini-1.5-Pro, with regressive sycophancy (changing correct assessments to wrong ones) at 14.66%.

## Benchmark Incomparability Warning

Vendor benchmarks (e.g., Qodo's 60.1% F1 on injected defects in curated PRs) are not comparable to the independent academic 19.38% figure. They measure different things on different datasets. The true capability floor for general PR review is closer to the academic benchmark.

**The takeaway:** Use LLMs to surface candidate issues early and reduce reviewer preparation time. Remove them from the merge approval decision entirely. Multi-run aggregation (5 passes) increases F1 by up to 43.67% and is worth the latency cost for high-stakes reviews.
