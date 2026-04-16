---
name: LLM Audit Prompt Anatomy
description: Six structural elements required for stable LLM rule evaluation prompts. The criterion statement is the highest-leverage element (removing it drops human correlation by 26%). Evidence-before-verdict ordering is a structural requirement, not a stylistic preference. Evaluation and repair must be separate calls.
type: concept
confidence: high
created: 2026-04-13
updated: 2026-04-13
sources:
  - https://arxiv.org/abs/2601.08654
  - https://arxiv.org/html/2503.23989v1
  - https://arxiv.org/html/2501.00274v1
  - https://aclanthology.org/2025.coling-main.710.pdf
  - https://www.promptfoo.dev/docs/configuration/expected-outputs/model-graded/llm-rubric/
related:
  - docs/research/2026-04-13-rule-repair-eval-prompts.research.md
  - docs/context/llm-rule-structural-characteristics.context.md
  - docs/context/rule-repair-strategies-by-failure-mode.context.md
  - docs/context/rubric-specificity-and-deterministic-first-evaluation.context.md
---

# LLM Audit Prompt Anatomy

## Key Insight

Five independent T1 studies converge on six structural elements required for stable LLM rule evaluation. The criterion statement is the highest-leverage element — removing it drops correlation with human judgment from 0.666 to 0.487. Evidence-before-verdict ordering is not stylistic: prompts that emit verdict first produce confirmation bias where reasoning rationalizes the pre-committed verdict rather than deriving from evidence. Evaluation and repair generation must be separate calls to preserve evidence-anchored integrity.

## Six Required Elements

An evaluation prompt for rule auditing must contain all six:

1. **Criterion statement** — a single precise behavioral definition of the dimension being evaluated. Not "is this rule well-specified?" but "does the scope glob include a directory prefix that targets a specific architectural layer rather than matching all files of an extension?" Observable behavioral definition, not a quality label.

2. **PASS/FAIL scale declaration with behavioral definitions** — binary for compliance decisions. Define what PASS means and what FAIL/WARN means in observable terms. Do not use 1–5 or percentage scales for compliance decisions — binary produces more stable inter-run consistency.

3. **Anchor examples** — one PASS anchor and one FAIL anchor demonstrating the criterion. Without these, LLMs default to PASS on ambiguous cases. Anchors must demonstrate observable behavior, not label quality levels.

4. **Evidence requirement with CoT** — explicit instruction: "Explain your reasoning and cite the specific text from the rule that supports your verdict, before stating your verdict." Chain-of-thought is mandatory for auditable enforcement; it makes visible whether the evaluator is applying the criterion or pattern-matching on surface features.

5. **Structured output format** — constrain output to a schema: `Dimension | Evidence (quoted from rule) | Reasoning | Verdict (WARN or PASS)`. Structured output reduces ambiguity and enables downstream aggregation.

6. **Default-closed instruction** — "When evidence is borderline, surface as WARN, not PASS." Without this, LLMs default to PASS on uncertain cases, hiding real issues. This is the default-closed stance applied to the evaluator itself.

## Evidence-Before-Verdict Ordering (Required)

The output template must enforce: `evidence → reasoning → verdict`. Not `verdict → reasoning`.

Prompts that elicit verdict before evidence produce confirmation bias: the reasoning rationalizes the pre-emitted verdict rather than deriving from it. RULERS (arXiv 2601.08654) enforces evidence-first as a hard constraint and demonstrates that evidence-anchored scoring "significantly outperforms representative baselines in human agreement."

Practical implication: the output format schema must list evidence before verdict. If you're seeing output where the verdict appears in the first sentence, the prompt is not enforcing evidence-first ordering.

## Full Rubric in One Call (Not Per-Dimension Sequential Calls)

Present all evaluation dimensions simultaneously in one call. Never split into per-dimension sequential calls.

Sequential calls score 11.5 points lower on average (Rubric Is All You Need, arXiv 2503.23989) and produce false-positive cascades. At 20–30% false positive rates, rule audit systems enter the same trust-degradation spiral that causes developers to disable rules wholesale. The single-call constraint is not an efficiency choice — it is a quality imperative.

Achieving per-dimension isolation within one call: use explicit output slots for each dimension (`## Dimension 1: Specificity` ... `## Dimension 2: Research Grounding` ...). This prevents halo effects (positive impression on one dimension inflating others) without the accuracy penalty of sequential calls.

## Evaluation and Repair: Separate Calls

Repair generation must be a separate call that receives the completed evaluation output as input. It must not be co-located within the evaluation prompt.

Interleaving repair recommendations within evaluation reasoning corrupts the evidence-anchored structure by introducing future-state reasoning ("what should be") into the assessment of current-state ("what is"). The evaluation call produces: evidence → verdict per dimension. The repair call receives those verdicts as input and produces: specific change recommendation per WARN/FAIL finding.

The repair call must also include an intent-preservation constraint: "The proposed repair must preserve the behavioral criterion in the Intent section. If any change would alter what files are in scope or what behavior is required, flag it as requiring human review."

## Locked Rubric vs. Open Generation

**Evaluation dimensions: locked.** The five check-rule audit dimensions (specificity, research grounding, staleness, fix-safety, rubric instability) are frozen specifications — not generated per-audit. Editing them ad hoc produces evaluation drift across versions. Treat them as versioned artifacts.

**Repair recommendations: open, then constrained.** The repair phase generates specific recommendations per finding — this requires generative flexibility. But constrain the output to a structured schema (CHANGE / FROM / TO / REASON) to make repair mechanically applicable without interpretation.

## Takeaway

A rule evaluation prompt missing any of the six elements will produce unreliable verdicts. The criterion statement and evidence-before-verdict ordering are the most commonly omitted and the most consequential. Run all dimensions in one call with explicit output slots per dimension. Keep evaluation and repair in separate calls.
