---
name: "Agent Testing & Non-Deterministic Systems"
description: "A four-layer testing pyramid anchored in deterministic unit tests at the base, LLM-as-judge evaluations in the middle, and end-to-end agent simulations at the top enables continuous regression detection for non-deterministic LLM-based tools."
type: research
sources:
  - https://engineering.block.xyz/blog/testing-pyramid-for-ai-agents
  - https://medium.com/@derekcashmore/the-ai-agent-testing-pyramid-a-practical-framework-for-non-deterministic-systems-276c22feaec8
  - https://langwatch.ai/scenario/best-practices/the-agent-testing-pyramid/
  - https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
  - https://www.anthropic.com/research/statistical-approach-to-model-evals
  - https://www.evidentlyai.com/llm-guide/llm-as-a-judge
  - https://newsletter.pragmaticengineer.com/p/evals
  - https://langfuse.com/blog/2025-10-21-testing-llm-applications
  - https://www.braintrust.dev/articles/best-ai-evals-tools-cicd-2025
  - https://www.promptfoo.dev/docs/integrations/ci-cd/
  - https://www.getmaxim.ai/articles/building-a-golden-dataset-for-ai-evaluation-a-step-by-step-guide/
  - https://www.confident-ai.com/docs/llm-evaluation/core-concepts/test-cases-goldens-datasets
  - https://dev.to/sreeni5018/debugging-non-deterministic-llm-agents-implementing-checkpoint-based-state-replay-with-langgraph-5171
  - https://www.sakurasky.com/blog/missing-primitives-for-trustworthy-ai-part-8/
  - https://medium.com/@scrudato/deterministic-tests-for-complex-llm-rag-applications-b5a354b75346
  - https://arxiv.org/abs/2505.17716
related:
  - docs/research/2026-04-07-llm-as-judge.research.md
  - docs/research/2026-04-07-agent-frameworks.research.md
  - docs/research/2026-04-07-agentic-planning.research.md
---

## Summary

Agent systems require a fundamentally different testing philosophy than traditional software: layers represent tolerance for uncertainty rather than proximity to production. The four-layer testing pyramid—deterministic mocked unit tests, record-and-replay integration tests, LLM-as-judge probabilistic evals, and full agent simulation—gives teams a practical strategy for building confidence across both the deterministic scaffolding and the inherently stochastic model behavior. Continuous regression detection is achievable by integrating eval pipelines into CI/CD with golden datasets, threshold-based quality gates, and statistical rigor in reporting.

## Sources

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|-----------|------|------|--------|
| 1 | https://engineering.block.xyz/blog/testing-pyramid-for-ai-agents | Testing Pyramid for AI Agents | Block Engineering | 2025 | T1 | verified |
| 2 | https://medium.com/@derekcashmore/the-ai-agent-testing-pyramid-a-practical-framework-for-non-deterministic-systems-276c22feaec8 | The AI Agent Testing Pyramid: A Practical Framework for Non-Deterministic Systems | Derek Ashmore / Medium | Feb 2026 | T5 | verified |
| 3 | https://langwatch.ai/scenario/best-practices/the-agent-testing-pyramid/ | The Agent Testing Pyramid | LangWatch / Scenario | 2025 | T4 | verified |
| 4 | https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents | Demystifying Evals for AI Agents | Anthropic Engineering | 2025 | T1 | verified |
| 5 | https://www.anthropic.com/research/statistical-approach-to-model-evals | A Statistical Approach to Model Evaluations | Anthropic Research | 2025 | T1 | verified |
| 6 | https://www.evidentlyai.com/llm-guide/llm-as-a-judge | LLM-as-a-Judge: A Complete Guide | Evidently AI | 2025 | T4 | verified |
| 7 | https://newsletter.pragmaticengineer.com/p/evals | A Pragmatic Guide to LLM Evals for Devs | Pragmatic Engineer | 2025 | T4 | verified |
| 8 | https://langfuse.com/blog/2025-10-21-testing-llm-applications | LLM Testing: A Practical Guide to Automated Testing for LLM Applications | Langfuse | Oct 2025 | T4 | verified |
| 9 | https://www.braintrust.dev/articles/best-ai-evals-tools-cicd-2025 | Best AI Evals Tools for CI/CD in 2025 | Braintrust | 2025 | T4 | verified |
| 10 | https://www.promptfoo.dev/docs/integrations/ci-cd/ | CI/CD Integration for LLM Eval and Security | Promptfoo | 2025 | T1 | verified |
| 11 | https://www.getmaxim.ai/articles/building-a-golden-dataset-for-ai-evaluation-a-step-by-step-guide/ | Building a Golden Dataset for AI Evaluation | Maxim AI | 2025 | T4 | verified |
| 12 | https://www.confident-ai.com/docs/llm-evaluation/core-concepts/test-cases-goldens-datasets | Test Cases, Goldens, and Datasets | Confident AI / DeepEval | 2025 | T1 | verified |
| 13 | https://dev.to/sreeni5018/debugging-non-deterministic-llm-agents-implementing-checkpoint-based-state-replay-with-langgraph-5171 | Debugging Non-Deterministic LLM Agents: Checkpoint-Based State Replay with LangGraph | DEV Community | 2025 | T5 | verified |
| 14 | https://www.sakurasky.com/blog/missing-primitives-for-trustworthy-ai-part-8/ | Trustworthy AI Agents: Deterministic Replay | Sakura Sky | 2025 | T4 | verified |
| 15 | https://medium.com/@scrudato/deterministic-tests-for-complex-llm-rag-applications-b5a354b75346 | Deterministic Tests for Complex LLM RAG Applications | John Scrudato / Medium | 2025 | T5 | verified |
| 16 | https://arxiv.org/abs/2505.17716 | Get Experience from Practice: LLM Agents with Record & Replay | Shanghai Jiao Tong University / arXiv | May 2025 | T3 | verified |

