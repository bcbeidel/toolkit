---
name: "Skill Chain Sequential and Recursive Design Rules"
description: "Start simple — single agents match multi-agent under equal compute; validate every boundary; use error fields not exceptions; design for idempotency; recursive patterns additionally require layered termination guardrails where only budget and timeout are hard guarantees."
type: context
sources:
  - https://www.anthropic.com/research/building-effective-agents
  - https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns
  - https://www.mindstudio.ai/blog/how-to-build-claude-code-skill-chain-business-workflow
  - https://arxiv.org/html/2604.02460v1
  - https://dextralabs.com/blog/recursive-language-models-rlm/
related:
  - docs/research/2026-04-10-skill-chaining-best-practices.research.md
  - docs/context/skill-chaining-definition-and-vocabulary.context.md
  - docs/context/skill-handoff-contracts-and-state-design.context.md
  - docs/context/skill-chain-failure-modes-and-antipatterns.context.md
---

# Skill Chain Sequential and Recursive Design Rules

**Start simple. A 2026 empirical study (arXiv 2604.02460) found that single agents consistently match or outperform multi-agent systems on multi-hop reasoning tasks under equal compute budgets.** Multi-agent chaining is not automatically better for complex tasks — MAS advantages in prior literature frequently stem from unaccounted computation differences, not architectural benefit. Multi-agent is justified when a single agent's effective context genuinely degrades (deletion, masking, distraction injection) or when tasks are truly parallelizable.

## Sequential Chain Rules (HIGH confidence)

**1. Follow the complexity ladder.** Direct model call → single agent with tools → multi-agent sequential chain. Add stages only when the simpler approach demonstrably fails. Anthropic: "Only increase complexity when it demonstrably improves outcomes."

**2. Validate at every boundary.** The orchestrator checks output quality before passing to the next skill. Malformed, low-confidence, or off-topic outputs must be retried or halted — not propagated. Validation is the highest-leverage intervention in sequential chain design.

**3. Use error fields, not exceptions.** Skills write failure state into their output so the orchestrator can decide whether to retry, skip, or escalate. Crashing with no recovery path is the wrong failure mode — it forces a full chain restart rather than targeted recovery.

**4. Design for idempotency.** Side-effectful skills should accept idempotency tokens and check already-completed steps before re-executing. This enables safe retries after partial failures. In wos plan files: "Always check completed_steps before re-executing."

## Recursive Pattern Rules (MODERATE confidence)

Recursive skill patterns — evaluator-optimizer loops, recursive decomposition, Tree of Thought — require explicit termination machinery. Recommended layered guardrails:

- **Semantic bound**: convergence criterion (quality threshold, no remaining subtasks, objective met)
- **Hard mechanical bounds**: token budget and wall-clock timeout are the only guaranteed terminators
- **Depth limit and call count**: useful signals but not reliable on their own — a loop can bypass soft limits if skill implementations do not propagate the orchestrator's depth counter correctly

**Only budget and timeout are hard guarantees.** Depth limits depend on correct propagation through every skill in the chain. Production incidents include recursive loops running for days because a single skill failed to forward the depth counter.

## The Validated Recursive Pattern

Anthropic's evaluator-optimizer is the most validated recursive pattern in production: one skill generates output, another evaluates it against criteria, and the loop continues until quality criteria are met. This works when: quality criteria are precise enough to drive convergence, and human feedback can demonstrably improve LLM responses.

For wos, the research → distillation pipeline can incorporate an evaluation step between research completion and distillation — verifying that findings meet quality standards before proceeding. This is preferable to unstructured recursion.

## Subagent Spawn Control

Claude has a documented tendency to spawn subagents in situations where direct action would suffice. The guidance: use subagents for parallel, isolated workstreams that do not need to share state; for sequential operations, shared-context tasks, or single-file edits, work directly rather than delegating.

**Bottom line:** Sequential chain correctness reduces to three rules — validate boundaries, fail explicitly, stay idempotent. Recursive patterns additionally require a semantic convergence criterion plus at least one hard mechanical termination bound. Single agents are the right default architecture; escalate to multi-agent only when context genuinely degrades.
