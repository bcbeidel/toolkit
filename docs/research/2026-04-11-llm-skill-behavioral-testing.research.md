---
name: "LLM Skill Behavioral Testing: Validation Approaches and Regression Patterns"
description: "Behavioral testing for LLM skills: all major eval frameworks converge on a three-layer architecture (deterministic → semantic → LLM-as-judge); structural linting reliably misses tone regression, factual drift, and cascade failures; CI hard-blocking gates are contested — trend monitoring is the more defensible pattern; for WOS-class meta-artifacts, golden datasets are perishable across model updates, making high-quality structural validation plus human review the dominant strategy."
type: research
sources:
  - https://www.promptfoo.dev/docs/integrations/ci-cd/
  - https://www.promptfoo.dev/docs/intro/
  - https://www.braintrust.dev/articles/llm-evaluation-guide
  - https://www.braintrust.dev/articles/how-to-eval
  - https://www.braintrust.dev/docs/core/experiments
  - https://docs.langchain.com/langsmith/evaluation-concepts
  - https://blog.langchain.com/regression-testing/
  - https://developers.openai.com/blog/eval-skills
  - https://developers.openai.com/cookbook/examples/evaluation/getting_started_with_openai_evals
  - https://developers.openai.com/api/docs/guides/evaluation-best-practices
  - https://www.llamaindex.ai/blog/evaluating-rag-with-deepeval-and-llamaindex
  - https://www.evidentlyai.com/llm-guide/llm-as-a-judge
  - https://www.evidentlyai.com/blog/llm-regression-testing-tutorial
  - https://www.traceloop.com/blog/automated-prompt-regression-testing-with-llm-as-a-judge-and-ci-cd
  - https://langfuse.com/blog/2025-10-21-testing-llm-applications
  - https://arxiv.org/html/2508.20737v1
  - https://arxiv.org/html/2412.05579v2
  - https://arxiv.org/html/2508.13144v1
  - https://deepchecks.com/llm-production-challenges-prompt-update-incidents/
  - https://galileo.ai/blog/llm-testing-strategies
  - https://dev.to/stuartp/testing-llm-prompts-in-production-pipelines-a-practical-approach-349b
  - https://arxiv.org/abs/2410.02736
  - https://arxiv.org/abs/2601.22025
  - https://newsletter.pragmaticengineer.com/p/evals
related: []
---

# LLM Skill Behavioral Testing: Validation Approaches and Regression Patterns

## Sub-questions

1. What eval-driven development patterns exist across OpenAI Evals, LangSmith, LlamaIndex, Promptfoo, and Braintrust for skill-level behavioral testing?
2. How do frameworks handle LLM non-determinism in output assertions?
3. What granularity of testing gives the best signal-to-noise vs. effort?
4. Do any frameworks distinguish structural linting from behavioral validation — what failure modes does structural checking miss?
5. What CI integration patterns are viable in production?
6. Is there ROI evidence for behavioral testing of LLM skills?

---

## Search Protocol

| # | Query | Results | Sources Pursued |
|---|-------|---------|----------------|
| 1 | Promptfoo LLM testing prompt evaluation CI integration 2024 2025 | 10 | promptfoo.dev/docs/integrations/ci-cd/, promptfoo.dev/docs/intro/ |
| 2 | Braintrust LLM eval application testing behavioral regression | 10 | braintrust.dev/articles/llm-evaluation-guide, braintrust.dev/articles/how-to-eval, braintrust.dev/docs/core/experiments |
| 3 | LangSmith prompt testing regression evaluation LLM workflows | 10 | docs.langchain.com/langsmith/evaluation-concepts, blog.langchain.com/regression-testing/ |
| 4 | OpenAI Evals framework application testing skill evaluation 2024 | 10 | developers.openai.com/blog/eval-skills, developers.openai.com/cookbook/examples/evaluation/getting_started_with_openai_evals, developers.openai.com/api/docs/guides/evaluation-best-practices |
| 5 | LLM behavioral testing non-determinism handling approaches property-based snapshot | 10 | arxiv.org/html/2508.20737v1 |
| 6 | LLM-as-judge evaluation methodology 2024 2025 best practices | 10 | evidentlyai.com/llm-guide/llm-as-a-judge, arxiv.org/html/2412.05579v2 |
| 7 | LLM prompt regression testing CI integration production patterns 2024 | 10 | traceloop.com/blog/automated-prompt-regression-testing-with-llm-as-a-judge-and-ci-cd, langfuse.com/blog/2025-10-21-testing-llm-applications, deepchecks.com/llm-production-challenges-prompt-update-incidents/ |
| 8 | structural vs behavioral LLM prompt validation failure modes linting | 10 | deepchecks.com/llm-production-challenges-prompt-update-incidents/ |
| 9 | LlamaIndex evaluation framework RAG testing 2024 2025 | 10 | llamaindex.ai/blog/evaluating-rag-with-deepeval-and-llamaindex |
| 10 | LLM evaluation ROI production failures prevented cost benefit 2024 | 10 | confident-ai.com/blog/the-ultimate-llm-evaluation-playbook (fetched — no quantitative data) |
| 11 | snapshot testing LLM outputs golden test regression prompt engineering | 10 | evidentlyai.com/blog/llm-regression-testing-tutorial |
| 12 | LLM testing granularity unit integration behavioral property-based signal noise ratio | 10 | arxiv.org/html/2508.13144v1, galileo.ai/blog/llm-testing-strategies |
| 13 | LLM evaluation test suite size dataset minimum cases regression quality | 10 | (search summary used; braintrust/evidentlyai already fetched) |
| 14 | Anthropic Claude skill testing evaluation prompt workflow CI patterns 2024 2025 | 10 | anthropic.com/engineering/AI-resistant-technical-evaluations (fetched — candidate eval focus, not skill testing) |

---