## Extracts

### Sub-question 1: What is the current best practice testing pyramid for agent systems (deterministic base, LLM-as-judge middle, e2e top)?

The consensus across Block Engineering [1], Derek Ashmore [2], and the LangWatch/Scenario documentation [3] has converged on a four-layer pyramid where each layer represents an increasing tolerance for uncertainty—not simply proximity to production.

**Layer 1 — Deterministic Unit Tests (Foundation)**
Most tests use mock providers that return canned responses instead of calling real models, keeping this layer fast, cheap, and completely deterministic [1]. Tests cover retry behavior, tool schema validation, state management, extension management, and subagent delegation [1][2]. "What we're validating here is the scaffolding around the model, not model behavior itself" [2]. LangWatch [3] adds API connections, data transformation pipelines, memory storage, authentication, and rate limiting to this layer.

**Layer 2 — Constrained Model / Record-and-Replay Integration**
Block Engineering [1] uses a record-and-playback methodology: real MCP server interactions and LLM responses are recorded in JSON fixtures. Tests validate tool call sequences and interaction flow without asserting exact outputs. Ashmore [2] calls this "constrained model tests"—real API calls with temperature=0, fixed seeds, and structured output modes—suitable for objectively verifiable outcomes like data extraction, classification, and query generation. LangWatch [3] applies ML methodology (train/val splits, iterative prompt optimization with DSPy) for probabilistic components in isolation.

**Layer 3 — LLM-as-Judge Probabilistic Evaluation**
Block Engineering runs three evaluation rounds with majority voting to reduce randomness [1]. Ashmore describes this layer as evaluating "semantic correctness, tone, reasoning quality, and safety" and enabling "regression testing with natural language variation" [2]. Anthropic's framework names this "model-based graders"—"flexible and scalable but non-deterministic and requiring calibration" [4]. The fundamental shift: lower layers verify deterministic correctness; this layer measures quality across acceptable variation.

**Layer 4 — End-to-End Agent Simulation**
At the top sit full agent simulations, fewer in number but validating "can the agent actually solve real problems" [1]. Block Engineering emphasizes that patterns over multiple runs matter—"a single run tells us almost nothing but patterns tell us everything" [1]. Anthropic recommends starting with 20–50 tasks drawn from real failures, noting that "early changes have large effect sizes, so small sample sizes suffice" [4]. LangChain's 2026 State of AI Agents report found that 57% of organizations have agents in production and quality is the top barrier to deployment cited by 32%.

**The fundamental reframe:** "Layers now represent uncertainty tolerance rather than test types" [2]. Agent testing embraces probabilistic validation—measuring trends instead of exact matches, success rates instead of binary outcomes.

---

### Sub-question 2: How do record-and-replay, property-based, and snapshot testing apply to non-deterministic outputs?

**Record-and-Replay**
The VCR.py pattern [15] captures all HTTP interactions (LLM API calls) in YAML cassette files on first run, then intercepts identical requests on subsequent runs to return recorded responses—eliminating non-determinism at the API boundary while preserving realistic response content. The same principle is applied at the agent level by the AgentRR paper [16] from Shanghai Jiao Tong University: recording execution traces so most task steps can be replayed from a pre-derived plan, "drastically decreasing the number of LLM calls required."

Sakura Sky [14] formalizes this into seven implementation requirements: structured execution traces (append-only JSON events), complete metadata capture (model ID, sampling parameters, tool versions), a replay engine with cursor-based deterministic access, deterministic stubs replacing live LLM and tool dependencies, an injection-based harness keeping agent code unchanged, governance integration for compliance, and a regression testing framework using historical traces as golden files. LangGraph's Time Travel feature [13] implements checkpoint-based state snapshots at each workflow node, enabling "deterministic debugging of stochastic behavior through historical reconstruction."

**Snapshot / Golden File Testing**
Deterministic replay opens the door to golden file testing for agent systems [14]: replay past production runs against a new model version and compare outputs to the historical record. Rather than hand-crafting expected outputs, the first successful real run becomes the fixture. This is especially powerful for impact analysis—"replay thousands of past interactions against new model versions before production deployment, quantifying behavioral changes" [14].

**Property-Based Testing**
Rather than asserting specific outputs, PBT asserts invariants that must hold across the entire input space. Research on LLM-generated PBT [arXiv 2510.25297] shows that combining PBT with example-based testing improves bug detection from 68.75% (either alone) to 81.25% (combined). For agent systems, applicable invariants include: tool call schemas are always valid, retry counts never exceed configured maximums, context window budget is never exceeded, and structured output always parses as valid JSON. These invariants are deterministic even when model outputs vary—making PBT compatible with the bottom two pyramid layers.

---

### Sub-question 3: What eval pipeline designs support continuous regression detection for LLM-based tools?

