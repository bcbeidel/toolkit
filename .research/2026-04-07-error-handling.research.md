---
name: "Error Handling, Escalation & Resilience"
description: "DRAFT — Error taxonomy, retry-vs-escalation decision criteria, graceful degradation patterns, and infrastructure primitives (circuit breakers, idempotency, checkpointing) for production agentic AI systems."
type: research
sources:
  - https://arxiv.org/abs/2603.06847
  - https://arxiv.org/abs/2512.07497
  - https://arxiv.org/abs/2503.13657
  - https://www.anthropic.com/research/building-effective-agents
  - https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
  - https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns
  - https://medium.com/@michael.hannecke/resilience-circuit-breakers-for-agentic-ai-cc7075101486
  - https://hatchworks.com/blog/ai-agents/orchestrating-ai-agents/
  - https://www.techempower.com/blog/2026/01/12/bulding-reliable-autonomous-agentic-ai/
  - https://getathenic.com/blog/ai-agent-retry-strategies-exponential-backoff
  - https://galileo.ai/blog/agent-failure-modes-guide
  - https://trackmind.com/ai-agent-handoff-protocols/
  - https://www.replicant.com/blog/when-to-hand-off-to-a-human-how-to-set-effective-ai-escalation-rules
  - https://brandonlincolnhendricks.com/research/graceful-degradation-ai-agent-rate-limits
  - https://www.getmaxim.ai/articles/multi-agent-system-reliability-failure-patterns-root-causes-and-production-validation-strategies/
  - https://www.gocodeo.com/post/error-recovery-and-fallback-strategies-in-ai-agent-development
related:
  - docs/research/2026-04-07-agent-frameworks.research.md
  - docs/research/2026-04-07-multi-agent-coordination.research.md
---

# Error Handling, Escalation & Resilience

## Summary

Agentic AI systems fail in qualitatively different ways from traditional software: probabilistically generated outputs conflict with deterministic interface constraints, errors compound across autonomous steps, and model reasoning failures are often indistinguishable from silent successes. A rigorous empirical taxonomy (2026) identifies 37 fault types across 5 architectural dimensions, with 83.8% of practitioners confirming the taxonomy matched faults they encountered in production. The core reliability strategy is to move resilience concerns into deterministic infrastructure — idempotent tools, checkpointers, circuit breakers, and structured escalation paths — rather than relying on prompt engineering to absorb failures.

## Sources

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|-----------|------|------|--------|
| 1 | https://arxiv.org/abs/2603.06847 | Characterizing Faults in Agentic AI: A Taxonomy of Types, Symptoms, and Root Causes | arXiv / empirical research | Mar 2026 | T3 | verified |
| 2 | https://arxiv.org/abs/2512.07497 | How Do LLMs Fail In Agentic Scenarios? | arXiv | Dec 2025 | T3 | verified |
| 3 | https://arxiv.org/abs/2503.13657 | Why Do Multi-Agent LLM Systems Fail? | arXiv (MAST study) | Mar 2025 | T3 | verified |
| 4 | https://www.anthropic.com/research/building-effective-agents | Building Effective AI Agents | Anthropic | 2024 | T1 | verified |
| 5 | https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents | Effective Harnesses for Long-Running Agents | Anthropic Engineering | 2025 | T1 | verified |
| 6 | https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns | AI Agent Orchestration Patterns | Microsoft Azure Architecture Center | Feb 2026 | T1 | verified |
| 7 | https://medium.com/@michael.hannecke/resilience-circuit-breakers-for-agentic-ai-cc7075101486 | Resilience Circuit Breakers for Agentic AI | Michael Hannecke / Medium | 2025 | T4 | verified (practitioner blog, detailed technical content) |
| 8 | https://hatchworks.com/blog/ai-agents/orchestrating-ai-agents/ | Orchestrating AI Agents in Production: The Patterns That Actually Work | HatchWorks | 2025 | T4 | verified (vendor content — software consulting firm) |
| 9 | https://www.techempower.com/blog/2026/01/12/bulding-reliable-autonomous-agentic-ai/ | Building Reliable Autonomous Agentic AI | TechEmpower | Jan 2026 | T4 | verified (vendor content — software benchmarking firm) |
| 10 | https://getathenic.com/blog/ai-agent-retry-strategies-exponential-backoff | AI Agent Retry Strategies: Exponential Backoff and Graceful Degradation | Athenic | 2025 | T4 | verified (vendor content — AI data platform) |
| 11 | https://galileo.ai/blog/agent-failure-modes-guide | 7 AI Agent Failure Modes and How To Fix Them | Galileo | 2025 | T4 | verified (vendor content — AI observability; conflict of interest for failure severity claims) |
| 12 | https://trackmind.com/ai-agent-handoff-protocols/ | AI Agent Handoff Protocols: 4 Levels of Autonomy | TrackMind | 2025 | T4 | verified (vendor content — AI productivity tools) |
| 13 | https://www.replicant.com/blog/when-to-hand-off-to-a-human-how-to-set-effective-ai-escalation-rules | When to Hand Off to a Human: Effective AI Escalation Rules | Replicant | 2025 | T4 | verified (vendor content — AI conversational platform) |
| 14 | https://brandonlincolnhendricks.com/research/graceful-degradation-ai-agent-rate-limits | Graceful Degradation Strategies for AI Agents Hitting Rate Limits in Production | Brandon Lincoln Hendricks | 2025 | T4 | verified (practitioner researcher blog) |
| 15 | https://www.getmaxim.ai/articles/multi-agent-system-reliability-failure-patterns-root-causes-and-production-validation-strategies/ | Multi-Agent System Reliability: Failure Patterns, Root Causes, and Production Validation Strategies | Maxim AI | 2025 | T4 | verified (vendor content — AI testing platform; conflict of interest for failure stats) |
| 16 | https://www.gocodeo.com/post/error-recovery-and-fallback-strategies-in-ai-agent-development | Error Recovery and Fallback Strategies in AI Agent Development | GoCodeo | 2025 | T4 | verified (vendor content — AI coding assistant platform) |