## Sources

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|-----------|------|------|--------|
| 1 | https://www.promptfoo.dev/docs/integrations/ci-cd/ | CI/CD Integration for LLM Eval and Security | Promptfoo | 2025 | T1 | verified |
| 2 | https://www.promptfoo.dev/docs/intro/ | Intro | Promptfoo | 2025 | T1 | verified |
| 3 | https://www.braintrust.dev/articles/llm-evaluation-guide | What is LLM evaluation? A practical guide to evals, metrics, and regression testing | Braintrust | 2024–2025 | T1 | verified |
| 4 | https://www.braintrust.dev/articles/how-to-eval | How to eval: The Braintrust way | Braintrust | 2024–2025 | T1 | verified |
| 5 | https://www.braintrust.dev/docs/core/experiments | Evaluate systematically | Braintrust | 2025 | T1 | verified |
| 6 | https://docs.langchain.com/langsmith/evaluation-concepts | Evaluation concepts | LangChain / LangSmith | 2025 | T1 | verified |
| 7 | https://blog.langchain.com/regression-testing/ | Regression Testing with LangSmith | LangChain | 2024 | T1 | verified |
| 8 | https://developers.openai.com/blog/eval-skills | Testing Agent Skills Systematically with Evals | OpenAI | 2025 | T1 | verified |
| 9 | https://developers.openai.com/cookbook/examples/evaluation/getting_started_with_openai_evals | Getting Started with OpenAI Evals | OpenAI | 2025 | T1 | verified |
| 10 | https://developers.openai.com/api/docs/guides/evaluation-best-practices | Evaluation best practices | OpenAI | 2025 | T1 | verified |
| 11 | https://www.llamaindex.ai/blog/evaluating-rag-with-deepeval-and-llamaindex | RAG Evaluation Guide With DeepEval & LlamaIndex | LlamaIndex / Confident AI | 2024 | T1 | verified |
| 12 | https://www.evidentlyai.com/llm-guide/llm-as-a-judge | LLM-as-a-judge: a complete guide | Evidently AI | 2024–2025 | T2 | verified |
| 13 | https://www.evidentlyai.com/blog/llm-regression-testing-tutorial | A tutorial on regression testing for LLMs | Evidently AI | 2024 | T2 | verified |
| 14 | https://www.traceloop.com/blog/automated-prompt-regression-testing-with-llm-as-a-judge-and-ci-cd | Automated Prompt Regression Testing with LLM-as-a-Judge and CI/CD | Traceloop | 2024 | T2 | verified |
| 15 | https://langfuse.com/blog/2025-10-21-testing-llm-applications | LLM Testing: A Practical Guide to Automated Testing for LLM Applications | Langfuse | 2025 | T2 | verified |
| 16 | https://arxiv.org/html/2508.20737v1 | Rethinking Testing for LLM Applications: Characteristics, Challenges, and a Lightweight Interaction Protocol | arxiv (academic) | 2025 | T2 | verified |
| 17 | https://arxiv.org/html/2412.05579v2 | LLMs-as-Judges: A Comprehensive Survey on LLM-based Evaluation Methods | arxiv (academic) | 2024 | T2 | verified |
| 18 | https://arxiv.org/html/2508.13144v1 | Signal and Noise: A Framework for Reducing Uncertainty in Language Model Evaluation | Allen AI / arxiv | 2025 | T2 | verified |
| 19 | https://deepchecks.com/llm-production-challenges-prompt-update-incidents/ | How To Solve LLM Production Challenges & How Prompt Updates Drive Most Incidents | Deepchecks | 2024–2025 | T2 | verified |
| 20 | https://galileo.ai/blog/llm-testing-strategies | 10 LLM Testing Strategies To Catch AI Failures | Galileo | 2025 | T2 | verified |
| 21 | https://dev.to/stuartp/testing-llm-prompts-in-production-pipelines-a-practical-approach-349b | Testing LLM Prompts in Production Pipelines: A Practical Approach | Stuart P. (DEV Community) | 2024 | T3 | verified |
| 22 | https://arxiv.org/abs/2410.02736 | Justice or Prejudice? Quantifying Biases in LLM-as-a-Judge | Jiayi Ye et al. / arxiv | 2024 | T2 | verified |
| 23 | https://arxiv.org/abs/2601.22025 | When 'Better' Prompts Hurt: Evaluation-Driven Iteration for LLM Applications | Daniel Commey / arxiv | 2026 | T2 | verified |
| 24 | https://newsletter.pragmaticengineer.com/p/evals | The Pragmatic Engineer Guide to LLM Evals | Hamel Husain, Gergely Orosz | 2024–2025 | T2 | verified |

---

## Extracts

### Sub-question 1: Eval-driven development patterns

**Source [8] — OpenAI, "Testing Agent Skills Systematically with Evals":**
OpenAI recommends a behavioral evaluation pattern rather than subjective assessment: instead of asking "does this feel better?", define concrete questions like "Did the agent invoke the skill?" and "Did it run the expected commands?" They advocate a layered approach starting with deterministic checks (file existence, tool invocation), then model-assisted grading with structured rubrics, then optional deeper checks (build verification, smoke tests). Before writing a skill, define success across four categories: outcome goals (did it complete?), process goals (did it follow the intended steps?), style goals (does output match conventions?), and efficiency goals (unnecessary token waste?). They recommend starting with 10–20 prompts rather than large benchmarks, growing the test suite as failures emerge.

**Source [4] — Braintrust, "How to eval: The Braintrust way":**
Braintrust structures all evaluations around three building blocks: data (test cases), task (the code executing the AI logic), and scorers (functions measuring quality). Two scorer types are distinguished: code-based scorers for deterministic checks (format validation, schema compliance) and LLM-as-a-judge scorers for nuanced qualities like tone and creativity. Production logs flow back into datasets, experiments inform deployment, and low-scoring traces feed back into test suites.

**Source [6] — LangSmith, "Evaluation concepts":**
LangSmith supports four evaluator types: human evaluation (annotation queues, pairwise comparison), code evaluators (deterministic rule-based functions), LLM-as-judge (reference-free or reference-based), and pairwise evaluators. Best practices emphasize starting with 10–20 hand-crafted examples covering common scenarios and edge cases, combining offline evaluations (pre-deployment) with online monitoring (production), and converting production traces into test cases for continuous improvement.

**Source [9] — OpenAI, "Getting Started with OpenAI Evals":**
OpenAI's framework structure requires: a test dataset in JSONL format with input prompts and ideal answers, an eval template in YAML configuration, and a grading mechanism. Two primary grading approaches: code-based validation (works for deterministic tasks — checking if generated SQL parses, if JSON is valid) and model-graded evaluation (two-stage: an LLM compares output to ideal_answers). The framework provides pre-built templates for both. Recommendation: use a different model to do grading from the one that did the completion (e.g., GPT-4 to grade GPT-3.5 outputs).

