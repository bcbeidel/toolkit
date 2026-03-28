---
name: "Agent Observability and Tracing"
description: "OpenTelemetry GenAI semantic conventions as the vendor-neutral standard for agent tracing: the three-layer span model (agent, LLM, tool), key attributes, and structured logging with trace correlation"
metadata:
  type: reference
  sources:
    - https://opentelemetry.io/blog/2025/ai-agent-observability/
    - https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-agent-spans/
    - https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-spans/
    - https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-events/
    - https://www.w3.org/TR/trace-context/
    - https://arize-ai.github.io/openinference/spec/
  related:
    - docs/research/observability-audit-trails.md
    - docs/context/show-your-work-patterns.md
    - docs/context/observability-trust-debuggability.md
    - docs/context/workflow-orchestration.md
    - docs/context/tool-design-for-llms.md
---

OpenTelemetry GenAI semantic conventions provide the emerging vendor-neutral standard for tracing agent execution. The `gen_ai.*` attribute namespace defines three layers that map directly to how agent systems operate: agent invocation, LLM calls, and tool execution. Even without deploying a full OTel collector, structuring internal traces with these conventions ensures future compatibility and a shared vocabulary.

## The Three-Layer Span Model

A trace captures a full agent request as a tree of spans, each with a `span_id` and optional `parent_span_id`:

```
invoke_agent (root span)
  +-- chat (LLM call to plan)
  +-- execute_tool (tool invocation)
  |   +-- chat (LLM call within tool)
  +-- chat (LLM call to synthesize)
  +-- execute_tool (final tool call)
```

**Agent layer.** Spans use `gen_ai.operation.name` of `invoke_agent`, with attributes `gen_ai.agent.id`, `gen_ai.agent.name`, `gen_ai.agent.description`, and `gen_ai.agent.version`. Span kind is CLIENT for cross-process agents, INTERNAL for same-process.

**LLM call layer.** Individual model invocations use `chat` or `text_completion` as the operation name. Token usage is recorded via `gen_ai.usage.input_tokens` and `gen_ai.usage.output_tokens`. Model identity uses `gen_ai.request.model` and `gen_ai.system` (provider).

**Tool layer.** Tool execution spans use `execute_tool` with `gen_ai.tool.name`. Sentry, Langfuse, and other vendors have aligned their implementations with these OTel conventions, confirming industry convergence.

## Structured Logging with Trace Correlation

The minimum viable observability pattern: every log entry carries `trace_id` and `span_id` from request entry. This enables cross-cutting queries connecting agent decisions to outcomes. JSON format with standardized fields (`session_id`, `agent_id`, `tool_name`, `timestamp`). For distributed scenarios, W3C Trace Context propagates via the `traceparent` header: `{version}-{trace_id}-{parent_id}-{trace_flags}`.

## Complementary Trace Formats

**OpenInference** (Arize AI) adds a span-kind taxonomy (`LLM`, `RETRIEVER`, `TOOL`, `AGENT`, `EMBEDDING`, `CHAIN`, `RERANKER`) on top of OTel spans with richer AI-specific typing. It predates OTel GenAI conventions and is widely adopted in practice.

**PROV-AGENT** extends W3C PROV with AI-specific entity classes (`AIAgent`, `AgentTool`, `AIModelInvocation`, `Prompt`, `ResponseData`) for full provenance graphs. Unlike span trees, provenance graphs can represent complex agent-to-agent interactions, iterative refinement loops, and multi-workflow chains. Currently a research prototype, not production tooling.

## Caveats

The GenAI semantic conventions remain experimental (requiring `OTEL_SEMCONV_STABILITY_OPT_IN`). Proposed extensions for Tasks, Actions, Teams, Artifacts, and Memory are not yet ratified. Content capture of prompts and completions is opt-in via `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT` for privacy and performance reasons. Agent workloads may generate orders of magnitude more spans than traditional applications, making overhead a practical concern that requires tiered capture strategies.