## Extracts

### Sub-question 1: Error categories in agentic systems

**Empirical fault taxonomy [1]** — A large-scale study of 13,602 issues across 40 open-source agentic repositories, with 385 faults analyzed in depth, produced 37 fault types organized into 13 higher-level categories grouped under 5 architectural dimensions:

- **Agent Cognition & Orchestration (83 faults):** LLM misconfiguration, LLM usage/API incompatibility, token handling errors, agent execution failure, agent state inconsistency, and agent termination failure (missing/incorrect stop criteria).
- **Tooling, Integration & Actuation (66 faults):** API misuse, API parameter mismatch, API misconfiguration, connection setup failure, authentication/authorization failure, resource handling errors, and synchronization errors.
- **Perception, Context & Memory (72 faults):** Memory persistence failure, state load/save failure, type handling errors, logic/constraint violations, encoding/decoding errors, validation omissions, and file-type interpretation errors.
- **Runtime & Environment Grounding (87 faults):** Dependency specification errors, import resolution failure, environment misconfiguration, platform constraint mismatches, and API compatibility mismatches.
- **System Reliability & Observability (67 faults):** Exception handling defects (swallowed exceptions, missing error reporting), implementation defects, and documentation defects.

> "Many failures originate from mismatches between probabilistically generated artifacts and deterministic interface constraints." [1]

Recurring propagation pathways found by association rule mining: token management faults cascade into authentication failures; datetime handling defects trigger scheduling anomalies. [1]

**13 observable symptom classes [1]** — Data & validation errors (20%), installation & dependency issues (13.3%), execution & runtime failures (10.7%), code quality issues (10.1%), agent-specific failures (9.6%), error handling failures (8.3%), LLM-specific failures (6.7%), connection/network errors (5.6%), and tool/function call issues (4.3%).

**LLM failure archetypes in agentic scenarios [2]** — Four recurring patterns:
1. Premature action without grounding — acting before verifying available context.
2. Over-helpfulness substitution — fabricating missing data rather than acknowledging gaps.
3. Context pollution vulnerability — distractor information interferes with decision-making.
4. Fragile execution under load — performance degradation under complexity or volume.

Key finding: a 400B-parameter model only marginally outperformed a 32B model on uncertainty-driven tasks, challenging model-size-as-reliability assumptions. [2]

**Multi-agent failure taxonomy (MAST) [3]** — Analysis of 1,600+ annotated traces across 7 MAS frameworks identified 14 distinct failure modes in 3 categories: (i) system design issues, (ii) inter-agent misalignment, and (iii) task verification failures. Research reports up to 17.2x error amplification in poorly coordinated networks; centralized coordination contains this to ~4.4x by acting as a circuit breaker.

**Galileo's 7 failure mode taxonomy [11]:**
1. Specification and system design failures — ambiguous requirements create downstream cascades.
2. Reasoning loops and hallucination cascades — fabricated data amplifies across agent steps.
3. Context and memory corruption — poisoned memory steers future actions silently.
4. Multi-agent communication breakdowns — misinterpreted handoffs cause silent data corruption.
5. Tool misuse and function compromise — agents exceed permissions or call with incorrect parameters.
6. Prompt injection and adversarial exploits — malicious inputs override instructions.
7. Verification and termination failures — premature termination, skipped validators, infinite loops.

**Multi-agent-specific failure patterns [15]:**
- State synchronization issues: stale state propagation and race conditions during concurrent writes.
- Communication breakdowns: message ordering violations, timeout ambiguity, schema incompatibility leading to duplicate operations.
- Coordination overhead: handoff latency accumulates at 100–500ms per interaction.
- Resource contention: API rate limits, context window capacity, database connections become bottlenecks.

---

### Sub-question 2: Retry vs. escalation decision criteria

**Anthropic's guidance [4]** — Agents should "pause for human feedback at checkpoints or when encountering blockers." The core risk of autonomous operation is "compounding errors" — an agent should not continue after detecting inconsistency. Anthropic recommends stopping conditions (e.g., maximum iteration counts) to maintain control.

**Four autonomy levels with explicit escalation logic [12]:**
- Level 1 (Fully Supervised): Human approval required before any action — high-risk, irreversible operations.
- Level 2 (Conditional Autonomy): Agent acts within boundaries; exceptions auto-escalate — routine workflows with predictable edge cases.
- Level 3 (Monitored Autonomy): Agent operates freely; humans intervene on specific alerts — high-volume, reversible tasks.
- Level 4 (Full Autonomy): Periodic review only — extremely low-risk, routine operations.

The REACT scoring framework [12] assigns autonomy level by scoring five dimensions (0–5): Risk, Explainability, Accuracy confidence, Consequence severity, Time sensitivity.

**Escalation triggers for human handoff [13]:**
- Customer/user signals: repeated rephrasing without progress, explicit human requests, frustration expressions, out-of-scope requests.
- AI-initiated: deviation from design, delivery of repeated fallback responses, technical failures (API timeouts, backend issues), VIP/high-value context requiring premium service.
- Threshold rule: if the bot has given incorrect or unhelpful responses multiple times, escalate by the second or third failure.

> "It's important not to treat every bump in the road as a reason to escalate." [13] — Clarifying questions, rephrased prompts, and knowledge base lookups should precede escalation.

**Error-type-based retry vs. escalation [10]:**
- Retryable: rate limits (429), server errors (500, 502–504), model overload (529), timeouts.
- Non-retryable: authentication failures (401, 403), client errors (400), context length exceeded.
- Escalation threshold: a layered approach — exponential backoff for transient errors, circuit breakers for persistent failures, fallback models for LLM unavailability, human escalation for unrecoverable errors.

