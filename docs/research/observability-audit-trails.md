---
name: "Observability and Audit Trails for Agent Systems"
description: "How to make agent activity inspectable through structured logging, OpenTelemetry tracing, search protocol recording, checkpoint annotations, and provenance tracking — covering standards, trace formats, and show-your-work patterns that enable debugging and trust"
type: research
sources:
  - https://opentelemetry.io/blog/2025/ai-agent-observability/
  - https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-agent-spans/
  - https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-spans/
  - https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-events/
  - https://github.com/open-telemetry/semantic-conventions/issues/2664
  - https://opentelemetry.io/blog/2024/llm-observability/
  - https://github.com/traceloop/openllmetry
  - https://arize-ai.github.io/openinference/spec/
  - https://github.com/Arize-ai/openinference
  - https://github.com/agentkitai/agentlens
  - https://arxiv.org/html/2508.02866v2
  - https://www.w3.org/TR/trace-context/
  - https://langfuse.com/docs/observability/overview
  - https://develop.sentry.dev/sdk/telemetry/traces/modules/ai-agents/
  - https://blog.langchain.com/debugging-deep-agents-with-langsmith/
  - https://allen.hutchison.org/2026/02/17/the-observability-gap/
related:
  - docs/research/workflow-orchestration.md
  - docs/research/tool-design-for-llms.md
  - docs/research/validation-architecture.md
  - docs/research/multi-agent-coordination.md
  - docs/context/agent-observability-tracing.md
  - docs/context/show-your-work-patterns.md
  - docs/context/observability-trust-debuggability.md
---

## Summary

Agent observability is the ability to trace, evaluate, and debug agent runs -- including prompts, tool calls, outputs, cost, and quality signals -- so that operators can reconstruct a full run, compare versions, detect drift, and connect technical metrics to user outcomes. Unlike traditional application monitoring, agent observability must capture reasoning chains, non-deterministic decision paths, and tool orchestration that characterize agentic systems.

**Key findings:**

- **OpenTelemetry GenAI semantic conventions provide a vendor-neutral standard for agent tracing.** The `gen_ai.*` attribute namespace defines spans for agent invocation (`invoke_agent`), tool execution (`execute_tool`), and LLM calls (`chat`, `text_completion`), with attributes for token usage, model identity, and agent metadata (HIGH).
- **The trace-span hierarchy maps naturally to agent execution.** A trace captures a full request; child spans represent agent invocations, LLM calls, and tool executions, forming a tree that mirrors the agent's reasoning and action sequence (HIGH).
- **Structured logging with trace correlation is the minimum viable observability pattern.** Every log entry should carry `trace_id` and `span_id` from the moment a request enters the system, enabling cross-cutting queries that connect agent decisions to their outcomes (HIGH).
- **Provenance tracking extends tracing into accountability.** PROV-AGENT and similar frameworks extend W3C PROV to model AI-specific artifacts (prompts, responses, tool invocations, model configurations), enabling audit trails that trace decisions back to originating inputs (MODERATE).
- **"Show your work" patterns -- search protocol logs, checkpoint annotations, reasoning traces -- are essential for trust.** The ReAct pattern (Thought-Action-Observation) and flight recorder patterns like AgentLens create inspectable records of agent reasoning that serve debugging, compliance, and user trust simultaneously (HIGH).
- **Tamper-evident audit trails using cryptographic hash chains protect the integrity of agent logs.** Append-only event storage with SHA-256 hash chains per session provides verifiable, immutable records of agent behavior (MODERATE).

17 searches across 1 source (google), 170 results found, 31 used. 16 sources verified, 0 removed.

## Research Brief

This investigation examines how to make agent activity inspectable, focusing on the technical patterns, standards, and tools that enable debugging and trust in LLM agent systems. The scope covers structured logging, OpenTelemetry-based tracing, search protocol recording, checkpoint annotations, trace formats, and provenance tracking. The domain is software agent systems built on LLMs, particularly those using tool calling and multi-step reasoning. The investigation is constrained to patterns applicable to plugin-style agent architectures (like WOS) rather than large-scale multi-agent deployments.

### Sub-Questions

