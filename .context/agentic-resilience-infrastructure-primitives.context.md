---
name: Agentic Resilience Infrastructure Primitives
description: "Retry with exponential backoff, circuit breakers with a DEGRADED intermediate state, idempotency keys, and checkpointing are the four deterministic infrastructure primitives that move reliability out of prompts and into the runtime."
type: concept
confidence: high
created: 2026-04-10
updated: 2026-04-10
sources:
  - https://medium.com/@michael.hannecke/resilience-circuit-breakers-for-agentic-ai-cc7075101486
  - https://hatchworks.com/blog/ai-agents/orchestrating-ai-agents/
  - https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
  - https://www.anthropic.com/research/building-effective-agents
  - https://getathenic.com/blog/ai-agent-retry-strategies-exponential-backoff
  - https://www.techempower.com/blog/2026/01/12/bulding-reliable-autonomous-agentic-ai/
  - https://arxiv.org/abs/2503.16416
related:
  - docs/context/agentic-fault-taxonomy-and-interface-mismatch-pattern.context.md
  - docs/context/multi-agent-shared-state-failure-mechanisms.context.md
  - docs/context/agentic-failure-recovery-classify-retry-replan-abandon.context.md
  - docs/context/agentic-planning-hybrid-global-plan-local-react.context.md
---
# Agentic Resilience Infrastructure Primitives

**"Move reliability into deterministic infrastructure (not prompt magic). Prompts don't roll back production systems; your runtime does."** Four primitives implement this principle: retry with backoff, circuit breakers, idempotency keys, and checkpointing.

## 1. Retry with Exponential Backoff and Jitter

Retryable errors: HTTP 429 (rate limit), 500/502–504 (server errors), 529 (model overload), timeouts.
Non-retryable errors: 400 (bad request), 401/403 (auth), context length exceeded.

Parameters: 1s initial delay, 2× multiplier, cap at 32–60s, ±30–50% jitter. Without jitter, synchronized retries from multiple agents create thundering herds. User-facing requests warrant 2–3 retries; background jobs 5–7.

This is validated distributed systems practice; the specific numbers are practitioner heuristics, not empirically derived.

## 2. Circuit Breakers with DEGRADED State

Traditional CLOSED/OPEN binary is insufficient for user-facing agents. Add a DEGRADED intermediate state:

| State | Behavior | Entry Trigger |
|-------|----------|---------------|
| CLOSED | Full capabilities; collect baseline metrics | Normal operation |
| DEGRADED | Disable high-risk tools (web access, code execution); switch to conservative models; add mandatory human review; mark outputs as low-confidence | Semantic failure threshold exceeded, cost anomalies |
| OPEN | Graceful fallback, escalation to human, partial processing with transparency | Health score <0.5 |
| HALF-OPEN | Graduated re-enablement at 5%/20%/50% traffic; success-based, not time-based | Recovery testing |

Health scoring uses composite metrics with exponential decay (recent failures weighted higher): ≥0.8 = CLOSED, 0.5–0.8 = DEGRADED, <0.5 = OPEN.

**Critical limitation**: circuit breakers trip on observable failure signals (API errors, timeouts, schema violations). Semantic failures — hallucinations, goal drift, confident wrong answers — produce no infrastructure-level error. The circuit remains CLOSED while the agent reasons incorrectly. Validation overhead to detect semantic failures can exceed 200% of base execution cost.

## 3. Idempotency Keys

Persist a run-level idempotency key across the agent, tool layer, and messaging bus. Every external write operation must check this key before executing — repeated calls with the same key produce identical outcomes without duplicating actions.

**Important scope limitation**: idempotency keys prevent duplicate infrastructure calls on retry. They do not prevent an agent from deciding to repeat an action for cognitive reasons within a single run. Idempotency is an infrastructure primitive, not a behavioral constraint on the model.

## 4. Checkpointing with State Separation

Separate three state domains:
- **Task state**: workflow checkpoints and artifacts — durable, replayable, survives restarts
- **Session context**: short-lived conversation window
- **System state**: authoritative policies and permissions

Anthropic's production harness uses git commits + progress files: agents commit progress with descriptive messages; session initialization reads progress files to resume from last known good state. LangGraph implements checkpoint-interrupt with `RetryPolicy(max_attempts=3, initial_interval=1.0)`, requiring a checkpointer for state persistence across execution boundaries.

Dead-letter queues handle steps that exhaust retries — they capture irretrievable failures with a clear remediation path and audit trail.

## The Two-Phase Action Pattern

For irreversible operations: Plan → Validate → Execute. The plan is a structured, signed artifact stored before execution, creating proof of what was approved versus what actually ran. Validation happens between proposal and execution — not after.

## Takeaway

Implement all four primitives as infrastructure, not as prompt instructions. Do not rely on model self-awareness to catch retryable errors, manage retry counts, or ensure idempotency. The runtime is the last line of defense for these properties.
