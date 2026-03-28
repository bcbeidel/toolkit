---
name: "Observability, Trust, and Debuggability"
description: "Design patterns that connect agent observability to debugging and trust: tiered content capture, trace-correlated logs, visual trace trees, cryptographic audit chains, and provenance graphs -- with the critical distinction that traces enable debugging but not trust"
metadata:
  type: reference
  sources:
    - https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-events/
    - https://github.com/agentkitai/agentlens
    - https://arxiv.org/html/2508.02866v2
    - https://allen.hutchison.org/2026/02/17/the-observability-gap/
    - https://langfuse.com/docs/observability/overview
  related:
    - docs/research/observability-audit-trails.md
    - docs/context/agent-observability-tracing.md
    - docs/context/show-your-work-patterns.md
    - docs/context/validation-architecture.md
    - docs/context/human-in-the-loop-design.md
---

Traces show what an agent did. They do not show whether its reasoning was sound. This distinction is the most important insight in agent observability: a complete execution trace can create false confidence when operators trust a system more because they can see its steps, even when those steps contain flawed reasoning.

## Five Design Patterns

**Tiered content capture.** Separate metadata tracing (always on, low overhead) from content capture (opt-in, high overhead). OTel implements this with the `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT` toggle. In production, trace structure and metrics flow continuously; prompt and completion content is captured only when debugging or auditing requires it. This is the foundational pattern -- without it, the overhead of full content logging kills adoption.

**Trace-correlated structured logs.** Every log entry carries `trace_id` and `span_id`, enabling queries that cross-cut between traces (request flow) and logs (detailed events). JSON format with standardized fields (`session_id`, `agent_id`, `tool_name`, `timestamp`). This bridges observability (what happened) and debugging (why it happened).

**Visual trace trees.** Render agent execution as expandable trees showing the full path from input to output. LangSmith, Langfuse, and Arize Phoenix provide this: expand steps to see exact prompts and responses, pinpoint errors, understand tool selection. This is the primary mechanism by which non-engineers inspect agent behavior.

**Cryptographic audit chains.** Append-only event storage with SHA-256 hash chains per session. Each event references the previous event's hash, creating a chain that detects post-hoc modification. Protects against external log tampering, but does not prevent the agent from omitting events during recording. The threat model matters: hash chains guard against log modification, not log omission.

**Provenance graphs.** Model agent execution as a directed graph using W3C PROV extensions. Enables queries spanning traditional traces: "What inputs led to this decision?" and "How did error propagate across agent boundaries?" High potential for full accountability but currently at research stage.

## Traces Enable Debugging, Not Trust

Trust requires three independent capabilities:

1. **Observability** -- can you see what the agent did? (traces, logs, show-your-work patterns)
2. **Evaluation** -- did the agent produce correct outputs? (automated testing, ground truth comparison)
3. **Alignment verification** -- did the agent follow intended behaviors? (constraint checking, policy enforcement)

Observability is necessary but not sufficient. Systems that equate traceability with trustworthiness have a dangerous gap: they can tell you the agent's steps were recorded, not that those steps were right. The observability gap identified by Hutchison makes this explicit -- operational health, model behavior, data quality, and reasoning traceability must all be present.

Design systems that combine tracing with automated evaluation, not systems that assume seeing the work means the work is good.