1. What structured logging and tracing approaches work for LLM agent systems, and how does OpenTelemetry apply?
2. How do existing agent frameworks implement "show your work" patterns (search protocol recording, checkpoint annotations, audit trails)?
3. What trace formats and data models best capture agent reasoning chains and tool invocations?
4. What design patterns enable trust and debuggability in agent systems through observability?

## Sources

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|-----------|------|------|--------|
| 1 | https://opentelemetry.io/blog/2025/ai-agent-observability/ | AI Agent Observability - Evolving Standards | OpenTelemetry / CNCF | 2025 | T1 | verified |
| 2 | https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-agent-spans/ | Semantic Conventions for GenAI Agent Spans | OpenTelemetry / CNCF | 2025 | T1 | verified |
| 3 | https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-spans/ | Semantic Conventions for GenAI Client Spans | OpenTelemetry / CNCF | 2025 | T1 | verified |
| 4 | https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-events/ | Semantic Conventions for GenAI Events | OpenTelemetry / CNCF | 2025 | T1 | verified |
| 5 | https://github.com/open-telemetry/semantic-conventions/issues/2664 | Semantic Conventions for GenAI Agentic Systems | OpenTelemetry Contributors | 2025 | T1 | verified |
| 6 | https://opentelemetry.io/blog/2024/llm-observability/ | Introduction to Observability for LLM Applications | OpenTelemetry / CNCF | 2024 | T1 | verified |
| 7 | https://github.com/traceloop/openllmetry | OpenLLMetry - Open-source GenAI Observability | Traceloop | 2025 | T4 | verified |
| 8 | https://arize-ai.github.io/openinference/spec/ | OpenInference Specification | Arize AI | 2025 | T4 | verified |
| 9 | https://github.com/Arize-ai/openinference | OpenInference - OpenTelemetry for AI Observability | Arize AI | 2025 | T4 | verified |
| 10 | https://github.com/agentkitai/agentlens | AgentLens - Flight Recorder for AI Agents | AgentKit AI | 2025 | T4 | verified |
| 11 | https://arxiv.org/html/2508.02866v2 | PROV-AGENT: Unified Provenance for AI Agent Workflows | UT-Battelle / Oak Ridge National Lab | 2025 | T2 | verified |
| 12 | https://www.w3.org/TR/trace-context/ | W3C Trace Context Specification | W3C | 2024 | T1 | verified |
| 13 | https://langfuse.com/docs/observability/overview | Langfuse LLM Observability & Tracing | Langfuse | 2025 | T4 | verified |
| 14 | https://develop.sentry.dev/sdk/telemetry/traces/modules/ai-agents/ | Sentry AI Agents Module Developer Docs | Sentry | 2025 | T4 | verified |
| 15 | https://blog.langchain.com/debugging-deep-agents-with-langsmith/ | Debugging Deep Agents with LangSmith | LangChain | 2025 | T4 | verified |
| 16 | https://allen.hutchison.org/2026/02/17/the-observability-gap/ | Bridging the Observability Gap in AI Agent Development | Allen Hutchison | 2026 | T5 | verified |

## Findings

### 1. What structured logging and tracing approaches work for LLM agent systems, and how does OpenTelemetry apply?

OpenTelemetry has emerged as the primary vendor-neutral standard for agent observability. The GenAI semantic conventions define a layered attribute namespace (`gen_ai.*`) that covers the full agent execution stack [1][2][3][4]:

**LLM Call Layer.** Individual model invocations are traced as spans with `gen_ai.operation.name` values of `chat` or `text_completion`. Token usage is recorded via `gen_ai.usage.input_tokens` and `gen_ai.usage.output_tokens`. Model identity uses `gen_ai.request.model` (exact model name requested) and `gen_ai.system` (provider). Prompt and completion content can be captured as events, gated by the `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT` environment variable -- making content capture opt-in for privacy and performance reasons [3][4] (HIGH -- T1 sources converge).

**Agent Layer.** Agent invocation spans use `gen_ai.operation.name` of `invoke_agent`, with span name `invoke_agent {gen_ai.agent.name}`. Agent attributes include `gen_ai.agent.id`, `gen_ai.agent.name`, `gen_ai.agent.description`, and `gen_ai.agent.version`. Span kind is CLIENT for cross-process agents, INTERNAL for same-process [2] (HIGH -- T1 source, directly from specification).

