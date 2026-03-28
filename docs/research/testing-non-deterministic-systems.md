---
name: "Testing Non-Deterministic Systems"
description: "Industry has converged on a three-layer testing pyramid for agent systems: deterministic unit tests, LLM-as-judge quality evaluation, and end-to-end scenarios, supported by property-based testing, golden dataset regression, and eval frameworks (DeepEval, promptfoo, Langfuse)"
metadata:
  type: research
  sources:
    - https://dev.to/aws/beyond-traditional-testing-addressing-the-challenges-of-non-deterministic-software-583a
    - https://engineering.block.xyz/blog/testing-pyramid-for-ai-agents
    - https://datagrid.com/blog/4-frameworks-test-non-deterministic-ai-agents
    - https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
    - https://www.anthropic.com/research/building-effective-agents
    - https://www.confident-ai.com/blog/llm-testing-in-2024-top-methods-and-strategies
    - https://langfuse.com/blog/2025-10-21-testing-llm-applications
    - https://towardsdatascience.com/how-we-are-testing-our-agents-in-dev/
    - https://www.sitepoint.com/testing-ai-agents-deterministic-evaluation-in-a-non-deterministic-world/
    - https://github.com/confident-ai/deepeval
    - https://www.promptfoo.dev/docs/configuration/expected-outputs/
    - https://rchaves.app/the-agent-testing-pyramid/
    - https://langfuse.com/blog/2025-11-12-evals
    - https://www.traceloop.com/blog/automated-prompt-regression-testing-with-llm-as-a-judge-and-ci-cd
  related:
    - docs/research/validation-architecture.md
    - docs/research/tool-design-for-llms.md
    - docs/context/agent-testing-pyramid.md
    - docs/context/llm-as-judge-evaluation.md
    - docs/context/eval-framework-landscape.md
---

## Summary

Testing agent-driven systems requires abandoning exact-match expectations in favor of layered strategies that separate deterministic from non-deterministic concerns. The industry has converged on an adapted testing pyramid (HIGH confidence):

1. **Base: deterministic unit tests** -- tool routing, state machines, schema validation, argument parsing. Use mock providers with record-and-replay. Run in CI.
2. **Middle: LLM quality evaluation** -- behavioral assertions via LLM-as-judge, structural checks (JSON schema, regex), soft scoring (0-1 continuous scale). Run pre-release.
3. **Top: end-to-end scenarios** -- multi-turn conversation simulations, complex tool-use sequences. Run on-demand.

Key patterns: property-based testing for invariant verification, golden dataset regression with fuzzy matching (cosine similarity, BERTScore), structural contracts for output shape, and eval frameworks (DeepEval, promptfoo, Langfuse) that bring CI/CD discipline to non-deterministic outputs. Contract testing for agent-tool interfaces is conceptually sound but has limited direct evidence in current practice.

16 searches across Google, 14 sources used (6 T1, 4 T4, 3 T5). Counter-evidence documented for each finding.

## Findings

### What testing strategies work for non-deterministic LLM outputs?

The fundamental shift is from exact-match assertions to property-based and behavioral assertions that verify what outputs *should* be rather than what they *are* (HIGH -- T1 + T4 sources converge [1][2][3][8]).

**Behavioral testing** replaces equality checks with semantic evaluation. Instead of `assert output == expected`, teams verify that outputs satisfy behavioral properties: Does the response address the query? Does it stay within scope? Does it use the correct tools? Three dimensions have emerged as standard evaluation axes: semantic distance (is the output close enough to a reference?), groundedness (can claims be traced to provided context?), and tool usage (did the agent invoke the right tool with correct parameters?) [8] (MODERATE -- single practitioner source, but consistent with framework documentation [10]).

**Structural assertions** check output shape independently of content. JSON schema validation, required field presence, response length bounds, and format compliance can all be tested deterministically even when the content varies. Promptfoo's assertion system supports checking JSON structure, regex patterns, and custom validation functions alongside semantic similarity [11] (HIGH -- T1 official documentation).

