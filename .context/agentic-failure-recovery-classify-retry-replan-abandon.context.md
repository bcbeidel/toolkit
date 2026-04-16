---
name: "Agentic Failure Recovery — Classify, Retry, Replan, Abandon"
description: "Effective agentic failure recovery follows a three-tier escalation (retry transient errors, replan on state divergence, abandon on permanent failures), with error classification at the tool boundary determining which tier to enter."
type: concept
confidence: high
created: 2026-04-10
updated: 2026-04-10
sources:
  - https://www.anthropic.com/research/building-effective-agents
  - https://www.gocodeo.com/post/error-recovery-and-fallback-strategies-in-ai-agent-development
  - https://sparkco.ai/blog/mastering-retry-logic-agents-a-deep-dive-into-2025-best-practices
  - https://arxiv.org/abs/2603.06847
  - https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
related:
  - docs/context/agentic-planning-hybrid-global-plan-local-react.context.md
  - docs/context/agentic-resilience-infrastructure-primitives.context.md
  - docs/context/agentic-fault-taxonomy-and-interface-mismatch-pattern.context.md
---
# Agentic Failure Recovery — Classify, Retry, Replan, Abandon

**Classify the failure before choosing a response.** The recovery tier — retry, replan, or abandon — is determined by error type, not by how many attempts have been made. LLM-based error classification is unreliable for semantic errors; wherever possible, classify at the tool boundary using structural signals.

## Error Classification

Five categories at the tool boundary:

1. **Execution errors** — tool invocation failures: API errors, network failures, CLI crashes
2. **Semantic errors** — syntactically valid but functionally wrong LLM output: hallucinated parameters, misinterpreted intent
3. **State errors** — agent's assumptions diverge from actual environment state
4. **Timeout/latency failures** — unresponsive processes, exceeded time budgets
5. **Dependency errors** — external service failures: rate limits, schema changes, downstream outages

## The Three-Tier Decision Rule

**Retry** (transient, retriable):
- HTTP 429, 500, 502–504, 529, timeouts
- Apply exponential backoff with jitter; cap at ~5 attempts
- Only safe if the operation is idempotent — dangerous on state-mutating calls without idempotency keys
- Risk: LLMs often misclassify semantic errors as transient, triggering retries that reproduce the same wrong behavior

**Replan** (state divergence or budget exhaustion):
- Triggered when: (a) state verification reveals divergence between expected and actual state, (b) semantic validation of outputs fails, or (c) retry budget is exhausted on a non-terminal task
- Replan from the last successful checkpoint, not from the beginning — this is the architectural distinction between agents that tolerate failure gracefully and those that require full restarts
- Replanning introduces latency and context cost; only trigger on confirmed divergence

**Abandon** (permanent failures):
- HTTP 400, 401, 403, context length exceeded, unrecoverable state corruption, explicit tool contract violations
- Log the failure with structured context: what was attempted, how far it got, what was learned, and what the handoff needs
- Escalate to human or fallback workflow — do not retry or replan

## Checkpointing is Architecturally Required

Multi-step plans must save execution snapshots at subtask boundaries. Recovery replays only from the last successful checkpoint. Without checkpointing, any failure forces a full restart — which may reproduce the root cause when the agent re-executes the same steps from the same initial context.

Anthropic's harness uses git commits + progress files: agents commit progress with descriptive messages; session initialization reads progress files to resume from last known good state.

## Stopping Conditions as Infrastructure

Stopping conditions must be implemented as infrastructure code, not prompt instructions:
- Hard caps on iterations, tool calls, spend, wall-clock time
- "No progress" detectors: repeated identical tool calls, restated plans, recurring error class
- On trigger: halt with a structured summary of attempts, learnings, and explicit human handoff needs

Anthropic: agents should "pause for human feedback at checkpoints or when encountering blockers." The emphasis is on not propagating failure silently. Do not design agents that continue after detecting inconsistency.

## Design Principle

**"Treat fallback as first-class logic — design recovery paths early, not as auxiliary features."**

Recovery path design questions to answer at architecture time:
- What happens when tool X returns an unexpected schema?
- What is the maximum retry count before replanning?
- What constitutes a "no progress" condition for this workflow?
- Where is the last valid checkpoint from which replanning can begin?

## Main Risk: Semantic Error Misclassification

The failure recovery pattern's principal weakness: LLM-based error triage can misclassify semantic errors (wrong output that looks correct structurally) as transient errors, causing retry storms that reproduce the same bad reasoning. Mitigation: schema validation at every tool boundary before entering retry logic; flag semantic validation failures as replan triggers, not retry triggers.

## Takeaway

Classify before recovering. Build stopping conditions in infrastructure. Checkpoint at subtask boundaries. The retry/replan/abandon tiers are a sound structure — but the decision boundaries are heuristics, not empirically validated thresholds. LLM self-assessment of errors is not reliable for semantic failures; use structural signals wherever possible.