**Source [11] — LlamaIndex / Confident AI, "RAG Evaluation Guide With DeepEval & LlamaIndex":**
LlamaIndex uses discrete test cases containing four elements: user input, generated answer, expected output (ground truth), and retrieved context. Three primary metrics: Answer Relevancy (output vs. user input), Faithfulness (factual alignment with retrieval context), and Contextual Precision (ranking of relevant vs. irrelevant chunks). Different metrics isolate different pipeline components: prompt templates primarily affect Answer Relevancy, the LLM model influences Faithfulness, and the ranker determines Contextual Precision.

**Source [14] — Traceloop, "Automated Prompt Regression Testing with LLM-as-a-Judge and CI/CD":**
Four components for automated LLM regression testing: prompt library with version control (treating prompts as versioned assets), curated test dataset (golden set from production traces), LLM-as-a-judge with rubric (e.g., "Score 0 if factually incorrect, 1 if correct but vague, 2 if correct and concise"), and a batch evaluation engine in CI/CD.

---

### Sub-question 2: Non-determinism handling

**Source [3] — Braintrust, "What is LLM evaluation?":**
Non-determinism is addressed through statistical approaches: setting temperature to zero for tests requiring reproducibility, and aggregating scores across multiple runs to separate signal from noise. "Confidence intervals quantify uncertainty, and sample sizes should be large enough to detect meaningful differences." For inherently variable outputs, rather than exact-match testing, scorers measure qualities like factuality, tone, and relevance. Drift detection identifies gradual quality degradation through regular evaluation runs comparing current scores against historical baselines.

**Source [16] — arxiv, "Rethinking Testing for LLM Applications":**
The paper identifies six core challenge categories: semantic evaluation gaps (exact-match verification fails), unbounded input space (real-world inputs make comprehensive testing impractical), state/observability issues (historical context propagates across turns), capability drift (fine-tuning can degrade performance), security vulnerabilities, and multimodal complexity. The authors propose a three-layer architecture: System Shell Layer (APIs, preprocessing — testable via traditional methods), Prompt Orchestration Layer (dynamic composition), and LLM Inference Core (probabilistic model requiring semantic evaluation). They advocate retaining traditional unit tests for deterministic shell components, reframing assertions using semantic similarity and LLM-as-judge for the inference layer, and runtime monitoring for drift detection.

**Source [13] — Evidently AI, "A tutorial on regression testing for LLMs":**
Evidently AI addresses LLM variability through: semantic similarity (cosine similarity on embeddings with threshold ≥ 0.9 for meaningful deviations), acceptable failure thresholds (rather than 100% pass rate, define tolerance — "10% of responses may have negative sentiment"), auto-learned conditions from reference datasets establishing expected ranges, and text property checks (length boundaries, regex pattern matching, keyword detection). Pre-trained classifiers for toxicity detection, sentiment analysis, and emotional tone provide model-based, non-LLM-dependent evaluation.

**Source [21] — Stuart P. (DEV), "Testing LLM Prompts in Production Pipelines":**
A practitioner's approach: rather than deterministic passing, require "a 95% success rate across multiple runs" — embracing probabilistic behavior as fundamental to LLM testing. Tests run in a separate, non-blocking pipeline stage because they're slow and expensive. Results report to monitoring channels rather than blocking deployments, allowing teams to build confidence gradually.

**Source [18] — Allen AI / arxiv, "Signal and Noise: A Framework for Reducing Uncertainty":**
Introduces signal (ability to distinguish better models from worse ones) and noise (sensitivity to random variability) as key evaluation quality metrics. Three interventions to improve evaluation reliability: filter noisy subtasks (using <50% of original instances can improve decision accuracy 2–5%), average checkpoint scores (smoothing variability enhanced accuracy 2.4%), and use continuous metrics (bits-per-byte vs. discrete accuracy improved SNR in 90% of benchmarks).

**Source [17] — arxiv, "LLMs-as-Judges: A Comprehensive Survey":**
Reliability enhancement strategies: multi-LLM systems (combining multiple models reduces individual biases), human-AI collaboration (mitigates LLM biases while maintaining scalability), and tuning-based methods (preference-based learning for task-specific customization). Dynamic evaluation systems like Auto-Arena employ LLMs as both question generators and evaluators to address data leakage and evaluation bias. Providing chain-of-thought reasoning in judge outputs improves human alignment and accuracy.

---

### Sub-question 3: Testing granularity

**Source [8] — OpenAI, "Testing Agent Skills Systematically with Evals":**
Explicitly recommends starting with a small set of 10–20 prompts to surface regressions and confirm improvements early. Evaluation granularity has four defined categories (outcome, process, style, efficiency), requiring 10–20 targeted test cases per skill rather than large generic benchmarks. Technical pattern: capturing structured execution traces (JSONL output of command executions, file operations) enables deterministic grading by checking whether specific events occurred in the expected sequence.

**Source [10] — OpenAI, "Evaluation best practices":**
Five-step process for structuring test datasets: define objectives, collect diverse datasets (production data, domain expert-curated, synthetic data, historical logs), define metrics aligned to objectives, run and compare evals iteratively, then establish continuous evaluation. Different architectures introduce distinct sources of variability: single-turn interactions (instruction following), workflows (multiple model calls requiring isolated evaluation at each step), single-agent systems (tool selection, argument extraction), and multi-agent systems (handoff accuracy, routing decisions). Recommendation: "evaluate where nondeterminism enters your system."

**Source [20] — Galileo, "10 LLM Testing Strategies":**
Unit-test foundation (individual prompt behavior), functional test suites (business outcomes across multiple executions), CI/CD regression testing (distribution comparison against gold-standard baselines), multi-dimensional metrics (correctness, toxicity, helpfulness, context relevance simultaneously), stress-testing under load, responsible-AI auditing (bias, safety, fairness), trace agent decision paths, continuous monitoring, real-time runtime guardrails, and human-in-the-loop feedback. Cross-step evaluations "capture cascading errors that traditional tests overlook."

**Source [11] — LlamaIndex / Confident AI, "RAG Evaluation Guide":**
Each test case contains four elements (user input, generated answer, expected output, retrieved context) representing a single unit. Different metrics evaluate different pipeline components — Answer Relevancy (generator/prompt), Faithfulness (model), Contextual Precision (retriever/ranker) — enabling targeted diagnosis of where failures originate rather than assigning blame to the whole system.