**Property-based testing** verifies invariants that must hold regardless of the specific output. For LLM systems, useful properties include: outputs must parse as valid JSON/YAML, tool calls must reference defined tools, response length falls within bounds, no sensitive data leakage, and idempotent operations produce consistent side effects [1]. The Hypothesis framework can generate random inputs to test these invariants, though defining meaningful properties for natural language is harder than for algorithmic outputs (MODERATE -- property-based testing for LLMs is discussed primarily in one T4 source [1]; the technique is well-established in traditional software but less proven for agent outputs).

**Soft scoring replaces binary pass/fail.** Multiple sources independently describe a continuous scoring model where LLM evaluation scores between 0-1 are categorized: below 0.5 is a hard failure, 0.5-0.8 is a "soft failure" (tolerable individually, but triggering a hard failure if 33% of tests are soft failures or more than 2 occur), and above 0.8 is a pass [3][8] (MODERATE -- two independent sources describe the same thresholds, suggesting shared origin or convergent practice).

**Multi-trial evaluation** averages scores across 3+ runs to absorb non-deterministic variance. Block Engineering runs LLM-as-judge evaluations three times and takes the majority result [2]. Anthropic defines each attempt at a task as a "trial" and recommends multiple trials for consistency [4] (HIGH -- T1 + T4 converge).

**Counter-evidence:** The soft failure model and multi-trial approach add cost and complexity. Running evals 3x triples LLM judge costs, and the thresholds (0.5/0.8) appear to be heuristics rather than empirically derived. Teams should calibrate thresholds to their specific quality requirements rather than adopting defaults.

### How should systems separate deterministic and LLM layers for independent testing?

The industry has converged on an adapted testing pyramid with three distinct layers mapped to determinism boundaries (HIGH -- multiple independent T1 + T4 sources [2][3][4][5][12]).

**Base layer: deterministic logic.** Tool call routing, argument parsing, response formatting, state machine transitions, retry behavior, max turn limits, and schema validation are all testable with traditional unit tests. Block Engineering uses mock providers that return canned responses instead of calling real models, keeping this layer fast, cheap, and completely deterministic [2]. This layer answers: "Did we write correct software?" If it's flaky, the problem is in the software, not the AI (HIGH -- T4 source with detailed implementation, consistent with T1 guidance [4][5]).

**Record-and-replay for the boundary.** Block Engineering's TestProvider operates in two modes: recording mode captures real LLM request/response pairs into JSON files keyed by input hash; replay mode serves those recordings deterministically. This converts the non-deterministic LLM boundary into a deterministic one for regression testing [2] (MODERATE -- detailed description from single source, but the pattern is well-known in API testing).

**Middle layer: LLM quality evaluation.** Frameworks like DeepEval measure faithfulness, relevance, and hallucination using LLM-as-judge. These tests are slower and costlier because they call an external judge model, but they catch quality regressions that deterministic tests cannot [3][10] (HIGH -- T1 framework docs + multiple practitioner sources).

**Top layer: end-to-end scenarios.** Scenario-based evaluation suites simulate multi-turn conversations or complex tool-use sequences, validating that the full pipeline holds together. These are fewest in number but test what matters most: can the agent solve real problems? [3][12] (HIGH -- multiple independent sources).

