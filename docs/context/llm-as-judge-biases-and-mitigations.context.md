---
name: "LLM-as-Judge Biases and Mitigations"
description: "LLM-as-judge: 14+ bias types; binary per-criterion rubrics + position swapping + sampling aggregation are best mitigations"
type: concept
confidence: high
created: 2026-04-10
updated: 2026-04-10
sources:
  - https://arxiv.org/html/2410.02736v1
  - https://arxiv.org/html/2411.15594v6
  - https://arxiv.org/html/2410.21819v2
  - https://aclanthology.org/2025.ijcnlp-long.18/
  - https://arxiv.org/abs/2409.15268
  - https://arxiv.org/abs/2601.08654
  - https://www.evidentlyai.com/llm-guide/llm-as-a-judge
  - https://arxiv.org/abs/2410.02736
related:
  - docs/context/rubric-specificity-and-deterministic-first-evaluation.context.md
  - docs/context/confidence-calibration-and-self-correction.context.md
  - docs/context/skill-behavioral-testing-layer-gap.context.md
  - docs/research/2026-04-11-llm-skill-behavioral-testing.research.md
---
LLM-as-judge has at least 14 distinct bias types, and no mitigation strategy fully removes any of them. The CALM framework's catalog of 12 biases misses two operationally critical ones discovered in subsequent research. The practical approach: design around the most severe biases with structural countermeasures, not trust.

## The 14+ Bias Types

The CALM framework (Ye et al., 2024) catalogs 12 types:

**Position bias** is the most severe. All models scored below 0.5 robustness when evaluating 3-4 candidates. GPT-4's judgment flipped when answer positions were swapped. A systematic study across 150,000+ evaluation instances confirmed position bias is "not due to random chance" — it is most strongly affected by judge model choice, not task complexity.

**Self-enhancement bias**: GPT-4 exhibits a 0.520 bias score with true positive rate 0.945 versus true negative rate 0.425 — a systematic discrepancy. Using a different model family for judging (e.g., Claude judging GPT-4o outputs) avoids this.

**Verbosity bias**: preference for longer responses, with complex model-specific patterns — some models show aversion to excess length, others show positive correlation.

Additional CALM biases: compassion-fade, bandwagon, distraction, fallacy-oversight, authority, sentiment, diversity, chain-of-thought, refinement-aware.

**Two missing biases from later research:**
- **Style-over-substance bias** (Feuer et al., ICLR 2025): judge preferences "do not correlate with concrete measures of safety, world knowledge, and instruction following" — judges prioritize stylistic preferences over factuality
- **Code-specific superficial bias** (Moon et al., EACL 2026): all tested LLM judges are susceptible to biases from variable names, comments, and formatting that should not affect correctness judgments

## No Mitigation Is Complete

The CALM authors state: mitigation strategies "often suffer from incomplete bias removal, added complexity, the introduction of new biases, inconsistent effectiveness, or impracticality for closed-source models."

Non-determinism is a structural threat independent of biases: inter-rater reliability ranges from 0.167 to 1.00 depending on random seed variation. Single-output evaluations mask inherent judgment variability, creating false reliability signals.

## Best Available Mitigations

**Position swapping**: evaluate in both orderings, average scores. Most widely recommended and most consistently effective mitigation for position bias.

**Cross-model judging**: use a different model family to avoid self-enhancement bias. Claude judging GPT outputs, GPT judging Claude outputs.

**Binary scoring**: reduces clustering and scale-dependent biases. LLMs cluster scores in the middle of Likert scales, introducing arbitrary variance. Binary outputs produce more stable evaluations.

**Sampling-based aggregation**: mean aggregation over multiple samples achieves 0.666 correlation versus 0.635 for greedy decoding — approximately 5% improvement. Krippendorff's alpha reaches 0.908 for GPT-4o on BIGGEN-Bench with sufficient samples.

**Ensemble evaluation**: diverse model panels outperform any single judge. AutoRubric's per-criterion atomic evaluation in separate LLM calls prevents halo effects and criterion conflation.

## Practical Design

Chain-of-thought can amplify biases — bandwagon effects and verbosity bias both amplify in collaborative debate settings. CoT's primary value in evaluation is compensating for rubric underspecification, not universally improving judgment quality.

Sycophancy as an evaluation failure mode: when an LLM judge is asked to evaluate another LLM's output, sycophantic tendencies may cause systematic overscoring. This is distinct from self-enhancement bias and affects cross-model evaluation.

Agent-as-a-Judge (Zhuge et al.) achieves ~90% human agreement on code-generation tasks versus ~70% for single-pass LLM-as-a-Judge, at approximately 97% cost reduction. For code compliance where tests can be run, agentic evaluation is qualitatively superior to single-pass judgment.

## Non-LLM Alternatives at Layer 2–3

Pre-trained classifiers and embedding similarity provide a non-LLM evaluation layer that avoids the second non-determinism problem entirely. These are preferred for properties that can be modeled deterministically:

- **Pre-trained classifiers** (toxicity, sentiment, tone, emotional register) — evaluated with a fixed model, producing stable scores independent of the judge LLM's version or sampling variability. Evidently AI's regression testing framework uses these as primary behavioral checks before invoking LLM-as-judge.
- **Embedding cosine similarity** — compare output embeddings against golden examples using a threshold (≥0.9 cosine similarity detects meaningful semantic drift). No LLM API call required; runs in milliseconds per assertion.

These approaches occupy the Layer 2–3 gap (see `skill-behavioral-testing-layer-gap.context.md`) and are recommended before adding LLM-as-judge to an eval pipeline.

## Agreement Rate Degradation for Specialized Tasks

The 80%+ human agreement figure from Zheng et al. (2023) applies to general instruction-following tasks with GPT-4 as judge. This figure degrades substantially for specialized and open-ended evaluation tasks. Multiple sources document agreement rates in the ~47–58% range for domain-specific or open-ended assessment — a level close to random for binary judgments.

For WOS skill evaluation — assessing routing precision, instruction density, agentic behavior quality — the 80% baseline cannot be assumed. These are specialized meta-level qualities that the general-domain agreement studies did not evaluate. The 80% figure provides a ceiling under optimal conditions, not a floor for arbitrary skill evaluation tasks. Any decision to adopt LLM-as-judge for WOS skill quality assessment should include a human calibration study on a representative sample before treating scores as reliable.