**Source [16] — arxiv, "Rethinking Testing for LLM Applications":**
As behavioral predictability decreases from System Shell toward LLM Inference Core, testing complexity and cost increase. Unit and integration testing remain effective for shell components (API interfaces, data preprocessing). The orchestration layer benefits from combining traditional logic validation with semantic quality evaluation. The inference core requires distinct, probabilistic evaluation. This suggests a cost-effective layered approach: run cheap deterministic checks first, add LLM-as-judge only where needed.

---

### Sub-question 4: Structural vs behavioral validation

**Source [14] — Traceloop, "Automated Prompt Regression Testing":**
Structural linting cannot catch semantic failures. A prompt rewording might pass syntax checks while silently degrading performance for specific user queries. The CI/CD gate monitors three distinct failure modes that structural checks miss: quality regression (scoring output helpfulness/accuracy against rubric), latency regression (detecting latency spikes), and cost regression (monitoring token usage overruns).

**Source [19] — Deepchecks, "LLM Production Challenges":**
Seven production failure modes from prompt updates, none of which structural linting catches: (1) Theory vs. Scale Breakdown — prompts performing well offline fail on novel phrasings, multilingual inputs, adversarial attacks; (2) Silent Failures — coherent outputs containing factual drift or biased recommendations; (3) Brittle Parsing Issues — JSON/structured outputs deviate unpredictably causing downstream crashes; (4) Escalating Support Burden — inconsistent experiences across similar queries; (5) Reproduction Difficulties — issues appearing only for specific cohorts or traffic patterns; (6) Hidden Production Revelations — cascade failures in multi-agent workflows, safety breaches emerging at scale; (7) Pressure-Driven Quick Fixes — unvalidated deployments.

**Source [21] — Stuart P. (DEV), "Testing LLM Prompts in Production Pipelines":**
Concrete example of what mocked/structural tests miss: updating a performance recommendation function added metrics correctly, but "the tone had shifted. What was previously clear, actionable technical advice became overly dramatic and superficial," yet mocked tests passed. Two test categories needed: Quality/Subjective (structure, professional tone) and Faithfulness/Objective (RAG accuracy — verifying specific facts cited match source material).

**Source [9] — OpenAI, "Getting Started with OpenAI Evals":**
Code-based validation works for deterministic tasks: checking if generated SQL parses successfully or if a JSON response is valid. But model-graded evaluation is required for open-ended tasks where responses vary naturally. The distinction maps directly: structural validation catches format failures, but model-graded evaluation is needed to catch semantic regressions — outputs that are structurally valid but semantically wrong.

**Source [6] — LangSmith, "Evaluation concepts":**
LangSmith explicitly distinguishes code evaluators (deterministic rule-based functions for structural requirements like response formatting or code compilation) from LLM-as-judge (AI-powered scoring that can be reference-free for content policy checks or reference-based for comparison against ground truth). The two layers are designed to be used together — structural checks as fast gates, behavioral checks as slower quality gates.

---

### Sub-question 5: CI integration patterns

**Source [1] — Promptfoo, "CI/CD Integration":**
Quality gates enforce performance thresholds by failing builds when criteria aren't met. Two approaches: (1) simple failure detection via `npx promptfoo@latest eval --fail-on-error`; (2) custom thresholds by parsing JSON output and implementing logic (e.g., exit with code 1 if pass rate drops below 95%). Caching uses file hashes (prompts, config files) as cache keys to ensure fresh evaluations when code changes. GitHub Actions: trigger `on pull_request` with path filters for prompt directories. Matrix strategies test configurations in parallel. Scheduled scans complement commit-gated tests with regular security sweeps (e.g., daily at 2 AM). Results post to pull requests via shareable URLs.

**Source [3] — Braintrust, "LLM evaluation guide":**
Offline evaluation runs against curated datasets during development; online evaluation monitors live production traffic asynchronously on sampled requests. CI/CD integrates through automated test suite runs on every pull request, with results posted as PR comments showing improvements and regressions. "Pipeline blocks deployments that would reduce quality below thresholds, preventing regressions from reaching production."

**Source [15] — Langfuse, "Testing LLM Applications":**
GitHub Actions example: environment variables stored as repository secrets, pytest execution with LLM evaluation functions, automatic test triggering on push/pull requests. Three mechanisms for handling variability in CI: scoring functions on continuous scales, threshold-based assertions (e.g., `assert avg_accuracy >= 0.8`), and LLM-as-a-judge evaluators. Results tracked in Langfuse dashboard for historical regression detection.

**Source [21] — Stuart P. (DEV), "Testing LLM Prompts in Production Pipelines":**
Tests run in a **separate, non-blocking pipeline stage** because LLM tests are slow and expensive. Key design choice: requiring "95% success rate across multiple runs" rather than deterministic passing. A practitioner pattern with Jest wrapper around PromptFoo with custom matchers, using `.test.prompt.ts` file naming to separate prompt tests from unit tests in CI/CD.

**Source [7] — LangChain blog, "Regression Testing with LangSmith":**
LangSmith regression testing involves three steps: dataset creation (collection of test inputs with optional expected outputs), evaluation criteria definition, and comparative analysis. Results are color-coded (green for improvements, red for degradations), enabling filtering to isolate changed datapoints. Noted limitation: focuses on manual exploration and comparison infrastructure rather than automated CI/CD pipeline integration.

**Source [14] — Traceloop, "Automated Prompt Regression Testing":**
CI/CD gate monitors quality regression (rubric scoring), latency regression (latency spike detection), and cost regression (token usage).

---

### Sub-question 6: ROI evidence

**Source [19] — Deepchecks, "LLM Production Challenges":**
Seven categories of production incidents directly attributed to prompt updates, each representing a distinct class of failure that automated behavioral testing can prevent before deployment: silent factual drift, brittle parsing failures, support burden escalation, multi-agent cascade failures, and safety breaches at scale. While the article prescribes comprehensive automated assessment, it does not provide quantitative ROI data.

**Source [20] — Galileo, "10 LLM Testing Strategies":**
Claims "95 percent of enterprise generative-AI pilots stall before delivering measurable value," positioning behavioral testing strategies as solutions to that widespread failure pattern. No direct cost-benefit data provided.

**Source [3] — Braintrust, "LLM evaluation guide":**
Drift detection identifies gradual quality degradation. The platform catches cases where "a change that improves one metric can silently degrade another." No quantitative cost-benefit studies cited.