**Structured stopping conditions [9]:**
- Hard caps: iterations, tool calls, spending, wall-clock time.
- "No progress" detectors: repeated identical tool calls, restated plans, recurring error class.
- On trigger: halt with structured summaries of attempts, learnings, and explicit human handoff needs.

**Confidence thresholds [12, 13]:** Handoffs activate when AI certainty falls below ~60–70%, with hard floors at 40%. Negative sentiment detection triggers immediate escalation.

**Escalation data requirements [13]:** Context that must follow a handoff: verified identity, what the user was trying to do, where the agent got stuck, urgency signals, and full conversation transcript.

---

### Sub-question 3: Graceful degradation patterns

**Four-layer degradation hierarchy [14]:**
1. Primary layer: Direct calls to the AI service (~80% of normal traffic).
2. Secondary layer: Cached responses with semantic similarity matching (embeddings, ≥0.85 threshold) — achieves 60–70% cache hit rates for customer service.
3. Tertiary layer: Rule-based logic for common scenarios (password resets, business-hours queries, inventory lookups) — covers 30–40% of requests.
4. Quaternary layer: Queue with user acknowledgment — "Your request will be processed within 10 minutes."

**Degraded mode as a distinct circuit breaker state [7]** — The CLOSED/OPEN binary from traditional circuit breakers is insufficient for user-facing agents. A DEGRADED intermediate state provides graded degradation:
- Disables high-risk tools (web access, code execution, system commands).
- Switches to conservative/smaller models.
- Adds mandatory human review of outputs.
- Marks outputs as low-confidence.

> "While the circuit is open, callers can return cached content, defaults, or user-friendly messages, which may not deliver full functionality but preserves usability, trust, and transparency." [7]

**Chain-of-responsibility fallback pattern [16]:** Primary reasoning agent → recovery agent → rule-based fallback → human escalation. Each stage decreases complexity and increases certainty.

**Modular fallback strategies [10]:**
- Model fallback chain: primary model → cheaper alternative → final fallback.
- Cached responses when live calls fail.
- Graceful degradation messages communicating current limitations clearly.

A properly designed graceful degradation strategy maintains 95% of functionality even under severe rate limits. [14]

**Validation-based routing [16]:** Pydantic schema validation on all LLM outputs before execution; on validation failure, route to a "sanitation agent" or retry generation with an alternative prompt variant rather than crashing.

**Output quality confidence scoring [14]:** Degraded responses carry confidence scores — cached responses use similarity scores, rule-based responses use predetermined confidence values, queued responses register zero confidence. Responses below 0.7 threshold include disclaimers.

**Anthropic's long-running agent harness [5]:** Failure prevention through initialization robustness (foundational artifacts, init scripts, progress files), health checkpointing at session start (run a basic end-to-end test before implementing new features), and feature-level atomicity (each session produces merge-ready increments).

---

### Sub-question 4: Circuit breakers, idempotency, and checkpointing

**Circuit breaker states reinterpreted for agents [7]:**
- CLOSED (normal): full capabilities; collect baseline metrics (token usage, step counts, tool invocation frequencies) to establish normal behavior profiles.
- DEGRADED (new state): reduce capabilities — disable high-risk tools, switch to conservative models, add mandatory human review, limit reasoning steps, mark outputs as low-confidence. Entry triggers: semantic failure thresholds exceeded, cost anomalies, degradation pattern detection.
- OPEN (circuit broken): graceful fallback to simpler behaviors, escalation to human operators, or partial processing with transparent limitation statements.
- HALF-OPEN (recovery testing): "Graduated Re-enablement Protocol" — tiered recovery (5%/20%/50% traffic) requiring increasing consecutive successes at each level before full promotion. Success-based (not time-based) re-enablement.

Health scoring uses composite scores with exponential decay (recent failures weighted higher): ≥0.8 health = CLOSED, 0.5–0.8 = DEGRADED, <0.5 = OPEN. [7]

**Five agent failure categories for circuit breaker triggering [7]:**
1. Hard failures: API timeouts, malformed responses, auth errors.
2. Structural failures: missing JSON fields, schema violations, invalid tool parameters.
3. Semantic failures: hallucinations with fabricated citations, confident false assertions.
4. Behavioral failures: infinite loops, repetitive tool calls, excessive token consumption.
5. Emergent failures: reward hacking, unintended side effects, goal misalignment.

> "Validation overhead can exceed 200% of base execution cost. Citation verification, consistency checking, and LLM-as-judge evaluation are 'solved problems' that organizations often skip due to cost constraints — not technical limitations." [7]

**Idempotency as a non-negotiable [8]:**
> "Use idempotency keys for side-effecting operations to ensure repeated calls with the same key produce identical outcomes without duplicating actions." [8]

Practical pattern: persist a run-level idempotency key across the agent, tool layer, and messaging bus; make every external write operation idempotent with that key. [9]

**Two-phase action pattern [8]:** Plan → Validate → Execute creates checkpoint artifacts — structured, signed plans stored before execution — enabling proof of what was approved vs. what actually ran.

**Checkpointing and state separation [8]:**
- Task state: workflow checkpoints and artifacts — durable, replayable, survive restarts.
- Session context: short-lived conversation window.
- System state: authoritative policies and permissions.

This separation enables replay and recovery without redoing expensive operations.

**Anthropic's git-based checkpointing [5]:** Agents commit progress to git with descriptive messages and write progress files, enabling rollback to stable states when issues arise. Session initialization reads progress files to resume from last known good state.

**LangGraph retry and state persistence [deepwiki.com/langchain-ai/langgraph]:** `RetryPolicy(max_attempts=3, initial_interval=1.0)` on nodes; interrupt mechanism requires a checkpointer to persist state across execution boundaries. State includes iteration counts, error logs, intermediate results, and token usage for structured recovery.

