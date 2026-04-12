---
name: "Few-Shot Examples, Tier Loading, and Cross-Tier Stability"
description: "A single few-shot example reduces prompt sensitivity across all tested model sizes; the value of examples is higher for smaller models, making examples non-optional for cross-tier skills"
type: context
sources:
  - https://arxiv.org/abs/2410.02185
  - https://arxiv.org/abs/2005.14165
  - https://arxiv.org/abs/2109.01652
  - https://arxiv.org/abs/2210.11416
related:
  - docs/research/2026-04-11-prompting-techniques-model-tiers.research.md
  - docs/context/format-sensitivity-and-cross-model-defaults.context.md
  - docs/context/tier-aware-skill-authoring-guidance-and-directive-calibration.context.md
  - docs/context/instruction-capacity-and-context-file-length.context.md
---
A single few-shot example is the most robust available technique for stabilizing output format across model tiers. Its value is highest where it is most often omitted: smaller and mid-tier models.

## The Cross-Tier Stability Finding

POSIX (arXiv 2410.02185, EMNLP 2024) tested prompt sensitivity across model sizes including 7B, 8B, and instruction-tuned variants. A single few-shot example significantly reduced prompt sensitivity across all models tested. Instruction tuning alone does not eliminate sensitivity — examples do. This is the strongest cross-tier finding for WOS skill output format stability.

## How Instruction Tuning Inverts the Base-Model Scaling Relationship

For base pretrained models, few-shot performance scales with model capacity: larger base models extract more from in-context demonstrations, and the gap between zero-shot and few-shot performance grows with model size (Brown et al. 2020, arXiv 2005.14165). This makes few-shot examples most valuable for large base models in the base-model era.

Instruction tuning breaks this relationship. Instruction tuning partially substitutes for few-shot examples by baking demonstration-like behaviors into weights. The FLAN study (arXiv 2109.01652) showed a 137B instruction-tuned model surpassing zero-shot 175B GPT-3 on 20 of 25 benchmarks. Flan-T5-XL at 3B parameters outperformed GPT-3 175B on MMLU zero-shot (arXiv 2210.11416). Instruction-tuned models at all sizes carry elevated zero-shot baselines — compressing the advantage that scale alone provided in the base-model era.

## The Inversion for Practical Deployment

In the instruction-tuned deployment world, the relationship inverts: few-shot examples are *more* critical for smaller and mid-tier models than for frontier models. Frontier instruction-tuned models have high zero-shot baselines — examples add incremental precision. Smaller instruction-tuned models have lower zero-shot baselines — examples provide a larger absolute lift, particularly for output format compliance.

For cross-tier skills (skills expected to run on Haiku, Sonnet, GPT-4o-mini, and open-source models), examples are not optional precision additions — they are load-bearing for smaller targets.

## WOS Skill Authoring Implications

Skills with specific output format requirements should include at least one `<example>` block. The rationale shifts depending on target tier:

- **Frontier models:** examples add precision and reduce variance; valuable but not always critical
- **Mid/smaller models:** examples provide the behavioral anchor that instruction tuning alone may not establish for novel output formats

For cross-tier skills, treat examples as non-optional. The cost of including an example block is fixed token overhead; the cost of omitting one is format instability on sub-frontier targets that may not surface during frontier-only testing.

The practical rule: if a skill has a structured output format or a multi-step action pattern, include at least one concrete `<example>` block regardless of the expected primary execution tier.
