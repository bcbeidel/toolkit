---
name: "Error Handling in Agent Systems"
description: "How LLM-based agents should handle failures: taxonomy of retryable vs. design-level errors, escalation thresholds, circuit breaker patterns, graceful degradation, and structured failure reporting"
type: research
sources:
  - https://www.sitepoint.com/error-handling-strategies-for-probabilistic-code-execution/
  - https://medium.com/@michael.hannecke/resilience-circuit-breakers-for-agentic-ai-cc7075101486
  - https://portkey.ai/blog/retries-fallbacks-and-circuit-breakers-in-llm-apps/
  - https://arxiv.org/abs/2508.07935
  - https://arxiv.org/abs/2503.13657
  - https://www.gocodeo.com/post/error-recovery-and-fallback-strategies-in-ai-agent-development
  - https://galileo.ai/blog/agent-failure-modes-guide
  - https://stackoverflow.blog/2025/06/30/reliability-for-unreliable-llms/
  - https://www.augmentcode.com/guides/why-multi-agent-llm-systems-fail-and-how-to-fix-them
  - https://neuraltrust.ai/blog/circuit-breakers
  - https://markaicode.com/implement-graceful-degradation-llm-frameworks/
related:
  - docs/research/multi-agent-coordination.md
  - docs/research/validation-architecture.md
  - docs/research/workflow-orchestration.md
  - docs/research/human-in-the-loop-design.md
  - docs/research/llm-capabilities-limitations.md
  - docs/context/error-classification-agent-systems.md
  - docs/context/escalation-circuit-breakers.md
  - docs/context/llm-error-handling-fundamentals.md
---

Error handling in LLM-agent systems differs fundamentally from traditional software. The failing component is non-deterministic, failures often look like successes (a hallucinated answer returns HTTP 200), and the same input can produce different failure modes across runs. This document investigates failure taxonomies, escalation strategies, circuit breaker patterns, and structured reporting for agent systems where the "code" is an LLM.

## Sources

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|-----------|------|------|--------|
| 1 | https://www.sitepoint.com/error-handling-strategies-for-probabilistic-code-execution/ | Reliable AI: Error Handling for Non-Deterministic Agents | SitePoint | 2026-03 | T3 | verified |
| 2 | https://medium.com/@michael.hannecke/resilience-circuit-breakers-for-agentic-ai-cc7075101486 | Resilience Circuit Breakers for Agentic AI | Michael Hannecke / Medium | 2025 | T4 | verified |
| 3 | https://portkey.ai/blog/retries-fallbacks-and-circuit-breakers-in-llm-apps/ | Retries, Fallbacks, and Circuit Breakers in LLM Apps | Portkey | 2025 | T3 | verified |
| 4 | https://arxiv.org/abs/2508.07935 | SHIELDA: Structured Handling of Exceptions in LLM-Driven Agentic Workflows | Zhou, Chen et al. | 2025-08 | T1 | verified |
| 5 | https://arxiv.org/abs/2503.13657 | Why Do Multi-Agent LLM Systems Fail? | Cemri, Pan, Yang et al. (UC Berkeley) | 2025-03 | T1 | verified |
| 6 | https://www.gocodeo.com/post/error-recovery-and-fallback-strategies-in-ai-agent-development | Error Recovery and Fallback Strategies in AI Agent Development | GoCodeo | 2025 | T4 | verified |
| 7 | https://galileo.ai/blog/agent-failure-modes-guide | 7 AI Agent Failure Modes and How To Fix Them | Galileo AI | 2025 | T3 | verified |
| 8 | https://stackoverflow.blog/2025/06/30/reliability-for-unreliable-llms/ | Reliability for Unreliable LLMs | Stack Overflow Blog | 2025-06 | T2 | verified |
| 9 | https://www.augmentcode.com/guides/why-multi-agent-llm-systems-fail-and-how-to-fix-them | Why Multi-Agent LLM Systems Fail (and How to Fix Them) | Augment Code | 2025 | T3 | verified |
| 10 | https://neuraltrust.ai/blog/circuit-breakers | Using Circuit Breakers to Secure the Next Generation of AI Agents | NeuralTrust | 2025 | T3 | verified |
| 11 | https://markaicode.com/implement-graceful-degradation-llm-frameworks/ | How to Implement Graceful Degradation in LLM Frameworks | MarkAICode | 2025 | T4 | verified |