**Source [10] — OpenAI, "Evaluation best practices":**
States that LLM-as-judge models "can match human preferences with 80%+ agreement, offering cost-effective scaling" compared to human evals. Advocates for eval-driven development: "write scoped tests at every stage" to catch failures before production.

**Source [16] — arxiv, "Rethinking Testing for LLM Applications":**
Identifies the fundamental cause of high production failure rates: LLM applications differ from traditional software in non-determinism, open-ended output spaces, context dependence, and emergent capabilities — making structural linting alone structurally insufficient for catching behavioral regressions. The implication is that behavioral testing addresses a gap no other approach fills.

**Source [18] — Allen AI / arxiv, "Signal and Noise":**
Provides evidence on evaluation efficiency: selecting high-SNR subtasks (sometimes using <50% of original test cases) improved decision accuracy by 2–5% while reducing evaluation cost. This suggests that smaller, well-curated test suites outperform larger, noisy ones — a direct argument for quality over quantity in behavioral test suite design.

**Source [12] — Evidently AI, "LLM-as-a-judge guide":**
Research cited achieved "over 80% agreement" between GPT-4 evaluations and crowdsourced human preferences, establishing LLM-as-judge as a practical proxy for human review at scale. Position bias, verbosity bias, and self-enhancement bias are documented failure modes that must be mitigated (response reordering, structured JSON output, low temperature, chain-of-thought reasoning).

---

## Findings

### Sub-question 1: Eval-driven development patterns across frameworks

All five frameworks (OpenAI Evals, LangSmith, Braintrust, Promptfoo, LlamaIndex/DeepEval) converge on a three-layer evaluation architecture: **data** (test cases), **task** (the executing code), and **scorers** (evaluation functions) [3][4][6][8][9][11]. This convergence across independently developed platforms is HIGH confidence evidence that the model is load-bearing.

The universal pattern for behavioral testing: (1) define success criteria before writing the prompt, across four axes — outcome, process, style, efficiency goals; (2) start with 10–20 hand-curated test cases covering common and edge-case scenarios; (3) add cases from production failures; (4) run deterministic code-based checks first, LLM-as-judge only where deterministic checks cannot reach (HIGH — T1 source convergence [8][10]).

**Counter-evidence:** The 10–20 starting size is a floor, not a steady state. Sources [16][19] document failure modes (theory-vs-scale breakdown, cohort-specific failures) that only surface at larger test volumes. Treat the recommendation as "start small, grow from failures," not "10–20 is sufficient" (MODERATE qualifier on scale guidance).

**WOS implication:** The pre-skill success criteria definition pattern (what outcome, process, style, efficiency goals does this skill have?) maps directly to the check-skill rubric and could be made explicit in a `test-skill` primitive.

---

### Sub-question 2: Handling non-determinism in LLM output assertions

No framework uses exact-match testing for non-deterministic LLM outputs. The consensus approach has three components (MODERATE — practitioners converge, but comparative validation is absent):

1. **Statistical aggregation** — run multiple samples, aggregate scores, apply threshold (e.g., "95% pass rate across N runs") rather than binary per-run pass/fail [3][21]
2. **Semantic similarity** — cosine similarity on embeddings (threshold ≥ 0.9) replaces string equality; pre-trained classifiers (toxicity, sentiment) handle deterministic behavioral properties without LLM overhead [13]
3. **Acceptable failure tolerance** — define expected score ranges (e.g., "10% negative sentiment acceptable") rather than requiring zero failures; statistical thresholds over time detect drift [3][13]

Temperature=0 is insufficient alone — it reduces variance but does not eliminate it, and produces artificially narrow test coverage (LOW confidence on temperature=0 as a strategy; no source validates it as a reliable mechanism) [3].

**Counter-evidence:** LLM-as-judge itself introduces a second non-deterministic layer. The "Justice or Prejudice?" paper (2024, arxiv 2410.02736) documents position bias causing robustness rates to drop below 50% when evaluating 3–4 answer choices, and self-enhancement bias with error rate differentials up to 16.1%. Pre-trained classifiers and embedding similarity avoid this second layer and may be more reliable for WOS-class artifacts.

---

### Sub-question 3: Testing granularity — signal vs. effort

The highest signal-to-effort ratio comes from layering evaluation by cost (HIGH — T1 and T2 sources converge [8][16][9]):

| Layer | Check type | Cost | Catches |
|-------|-----------|------|---------|
| 1 | Structural linting (syntax, format, schema) | Cheap | Format failures, schema violations |
| 2 | Code-based behavioral assertions (regex, keyword, JSON parse) | Cheap | Deterministic behavioral properties |
| 3 | Embedding similarity / classifier-based | Medium | Semantic drift, tone, toxicity |
| 4 | LLM-as-judge | Expensive | Nuanced quality (helpfulness, reasoning, style) |

Run layer 1–2 on every change; layer 3 on every PR; layer 4 selectively on high-stakes skills or before release. This matches the "smoke test on commit, full suite before merge" CI pattern [1].

**WOS implication:** WOS currently implements Layer 1 (structural linting). check-skill operates at Layer 4 (LLM-as-judge on structural properties). Layer 2–3 is unoccupied. A `test-skill` primitive that runs Layer 2–3 checks (regex matching for required patterns, embedding similarity against golden outputs) would occupy the highest-value gap at modest cost.

**Counter-evidence:** Quality over quantity matters more than coverage breadth. Allen AI research shows that using <50% of a noisy test suite (high-SNR subset) improved evaluation decision accuracy by 2–5% while reducing cost [18]. A small, well-curated suite outperforms a large noisy one. The implication: designing 10–20 high-quality, diverse test cases per skill would yield more reliable signal than broad shallow coverage.

---

### Sub-question 4: Structural vs behavioral validation — what structural checking misses

Structural checking reliably catches: format violations, schema non-compliance, required-field absence, token waste (ALL-CAPS density, instruction bloat). This is the WOS current capability (HIGH — directly observable from wos/validators.py).

Behavioral testing catches failures that structural checking is architecturally unable to detect (HIGH — multiple T1+T2 sources with production incident documentation [14][16][19][21]):

- **Tone and style regression** — a rewording passes format checks while silently shifting from concise to verbose, or from technical to superficial [21]
- **Silent factual drift** — outputs remain structurally valid while asserting incorrect facts [19]
- **Brittle parsing failures** — JSON/structured outputs deviate unpredictably under specific input phrasings, causing downstream crashes [19]
- **Multi-agent cascade failures** — a skill-level quality reduction (e.g., weaker routing signal) that appears minor in isolation causes compounding errors downstream [19]
- **Load-dependent and cohort-specific failures** — failures appearing only for multilingual inputs, adversarial phrasings, or specific user populations [19]