**CI philosophy:** CI validates the deterministic layers. Live LLM tests are too expensive, too slow, and too flaky for CI [2]. The middle and top layers run on-demand, pre-release, or on a schedule (MODERATE -- reflects one team's practice that may not generalize to all contexts).

**Architectural isolation via ports.** Hexagonal architecture (ports and adapters) supports this separation. Defining an IntelligencePort isolates prompts and orchestration logic from the specific LLM provider, enabling mock implementations for testing and provider swapping without touching business logic (MODERATE -- architectural pattern is well-established, but application to LLM systems specifically has limited direct evidence).

**Counter-evidence:** Clean separation assumes the LLM is a swappable component, but agent behavior emerges from the interaction between deterministic logic and LLM reasoning. Mocking the LLM removes the emergent behavior that causes production failures. The record-and-replay pattern captures one execution trace but misses the variance that makes testing necessary in the first place.

### What eval frameworks exist for LLM-based systems?

Three categories of tools have emerged, each with distinct strengths (HIGH -- multiple T1 sources document their own tools [10][11][7][13]).

**Code-first evaluation: DeepEval.** An open-source Python framework that integrates with pytest via `deepeval test run`. Supports 50+ research-backed metrics including G-Eval, answer relevancy, faithfulness, and hallucination detection. Uses LLM-as-judge with configurable judge models (OpenAI, Anthropic, Ollama, etc.). Designed for engineering teams who want evaluation as a code-level testing activity in local development and CI [10][6] (HIGH -- T1 official docs).

**Config-driven evaluation: promptfoo.** Uses YAML configuration to define test cases with assertions. Supports deterministic assertions (equality, JSON schema, regex), model-graded assertions (LLM-as-judge with rubrics), and similarity-based assertions. Quality gates enforce minimum performance thresholds. The `validate` command exits with code 1 on failure, integrating cleanly with CI/CD pipelines. Preferred by teams in Node.js environments and for security/red-teaming use cases [11] (HIGH -- T1 official docs).

**Observability-integrated evaluation: Langfuse.** Open-source LLM engineering platform combining tracing, evaluation, and dataset management. Supports LLM-as-judge, user feedback, manual labeling, and custom evaluation pipelines. Every evaluation execution creates a trace for inspection. Datasets enable structured experiment runs. Key differentiator is connecting evaluation with production observability -- teams can debug production traces and convert them into test cases [7][13] (HIGH -- T1 official docs).

**Regression testing: Traceloop.** Built on OpenTelemetry for deep trace visibility. Enables automated prompt regression testing where new prompt versions run against test datasets, with LLM-as-judge scoring each output. CI/CD gates check for quality, performance, and cost regressions [14] (MODERATE -- single T4 source).

**Anthropic's eval methodology.** Rather than providing a framework, Anthropic describes a methodology: define tasks with clear inputs and success criteria, run multiple trials per task, apply graders (deterministic + LLM-based). Start with 20-50 simple tasks drawn from real failures. Grade outcomes, not paths -- agents may find creative solutions that static evals incorrectly fail. In tau2-bench, Opus 4.5 discovered a loophole in an airline policy that "failed" the eval but actually produced a better solution for the user [4] (HIGH -- T1 source from LLM provider with deployment experience).

### How do snapshot testing and contract testing patterns apply to agent workflows?

**Adapted snapshot testing (golden datasets).** Traditional snapshot testing captures expected output and fails when output changes. For LLM systems, this adapts into golden dataset testing: maintain 20-50 curated input-output pairs covering common use cases and known failure modes [4]. Rather than exact comparison, use fuzzy matching via cosine similarity on embeddings or BERTScore to detect semantic drift [1]. The best test cases come from real production traffic [6] (MODERATE -- pattern is widely described but detailed implementation varies; fuzzy matching thresholds are not standardized).

**Record-and-replay as snapshot testing.** Block Engineering's TestProvider pattern [2] is essentially snapshot testing for LLM interactions: record real LLM responses, replay them deterministically. This provides regression protection for the integration layer without live LLM calls (HIGH -- T4 source with detailed implementation).

**Contract testing for agent-tool interfaces.** Consumer-driven contract testing (popularized by Pact) can apply to agent-tool boundaries: the agent (consumer) expects tools to accept certain input schemas and return certain output schemas; the tool (provider) verifies it meets those contracts. This catches integration breakage when tools evolve independently of agent code (MODERATE -- contract testing is well-established for microservices, but direct evidence of application to agent-tool boundaries is limited in current literature).

**Structural contracts for LLM outputs.** A more practical variant: define output contracts as JSON schemas, required fields, or format specifications that the LLM must satisfy. Promptfoo's JSON structure assertions [11] and DeepEval's schema validation [10] serve this purpose. These are deterministic and cheap to run, catching structural regressions (format changes, missing fields) while leaving semantic evaluation to costlier methods (HIGH -- supported by T1 framework documentation).

**Prompt regression testing as contract enforcement.** Traceloop's approach [14] treats the prompt-to-quality relationship as an implicit contract: when a prompt changes, automated evaluation verifies the new version meets the same quality thresholds as the previous version. CI/CD gates fail the build if quality regresses, analogous to contract test failures breaking a build (MODERATE -- T4 source, but the analogy to contract testing is the author's inference rather than explicit in the source).