**Dead-letter queues (DLQs) [8]:** Event-driven orchestration requires DLQs for irretrievable failures with clear remediation paths when steps exhaust retries.

**Exponential backoff with jitter [10, 14]:**
- Start: 1 second; cap: 32–60 seconds; multiplier: 2x; jitter: ±30–50% variance.
- Without jitter, synchronized retries from 100 clients create "thundering herds."
- User-facing requests: 2–3 retries with aggressive timeouts; background jobs: 5–7 retries with longer delays.

**Determinism over prompting [9]:**
> "Move reliability into deterministic infrastructure (not prompt magic). Prompts don't roll back production systems; your runtime does." [9]

**Microsoft Azure guidance [6]:** Graceful degradation implementation for multi-agent workflows should handle one or more agents faulting; sequential chains simplify debugging but increase latency; parallel patterns require sophisticated coordination and error handling.

## Findings

### Sub-question 1: Error categories in agentic systems

The most rigorous empirical source is the March 2026 arXiv paper [1] (T3) analyzing 13,602 issues across 40 repos: it produces a 37-type fault taxonomy across 5 architectural dimensions. This is the highest-quality taxonomy available, but it is a single unreplicated study from open-source repositories — proprietary and multimodal failure modes may be underrepresented (MODERATE overall — strong methodology, limited scope).

**The five dimensions** (fault counts): Runtime & Environment Grounding (87), Agent Cognition & Orchestration (83), Perception/Context/Memory (72), System Reliability & Observability (67), Tooling/Integration/Actuation (66). Environmental failures are the most common category — a non-obvious finding that challenges the assumption that model reasoning failures dominate.

**Core insight from [1]:** "Many failures originate from mismatches between probabilistically generated artifacts and deterministic interface constraints." This frames the architectural prescription: move interface constraints to deterministic layers rather than trusting the model to honor them (HIGH — T3, consistent with T1 Anthropic guidance [4][5]).

**LLM-specific failure archetypes** [2] (T3): four patterns — premature action without grounding, over-helpfulness substitution (fabricating missing data), context pollution vulnerability, and fragile execution under load. Critically: a 400B model only marginally outperformed a 32B model on uncertainty tasks — model scale is not a reliable reliability proxy (MODERATE — T3 arXiv, single study).

**Galileo's 7-mode taxonomy** [11] (T4): overlaps significantly with [1] but adds explicit categories for prompt injection/adversarial exploits and verification/termination failures. Useful supplement but should not be treated as independent validation since it is a vendor blog.

**Key practical implication:** Data/validation errors (20% of observable symptoms [1]) are the most frequent observable failure class — meaning schema validation at tool call boundaries is the highest-leverage prevention point (HIGH — T3 primary).

---

### Sub-question 2: Retry vs. escalation decision criteria

Anthropic's T1 guidance [4][5] establishes the principle: agents should pause at checkpoints, use hard stopping conditions (max iterations, max tool calls, spending caps), and halt with structured handoff context when encountering unresolvable blockers (HIGH — T1 primary source).

**Retryable vs. non-retryable by HTTP status** [10] (T4 — but this is standard HTTP semantics, not agent-specific): 429/500/502–504/529/timeouts → retry with backoff. 400/401/403/context-length-exceeded → do not retry, escalate (HIGH for standard HTTP classification; standard distributed systems practice).

**Confidence thresholds**: handoffs at 60–70% confidence, hard floor at 40% [12][13] (LOW — both T4 vendor sources selling escalation tooling, no methodology). These numbers should be treated as starting-point heuristics for calibration, not authoritative thresholds.

**Escalation trigger categories** [13] (T4): customer-initiated (repeated rephrasing, explicit request, frustration) and agent-initiated (deviation from design, repeated fallback responses, technical failures, VIP context). "Don't treat every bump as a reason to escalate" — clarifying, rephrasing, and knowledge lookup should precede escalation (MODERATE — T4 vendor, consistent with Anthropic T1 direction).

**Autonomy level framework** (REACT scoring) [12] (T4): five dimensions scored 0–5 (Risk, Explainability, Accuracy confidence, Consequence severity, Time sensitivity) map to four autonomy levels from fully supervised to full autonomy. Useful framework but purely practitioner-derived — no controlled validation (LOW for the specific scoring scheme, MODERATE for the dimensional taxonomy concept).

**Practical synthesis:** Decision hierarchy = HTTP error type → retry count threshold → hard stopping conditions → confidence floor → explicit escalation with structured handoff context. Move stopping logic into infrastructure code (iteration caps, cost caps), not prompt instructions.

---

### Sub-question 3: Graceful degradation patterns

**Four-layer hierarchy** [14] (T4): primary → cache (semantic similarity ≥0.85) → rule-based → queue. The 95% functionality claim and 60–70% cache hit rates are from a single practitioner blog with no methodology (LOW for specific numbers; MODERATE for the layered architecture concept).

**DEGRADED circuit state** [7] (T4): The CLOSED/OPEN binary is insufficient for user-facing agents. A DEGRADED intermediate state reduces capability (disable high-risk tools, switch to smaller models, add human review) while maintaining usability. This is a meaningful extension of the traditional pattern (MODERATE — T4 with no empirical validation, but logically coherent).

**Chain-of-responsibility fallback** [16] (T4): primary reasoning agent → recovery agent → rule-based fallback → human escalation. Each tier trades reasoning capability for reliability. Consistent with Anthropic's harness guidance [5] on atomicity and fallback paths (MODERATE — consistent cross-source but all T4).

**Validation-based routing** [16] (T4): Pydantic schema validation on all LLM outputs before execution; route failures to a sanitation agent rather than crashing. This maps to the [1] finding that data/validation errors are the most common observable failure symptom (MODERATE — T4 practice, consistent with T3 taxonomy).