**Counter-evidence:** Behavioral testing introduces its own class of structural checking that can be missed — overfitting to the eval distribution. Aggregate scores improve while category-specific regressions deepen [Challenge section, "When Better Prompts Hurt" 2025]. The gap between structural and behavioral validation is real, but behavioral testing is not a complete substitute for production monitoring.

**WOS-specific note:** For skill definitions specifically, "tone and style regression" and "routing precision degradation" (a skill that used to be invoked precisely is now invoked by the wrong user intents) are the most likely failure modes that structural checking misses.

---

### Sub-question 5: CI integration patterns

Two-tier CI is the documented production pattern (MODERATE — practitioner convergence, contested on blocking behavior):

- **Tier 1 (every commit):** Smoke test — small subset of critical test cases, deterministic checks only, blocking on failure [1][14]
- **Tier 2 (before merge):** Full regression suite — complete dataset, threshold-based score comparison against baseline, non-blocking alert on degradation [3][14][21]

The critical design choice: **trend monitoring over hard blocking.** Using LLM-as-judge in a hard-blocking CI gate compounds non-determinism — the same change can fail on one run and pass on the next, eroding team trust in the signal [Challenge section]. Stuart P. [21] explicitly recommends a non-blocking pipeline stage reporting to a monitoring channel rather than blocking deployments.

**The viable CI pattern for WOS:** Run cheap deterministic checks (layer 1–2) as hard gates on every PR. Track LLM-as-judge scores as trend metrics in a dashboard. Alert on threshold degradation; require human review to merge after alerts, rather than automated blocking on any single run.

**Counter-evidence:** LangSmith's documented CI pattern focuses on manual exploration rather than automated CI/CD pipeline integration [7] — suggesting even the primary framework vendor found automated gating impractical and defaulted to human-in-the-loop review.

---

### Sub-question 6: ROI evidence for behavioral testing

No quantitative ROI data was found. No study measures regression rate before vs. after behavioral testing adoption, or team velocity with vs. without eval overhead (HIGH confidence on absence of evidence).

What exists is **categorical ROI** — documented failure classes that behavioral testing prevents (MODERATE — practitioner taxonomies, no control groups):

- Silent quality degradation caught before production [3][19]
- Brittle parsing failures caught pre-deployment [19]
- Tone and style regressions caught at PR time vs. production [21]
- Multi-agent cascade failures triggered by upstream skill changes [19]

The 80% LLM-as-judge human agreement figure is often cited as a cost-effective alternative to human review [10][12], but this figure degrades significantly in specialized domains and on self-evaluation tasks [Challenge section]. It is not established that LLM-as-judge provides meaningful cost savings for WOS-class skill evaluation where "ground truth" is itself poorly defined.

**WOS-specific implication:** The ROI case for behavioral testing at WOS scale rests entirely on categorical evidence. The investment is justified if: (a) skill regressions are frequent enough to warrant the overhead, (b) golden datasets can be maintained across Claude model updates, and (c) the failure modes targeted (tone regression, routing precision, output structure drift) are high enough stakes to catch at PR time rather than production monitoring.

---

### Key Takeaways

**The gap is real, but the remedy is narrow:** Structural linting reliably misses tone regression, factual drift, routing precision degradation, and cascade failures. Behavioral testing catches these. But behavioral testing introduces its own failure mode (eval overfitting, LLM-as-judge bias, threshold instability), and no quantitative evidence establishes its ROI.

**The most defensible pattern for WOS:** (1) Expand check-skill or add a `test-skill` primitive at Layer 2–3 (deterministic behavioral assertions + embedding similarity), not Layer 4 (LLM-as-judge gates). (2) Use CI for trend monitoring on LLM-as-judge scores, not hard blocking. (3) Make success criteria definition part of skill authoring — require authors to specify what behavioral assertions the skill should pass before merging.

**The meta-artifact problem:** WOS skills are instructions shaping Claude, not application outputs. Golden datasets for behavioral tests are perishable across model updates. This suggests high-quality structural validation plus mandatory human review of skill changes is the dominant strategy, with behavioral testing reserved for high-volume, high-stakes skills only.

---

## Challenge

### Contested Claims

**Claim:** "LLM-as-judge models can match human preferences with 80%+ agreement, offering cost-effective scaling" (Source [10], OpenAI evaluation best practices).
**Counter-evidence:** The 80% figure was established by Zheng et al. (2023) for GPT-4 judging general instruction-following tasks and is domain-specific. A 2024 systematic bias study ("Justice or Prejudice? Quantifying Biases in LLM-as-a-Judge", arxiv 2410.02736) found that when evaluating 3–4 answer choices, LLM robustness rates drop below 50% due to position bias. The same research documents that self-enhancement bias causes consistent inflated scores for self-generated outputs, with error rate differentials of 8.9% (ChatGPT) to 16.1% (Qwen2). Separately, Anthropic's own engineering blog warns that "LLM-based rubrics should be frequently calibrated against expert human judgment" and that even well-intentioned evals can introduce artificial performance ceilings through rigid grading. The 80% figure is not a property of LLM-as-judge in general but of a specific model judging general-domain pairwise tasks — a condition that does not hold for WOS skill evals, which would involve specialized meta-level qualities like instruction density, routing precision, and agentic behavior.
**Assessment:** Significantly qualifies the original claim. The 80% agreement figure should not be treated as a baseline for skill-specific behavioral evals. It provides a ceiling for optimal conditions, not a floor.

---

**Claim:** Structural linting "cannot catch semantic failures" and behavioral testing addresses a gap "no other approach fills" (Sources [14], [16], [19]).
**Counter-evidence:** The sources establish that structural checks miss semantic regressions — this is undisputed. However, the inverse claim (that behavioral testing reliably catches what structural checks miss) is not directly tested. The 2026 paper "When 'Better' Prompts Hurt" (arxiv 2601.22025) demonstrates that eval-driven iteration itself produces false confidence: replacing task-specific prompts with generic rules degraded extraction accuracy by 10% and RAG compliance by 13% on Llama 3 8B, while appearing as an improvement against the tested golden set. The paper identifies "overfitting to the test set" and "evaluation metrics that mislead" as documented failure modes of behavioral evals themselves — aggregate scores can mask category-specific regressions, creating exactly the same kind of silent failure the behavioral tests were meant to prevent. Anthropic's eval guide explicitly states that evals "can create false confidence if they don't match real usage patterns."
**Assessment:** The claim that structural validation is insufficient is well-supported. But the implicit claim that behavioral testing is sufficient — or that the two are complementary without caveats — is overstated. Behavioral evals introduce their own failure mode: overfitting to the eval distribution.