**Tool Layer.** Tool execution spans use `execute_tool` with `gen_ai.tool.name`. Sentry's implementation aligns: `gen_ai.execute_tool` as the operation, with span name `execute_tool {gen_ai.tool.name}` [14] (HIGH -- T1 + T4 sources converge).

**Proposed Extensions.** Issue #2664 proposes six additional domains for agentic systems: Tasks, Actions, Agents, Teams, Artifacts, and Memory, with corresponding attribute families (`gen_ai.task.*`, `gen_ai.action.*`, etc.). Only the Tasks spec has been formally submitted; the rest remain pending [5] (MODERATE -- proposal stage, not yet ratified).

**Structured Logging Integration.** Every log entry should carry `trace_id` and `span_id` from request entry, enabling cross-cutting queries. JSON format with fields like `session_id`, `tool_name`, `agent_id`, and correlation IDs. Trace context propagation follows W3C Trace Context (`traceparent` header: `{version}-{trace_id}-{parent_id}-{trace_flags}`) for distributed scenarios [12] (HIGH -- W3C standard, T1).

**Counter-evidence:** The GenAI semantic conventions are still experimental (`OTEL_SEMCONV_STABILITY_OPT_IN` required). OpenInference from Arize AI predates and partially overlaps the OTel GenAI conventions, using its own span-kind taxonomy and attribute schema [8][9]. Vendors may continue shipping proprietary instrumentation alongside OTel support, creating a period of dual-format maintenance.

### 2. How do existing agent frameworks implement "show your work" patterns?

Existing frameworks implement inspectability through four distinct patterns (HIGH -- multiple T4 sources converge):

**Search Protocol Recording.** Logging every search query, source, date range, results found, and results used creates an auditable record of information gathering. The WOS research skill itself implements this pattern with a structured JSON protocol embedded in document comments. This connects directly to provenance: each search entry documents what was looked for, where, and what was selected [11][16].

**Checkpoint Annotations.** LangSmith implements checkpoints for regulated workflows: draft response, human review, publish/reject decision points. State checkpointing persists across infrastructure failures (pod restarts), enabling long-running agent tasks to survive context resets. LangGraph uses state checkpointing with persistence backends for multi-step agent workflows [15] (MODERATE -- single vendor source, but pattern is generalizable).

**Flight Recorder Pattern.** AgentLens exemplifies this: an MCP server that captures every LLM call, tool invocation, approval decision, and error in real-time. Sessions organize events with metadata (agent ID, timestamps, duration, status). Tamper-evident audit trail uses append-only storage with SHA-256 hash chains per session. The "flight recorder" metaphor (from aviation black boxes) captures the idea of continuous, low-overhead recording that is inspected after the fact [10] (MODERATE -- single implementation, but pattern is well-established in other domains).

**ReAct Reasoning Traces.** The ReAct pattern (Reasoning and Acting) generates explicit Thought-Action-Observation traces at each step. The agent records its reasoning (Thought), the action it takes (Action), and what it observes from the environment (Observation). This cycle repeats until task completion, creating a full reasoning transcript. Multiple observability tools (LangSmith, Langfuse, Arize Phoenix) render these traces as visual trees for debugging [13][15][16] (HIGH -- widely adopted pattern across multiple frameworks).

### 3. What trace formats and data models best capture agent reasoning chains and tool invocations?

Three complementary trace format standards have emerged (HIGH -- multiple T1/T4 sources):

**OpenTelemetry GenAI Spans.** The hierarchical span model: a trace (identified by `trace_id`) contains a tree of spans, each with a `span_id` and optional `parent_span_id`. For agent systems, the typical hierarchy is:

```
invoke_agent (root span)
  +-- chat (LLM call to plan)
  +-- execute_tool (tool invocation)
  |   +-- chat (LLM call within tool)
  +-- chat (LLM call to synthesize)
  +-- execute_tool (final tool call)
```

Each span carries typed attributes from the `gen_ai.*` namespace. Span kind (CLIENT vs INTERNAL) indicates whether the operation crosses process boundaries. The W3C Trace Context `traceparent` header propagates context across distributed systems [2][3][12] (HIGH -- T1 standards).