**The Three-Component Model**
The current standard [8] divides eval pipelines into: (1) Datasets—versioned collections of input/output pairs; (2) Experiment runners—tools executing the application against datasets; (3) Evaluators—scoring functions using LLM-as-judge, semantic similarity, or custom logic. "A test passes if the evaluation score meets your threshold" [8], treating this as automated regression testing.

**CI/CD Integration Patterns**
Leading tools provide varying levels of CI/CD integration [9]:
- **Braintrust**: Dedicated GitHub Action (`braintrustdata/eval-action`) posting experiment comparisons directly on PRs; every run links quality changes to specific git commits
- **Promptfoo**: Native support across GitHub Actions, GitLab CI, Jenkins, CircleCI, with built-in caching and quality gate support (`--fail-on-error`, custom threshold parsing) [10]
- **Langfuse**: Experiment runner SDK with `langfuse_client.run_experiment()`; requires custom pipeline code; stores datasets remotely for centralized management [8]
- **DeepEval / Confident AI**: pytest-native integration; 50+ built-in metrics covering RAG quality, agent behavior (tool correctness, task completion), and safety

**Detecting Regressions Statistically**
Anthropic's statistical approach [5] warns against naive comparison: "Clustered standard errors on popular evals can be over three times as large as naive standard errors." Recommendations: report confidence intervals from standard error of the mean, use paired-difference analysis since questions are shared across model versions, apply variance reduction by resampling answers multiple times per question, and run power analysis before evaluation to determine required sample sizes.

Anthropic also introduces two metrics for agent reliability [4]:
- **pass@k**: Probability of at least one correct solution in k attempts (useful for measuring potential)
- **pass^k**: Probability all k trials succeed (the correct metric for production agents where users expect reliability every time)

**Continuous Improvement Flywheel**
The Pragmatic Engineer [7] describes a flywheel: Analyze production failures → Measure with evals → Improve prompts/model → Automate in CI/CD → Repeat. The critical warning: "Avoid generic metrics—pre-built hallucination or helpfulness scores create false security; they don't correlate with actual user satisfaction and become optimization targets disconnected from reality." Use binary PASS/FAIL over point-scale ratings to force explicit quality threshold definitions.

---

### Sub-question 4: How should test fixtures be designed for systems with natural language inputs/outputs?

**Goldens vs Test Cases**
Confident AI / DeepEval [12] distinguishes two fixture types: *goldens* are editable templates in datasets containing inputs plus metadata for invoking the app; *test cases* are immutable runtime outputs generated during eval runs. The relationship is directional: goldens → test cases. Key rule: "Avoid pre-populating dynamic fields in goldens—actual_output, retrieval_context, and tools_called should remain empty," as pre-populating defeats the evaluation's purpose.

**Golden Dataset Construction**
Maxim AI [11] identifies five foundational elements for golden datasets:
1. **Defined scope** — tailor to specific tasks (agent workflows, tool use, retrieval grounding)
2. **Production fidelity** — source from real logs and representative user scenarios
3. **Diversity** — cover varied topics, intents, difficulty levels, languages, and adversarial cases
4. **Decontamination** — remove training data overlap through exact matching and embedding similarity checks
5. **Dynamic evolution** — continuously integrate new failure modes and updated requirements

The construction workflow: define metrics first, source from production logs and SME-designed scenarios, generate synthetic variants through human-in-the-loop review, write annotation rubrics, perform integrity checks, attach governance metadata, determine statistically meaningful sample sizes, and establish versioning with release gates [11].

**Evaluator Design for Natural Language Outputs**
Evidently AI [6] recommends structuring LLM-as-judge prompts to use binary choices or low-precision scales (not 1-10 ratings), explicitly defining what each label means with examples, splitting multi-criteria evaluations into separate single-focus judges, requesting chain-of-thought reasoning, and setting temperature to 0 for consistency. "It's easier to critique than to create"—evaluation requires simpler cognitive tasks than generation, making judges more reliable than generation models at detecting specific quality properties [6].

**Multi-Turn Fixture Design**
For conversational agents, Confident AI [12] uses `ConversationalTestCase` with a `turns` list following OpenAI message format, where each assistant output depends on prior user inputs. Block Engineering [1] uses record-and-playback to capture real multi-turn conversation flows, then validates tool call sequences without asserting exact outputs—decoupling correctness of flow from correctness of phrasing.

**Maintaining Fixtures Over Time**
Anthropic [4] recommends treating eval suites like unit tests: monitor for saturation (when a suite becomes too easy), regularly read transcripts to verify evaluation fairness, and rebuild balanced datasets testing both positive and negative cases. The Pragmatic Engineer [7] adds open coding of production failures to continuously surface new failure categories that should become new fixtures.

## Search Protocol

