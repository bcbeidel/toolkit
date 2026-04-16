---
name: "Rule Example Construction"
description: "How to construct positive and negative examples for LLM rule systems — behavioral anchoring techniques, few-shot example design, and the empirical case that concrete examples outperform prose instructions for compliance and consistency. Covers example quantity, diversity, source selection, and placement for rubric anchors, skill instructions, and evaluation criteria."
type: research
sources:
  - https://arxiv.org/abs/2005.14165
  - https://arxiv.org/abs/2109.01652
  - https://arxiv.org/abs/2210.11416
  - https://arxiv.org/abs/2410.02185
  - https://arxiv.org/html/2501.00274v1
  - https://arxiv.org/html/2503.23989v1
  - https://arxiv.org/abs/2601.08654
  - https://aclanthology.org/2025.coling-main.710.pdf
  - https://www.evidentlyai.com/llm-guide/llm-as-a-judge
  - https://www.promptfoo.dev/docs/configuration/expected-outputs/model-graded/llm-rubric/
  - https://semgrep.dev/blog/2020/writing-semgrep-rules-a-methodology/
  - https://freeplay.ai/blog/defining-the-right-evaluation-criteria-for-your-llm-project-a-practical-guide
  - https://www.agentrulegen.com/guides/how-to-write-ai-coding-rules
  - https://www.montecarlodata.com/blog-llm-as-judge/
  - https://blog.jetbrains.com/idea/2025/05/coding-guidelines-for-your-ai-agents/
related:
  - docs/research/2026-04-07-rule-enforcement.research.md
  - docs/research/2026-04-10-rules-creation-and-curation.research.md
  - docs/research/2026-04-11-prompting-techniques-model-tiers.research.md
  - docs/context/llm-rule-structural-characteristics.context.md
  - docs/context/rule-library-operational-practices.context.md
  - docs/context/few-shot-examples-tier-loading-and-cross-tier-stability.context.md
  - docs/context/linter-patterns-transferable-to-llm-rules.context.md
---

# Rule Example Construction

## Key Insights

1. **Examples outperform prose for compliance.** "Examples > paragraphs" is the practitioner consensus (agentrulegen.com), supported by the POSIX study (arXiv 2410.02185): a single few-shot example reduces prompt sensitivity significantly across all model tiers. This is not a frontier-model luxury — it is load-bearing for sub-frontier targets.
2. **Behavioral anchoring is required for calibrated rubric scoring.** Without concrete examples at each scale point, models default to "pass: true" — marking inadequate responses as passing. Anchors must describe observable behavior, not abstract descriptions of quality levels.
3. **Positive and negative examples together define the boundary.** A positive example alone defines acceptance; a negative example alone defines rejection. Both together define the evaluation boundary and substantially reduce false positive rates. Semgrep's methodology: require both before deployment.
4. **100 labeled examples before finalizing criteria.** Labeling ~100 real production examples (not synthetic) before writing a rule forces intentionality about what the rule actually measures. Edge cases visible only in real data are not discoverable through reasoning alone.
5. **Example source matters as much as example quantity.** Synthetic examples generated to illustrate a rule are less reliable than examples extracted from actual failures. Rules built from real failure cases have demonstrated coverage of the pattern that motivated the rule.
6. **A single well-constructed example often outperforms multiple weaker ones.** Research on few-shot prompting shows that more examples can decrease consistency if they introduce conflicting signals. The goal is one canonical, maximally informative example per case — not quantity.

## Research Question

How should concrete examples be constructed and embedded in LLM rule systems — covering positive cases (rule should pass), negative cases (rule should flag), behavioral rubric anchors, and few-shot instruction examples — to maximize compliance, calibration, and consistency?

## Sub-Questions