**Counter-evidence:** Traditional contract testing assumes specified interfaces with stable schemas. Agent-tool interactions often involve natural language or semi-structured data where the "contract" is harder to formalize. The emergent nature of agent behavior means the most important quality properties may not be capturable as contracts. Current evidence for contract testing patterns applied specifically to agent workflows is thin compared to the other strategies investigated.

## Challenge

### Assumptions Check

| Assumption | Supporting Evidence | Counter-Evidence | Impact if False |
|------------|-------------------|------------------|-----------------|
| The three-layer testing pyramid (deterministic / eval / E2E) is the right decomposition for agent systems | Multiple independent sources converge on this pattern [2][3][8][12] | No source challenges the pyramid itself, but several note proportions vary by maturity [12] | If false, teams might over-invest in one layer; low impact since the layers map to real architectural boundaries |
| LLM-as-judge is reliable enough for automated quality gates | Anthropic recommends it [4], research shows 85% alignment with human judgment, multiple teams use it in CI [8][14] | LLM judges exhibit position bias, length bias, and inconsistent reasoning when prompts change; requires "testing your tests" [8] | If unreliable, the entire middle layer of the pyramid becomes untrustworthy; teams fall back to manual review, losing automation benefits |
| Deterministic and non-deterministic layers can be cleanly separated | Block Engineering's TestProvider pattern [2], hexagonal architecture literature, Anthropic's composable patterns [5] | Real agent workflows have emergent behavior from layer interaction; mocking the LLM removes the very thing being tested | If separation is impractical, the base layer of the pyramid shrinks and testing cost increases substantially |
| Property-based testing transfers effectively from traditional software to LLM outputs | AWS article describes it for non-deterministic functions [1], Hypothesis framework exists | LLM outputs have different invariant structures than algorithmic outputs; properties are harder to define for natural language | If properties are too weak, tests pass trivially; if too strict, they produce false failures |
| Golden datasets and snapshot testing provide meaningful regression detection | Multiple sources recommend golden sets of 20-50 examples [4][6]; fuzzy matching techniques exist | LLM outputs drift semantically even when correct; snapshot tests may be overly sensitive or insensitive | If ineffective, prompt regressions go undetected until production |

### Premortem

| Failure Reason | Plausibility | Impact on Conclusion |
|----------------|-------------|---------------------|
| LLM-as-judge evaluation becomes a tautology (using LLMs to test LLMs creates circular validation) | Medium | Qualifies finding on middle-layer testing; teams should maintain human calibration and not rely solely on LLM judges |
| The testing pyramid pattern is descriptive of current practice rather than prescriptive best practice (survivorship bias from well-resourced teams like Block and Anthropic) | Medium | Qualifies applicability; smaller teams may need simpler approaches, not the full pyramid |
| Contract testing patterns from microservices don't map well to agent-tool interactions because agent behavior is emergent rather than specified | High | Weakens the contract testing finding; current evidence for this specific application is thin |

## Sources