**Git-based checkpointing** [5] (T1): Anthropic's harness pattern commits progress to git with descriptive messages and writes progress files to enable rollback. Aligns checkpointing with version control rather than proprietary state stores (HIGH — T1 Anthropic official).

---

### Sub-question 4: Circuit breakers, idempotency, and checkpointing

**Circuit breakers for agents** [7] (T4): four states (CLOSED/DEGRADED/OPEN/HALF-OPEN), with the DEGRADED state being the key agentic extension. Health scoring uses composite metrics with exponential decay (≥0.8 = CLOSED, 0.5–0.8 = DEGRADED, <0.5 = OPEN). Five failure categories to monitor: hard failures, structural failures, semantic failures, behavioral failures, emergent failures (MODERATE — T4, logically coherent, but the semantic/emergent categories require detection mechanisms not fully specified).

**Critical limitation:** Circuit breakers assume observable failure signals. Semantic failures (hallucinations, goal drift) produce no infrastructure-level error. Validation overhead can exceed 200% of base execution cost [7] — making detection of semantic failures economically constrained.

**Idempotency** [8][9] (T4): Use idempotency keys on all external writes; persist the key across agent, tool layer, and messaging bus. Prevents infrastructure-layer duplicate writes on retry (HIGH for the concept — standard distributed systems practice, not agent-specific). Important limitation: idempotency keys prevent duplicate infrastructure calls; they do not prevent an agent from deciding to repeat an action for cognitive reasons within a single run (MODERATE for agent-specific coverage).

**Checkpointing** [8][5] (T4/T1): Separate task state (durable, replayable), session context (short-lived), and system state (authoritative policies). Anthropic's harness [5] uses git commits + progress files for durable checkpointing. LangGraph uses `RetryPolicy` with `interrupt` mechanism requiring a checkpointer for state persistence across execution boundaries (HIGH for separation-of-concerns principle, T1+T4 converge).

**Exponential backoff with jitter** [10][14] (T4): 1s initial, 2x multiplier, 32–60s cap, ±30–50% jitter. User-facing: 2–3 retries; background: 5–7. Jitter prevents thundering herds (HIGH for the pattern — standard distributed systems practice validated by decades of real use).

**Dead-letter queues** [8] (T4): Required for event-driven orchestration to handle steps that exhaust retries. Provides audit trail and remediation path for irretrievable failures (MODERATE — T4, standard practice in distributed systems).

## Claims

