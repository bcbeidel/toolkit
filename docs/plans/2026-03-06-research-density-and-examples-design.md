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

Make references small, discrete, and MECE while preserving behavioral intent:

- Make each reference file own one discrete concern — no duplicated procedures
- Deduplicate overlapping reasoning (claim-verification procedures, SIFT prose,
  question patterns) while keeping reference data intact
- Protect all deterministic tool invocations (`audit.py`, `reindex.py`,
  `check_url.py`) — these are enforcement anchors, never trim candidates
- Audit SKILL.md against instructional design best practices (primacy, recency,
  lost-in-the-middle)
- For every edit, apply: **"would the model do the wrong thing without this?"**
- Word count reduction is a measurement signal, not a target

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

## Results

### #126 — Consider Command Examples

All 16 consider models now have concrete `<example>` blocks. Each example
matches the model's natural sweet spot (e.g., `5-whys` → CI debugging,
`eisenhower-matrix` → sprint priorities, `inversion` → platform launch).
16 files changed, 416 lines added.

### #124 — Research Skill Density Reduction

**Approach evolved during planning:** instead of merging files to reduce count,
we focused on making references MECE (mutually exclusive, collectively
exhaustive), trimming duplicated reasoning, and protecting deterministic tool
invocations.

| File | Before | After | Delta | What changed |
|------|--------|-------|-------|-------------|
| SKILL.md | 806 | 804 | -2 | Folded Document Standards into Output Format; fixed counter-evidence modes |
| claim-verification.md | 733 | 474 | -259 | Removed duplicated Phase 5.5 procedures (workflow owns these) |
| research-workflow.md | 2,052 | 1,912 | -140 | Trimmed SIFT prose duplication, HTML comment rationale |
| research-modes.md | 565 | 490 | -75 | Removed question patterns (SKILL.md owns these) |
| source-verification.md | 188 | 159 | -29 | Removed "When to Run" (workflow owns timing) |
| python-utilities.md | 223 | 202 | -21 | Removed "Validate Entire Project" (unused by research workflow) |
| challenge-phase.md | 461 | 461 | 0 | Already MECE |
| sift-framework.md | 443 | 443 | 0 | Already MECE |
| source-evaluation.md | 334 | 334 | 0 | Already concise |
| **Total** | **5,805** | **5,279** | **-526 (-9%)** | |

**Key principle applied:** deterministic stays in code, reasoning stays in
skills. All `uv run` commands for `audit.py`, `reindex.py`, and `check_url.py`
preserved. Phase gate structure unchanged. Every removal justified by
duplication analysis, not word count targets.

### Reference File Split

Split `research-workflow.md` (1,912 words) at the Phase 3/Phase 4 boundary:

| File | Words | Content |
|------|-------|---------|
| research-workflow.md | 943 | Phases 1-3 (Frame, Gather, Verify) + context reset resumption |
| research-synthesis.md | 1,017 | Phases 4-6 (Challenge, Synthesize, Finalize) + Quality Checklist |

This leverages the write-to-disk checkpoint design: on context reset, the
model only needs the relevant half's instructions. SKILL.md references list
updated; cross-references in claim-verification.md and SKILL.md updated to
point to the correct file for each phase.

### Tests

244 tests pass. All reference cross-links verified.