| # | Query | Engine | Results |
|---|-------|--------|---------|
| 1 | agent testing pyramid LLM deterministic unit tests 2025 | WebSearch | 10 results; selected engineering.block.xyz, langwatch.ai/scenario, medium.com/@derekcashmore |
| 2 | LLM as judge testing non-deterministic outputs best practices 2025 | WebSearch | 10 results; selected evidentlyai.com, confident-ai.com, agenta.ai |
| 3 | eval pipeline LLM regression testing continuous integration 2025 | WebSearch | 10 results; selected braintrust.dev, langfuse.com, promptfoo.dev |
| 4 | record replay snapshot testing LLM agent non-deterministic 2025 | WebSearch | 10 results; selected arxiv.org/abs/2505.17716, sakurasky.com, medium.com/@scrudato |
| 5 | Anthropic evaluation methodology evals best practices 2025 | WebSearch | 10 results; selected anthropic.com/engineering/demystifying-evals, anthropic.com/research/statistical-approach |
| 6 | test fixtures natural language inputs LLM testing golden datasets 2025 | WebSearch | 10 results; selected getmaxim.ai, confident-ai.com/docs, evidentlyai.com |
| 7 | property based testing LLM applications invariants 2025 | WebSearch | 10 results; selected arxiv.org/abs/2510.25297, arxiv.org/abs/2506.18315 |
| 8 | DeepEval Promptfoo open source LLM testing framework comparison 2025 | WebSearch | 10 results; selected deepeval.com, zenml.io, promptfoo.dev |
| 9 | agent simulation testing end-to-end scenario framework LLM 2025 2026 | WebSearch | 10 results; selected getmaxim.ai/articles/exploring-effective-testing-frameworks |
| 10 | engineering.block.xyz/blog/testing-pyramid-for-ai-agents | WebFetch | Full article content extracted |
| 11 | anthropic.com/engineering/demystifying-evals-for-ai-agents | WebFetch | Full article content extracted |
| 12 | medium.com/@derekcashmore — AI agent testing pyramid | WebFetch | Full article content extracted |
| 13 | evidentlyai.com/llm-guide/llm-as-a-judge | WebFetch | Full article content extracted |
| 14 | langfuse.com/blog/2025-10-21-testing-llm-applications | WebFetch | Full article content extracted |
| 15 | braintrust.dev/articles/best-ai-evals-tools-cicd-2025 | WebFetch | Full article content extracted |
| 16 | promptfoo.dev/docs/integrations/ci-cd | WebFetch | Full article content extracted |
| 17 | getmaxim.ai/articles/building-a-golden-dataset | WebFetch | Full article content extracted |
| 18 | confident-ai.com/docs/llm-evaluation/core-concepts/test-cases-goldens-datasets | WebFetch | Full article content extracted |
| 19 | dev.to/sreeni5018 — LangGraph state replay | WebFetch | Full article content extracted |
| 20 | sakurasky.com/blog/missing-primitives-for-trustworthy-ai-part-8 | WebFetch | Full article content extracted |
| 21 | newsletter.pragmaticengineer.com/p/evals | WebFetch | Full article content extracted |
| 22 | langwatch.ai/scenario/best-practices/the-agent-testing-pyramid | WebFetch | Full article content extracted |
| 23 | medium.com/@scrudato — deterministic tests LLM RAG | WebFetch | Full article content extracted |
| 24 | anthropic.com/research/statistical-approach-to-model-evals | WebFetch | Full article content extracted |

## Challenge

### Claims Examined

| # | Claim | Challenge | Verdict |
|---|-------|-----------|---------|
| 1 | "The consensus across Block Engineering, Derek Ashmore, and the LangWatch/Scenario documentation has converged on a four-layer pyramid" | The "consensus" is vendor-adjacent practitioner content, not independent empirical validation. Rwilinski.ai proposes a three-layer structure (unit evals → trajectory evals → A/B testing) that replaces the integration and LLM-judge layers with real-user A/B as the apex. EPAM's "Testing Pyramid 2.0" argues the standard pyramid collapses when business logic lives inside a probabilistic model and proposes an integration-first model instead. The Automation Panda "Testing Skyscraper" (2025) and WireMock's economic critique both argue the pyramid metaphor imposes outdated quantity ratios rather than strategic risk coverage. Disagreement exists about both the number of layers and what each layer should contain. | qualified |
| 2 | "Block Engineering uses a record-and-playback methodology…Tests validate tool call sequences and interaction flow without asserting exact outputs" | Record-and-replay creates a silent validity problem: cassette files are recorded against a specific model version, tool version, and prompt state. When any of those change—model update, tool API version bump, prompt revision—the replay environment has drifted from the recording and the stubs no longer represent real system behavior. The Sakura Sky implementation requirements (source 14) acknowledge this, stating stubs must verify model IDs and version metadata and surface mismatches immediately; without this, the recorded test passes while the live system behaves differently. The arXiv AgentRR paper (source 16) focuses on cost and performance benefits, not on whether the recorded trace remains a valid regression signal after model or context drift. The technique also does not detect multi-agent cascading failures (MAST taxonomy documents 14 system-level failure modes invisible at the individual-agent level). | qualified |
| 3 | "Block Engineering runs three evaluation rounds with majority voting to reduce randomness…[LLM judges enable] regression testing with natural language variation" | Empirical research directly challenges whether LLM judges are reliable enough for regression detection. CIP.org (peer-reviewed sources cited) documents positional bias at 60–69% second-option preference, scale interpretation inconsistency (1.68 vs 3.17 on equivalent tasks with different scale formats), and 100% classification sensitivity to prompt template changes in ambiguous cases. The CMU ML blog (Dec 2025) identifies "rating indeterminacy"—where multiple scores are legitimately correct—leading to ranking inversions where the judge ranked best by standard agreement metrics increased estimation bias by 28%. The arXiv empirical study (2506.13639) finds chain-of-thought reasoning provides diminishing returns when criteria are clear, and omitting reference answers drops correlation from 0.666 to 0.487. Three-round majority voting reduces variance but does not eliminate positional, verbosity, or self-enhancement bias. Braintrust explicitly recommends against LLM judges for factual verification without grounding and warns of reward hacking where models exploit judge weaknesses. | qualified |
| 4 | "Continuous regression detection is achievable by integrating eval pipelines into CI/CD with golden datasets, threshold-based quality gates, and statistical rigor" | The LangChain State of AI Agents report (2026) shows only 52.4% of organizations run offline evals at all, and 37.3% run online evals—meaning roughly half of agent-shipping teams evaluate nothing systematically. The report does not break out CI/CD-integrated eval adoption, which is likely a subset of the 52.4%. A separate signal: the ZenML LLMOps study of 1,200 production deployments found sophisticated eval pipelines documented at Ramp, GitHub, and Cox Automotive without indicating whether these represent 5% or 50% of teams. The arXiv industry study (2504.18985) identifies a "moving target" problem—LLM capabilities change fast enough that evaluations have a "limited shelf life," requiring ongoing reassessment rather than stable thresholds. "Achievable" and "adopted" are different claims; the evidence supports the former but not the latter as the current norm. | qualified |
| 5 | "Layers now represent uncertainty tolerance rather than test types" (the fundamental reframe) | This reframe is asserted by a single practitioner source (Ashmore) and adopted by others writing in the same genre. It is a useful conceptual shift but lacks empirical validation—no study measures whether framing tests as "uncertainty tolerance layers" leads to better agent reliability outcomes than alternative framings. The rwilinski.ai three-layer model reframes the apex entirely around real user validation (A/B testing) rather than simulated e2e, arguing that synthetic end-to-end tests penalize improved agents that solve problems via different paths. This is a direct structural counter to the four-layer model's top tier. | qualified |

