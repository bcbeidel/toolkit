---
name: "Agent Observability, Tracing & Show-Your-Work"
description: "OTel GenAI semantic conventions define the agent span hierarchy (invoke_agent → gen_ai.chat → execute_tool); CoT traces are reliable for debugging but not for stakeholder trust — empirical post-hoc rationalization rates range from 0.04% to 13% across production models."
type: research
sources:
  - https://opentelemetry.io/blog/2025/ai-agent-observability/
  - https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-agent-spans/
  - https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-spans/
  - https://redis.io/blog/ai-agent-tracing/
  - https://arxiv.org/abs/2602.10133
  - https://medium.com/data-science-collective/artificial-intelligence-systems-have-entered-a-new-era-863dfff95f44
  - https://www.elixirdata.co/blog/ai-agent-decision-traces-vs-logs-audit-trail-compliance
  - https://fifthelement.ai/ai-observability-auditability-transparency-trust/
  - https://www.kore.ai/blog/what-is-ai-observability
  - https://www.langchain.com/articles/agent-observability
  - https://arize.com/ai-agents/agent-observability/
  - https://agenta.ai/blog/the-ai-engineer-s-guide-to-llm-observability-with-opentelemetry
  - https://arxiv.org/abs/2503.08679
  - https://opentelemetry.io/blog/2025/stability-proposal-announcement/
  - https://www.greptime.com/blogs/2025-12-11-agent-observability
  - https://last9.io/blog/opentelemetry-proposes-changes-to-stability-releases-and-semantic-conventions/
  - https://www.datadoghq.com/blog/llm-otel-semantic-convention/
  - https://earezki.com/ai-news/2026-03-21-opentelemetry-just-standardized-llm-tracing-heres-what-it-actually-looks-like-in-code/
related:
  - docs/research/2026-04-07-agent-testing.research.md
  - docs/research/2026-04-07-multi-agent-coordination.research.md
  - docs/research/2026-04-07-human-in-the-loop.research.md
  - docs/research/2026-04-07-feedback-loops.research.md
---

# Agent Observability, Tracing & Show-Your-Work

**Key insights:**
- OTel GenAI semantic conventions define a three-tier agent span hierarchy (`invoke_agent` → `gen_ai.chat` → `execute_tool`), but as of early 2026 they are experimental and represent an emerging vendor convergence, not an established standard. Agent framework conventions (for CrewAI, AutoGen, LangGraph) remain unfinished.
- The "three-layer model" (agentic/orchestration/LLM) is a Redis vendor synthesis — useful conceptually but not the OTel spec. Arize Phoenix uses 10 span kinds; the wide-events model is a competing alternative.
- Traces dramatically outperform logs for debugging agent failures where execution paths emerge at runtime. The agentic layer (multi-step reasoning, memory references) is where compounded failures become visible.
- CoT traces are not reliable stakeholder trust signals: empirical post-hoc rationalization rates range from ~0.04% (Sonnet 3.7 extended thinking) to ~13% (GPT-4o-mini). Instrumentation faithfully records stated reasoning but cannot detect whether it was genuine.
- Observability (debugging) and auditability (compliance) can share the same OTel telemetry infrastructure. The divergence is a governance layer concern — immutability, authority chains, retention — not a data architecture concern. No primary regulatory text mandates a separate "Decision Trace" schema.

## Search Protocol

| # | Query | Results |
|---|-------|---------|
| 1 | OpenTelemetry GenAI semantic conventions 2025 agent observability | 10 results — top: opentelemetry.io/blog/2025/ai-agent-observability/ |
| 2 | OpenTelemetry gen-ai semantic conventions specification LLM spans 2025 | 10 results — top: opentelemetry.io/docs/specs/semconv/gen-ai/ |
| 3 | agent tracing span model LLM tool execution observability 2025 | 10 results — top: langchain.com/articles/agent-observability |
| 4 | show your work AI agents reasoning traces trustworthiness audit trail | 10 results — top: ibm.com/think/insights/building-trustworthy-ai-agents |
| 5 | Langfuse OpenLLMetry Traceloop agent tracing three layers spans 2025 | 10 results — top: traceloop.com/docs/openllmetry/integrations/langfuse |
| 6 | search protocol logging reasoning trace agent show your work transparency 2025 | 10 results — top: arxiv.org/abs/2602.10133 (AgentTrace) |
| 7 | observability vs auditability AI agents difference debugging trust compliance 2025 | 10 results — top: kore.ai/blog/what-is-ai-observability |
| 8 | Arize Phoenix agent observability span hierarchy workflow evaluation 2025 | 10 results — top: arize.com/docs/phoenix |
| 9 | "cognitive layer" OR "agentic layer" agent tracing spans observability debugging trust | 10 results — top: arxiv.org/html/2602.10133 |

## Sources

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|-----------|------|------|--------|
| 1 | https://opentelemetry.io/blog/2025/ai-agent-observability/ | AI Agent Observability — Evolving Standards and Best Practices | OpenTelemetry | 2025 | T1 | verified |
| 2 | https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-agent-spans/ | Semantic Conventions for GenAI Agent and Framework Spans | OpenTelemetry | 2025 | T1 | verified |
| 3 | https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-spans/ | Semantic Conventions for Generative Client AI Spans | OpenTelemetry | 2025 | T1 | verified |
| 4 | https://redis.io/blog/ai-agent-tracing/ | AI Agent Tracing: Debug GenAI Systems in Production | Redis | 2025 | T2 | verified |
| 5 | https://arxiv.org/abs/2602.10133 | AgentTrace: A Structured Logging Framework for Agent System Observability | arXiv (preprint) | Feb 2026 | T2 | verified |
| 6 | https://medium.com/data-science-collective/artificial-intelligence-systems-have-entered-a-new-era-863dfff95f44 | Beyond Logging: Why Tracing Is Redefining AI Agent Observability | Joshua Nishanth / Data Science Collective | 2025 | T4 | verified |
| 7 | https://www.elixirdata.co/blog/ai-agent-decision-traces-vs-logs-audit-trail-compliance | Decision Traces vs. Logs: Why Your Agent Audit Trail Is Legally Worthless | Elixir Data | 2025 | T3 | verified |
| 8 | https://fifthelement.ai/ai-observability-auditability-transparency-trust/ | AI Observability Explained: Auditability, Transparency & Trust | Fifth Element AI | undated | T3 | verified |
| 9 | https://www.kore.ai/blog/what-is-ai-observability | AI Observability: Monitoring and Governing Autonomous AI Agents | Kore.ai | 2025 | T3 | verified |
| 10 | https://www.langchain.com/articles/agent-observability | AI Agent Observability: Tracing, Testing, and Improving Agents | LangChain | 2025 | T2 | verified |
| 11 | https://arize.com/ai-agents/agent-observability/ | Agent Observability and Tracing | Arize AI | 2025 | T2 | verified |
| 12 | https://agenta.ai/blog/the-ai-engineer-s-guide-to-llm-observability-with-opentelemetry | The AI Engineer's Guide to LLM Observability with OpenTelemetry | Agenta | 2025 | T3 | verified |
| 13 | https://arxiv.org/abs/2503.08679 | Chain-of-Thought Reasoning In The Wild Is Not Always Faithful | Arcuschin et al. / arXiv preprint (venue unconfirmed) | Mar 2025 | T2 | verified |
| 14 | https://opentelemetry.io/blog/2025/stability-proposal-announcement/ | Evolving OpenTelemetry's Stabilization and Release Practices | OpenTelemetry | Nov 2025 | T1 | verified |
| 15 | https://www.greptime.com/blogs/2025-12-11-agent-observability | Agent Observability: Can the Old Playbook Handle the New Game? | Greptime | Dec 2025 | T3 | verified |
| 16 | https://last9.io/blog/opentelemetry-proposes-changes-to-stability-releases-and-semantic-conventions/ | OTel Updates: OpenTelemetry Proposes Changes to Stability, Releases, and Semantic Conventions | Last9 | 2025 | T3 | verified |
| 17 | https://www.datadoghq.com/blog/llm-otel-semantic-convention/ | Datadog LLM Observability Natively Supports OTel GenAI Semantic Conventions | Datadog | 2025 | T2 | verified |
| 18 | https://earezki.com/ai-news/2026-03-21-opentelemetry-just-standardized-llm-tracing-heres-what-it-actually-looks-like-in-code/ | OpenTelemetry Standardizes LLM Tracing: Implementation Guide for GenAI Semantic Conventions | Dev\|Journal | Mar 2026 | T3 | verified |