## Research Protocol

| # | Query | Engine | Results | Useful |
|---|-------|--------|---------|--------|
| 1 | "LLM agent error handling failure taxonomy retryable errors vs blockers 2025 2026" | WebSearch | 10 | 5 |
| 2 | "circuit breaker pattern LLM agent systems graceful degradation" | WebSearch | 10 | 5 |
| 3 | "agent escalation thresholds when to retry vs escalate to human LLM" | WebSearch | 10 | 3 |
| 4 | "structured failure reporting AI agent systems error classification" | WebSearch | 10 | 5 |
| 5 | "error handling differs LLM non-deterministic vs traditional software deterministic code 2025" | WebSearch | 10 | 3 |
| 6 | "SHIELDA structured handling exceptions LLM agentic workflows arxiv 2508" | WebSearch | 10 | 4 |
| 7 | "sitepoint error handling strategies for probabilistic code LLM agent observe classify mutate bound" | WebSearch | 10 | 3 |
| 8 | "portkey retries fallbacks circuit breakers LLM apps what to use when" | WebSearch | 10 | 3 |
| 9 | "arxiv 2503.13657 multi-agent LLM systems fail MAST taxonomy failure modes" | WebSearch | 10 | 4 |
| 10 | "gocodeo error recovery fallback strategies AI agent retry escalation graceful degradation" | WebSearch | 10 | 3 |
| 11 | "stackoverflow blog reliability for unreliable LLMs control loops validation 2025" | WebSearch | 10 | 2 |
| 12 | "galileo 7 AI agent failure modes classification taxonomy planning execution" | WebSearch | 10 | 3 |
| 13 | "augment code multi-agent LLM systems fail fix retry design error" | WebSearch | 10 | 3 |
| 14 | "neuraltrust circuit breakers secure next generation AI agents safety guardrails" | WebSearch | 10 | 2 |

## Extracts by Sub-Question

### SQ1: What failure taxonomy works for LLM-based agent systems?

**SHIELDA taxonomy [4]:** 36 exception types across 12 agent artifacts (Goal, Memory, Reasoning, Planning, Tool, Interface, Task Flow, External System, etc.). Framework uses an exception classifier to select handling patterns from a registry. Phase-aware recovery links execution errors to reasoning-phase root causes.

**MAST taxonomy [5]:** 14 unique failure modes in 3 categories: (i) system design issues, (ii) inter-agent misalignment, (iii) task verification. Developed from 150 annotated traces across 7 multi-agent frameworks. High inter-annotator agreement (kappa = 0.88). Mapped to execution stages: Pre-Execution, Execution, Post-Execution.

**Galileo failure modes [7]:** 7 failure modes structured around Memory -> Reflection -> Planning -> Action flow. Corrupted memory in early steps cascades into subsequent reflections, plans, and actions. Categories include specification/requirement failures and execution/verification failures.

**SitePoint error taxonomy [1]:** Classifies errors as retryable or terminal. A KeyError from schema drift is retryable; an authentication failure is not. 401 errors never retry; 503 errors always retry. Pattern: "observe, classify, mutate, bound."

**Key distinction — retryable vs. design-level:**
- Retryable: transient API errors (503, timeout), rate limits (429), parsing failures from non-deterministic output, tool execution errors from recoverable state
- Design-level blockers: authentication failures (401), missing capabilities, specification ambiguity, inter-agent protocol mismatches, fundamental task impossibility

### SQ2: How should escalation thresholds be defined?

**Augment Code [9]:** Multi-agent LLM systems fail at 41-86.7% rates. Nearly 79% of problems originate from specification and coordination issues, not technical implementation. Absence of retry limiters leads to runaway costs. Solution: explicit thresholds and retry limits.

**GoCodeo [6]:** Retry with capped exponential backoff (e.g., `@retry(wait=wait_exponential(), stop=stop_after_attempt(3))`). On validation failure, route to sanitation agent or retry generation. Escalate to human reviewer when confidence is low or failure persists, especially for code modification, infrastructure changes, or cost-heavy operations.