1. What does the empirical evidence say about the effect of examples on LLM rule compliance and instruction following, across model tiers?
2. What structural properties distinguish a well-constructed positive or negative rule example from a poorly constructed one?
3. How should rubric behavioral anchors be constructed for ordinal scoring rubrics used in LLM-as-judge evaluations?
4. How are production examples sourced and selected — from real failures, labeled data, or synthesized cases?
5. How many examples are sufficient, and what is the diminishing-returns curve?
6. What placement and formatting conventions maximize example utility in rule instructions and rubric criteria?

---

## Sources

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|-----------|------|------|--------|
| 1 | https://arxiv.org/abs/2005.14165 | Language Models are Few-Shot Learners (GPT-3) | Brown et al. / OpenAI | 2020 | T1 | verified |
| 2 | https://arxiv.org/abs/2109.01652 | Finetuned Language Models are Zero-Shot Learners (FLAN) | Wei et al. / Google | 2021 | T1 | verified |
| 3 | https://arxiv.org/abs/2210.11416 | Scaling Instruction-Finetuned Language Models (Flan-T5) | Chung et al. / Google | 2022 | T1 | verified |
| 4 | https://arxiv.org/abs/2410.02185 | POSIX: A Prompt Sensitivity Index for LLMs | Chatterjee et al. | 2024 | T1 | verified |
| 5 | https://arxiv.org/html/2501.00274v1 | LLM-Rubric: A Multidimensional, Calibrated Approach to Automated Evaluation | arXiv | 2025 | T1 | verified (preprint) |
| 6 | https://arxiv.org/html/2503.23989v1 | Rubric Is All You Need: Enhancing LLM-based Code Evaluation With Question-Specific Rubrics | arXiv | 2025 | T1 | verified (preprint) |
| 7 | https://arxiv.org/abs/2601.08654 | RULERS: Locked Rubrics and Evidence-Anchored Scoring | arXiv | 2026 | T1 | verified (preprint) |
| 8 | https://aclanthology.org/2025.coling-main.710.pdf | Evaluating the Consistency of LLM Evaluators | ACL Anthology (COLING 2025) | 2025 | T1 | verified |
| 9 | https://www.evidentlyai.com/llm-guide/llm-as-a-judge | LLM-as-a-judge: a complete guide | Evidently AI | 2024–2025 | T2 | verified |
| 10 | https://www.promptfoo.dev/docs/configuration/expected-outputs/model-graded/llm-rubric/ | LLM Rubric | Promptfoo (official docs) | 2025 | T1 | verified |
| 11 | https://semgrep.dev/blog/2020/writing-semgrep-rules-a-methodology/ | Writing Semgrep Rules: A Methodology | Semgrep | 2020 | T2 | verified |
| 12 | https://freeplay.ai/blog/defining-the-right-evaluation-criteria-for-your-llm-project-a-practical-guide | Defining the Right Evaluation Criteria for Your LLM Project | Freeplay | 2024–2025 | T2 | verified |
| 13 | https://www.agentrulegen.com/guides/how-to-write-ai-coding-rules | How to Write AI Coding Rules | Agent Rules Builder | 2026 | T3 | verified |
| 14 | https://www.montecarlodata.com/blog-llm-as-judge/ | LLM-As-Judge: 7 Best Practices & Evaluation Templates | Monte Carlo Data | 2024–2025 | T2 | verified |
| 15 | https://blog.jetbrains.com/idea/2025/05/coding-guidelines-for-your-ai-agents/ | Coding Guidelines for Your AI Agents | JetBrains | May 2025 | T2 | verified |

---

## Raw Extracts

### Sub-question 1: Empirical evidence for examples vs. prose on rule compliance

**From [4] (POSIX — arXiv 2410.02185):**

A single few-shot example significantly reduced prompt sensitivity across all model sizes tested (7B, 8B, and instruction-tuned variants). The key cross-tier finding: instruction tuning alone does not eliminate sensitivity to prompt phrasing. Examples do. This holds even for frontier instruction-tuned models, though the absolute lift is largest for smaller targets.