### Gaps Identified

- **No empirical validation of pyramid structure superiority**: All sources advocating the four-layer pyramid are practitioner blogs or vendor documentation. No controlled study compares teams using this structure versus alternatives (three-layer, trophy, skyscraper) on actual regression detection rates or agent reliability outcomes.
- **Record-and-replay maintenance cost undocumented**: The draft describes recording mechanics but does not address the maintenance burden when model versions, tool APIs, or prompts change frequently—a real operational cost in fast-moving agent stacks that could make replay fixtures a liability rather than an asset.
- **LLM judge calibration requirements unspecified**: The draft notes judges require "calibration" but does not specify what calibration entails operationally—how many human-labeled samples, at what cost, how often re-calibration is needed as the judge model itself is updated.
- **Threshold-setting methodology absent**: The draft assumes teams can define "quality gates" and score thresholds but does not address how to set those thresholds initially or how to update them without introducing ratchet effects (where thresholds drift upward to match whatever the current model produces).
- **Multi-agent system failures**: All four pyramid layers evaluate individual agents or individual interaction sequences. The MAST taxonomy's 14 documented multi-agent failure modes (cascading errors, correlated biases from shared base models, self-validation gaps) are invisible at any single-agent test layer. The pyramid as described offers no coverage strategy for emergent system-level failures.
- **CI/CD integration adoption gap**: The draft presents continuous eval in CI/CD as an established practice. The LangChain data (52% offline eval adoption, CI/CD integration rate unknown but lower) suggests this is aspirational for the majority of teams currently shipping agents in production.

### Additional Sources

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|-----------|------|------|--------|
| C1 | https://automationpanda.com/2025/09/29/the-testing-skyscraper-a-modern-alternative-to-the-testing-pyramid/ | The Testing Skyscraper: A Modern Alternative to the Testing Pyramid | Automation Panda | Sep 2025 | T5 | confirmed |
| C2 | https://www.wiremock.io/post/rethinking-the-testing-pyramid | The Testing Pyramid Is an Outdated Economic Model | WireMock / Tom Akehurst | 2025 | T4 | confirmed |
| C3 | https://rwilinski.ai/posts/evals-pyramid/ | Agentic Evals Pyramid | rwilinski.ai | 2025 | T5 | confirmed |
| C4 | https://www.epam.com/insights/ai/blogs/reimagining-testing-pyramid-for-genai-applications | Traditional Testing Is Failing GenAI Applications: Introducing the Testing Pyramid 2.0 | EPAM | 2025 | T4 | confirmed |
| C5 | https://www.cip.org/blog/llm-judges-are-unreliable | LLM Judges Are Unreliable | Collective Intelligence Project | 2025 | T4 | confirmed |
| C6 | https://arxiv.org/html/2506.13639v1 | An Empirical Study of LLM-as-a-Judge: How Design Choices Impact Evaluation Reliability | arXiv | Jun 2025 | T3 | confirmed |
| C7 | https://blog.ml.cmu.edu/2025/12/09/validating-llm-as-a-judge-systems-under-rating-indeterminacy/ | Validating LLM-as-a-Judge Systems under Rating Indeterminacy | CMU ML Blog | Dec 2025 | T3 | confirmed |
| C8 | https://www.braintrust.dev/articles/what-is-llm-as-a-judge | What Is an LLM-as-a-Judge? When to Use It (and When Not To) | Braintrust | 2025 | T4 | confirmed |
| C9 | https://www.langchain.com/state-of-agent-engineering | State of AI Agent Engineering | LangChain | 2026 | T4 | confirmed |
| C10 | https://arxiv.org/html/2504.18985v1 | Tracking the Moving Target: A Framework for Continuous Evaluation of LLM Test Generation in Industry | arXiv | Apr 2025 | T3 | confirmed |