**Escalation decision framework:**
1. **Retry** (same strategy): Transient errors, rate limits, parsing failures. Cap at 3 attempts with exponential backoff.
2. **Retry with mutation** (modified strategy): Context-aware correction — feed error, traceback, and previous output into correction callback for LLM to self-correct [1].
3. **Fallback** (alternative strategy): Route to simpler model, disable tool access, return cached responses, reduce reasoning depth [2].
4. **Escalate to peer agent**: Hand off to specialized agent with different capabilities.
5. **Escalate to human**: Confidence below threshold, repeated failures, high-risk operations, explicit user request.
6. **Fail with report**: Unrecoverable error — structured failure report with full context.

**Confidence-based thresholds:** When agent confidence drops below threshold for intent classification, entity recognition, knowledge retrieval, or response generation, escalate immediately. Set minimum thresholds that prompt handoff when data is insufficient for reliable decisions.

### SQ3: What structured failure reporting formats exist?

**SHIELDA [4]:** Five core components — exception classifier, handler pattern registry, structured executor, escalation controller, and AgentOps infrastructure. Exception classifier monitors execution, identifies type from taxonomy, determines phase, isolates relevant artifacts.

**SitePoint [1]:** Every agent execution instrumented with OpenTelemetry spans. Errors classified dynamically rather than static exception hierarchies. Structured error reports include: error type, traceback, previous output, correction callback result, retry count, token spend.

**MAST [5]:** Step-level granularity error identification. Traces mapped to execution stages with root cause analysis. LLM-as-a-Judge pipeline for scalable annotation.

**Practical reporting structure:**
- Error classification (taxonomy category)
- Execution phase (pre-execution, execution, post-execution)
- Affected artifacts (memory, plan, tool, output)
- Retry history (attempts, mutations applied, outcomes)
- Cost accounting (tokens spent, API calls made)
- Escalation path taken
- Resolution or terminal failure reason

### SQ4: How do circuit breaker patterns apply to LLM agent workflows?

**Portkey [3]:** Three-layer defense: retries (transient), fallbacks (provider degradation), circuit breakers (systemic failure). Circuit breaker trips when failure thresholds crossed — failing provider removed from routing pool, no requests sent during cooldown period. Prevents cascading failures from piling traffic onto degraded service.

**Hannecke [2]:** Classic circuit breaker assumes you know when something fails. With LLM reasoning systems, biggest failures look like successes (hallucination returns 200). Agents need a DEGRADED state for partial capability, graduated re-enablement with multiple probe samples, and detection for semantic failures. Five failure categories including semantic failures.

**Standard states extended for LLM:**
- **Closed**: Normal operation, tracking failures
- **Open**: Failing fast, no requests to failing component
- **Half-Open**: Limited test requests to check recovery
- **Degraded** (LLM-specific): Partial capability — using simpler model, reduced tool access, limited reasoning depth

**NeuralTrust [10]:** Circuit breakers as safety mechanism interrupting LLM when forming harmful representations. Representation Rerouting (RR) technique — penalizes harmful internal representations during training. Less than 1% capability degradation on benchmarks. This is a safety/security application rather than reliability, but the pattern applies.

### SQ5: How does graceful degradation work when the failing component is an LLM?

**GoCodeo [6]:** Design agent stack as chain-of-responsibility with decreasing complexity. Fallback routing from failing agent to simpler or more deterministic agent. Instrument with structured logs, metrics, and error traces.

**Hannecke [2]:** Graceful degradation strategies: fall back to simpler model, disable tool access for pure LLM response, return cached/templated responses, limit reasoning depth. Or route elsewhere: human operator handoff, alternative agent, queue for later processing.

**MarkAICode [11]:** Implement graceful degradation with exponential retry logic. Trigger simpler fallback paths on crashes and timeouts.

**Degradation ladder:**
1. Full capability (primary model + all tools + full reasoning)
2. Reduced reasoning (simpler model, full tools)
3. Reduced tools (primary model, limited tool access)
4. Cached/templated responses (no LLM, deterministic fallback)
5. Human handoff (structured context transfer)
6. Graceful failure (structured error report, no output attempted)