**OpenInference Schema.** Arize AI's OpenInference adds a span-kind taxonomy (`LLM`, `RETRIEVER`, `TOOL`, `AGENT`, `EMBEDDING`, `CHAIN`, `RERANKER`) on top of OTel spans. Attributes use dot-separated namespaces with flattened list indexing: `llm.input_messages.0.message.role`. This provides richer AI-specific typing than base OTel but introduces a parallel attribute vocabulary [8][9] (HIGH -- T4, widely adopted in practice).

**PROV-AGENT Provenance Graph.** For scenarios requiring full accountability, PROV-AGENT extends W3C PROV with AI-specific entity classes: `AIAgent`, `AgentTool`, `AIModelInvocation`, `AIModel`, `Prompt`, `ResponseData`. Relations include `used`, `wasGeneratedBy`, `wasAttributedTo`, `wasInformedBy`, and `wasAssociatedWith`. This creates a directed graph (not just a tree) that can represent complex agent-to-agent interactions, iterative refinement loops, and multi-workflow provenance chains. MCP integration uses decorators (`@flowcept_agent_tool`) and LLM wrappers (`FlowceptLLM`) for automatic capture [11] (MODERATE -- T2 research paper, not yet widely adopted in production).

**Convergence trend:** Sentry's AI Agents module aligns its span operations directly with OTel GenAI conventions (`gen_ai.invoke_agent`, `gen_ai.execute_tool`), and Langfuse supports both OpenInference and OTel formats [13][14]. The industry is converging on OTel GenAI as the base layer, with OpenInference and vendor extensions adding specialized attributes on top.

### 4. What design patterns enable trust and debuggability in agent systems through observability?

Five design patterns emerge from the surveyed literature and tooling (HIGH for patterns 1-3, MODERATE for 4-5):

**Pattern 1: Tiered Content Capture.** Separate metadata tracing (always on, low overhead) from content capture (opt-in, high overhead). OTel implements this with the `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT` toggle. In production, trace structure and metrics flow continuously; prompt/completion content is captured only when debugging or auditing requires it [4] (HIGH).

**Pattern 2: Trace-Correlated Structured Logs.** Every log entry carries `trace_id` and `span_id`, enabling queries that cross-cut between traces (request flow) and logs (detailed events). JSON format with standardized fields (`session_id`, `agent_id`, `tool_name`, `timestamp`, `environment`). This bridges the gap between observability (what happened) and debugging (why it happened) [12][16] (HIGH).

**Pattern 3: Visual Trace Trees.** Render agent execution as expandable trees showing the full path from input to output. LangSmith, Langfuse, and Arize Phoenix all provide this: expand individual steps to see exact prompts and responses, quickly pinpoint error locations, understand tool selection reasoning. This is the primary mechanism by which non-engineers can inspect agent behavior [13][15] (HIGH).

**Pattern 4: Cryptographic Audit Chains.** Append-only event storage with SHA-256 hash chains per session creates tamper-evident records. Each event references the previous event's hash, creating a chain that detects post-hoc modification. AgentLens implements this pattern with SQLite or PostgreSQL backends [10] (MODERATE -- single implementation, protection scope limited to post-hoc tampering).

**Pattern 5: Provenance Graphs.** For full accountability, model agent execution as a provenance graph using W3C PROV extensions. This enables queries that span the traditional trace: "What inputs led to this decision?", "Which model configuration produced this hallucination?", "How did error propagate across agent boundaries?" PROV-AGENT demonstrates this with MCP-aligned tool decorators [11] (MODERATE -- research stage, high potential).

**Counter-evidence:** Traces show what the agent did, not whether its reasoning was sound. Having a complete execution trace can create false confidence -- operators may trust a system more because they can see its steps, even when those steps contain flawed reasoning. Observability enables debugging but does not substitute for evaluation (testing whether the agent produces correct outputs) or alignment verification (testing whether the agent follows intended behaviors). The observability gap described by Hutchison [16] explicitly calls out that operational health metrics, model behavior metrics, data quality metrics, and reasoning traceability must all be present -- traces alone are insufficient.

## Challenge

### Assumptions Check