## Findings

### What is the current best practice testing pyramid for agent systems?

A four-layer structure has emerged as the dominant practitioner model, but the underlying concept — **layers represent uncertainty tolerance, not proximity to production** — is the durable insight rather than any specific layer count. (MODERATE — T1 Anthropic + T4 Block Engineering + T4 vendors converge; no peer-reviewed study validates structure superiority over alternatives)

**Layer 1 — Deterministic unit tests (foundation):** Test the scaffolding around the model, not model behavior. Use mock providers returning canned responses. Cover retry logic, tool schema validation, state management, and subagent delegation [1][2]. Fast, cheap, deterministic. All sources agree this is the base [1][2][3][4].

**Layer 2 — Integration / record-and-replay:** Real API calls with temperature=0 and fixed seeds, or recorded cassette replay. Validates tool call sequences and interaction flow without asserting exact outputs [1][2]. Cassette-based replay requires metadata verification (model ID, tool version, prompt state) to detect fixture drift — a maintenance cost not reflected in most descriptions of the pattern [14].

**Layer 3 — LLM-as-judge probabilistic evaluation:** Semantic correctness, tone, reasoning quality, safety across varied natural language outputs. Run 3 rounds with majority voting to reduce variance [1][4]. The key limitation: LLM judges are subject to positional bias (60–69%), scale interpretation inconsistency, and rating indeterminacy — they are useful for trend measurement but not reliable as a sole binary gate [C5][C6][C7]. (HIGH for usefulness; HIGH for limitations)

**Layer 4 — End-to-end agent simulation:** Full task completion across real-world scenarios, evaluated by pass rate not binary outcome. Start with 20–50 tasks from real failures; small sample sizes suffice at early stages when effect sizes are large [4]. Patterns over multiple runs matter more than single-run outcomes [1].

**Counter-evidence:** Three alternative structures have genuine support — the rwilinski.ai three-layer model replaces e2e simulation with real A/B testing as the apex [C3]; EPAM's "Pyramid 2.0" proposes an integration-first model when business logic lives inside the model [C4]; WireMock argues the pyramid imposes quantity ratios inappropriate for risk-based testing [C2]. These are practitioner alternatives, not peer-reviewed studies.

### How do record-and-replay, property-based, and snapshot testing apply to non-deterministic outputs?

**Record-and-replay** is the most-cited technique for bridging determinism and real model behavior. VCR.py captures HTTP interactions as YAML cassettes; the AgentRR (arXiv SJTU) approach extends this to agent execution traces [15][16]. The technique enables deterministic regression of stochastic agents — run the same scenario against a new model version and compare. (MODERATE — T3 arXiv + T4 practitioner; real implementation requires maintenance discipline)

The silent validity problem: cassette files go stale when model version, tool API, or prompt changes. Sakura Sky's seven implementation requirements [14] mandate metadata verification to surface these mismatches. Without this, replay tests pass while the live system has diverged. Replay also has zero coverage of multi-agent cascading failures (MAST taxonomy: 14 system-level failure modes) that are invisible at the individual-agent trace level.

**Property-based testing** asserts structural invariants that hold regardless of model output: tool call schemas are always valid, retry counts never exceed limits, context window budget is never exceeded, structured output always parses as valid JSON [88]. These invariants are deterministic even when model content varies. Combining PBT with example-based testing improves bug detection from 68.75% to 81.25% [see search protocol source]. (MODERATE — T3 arXiv preprint; benefit statistic from one study)

**Snapshot / golden file testing**: Use first successful production runs as fixtures; replay new model versions against them to quantify behavioral change before deployment. Maxim AI's golden dataset construction methodology [11] applies: production fidelity, diversity, decontamination, dynamic evolution, and versioning with release gates.

### What eval pipeline designs support continuous regression detection?

The standard design is a three-component pipeline: **datasets → experiment runners → evaluators**. Score threshold gates in CI/CD enable automated regression blocking [8][9][10].

For CI/CD integration, Promptfoo [10] and Braintrust [9] have the strongest native support — Promptfoo integrates with GitHub Actions, GitLab CI, Jenkins, and CircleCI with built-in `--fail-on-error` gates. Langfuse and DeepEval require custom pipeline code but offer more flexibility.

**Statistical rigor requirements from Anthropic [5]**: Clustered standard errors on popular evals can be 3× larger than naive standard errors. Best practices: report confidence intervals, use paired-difference analysis, apply variance reduction by resampling answers multiple times per question, and run power analysis to determine sample size before evaluation. Prefer **pass^k** (all k trials succeed) over pass@1 for production agents — users expect reliability every time, not just occasionally [4].

**Critical limitation on adoption**: Only 52.4% of organizations run offline evals at all (LangChain 2026 State of AI Agents [C9]); CI/CD-integrated eval is an unknown but smaller subset. The "continuous regression detection" framing describes an achievable architecture, not current norm. Additionally, LLM capabilities change fast enough that eval thresholds have a "limited shelf life" — thresholds require ongoing reassessment as model versions improve [C10].