### SQ6: How does error handling differ for LLM vs. traditional software?

**Stack Overflow [8]:** LLMs are non-deterministic by design — same prompt, same settings, different hardware state produces different tokens. Even temperature=0 is not deterministic due to floating-point GPU operations. At no point did the LLM become deterministic; what changed is the system gained control loops. Reducing uncertainty through redundancy and validation, not converting probability into certainty.

**Key differences:**

| Aspect | Traditional Software | LLM Agent Systems |
|--------|--------------------|--------------------|
| Failure detection | Exceptions, error codes | Semantic evaluation required — failures may look like successes |
| Determinism | Same input = same output | Same input = different outputs across runs |
| Retry value | Limited (same bug = same error) | High (non-determinism means retry may succeed) |
| Error cascading | Linear, traceable | Compounding — .95^4 classifiers = .814 pipeline accuracy |
| Cost of failure | Compute time | Token spend (monetary cost per attempt) |
| Failure taxonomy | Static exception hierarchies | Dynamic classification against evolving taxonomy |
| Recovery strategy | Fix code, redeploy | Mutate context, adjust prompt, change model |
| Validation | Unit tests, type checking | LLM-as-judge, output schema validation, semantic checks |

**Compounding errors [8]:** A dialog system with 4 classifiers at 95% stability shows .95^4 = .814 expected performance. Reasoning models compound errors when earlier mistakes feed into later steps.

**Control loop architecture [8]:** Reliable GenAI = pipeline with generation step (candidate answer) + evaluation step (assess answer) + routing layer (accept/reject/retry). Systems combine deterministic testing (agent state, API bindings, tools) with stochastic behavior testing (plan generation, output quality).

## Challenge

**Counter-evidence and tensions:**

1. **Retry may not help for LLM errors.** While non-determinism makes retries more valuable than in deterministic systems, retrying the same prompt often produces the same class of error. Context mutation between retries (feeding error info back) is what makes retries effective — bare retries are nearly as useless as in traditional code [1][8].

2. **Taxonomy completeness is uncertain.** SHIELDA's 36 types and MAST's 14 modes were developed on specific benchmarks and frameworks. Production systems may encounter failure modes outside these taxonomies. The field is young — no taxonomy has been validated across diverse real-world deployments at scale.

3. **Circuit breakers assume measurable failure.** The classic pattern trips on error rates. For LLM systems, the hardest failures — hallucinations, subtle reasoning errors, confident wrong answers — don't register as errors at the infrastructure level [2]. Semantic failure detection requires its own evaluation pipeline, which itself may fail.

4. **Escalation to humans may not scale.** In high-throughput agent systems, human escalation creates a bottleneck. If 41-86.7% of multi-agent runs fail [9], escalating all failures overwhelms human reviewers. The escalation threshold must be tuned to balance reliability against throughput.

5. **Cost of reliability is significant.** Each retry, fallback evaluation, and circuit breaker probe costs tokens and API calls. A system that retries 3 times with context mutation and runs LLM-as-judge validation may spend 5-10x the tokens of a single attempt. The reliability architecture must account for budget constraints [8][9].

## Findings

### How should agents classify failures?

A two-axis taxonomy works best for practical agent systems: **retryability** (can this succeed on retry?) crossed with **origin phase** (where did the failure originate?) (HIGH — T1 + T3 sources converge [4][5][7]).

**Retryability axis:**
- **Transient**: Will likely succeed on immediate retry (rate limits, timeouts, transient API errors)
- **Correctable**: Will succeed with modified approach (parsing errors, schema mismatches, context insufficiency)
- **Structural**: Cannot succeed without design changes (missing capabilities, protocol mismatches, specification gaps)

**Origin phase axis (from SHIELDA [4]):**
- **Reasoning**: Goal misinterpretation, flawed planning, incorrect decomposition
- **Execution**: Tool failures, API errors, state corruption
- **Verification**: Incorrect self-assessment, premature termination, infinite loops