| Assumption | Supporting Evidence | Counter-Evidence | Impact if False |
|------------|-------------------|------------------|-----------------|
| OpenTelemetry GenAI conventions will become the dominant standard for agent observability | Six T1 sources from OTel project; Datadog, Sentry, Langfuse all adopting OTel conventions; CNCF backing [1][2][3][4][5][6] | Conventions are still experimental; competing specs exist (OpenInference predates OTel GenAI); vendor lock-in incentives may slow adoption [8][9] | If OTel conventions fragment or stall, teams must choose between incompatible vendor-specific schemas, increasing migration cost |
| Trace-span hierarchies are sufficient to capture agent reasoning | Multiple frameworks model agent execution as span trees [2][14][15]; natural mapping from tool calls to child spans | Complex agent patterns (backtracking, parallel hypothesis evaluation, meta-reasoning about strategy) may not map cleanly to tree structures; DAGs or graphs may be needed [5][11] | If tree-structured traces miss important execution patterns, debugging tools built on them will have blind spots for non-linear agent behavior |
| Structured logging with trace correlation is achievable at low overhead | General structured logging adds minimal per-entry overhead; async buffering reduces further; OTel batching is well-established | Agent systems may generate orders of magnitude more log entries than traditional applications (every reasoning step, every token); content capture (prompts/completions) can be very large [4] | If overhead is significant, teams will disable detailed logging in production -- exactly when they need it most |
| Tamper-evident hash chains provide meaningful audit guarantees | AgentLens implements SHA-256 hash chains per session [10]; append-only storage prevents modification | Hash chains only protect against post-hoc tampering; they do not prevent the agent from omitting events during recording; a compromised runtime can simply not log | If the threat model is the agent itself (or its runtime), hash chains are security theater; they only protect against external log modification |

### Premortem

| Failure Reason | Plausibility | Impact on Conclusion |
|----------------|-------------|---------------------|
| Standards fragmentation: OTel GenAI conventions remain experimental while vendors ship incompatible alternatives, creating a multi-standard landscape rather than convergence | Medium | Qualifies finding on OTel as vendor-neutral standard; recommendation should include hedging strategy (use OTel as primary, with adapter pattern for vendor-specific features) |
| Observability overhead kills adoption: detailed agent tracing in production proves too expensive in tokens/latency, so teams only enable it in development where the bugs they need to find don't reproduce | Medium | Qualifies finding on structured logging; recommendation should include tiered logging levels and sampling strategies specific to agent workloads |
| "Show your work" creates false confidence: having a trace of agent reasoning makes operators trust the system more than warranted, because traces show what the agent did but not whether its reasoning was sound | Low | Qualifies finding on trust patterns; recommendation should note that traces enable debugging but don't substitute for evaluation and testing of agent reasoning quality |

## Claims

| # | Claim | Type | Source | Status |
|---|-------|------|--------|--------|
| 1 | OTel GenAI conventions define `invoke_agent` as the operation name for agent invocation spans | attribution | [2] | verified |
| 2 | Agent span attributes include `gen_ai.agent.id`, `gen_ai.agent.name`, `gen_ai.agent.description`, `gen_ai.agent.version` | attribution | [2] | verified |
| 3 | Token usage tracked via `gen_ai.usage.input_tokens` and `gen_ai.usage.output_tokens` | attribution | [3] | verified |
| 4 | Content capture gated by `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT` environment variable | attribution | [4] | verified |
| 5 | Issue #2664 proposes six domains: Tasks, Actions, Agents, Teams, Artifacts, Memory | attribution | [5] | verified |
| 6 | W3C traceparent format: `{version}-{trace-id}-{parent-id}-{trace-flags}` | attribution | [12] | verified |
| 7 | AgentLens uses SHA-256 hash chains per session for tamper-evident audit | attribution | [10] | verified |
| 8 | PROV-AGENT extends W3C PROV with `AIAgent`, `AgentTool`, `AIModelInvocation` entity classes | attribution | [11] | verified |
| 9 | PROV-AGENT uses `@flowcept_agent_tool` decorator for MCP integration | attribution | [11] | verified |
| 10 | Sentry AI Agents module uses `gen_ai.invoke_agent` and `gen_ai.execute_tool` as span operations | attribution | [14] | verified |
| 11 | OpenInference uses `openinference.span.kind` with values like LLM, RETRIEVER, TOOL, AGENT | attribution | [8] | verified |
| 12 | Structured logging adds 0.1-0.5ms per entry overhead | statistic | -- | human-review |

