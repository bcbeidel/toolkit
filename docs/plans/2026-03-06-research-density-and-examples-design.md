---
name: Research Density Reduction and Consider Command Examples
description: Design for issues #124 and #126 — reduce research skill instruction density and add worked examples to consider commands
related:
  - skills/research/SKILL.md
  - commands/consider.md
---

# Research Density Reduction and Consider Command Examples

**Branch:** `feat/124-126-research-density-and-examples`
**Issues:** #124, #126

## Context

The research skill loads ~5,800 words across 9 files — 3x larger than the next
largest skill. The 16 consider command models lack worked examples, relying on
abstract templates to communicate expected output quality.

These issues share instructional design research: fewer, better instructions
with concrete examples produce higher compliance than verbose descriptions.

## Design

### #126 — Worked Examples for Consider Commands

Add one `<example>` block to each of the 16 consider command files:

- Each example matches the model's natural sweet spot (e.g., `5-whys` gets a
  debugging scenario, `eisenhower-matrix` gets a prioritization scenario)
- ~10-15 lines, placed adjacent to `<output_format>`
- Demonstrates expected depth and specificity, not rigid structure
- Shows what the `<success_criteria>` looks like in practice

### #124 — Research Skill Instruction Density Reduction

Reduce instruction volume while preserving behavioral intent:

- Merge files where content naturally belongs together:
  - `source-evaluation.md` + `source-verification.md` → unified source handling
  - `python-utilities.md` content folded into `research-workflow.md`
- Deduplicate overlapping content between `claim-verification.md` and
  `research-workflow.md` Phase 5.5
- For every edit, apply: **"would the model do the wrong thing without this?"**
- Word count reduction is a measurement signal, not a target
- File count may change as a side effect, not a goal

## Sequencing

1. #126 first — mechanical, lower risk
2. #124 second — careful editing, measure before/after
3. Separate commits on same branch

## Acceptance Criteria

### #126
- All 16 consider models have a concrete worked example
- Examples demonstrate the quality bar from `<success_criteria>`

### #124
- Research skill instructions are more concise without losing behavioral intent
- Every removal justified ("model handles this without prompting" or "duplicated at X")
- SIFT workflow, source verification, claim checking, and phase gates preserved
- Before/after word count reported as measurement
- Tests pass, lint clean

## Research Basis

- IFScale benchmark (Jaroslawicz et al., 2025): instruction compliance degrades
  at 250+ constraints, primacy bias peaks at 150-200
- Anthropic/OpenAI/Google convergence: "two short examples are more effective
  than a long paragraph describing desired output"
- Worked example effect: concrete solved examples reduce cognitive load
- Expertise reversal: examples help novel tasks, can hurt well-understood ones
- Source: `notes/docs/research/2026-03-04-instructional-design.md`,
  `notes/docs/context/instructional-design/verification-and-worked-examples.md`