The critical insight: execution-phase errors often have reasoning-phase root causes [4]. An agent that repeatedly fails at a tool call may have a flawed plan, not a tool problem. Tracing errors back to their originating phase prevents wasted retries on symptoms.

**Confidence: HIGH** — converging evidence from SHIELDA (T1), MAST (T1), Galileo (T3), and SitePoint (T3).

### How should escalation thresholds work?

Escalation should follow a layered strategy with explicit thresholds at each level (HIGH — multiple sources converge [1][3][6][9]).

**Layer 1 — Retry with backoff** (transient errors):
- Max 3 attempts with exponential backoff
- Triggered by: HTTP 503, timeouts, rate limits (429)
- Budget cap: token cost of retries must not exceed 3x original attempt

**Layer 2 — Retry with context mutation** (correctable errors):
- Feed error message, traceback, and previous output into correction callback
- LLM generates corrected approach based on failure information
- Max 2 mutation attempts before escalating
- Triggered by: parsing failures, schema drift, validation errors

**Layer 3 — Fallback** (degraded capability):
- Switch to simpler model, reduce tool access, limit reasoning depth
- Triggered by: repeated mutation failures, model-specific errors
- Must maintain minimum acceptable output quality

**Layer 4 — Peer escalation** (capability gap):
- Hand off to specialized agent with appropriate capabilities
- Pass full context: task, attempts, failure history, partial results
- Triggered by: task requires capabilities current agent lacks

**Layer 5 — Human escalation** (design-level blockers):
- Structured handoff with classification scores, attempt history, suggested next steps
- Triggered by: confidence below threshold, high-risk operations, specification ambiguity, explicit user request, budget exhaustion
- Context-rich: "start at line ten, not line one"

**Confidence: HIGH** — consistent across SitePoint (T3), Portkey (T3), GoCodeo (T4), Augment (T3).

### How should circuit breakers adapt for LLM systems?

Standard three-state circuit breakers are insufficient. LLM systems need a four-state model with semantic failure detection (MODERATE — T3 + T4 sources, limited empirical validation [2][3]).

**Extended states:**
- **Closed**: Normal operation. Track both infrastructure errors (HTTP codes) and semantic errors (evaluation failures, hallucination detection).
- **Open**: No requests to failing component. Return cached results or route to fallback.
- **Half-Open**: Send probe requests. For LLM, probes need semantic evaluation — a 200 response is not sufficient to confirm recovery.
- **Degraded**: Partial capability. Use simpler model or reduced feature set. Allow requests but with lower expectations and additional validation.

**Key adaptation: semantic failure detection.** Traditional circuit breakers trip on error codes. LLM circuit breakers must also trip on:
- Hallucination rate exceeding threshold (requires evaluation pipeline)
- Response quality degradation (detected by LLM-as-judge or schema validation)
- Latency spikes indicating model degradation
- Cost anomalies (token consumption significantly above baseline)

**Transition thresholds (from Portkey [3]):**
- Closed -> Open: N consecutive failures or error rate > threshold within time window
- Open -> Half-Open: After cooldown period, send limited probe requests
- Half-Open -> Closed: M consecutive successful probes (with semantic validation)
- Half-Open -> Open: Any probe failure returns to open state
- Any -> Degraded: Partial failures detected (semantic quality below threshold but above minimum)

**Confidence: MODERATE** — the four-state model is proposed by practitioner sources (T3/T4) but lacks rigorous empirical validation. Semantic failure detection is the key challenge and remains an active research area.

### How should failures be reported?

Structured failure reports should capture the full error lifecycle, not just the terminal state (HIGH — T1 + T3 sources converge [1][4][5]).

**Minimum report fields:**
```
error_type: <taxonomy classification>
origin_phase: reasoning | execution | verification
retryability: transient | correctable | structural
affected_artifacts: [memory, plan, tool_call, output]
attempt_history:
  - attempt: 1
    strategy: direct
    outcome: <error details>
    tokens_spent: N
  - attempt: 2
    strategy: context_mutation
    mutation: <what changed>
    outcome: <error details>
    tokens_spent: N
escalation_path: retry -> mutate -> fallback -> human
resolution: <resolved | escalated | failed>
total_cost: <tokens, API calls, wall time>
```

