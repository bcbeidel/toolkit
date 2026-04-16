---
name: "Eval Pipeline CI/CD Integration and the Adoption Gap"
description: "Golden datasets and CI/CD eval pipelines enable continuous regression detection for LLM systems — but only 52% of organizations run offline evals at all, making CI/CD integration an achievable architecture rather than current industry norm."
type: concept
confidence: high
created: 2026-04-10
updated: 2026-04-10
sources:
  - https://www.braintrust.dev/articles/best-ai-evals-tools-cicd-2025
  - https://www.promptfoo.dev/docs/integrations/ci-cd/
  - https://www.getmaxim.ai/articles/building-a-golden-dataset-for-ai-evaluation-a-step-by-step-guide/
  - https://www.anthropic.com/research/statistical-approach-to-model-evals
  - https://www.langchain.com/state-of-agent-engineering
  - https://developers.openai.com/blog/eval-skills
  - https://arxiv.org/html/2508.13144v1
related:
  - docs/context/agent-testing-pyramid-uncertainty-tolerance-layers.context.md
  - docs/context/llm-judge-as-trend-detector-not-hard-gate.context.md
  - docs/context/record-replay-fixture-drift-and-metadata-verification.context.md
  - docs/context/behavioral-testing-roi-and-investment-threshold.context.md
  - docs/research/2026-04-11-llm-skill-behavioral-testing.research.md
---
## Key Insight

Continuous regression detection via eval pipelines is architecturally achievable and well-tooled. However, the LangChain State of AI Agents report (2026, N=1,340) shows only 52.4% of organizations run offline evals at all. CI/CD-integrated eval is a subset of that. "Achievable" and "adopted as the norm" are different claims — the evidence supports the former.

## The Three-Component Pipeline

The standard design divides eval infrastructure into:
1. **Datasets** — versioned collections of input/output golden pairs
2. **Experiment runners** — tools executing the application against datasets
3. **Evaluators** — scoring functions using LLM-as-judge, semantic similarity, or custom logic

"A test passes if the evaluation score meets your threshold" — treating this as automated regression testing.

## CI/CD Integration: Tool Landscape

**Promptfoo (T1):** Native support across GitHub Actions, GitLab CI, Jenkins, and CircleCI. Built-in `--fail-on-error` flag and custom threshold parsing. The most operationally complete CI/CD integration in the open-source eval space.

**Braintrust (T4):** Dedicated `braintrustdata/eval-action` GitHub Action. Posts experiment comparisons directly on PRs; links every quality change to a specific git commit.

**Langfuse and DeepEval:** More flexibility but require custom pipeline code. DeepEval integrates natively with pytest — 50+ built-in metrics covering RAG quality, agent behavior, and safety.

## Golden Dataset Construction

Maxim AI's methodology identifies five foundational elements:
1. **Defined scope** — specific tasks (agent workflows, tool use, retrieval grounding), not generic "quality"
2. **Production fidelity** — source from real logs and representative user scenarios
3. **Diversity** — varied topics, intents, difficulty levels, and adversarial cases
4. **Decontamination** — remove training data overlap through exact matching and embedding similarity checks
5. **Dynamic evolution** — continuously integrate new failure modes and updated requirements

Avoid pre-populating dynamic fields in golden templates (`actual_output`, `retrieval_context`, `tools_called`). These should be generated fresh at eval time — pre-populating defeats the evaluation's purpose.

## Statistical Rigor (Anthropic Guidance)

Naive comparison of eval scores underestimates variance. Recommendations:
- Report confidence intervals from the standard error of the mean
- Use paired-difference analysis (questions are shared across model versions)
- Apply variance reduction by resampling answers multiple times per question
- Run power analysis before evaluation to determine required sample sizes

Prefer **pass^k** (all k trials succeed) over pass@1 for production agents — users expect reliability every time.

## The Shelf-Life Problem

LLM capabilities change fast enough that eval thresholds have a "limited shelf life" (arXiv 2025). Thresholds require ongoing reassessment as model versions improve, not one-time calibration. Avoid generic pre-built metrics (hallucination scores, helpfulness scores) — they do not correlate with user satisfaction and become gaming targets disconnected from reality.

## The "10–20 Prompts" Floor Problem

OpenAI's recommendation to start with "10–20 prompts" is a floor for surfacing obvious regressions, not a steady-state target. It is not sufficient to detect distribution-specific failures. Three failure classes require scale to surface that 10–20 examples systematically miss:

- **Novel phrasings and edge cases** — a curated 10–20 set under-represents the long tail of real user inputs. Failures on unusual but valid phrasings are invisible to small golden sets.
- **Cohort-specific failures** — issues appearing only for multilingual inputs, adversarial phrasings, or specific user populations require representation of those populations in the test corpus.
- **Cascade failures** — multi-agent failures that compound across pipeline steps only emerge when the full pipeline is exercised at volume, not from isolated single-skill golden examples.

A minimum viable test suite size is empirically undefined — no source reviewed provides a principled methodology for sizing. The actionable approach: start at 10–20, then grow the test suite from production failures and discovered edge cases, not from a fixed target number.

Allen AI research (Signal and Noise, 2025) provides a related insight: selecting high-SNR test subsets (sometimes <50% of original cases) improved evaluation decision accuracy by 2–5% — meaning 40 well-chosen examples outperforms 100 noisy ones. The emphasis should be on case quality and diversity, not case count.

## Takeaway

Build eval pipelines as three components (dataset → runner → evaluator). Instrument golden datasets from production logs with diversity and decontamination. Use Promptfoo or Braintrust for the most complete CI/CD gate support. Apply statistical rigor to score comparison. Accept that eval thresholds need periodic reassessment as model capabilities shift. Treat the 10–20 starting size as a regression floor, not a ceiling — grow from production failures and edge cases. Do not assume your organization is the 52% that has evals — verify before claiming continuous regression detection.
