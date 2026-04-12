---
name: "CoT Tier Threshold and Skill Authoring"
description: "Chain-of-thought prompting requires sufficient model capacity; the classic ~100B-parameter threshold has shifted down to ~7–10B for instruction-tuned models, with implications for WOS skill CoT structure"
type: context
sources:
  - https://arxiv.org/abs/2201.11903
  - https://arxiv.org/abs/2206.07682
  - https://arxiv.org/html/2404.14812v2
  - https://arxiv.org/abs/2109.01652
  - https://arxiv.org/abs/2210.11416
related:
  - docs/research/2026-04-11-prompting-techniques-model-tiers.research.md
  - docs/context/instruction-capacity-and-context-file-length.context.md
  - docs/context/tier-aware-skill-authoring-guidance-and-directive-calibration.context.md
---
CoT-structured skill instructions are safe for modern instruction-tuned models at or above approximately 7B parameters — the effective threshold has shifted substantially from the original ~100B finding. The key distinction is base pretrained vs. instruction-tuned models.

## The Original Threshold

Wei et al. (2022, NeurIPS) established that chain-of-thought prompting is harmful or neutral for models below approximately 100B parameters (10^23 training FLOPs). For base pretrained models — trained only to predict the next token — CoT elicitation requires a minimum capacity to execute multi-step reasoning. Smaller base models prompted with CoT produce worse outputs than the same models prompted without it (arXiv 2201.11903, arXiv 2206.07682).

## How Instruction Tuning Changed the Threshold

The 100B threshold applies to base pretrained models. Modern deployed models are instruction-tuned — trained on curated instruction-response pairs that bake reasoning behaviors into weights. This fundamentally changes the capacity requirement for CoT benefit.

Post-2022 evidence: instruction-tuned models at 7B–13B (Llama-2-7B, Mistral-7B, Llama-2-13B) show measurable CoT benefits via prompt engineering and CoT-tuned instruction datasets (arXiv 2404.14812). The FLAN lineage demonstrated that instruction tuning enables smaller models to perform well on tasks requiring multi-step reasoning — a 137B instruction-tuned FLAN model surpassed zero-shot 175B GPT-3 on 20 of 25 benchmarks (arXiv 2109.01652), compressing the scale advantage that base models require. Instruction-tuned models at 3B–7B show meaningfully elevated zero-shot baselines compared to same-sized base models (arXiv 2210.11416).

The operative threshold for instruction-tuned deployed models is closer to 7–10B parameters. Below this range, CoT prompting may still be harmful, particularly for models that were not CoT-tuned during instruction fine-tuning.

## Confidence

MODERATE. Multiple post-2022 T1 sources support the threshold shift, but no single paper formally revises the 100B threshold with a controlled study comparing base vs. instruction-tuned models across the same parameter range. The 7–10B estimate is derived from convergent evidence across studies, not a single definitive experiment.

## WOS Skill Authoring Implications

All practical WOS deployment targets — Claude Haiku, Sonnet, Opus, GPT-4o-mini, and mainstream open-source models — are instruction-tuned and exceed 7B parameters. CoT-structured instructions (explicit "first/then/finally" reasoning chains, step decomposition before action) are safe for these targets.

For hypothetical future deployment on very small or base models, CoT structure would need to be removed or replaced with direct instruction forms. This is not a current WOS concern but is worth noting if skill portability extends to edge-deployed base models.

The practical authoring takeaway: write CoT structure (numbered steps, explicit reasoning sequences) freely for modern instruction-tuned targets. The constraint is model capacity for multi-step execution, not CoT format sensitivity per se.
