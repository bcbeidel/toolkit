---
name: "Skill Golden Dataset Perishability"
description: "Golden datasets for WOS skill behavioral tests are perishable across LLM model updates — a WOS skill defines behavior for Claude indirectly, so any fixed expected-output dataset becomes invalid when Claude's model changes, making structural validation plus human review the dominant strategy."
type: context
sources:
  - https://developers.openai.com/blog/eval-skills
  - https://arxiv.org/html/2508.20737v1
  - https://deepchecks.com/llm-production-challenges-prompt-update-incidents/
  - https://arxiv.org/abs/2601.22025
related:
  - docs/research/2026-04-11-llm-skill-behavioral-testing.research.md
  - docs/context/skill-behavioral-testing-layer-gap.context.md
  - docs/context/behavioral-testing-roi-and-investment-threshold.context.md
---
# Skill Golden Dataset Perishability

Golden datasets for WOS skill behavioral tests are perishable by design. This is not a maintenance inconvenience — it is a structural property of what WOS skills are.

## Why WOS Skill Datasets Expire

A WOS skill defines behavior for Claude — it is a set of instructions that Claude interprets and acts on. The expected output from a skill is not the skill text itself; it is what Claude does when it reads the skill. When Claude's model version changes, Claude's interpretation of the same instructions changes. A golden dataset of expected outputs calibrated against Claude 3.5 Sonnet will not accurately represent expected outputs from Claude 3.7 or later versions.

This is categorically different from testing a deterministic function. If you write a test for `parse_document()`, the expected output does not change when Claude's model updates. If you write a test that checks what Claude does when given `/wos:research`, the expected output changes with every model update that affects Claude's behavior.

## The Compound Problem

For meta-artifacts like WOS skills, this perishability compounds with two other challenges:

**Open-ended input space.** A skill like `/wos:research` is invoked with arbitrary user queries in arbitrary project contexts. Constructing a representative golden dataset requires specifying expected Claude outputs across a combinatorially large input space — a task that may exceed the effort of maintaining the skill itself.

**No ground truth.** For application outputs (SQL queries, API responses), ground truth is defined by the domain. For skill outputs (research documents, plan files), ground truth is convention-dependent and changes as WOS conventions evolve. A golden dataset encoding current conventions becomes incorrect the moment conventions are updated.

## Implications for Strategy

These properties do not make behavioral testing impossible. They set a high bar for when it is worth the overhead:

- Behavioral testing is justified for high-volume, high-stakes skills where regression cost clearly exceeds dataset maintenance cost.
- Golden datasets require explicit versioning by Claude model version and WOS convention version.
- Dataset staleness must be actively detected, not assumed away. A stale golden dataset produces false confidence — worse than no testing.

## The Dominant Strategy for WOS

For the majority of WOS skills, high-quality structural validation (Layer 1 linting via `wos/validators.py`) plus mandatory human review of skill changes is the correct strategy. Structural properties — instruction line count, ALL-CAPS density, SKILL.md body length, description quality, name format — are model-update-stable. These checks remain valid across Claude model versions. Human review of skill changes provides coverage for semantic regressions that a perishable golden dataset would catch unreliably anyway.

Behavioral testing is reserved for skills that are edited frequently, have measurable downstream failure costs, and where the investment in version-pinned golden dataset maintenance is explicitly justified.
