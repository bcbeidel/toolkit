---
name: "Record-and-Replay Fixture Drift and Metadata Verification"
description: "Record-and-replay cassettes go stale when model version, tool API, or prompt state changes — without metadata verification, replay tests pass while the live system has diverged from the recording."
type: concept
confidence: high
created: 2026-04-10
updated: 2026-04-10
sources:
  - https://arxiv.org/abs/2505.17716
  - https://www.sakurasky.com/blog/missing-primitives-for-trustworthy-ai-part-8/
  - https://medium.com/@scrudato/deterministic-tests-for-complex-llm-rag-applications-b5a354b75346
related:
  - docs/context/agent-testing-pyramid-uncertainty-tolerance-layers.context.md
  - docs/context/eval-pipeline-ci-cd-integration-and-adoption-gap.context.md
---
## Key Insight

Record-and-replay is the most-cited technique for bridging determinism and real model behavior in agent testing. Its critical vulnerability: cassette files record against a specific model version, tool API version, and prompt state. When any of those change, the replay environment has silently diverged from the recording — and the test still passes.

## How It Works

The VCR.py pattern captures HTTP interactions (LLM API calls) in YAML cassette files on first run, then intercepts identical requests on subsequent runs to return recorded responses. This eliminates non-determinism at the API boundary while preserving realistic response content.

The AgentRR paper (arXiv, Shanghai Jiao Tong University, 2025) extends this to agent execution traces: by recording full agent execution, most task steps can be replayed from a pre-derived plan, reducing the number of live LLM calls required.

Block Engineering applies this at the integration layer: real MCP server interactions and LLM responses are recorded in JSON fixtures. Tests validate tool call sequences and interaction flow without asserting exact outputs.

## The Silent Validity Problem

Cassette files go stale when:
- The model version changes (new model release, provider update)
- A tool API version bumps (changed schema, new parameters)
- The prompt changes (any iteration in production)

In each case, replay tests pass using the old recording while the live system behaves differently. The test suite provides false confidence.

## Sakura Sky's Seven Implementation Requirements

To make replay trustworthy, seven requirements must be met:

1. **Structured execution traces** — append-only JSON events, not logs
2. **Complete metadata capture** — model ID, sampling parameters, tool versions recorded in each cassette
3. **Replay engine with cursor-based deterministic access** — deterministic replay ordering
4. **Deterministic stubs** — replacing live LLM and tool dependencies during replay
5. **Injection-based harness** — agent code unchanged; dependencies injected
6. **Governance integration** — compliance and audit requirements handled at replay time
7. **Regression framework** — historical traces used as golden files; mismatches surface automatically

Requirement 2 is the critical one: without version metadata in each cassette, there is no mechanism to detect that the recording is no longer representative of the current system. When any dependency changes, the harness should surface a mismatch immediately rather than silently replaying a stale response.

## Zero Coverage of Multi-Agent Cascading Failures

Record-and-replay operates at the individual-agent trace level. The MAST taxonomy documents 14 system-level failure modes in multi-agent systems — cascading errors, correlated biases from shared base models — that are invisible at the individual agent interaction level. Replay-based tests cannot detect these failures regardless of metadata verification discipline.

## Takeaway

Use record-and-replay for Layer 2 integration confidence, but treat the metadata verification requirement as non-negotiable. Record model ID, tool versions, and prompt hashes in every cassette. Build the harness to surface version mismatches before replaying stale fixtures. Know that replay gives zero coverage of multi-agent cascading failures.
