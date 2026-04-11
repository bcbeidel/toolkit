---
name: Performance Test Type Taxonomy and Environment Parity Prerequisite
description: "The six-type performance test taxonomy (smoke, average-load, stress, spike, soak, breakpoint) is industry-standard; each type gates the next. Environment parity — not threshold calibration — is the real prerequisite for reliable CI performance gating."
type: concept
confidence: high
created: 2026-04-10
updated: 2026-04-10
sources:
  - https://grafana.com/docs/k6/latest/testing-guides/test-types/
  - https://www.locust.cloud/blog/5-essential-load-test-profiles/
  - https://www.harness.io/blog/load-testing-an-essential-guide-for-2026
  - https://grafana.com/docs/k6/latest/testing-guides/automated-performance-testing/
related:
  - docs/context/core-web-vitals-thresholds-and-seo-floor-not-target.context.md
  - docs/context/percentile-approximation-hazard-and-histogram-based-slo-metrics.context.md
  - docs/context/continuous-profiling-production-standard-and-tool-selection.context.md
  - docs/context/ci-pipeline-test-layer-ordering-and-quality-gate-calibration.context.md
---
# Performance Test Type Taxonomy and Environment Parity Prerequisite

## Key Insight

Use performance test types sequentially — each type gates the next. Do not run stress or soak tests before average-load tests pass. Threshold calibration is secondary; environment parity is the dominant prerequisite for shift-left performance gating to be reliable.

## The Six-Type Taxonomy (HIGH confidence — multiple T1 + T4 sources converge)

| Test Type | Purpose | When to Run |
|---|---|---|
| **Smoke** | Minimal load; verify baseline correctness, no errors | Every code or script change |
| **Average-load** | Normal expected traffic; confirm production performance standards | Regularly; establishes healthy baseline |
| **Stress** | Loads exceeding expected average; stability under peak traffic | After average-load tests pass |
| **Spike** | Sudden, massive surge with minimal ramp-up | Before events with known traffic spikes (launches, sales) |
| **Soak/endurance** | Sustained heavy load for hours; exposes memory leaks, disk exhaustion, queue failures | After other types pass; catches degradation over time |
| **Breakpoint** | Increases load until error rate threshold is crossed; establishes maximum capacity | Capacity planning |

A seventh type — **recovery testing** (apply overload, then reduce to confirm the system recovers) — appears in Locust documentation but is not part of the canonical k6 taxonomy.

## Environment Parity is the Real Gate

Shift-left performance testing only works if CI environments reliably represent production. This is the unsolved prerequisite that most guides underweight:

- Shared CI runners introduce noisy-neighbor effects
- Cloud CI environments differ from production in autoscaling behavior, cache warmth, and network topology
- Identical load tests across tools produce 10–20% result variance due to differences in TCP/TLS handling and timing definitions
- Flaky performance test rates rose from 10% (2022) to 26% (2025)

If CI environments cannot reproduce production conditions, performance gates either generate false positives that erode developer trust or miss real regressions that only appear under production topology.

## Best Practices for Test Design

- Base test traffic shapes on actual production data and user behavior patterns, not guessed shapes
- Reserve soak and stress tests for staging environments; run lightweight smoke and load tests in CI
- Combine load testing with chaos engineering (failure injection) to evaluate resilience simultaneously
- Use percentile metrics (p50, p90, p95, p99) as thresholds — never averages (averages hide tail behavior)

## The Statistical Gating Model (MODERATE confidence — T4 source, no T1 academic validation)

When establishing CI thresholds from baselines:
- Establish baselines from multiple runs, not a single test
- Warning threshold: +1.5 standard deviations → notification without blocking
- Critical threshold: +2.5 standard deviations → block deployment, escalate

These thresholds assume environment stability. Verify stability before trusting confidence intervals.

## Takeaway

Run performance tests in type order: smoke → average-load → stress → spike → soak → breakpoint. Each type targets a distinct failure mode. Before investing in threshold calibration, invest in environment fidelity. A perfectly calibrated gate on an unrepresentative CI environment produces noise, not signal.