The mechanism: examples constrain the output distribution that the model samples from. A prose instruction allows wide interpretation. An example demonstrates a specific acceptable interpretation, eliminating ambiguity in output format and decision boundary.

**From [1] (GPT-3 — arXiv 2005.14165) and [2] (FLAN — arXiv 2109.01652):**

For base pretrained models, few-shot performance scales with model capacity — larger models extract more from in-context demonstrations, and the gap between zero-shot and few-shot performance grows with size. Instruction tuning partially substitutes for few-shot examples by baking demonstration-like behaviors into weights. The FLAN study showed a 137B instruction-tuned model surpassing zero-shot 175B GPT-3 on 20 of 25 benchmarks.

The practical inversion for deployment: in instruction-tuned models, examples are more critical for smaller tiers than frontier models. Frontier models have high zero-shot baselines — examples add incremental precision. Smaller instruction-tuned models have lower zero-shot baselines — examples provide larger absolute lift, particularly for output format compliance and structured task execution.

**From [13] (Agent Rules Builder):**

Practitioner consensus formulated as a design principle: "examples > paragraphs." Concrete examples are identified as one of three highest-leverage rule authoring choices (alongside NEVER/ALWAYS directives and attention gradient placement). Concrete before-and-after examples in rule definitions are listed as mandatory for any rule that governs code style, output format, or behavioral choices with more than binary interpretation.

**From [8] (COLING 2025 — Consistency of LLM Evaluators):**

"Structural elements enhancing consistency: explicit examples within criteria, clear boundaries between rating levels, specific terminology in criteria descriptions." When explicit examples were present within evaluation criteria, inter-evaluator agreement increased measurably. The effect was consistent across all model families tested.

---

### Sub-question 2: Structural properties of well-constructed positive and negative examples

**From [11] (Semgrep methodology):**

Rule test cases require both positive matches (should flag) and negative non-matching cases (should not flag). The construction guidance:

- Positive examples must exhibit exactly the pattern the rule targets — not a broader pattern that contains the target. Overly broad positive examples lead to rules that fire on cases outside the intended scope.
- Negative examples must be maximally similar to positive examples while being correct. The most diagnostic negative examples are "near-misses" — correct code that superficially resembles the violation pattern. Generic correct code adds little to no diagnostic value as a negative example.
- "Making it easy for developers to provide feedback on the signal quality of a rule is quite valuable for building a continuous scanning system." The negative case set grows over time as false positives are reported — each FP becomes a new negative test case.

**From [9] (Evidently AI — LLM-as-Judge):**

Effective examples in LLM evaluation rules:
- Explain the meaning of the score level they anchor
- Demonstrate the observable characteristic, not just label it
- Account for edge cases observed in data (not synthesized)
- Consider whether ambiguous situations should be flagged separately rather than forced into positive/negative

The three-option approach (pass / fail / uncertain) is noted as reducing forced classification of ambiguous examples. This applies to the evaluation system: examples should demonstrate clear positive and clear negative cases; genuinely ambiguous cases should not be used as examples — they belong in the edge case documentation.

**From [15] (JetBrains — coding guidelines for AI agents):**

JetBrains recommends including "real code examples with explanations" rather than abstract descriptions of desired behavior. The do/don't format (showing the violation alongside the correct version) is identified as the highest-utility structure for agent-facing rules: it eliminates the need for the agent to infer what the violation looks like from an abstract criterion description.

**From [6] (arXiv 2025 — Rubric Is All You Need):**

Question-specific (QS) rubrics break down problems into discrete implementation steps with binary marking per step. For code evaluation, each step's positive example is a working implementation of that step — not a description of what a working implementation contains. This distinction matters: "what correct code looks like" is often easier for the rule author to describe abstractly, but harder for the model to evaluate consistently without seeing a concrete instance.

---

### Sub-question 3: Behavioral anchors for ordinal rubric scoring

**From [10] (Promptfoo — LLM Rubric):**

