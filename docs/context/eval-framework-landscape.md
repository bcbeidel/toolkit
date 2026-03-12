---
name: "Eval Framework Landscape"
description: "Three categories of LLM evaluation tools — code-first (DeepEval), config-driven (promptfoo), and observability-integrated (Langfuse) — with selection criteria and Anthropic's methodology-first approach"
type: reference
sources:
  - https://github.com/confident-ai/deepeval
  - https://www.promptfoo.dev/docs/configuration/expected-outputs/
  - https://langfuse.com/blog/2025-10-21-testing-llm-applications
  - https://langfuse.com/blog/2025-11-12-evals
  - https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
  - https://www.traceloop.com/blog/automated-prompt-regression-testing-with-llm-as-a-judge-and-ci-cd
related:
  - docs/research/testing-non-deterministic-systems.md
  - docs/context/agent-testing-pyramid.md
  - docs/context/llm-as-judge-evaluation.md
  - docs/context/validation-architecture.md
---

Three categories of eval tooling have emerged for LLM systems, each optimized for different team workflows. The choice depends less on technical capability (they overlap significantly) and more on how a team wants to work.

## Code-First: DeepEval

Open-source Python framework that integrates with pytest via `deepeval test run`. Supports 50+ research-backed metrics including G-Eval, answer relevancy, faithfulness, and hallucination detection. Uses LLM-as-judge with configurable judge models (OpenAI, Anthropic, Ollama, local models).

**Best for:** Engineering teams who want evaluation as a code-level testing activity. Python-native teams who already use pytest. Teams that want fine-grained control over metric implementation.

**Integration pattern:** Write test files alongside application code, run via pytest in local development and CI. Evaluation metrics are Python objects configured in test fixtures.

## Config-Driven: promptfoo

Uses YAML configuration to define test cases with assertions. Supports deterministic assertions (equality, JSON schema, regex), model-graded assertions (LLM-as-judge with rubrics), and similarity-based assertions. Quality gates enforce minimum performance thresholds. The `validate` command exits with code 1 on failure, integrating cleanly with CI/CD pipelines.

**Best for:** Teams that prefer configuration over code. Node.js environments. Security and red-teaming use cases. Teams that want non-engineers to define test cases.

**Integration pattern:** YAML test suites checked into the repository, executed via CLI in CI/CD. Assertions are declarative -- no code needed for standard checks.

## Observability-Integrated: Langfuse

Open-source platform combining tracing, evaluation, and dataset management. Supports LLM-as-judge, user feedback, manual labeling, and custom evaluation pipelines. Every evaluation execution creates a trace for inspection. Datasets enable structured experiment runs.

**Best for:** Teams that want to connect evaluation with production observability. Organizations that need to debug production traces and convert them into test cases. Teams building evaluation workflows that span development and production.

**Integration pattern:** Instrument application with Langfuse tracing, collect production data, create datasets from real traffic, run evaluations against datasets, inspect results via the Langfuse dashboard.

## Regression-Focused: Traceloop

Built on OpenTelemetry for deep trace visibility. Enables automated prompt regression testing where new prompt versions run against test datasets, with LLM-as-judge scoring each output. CI/CD gates check for quality, performance, and cost regressions.

**Best for:** Teams already using OpenTelemetry. Prompt engineering workflows where regression detection is the primary concern.

## Methodology Over Framework: Anthropic's Approach

Rather than providing a framework, Anthropic describes a methodology: define tasks with clear inputs and success criteria, run multiple trials per task, apply graders (deterministic + LLM-based). Start with 20-50 simple tasks drawn from real failures.

The critical insight: grade outcomes, not paths. Agents may find creative solutions that static evals incorrectly fail. In tau-bench, Opus 4.5 discovered a loophole in an airline policy that "failed" the eval but actually produced a better solution for the user. Eval design must account for legitimate alternate paths.

## Selection Criteria

| Factor | DeepEval | promptfoo | Langfuse |
|--------|----------|-----------|----------|
| Language | Python | Node.js/YAML | Language-agnostic |
| Config style | Code | YAML | Dashboard + API |
| CI/CD | pytest | CLI exit codes | API-driven |
| Production link | No | No | Yes (tracing) |
| Open source | Yes | Yes | Yes |

The frameworks overlap more than they differ. Pick based on team workflow preferences, not feature comparison. A team can start with structural assertions in any framework and add LLM-as-judge metrics incrementally as quality requirements become clearer.

## Key Takeaway

Start with methodology (what to test, what "good" looks like), then pick a framework that fits the team's workflow. The framework matters less than having a systematic approach to evaluation -- 20 well-chosen test cases with clear success criteria outperform 200 poorly defined ones in any tool.
