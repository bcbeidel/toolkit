---
name: Synthesize
description: Phase 6 — organize findings by sub-question with confidence levels and writing constraints
stage: synthesize
pipeline: research
tools: [Read, Write, Edit, Glob, Grep, Bash]
---

## Purpose

Synthesize research extracts into structured findings organized by sub-question, with confidence levels and source attribution.

## Input

- **Path to DRAFT document** with challenge section completed

# Phase 6: Synthesize

Organize findings by sub-question. Annotate each finding with a
confidence level:

| Level | Criteria |
|-------|----------|
| HIGH | Multiple independent T1-T3 sources converge; methodology sound |
| MODERATE | Credible sources support; primary evidence not directly verified |
| LOW | Single source; unverified; some counter-evidence exists |

## Writing Constraints

- Every quote, statistic, attribution, and superlative must trace to a
  cited source. If no source supports a factual claim, do not include it.
- General observations and trend descriptions are fine without specific
  citations.
- If mode requires counter-evidence, dedicate a section to arguments and
  perspectives that challenge the main findings.

Connect findings to the user's context, identify gaps, suggest follow-ups.
Update document on disk with `## Findings` section. Update frontmatter
`description:` to reflect actual findings.

## Output

`## Findings` section on disk with:
- Findings organized by sub-question
- Confidence levels (HIGH/MODERATE/LOW) on every finding
- Source attribution for all factual claims

### Phase Gate: Phase 6 → Phase 7

`## Findings` section exists on disk.

## Constraints

- Do not search for new sources (no WebSearch or WebFetch).
- Do not verify claims — that's the verifier's job.
- Do not prompt the user for input.