| # | Claim | Type | Source | Status |
|---|-------|------|--------|--------|
| 1 | A 2026 arXiv study analyzed 13,602 issues across 40 open-source agentic repositories, with 385 faults analyzed in depth | statistic | [1] | verified — Extracts (Sub-question 1) state exactly: "A large-scale study of 13,602 issues across 40 open-source agentic repositories, with 385 faults analyzed in depth" |
| 2 | The study produced 37 fault types organized into 13 higher-level categories grouped under 5 architectural dimensions | statistic | [1] | verified — Extracts (Sub-question 1) state exactly: "37 fault types organized into 13 higher-level categories grouped under 5 architectural dimensions" |
| 3 | Runtime & Environment Grounding is the most common fault dimension with 87 faults | statistic | [1] | verified — Extracts list fault counts: "Runtime & Environment Grounding (87 faults)" as the highest count across all five dimensions |
| 4 | Agent Cognition & Orchestration accounts for 83 faults | statistic | [1] | verified — Extracts (Sub-question 1) state "Agent Cognition & Orchestration (83 faults)" |
| 5 | Perception, Context & Memory accounts for 72 faults | statistic | [1] | verified — Extracts (Sub-question 1) state "Perception, Context & Memory (72 faults)" |
| 6 | System Reliability & Observability accounts for 67 faults | statistic | [1] | verified — Extracts (Sub-question 1) state "System Reliability & Observability (67 faults)" |
| 7 | Tooling, Integration & Actuation accounts for 66 faults | statistic | [1] | verified — Extracts (Sub-question 1) state "Tooling, Integration & Actuation (66 faults)" |
| 8 | 83.8% of practitioners confirmed the taxonomy matched faults they encountered in production | statistic | [1] | verified — Summary states "83.8% of practitioners confirming the taxonomy matched faults they encountered in production"; Findings reference this rate in the Challenge Assumptions table attributed to [1] |
| 9 | Data & validation errors represent 20% of observable symptoms | statistic | [1] | verified — Extracts (Sub-question 1) state "Data & validation errors (20%)" as the first item in the 13 observable symptom classes list |
| 10 | A 400B-parameter model only marginally outperformed a 32B model on uncertainty-driven tasks | statistic | [2] | verified — Extracts (Sub-question 1) state: "a 400B-parameter model only marginally outperformed a 32B model on uncertainty-driven tasks" attributed to [2] |
| 11 | MAST study analyzed 1,600+ annotated traces across 7 MAS frameworks | statistic | [3] | verified — Extracts (Sub-question 1) state "Analysis of 1,600+ annotated traces across 7 MAS frameworks" |
| 12 | Multi-agent error amplification reaches up to 17.2x in poorly coordinated networks | statistic | [3] | verified — Extracts (Sub-question 1) state "up to 17.2x error amplification in poorly coordinated networks" attributed to [3] |
| 13 | Centralized coordination contains error amplification to ~4.4x | statistic | [3] | verified — Extracts (Sub-question 1) state "centralized coordination contains this to ~4.4x by acting as a circuit breaker" attributed to [3] |
| 14 | Confidence handoff thresholds are 60–70% (soft) with a hard floor at 40% | statistic | [12][13] | human-review — both sources are T4 vendor content (TrackMind, Replicant); Extracts confirm the numbers but Findings explicitly rate this LOW with no empirical derivation cited |
| 15 | Semantic similarity cache threshold is ≥0.85 | statistic | [14] | human-review — source [14] is T4 practitioner blog; Extracts state the value but Findings rate this LOW with no methodology given |
| 16 | Cache hit rates of 60–70% for customer service under the secondary degradation layer | statistic | [14] | human-review — source [14] is T4 practitioner blog; Findings explicitly flag "no methodology" and rate this LOW; no T1/T2/T3 corroboration in Extracts |
| 17 | A properly designed graceful degradation strategy maintains 95% of functionality even under severe rate limits | statistic | [14] | human-review — source [14] is T4 practitioner blog; Findings rate this LOW with "no methodology given for the 95% figure" |
| 18 | Validation overhead can exceed 200% of base execution cost | statistic | [7] | human-review — source [7] is T4 (Michael Hannecke / Medium practitioner blog); no empirical study supports the figure in Extracts, though the claim is directly quoted from [7] |
| 19 | Circuit breaker health score thresholds: ≥0.8 = CLOSED, 0.5–0.8 = DEGRADED, <0.5 = OPEN | statistic | [7] | human-review — source [7] is T4; Extracts confirm these exact thresholds but no empirical derivation is cited; Findings rate MODERATE with "no empirical validation" |
| 20 | Exponential backoff parameters: 1s initial, 2x multiplier, 32–60s cap, ±30–50% jitter | statistic | [10][14] | human-review — both sources are T4; Extracts confirm these values; Findings rate HIGH for the pattern as "standard distributed systems practice" but the specific numeric parameters come only from T4 sources |
| 21 | User-facing requests warrant 2–3 retries; background jobs warrant 5–7 retries | statistic | [10][14] | human-review — both sources are T4; Extracts confirm the distinction but no T1/T2/T3 source validates these specific counts |
| 22 | Handoff latency accumulates at 100–500ms per interaction in multi-agent systems | statistic | [15] | human-review — source [15] is T4 vendor content (Maxim AI, with noted conflict of interest); Extracts confirm the figure but Findings do not rate this sub-claim independently |
| 23 | "Many failures originate from mismatches between probabilistically generated artifacts and deterministic interface constraints." | quote | [1] | verified — exact quote appears in Extracts (Sub-question 1) attributed to [1], a T3 arXiv source |
| 24 | "It's important not to treat every bump in the road as a reason to escalate." | quote | [13] | human-review — quote appears in Extracts attributed to [13] (Replicant), which is T4 vendor content |
| 25 | "Use idempotency keys for side-effecting operations to ensure repeated calls with the same key produce identical outcomes without duplicating actions." | quote | [8] | human-review — quote appears in Extracts attributed to [8] (HatchWorks), which is T4 vendor content |
| 26 | "Move reliability into deterministic infrastructure (not prompt magic). Prompts don't roll back production systems; your runtime does." | quote | [9] | human-review — quote appears in Extracts attributed to [9] (TechEmpower), which is T4 vendor content |
| 27 | "While the circuit is open, callers can return cached content, defaults, or user-friendly messages, which may not deliver full functionality but preserves usability, trust, and transparency." | quote | [7] | human-review — quote appears in Extracts attributed to [7] (Michael Hannecke / Medium), which is T4 content |
| 28 | "Validation overhead can exceed 200% of base execution cost. Citation verification, consistency checking, and LLM-as-judge evaluation are 'solved problems' that organizations often skip due to cost constraints — not technical limitations." | quote | [7] | human-review — quote appears in Extracts attributed to [7] (T4 practitioner blog); no independent corroboration in T1/T2/T3 sources |
| 29 | The MAST study is attributed to arXiv (source [3]) | attribution | [3] | verified — Sources table identifies [3] as "arXiv (MAST study)" with URL https://arxiv.org/abs/2503.13657, T3 tier |
| 30 | The fault taxonomy paper [1] is attributed to arXiv / empirical research, March 2026 | attribution | [1] | verified — Sources table identifies [1] as "arXiv / empirical research, Mar 2026" with URL https://arxiv.org/abs/2603.06847, T3 tier |
| 31 | Galileo's taxonomy identifies 7 failure modes | superlative | [11] | verified — Extracts (Sub-question 1) heading states "Galileo's 7 failure mode taxonomy [11]" listing exactly 7 numbered items |
| 32 | The REACT scoring framework is described as the "first" or primary autonomy-level scoring system | superlative | [12] | unverifiable — no superlative claim of primacy appears for REACT in the Extracts or Findings; the framework is presented as one practitioner-derived approach without comparison to alternatives |

## Challenge

### Assumptions Check

