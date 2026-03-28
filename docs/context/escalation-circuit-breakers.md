---
name: "Escalation Strategies and Circuit Breakers for LLM Agents"
description: "Five-layer escalation model with budget-aware thresholds and a four-state circuit breaker pattern adapted for systems where failures look like successes"
metadata:
  type: reference
  sources:
    - https://www.sitepoint.com/error-handling-strategies-for-probabilistic-code-execution/
    - https://portkey.ai/blog/retries-fallbacks-and-circuit-breakers-in-llm-apps/
    - https://medium.com/@michael.hannecke/resilience-circuit-breakers-for-agentic-ai-cc7075101486
    - https://www.gocodeo.com/post/error-recovery-and-fallback-strategies-in-ai-agent-development
    - https://www.augmentcode.com/guides/why-multi-agent-llm-systems-fail-and-how-to-fix-them
  related:
    - docs/research/error-handling-agent-systems.md
    - docs/context/error-classification-agent-systems.md
    - docs/context/llm-error-handling-fundamentals.md
    - docs/context/human-in-the-loop-design.md
    - docs/context/workflow-orchestration.md
---

When an LLM agent fails, the response should be proportional to the failure type. A transient API error does not warrant human escalation. A structural specification gap does not benefit from retries. This document describes a five-layer escalation model and an adapted circuit breaker pattern for agent systems.

## Five-Layer Escalation

Each layer is attempted only after the previous layer is exhausted. Explicit thresholds prevent both premature escalation and runaway retry costs.

**Layer 1 -- Retry with backoff** (transient errors). Max 3 attempts with exponential backoff. Triggered by HTTP 503, timeouts, rate limits (429). Budget cap: retry cost must not exceed 3x the original attempt's token spend.

**Layer 2 -- Retry with context mutation** (correctable errors). Feed the error message, traceback, and previous output into a correction callback so the LLM generates a modified approach. Max 2 mutation attempts. Triggered by parsing failures, schema drift, validation errors. Bare retries without mutation are nearly as useless for LLMs as they are for deterministic code -- the mutation is what adds value.

**Layer 3 -- Fallback** (degraded capability). Switch to a simpler model, reduce tool access, or limit reasoning depth. Triggered by repeated mutation failures or model-specific errors. Must maintain minimum acceptable output quality -- degradation is controlled, not arbitrary.

**Layer 4 -- Peer escalation** (capability gap). Hand off to a specialized agent with different capabilities. Pass full context: task description, all attempts, failure history, and partial results. Triggered when the task requires capabilities the current agent lacks.

**Layer 5 -- Human escalation** (design-level blockers). Structured handoff with classification scores, attempt history, and suggested next steps. Triggered by confidence below threshold, high-risk operations, specification ambiguity, explicit user request, or budget exhaustion. Context-rich handoffs let the human start at the decision point, not from scratch.

When 79% of multi-agent failures stem from specification (41.8%) and coordination (36.9%) issues, most structural errors should escalate quickly to Layer 4 or 5 rather than burning budget on Layers 1-3.

## Four-State Circuit Breaker

Standard three-state circuit breakers (closed, open, half-open) are insufficient for LLM systems because the hardest failures -- hallucinations, confident wrong answers -- return HTTP 200 and don't register as errors. LLM circuit breakers need a fourth state and semantic failure detection.

**States:**
- **Closed**: Normal operation. Track both infrastructure errors (HTTP codes) and semantic errors (hallucination rate, quality degradation, cost anomalies).
- **Open**: No requests to the failing component. Return cached results or route to fallback.
- **Half-Open**: Limited probe requests. Probes require semantic evaluation -- a 200 response is not sufficient to confirm recovery.
- **Degraded**: Partial capability. Use a simpler model or reduced feature set. Allow requests with lower expectations and additional validation.

**Transition thresholds:**
- Closed to Open: N consecutive failures or error rate above threshold within a time window.
- Open to Half-Open: After cooldown, send limited probes.
- Half-Open to Closed: M consecutive successful probes with semantic validation.
- Half-Open to Open: Any probe failure.
- Any state to Degraded: Partial failures detected (quality below threshold but above minimum viable).

The semantic failure detection pipeline itself becomes a critical dependency that needs its own error handling -- a circuit breaker for the circuit breaker's evaluator.

## Budget Awareness

Every escalation layer costs tokens. A system with 3 retries, context mutation, and LLM-as-judge validation may spend 5-10x the tokens of a single attempt. Set explicit token budgets per task. When the budget is exhausted, escalate to human rather than continuing to spend.
