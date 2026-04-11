---
name: "OTel GenAI Span Hierarchy and Adoption Status"
description: "OTel GenAI semantic conventions define a three-tier agent span hierarchy (invoke_agent → gen_ai.chat → execute_tool) that is production-usable but still experimental as of early 2026, with vendor convergence underway and agent framework conventions unfinished."
type: concept
confidence: high
created: 2026-04-10
updated: 2026-04-10
sources:
  - https://opentelemetry.io/blog/2025/ai-agent-observability/
  - https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-agent-spans/
  - https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-spans/
  - https://www.datadoghq.com/blog/llm-otel-semantic-convention/
  - https://opentelemetry.io/blog/2025/stability-proposal-announcement/
related:
  - docs/context/cot-traces-debugging-vs-stakeholder-trust.context.md
  - docs/context/observability-vs-auditability-shared-infrastructure.context.md
  - docs/context/agent-feedback-loop-lifecycle-coverage-and-traces.context.md
---
## Key Insight

The OTel GenAI semantic conventions formally define a three-tier agent span hierarchy that is well-specified and usable in production. As of early 2026, these conventions remain experimental — but "experimental" means attribute names may change, not that the infrastructure is unsafe. Major vendors (Datadog, Langfuse, Langsmith) converged on OTel GenAI support in 2025. Agent framework conventions for multi-agent orchestration remain unfinished.

## The Formal Hierarchy

OTel defines 8 `gen_ai.operation.name` values across the full agent execution surface:

- `invoke_agent` — agent root span (span kind: CLIENT for remote, INTERNAL for in-process)
- `gen_ai.chat`, `generate_content`, `text_completion` — LLM call spans
- `embeddings`, `retrieval` — retrieval-layer spans
- `execute_tool` — tool execution spans
- `create_agent` — agent initialization spans

The formal hierarchy: `invoke_agent` → `gen_ai.chat` → `execute_tool`. Each tier has distinct required attributes: agent spans capture `gen_ai.agent.id`, `gen_ai.conversation.id`, token totals; LLM spans capture model, token usage per call, latency, request parameters; tool spans capture tool name and execution timing.

Sensitive content (prompts, completions, system instructions) SHOULD NOT be captured by default. Opt-in is required — this is a deliberate privacy-safety tradeoff built into the spec.

## Three-Layer Conceptual Model vs. OTel Spec

The "three-layer model" — LLM layer, orchestration layer, agentic layer — originates from the Redis vendor blog, not the OTel specification. The OTel spec defines operation types and hierarchy rules but does not name or label these as three layers. The Redis framing is technically grounded and useful for reasoning, but treat it as one synthesis rather than a normative standard.

Arize Phoenix extends the span-kind taxonomy to 10 types: CHAIN, LLM, TOOL, RETRIEVER, EMBEDDING, AGENT, RERANKER, GUARDRAIL, EVALUATOR. For RAG and evaluation-heavy workflows, this richer taxonomy is more appropriate than a simple three-layer model.

## Adoption Status (HIGH confidence on the spec; MODERATE on adoption)

Until 2025, major vendors operated with incompatible proprietary tracing formats. Datadog added native OTel GenAI support in v1.37+ (2025). Langfuse's `langfuse.*` namespace attributes still take precedence over OTel convention attributes — standards-adjacent, not fully standards-compliant.

"Experimental" status has two distinct risks being conflated: API instability and convention instability. The November 2025 OTel stability proposal acknowledged this and proposed decoupling them, allowing stable instrumentation to emit experimental conventions. As of early 2026, this proposal was open for community feedback and not yet released.

**Practical implication:** Teams can use current OTel GenAI instrumentation in production with the expectation that span attribute names may change in future versions, requiring dashboard updates. The drift risk is operational, not architectural.

## What Remains Unfinished

Agent framework conventions — targeting IBM Bee Stack, IBM wxFlow, CrewAI, AutoGen, and LangGraph (GitHub issue #1530) — remain in progress as of early 2026. The three-tier hierarchy applies to single-agent application spans. Multi-agent orchestration spans, where the three-layer model is most needed, remain under-specified until #1530 finalizes.

## Takeaway

Instrument using OTel GenAI conventions now — the spec is well-specified and major vendors are converging. Keep sensitive content opt-in. The three-layer framing is a useful conceptual map, not a normative label from the spec. Treat multi-agent orchestration as not yet standardized; use vendor-specific instrumentation for those use cases until the framework conventions are finalized.
