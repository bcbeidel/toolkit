---
name: Rule Library Operational Practices
description: "Five operational practices for maintaining LLM rule libraries — warn-before-enforce, 100 labeled examples, chain-of-thought reasoning, structured output, and positive+negative test cases."
type: concept
confidence: high
created: 2026-04-10
updated: 2026-04-10
sources:
  - https://www.evidentlyai.com/llm-guide/llm-as-a-judge
  - https://semgrep.dev/blog/2020/writing-semgrep-rules-a-methodology/
  - https://medium.com/agoda-engineering/how-to-make-linting-rules-work-from-enforcement-to-education-be7071d2fcf0
  - https://freeplay.ai/blog/defining-the-right-evaluation-criteria-for-your-llm-project-a-practical-guide
  - https://www.montecarlodata.com/blog-llm-as-judge/
related:
  - docs/context/llm-rule-structural-characteristics.context.md
  - docs/context/rule-system-failure-modes-fatigue-and-instability.context.md
  - docs/context/linter-patterns-transferable-to-llm-rules.context.md
  - docs/context/rubric-specificity-and-deterministic-first-evaluation.context.md
---
# Rule Library Operational Practices

## Key Insight

Writing a good rule is necessary but not sufficient. Rules require operational practices to deploy, calibrate, and maintain without triggering alert fatigue or rubric instability. Five practices are evidence-backed and cross-validated across LLM evaluation and code linting research.

## Practice 1: Warn-Before-Enforce

Launch rules in warning mode against known failure examples before switching to enforcement. "Give your team time to familiarize themselves with new rules and fix existing violations without disrupting development, then switch to error mode once the team is comfortable and the codebase is clean."

This applies to both human code linting and LLM evaluation pipelines. The warning period exposes miscalibrations (FPs, ambiguous criteria) before they affect production decisions. Quarterly reviews and trial periods are the recommended cadence. Legacy violations should be cleaned with automation, not forced into immediate compliance.

## Practice 2: 100 Labeled Examples Before Deployment

Before deploying a rule to production, label ~100 examples from real data — a mix of good results, edge cases, and failures. "Label data yourself first" forces intentionality about what the rule is actually measuring. Phase 2: adjust criteria where vagueness surfaced during labeling. Phase 3: continuously review new batches and expand coverage with discovered edge cases.

"Start with customer outcomes: what will success look like? What will make them disappointed?" Ground rules in observed behavior, not hypothetical categories.

## Practice 3: Chain-of-Thought Reasoning (Required)

Rules that produce only pass/fail are undebuggable and uncalibratable. "Ask the model to explain its reasoning or think step by step." This creates an auditable trail for calibration and debugging. Chain-of-thought is particularly important for borderline cases — it makes visible whether the rule is applying the intended criterion or pattern-matching on surface features.

"Chain-of-thought standardizes judgments and accelerates human understanding of alerts." It also produces structured reasoning that can be sampled for disagreement analysis.

## Practice 4: Structured Output

Constrain evaluation output to structured formats (JSON or equivalent). This "reduces ambiguity" and creates "standardized, more interpretable evaluation inputs and outputs." Structured output also enables downstream aggregation, anomaly detection over time periods, and programmatic thresholding.

Few-shot prompting with examples of structured output format is more reliable than relying on format instructions alone. Research shows a single well-structured example often works best; adding more examples can decrease consistency.

## Practice 5: Positive and Negative Test Cases

Every rule requires test cases for both positive matches (should flag) and negative non-matching cases (should not flag). Multi-collection validation before deployment. For LLM rules: test cases should be drawn from actual production data, not synthetic examples. "A rule that fires twice with 100% accuracy is more valuable than one that fires 200 times with 50% accuracy."

Track rule metrics continuously: firing frequency, false positive rates, remediation rates. Rules that are never triggered or always triggered are both miscalibrated. Quarterly review of these metrics enables evidence-based rule retirement.

## Takeaway

The operational lifecycle for any rule is: label real examples → draft rule with rationale → deploy in warning mode → measure FP/TP rates → require CoT reasoning for audits → lock rubric text as versioned artifact → review quarterly. Rules that skip steps in this lifecycle typically surface their omissions as rule system failure modes within one development cycle.