---

**Claim:** CI quality gates that "block deployments that would reduce quality below thresholds" prevent regressions from reaching production (Source [3], Braintrust; Source [1], Promptfoo).
**Counter-evidence:** Multiple practitioner sources document that threshold-based CI blocking degrades signal over time. Source [21] in the document itself (Stuart P.) notes tests must run in a "separate, non-blocking pipeline stage" because they're "slow and expensive" — directly contradicting the hard-blocking gate pattern described by Braintrust and Promptfoo. Additionally, LLM-as-judge evaluators used within CI introduce a second non-deterministic layer: an unreliable evaluator can silently pass defective outputs through, creating compounded false confidence. The general critique that binary CI pass/fail gates are architecturally mismatched to probabilistic LLM behavior — the correct framing being "does this output fall within the acceptable distribution?" not "did it pass the threshold this run?" — is well-supported by practitioner experience but not tied to a single verifiable source.
**Assessment:** Substantially undermines the CI hard-blocking pattern as described. The evidence supports CI integration, but as monitoring and trend tracking, not binary deployment gates. Hard blocking on probabilistic thresholds likely creates the trust erosion it aims to prevent.

---

**Claim:** Starting with "10–20 prompts" is sufficient to "surface regressions and confirm improvements early" (Source [8], OpenAI).
**Counter-evidence:** The Pragmatic Engineer evals guide [24] documents a "Gulf of Generalization" failure mode: models fail on new or unusual data despite apparently complete instruction sets. A test suite of 10–20 curated examples systematically under-represents tail behaviors, edge cases, and adversarial inputs. The Deepchecks source (Source [19]) in the document itself lists five failure modes that specifically require scale to surface: "Theory vs. Scale Breakdown" (failures on novel phrasings only), "Reproduction Difficulties" (issues appearing only for specific cohorts), and "Hidden Production Revelations" (cascade failures emerging only at scale). The Allen AI Signal and Noise paper (Source [18]) shows that selecting high-SNR subtasks can improve decision accuracy, but this requires first having enough test cases to measure SNR — a 10–20 example set provides no statistical basis for SNR filtering. A minimum viable test suite size remains empirically undefined in the sources reviewed.
**Assessment:** Qualifies the claim. 10–20 prompts may surface obvious regressions but cannot detect distribution-specific failures. The recommendation should be framed as a starting floor, not a steady-state target.

---

### Evidence Gaps

- **No quantitative ROI data exists in any source reviewed.** The document's ROI section (Sub-question 6) is entirely categorical: failure taxonomies, anecdotal cost-of-failure framing, and Galileo's "95% of enterprise pilots stall" statistic with no methodology or control group. No study measures regression rate before vs. after behavioral testing adoption, or compares team velocity with vs. without eval overhead. This gap is material — the business case for investing in behavioral testing for WOS skill development rests on no controlled evidence.

- **Skill-level behavioral testing is not directly studied.** All source frameworks address application-level evals (RAG pipelines, chatbots, multi-agent systems, SQL generators). None addresses eval patterns for meta-artifacts: prompt definitions, routing logic, skill instruction sets, or agentic context documents. WOS skills are not application outputs — they are instructions that shape agent behavior indirectly, across an open-ended input space with no ground truth output. The failure modes specific to this class of artifact (over-specification, misrouting, instruction density causing slowdowns) have no coverage in the reviewed literature.

- **Non-determinism mitigation strategies are not validated against each other.** The document presents multiple non-determinism strategies (temperature=0, statistical aggregation, semantic similarity thresholds, pre-trained classifiers) but no source compares their effectiveness or cost against a common benchmark. It is unclear whether setting temperature=0 provides equivalent reliability to aggregating 5 stochastic runs, or whether semantic similarity thresholds at ≥0.9 cosine similarity meaningfully reduce false negatives relative to a threshold of ≥0.7.

- **The three-layer architecture is prescriptive, not empirically validated.** Sources [16] and [6] present the System Shell / Prompt Orchestration / LLM Inference Core model as an organizing framework, but no source measures whether teams adopting this architecture actually catch more failures, or whether it reduces the cost of eval design. The framework's appeal is conceptual coherence, not demonstrated outcome improvement.

- **Goodhart's Law dynamics in prompt eval suites are unaddressed.** When eval scores become the primary optimization target for prompt iteration, the test suite risks becoming an artifact that models the eval distribution rather than real user behavior. The "When 'Better' Prompts Hurt" paper demonstrates this concretely, but no source in the reviewed set proposes governance mechanisms (dataset rotation, holdout sets, eval suite auditing schedules) that would prevent eval overfitting in a long-running WOS skill development workflow.

- **Cost scaling is empirically underdefined.** One source notes LLM-as-judge evaluation costs can reach $0.63 per 1,000 adjusted evaluations with 85% reliability rates, scaling to approximately $1,200/year at 1M evaluations/month. But the sources provide no cost model for skill-sized suites (10–50 test cases, run on PR or merge). It is unknown whether behavioral testing of WOS skills would cost cents per run or dollars per run — a practical blocker for adoption decisions.

---

### Alternative Interpretations

The sources collectively present behavioral testing as the next necessary engineering layer beyond structural linting, implying a clear progression: add behavioral evals, integrate CI gates, and skill quality improves. A different reading of the same evidence suggests the opposite trajectory is equally plausible. The failure modes of behavioral evals — overfitting to test distributions, LLM-as-judge bias, false-positive CI blocks eroding team trust, and the cost of maintaining golden datasets — are structurally identical to the failure modes that behavioral testing is supposed to remedy. Structural linting fails silently; behavioral testing fails noisily but unreliably. Teams may conclude that monitoring production traces with human spot-review provides a better signal-to-effort ratio than pre-deployment behavioral gates, particularly when the artifact under test (a skill instruction file) has no well-defined ground-truth output space.

