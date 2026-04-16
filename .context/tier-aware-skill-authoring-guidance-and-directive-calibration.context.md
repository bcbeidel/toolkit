---
name: "Tier-Aware Skill Authoring Guidance and Directive Calibration"
description: "Anthropic is the only framework with tier-specific skill authoring guidance; the guidance is heuristic, not empirical, and directive density calibrates inversely with model capability"
type: context
sources:
  - https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
  - https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
  - https://arxiv.org/abs/2310.11324
related:
  - docs/research/2026-04-11-prompting-techniques-model-tiers.research.md
  - docs/context/format-sensitivity-and-cross-model-defaults.context.md
  - docs/context/instruction-capacity-and-context-file-length.context.md
  - docs/context/few-shot-examples-tier-loading-and-cross-tier-stability.context.md
  - docs/context/cot-tier-threshold-and-skill-authoring.context.md
  - docs/context/persona-framing-accuracy-cost-and-task-boundary.context.md
---
Anthropic publishes the only major framework guidance that explicitly differentiates skill authoring by model tier. That guidance is heuristic, not empirically measured — a useful reference, but not a substitute for testing. Directive density (ALL-CAPS, MUST, CRITICAL) calibrates inversely with model capability, and no formal tier annotation standard exists.

## Anthropic's Tier-Specific Heuristics

Anthropic's Skill Authoring Best Practices differentiates three tiers: Haiku ("does the skill provide enough guidance?"), Sonnet ("is it clear and efficient?"), Opus ("does it avoid over-explaining?"). No other major framework or model provider publishes equivalent guidance. OpenAI publishes no tier-specific prompting guide for GPT-4o vs. GPT-4o-mini differences. LangChain and LlamaIndex support tiered model routing architecturally but publish no prompt authoring guidance differentiated by model tier.

This guidance is framed as testing considerations, not measured thresholds. No Anthropic benchmark data comparing instruction length or format sensitivity across Haiku/Sonnet/Opus has been published. It is directional heuristic, and should be treated as such — useful for calibration, not a replacement for empirical skill testing.

## Directive Density Inverts With Capability

Anthropic explicitly deprecated ALL-CAPS and MUST-style directives for Opus 4.5+: "Where you might have said 'CRITICAL: You MUST use this tool when...', you can use more normal prompting like 'Use this tool when...'" This represents the clearest published evidence that directive density calibrates inversely with capability — stronger directives were appropriate for earlier or weaker models, and are now unnecessary (and potentially counterproductive) for frontier models.

The implication for cross-tier work: WOS skills targeting sub-frontier models may legitimately need stronger directive language than frontier-calibrated criteria would allow. The WOS check-skill ALL-CAPS directive density criterion correctly identifies frontier-tier over-engineering, but skills verified to run on smaller models are not miscalibrated if they use stronger directive forms.

## The Unreliability of Tier Annotations

No academic, framework, or industry source describes a minimum model tier annotation for skill definitions as a standardized practice. The concept does not exist as a formal specification. Evidence against its reliability: format performance only weakly correlates between models (arXiv 2310.11324). A skill's success on Sonnet does not reliably predict success on Haiku, even accounting for tier. Specific task-format-instruction combinations create idiosyncratic behavior that tier alone does not capture.

A `min_model_tier` frontmatter field would lack both an anchoring standard and sufficient predictive reliability to be actionable.

## A More Honest Signal: `tested_with`

The most practical form of tier signaling found in production is Anthropic's informal test checklist — a verification record of which models the skill author tested against. A `tested_with` list is more honest and more actionable than a forward-looking `min_model_tier` capability claim. It describes what is known, not what is predicted.

WOS skill authors should note which models they verified a skill against. Cross-tier skills should be verified against at least one sub-frontier target before treating examples and directive choices as optional.
