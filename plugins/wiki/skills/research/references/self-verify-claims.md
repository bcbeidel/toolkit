---
name: Self-Verify Claims (CoVe)
description: Phase 7 — extract claims from findings, run Chain-of-Verification to catch fabrication
stage: verify
pipeline: research
tools: [Read, Write, Edit, Glob, Grep, Bash, WebFetch]
---

## Purpose

Extract claims from findings and run Chain-of-Verification (CoVe) to catch fabrication, statistical errors, and misattributions.

## Input

- **Path to DRAFT document** with findings section completed

## Context Model

**Context isolation.** The verifier is the primary beneficiary of the
per-agent context model. It starts with a fresh context containing only
this system prompt and the dispatch prompt. The full attention budget is
available for claim-by-claim verification, with no accumulated search
results from earlier phases competing for attention.

# Phase 7: Self-Verify Claims (CoVe)

Extract every quote, statistic, attribution, and superlative from
Findings into a `## Claims` table.

## Claim Types

| Type | Example |
|------|---------|
| quote | "Software is eating the world" — Andreessen |
| statistic | "30+ integrations available" |
| attribution | "Chesky founded Airbnb" |
| superlative | "the first company to achieve..." |

General observations and methodology notes do not need registration.

## Claims Table Format

| # | Claim | Type | Source | Status |
|---|-------|------|--------|--------|
| 1 | "exact claim text" | quote | [1] | unverified |

Source references map to the numbered Sources table. All claims start as
`unverified`. Claims without a citeable source use `—` as source.

## CoVe Procedure

Chain-of-Verification catches fabrication from parametric knowledge.

1. Extract all quotes, statistics, attributions, and superlatives from
   Findings into the Claims Table.
2. For each claim, generate a verification question (e.g., "What exact
   words did [person] say about [topic]?").
3. Answer each question in a **separate context without the draft
   document**. This prevents confirmation bias — it is the reason
   Phase 7 is a distinct phase.
4. Compare: CoVe agrees → advance to Phase 8. CoVe contradicts → route
   through contradiction resolution. CoVe uncertain → advance to Phase 8.

## Contradiction Resolution

When CoVe contradicts a claim: if the claim has a cited source, escalate
to Phase 8 — the source is the tiebreaker between draft and CoVe. If no
source, assign `human-review`.

## Output

The DRAFT document must have:
- `## Claims` table populated with all extracted claims
- No cells containing `unverified` in the Status column
- All claims resolved to: verified, corrected, removed, unverifiable, or human-review

### Phase Gate: Phase 7 → Phase 8

`## Claims` table populated, CoVe complete.

## Constraints

- Use WebFetch only for re-verification of existing citations, not for discovering new sources (no WebSearch).
- Do not modify findings structure — only update claim statuses and correct factual errors.
- Do not prompt the user for input.