The canonical behavioral anchor format: each scale point described with a concrete behavioral demonstration.

> "Score of 0.1: Only a slight smile. Score of 0.5: Laughing out loud. Score of 1.0: Rolling on the floor laughing."

Each score level specifies observable behavior — not a description of quality. The distinction: "highly relevant" is a quality label; "The response directly answers the question asked using the same terminology as the user" is an observable behavior. Only the latter anchors the score reliably.

Without behavioral anchors: "models default to assuming pass: true, potentially marking inadequate responses as passing." The default assumption is calibrated toward the positive case. Anchors shift the model's prior by demonstrating what the negative cases look like at each level.

**From [5] (arXiv 2025 — LLM-Rubric multidimensional):**

Decomposing a holistic judgment into 8 specifically anchored dimensions improved RMSE from 0.86–0.98 (worse than random) to 0.39–0.42. Each dimension required its own anchor examples. Ablation: dimensions covering "redundancy, conciseness, and efficiency" were the hardest to anchor reliably. The implication: abstract quality dimensions (concise, efficient, clean) require more concrete behavioral anchors than functional dimensions (correct, complete, error-free), because the abstract dimensions have wider disagreement among human raters that examples must resolve.

**From [7] (RULERS — arXiv 2601.08654):**

RULERS compiles rubrics into versioned, immutable bundles with deterministic evidence anchoring. The key structural finding: anchoring each score point to a specific piece of evidence from the evaluated artifact (rather than to a stand-alone example) outperforms unanchored rubrics by +0.17 QWK. This evidence-anchoring technique — "Score X applies when the artifact contains [specific feature or property]" — converts the abstract-scale problem into a pattern-matching problem, which models execute more consistently.

Rule-compiling with anchored evidence enables smaller models to rival larger proprietary judges. Rubric structure matters more than model size when anchoring is strong.

---

### Sub-question 4: Production example sourcing and selection

**From [12] (Freeplay — Evaluation Criteria):**

Before deploying a rule, label ~100 examples from real production data — a mix of good results, edge cases, and failures. "Label data yourself first" is the core practice; it forces intentionality about what the rule is actually measuring. Phase breakdown:

1. Label 100 real examples: mix good results, edge cases, and clear failures
2. Adjust criteria where vagueness surfaced during labeling
3. Draft examples from the labeled set — real data captures failure modes that synthetic examples miss
4. Continuously review new batches and expand the edge case set

"Start with customer outcomes: what will success look like? What will make them disappointed?" Ground rule examples in observed behavior, not hypothetical categories.

**From [11] (Semgrep methodology):**

"Write rules that match the exact pattern you observed in a real bug or vulnerability." The starting example must come from a real failure case observed in the codebase or in production. Synthesized examples hypothesize what violations look like; real examples demonstrate what violations actually look like — the difference surfaces in edge case coverage.

The "two for one" pattern: every new FP that is added to the negative test case list tightens the rule's precision. The negative example library grows organically from the rule's operational history.

**From [9] (Evidently AI):**

"If you have several aspects to evaluate, like completeness, accuracy, and relevance, it's best to split them into separate evaluators." When sourcing examples for multi-dimension rules, this also means sourcing examples separately per dimension. A single document that is both incomplete and inaccurate does not serve as a good example for either criterion — the signals are confounded. Examples for separate evaluation dimensions should fail cleanly on one dimension while passing the others.

---

### Sub-question 5: Example quantity and diminishing returns

**From [14] (Monte Carlo — 7 Best Practices):**

"Few-shot prompting: 'provide one or more examples demonstrating what good or bad outputs look like.' Research shows a single example often works best; adding more can decrease performance." The diminishing-returns curve is steep: the first example provides the largest lift; additional examples provide marginal benefit at best, and risk introducing conflicting signals or confusing the model about which example is canonical.

**From [4] (POSIX — arXiv 2410.02185):**