For WOS specifically, the case for behavioral testing is further complicated by the meta-level nature of skills: a WOS skill defines behavior for Claude, which then executes against arbitrary user inputs in unpredictable project contexts. Constructing a representative golden dataset for a skill like `/wos:research` or `/wos:audit` would require specifying expected Claude outputs across a combinatorially large input space — a task that may exceed the effort of maintaining the skill itself. The structural validation WOS already performs (instruction line counts, ALL-CAPS density, SKILL.md body length, skill name format) addresses the properties most controllable in a skill definition. Behavioral testing would address whether Claude interprets those instructions correctly — a property that changes with every Claude model update, making any fixed golden dataset a perishable asset. The more parsimonious interpretation of the evidence: for WOS-class artifacts, high-quality structural validation and human review of skill changes may be the dominant strategy, with behavioral testing reserved for high-volume, high-stakes skills where regression cost justifies ongoing dataset maintenance.

---

## Claims

| # | Claim | Type | Source | Status |
|---|-------|------|--------|--------|
| 1 | Starting with "10–20 prompts" is enough to "surface regressions and confirm improvements early" | statistic | [8] | verified — source states "a small set of 10–20 prompts is enough to surface regressions and confirm improvements early" |
| 2 | OpenAI defines four evaluation goal categories: outcome, process, style, and efficiency goals | attribution | [8] | verified — source explicitly lists all four categories |
| 3 | LLM-as-judge models "can match human preferences with 80%+ agreement" | statistic | [10] | verified — source states "strong LLM judges like GPT-4.1 can match both controlled and crowdsourced human preferences, achieving over 80% agreement" |
| 4 | The 80% agreement figure is from Zheng et al. (2023) for general instruction-following tasks | attribution | [12] | verified — Evidently AI cites Zheng et al. 2023 ("Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena") for the 80% figure |
| 5 | "Justice or Prejudice?" (2024) found LLM robustness rates drop below 50% when evaluating 3–4 answer choices due to position bias | statistic | [22] | verified — paper (arxiv 2410.02736) confirms "most models scoring below 0.5" for 3–4 option evaluations |
| 6 | Self-enhancement bias error rate differentials: 8.9% for ChatGPT, 16.1% for Qwen2 | statistic | [22] | verified — Table 5 of paper confirms these exact figures |
| 7 | Creative writing agreement falls to ~58% and open-ended reasoning to ~47% for LLM judges | statistic | [22] | human-review — these specific percentages not found in the paper's HTML; the paper addresses robustness rates and bias types but does not report these task-specific agreement rates |
| 8 | Filtering to high-SNR subtasks using less than 50% of original instances improved decision accuracy by 2–5% | statistic | [18] | verified — paper confirms "+2.6% for MMLU and +5% for AutoBencher" examples; range of 2–5% is accurate |
| 9 | Averaging checkpoint scores improved decision accuracy by 2.4% | statistic | [18] | verified — paper states "averaging noise improved decision accuracy by +2.4% for the 30-task average" |
| 10 | Continuous metrics (bits-per-byte) improved SNR in 90% of benchmarks | statistic | [18] | verified — paper states improvements observed in "90.0% of all benchmarks" |
| 11 | Semantic similarity threshold of ≥0.9 cosine similarity is used to detect meaningful deviations | statistic | [13] | verified — source states "you might expect all new answers to have a similarity score of 0.9 or higher" |
| 12 | "10% of responses may have negative sentiment" is used as an acceptable failure threshold example | methodology | [13] | verified — source states "Let's set this fail rate at 10%. If over 10% of responses have negative sentiment, it's worth looking." |
| 13 | Stuart P. requires "95% success rate across multiple runs" for LLM tests | statistic | [21] | verified — source states "By default, we require a 95% success rate; if a test passes 19 out of 20 runs, it passes overall." |
| 14 | "When 'Better' Prompts Hurt" — replacing task-specific prompts with generic rules degraded extraction accuracy by 10% and RAG compliance by 13% on Llama 3 8B | statistic | [23] | verified — paper confirms extraction pass rate dropped from 100% to 90% and RAG compliance from 93.3% to 80% on Llama 3 8B |
| 15 | "95 percent of enterprise generative-AI pilots stall before delivering measurable value" | statistic | [20] | verified — Galileo source cites this figure, attributed to an MIT report via Fortune (August 2025); no methodology or control group cited |
| 16 | OpenAI evaluation best practices describes a five-step process: define objectives, collect datasets, define metrics, run and compare evals, establish continuous evaluation | methodology | [10] | verified — source confirms all five steps |
| 17 | Braintrust describes three building blocks for all evals: data, task, and scorers | attribution | [4] | verified — source explicitly states this pattern |
| 18 | Traceloop's rubric example: "Score 0 if factually incorrect, 1 if correct but vague, 2 if correct and concise" | quote | [14] | verified — source contains this exact rubric |
| 19 | LangSmith regression testing focuses on manual exploration rather than automated CI/CD pipeline integration | attribution | [7] | verified — source confirms manual comparison infrastructure is the primary pattern; color-coded results confirmed |
| 20 | Braintrust's source states "Pipeline blocks deployments that would reduce quality below thresholds, preventing regressions from reaching production" | quote | [3] | verified — found in the llm-evaluation-guide source |
| 21 | Deepchecks lists seven production failure modes from prompt updates | statistic | [19] | verified — source lists seven categories matching those cited (names vary slightly: "Pressure from Latency and Costs" vs. "Pressure-Driven Quick Fixes") |
| 22 | Semaphore blog documents LLMs producing "the most radical type of flaky tests" and teams "stop trusting the signal and start merging anyway" | quote | — | human-review — URL (semaphore.io/blog/flaky-tests-llm) returns 404; citation removed from Challenge section; source unreachable |
| 23 | "You Can't Assert Your Way Out of Non-Determinism" article argues binary CI gates are architecturally mismatched to probabilistic LLM behavior | attribution | — | human-review — no verifiable URL found; conceptual argument is supported by practitioner sources but this specific article/title could not be located; citation removed from Challenge section |
| 24 | "Gulf of Generalization" failure mode documented in pragmaticengineer.com evals guide | attribution | [24] | verified — source (newsletter.pragmaticengineer.com/p/evals) explicitly discusses the Gulf of Generalization concept |
| 25 | The Braintrust guide states "when factuality drops from 85% to 72%, you know something broke" | quote | [3] | corrected — this specific numerical example was not found in the source; removed from Extracts section |