**Counter-evidence:** Using binary PASS/FAIL over point-scale ratings forces explicit threshold definition and reduces LLM judge score ambiguity [7]. Avoid generic pre-built metrics (hallucination scores, helpfulness scores) — they don't correlate with user satisfaction and become gaming targets [7].

### How should test fixtures be designed for systems with natural language inputs/outputs?

**Goldens vs. test cases distinction** [12]: Goldens are editable templates (inputs + metadata, no expected outputs pre-filled); test cases are immutable runtime outputs generated during eval. Never pre-populate `actual_output`, `retrieval_context`, or `tools_called` in goldens — doing so defeats the evaluation purpose.

**Golden dataset construction** [11]: Build from production logs with diversity across topics, intents, difficulty levels, and adversarial cases. Decontaminate for training data overlap. Evolve continuously by integrating new failure modes. Treat the dataset as a versioned artifact with release gates.

**LLM judge prompt design** [6]: Use binary choices or low-precision scales (not 1–10 ratings). Define labels explicitly with examples. Split multi-criteria evaluations into separate single-focus judges. Request chain-of-thought. Set temperature=0 for consistency. Binary PASS/FAIL forces explicit threshold definition and is more reliable than graduated scales for regression detection.

**Fixture maintenance** [4][7]: Treat eval suites like unit tests — monitor for saturation (when suites become too easy), read transcripts regularly to verify judge fairness, continuously rebuild from production failure analysis. Open-code production failures to surface new failure categories that become new fixtures.

## Takeaways

1. **Layers = uncertainty tolerance, not test type.** The durable insight from the testing pyramid is not the layer count but the principle: build confidence progressively from deterministic scaffolding tests (mocks, schema validation) up to probabilistic quality evaluation (LLM judges, e2e simulation). Use pass rates and trends, not binary outcomes.

2. **Record-and-replay works but requires fixture maintenance.** Cassette files go stale with model/tool/prompt changes. Implement metadata verification (model ID, tool version, prompt hash) to detect drift. Treat recorded traces as versioned artifacts, not permanent fixtures.

3. **LLM judges are trend detectors, not hard gates.** Positional bias (60–69%), scale inconsistency, and rating indeterminacy make LLM judges unsuitable as sole binary CI gates. Use majority voting (3 rounds), binary PASS/FAIL prompts, temperature=0, and single-focus criteria. Combine with deterministic structural checks for gating decisions.

4. **Continuous eval in CI/CD is achievable but not yet the norm.** Promptfoo and Braintrust have the strongest native CI/CD integration. Only ~52% of teams run any offline evals; CI/CD-integrated is a subset. Eval thresholds have a limited shelf life as model capabilities improve — plan for reassessment cadences.

5. **Property-based testing complements example-based testing.** Assert structural invariants (schema validity, budget limits, JSON parsability) that hold regardless of model output. Combining PBT with example-based testing improves bug detection from ~69% to ~81% in research settings.

## Claims

