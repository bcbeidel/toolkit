---
name: "Abstraction Level Design for Agent-Facing Artifacts"
description: "How calibrating abstraction altitude — WHAT/WHY vs. HOW — across specifications, plans, and instructions affects agent execution reliability, with empirical thresholds for the specificity-flexibility tradeoff"
metadata:
  type: reference
  sources:
    - https://arxiv.org/html/2512.02246v1
    - https://arxiv.org/html/2505.13360v1
    - https://arxiv.org/html/2510.23564v1
    - https://arxiv.org/html/2601.22290
    - https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
    - https://openreview.net/pdf?id=sY5N0zY5Od
  related:
    - docs/research/abstraction-level-design.md
    - docs/context/prompt-engineering.md
    - docs/context/agentic-planning-execution.md
    - docs/context/writing-for-llm-consumption.md
---

Abstraction altitude — how much implementation detail an artifact exposes — is not a style choice but an engineering variable. Higher altitude means more WHAT/WHY; lower altitude means more HOW. Each artifact type has a natural altitude range, and deviating from it in either direction degrades agent execution quality.

## The Altitude Spectrum

| Altitude | Content | Artifact Type | Agent Freedom |
|----------|---------|---------------|---------------|
| Highest | Purpose and constraints only | Specifications | Maximum |
| High | Goals with observable outcomes | Plans | High |
| Medium | Patterns with adaptation latitude | Research context | Medium |
| Low | Step-by-step procedures | Instructions | Low |
| Lowest | Exact commands, no deviation | Scripts/hooks | None |

This maps to the declarative-imperative spectrum: declarative artifacts specify WHAT should happen; imperative artifacts specify HOW. DSPy validates the principle architecturally — separating WHAT (signatures) from HOW (prompting strategies) enables automated optimization that outperforms hand-crafted prompts.

## Specifications: WHAT and WHY, Never HOW

Specifications should describe desired end states and constraints, not implementation steps. Copilot Workspace demonstrates this with a three-layer pipeline: specification (current vs. desired state), plan (files and actions), implementation (code diffs). The specification layer never mentions file paths or functions.

High altitude does not mean low coverage. LLMs guess unspecified requirements correctly only 41.1% of the time, with conditional requirements dropping to 22.9%. Specifications must be explicit about constraints and edge cases — they just must not prescribe implementation.

## Plans: Observable Outcomes at Middle Altitude

The optimal plan altitude is "observable outcomes" — statements an agent can verify without human judgment. ReCode (2025) found an inverted-U pattern for decomposition depth, peaking at depth 8 on ScienceWorld. Both shallow decomposition (insufficient) and excessive decomposition (over-fragmentation) reduce performance. Adaptive granularity achieved 20.9% improvement over the best fixed-granularity baseline while using 78.9% fewer tokens.

For reliable execution, plan items need three properties: minimality (cannot be further decomposed), verifiability (correctness is objectively determinable), and functional determinism (correct reasoning yields a unique output). The practical test: can the agent determine whether this item is done without asking a human?

| Altitude | Example | Verifiable? |
|----------|---------|-------------|
| Too high | "Improve the authentication system" | No |
| Right | "Login endpoint returns 401 for expired tokens" | Yes — testable |
| Too low | "Add `if token.expired: return 401` to line 47" | Yes, but constrains implementation |

## Instructions: The Specificity Calibration Problem

Instructions sit at the lowest natural-language altitude, and their calibration is the most empirically studied. Key thresholds:

- **Procedural tasks** (math, logic, code): specificity improves accuracy significantly (+0.47 on math)
- **Inference tasks** (commonsense, decisions): specificity barely helps (+0.02) or hurts
- **Unspecified requirements** regress 2x more across model updates
- **Over-specification** (all requirements at once) degrades accuracy 15-20% from instruction-density ceiling effects

The resolution is selective specification: explicitly specify requirements that are critical, unstable across model updates, or unlikely to be guessed from context. Leave predictable requirements to model defaults.

Anthropic's degrees-of-freedom framework operationalizes this: high freedom (text guidelines) for open-ended tasks, medium freedom (pseudocode with parameters) for patterned tasks, low freedom (exact scripts) for fragile operations.

## The Model-Capacity Modifier

Larger models tolerate higher altitude. GPT-4 performs reasonably with vague prompts (0.60 accuracy); O3-mini collapses to 0.34 on the same prompts. Instructions targeting multiple model tiers must be written at the altitude the weakest model requires, or provide progressive disclosure that smaller models consume fully while larger models skim.

The bottom line: altitude is an engineering parameter, not a preference. Specs say WHAT. Plans say DONE-WHEN. Instructions say HOW — but only as much HOW as the task demands and the model needs.
