---
name: Prompt Drift — Types and Detection Hierarchy
description: "Three distinct drift types (data, concept, model) require different detection approaches; model-based detection (binary classifier + ROC AUC) is the recommended default over Wasserstein distance."
type: concept
confidence: high
created: 2026-04-10
updated: 2026-04-10
sources:
  - https://docs.aws.amazon.com/prescriptive-guidance/latest/gen-ai-lifecycle-operational-excellence/prod-monitoring-drift.html
  - https://orq.ai/blog/model-vs-data-drift
  - https://medium.com/@EvePaunova/tracking-behavioral-drift-in-large-language-models-a-comprehensive-framework-for-monitoring-86f1dc1cb34e
related:
  - docs/context/prompt-immutable-versioning-and-attribution.context.md
  - docs/context/prompt-regression-deterministic-first-assertion-layering.context.md
  - docs/context/knowledge-confidence-lifecycle-and-state-tracking.context.md
---
# Prompt Drift — Types and Detection Hierarchy

Prompt drift has three distinct causes, each requiring a different detection approach. Treating them as one problem leads to applying the wrong detection method and missing the actual signal.

## Three Drift Types

**Data drift** — statistical change in input distributions: topics shift, vocabulary changes, user intent evolves. The prompt has not changed; the population of inputs it receives has. Detectable via embedding distribution comparison between a reference window and a current window.

**Concept drift** — the relationship between inputs and desired outputs shifts. What users expect from the system has changed, or domain semantics have evolved. Harder to detect than data drift because it requires business metric monitoring and user feedback signals, not just input distribution analysis.

**Model drift** — the model provider silently updates the underlying model. Output behavior changes without any prompt change. This is the most insidious type: your prompts are identical, your inputs are identical, but your outputs are different. Provider changelogs and behavioral benchmarking are the primary detection mechanisms.

**Editorial "prompt drift"** is a fourth category: incremental edits to prompt templates that individually seem harmless but cumulatively alter instructions, tone, or constraints. Immutable versioning is the primary prevention mechanism — forcing explicit version creation for any change makes cumulative drift visible.

## Detection Hierarchy — Start Simple

EvidentlyAI recommends a binary classifier (ROC AUC) as "the preferred default" for embedding drift detection:
- Interpretable threshold
- Consistent behavior across embedding models
- Lower setup cost than statistical methods

**Wasserstein distance** is technically defensible and more sensitive to distribution shape, but computationally intensive, requires threshold tuning, and shows inconsistent behavior on noisier baseline datasets. Use it as a step-up option for teams with mature monitoring infrastructure, not as the starting point.

**LLM-as-judge semantic classification** is useful for drift characterization once a statistical signal is detected — to categorize what kind of shift occurred (new topic, intent shift, complexity increase). Subject to the same reliability caveats as general LLM-as-judge use (see sibling file).

## Prevention Is Cheaper Than Detection

Immutable versioning, CI regression gates, and statistical input monitoring together prevent most drift from going undetected. The detection hierarchy is a monitoring backstop, not a substitute for preventive discipline.

For teams starting monitoring:
1. Start with model-based drift detection (binary classifier on embeddings)
2. Add behavioral benchmarking — 15–20 synthetic benchmark prompts across instruction-following, factuality, and reasoning; 10 runs per version for statistical reliability
3. Add LLM-as-judge for drift characterization once statistical detection is working
4. Add Wasserstein distance only when simpler methods produce too many false signals

**The takeaway:** Distinguish data drift, concept drift, and model drift — each has a different cause and different mitigation. Default to binary classifier + ROC AUC for detection. Immutable versioning is the first line of prevention before drift detection is even needed.