| # | URL | Title | Author/Org | Date | Status | Tier |
|---|-----|-------|-----------|------|--------|------|
| 1 | https://dev.to/aws/beyond-traditional-testing-addressing-the-challenges-of-non-deterministic-software-583a | Beyond Traditional Testing | Danilo Poccia / AWS | 2024 | verified | T4 |
| 2 | https://engineering.block.xyz/blog/testing-pyramid-for-ai-agents | Testing Pyramid for AI Agents | Block Engineering | 2026 | verified | T4 |
| 3 | https://datagrid.com/blog/4-frameworks-test-non-deterministic-ai-agents | 4 Frameworks to Test Non-Deterministic AI Agent Behavior | Datagrid | 2025 | verified | T5 |
| 4 | https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents | Demystifying Evals for AI Agents | Anthropic | 2025 | verified | T1 |
| 5 | https://www.anthropic.com/research/building-effective-agents | Building Effective Agents | Anthropic | 2024 | verified | T1 |
| 6 | https://www.confident-ai.com/blog/llm-testing-in-2024-top-methods-and-strategies | LLM Testing in 2025: Top Methods and Strategies | Confident AI | 2025 | verified | T4 |
| 7 | https://langfuse.com/blog/2025-10-21-testing-llm-applications | LLM Testing: A Practical Guide | Langfuse | 2025 | verified | T1 |
| 8 | https://towardsdatascience.com/how-we-are-testing-our-agents-in-dev/ | How We Are Testing Our Agents in Dev | Towards Data Science | 2025 | verified | T4 |
| 9 | https://www.sitepoint.com/testing-ai-agents-deterministic-evaluation-in-a-non-deterministic-world/ | Testing AI Agents: Validating Non-Deterministic Behavior | SitePoint | 2025 | verified | T5 |
| 10 | https://github.com/confident-ai/deepeval | DeepEval: The LLM Evaluation Framework | Confident AI | 2025 | verified | T1 |
| 11 | https://www.promptfoo.dev/docs/configuration/expected-outputs/ | Assertions and Metrics - LLM Output Validation | Promptfoo | 2025 | verified | T1 |
| 12 | https://rchaves.app/the-agent-testing-pyramid/ | The Agent Testing Pyramid | Rogerio Chaves | 2025 | verified | T5 |
| 13 | https://langfuse.com/blog/2025-11-12-evals | Evaluating LLM Applications: A Comprehensive Roadmap | Langfuse | 2025 | verified | T1 |
| 14 | https://www.traceloop.com/blog/automated-prompt-regression-testing-with-llm-as-a-judge-and-ci-cd | Automated Prompt Regression Testing | Traceloop | 2025 | verified | T4 |

## Claims

| # | Claim | Type | Source | Status |
|---|-------|------|--------|--------|
| 1 | DeepEval supports 50+ research-backed metrics | statistic | [10] | corrected (initial search said "60+"; official docs say "50+") |
| 2 | Block Engineering's TestProvider saves recordings to a JSON file keyed by a hash of the input messages | attribution | [2] | verified |
| 3 | Anthropic recommends 20-50 simple tasks drawn from real failures for eval suites | statistic | [4] | verified |
| 4 | Opus 4.5 solved a tau2-bench problem by discovering a loophole in airline policy | attribution | [4] | verified |
| 5 | LLM judges can align with human judgment up to 85%, higher than human-to-human agreement at 81% | statistic | Chatbot Arena research | verified |
| 6 | Soft failure thresholds: below 0.5 hard failure, 0.5-0.8 soft failure, above 0.8 pass | statistic | [8] | verified |
| 7 | Promptfoo's validate command exits with code 1 if validation fails | attribution | [11] | verified |
| 8 | Langfuse's LLM-as-a-Judge evaluator execution creates a trace for inspection | attribution | [7] | verified |
| 9 | Traceloop is built on OpenTelemetry | attribution | [14] | verified |

## Key Takeaways

1. **Test the layers you can control deterministically, evaluate the rest.** The three-layer pyramid (deterministic / eval / E2E) maps to real architectural boundaries. Put maximum investment in the deterministic base layer where traditional testing works.