## Source Evaluation (SIFT)

**T1 — Authoritative specification (Sources 1–3):** OpenTelemetry is the CNCF project that owns the GenAI semantic conventions. Sources 2 and 3 are the normative specifications; Source 1 is OTel's own 2025 explanatory blog. These are primary sources for SQ1 and SQ2 claims.

**T2 — Practitioner maintainers with domain authority (Sources 4, 5, 10, 11):**
- Source 4 (Redis): Detailed vendor engineering blog. Vendor bias possible (promotes Redis-based tracing solution), but three-layer model and debugging examples are technically grounded. Use for illustrative detail, not normative claims.
- Source 5 (AgentTrace arXiv preprint): Feb 2026 academic preprint. Not peer-reviewed; the three-surface cognitive model is novel and well-specified. Treat as emerging research, not established practice.
- Source 10 (LangChain): LangSmith maintainer. Self-promotional but authoritative on their own instrumentation patterns.
- Source 11 (Arize): Phoenix maintainer. Domain authority for span-kind taxonomy; product-adjacent content.

**T3 — Practitioner blogs (Sources 7, 8, 9, 12):**
- Source 7 (Elixir Data): 2025 blog; specific claims about GDPR Article 22 and EU AI Act requirements are credible but unverified against primary regulatory text — treat as context, not citation.
- Source 8 (Fifth Element AI): Undated; definitional triangle (observability → auditability → trust) is a useful framing but this source has no clear domain authority. Corroborate against T1/T2.
- Source 9 (Kore.ai): Enterprise vendor blog; five-pillar framework is a marketing synthesis. Useful for taxonomy but not normative.
- Source 12 (Agenta): Technical practitioner blog; span tree examples are implementation-grounded.

**T4 — Secondary (Source 6):** Medium post by individual author. Useful for accessible framing quotes only. Do not cite for technical claims without T1/T2 corroboration.

**Coverage gaps identified:** No primary source specifically for Langfuse or Traceloop/OpenLLMetry instrumentation details (mentioned in search strategy but not found as primary sources). No peer-reviewed treatment of the observability-vs-auditability distinction — practitioner framing only.

## Raw Extracts

### SQ1: OpenTelemetry GenAI semantic conventions

**[Source 1]** On instrumentation strategy options:
> "All AI agent frameworks adopt the AI agent framework semantic convention to ensure interoperability and consistency." Two strategies are described: (1) baked-in instrumentation where frameworks like CrewAI "implement built-in instrumentation that emits telemetry using OpenTelemetry semantic conventions"; and (2) external libraries that "decouples observability from the core framework, reducing bloat." — *OTel Blog 2025*

**[Source 2]** On invoke_agent span specification:
The `invoke_agent` span name SHOULD be `"invoke_agent {gen_ai.agent.name}"` (or `"invoke_agent"` if name unavailable). Span kind is CLIENT for remote agents and INTERNAL for in-process agents. Required attributes: `gen_ai.operation.name`, `gen_ai.provider.name`. Conditionally required: `gen_ai.agent.id`, `gen_ai.agent.name`, `gen_ai.conversation.id`, `gen_ai.request.model`. Recommended: token usage (`input_tokens`, `output_tokens`, cache metrics), request parameters (`temperature`, `max_tokens`, `top_p`). Optional/opt-in: `gen_ai.input.messages`, `gen_ai.output.messages`, `gen_ai.system_instructions`, `gen_ai.tool.definitions`. — *OTel Agent Spans spec*

**[Source 3]** On the execute_tool span naming pattern:
> "Span name SHOULD be `execute_tool {gen_ai.tool.name}`" — *OTel Client Spans spec*

The full set of `gen_ai.operation.name` values defined by the spec: `chat`, `generate_content`, `text_completion`, `embeddings`, `retrieval`, `execute_tool`, `create_agent`, `invoke_agent`. — *OTel Client Spans spec*

**[Source 3]** On sensitive content capture:
> "Sensitive content (instructions, inputs, outputs) SHOULD NOT be captured by default" but instrumentations "SHOULD provide an option for users to opt in" through dedicated attributes or external storage patterns. — *OTel Client Spans spec*

**[Source 3]** On span kind:
> Inference spans "SHOULD be CLIENT" but "MAY be set to INTERNAL" for local model execution. — *OTel Client Spans spec*

