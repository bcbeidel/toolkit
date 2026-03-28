---
name: "Agent Testing Pyramid"
description: "Three-layer testing model for agent systems — deterministic unit tests, LLM-as-judge evaluation, and end-to-end scenarios — with CI integration philosophy and property-based testing for invariant verification"
metadata:
  type: reference
  sources:
    - https://engineering.block.xyz/blog/testing-pyramid-for-ai-agents
    - https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
    - https://www.anthropic.com/research/building-effective-agents
    - https://datagrid.com/blog/4-frameworks-test-non-deterministic-ai-agents
    - https://rchaves.app/the-agent-testing-pyramid/
    - https://dev.to/aws/beyond-traditional-testing-addressing-the-challenges-of-non-deterministic-software-583a
  related:
    - docs/research/testing-non-deterministic-systems.md
    - docs/context/llm-as-judge-evaluation.md
    - docs/context/eval-framework-landscape.md
    - docs/context/validation-architecture.md
    - docs/context/tool-design-for-llms.md
---

Testing agent systems requires abandoning exact-match expectations. The industry has converged on an adapted testing pyramid that separates deterministic from non-deterministic concerns at architectural boundaries. Maximum investment goes to the deterministic base where traditional testing works; costlier evaluation methods apply only where they must.

## The Three Layers

**Base: Deterministic Unit Tests.** Tool call routing, argument parsing, response formatting, state machine transitions, retry logic, and schema validation are all testable with standard unit tests. Use mock providers that return canned responses instead of calling real models. These tests run in CI on every commit -- they are fast, cheap, and completely deterministic. If they flake, the problem is in the software, not the AI. This layer answers: "Did we write correct software?"

**Middle: LLM Quality Evaluation.** Behavioral assertions via LLM-as-judge, structural checks (JSON schema, regex), and soft scoring on a continuous 0-1 scale. These tests call an external judge model, making them slower and more expensive. They catch quality regressions that deterministic tests cannot detect. Run pre-release, not in CI.

**Top: End-to-End Scenarios.** Multi-turn conversation simulations and complex tool-use sequences that validate the full pipeline. Fewest in number but test what matters most: can the agent solve real problems? Run on-demand or on a schedule.

## Separating the Layers

Clean separation relies on treating the LLM as a swappable component behind a defined interface. Block Engineering's TestProvider pattern operates in two modes: recording mode captures real LLM request/response pairs into JSON files keyed by input hash; replay mode serves those recordings deterministically. This converts the non-deterministic boundary into a deterministic one for regression testing.

Hexagonal architecture (ports and adapters) supports this separation formally. Defining an IntelligencePort isolates prompts and orchestration logic from the specific provider, enabling mock implementations for testing and provider swapping without touching business logic.

**The limitation:** Agent behavior emerges from the interaction between deterministic logic and LLM reasoning. Mocking the LLM removes the emergent behavior that causes production failures. Record-and-replay captures one execution trace but misses the variance that makes testing necessary. Accept this tradeoff -- the base layer catches software bugs, the upper layers catch behavior regressions.

## Property-Based and Structural Testing

Before reaching for expensive LLM-as-judge evaluation, exhaust cheap deterministic assertions. Property-based testing verifies invariants that must hold regardless of specific output: outputs parse as valid JSON/YAML, tool calls reference defined tools, response length falls within bounds, no sensitive data leakage, and idempotent operations produce consistent side effects. Structural assertions check output shape independently of content -- JSON schema validation, required field presence, and format compliance are all deterministic.

Most teams jump straight to LLM-as-judge for everything. Starting with structural and property-based assertions catches the cheapest failures first and reserves expensive evaluation for genuinely semantic questions.

## CI Philosophy

CI validates the deterministic base layer only. Live LLM tests are too expensive, too slow, and too flaky for CI pipelines. The middle and top layers run on-demand, pre-release, or on a schedule. This means the build can break on tool routing errors or schema violations but not on subjective quality judgments -- which is the right tradeoff for development velocity.

## Key Takeaway

The pyramid maps to real architectural boundaries: software correctness at the base, output quality in the middle, system behavior at the top. Teams that invest disproportionately in the base layer get the best return -- most agent failures trace to deterministic bugs (wrong tool selected, malformed arguments, missing error handling), not to LLM reasoning failures.