**Observability requirements:**
- Every agent execution instrumented with spans (OpenTelemetry or equivalent) [1]
- Errors classified dynamically against taxonomy, not static exception types
- Retry history preserved — each attempt's input, output, and mutation recorded
- Cost accounting at every level — token spend per attempt, total pipeline cost

**Confidence: HIGH** — SHIELDA (T1) and SitePoint (T3) provide convergent structured approaches. MAST (T1) validates step-level granularity.

### How does error handling differ when the "code" is an LLM?

The fundamental difference: LLM failures are probabilistic, partially observable, and costly (HIGH — T1 + T2 sources converge [5][8]).

**Five key differences that change error handling design:**

1. **Failures look like successes.** A hallucinated answer returns HTTP 200. Error detection requires semantic evaluation, not just status codes. Every output needs validation — either deterministic (schema, type checks) or probabilistic (LLM-as-judge) [2][8].

2. **Retries have value but need mutation.** Unlike deterministic code where the same bug produces the same error, LLM non-determinism means a retry might succeed. But bare retries are insufficient — context mutation (feeding error info back into the prompt) is what makes retries effective [1][8].

3. **Errors compound multiplicatively.** Four classifiers at 95% reliability produce 81.4% pipeline reliability (.95^4). Each additional LLM step in an agent pipeline multiplies failure probability. Error handling must account for this compounding, not just individual step reliability [8].

4. **Recovery means changing the prompt, not the code.** Traditional software fixes bugs by changing code. LLM agent recovery means mutating context, adjusting prompts, switching models, or reducing capability scope. The "fix" is often architectural (add validation step) rather than code-level [8].

5. **Cost is per-attempt.** Every retry costs tokens. A reliability architecture with 3 retries, context mutation, and LLM-as-judge validation may spend 5-10x the tokens of a single attempt. Error handling must be budget-aware [8][9].

**Confidence: HIGH** — Stack Overflow (T2) and MAST (T1) provide strong convergent evidence on non-determinism challenges. SitePoint (T3) validates budget-awareness.

## Claims

| # | Claim | Type | Source | Status |
|---|-------|------|--------|--------|
| 1 | SHIELDA identifies 36 exception types across 12 agent artifacts | statistic | [4] | verified |
| 2 | MAST identifies 14 failure modes in 3 categories with kappa = 0.88 | statistic | [5] | verified |
| 3 | Multi-agent systems fail at 41-86.7% rates across 7 SOTA frameworks | statistic | [5][9] | verified |
| 4 | ~79% of multi-agent problems originate from specification (41.8%) + coordination (36.9%) | statistic | [5][9] | verified |
| 5 | Four 95% classifiers produce 81.4% pipeline reliability | calculation | [8] | verified (math checks: .95^4 = .8145) |
| 6 | Circuit breaker RR technique shows <1% capability degradation | statistic | [10] | verified |
| 7 | MAST dataset comprises 1600+ annotated traces across 7 frameworks | statistic | [5] | verified |
| 8 | SHIELDA was published at ICLR 2026 | attribution | [4] | unverified — not confirmed by search |

## Takeaways

Error handling for LLM-agent systems requires three shifts from traditional practice:

1. **Classify by retryability and origin phase, not exception type.** Traditional exception hierarchies assume deterministic failures. Agent errors need a two-axis taxonomy: can it succeed on retry (transient/correctable/structural) and where did it originate (reasoning/execution/verification). Execution failures often have reasoning-phase root causes.

2. **Build layered escalation with budget awareness.** Five escalation layers (retry, mutate, fallback, peer escalate, human escalate) with explicit thresholds at each level. Every layer costs tokens. Cap retry budgets at multiples of the original attempt cost. When 79% of multi-agent failures stem from specification issues, most structural errors should escalate quickly rather than burning budget on retries.

3. **Extend circuit breakers with semantic failure detection and a degraded state.** Standard three-state circuit breakers miss the defining challenge of LLM systems: failures that look like successes. Add a degraded state for partial capability and require semantic validation in probe requests. The evaluation pipeline itself becomes a critical dependency that needs its own error handling.