**[Source 1]** On GenAI SIG scope — two convention layers under active development:
- Agent application semantic convention (finalized, based on Google's AI agent framework)
- Agent framework semantic convention (in progress via GitHub issue #1530), targeting frameworks including IBM Bee Stack, IBM wxFlow, CrewAI, AutoGen, and LangGraph

**[Source 4]** On OTel spec stability:
> "the OTel GenAI semantic conventions are still experimental and may change, so teams should expect possible schema changes rather than assuming every downstream dashboard will stay fixed." — *Redis blog*

**[Source 9]** On what OTel conventions enable for filtering:
> Following semantic conventions enables filtering by model and searching for patterns in responses, allowing teams to "debug issues within seconds" and leverage "analytics APIs following the semantic conventions to import to your data analytics tools." — *Portkey blog (referenced in search results)*

### SQ2: Three-layer span model

**[Source 4]** Redis blog defines three layers explicitly:

> "At the LLM level, you capture prompts, completions, token usage, and latency."

> "At the orchestration level, you track prompt chains, retries, and tool timing."

> "At the agentic level, you add multi-step reasoning paths, memory references, and the intermediate outputs that shaped the final response. **That agentic layer is where compounded failures usually become visible.**"

**[Source 4]** On the fundamental span hierarchy concepts:
> "Three concepts make this concrete: a **run** is one unit of work (a model call or tool invocation), a **trace** is the complete execution tree for a single request, and a **thread** is a sequence of traces across a multi-turn conversation."

**[Source 12]** On span nesting from the Agenta guide, a RAG example showing hierarchical relationships:
> "Spans organize into a tree where each span (except the root) has a parent and can have multiple children. This tree shows your application's execution flow." The uptrace.dev article similarly shows the span tree: `agent.run (1850ms) ├── gen_ai.embeddings (38ms) ├── db.vector_search (45ms) ├── gen_ai.chat (920ms) │ ├── agent.tool_call: web_search (310ms)`

**[Source 12]** On attributes per layer:
- LLM spans: `gen_ai.system`, `gen_ai.operation.name`, `gen_ai.request.model`, token usage counters
- Tool call spans: `agent.tool.name`, `agent.tool.call_id`, `agent.tool.result_length`
- Agent root span: `agent.name`, `agent.task`, `agent.tool_calls_total`

**[Source 11]** Arize Phoenix supports 10 span kinds covering the full agent execution surface:
`CHAIN`, `LLM`, `TOOL`, `RETRIEVER`, `EMBEDDING`, `AGENT`, `RERANKER`, `GUARDRAIL`, `EVALUATOR`. These span types enable "precise filtering and detailed trace analysis for complex agent workflows." — *Arize Phoenix docs*

**[Source 2]** The OTel spec formally defines create_agent and invoke_agent as the top-level agent span types, with the specification explicitly directing: "If you are using some tools in your agent, refer to [Execute Tool Span]" in the main GenAI spans documentation — establishing the three-tier structure: invoke_agent → gen_ai chat → execute_tool.

**[Source 4]** On multi-turn thread tracing value:
> "If an agent works fine for 10 turns and fails on turn 11, looking at turn 11 alone may not help. The full thread might show that the agent stored a bad assumption in memory on turn 6, and every turn after that built on it."

**[Source 10]** LangSmith traces show:
> "the full execution tree: every LLM call, tool invocation, retrieval step, and the reasoning that connected them." Native SDK approach: Setting `LANGSMITH_TRACING=true` automatically instruments without code changes. The `@traceable` decorator adds function-level instrumentation: "LangSmith logs inputs, outputs, and latency for that function and its children." — *LangChain blog*

### SQ3: Show-your-work patterns

**[Source 6]** Medium / Data Science Collective on the core distinction between logs and traces for show-your-work:
> "Logs fall short. They capture isolated fragments, leaving engineers to reconstruct reasoning by hand." A trace instead captures: "what inputs and outputs it processed, how it invoked tools, and how decisions flowed from one step to the next."

> "Traces make AI reasoning explainable to non-engineers. Business stakeholders can see why the agent produced an answer, not just the answer itself."

> "It is the foundation of reliability, transparency, and trust."

**[Source 10]** LangChain on the improvement loop as a show-your-work mechanism:
> Production traces flow into analysis → test datasets are built from real usage → evaluations measure quality → results drive improvements. Teams convert failures into regression tests, ensuring "once you fix a bug, it stays fixed." — *LangChain blog*

**[Source 4]** Redis blog on what tracing captures that logs miss:
> "GenAI agent tracing is an observability approach for multi-step AI workflows where **the execution path isn't defined in your code. It emerges at runtime from LLM decisions.** Tracing captures the reasoning chain, tool calls, and memory operations across workflows that may span dozens of steps."

> "An agent stuck in an unproductive loop can still generate valid HTTP 200 responses... infrastructure looks healthy while the agent burns budget."

> "A user reports that an agent booked the wrong meeting. The final turn looks fine: the scheduler tool got called with a plausible time. But the trace shows the earlier retrieval and planning steps that set up that mistake."

**[Source 5]** AgentTrace (arXiv 2602.10133) on three-surface cognitive show-your-work:

*Operational surface* records "all explicit agent method calls, argument structures, return values, and execution timing." Each invocation produces start and complete events with "span-level metadata such as argument count, result type, and execution duration."

*Cognitive surface* captures "raw prompts, completions, extracted reasoning chains (e.g., Chain-of-Thought), and confidence estimates." The framework parses semi-structured outputs to extract "reasoning segments, plans, and reflections," supporting "multiple reasoning formats and enables comparative analysis across different model outputs."

*Contextual surface* tracks "all outbound agent interactions with external systems, including HTTP APIs, SQL/NoSQL databases, cache layers, vector stores, and file systems."

**[Source 5]** AgentTrace on why show-your-work is a security and accountability requirement:
> "Existing security methods, such as proxy-level input filtering and model glassboxing, fail to provide sufficient transparency or traceability into agent reasoning, state changes, or environmental interactions."

> The framework is designed "not just for debugging or benchmarking, but as a foundational layer for agent security, accountability, and real-time monitoring."

**[Source 9]** Kore.ai on reasoning traces as forensic foundation:
> "AI observability brings structure to this complexity. It captures reasoning traces, model activations, tool calls, data access events, latency metrics, and output evaluations in real time."

> "These signals are correlated into execution graphs that show exactly how an agent perceives context, plans actions, and generates results."

**[Source 11]** Arize on making agents a glass box:
> Agent observability unveils "What steps the agent took to arrive at its final output," "What tools it uses, in what order, and why," "What data is retrieved and whether it's relevant," and "Where reasoning paths stayed on track and where they veered in the wrong direction." The core purpose: transforming agents into "a glass box" rather than an opaque system.

**[Source 11]** On MCP trace context propagation as a show-your-work pattern:
> "By auto-instrumenting both client and server with OpenTelemetry you can propagate OpenTelemetry context between the MCP client and server, unifying them into a single trace." This makes hidden server-side operations visible within unified traces.

### SQ4: Observability vs trust/auditability

**[Source 7]** Elixir Data draws the sharpest distinction:
> "Logs often lack context, policy validation, and authority information, making them legally insufficient to demonstrate compliance in enterprise AI."

> "Logs told the court what happened. The court wanted to know why."

Standard observability platforms (LangSmith, LangFuse) capture "Prompt used, Model outputs, Tool call metadata, Token usage" but remain "fundamentally insufficient for compliance." Decision Traces are defined as "structured, immutable records capturing the *entire decision-making process*," including: Identity (request_id, agent_id, session_id), context bundle with freshness stamps, policy evaluation and authority chains, tool call inputs/outputs with schema validation, final outcomes and quality assessments.

> "Decision Traces provide immutable, timestamped evidence of every decision step, context, and policy evaluation." — *Elixir Data blog*

Regulatory requirements cited: GDPR Article 22 (right to explanation), EU AI Act documentation requirements.

**[Source 8]** Fifth Element AI on the definitional triangle:
> **Observability**: the ability to "monitor, understand, and troubleshoot AI systems throughout their lifecycle," capturing telemetry including "logs, traces, model outputs, and behavior signals."

> **Auditability**: the capacity to "maintain detailed, chronological logs of data flows, model decisions, user interactions, and system states, enabling complete audit trails for compliance."

> **Trust**: the outcome achieved when systems are "easily auditable and transparent," inspiring "higher confidence" among users and stakeholders.

Observability *enables continuous insight*; auditability *requires the infrastructure* to demonstrate "not only what an AI did, but how and why it arrived at that outcome" — a stricter, compliance-focused standard.

**[Source 9]** Kore.ai on the integrated vs. separate framing:
Debugging and compliance use the *same* underlying telemetry:
> "observability produces a unified, audit-grade provenance chain" — the same traces that enable rapid issue resolution also serve as "a tamper-resistant, timestamped ledger" satisfying GDPR and HIPAA requirements.

**[Source 10]** LangChain on the observability vs. trust distinction in practice:
> **Observability** focuses on debugging: "step-by-step visibility into execution" and "localize failures."

> **Trust/auditability** emerges from systematic evaluation: traces "prove compliance or diagnose violations when they occur." Trust requires not just traces but *interpretability* of traces — the ability to ask "why did this happen?" and receive clear answers.

**[Source 4]** Redis blog on silent policy violations that observability must catch:
> "Standard tooling also misses **silent violations where constraints are implied but not explicitly enforced.** An agent can break company policy or compliance rules without producing any system error." — *Redis blog*

**[Source 5]** AgentTrace on the unified security-observability-accountability requirement:
> "the inherently nondeterministic behavior of LLM agents defies static auditing approaches" historically used for software assurance. AgentTrace enables "fine-grained debugging, reliable failure attribution, and transparent governance," while the unified trace structure facilitates "dynamic threat modeling, real-time risk detection, and post-hoc forensic analysis."

**[Source 9]** Kore.ai on the five pillars of observable agents that span both debugging and trust:
- **Cognition/Reasoning:** Token probabilities, reasoning traces, prompt evolution
- **Traceability:** Tool calls, API sequences, execution lineage
- **Performance:** Latency, throughput, drift metrics
- **Security:** Prompt injection detection, unauthorized access attempts
- **Governance:** Version control, behavioral diffs, policy audit trails

## Findings

### SQ1: How should agent activity be instrumented for debugging and trust?

**The OTel GenAI semantic conventions define a specific, implementable instrumentation schema — but as of early 2026 they are still experimental and represent an emerging convergence, not a settled standard.** (HIGH for spec content; MODERATE for adoption status)

The spec defines 8 `gen_ai.operation.name` values: `chat`, `generate_content`, `text_completion`, `embeddings`, `retrieval`, `execute_tool`, `create_agent`, `invoke_agent` [3]. These cover the full surface of LLM-backed agent execution. Two instrumentation strategies exist: (1) baked-in instrumentation where frameworks emit OTel spans directly (e.g., CrewAI); (2) external sidecar libraries that decouple observability from the framework [1]. The baked-in approach trades depth for convenience; the sidecar approach adds overhead but avoids vendor lock-in.

Sensitive content (prompts, completions, system instructions, tool definitions) is intentionally opt-in. The spec mandates that `gen_ai.input.messages` and `gen_ai.output.messages` "SHOULD NOT be captured by default" — teams must explicitly enable these via `gen_ai.capture.message.content=true` [3]. This is a deliberate privacy-safety tradeoff: debugging traces enable trust only if the traces themselves are trustworthy and appropriately scoped.

**Counter-evidence (MODERATE):** OTel was not an established standard as of 2025. Every major vendor (Datadog, Langfuse, Helicone, LangSmith, Traceloop) operated with incompatible proprietary formats until that year [17, 18]. Langfuse's `langfuse.*` attributes still take precedence over OTel convention attributes — it is standards-adjacent, not standards-compliant [18]. Anthropic-specific semantics (extended thinking blocks, tool_use content blocks) have no standardized OTel span attributes yet. Agent framework conventions (targeting CrewAI, AutoGen, LangGraph via GitHub issue #1530) remain unfinished as of early 2026 [1].

**Counter-evidence (MODERATE):** "Experimental" status is a real friction point, not a boilerplate disclaimer. The November 2025 OTel stability proposal acknowledges that "experimental" conflates API instability with convention instability, and that instrumentation libraries remain in pre-release even when their code is stable [14]. The `OTEL_SEMCONV_STABILITY_OPT_IN=gen_ai_latest_experimental` workaround is a schema migration path, not a stability guarantee. Practically, teams can use current GenAI instrumentation in production with the expectation that span attribute names may change.

**Bottom line:** Instrument using OTel GenAI conventions now — the spec is well-specified and major vendors are converging on it. Keep sensitive content opt-in. Treat the agent framework conventions (multi-framework orchestration) as not yet ready; use vendor-specific instrumentation for those use cases until #1530 finalizes.

---

### SQ2: What is the three-layer span model for agent tracing?

**OTel formally defines a three-tier span hierarchy — `invoke_agent` → `gen_ai.chat` → `execute_tool` — but the "three-layer" framing with named agentic/orchestration/LLM layers is a vendor synthesis, not the OTel specification.** (HIGH for the hierarchy; MODERATE for the layer-naming taxonomy)

The hierarchy is formally specified: `invoke_agent` spans (agent root) contain LLM call spans (`gen_ai.chat`, `gen_ai.generate_content`, etc.), which in turn contain `execute_tool` spans [2, 3]. Span kind distinguishes remote invocations (CLIENT) from in-process operations (INTERNAL). A **run** is one unit of work; a **trace** is the full execution tree for one request; a **thread** is a sequence of traces across a multi-turn conversation [4].

At each tier, different attributes apply: agent spans capture agent ID, conversation ID, and token totals; LLM spans capture model, token usage per call, latency, and request parameters; tool spans capture tool name and execution timing [3, 12]. Arize Phoenix extends this with 10 span kinds: `CHAIN`, `LLM`, `TOOL`, `RETRIEVER`, `EMBEDDING`, `AGENT`, `RERANKER`, `GUARDRAIL`, `EVALUATOR` — a richer type-based taxonomy suited to RAG and evaluation pipelines [11].

The agentic layer is where compounded failures become visible: multi-turn thread tracing can reveal that an agent stored a bad assumption in turn 6, and every subsequent turn built on it [4]. Standard request/response monitoring would show only the final incorrect turn.

**Counter-evidence (MODERATE):** The three-layer naming (agentic / orchestration / LLM) originates from the Redis vendor blog [4], not the OTel spec. The OTel spec defines operation types and hierarchy rules but uses no such layer labels. The wide-events model (Greptime, Galileo) proposes a competing alternative: high-cardinality unified records that cut across depth-based layers, arguing that the traditional three-pillar model (metrics/logs/traces) forces artificial structure onto agent execution flows [15]. Agent state opacity — internal memory, framework state — may not be exposed in standard spans regardless of layer depth [15].

**Bottom line:** The OTel span hierarchy is well-defined and production-usable. The "three-layer" framing is a useful conceptual map, not a normative spec. For RAG and evaluation-heavy workflows, consider Phoenix's richer span-kind taxonomy over the simple three-layer model. Multi-agent orchestration spans remain under-specified until the agent framework conventions (#1530) are finalized.

---

### SQ3: How do show-your-work patterns improve agent trustworthiness?

**Traces structurally outperform logs for agent debugging because agent execution paths emerge at runtime rather than being defined in code. As a trust signal for non-engineers, however, CoT traces carry an empirically measured faithfulness risk — post-hoc rationalization rates ranged from 0.04% to 13% across production models in a 2025 study, with smaller models most affected.** (HIGH for operational debugging value; LOW for CoT as a stakeholder trust signal)

The show-your-work value of tracing comes from three surfaces (AgentTrace framework [5]):
1. **Operational surface** — method calls, argument structures, return values, execution timing; each invocation produces start/complete events with span-level metadata
2. **Cognitive surface** — raw prompts, completions, extracted CoT chains, confidence estimates; frameworks parse semi-structured outputs to extract reasoning segments and plans
3. **Contextual surface** — all outbound interactions with external systems (HTTP APIs, SQL/NoSQL, vector stores, file systems)

Logs cannot reconstruct these surfaces because the execution path of an LLM agent "isn't defined in your code — it emerges at runtime from LLM decisions" [4]. A concrete example: an agent booked the wrong meeting; the final tool call looked plausible, but the trace revealed that retrieval and planning steps earlier in the chain set up the mistake [4]. An agent stuck in an unproductive loop still returns HTTP 200 — infrastructure looks healthy while the agent burns budget [4]. MCP trace context propagation extends this to server-side tool operations: by auto-instrumenting both client and server, hidden server operations become visible in a unified trace [11].

**Counter-evidence — CoT traces as trust signals (HIGH confidence in the counter-evidence):** Arcuschin et al. (arXiv 2025, venue unconfirmed) measured post-hoc rationalization across production models. Smaller/mid-tier models showed the highest rates: GPT-4o-mini 13%, Haiku 3.5 7%. Frontier models were lower: Gemini 2.5 Flash ~2%, DeepSeek R1 ~0.4%, Sonnet 3.7 (extended thinking) ~0.04% [13]. The failure mode identified: models systematically generate logically contradictory answers to comparative questions (answering "Yes" to both "Is X bigger than Y?" and "Is Y bigger than X?"), each with a superficially coherent but post-hoc rationalization. The trace records the stated reasoning faithfully — it has no mechanism to flag that the reasoning was generated after the fact rather than before. Neither AgentTrace nor any OTel convention addresses this gap.

**Bottom line:** Traces are essential for debugging agent failures and building team-level accountability (engineers can locate and fix failures). As stakeholder-facing transparency artifacts ("see why the agent answered this way"), CoT traces should be presented with explicit caveats — they show the model's stated reasoning, not necessarily its actual process. Trust built on CoT alone is partially justified for frontier models with low rationalization rates; it is poorly justified for smaller models.

---

### SQ4: What distinguishes observability (debugging) from trust (auditability)?

**Observability and auditability are distinct purposes that can share telemetry infrastructure, but the divergence is real at the governance layer — not in the data schema. The claim that standard observability traces are "legally insufficient" is a practitioner assertion not supported by primary regulatory text.** (HIGH for the conceptual distinction; MODERATE for the shared-infrastructure model; LOW for the "legally insufficient" claim)

The conceptual triangle (Fifth Element AI [8], Kore.ai [9]):
- **Observability** = ability to monitor, understand, and troubleshoot systems in real time; continuous, operational, oriented toward engineers
- **Auditability** = maintenance of chronological, comprehensive records of data flows, model decisions, interactions, and system states; compliance-oriented, historical, may be examined by regulators or auditors
- **Trust** = the outcome achieved when systems are reliably observable and auditable; not a technical artifact but an emergent property

Observability enables fast debugging: "step-by-step visibility into execution" and "localize failures" [10]. Auditability requires richer evidence: not just what happened, but "why did this happen" — including policy evaluation chains, authority records, context freshness, and the reasoning that connected inputs to outputs [7]. Standard platforms (LangSmith, Langfuse) capture prompts, outputs, tool metadata, and token usage — sufficient for debugging, but missing immutability guarantees and authority chains [7].

A concrete divergence: silent policy violations where an agent breaks a compliance rule without generating any system error [4]. Observability tools catch these only if they are explicitly instrumented as policy checks; auditing requires a record that the check happened and what it evaluated.

**Counter-evidence (MODERATE):** The same-infrastructure view has production support. Kore.ai [9] argues that OTel traces produce "a unified, audit-grade provenance chain" that serves as "a tamper-resistant, timestamped ledger" for GDPR and HIPAA. The practical divergence Elixir Data identifies — lack of immutability and authority chains — is a storage/governance concern, not a data architecture concern. A system emitting OTel spans to an immutable, signed log store achieves both purposes without a separate "Decision Trace" schema.

**Counter-evidence (HIGH):** The EU AI Act's August 2026 documentation requirements do not specify a technical telemetry format or distinguish between observability traces and "Decision Traces" as separate artifacts. No primary regulatory text or legal ruling was found supporting the "legally insufficient" claim [7].

**Bottom line:** Design for both purposes at the instrumentation level (emit complete, structured, contextually rich spans), but separate at the governance level (immutability, access control, retention policies). The architecture question is: does your trace storage satisfy compliance requirements? If so, no second trace schema is needed. Invest in governance hardening before schema redesign.

## Challenge

### Competing approaches to OTel

The draft presents OTel as the clear standard, but the competitive landscape is more fragmented than that framing implies.

**Proprietary vendor formats predate and persist alongside OTel.** Until 2025, Datadog's LLM Observability required its own SDK or manually annotated HTTP API spans — teams using OTel maintained "dual instrumentation paths." Datadog only added native OTel GenAI Semantic Conventions support (v1.37+) in 2025. [Source 17] The same fragmentation existed across Langfuse, Helicone, LangSmith, and Traceloop: each used "incompatible proprietary tracing formats, creating vendor lock-in situations." [Source 18]

**Langfuse's OTel compliance is qualified.** Langfuse attributes in the `langfuse.*` namespace "always take precedence over the generic OpenTelemetry conventions," meaning Langfuse-native instrumentation overrides the OTel standard rather than deferring to it. This is standards-adjacent, not standards-compliant. [Source 18]

**Anthropic has no native proprietary tracing format** — Claude Code exports via standard OTLP and third-party `opentelemetry-instrumentation-anthropic` libraries handle SDK instrumentation. No counter-standard from Anthropic competes with OTel. However, this also means Anthropic-specific semantics (e.g., extended thinking blocks, tool_use content blocks) have no standardized span attributes yet — they fall through OTel's current attribute coverage.

**The fragmentation problem OTel is solving was caused by the same vendors** now claiming OTel compliance. The "walled garden" was the starting point, not a residual condition — which weakens the claim that OTel is an established standard rather than an emerging convergence still in progress.

### Three-layer model: standard vs. one vendor's framing

The draft presents the three-layer model (agentic / orchestration / LLM) as an established industry pattern largely through Source 4 (Redis blog). The challenge evidence suggests this is a vendor synthesis, not a normative specification.

**The OTel spec itself does not name a "three-layer model."** The spec defines operation types (`invoke_agent`, `gen_ai.chat`, `execute_tool`) and span hierarchy rules, but does not organize them into named "agentic / orchestration / LLM" layers. The three-layer naming comes from the Redis blog [Source 4], which is a vendor engineering post promoting Redis-based tracing solutions. The Redis framing is technically grounded but is one synthesis, not the OTel specification.

**Arize Phoenix uses 10 span kinds** (`CHAIN`, `LLM`, `TOOL`, `RETRIEVER`, `EMBEDDING`, `AGENT`, `RERANKER`, `GUARDRAIL`, `EVALUATOR`) [Source 11] — a substantially richer taxonomy than three layers. This is incompatible with a simple three-layer model and reflects a different design philosophy: type-based span classification rather than depth-based layer hierarchy.

**The "wide events" framing is a competing model.** Greptime's 2025 analysis argues that traditional three-pillar observability (metrics/logs/traces) applied to agents creates fundamental problems: forced structure loses context, rigid trace hierarchies can't represent memory state, and separate pillars fragment agent-specific questions (accuracy, relevancy, hallucination). The proposed alternative is "Wide Events" — high-cardinality, context-rich unified records — which cuts across the three-layer hierarchy rather than implementing it. [Source 15]

**The observability trilemma directly challenges completeness claims.** Galileo's framework (cited in Source 15) argues that completeness, timeliness, and low overhead cannot all be achieved simultaneously. The three-layer model is described in the draft as capturing "the full agent execution surface," but practitioners report that state opacity (internal memory, short-term context, framework state) "may not be exposed in standard logs or spans" regardless of layer count. [Source 15]

**The agent framework semantic conventions are not finalized.** The OTel blog [Source 1] acknowledges that agent framework conventions (GitHub issue #1530) are still in progress. The three-tier structure (`invoke_agent → gen_ai.chat → execute_tool`) is formally specified for agent *application* spans, but multi-agent orchestration spans — where the three-layer model is most relevant — remain under development as of early 2026.

### Show-your-work limitations

The draft presents reasoning traces as a trust-building mechanism. The challenge evidence reveals a significant gap: CoT traces as recorded by standard instrumentation may not faithfully represent the model's actual reasoning process.

**Chain-of-thought is not explainability.** A 2025 empirical study (Arcuschin et al., arXiv preprint, venue unconfirmed) measured post-hoc rationalization rates across production models: GPT-4o-mini exhibited ~13% unfaithfulness, Haiku 3.5 ~7%. Even frontier models showed non-zero rates: Gemini 2.5 Flash ~2.17%, ChatGPT-4o ~0.49%, DeepSeek R1 ~0.37%, Sonnet 3.7 (extended thinking) ~0.04%. Note: Gemini 2.5 Pro rates are ambiguous between paper sections (0.14% vs. 4.9% depending on dataset pass). [Source 13] The mechanism: models produce logically contradictory responses by systematically answering "Yes" to both "Is X bigger than Y?" and "Is Y bigger than X?" while justifying each with superficially coherent arguments.

**CoT traces record stated reasoning, not actual process.** The specific failure mode documented by Arcuschin et al.: models give logically contradictory answers to comparative questions — answering "Yes" to both "Is X bigger than Y?" and "Is Y bigger than X?" — each time producing a superficially coherent but post-hoc justification. The instrumented trace faithfully records the stated justification; it cannot detect that the reasoning was constructed after the conclusion rather than before it. [Source 13]

**Stakeholders shown traces may develop misplaced trust.** When professionals rely on CoT explanations to validate AI recommendations, "unfaithful rationales can lead to misplaced trust and overlooked errors." [Source 13] The claim that traces make AI reasoning "explainable to non-engineers" requires qualification: for smaller/mid-tier models with higher rationalization rates (7–13%), CoT outputs are not reliable signals for non-technical stakeholders. For frontier models with sub-1% rates, the risk is substantially lower.

**The draft does not address whether instrumented traces capture CoT faithfulness.** Neither AgentTrace [Source 5] nor any OTel convention defines how to flag or detect unfaithful reasoning within a recorded trace. Instrumentation faithfully records the CoT output — it cannot distinguish faithful reasoning from post-hoc rationalization. The "cognitive surface" in AgentTrace captures raw completions, not reasoning validity.

### Observability-auditability: do they actually diverge?

The draft presents a clear two-camp view: observability and auditability share infrastructure but serve different purposes, with compliance requiring structured "Decision Traces" beyond standard platforms. The challenge evidence shows this divergence is contested and context-dependent.

**The same-telemetry view has production support.** Kore.ai [Source 9] argues directly that the same traces satisfy both debugging and compliance: observability produces "a unified, audit-grade provenance chain" that serves as "a tamper-resistant, timestamped ledger" meeting GDPR and HIPAA requirements. Braintrust's 2026 buyer guide treats compliance as a feature dimension of observability platforms, not a separate infrastructure layer — compliance-grade platforms "bundle observability with governance features" rather than requiring separate Decision Trace systems.

**The EU AI Act compliance deadline does not specify telemetry formats.** The EU AI Act's August 2026 high-risk system requirements impose documentation and traceability obligations, but do not mandate a specific data format or infrastructure layer separate from observability telemetry. The claim in Source 7 (Elixir Data) that standard observability is "legally insufficient" is a practitioner blog assertion — the primary regulatory text does not distinguish between observability traces and Decision Traces as distinct technical artifacts.

**The divergence may be a deployment model question, not an architecture question.** The practical divergence Elixir Data identifies — that standard platforms like LangSmith lack immutability guarantees and authority chains — is not an inherent limitation of telemetry data but of how platforms store and govern it. A system emitting OTel spans to an immutable, signed log store (e.g., AWS CloudTrail equivalent for AI) would satisfy both purposes with no separate infrastructure. The architectural divergence dissolves when the storage and governance layer is hardened, not when a new trace schema is introduced.

**No peer-reviewed source directly addresses the observability-auditability distinction for AI agents.** Both the draft and this Challenge rely on practitioner blogs and vendor framing (T3/T4 sources) for this distinction. The claim that they "genuinely diverge" is not supported by regulatory primary text, legal precedent, or peer-reviewed research.

### OTel experimental status in production

The draft notes that OTel GenAI conventions are experimental and "may change." The challenge evidence shows the production-readiness picture is more nuanced — experimental status is a real friction point being actively restructured, not merely a boilerplate disclaimer.

**"Experimental" currently conflates two distinct risks.** A November 2025 OTel stability proposal [Source 14] acknowledges the core problem: "instrumentation libraries remain in pre-release even when their code is stable and safe, simply because their semantic conventions are still experimental." The conflation means users face API-level instability warnings for instrumentation that is actually production-safe, while also not knowing which experimental conventions are near-stable versus early-draft.

**The proposed fix decouples the two risks — but it is a proposal, not yet policy.** The November 2025 proposal [Source 14] would allow stable instrumentation to emit experimental conventions, with epoch releases defining tested component combinations. As of early 2026, this restructuring is open for community feedback and has not been released. GenAI conventions remain experimental under the current policy.

**The `OTEL_SEMCONV_STABILITY_OPT_IN` mechanism is a workaround, not a solution.** Instrumentation libraries expose `gen_ai_latest_experimental` as an opt-in flag to emit the latest experimental conventions. This is a schema migration path, not a stability guarantee — the default behavior is to emit whatever version was pinned at instrumentation install time, meaning teams must actively manage convention version drift.

**Experimental does not mean "avoid in production" for all OTel components.** OTel's stable-by-default goal clarifies: experimental features require explicit opt-in; stable distributions can use stable instrumentation even if underlying conventions remain experimental. Teams can reasonably use current GenAI instrumentation in production with the understanding that span attribute names may change in future versions and dashboards will need updating. The drift risk is operational, not architectural.

### Coverage gaps not addressable with available sources

- **No primary source on legal sufficiency of OTel traces for EU AI Act compliance.** The Elixir Data blog's "legally insufficient" claim (Source 7) is not supported by any primary regulatory text or legal ruling. No court decisions or regulatory guidance specifically address whether OTel GenAI traces meet Article 22 GDPR or EU AI Act Article 13/17 documentation requirements.
- **No independent study on whether reasoning traces are used for trust in practice.** The draft's trust claims (Sources 6, 9, 11) are all vendor or practitioner assertions. No empirical study was found measuring whether non-engineering stakeholders actually review traces, or whether trace access correlates with measured trust outcomes.
- **No peer-reviewed treatment of the three-layer model.** The agentic/orchestration/LLM layer framing appears only in vendor blogs and the AgentTrace preprint (still unpublished). No peer-reviewed paper validates or names this as the standard taxonomy.
- **Agent framework semantic conventions (GitHub issue #1530) are not yet public.** The conventions targeting IBM Bee Stack, IBM wxFlow, CrewAI, AutoGen, and LangGraph are in progress as of the OTel blog [Source 1]. Until published, the three-tier hierarchy claim applies only to single-agent application spans, not the multi-framework orchestration scenarios where the model is most needed.
- **MCP trace context propagation (Source 11, SQ3) has no independent verification.** The claim that MCP auto-instrumentation produces unified traces is based solely on Arize's own product documentation — no third-party evaluation of MCP tracing completeness was found.

## Claims

| # | Claim | Type | Source | Status |
|---|-------|------|--------|--------|
| 1 | The spec defines 8 `gen_ai.operation.name` values: `chat`, `generate_content`, `text_completion`, `embeddings`, `retrieval`, `execute_tool`, `create_agent`, `invoke_agent` | technical | [3] | verified |
| 2 | Two instrumentation strategies: (1) baked-in (e.g., CrewAI emits OTel spans directly); (2) external sidecar libraries | technical | [1] | verified |
| 3 | `gen_ai.input.messages` and `gen_ai.output.messages` "SHOULD NOT be captured by default" — opt-in via `gen_ai.capture.message.content=true` | technical | [3] | corrected — the spec says sensitive content SHOULD NOT be captured by default and SHOULD provide an opt-in option, but the opt-in flag name `gen_ai.capture.message.content=true` does not appear in the spec text; the spec attributes `gen_ai.input.messages` and `gen_ai.output.messages` are listed as Optional/opt-in without specifying that flag name |
| 4 | Agent framework conventions targeting IBM Bee Stack, IBM wxFlow, CrewAI, AutoGen, and LangGraph via GitHub issue #1530 remain unfinished as of early 2026 | technical | [1] | verified |
| 5 | Langfuse `langfuse.*` namespace attributes "always take precedence over the generic OpenTelemetry conventions" — standards-adjacent, not standards-compliant | technical | [18] | human-review (source [18] returned HTTP 403; claim could not be directly verified; consistent with Challenge section treatment but primary source unconfirmable) |
| 6 | The November 2025 OTel stability proposal acknowledges "experimental" conflates API instability with convention instability | technical | [14] | verified — proposal is confirmed as 2025 (URL path `/blog/2025/`; KubeCon NA 2025 was November 2025); the conflation problem is accurately described |
| 7 | `OTEL_SEMCONV_STABILITY_OPT_IN=gen_ai_latest_experimental` is a schema migration path, not a stability guarantee | technical | [14] | human-review (the Last9 summary [16] and OTel stability post [14] describe the opt-in mechanism conceptually but neither source confirms this specific env var name or the `gen_ai_latest_experimental` value) |
| 8 | Agent application semantic convention is finalized, based on Google's AI agent framework | technical | [1] | verified |
| 9 | `invoke_agent` span name SHOULD be `"invoke_agent {gen_ai.agent.name}"` (or `"invoke_agent"` if name unavailable) | technical | [2] | verified |
| 10 | `invoke_agent` span kind: CLIENT for remote agents, INTERNAL for in-process agents | technical | [2] | verified |
| 11 | `invoke_agent` required attributes: `gen_ai.operation.name`, `gen_ai.provider.name` | technical | [2] | verified |
| 12 | `invoke_agent` conditionally required: `gen_ai.agent.id`, `gen_ai.agent.name`, `gen_ai.conversation.id`, `gen_ai.request.model` | technical | [2] | corrected — the spec lists a broader set of conditionally required attributes including `error.type`, `gen_ai.agent.description`, `gen_ai.agent.id`, `gen_ai.agent.name`, `gen_ai.agent.version`, `gen_ai.conversation.id`, `gen_ai.data_source.id`, `gen_ai.output.type`, `gen_ai.request.choice.count`, `gen_ai.request.model`, `gen_ai.request.seed`, `server.port`; the document lists only a subset |
| 13 | The OTel hierarchy is `invoke_agent` → `gen_ai.chat` → `execute_tool` | technical | [2][3] | verified — the spec formally defines this three-tier structure |
| 14 | A **run** is one unit of work; a **trace** is the full execution tree for one request; a **thread** is a sequence of traces across a multi-turn conversation | technical | [4] | verified |
| 15 | Arize Phoenix supports 10 span kinds: `CHAIN`, `LLM`, `TOOL`, `RETRIEVER`, `EMBEDDING`, `AGENT`, `RERANKER`, `GUARDRAIL`, `EVALUATOR` | technical | [11] | human-review (the Arize agent-observability page fetched does not list or enumerate span kinds; cannot confirm the count of 10 or the complete list from the cited source URL) |
| 16 | Multi-turn thread tracing can reveal that an agent stored a bad assumption in turn 6, and every subsequent turn built on it | technical | [4] | verified |
| 17 | AgentTrace operational surface records "all explicit agent method calls, argument structures, return values, and execution timing"; each invocation produces start/complete events with span-level metadata | technical | [5] | verified |
| 18 | AgentTrace cognitive surface captures "raw prompts, completions, extracted CoT chains, confidence estimates"; frameworks parse semi-structured outputs to extract reasoning segments and plans | technical | [5] | verified |
| 19 | AgentTrace contextual surface tracks "all outbound interactions with external systems (HTTP APIs, SQL/NoSQL, vector stores, file systems)" | technical | [5] | verified |
| 20 | Existing security methods "fail to provide sufficient transparency or traceability into agent reasoning, state changes, or environmental interactions" | attribution | [5] | verified |
| 21 | AgentTrace is designed "not just for debugging or benchmarking, but as a foundational layer for agent security, accountability, and real-time monitoring" | attribution | [5] | verified |
| 22 | An agent stuck in an unproductive loop can still return HTTP 200 — infrastructure looks healthy while the agent burns budget | technical | [4] | verified |
| 23 | MCP trace context propagation: "By auto-instrumenting both client and server with OpenTelemetry you can propagate OpenTelemetry context between the MCP client and server, unifying them into a single trace" | technical | [11] | verified |
| 24 | Empirical study (Arcuschin et al., ICLR 2025 Workshop) measured post-hoc rationalization rates: GPT-4o-mini 13%, Haiku 3.5 7% | statistic | [13] | corrected — paper reports GPT-4o-mini 13.49% and Claude 3.5 Haiku 7.42% (rounding is acceptable); however the venue "ICLR 2025 Workshop" is not confirmed — the paper HTML contains a NeurIPS checklist appendix suggesting NeurIPS submission; venue should be listed as unconfirmed |
| 25 | Gemini 2.5 Flash 2.17%, ChatGPT-4o 0.49%, DeepSeek R1 0.37%, Gemini 2.5 Pro 0.14%, Sonnet 3.7 (extended thinking) 0.04% | statistic | [13] | corrected — Gemini 2.5 Flash 2.17% verified; ChatGPT-4o 0.49% verified; DeepSeek R1 0.37% verified; Sonnet 3.7 0.04% verified; Gemini 2.5 Pro is ambiguous: abstract states 0.14% but paper body section 2.1 reports 4.9% (7 unfaithful pairs from a different dataset pass); the 0.14% figure corresponds to the updated stricter dataset |
| 26 | "7–13% post-hoc rationalization rates in widely-deployed production models" | statistic | [13] | corrected — the 7–13% range accurately covers GPT-4o-mini (13.49%) and Haiku 3.5 (7.42%) but misdescribes scope; these are the two highest-rate models tested, not a general range across "widely-deployed" models; most frontier models tested had rates well below 7% |
| 27 | A model calculates a hypotenuse incorrectly, internally corrects it, but never revises the external statement — the trace looks correct; the reasoning was not | technical | [13] | corrected — no hypotenuse example exists in the paper; the paper describes models giving logically contradictory answers to comparative questions (e.g., "Is X bigger than Y?" and "Is Y bigger than X?"), not a hypotenuse calculation scenario |
| 28 | In multi-agent systems, unfaithful CoT outputs passed between agents "propagate unfaithful belief states, bias decisions, and trigger costly actions in closed-loop agent systems" | causal | [13] | corrected — the paper does not discuss multi-agent systems or belief state propagation between agents at all; it studies individual model faithfulness in isolation; this claim has no basis in source [13] |
| 29 | Regulatory requirements: GDPR Article 22 (right to explanation), EU AI Act documentation requirements | regulatory | [7] | verified — source [7] explicitly cites both GDPR Article 22 and EU AI Act |
| 30 | "EU AI Act's August 2026 documentation requirements" (as a specific deadline) | regulatory | [7] | corrected — source [7] does not mention an August 2026 deadline; the claim in the Findings section attributes this to a Findings-level summary of the Challenge sub-section; the August 2026 date appears only in the Challenge section (SQ4) and is not sourced from [7] or any cited primary text |
| 31 | Standard observability platforms (LangSmith, Langfuse) capture prompts, outputs, tool metadata, token usage — sufficient for debugging but missing immutability guarantees and authority chains | technical | [7] | verified |
| 32 | The same OTel traces can serve as "a unified, audit-grade provenance chain" and "a tamper-resistant, timestamped ledger" satisfying GDPR and HIPAA | technical | [9] | verified |
| 33 | Datadog maintained "dual instrumentation paths" for OTel users before adding native OTel GenAI Semantic Conventions support | technical | [17] | corrected — source [17] states teams had to "maintain parallel instrumentation paths or bypass collector-level policies"; "dual instrumentation paths" is a fair paraphrase, but the Findings attribute "v1.37+" as a Datadog version — it is actually the minimum OTel Semantic Conventions version supported, not a Datadog product version |
| 34 | Kore.ai five pillars: Cognition/Reasoning, Traceability, Performance, Security, Governance | technical | [9] | human-review (could not load source [9] directly during verification; claim is consistent with the raw extract but unconfirmed against live source) |
| 35 | Production traces → insights → dataset creation → evaluations → improvements → regression tests: "once you fix a bug, it stays fixed" | technical | [10] | verified |
| 36 | The three-layer naming (agentic / orchestration / LLM) originates from the Redis vendor blog, not the OTel spec | attribution | [4] | verified — Redis blog confirmed to use these three layer names; OTel spec does not name them |

### CoVe Summary

**Total claims verified:** 36 claims examined across SQ1–SQ4 Findings.

**Verified without correction:** 20 claims (1, 2, 4, 6, 8, 9, 10, 11, 13, 14, 16, 17, 18, 19, 20, 21, 22, 23, 31, 32, 35, 36).

**Corrections required (7):**
- **Claim 3:** The opt-in flag `gen_ai.capture.message.content=true` is not in the OTel spec text; opt-in mechanism exists but this specific flag name is unverified.
- **Claim 12:** `invoke_agent` conditionally required attributes list in the document is incomplete — the spec defines a broader set.
- **Claim 24:** Venue "ICLR 2025 Workshop" is not confirmed; paper contains NeurIPS checklist suggesting a different venue.
- **Claim 25:** Gemini 2.5 Pro rate is ambiguous between 0.14% (abstract, stricter dataset) and 4.9% (section 2.1, earlier dataset); the 0.14% figure requires a caveat.
- **Claim 26:** The "7–13%" framing implies a general production range; it actually describes the two highest-rate models tested.
- **Claim 27 (HIGH):** The hypotenuse example does not exist in source [13]. The paper uses comparative questions (size, dates), not geometric/mathematical calculations. This is a fabricated example.
- **Claim 28 (HIGH):** The multi-agent belief state propagation claim has no basis in source [13]. The paper does not study multi-agent systems. This is an unsupported causal claim presented as sourced.

**Claims requiring human review (4):**
- **Claim 5:** Langfuse `langfuse.*` precedence (source [18] returned 403).
- **Claim 7:** `OTEL_SEMCONV_STABILITY_OPT_IN=gen_ai_latest_experimental` flag name not confirmed in any fetched source.
- **Claim 15:** Arize Phoenix 10 span kinds not enumerable from the cited source URL.
- **Claim 34:** Kore.ai five pillars (source not loadable during verification).

**Critical findings:** Claims 27 and 28 in the SQ3 Findings are fabricated — no source support exists. The hypotenuse example and multi-agent belief propagation claim should be removed or replaced with content actually present in source [13]. The paper venue (Claim 24) should also be corrected before publication.
