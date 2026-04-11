---
name: Test Strategy Architecture-Driven Selection
description: "No single test model is universally optimal; the Pyramid, Trophy, and Honeycomb each fit a specific architecture and team context — choose by system shape, not doctrine."
type: concept
confidence: high
created: 2026-04-10
updated: 2026-04-10
sources:
  - https://web.dev/articles/ta-strategies
  - https://kentcdodds.com/blog/the-testing-trophy-and-testing-classifications
  - https://www.wiremock.io/post/rethinking-the-testing-pyramid
related:
  - docs/context/ci-pipeline-test-layer-ordering-and-quality-gate-calibration.context.md
  - docs/context/shift-left-testing-durable-principle-overstated-statistics.context.md
  - docs/context/consumer-driven-contract-testing-scope-and-adoption-barriers.context.md
  - docs/context/agent-testing-pyramid-uncertainty-tolerance-layers.context.md
---
# Test Strategy Architecture-Driven Selection

## Key Insight

The most defensible recommendation in 2025 is architecture-driven test strategy selection, not doctrine-driven. The "pyramid is dead" argument traces to a vendor (WireMock) with a commercial interest in integration testing. Unit-test foundations remain valid for most architectures. Adapt the proportions to your system; don't discard the principle.

## The Three Primary Models

**Test Pyramid** (Mike Cohn): Base of unit tests, middle of integration tests, top of E2E. Fast feedback, granular isolation, low cost per test. Sound for monolithic and layered architectures with stable internal logic. Still the most common starting point; all sources — including those critiquing it — preserve the unit-test foundation.

**Testing Trophy** (Kent Dodds, building on Guillermo Rauch's principle): Four layers — static analysis, unit, integration (primary), E2E. The associated maxim is "Write tests. Not too many. Mostly integration." Best suited to JavaScript/React frontends and teams using Testing Library. Emphasizes that tests should "resemble the way your software is used" to maximize confidence per test written.

**Testing Honeycomb** (Spotify): Designed for microservices. Inverts the pyramid — minimal implementation tests (unit-like), substantial integration tests, sparse E2E. Rationale: microservice complexity lies in inter-service interactions, not in internal logic of individual services. (MODERATE confidence — T2 sources; no direct Spotify primary documentation available.)

## Architecture-to-Strategy Selection Matrix

| Architecture | Team | Manual Testing | Recommended Strategy |
|---|---|---|---|
| Small/monolith | Developers only | High | Ice Cone / Crab |
| Small/monolith | Developers only | Low | Test Pyramid |
| Large/modular | Developers only | High | Trophy / Diamond |
| Large/modular | Developers only | Low | Trophy / Honeycomb |
| Large | Dev + QA | High | Trophy / Crab |

Source: Google web.dev (T1), synthesis across multiple T2/T3 sources.

## Common Misreadings

The WireMock argument that the pyramid is "outdated" rests on three real advances — faster test infrastructure, better frameworks, better observability — but the conclusion that integration tests should universally dominate is vendor-positioned. No T1 or academic source advocates abandoning unit-test foundations. The pyramid's rigid proportions may not fit microservices, but its principle does.

Similarly, Dodds's Trophy does not advocate for skipping unit tests — it advocates against chasing unit test coverage at the expense of integration confidence. The statically-typed base (ESLint, Flow) replaces some unit test coverage in the JavaScript ecosystem specifically.

## Takeaway

Start from architecture: monolith → Pyramid; JavaScript/frontend SPA → Trophy; microservices → Honeycomb. The goal — "ship working software serving user needs, not achieving 100% coverage" — holds across all models. Write tests that detect real user-facing errors. Avoid coverage-chasing that doesn't map to actual application quality.