2. **LLM-as-judge is the practical middle ground** between "can't test it" and "test it perfectly." Research shows 85% alignment with human judgment. Use it with multi-trial evaluation (3+ runs) and always test the judge prompts themselves.

3. **Property-based and structural assertions are underutilized.** Most teams jump to LLM-as-judge for everything. Start with cheap structural assertions (schema validation, format compliance, tool call correctness) before reaching for expensive eval metrics.

4. **Golden datasets beat snapshots for LLM regression.** Maintain 20-50 curated test cases from real failures and production traffic. Use fuzzy semantic matching rather than exact comparison.

5. **Contract testing for agent-tool interfaces is promising but unproven.** Structural output contracts (JSON schemas, required fields) work well. Full consumer-driven contract testing (Pact-style) for agent-tool boundaries lacks established patterns.

6. **Don't run live LLM tests in CI.** Use record-and-replay for deterministic regression, LLM-as-judge evaluations pre-release, and E2E scenario tests on-demand.

## Limitations

- Sources are predominantly from tool vendors (Anthropic, Confident AI, Promptfoo, Langfuse) documenting their own approaches. Independent academic research on agent testing patterns is emerging but limited.
- The testing pyramid pattern is primarily documented by well-resourced teams (Block, Anthropic). Applicability to smaller teams and simpler agent systems needs qualification.
- Contract testing for agent workflows is an analogy from microservices, not a documented practice. Evidence is thin.
- Property-based testing for LLM outputs is theoretically sound but lacks detailed case studies beyond simple structural invariants.

## Follow-Ups

- Investigate LLM-as-judge calibration techniques: how to detect and correct for position bias, length bias, and prompt sensitivity in judge evaluations.
- Research multi-agent evaluation patterns (agent-as-judge) where multiple LLM agents collaboratively assess outputs.
- Explore how teams establish and update fuzzy matching thresholds for golden dataset regression tests.
- Study how the testing pyramid proportions should shift as agent systems mature from prototype to production.

## Search Protocol

| Query | Source | Date Range | Found | Used |
|-------|--------|------------|-------|------|
| testing non-deterministic LLM outputs behavioral testing structural assertions | google | 2024-2025 | 10 | 4 |
| property-based testing LLM agent workflows | google | 2024-2025 | 10 | 2 |
| testing AI agent systems non-deterministic outputs engineering patterns | google | 2025 | 10 | 4 |
| separating deterministic LLM layers testing architecture hexagonal ports adapters | google | 2024-2025 | 10 | 2 |
| LLM eval frameworks DeepEval Braintrust promptfoo comparison | google | 2025 | 10 | 3 |
| snapshot testing contract testing AI agent workflows pact consumer-driven | google | 2025 | 10 | 1 |
| LLM output snapshot testing golden file testing fuzzy matching approval tests | google | 2025 | 10 | 3 |
| Anthropic building effective agents testing evaluation patterns | google | 2024 | 10 | 2 |
| LLM-as-judge evaluation pattern testing agent outputs | google | 2025 | 10 | 3 |
| Anthropic demystifying evals agents evaluation best practices | google | 2025 | 10 | 2 |
| testing pyramid AI agents unit integration end-to-end deterministic non-deterministic layers | google | 2025 | 10 | 4 |
| promptfoo LLM testing assertions YAML CI/CD integration | google | 2025 | 10 | 2 |
| DeepEval pytest integration LLM metrics faithfulness hallucination testing | google | 2025 | 10 | 2 |
| Langfuse evaluation tracing LLM testing observability | google | 2025 | 10 | 2 |
| Block engineering testing pyramid AI agents blog deterministic mock providers | google | 2025 | 10 | 1 |
| towards data science testing agents dev practical approaches mock LLM | google | 2025 | 10 | 2 |

16 searches across Google, 160 results found, 37 results used, 14 sources retained.
Not searched: ACM Digital Library, IEEE Xplore, Google Scholar (direct access).
