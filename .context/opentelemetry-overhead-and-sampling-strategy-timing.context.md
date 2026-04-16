---
name: OpenTelemetry Overhead and Sampling Strategy Timing
description: "OTel is the correct observability standard, but untuned auto-instrumentation can reach 7–42% overhead — design sampling strategy before rollout, not after."
type: concept
confidence: high
created: 2026-04-10
updated: 2026-04-10
sources:
  - https://opentelemetry.io/docs/concepts/signals/traces/
  - https://opentelemetry.io/docs/concepts/observability-primer/
  - https://last9.io/blog/distributed-tracing-with-opentelemetry/
related:
  - docs/context/raft-consensus-and-event-sourcing-adoption-constraints.context.md
  - docs/context/distributed-resilience-stack-circuit-breaker-retry-jitter.context.md
  - docs/context/saga-orchestration-vs-choreography-default.context.md
---
# OpenTelemetry Overhead and Sampling Strategy Timing

OpenTelemetry (OTel) is the CNCF-standard observability framework — vendor-neutral, with broad language SDK support. The "1–5% overhead" claim widely cited in documentation reflects best-case, tuned deployments. Untuned auto-instrumentation in production can reach 7–42% CPU overhead and comparable latency increases. Sampling strategy must be designed before rollout.

## OpenTelemetry as the Standard

OTel provides a unified model for the three observability signals:
- **Traces**: the path of a request across multiple services; each trace is composed of spans
- **Metrics**: aggregated numeric data over time periods (request rates, error rates, latency histograms)
- **Logs**: timestamped messages emitted by services

Context propagation enables trace continuity across service boundaries by injecting trace context into outgoing request headers and extracting from incoming headers. W3C Trace Context is the default standard format; B3 format is supported for Zipkin compatibility. Without propagation, spans from different services appear as disconnected traces.

## Overhead Reality by Instrumentation Method

| Method | Best-Case Overhead | Production Range |
|--------|-------------------|-----------------|
| eBPF zero-code | ~1% CPU | ~1–3% |
| Manual instrumentation | ~2–5% | 3–8% |
| Java agent auto-instrumentation | ~3–8% | 7–42% |

The 1–5% figure represents tuned, optimized deployments: manual instrumentation of low-cardinality spans with aggressive head-based sampling. Auto-instrumentation at full cardinality without sampling — the default entry path for most teams evaluating OTel — produces overhead well outside this range.

A documented production example: P99 latency rising from ~10ms to ~15ms under sustained load, plus ~4 MB/s additional outbound traffic with full request-level traces. InfoQ's 2025 report on OTel's Go performance found measurable throughput degradation even with careful configuration.

## Sampling Strategy: Design First

Sampling determines which traces are recorded and exported. Without sampling, a high-traffic service emitting traces on every request can generate terabytes of telemetry data and produce the 7–42% overhead range.

**Head-based sampling** (decision at trace start):
- Configurable sampling rate (e.g., 10% of all requests)
- Use parent-based preservation: if a parent span is sampled, all child spans in the same trace are also sampled (preserves complete traces)
- Fast, low overhead; cannot prioritize error traces over successful ones at decision time

**Tail-based sampling** (decision after trace completes, at Collector level):
- Analyzes complete traces before deciding whether to retain them
- Can always keep errors and slow requests while sampling down normal traffic
- More expensive to operate (Collector must buffer spans until trace completes)
- Recommended for production systems where error visibility is more important than uniform sampling

**Starting recommendation:**
1. Capture all errors (trace_status = ERROR)
2. Capture all requests exceeding a latency threshold (e.g., P95 of normal response time)
3. Apply probabilistic sampling (1–10%) for normal traffic
4. Add high-cardinality attributes for debugging: `user.id`, `order.id`, `feature_flag.*`, `deployment.environment`

## High-Cardinality Attributes

High-cardinality attributes (user_id, order_id, feature flags, customer tier) are the primary mechanism for debugging distributed failures — they allow filtering traces to a specific user, transaction, or deployment segment. Include them on spans at instrumentation time.

Security: sanitize PII attributes before export — either at instrumentation time via attribute masking in code, or at Collector level via processor plugins.

## Three Instrumentation Paths

1. **Manual instrumentation**: full control, custom spans, highest visibility; correct for business-critical paths where observability granularity matters
2. **Auto-instrumentation**: hooks into supported libraries automatically with minimal code changes; correct for standard HTTP/database/messaging instrumentation
3. **Zero-code eBPF**: kernel-level tracing for compiled binaries you can't modify; lowest overhead, lowest visibility control

## Takeaway

Adopt OTel as the observability standard. Before production rollout, design your sampling strategy: decide which traces to always keep (errors, slow requests), what sample rate to apply to normal traffic, and what high-cardinality attributes to include. Untuned instrumentation in production will exceed the 1–5% overhead claim and can create performance problems that undermine confidence in the observability system itself.