A single few-shot example significantly reduced prompt sensitivity. Additional examples were not tested against a strict diminishing-returns curve in this study, but the finding that a single example produces significant and reliable improvement supports the "one canonical example" recommendation for format and boundary-definition purposes.

**From [9] (Evidently AI):**

For LLM evaluation rubrics: the recommendation is one positive example and one negative example per scale boundary — not one example per score point on a multi-point scale. Scale points without a clear behavioral distinction do not need separate examples; the adjacent anchors define the range. Adding examples for scale points that cannot be clearly distinguished in practice introduces ambiguity rather than resolving it.

---

### Sub-question 6: Placement and formatting conventions

**From [10] (Promptfoo — LLM Rubric):**

Example placement within rubric criteria: anchors appear inline with their corresponding score level, not in a separate section. The pattern: declare the criterion, define the scoring scale, place the behavioral anchor immediately after each score definition. This proximity ensures the model evaluates the anchor in the same context as the criterion it anchors.

**From [15] (JetBrains — coding guidelines):**

Format preference for agent-facing rule examples: do/don't blocks showing the violation and the correct version side by side. This structure does not require the agent to infer what the violation looks like — it demonstrates it directly. For code rules, real code examples are strongly preferred over abstract descriptions: "what the LLM agent needs to see is what correct code looks like in your specific context, not a generic description of best practices."

**From [13] (Agent Rules Builder):**

Attention gradient: examples that appear at the start of a rule section and at the end receive more attention than examples buried in the middle. For rules with both a positive and negative example, lead with the negative (violation) example to exploit the primacy effect for the rejection case, then close with the positive (correct) example. This order sets the evaluation default to stricter before demonstrating the acceptable alternative.

The "IMPORTANT" / "NEVER" convention used in rule instructions also applies to examples: examples preceded by explicit framing ("Here is an example of what NOT to do") receive significantly more attention weight than unlabeled examples.

---

## Synthesis

### The example construction lifecycle

Effective rule examples are not authored once and frozen. They follow a construction lifecycle:

1. **Source from real failures.** Identify the real failure case that motivated the rule. The initial positive example (violation) comes from this case.
2. **Construct a maximally similar negative example.** The negative case (correct) should be as similar as possible to the violation — same structure, different outcome. Generic correct cases add minimal diagnostic value.
3. **Anchor ordinal rubric points behaviorally.** For scoring rubrics, each score point needs an observable behavior anchor, not a quality label.
4. **Validate with labeled production data.** Label 100 real examples before freezing criteria. The labeling exercise surfaces edge cases the initial examples did not cover.
5. **Expand the negative library from FPs.** Each false positive the rule generates becomes a new negative test case, tightening precision over time.
6. **One canonical example per case; resist expansion.** Adding more examples introduces conflicting signals. Prioritize one maximally informative example per case.

### The example-prose gap in agent-facing rules

Prose instructions describe what the model should do. Examples demonstrate the boundary of acceptable behavior. For LLM rule systems, the critical gap is not what the rule says but where it draws the line — and only examples, not prose, define that boundary with enough precision to produce consistent model behavior across runs and model tiers.

This gap widens with sub-frontier models. Frontier models can often infer the intended boundary from precise prose. Smaller instruction-tuned models cannot — they require examples to establish the behavioral anchor that their zero-shot baseline does not provide.

For WOS rules and skill instructions targeting cross-tier deployment, examples are not optional precision additions. They are load-bearing for the models where the skill is most likely to fail.

## Takeaway

Construct rule examples from real failures, not synthetic cases. Pair every positive example with a maximally similar negative example that fails only on the criterion being tested. For ordinal rubrics, anchor each score point with an observable behavior — not a quality label. Deploy one canonical example per case; resist adding more unless a false positive has exposed a gap in the boundary definition. Place examples close to the criterion they anchor, and frame them explicitly (NOT: / CORRECT:) to maximize attention weight.