## Key Takeaways

**For WOS and similar plugin-style agent systems:**

1. **Adopt OTel GenAI conventions as the trace schema.** Even without a full OTel collector, structuring internal traces with `gen_ai.*` attributes ensures future compatibility and provides a shared vocabulary for agent operations. The three-layer model (agent invocation, LLM call, tool execution) maps directly to how WOS skills operate.

2. **Implement search protocol recording as a first-class feature.** WOS already does this in the research skill. Generalizing it -- structured JSON logs of every search, every tool call, every decision point -- creates the audit trail that enables both debugging and trust. The pattern is cheap to implement and high-value for post-hoc analysis.

3. **Use tiered content capture.** Always log trace structure (what spans executed, in what order, with what timing). Make content capture (actual prompts, completions, tool arguments) opt-in. This balances observability with performance and privacy.

4. **Checkpoint annotations at phase gates.** WOS research phases already function as checkpoints. Annotating these transitions in the trace (phase entry, gate condition, pass/fail) creates a high-level summary of agent progress that is useful without reading the full trace.

5. **Traces enable debugging, not trust.** Trust requires evaluation (did the agent produce correct outputs?) and alignment verification (did the agent follow intended behaviors?). Observability is necessary but not sufficient. Design systems that combine tracing with automated evaluation, not systems that assume traceability equals trustworthiness.

**Limitations:** This investigation focused on standards and patterns rather than performance benchmarking of specific implementations. The OTel GenAI conventions are experimental and may change. PROV-AGENT is a research prototype, not production tooling. The overhead claim (claim 12) for structured logging is from general logging literature, not agent-specific measurement.

**Follow-ups:** Benchmark trace overhead for agent-scale workloads (thousands of spans per request). Evaluate whether WOS should emit OTel-compatible traces or a lighter-weight internal format. Investigate how checkpoint annotations could integrate with the existing phase-gate workflow in research and plan skills.

## Search Protocol

| Query | Source | Date Range | Found | Used |
|-------|--------|------------|-------|------|
| OpenTelemetry LLM agent observability tracing 2025 2026 | google | 2024-2026 | 10 | 4 |
| structured logging AI agent systems debugging audit trail | google | 2024-2026 | 10 | 3 |
| agent observability show your work LLM transparency trace format | google | 2024-2026 | 10 | 3 |
| OpenTelemetry gen_ai semantic conventions agent spans attributes specification 2025 | google | 2025 | 10 | 3 |
| Langfuse OpenInference agent tracing trace format spans tool calls | google | 2024-2026 | 10 | 2 |
| LangSmith agent trace structure reasoning steps checkpoint debugging | google | 2024-2026 | 10 | 2 |
| Arize Phoenix OpenInference trace model LLM spans attributes schema | google | 2024-2026 | 10 | 2 |
| flight recorder pattern agent observability MCP tool call logging | google | 2024-2026 | 10 | 2 |
| structured JSON logging agent systems search protocol recording best practices | google | 2024-2026 | 10 | 1 |
| Sentry AI agent observability module trace spans tool calls 2025 | google | 2025 | 10 | 1 |
| agent trust debugging chain of thought logging explainability pattern | google | 2024-2026 | 10 | 2 |
| W3C trace context distributed tracing agent systems traceparent format | google | 2024 | 10 | 1 |
| AgentLens MCP flight recorder tamper-evident audit trail | google | 2025 | 10 | 1 |
| OpenTelemetry GenAI events semantic conventions content capture | google | 2025 | 10 | 1 |
| research protocol logging search provenance PROV-AGENT | google | 2025 | 10 | 2 |
| OpenTelemetry gen_ai.agent.id gen_ai.tool.name execute_tool attributes | google | 2025 | 10 | 1 |
| OpenTelemetry gen_ai.usage.input_tokens gen_ai.request.model attributes | google | 2025 | 10 | 1 |

17 searches across 1 source (google), 170 found, 32 used. Sources not searched: IEEE/ACM digital libraries (paywalled), vendor documentation portals requiring authentication, private Slack/Discord communities.