| # | Claim | Type | Source | CoVe Question | CoVe Answer | Status |
|---|-------|------|--------|--------------|-------------|--------|
| 1 | "Clustered standard errors on popular evals can be over three times as large as naive standard errors" | quoted statistic | Anthropic Research [5] — anthropic.com/research/statistical-approach-to-model-evals | Does source [5] contain this exact or equivalent statement? | Source [5] is listed as T1 (Anthropic Research, 2025) and the Findings section attributes this figure directly to it in Sub-question 3; the same wording appears verbatim in the Extracts. The document's own sourcing is internally consistent. Cannot cross-check the live URL without fetching, but attribution is unambiguous. | human-review |
| 2 | "Only 52.4% of organizations run offline evals at all" | quoted statistic | LangChain 2026 State of AI Agents [C9] | Is this figure attributed to [C9] throughout the document, and is the source identified as LangChain 2026? | Yes — the figure appears in the Findings ("Only 52.4% of organizations run offline evals at all (LangChain 2026 State of AI Agents [C9])") and in the Challenge section and Takeaways. Source C9 is listed as T4, LangChain, 2026. Attribution is consistent across all three sections. | human-review |
| 3 | "57% of organizations have agents in production and quality is the top barrier to deployment cited by 32%" | quoted statistic | LangChain 2026 State of AI Agents (inline in Extracts, Layer 4) | Is the 57%/32% figure tied to the same LangChain [C9] source used elsewhere in the document? | The claim appears in the Extracts section (Layer 4) without an inline citation marker, unlike other Extracts claims that carry numbered citations. Source [C9] is added only in the Challenge/Additional Sources section. The 57%/32% figure has no traceable citation anchor in the Extracts where it appears — it cannot be confirmed as coming from [C9] or any other listed source based solely on the document itself. | human-review |
| 4 | "Positional bias at 60–69% second-option preference" for LLM judges | quoted statistic | CIP.org [C5] — cip.org/blog/llm-judges-are-unreliable | Is [C5] the source, and does the document attribute this range consistently? | The 60–69% figure is attributed to [C5] in the Challenge section ("CIP.org (peer-reviewed sources cited) documents positional bias at 60–69% second-option preference"). The same figure appears in Findings and Takeaways as "Positional bias (60–69%)." Attribution to [C5] is internally consistent across all sections. | human-review |
| 5 | "Combining PBT with example-based testing improves bug detection from 68.75% (either alone) to 81.25% (combined)" | quoted statistic | arXiv 2510.25297 (referenced in Search Protocol query 7) | Does a cited source in the document support these specific percentages? | The Extracts cite "Research on LLM-generated PBT [arXiv 2510.25297]" for these figures, but arXiv:2510.25297 does not appear in the Sources frontmatter or the Sources table — only arXiv:2505.17716 is listed. The Search Protocol row 7 references arXiv:2510.25297 as a result but it was not elevated to a listed source. The Findings section notes "(MODERATE — T3 arXiv preprint; benefit statistic from one study)" and later says "[see search protocol source]" rather than citing a numbered source. The supporting paper is not formally tracked. | human-review |
| 6 | Anthropic recommends "starting with 20–50 tasks drawn from real failures" for e2e agent simulation | named attribution with specific number | Anthropic Engineering [4] — anthropic.com/engineering/demystifying-evals-for-ai-agents | Is source [4] the named attribution for this specific recommendation? | Yes — the Extracts state: "Anthropic recommends starting with 20–50 tasks drawn from real failures, noting that 'early changes have large effect sizes, so small sample sizes suffice' [4]." The Findings repeat "Start with 20–50 tasks from real failures; small sample sizes suffice at early stages when effect sizes are large [4]." Attribution is consistent. | human-review |
| 7 | pass^k is described as "the correct metric for production agents where users expect reliability every time" | superlative / named capability | Anthropic Engineering [4] | Does the document attribute this framing to [4], and is pass^k defined consistently? | Yes — Sub-question 3 Extracts define both metrics with source [4]: "pass^k: Probability all k trials succeed (the correct metric for production agents where users expect reliability every time)." The Findings section repeats "Prefer pass^k (all k trials succeed) over pass@1 for production agents [4]." Internally consistent. | human-review |
| 8 | Promptfoo "Native support across GitHub Actions, GitLab CI, Jenkins, CircleCI, with built-in caching and quality gate support" | named tool capability | Promptfoo [10] — promptfoo.dev/docs/integrations/ci-cd | Is Promptfoo's CI/CD scope attributed to source [10] throughout the document? | Yes — the Extracts cite [10] for this exact list. The Findings section states "Promptfoo [10] and Braintrust [9] have the strongest native support — Promptfoo integrates with GitHub Actions, GitLab CI, Jenkins, and CircleCI with built-in --fail-on-error gates." Source [10] is listed as T1 (Promptfoo, 2025). Attribution is consistent. | human-review |
| 9 | "Block Engineering runs three evaluation rounds with majority voting to reduce randomness" | named attribution | Block Engineering [1] — engineering.block.xyz/blog/testing-pyramid-for-ai-agents | Is three-round majority voting attributed to [1] in the document? | Yes — the Extracts state "Block Engineering runs three evaluation rounds with majority voting to reduce randomness [1]." The Findings repeat "Run 3 rounds with majority voting to reduce variance [1][4]." Source [1] is T1 (Block Engineering, 2025). Consistent across both sections. | human-review |
| 10 | AgentRR paper "drastically decreasing the number of LLM calls required" by replaying pre-derived plans | quoted phrase | arXiv:2505.17716, Shanghai Jiao Tong University [16] | Is this quoted phrase attributed to source [16] and does [16] appear in both the frontmatter sources and the Sources table? | Yes — arXiv:2505.17716 is listed in the frontmatter `sources` array and in the Sources table as row 16 (T3, Shanghai Jiao Tong University, May 2025). The Extracts attribute the phrase "drastically decreasing the number of LLM calls required" to [16]. Consistent. The phrase is in quotation marks suggesting it is a direct quote, but cannot be verified without fetching the paper. | human-review |
| 11 | "The judge ranked best by standard agreement metrics increased estimation bias by 28%" | quoted statistic | CMU ML Blog [C7] — blog.ml.cmu.edu/2025/12/09/validating-llm-as-a-judge-systems-under-rating-indeterminacy | Is this figure attributed to [C7] and does [C7] appear consistently in the document? | The 28% figure appears only in the Challenge section: "the judge ranked best by standard agreement metrics increased estimation bias by 28%." Source [C7] is listed in the Additional Sources table (T3, CMU ML Blog, Dec 2025). The figure does not recur in the Findings or Takeaways, which reference "rating indeterminacy" conceptually without the specific number. Attribution to [C7] in the Challenge section is the only anchor — not traceable to any other part of the document. | human-review |
| 12 | "DeepEval / Confident AI: pytest-native integration; 50+ built-in metrics covering RAG quality, agent behavior (tool correctness, task completion), and safety" | specific tool capability count | Braintrust [9] comparison article — braintrust.dev/articles/best-ai-evals-tools-cicd-2025 | Is the "50+ built-in metrics" figure for DeepEval attributed to a specific source in the document? | The claim appears in the Extracts under "CI/CD Integration Patterns" with a header citation "[9]" applying to the entire bulleted list. Source [9] is the Braintrust article comparing eval tools for CI/CD. The "50+" figure for a competitor (DeepEval) is reported within a Braintrust-authored comparison — introducing potential attribution bias. No independent DeepEval source (e.g., deepeval.com) is in the document's sources list. The count is not traceable to a primary source for DeepEval itself. | human-review |