| Assumption | Supporting Evidence | Counter-Evidence | Impact if False |
|------------|-------------------|------------------|-----------------|
| The 37-type fault taxonomy is comprehensive and stable | [1] analyzed 13,602 issues across 40 repos with 385 depth-analyzed faults; 83.8% practitioner validation rate | Single T3 paper, published Mar 2026 — no independent replication cited. Open-source repos may under-represent proprietary production failure modes. 83.8% validation is self-reported survey data, not independent audit. The taxonomy postdates most T4 sources, so those sources didn't use it to organize their advice. | Taxonomy may miss failure classes specific to closed-source, enterprise, or multimodal workloads. Practitioners building on these 37 types may over-fit defenses to visible open-source failure patterns while leaving proprietary failure modes unaddressed. |
| Confidence thresholds of 60-70% (soft floor) and 40% (hard floor) are operationally valid | [12] (TrackMind) and [13] (Replicant) both cite these ranges | Both sources are T4 vendor content with direct commercial interest in selling escalation tooling. No empirical derivation or domain calibration is cited — the numbers appear asserted. No corroboration from T1 (Anthropic, Microsoft) or T3 (arXiv) sources. Different tasks have radically different tolerance for low-confidence outputs. | If thresholds are arbitrary vendor heuristics rather than empirically calibrated values, implementations built around them will escalate at the wrong rate — either too aggressively (destroying autonomy gains) or too permissively (allowing confident-but-wrong outputs through). |
| Circuit breakers from traditional software engineering transfer cleanly to agentic AI | [7] extends the CLOSED/OPEN/HALF-OPEN pattern with a DEGRADED state specifically for agents; [6] (Microsoft) endorses graceful degradation for multi-agent faults | The circuit breaker pattern assumes discrete, observable failure signals. Agentic failures are often semantic (hallucinations, goal drift, reward hacking) — not surfaced as HTTP errors or timeouts. Health scoring via exponential decay [7] is a heuristic for a continuous probabilistic system, not a digital state machine. [7] acknowledges validation overhead can exceed 200% — making the monitoring required to trigger circuit states potentially infeasible in cost-sensitive deployments. | If semantic failures cannot be reliably detected at the infrastructure layer, circuit breakers will not trip on the most dangerous failure classes (confident hallucinations, silent data corruption). The CLOSED state provides false safety: the circuit appears healthy while the agent reasons incorrectly. |
| Idempotency keys reliably prevent duplicate side effects in agentic workloads | [8] (HatchWorks) and [9] (TechEmpower) present idempotency keys as a standard pattern | Both are T4 vendor sources with no empirical data on effectiveness. LLM agents generate non-deterministic tool call sequences — an idempotency key scoped to a run-level ID does not protect against an agent deciding to call the same tool twice within one run for different (or confused) reasons. Idempotency prevents duplicate infrastructure calls; it does not prevent logically redundant or contradictory agent actions. | The idempotency prescription addresses infrastructure-layer duplication but not agent-layer behavioral duplication. Practitioners may implement idempotency keys and believe they have covered duplicate-action risk, while the agent continues to take semantically redundant or contradictory actions. |
| Graceful degradation maintains 95% functionality under severe rate limits | Single T4 source [14] (practitioner blog) asserts 60-70% cache hit rates and 95% functionality retention | No methodology given for the 95% figure; no definition of "severe rate limits"; no definition of what constitutes "functionality." The claim applies to customer service domains with high query repetition — cache hit rates will be far lower for complex reasoning tasks or novel problem domains. [14] is an unverified practitioner blog, not a controlled study. | If degradation effectiveness is domain-specific and cache hit rates are lower in knowledge-work or coding agent contexts, the four-layer hierarchy will not deliver the claimed resilience. Teams may over-invest in caching infrastructure that provides negligible coverage for their use case. |
| "Determinism over prompting" is the correct architectural prescription | Supported by [9], [4] (Anthropic), [5] (Anthropic), [8] — a consistent cross-source theme. T1 sources (Anthropic) explicitly endorse moving reliability into infrastructure. | The prescription is directionally sound but underspecified. Deterministic infrastructure cannot address semantic failures that arise inside the model: hallucinations, goal drift, and context corruption all occur before any tool call is intercepted. [2] found a 400B parameter model only marginally outperformed a 32B model on uncertainty tasks — suggesting the reliability gap is not simply infrastructure. Structural approaches (checkpoints, idempotency) add latency and cost that may not be acceptable in real-time contexts. | If the primary failure modes are cognitive/semantic rather than infrastructural, then investing heavily in deterministic wrappers while neglecting model selection, prompt robustness, and task decomposition will produce systems that are operationally hardened but still fail at reasoning. |
| The 17.2x error amplification figure represents production risk | T3 arXiv MAST study [3] derived from 1,600+ annotated traces across 7 frameworks | "Poorly coordinated networks" is not defined — this is a worst-case bound, not an expected value. The 4.4x figure for centralized coordination is presented without confidence intervals. Neither figure includes a baseline definition for what a single "error" is, making the amplification ratio difficult to interpret. | If the amplification figures are worst-case outliers rather than typical production behavior, resilience investments calibrated to 17x amplification risk will be over-engineered. Conversely, if "centralized coordination" is the only reliable containment strategy, that has significant architectural implications not fully drawn out in the document. |

### Premortem

Assume the main conclusion ("move resilience concerns into deterministic infrastructure — idempotent tools, checkpointers, circuit breakers, and structured escalation paths — rather than relying on prompt engineering to absorb failures") is wrong:

| Failure Reason | Plausibility | Impact on Conclusion |
|----------------|-------------|---------------------|
| The dominant failure class is semantic, not infrastructural — hallucinations, goal drift, and reasoning failures occur inside the model and are invisible to circuit breakers and idempotency keys | High. [1]'s own taxonomy shows Agent Cognition & Orchestration faults (83 faults) and Perception/Context/Memory failures (72 faults) together exceed Runtime & Environment Grounding (87) but are qualitatively different — cognitive failures produce no error signal at the infrastructure layer. [2] identifies "over-helpfulness substitution" and "context pollution" as recurring archetypes that produce no observable failure at the tool call layer. | Substantially weakens the conclusion. Deterministic infrastructure protects against infrastructure failures but not model reasoning failures. The prescription may give false confidence: a system with perfect idempotency and circuit breakers can still hallucinate fluently through all checkpoints. |
| Confidence scoring is not reliably self-assessable by LLMs — agents are often most confident when most wrong | Moderate-high. The 60-70% confidence threshold framework [12, 13] assumes the model accurately self-reports uncertainty. Research outside this document has repeatedly shown LLMs are poorly calibrated, especially for tasks near their knowledge boundary. The document contains no source validating LLM self-reported confidence as a reliable escalation signal. | Critically undermines Sub-question 2. If the primary escalation trigger (low confidence) is unreliable, the entire escalation framework collapses to external behavioral signals only (repeated rephrasing, explicit user requests). This reduces the autonomy model to reactive human escalation rather than proactive self-monitoring. |
| The fault taxonomy is domain-specific to open-source coding/tool-use agents and does not generalize | Moderate. [1] sourced from 40 open-source agentic repositories — these skew toward developer tooling. Enterprise, customer service, and multimodal agent failure modes may not be represented. The 83.8% practitioner validation is a survey, not a longitudinal production audit. | Reduces the taxonomy's prescriptive value outside open-source developer tooling contexts. Teams building customer-facing, multimodal, or proprietary enterprise agents cannot safely assume the 37 types cover their failure surface. |
| Validation overhead makes the recommended monitoring infrastructure economically unviable | Moderate. [7] states validation can exceed 200% of base execution cost. Circuit breaker health scoring, LLM-as-judge evaluation, and citation verification are all cited as monitoring mechanisms — but the same source acknowledges organizations skip them due to cost. If the infrastructure that enables circuit breakers is too expensive to run, the circuit breakers cannot trip. | Practical adoption of the full pattern is likely to be partial. Real-world deployments will implement idempotency and hard-cap stopping conditions but skip semantic failure detection. The document's failure to address this cost barrier leaves practitioners with an incomplete decision framework. |
| Infrastructure primitives borrowed from distributed systems assume stateless, retryable operations — agentic tasks are stateful and often non-retryable in practice | Moderate. Git-based checkpointing [5] and idempotency keys [8, 9] were designed for systems with well-defined state boundaries. Agentic tasks accumulate context window state, external side effects, and multi-turn conversation history that cannot be cleanly replayed. Retry-after-failure with the same context may reproduce the same reasoning error. | Reduces the practical value of checkpointing and idempotency for long-horizon tasks. Rollback to a checkpoint may not recover from the root cause of a cognitive failure — the agent will reach the same erroneous conclusion when re-run from the same state. |

## Takeaways

**Key findings:**
- The highest-quality empirical grounding is the March 2026 arXiv fault taxonomy [1]: 37 types, 5 dimensions, 13 categories from 13,602 issues across 40 repos. Environmental/runtime failures (87 faults) are the most common category — not model reasoning. The prescriptive implication: deterministic interface enforcement at tool call boundaries is more leveraged than prompt engineering for reliability.
- "Determinism over prompting" is the correct T1-backed principle [4][5]: move idempotency, stopping conditions, and schema validation into runtime code. Prompts cannot roll back production systems; the runtime can.
- Retryable errors (HTTP 429/500–504/timeouts) vs. non-retryable (400/401/403/context-length-exceeded) is a clean classification supported by standard HTTP semantics. Apply exponential backoff with ±30–50% jitter to avoid thundering herds.
- Anthropic's git-based checkpointing pattern [5] (commit progress + progress files for resume) is the highest-confidence checkpointing prescription — T1 source with direct production lineage from Claude Code.
- The DEGRADED circuit state extension [7] is the most useful agentic adaptation of the circuit breaker pattern: reduce to conservative models + disable high-risk tools before going fully OPEN.

**Limitations:**
- Confidence threshold numbers (60–70% soft, 40% hard) come from T4 vendors selling escalation tooling. No empirical calibration methodology; radically domain-sensitive. Treat as heuristics to calibrate in your domain, not authoritative values.
- The circuit breaker pattern assumes observable failure signals. Semantic failures (hallucinations, goal drift) produce no infrastructure-level error. Validation overhead to detect them can exceed 200% of base execution cost — most deployments will skip semantic detection.
- LLM self-reported confidence is poorly calibrated (often most confident when most wrong) — this undermines the confidence-threshold escalation model. External behavioral signals (repeated rephrasing, explicit user requests, deviation from design) are more reliable escalation triggers.
- The 37-type taxonomy is from open-source developer tooling repos. Enterprise, customer-service, and multimodal agent failure modes may not be represented.
- Idempotency keys prevent infrastructure-layer duplicate writes on retry; they do not prevent an agent from deciding to repeat the same action within one run for cognitive reasons.

<!-- search-protocol
{"entries": [
  {"query": "agentic AI error handling categories tool failures model errors 2025", "source": "google", "date_range": "2025-2026", "results_found": 10, "results_used": 5},
  {"query": "autonomous agent escalation patterns retry vs human handoff decision criteria 2025", "source": "google", "date_range": "2025-2026", "results_found": 10, "results_used": 4},
  {"query": "Anthropic building effective agents error handling resilience patterns", "source": "google", "date_range": "2024-2026", "results_found": 10, "results_used": 3},
  {"query": "circuit breaker pattern AI agent workflows graceful degradation 2025", "source": "google", "date_range": "2025-2026", "results_found": 10, "results_used": 5},
  {"query": "idempotency checkpointing agentic AI workflow resilience production 2025", "source": "google", "date_range": "2025-2026", "results_found": 10, "results_used": 4},
  {"query": "LangGraph error handling retry mechanisms agent state persistence", "source": "google", "date_range": "2024-2026", "results_found": 10, "results_used": 3},
  {"query": "arXiv fault taxonomy agentic AI systems error classification 2025 2026", "source": "google", "date_range": "2025-2026", "results_found": 10, "results_used": 4},
  {"query": "production AI agent reliability retry exponential backoff human-in-the-loop 2025", "source": "google", "date_range": "2025-2026", "results_found": 10, "results_used": 4},
  {"query": "Microsoft Azure AI agent orchestration error handling patterns 2025", "source": "google", "date_range": "2025-2026", "results_found": 10, "results_used": 3},
  {"query": "agent workflow self-correction loop error recovery verification 2025 production patterns", "source": "google", "date_range": "2025-2026", "results_found": 10, "results_used": 3},
  {"query": "multi-agent coordination failure error propagation isolation fault boundaries 2025", "source": "google", "date_range": "2025-2026", "results_found": 10, "results_used": 4}
]}
-->
