---
name: "Skill Handoff Contracts and State Design"
description: "Clean skill handoffs require three components: output contracts, shared state, and an orchestrator; structured JSON beats plain text; typed schemas are necessary but not sufficient — behavioral drift occurs even with schemas."
type: concept
confidence: high
created: 2026-04-10
updated: 2026-04-10
sources:
  - https://www.anthropic.com/research/building-effective-agents
  - https://openai.github.io/openai-agents-python/multi_agent/
  - https://learn.microsoft.com/en-us/semantic-kernel/frameworks/agent/agent-orchestration/
  - https://www.mindstudio.ai/blog/claude-code-skill-collaboration-chaining-workflows
  - https://www.mindstudio.ai/blog/how-to-build-claude-code-skill-chain-business-workflow
  - https://github.blog/ai-and-ml/generative-ai/multi-agent-workflows-often-fail-heres-how-to-engineer-ones-that-dont/
  - https://arxiv.org/html/2602.22302
related:
  - docs/research/2026-04-10-skill-chaining-best-practices.research.md
  - docs/context/skill-chaining-definition-and-vocabulary.context.md
  - docs/context/skill-chain-sequential-and-recursive-design-rules.context.md
  - docs/context/skill-chain-failure-modes-and-antipatterns.context.md
---
# Skill Handoff Contracts and State Design

**Three components are necessary for clean skill handoffs: output contracts, shared state, and an orchestrator (HIGH confidence, T1 sources converge).** Without all three, chains become fragile — skills cannot consume each other's outputs reliably, state diverges across invocations, and the orchestrator cannot route or validate correctly.

## The Three Required Components

**Output contracts** — each skill declares what structured fields it produces and what it requires as input. Downstream skills read only declared required fields, which prevents breakage from minor changes. Define output contracts before implementing the skill itself; the contract is more important than the internal logic.

**Shared state** — a single source of truth persists across skill invocations. Multiple files for different stages is an antipattern. State should log each transition with timestamp and skill name. When a skill encounters a failure, it writes an error field into state rather than raising an exception — this lets the orchestrator decide whether to retry, skip, or escalate.

**Orchestrator** — reads state, identifies the current stage, invokes the appropriate skill, validates the output, and advances to the next step. Validation at every boundary is not optional: malformed, low-confidence, or off-topic outputs must be retried or halted, not propagated downstream.

## Structured JSON Over Plain Text

Plain text outputs are fragile. Every major framework (Anthropic, OpenAI, Microsoft Semantic Kernel, LlamaIndex) provides typed schema mechanisms for inter-skill communication. The GitHub Engineering guidance states: "typed schemas are table stakes — without them, nothing else works."

Practical rules:
- Define required output fields; allow additional fields freely.
- Compact returns: pass only what the next step needs, not a full transcript of the skill's internal state. Store verbose outputs separately; pass minimal references.
- Anthropic recommends XML tags to structure handoff content between prompts, with a single clear objective per subtask.

## Schemas Are Necessary But Not Sufficient

Important caveat: behavioral drift — progressive divergence of agent output from intended specifications — occurs in deployed multi-agent systems even when typed schemas are in place (Agent Behavioral Contracts, arXiv 2602.22302, 2026). Schemas prevent structural malformation; they cannot prevent semantic drift over extended interaction sequences.

The implication for wos: output contracts define the shape of a handoff; they do not guarantee that the content will remain behaviorally consistent across a long-running chain spanning multiple sessions. Behavioral drift is a separate and currently unsolved failure mode.

## Error Handling at Boundaries

Error fields, not exceptions, are the standard at skill boundaries. When a skill fails:
1. Write an error field with a plain-language description into the state object.
2. The orchestrator reads the error and decides: retry, skip, or escalate.
3. Never crash with no recovery path — the orchestrator must be able to reason about failures.

This design keeps chain failure recoverable rather than catastrophic.

**Bottom line:** The handoff contract between skills is more important than any individual skill's internal quality. Define what every skill produces and what it requires before writing a single line of skill logic. Use structured JSON, a single state source of truth, and error fields at every boundary.
