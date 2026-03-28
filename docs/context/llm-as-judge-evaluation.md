---
name: "LLM-as-Judge Evaluation"
description: "Using LLMs to evaluate LLM outputs: multi-trial scoring, soft failure thresholds, golden dataset regression, calibration concerns, and practical guidelines for automated quality gates"
metadata:
  type: reference
  sources:
    - https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
    - https://engineering.block.xyz/blog/testing-pyramid-for-ai-agents
    - https://towardsdatascience.com/how-we-are-testing-our-agents-in-dev/
    - https://www.confident-ai.com/blog/llm-testing-in-2024-top-methods-and-strategies
    - https://www.traceloop.com/blog/automated-prompt-regression-testing-with-llm-as-a-judge-and-ci-cd
  related:
    - docs/research/testing-non-deterministic-systems.md
    - docs/context/agent-testing-pyramid.md
    - docs/context/eval-framework-landscape.md
    - docs/context/validation-architecture.md
    - docs/context/prompt-engineering.md
---

LLM-as-judge is the practical middle ground between "can't test it" and "test it perfectly." Research shows approximately 85% alignment with human judgment -- higher than human-to-human agreement at 81%. It is the standard approach for the middle layer of the agent testing pyramid, catching quality regressions that deterministic tests cannot detect.

## How It Works

Instead of exact-match assertions, an evaluator LLM scores agent outputs against defined criteria. Three evaluation dimensions have emerged as standard axes:

- **Semantic distance:** Is the output close enough to a reference answer?
- **Groundedness:** Can claims be traced to provided context?
- **Tool usage:** Did the agent invoke the right tool with correct parameters?

The evaluator returns scores rather than binary pass/fail, enabling nuanced quality assessment across these dimensions.

## Soft Failure Model

Multiple teams have converged on a continuous scoring model that categorizes LLM evaluation scores between 0 and 1:

- **Below 0.5:** Hard failure -- the output is unacceptable
- **0.5 to 0.8:** Soft failure -- tolerable individually, but triggers a hard failure if more than 33% of tests are soft failures or more than 2 occur in a suite
- **Above 0.8:** Pass

These thresholds appear to be heuristics from practice rather than empirically derived values. Teams should calibrate them to their specific quality requirements rather than adopting defaults. The key insight is the three-tier model itself, not the specific numbers.

## Multi-Trial Evaluation

Non-deterministic variance means a single evaluation run can produce misleading results. The standard mitigation is multi-trial evaluation: run the same evaluation 3+ times and take the majority result. Block Engineering runs LLM-as-judge evaluations three times; Anthropic defines each attempt at a task as a "trial" and recommends multiple trials for consistency.

The tradeoff is cost -- running evals 3x triples LLM judge costs. For expensive evaluations, teams may accept single-trial results for high-confidence scores (above 0.9 or below 0.3) and only multi-trial ambiguous scores.

## Golden Dataset Regression

Traditional snapshot testing adapts into golden dataset testing for LLM systems. Maintain 20-50 curated input-output pairs covering common use cases and known failure modes. The best test cases come from real production traffic and actual failures.

Rather than exact comparison, use fuzzy matching: cosine similarity on embeddings or BERTScore to detect semantic drift. This catches meaningful regressions while tolerating the natural variance in LLM outputs. Thresholds for fuzzy matching are not standardized -- teams must calibrate through experimentation.

Prompt regression testing extends this: when a prompt changes, automated evaluation verifies the new version meets the same quality thresholds as the previous version. CI/CD gates fail the build if quality regresses.

## Calibration Concerns

LLM judges have known biases: position bias (favoring content that appears first), length bias (favoring longer responses), and inconsistent reasoning when judge prompts change. This creates a "testing your tests" problem -- judge prompts themselves need validation.

Practical mitigations:
- Maintain a small set of human-graded examples to calibrate judge accuracy
- Test judge prompts against known-good and known-bad examples before deploying
- Rotate position of candidate outputs to detect position bias
- Monitor judge score distributions over time for drift

The circular validation concern (using LLMs to test LLMs) is real but manageable. LLM-as-judge works best as one layer in a multi-layer strategy, not as the sole quality gate. Pair it with deterministic structural assertions below and periodic human review above.

## Key Takeaway

Start with the cheapest evaluation that catches the failure mode. Structural assertions first, LLM-as-judge for semantic quality, human review for ambiguous cases. Build golden datasets from real failures, not synthetic examples. Always test the judge.
