---
name: "Persona Framing Accuracy Cost and Task Boundary"
description: "Expert persona framing in system prompts consistently reduces factual accuracy across model sizes; the harm concentrates on knowledge-retrieval tasks and worsens at larger scales"
type: context
sources:
  - https://arxiv.org/abs/2311.10054
  - https://aclanthology.org/2024.findings-emnlp.888/
  - https://arxiv.org/abs/2603.18507
  - https://arxiv.org/abs/2508.19764
  - https://best.openssf.org/Security-Focused-Guide-for-AI-Code-Assistant-Instructions
  - https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
related:
  - docs/research/2026-04-11-prompting-techniques-model-tiers.research.md
  - docs/context/prompt-design-principles-framing-and-emphasis.context.md
  - docs/context/tier-aware-skill-authoring-guidance-and-directive-calibration.context.md
---
Expert persona framing in system prompts reliably reduces factual accuracy across model sizes from 7B to 72B. The mechanism is not about model capability — it is about where the model directs attention. Personas redirect computation toward acting like the persona rather than retrieving pretraining knowledge.

## The Core Evidence

A controlled study (arXiv 2311.10054, EMNLP 2024 Findings) tested 9 open-source models across 4 families on knowledge-retrieval tasks. No persona condition led to statistically better factual performance. Adding personas consistently degraded accuracy, and the degradation was worse for larger models — Llama3-70B showed more negative effects than smaller models in the same family.

The PRISM paper (arXiv 2603.18507) quantified the MMLU accuracy cost: 71.6% baseline → 68.0% with a minimum persona → 66.3% with a long persona. The mechanism is explicit: the model prioritizes acting like the persona over retrieving factual knowledge from pretraining weights.

## Task-Type Boundary

The harm is task-type dependent. Expert personas show MT-Bench gains in generation-heavy categories: STEM (+0.60 points) and Extraction (+0.65 points). For open-ended generation, advice, and reasoning tasks, carefully designed expert personas can help — but this benefit concentrates in larger, more capable models and involves generating plausible text rather than retrieving known facts.

The task-type split: **factual retrieval and validation → personas hurt; open-ended generation → personas may help for capable models.** The research and audit tasks in WOS skill authoring fall squarely in the first category.

## Security Generalization

The OpenSSF Security-Focused Guide for AI Code Assistant Instructions (Aug 2025) found that persona prompting produced the highest average security weakness count among all evaluated prompting techniques. This is a security-context finding, not a claim about general task performance — but it reinforces that persona framing introduces risk in precision-sensitive work.

## Confidence

HIGH for factual task harm — 9-model study with consistent direction, confirmed by PRISM paper with measured MMLU drops. MODERATE for generation task benefit — task-type distinction is inferred from convergent evidence across studies, not directly compared in a single controlled experiment.

## WOS Skill Authoring Implications

WOS skills should avoid strong expert persona framing. The critical distinction:

- **Behavioral role framing** ("you are a helpful assistant that...") is lower risk — it shapes tone and interaction style without asserting expertise claims that redirect knowledge retrieval.
- **Expertise claims** ("you are a world-class security researcher") are higher risk — they trigger the persona-over-knowledge mechanism identified in the studies.

Skills requiring factual precision — research, audit, validation — should use no persona framing at all. The Anthropic recommendation to "give Claude a role" is compatible with the evidence if read as weak behavioral framing, not expertise framing. No WOS skill requires strong expert persona assertions to execute correctly.
