# Claim Verification Reference

Used during Phase 8 (Self-Verify Claims) and Phase 9 (Citation Re-Verify).

## Claim Types

Register these — they map to observed fabrication failure modes:

| Type | Example |
|------|---------|
| quote | "Software is eating the world" — Andreessen |
| statistic | "30+ integrations available" |
| attribution | "Chesky founded Airbnb" |
| superlative | "the first company to achieve..." |

General observations and methodology notes do not need registration.

## Claims Table Format

Add a `## Claims` section during Phase 8:

| # | Claim | Type | Source | Status |
|---|-------|------|--------|--------|
| 1 | "exact claim text" | quote | [1] | unverified |

Source references map to the numbered Sources table. All claims start as `unverified`. Claims without a citeable source use `—` as source.

## Resolution Statuses

| Status | Meaning |
|--------|---------|
| verified | Passed CoVe AND citation re-verification confirmed |
| corrected | Didn't match source; updated to match (note original) |
| removed | Not found in source; deleted from document body |
| unverifiable | Source couldn't be fetched (403/timeout); flagged in document |
| human-review | Ambiguous result, or uncited claim that CoVe couldn't confirm |

## CoVe Procedure (Phase 8)

Chain-of-Verification catches fabrication from parametric knowledge.

1. Extract all quotes, statistics, attributions, and superlatives from Findings into the Claims Table.
2. For each claim, generate a verification question (e.g., "What exact words did [person] say about [topic]?").
3. Answer each question in a **separate context without the draft document**. This prevents confirmation bias — it is the reason Phase 8 is a distinct phase.
4. Compare: CoVe agrees → advance to Phase 9. CoVe contradicts → route through contradiction resolution. CoVe uncertain → advance to Phase 9.

## Citation Re-Verification (Phase 9)

1. Group remaining `unverified` claims by source URL.
2. Re-fetch each source via WebFetch.
3. Search fetched content for the specific fact asserted.
4. Assign status: source confirms → `verified`. Source differs → `corrected`. Source doesn't mention → `removed`. Source unfetchable → `unverifiable`. Source ambiguous → `human-review`.

**Example — Phase 8→9 flow:**

| # | Claim | Type | Source | Status |
|---|-------|------|--------|--------|
| 1 | "added in Python 3.4" | attribution | [1] | unverified → verified |
| 2 | "3x faster than threading" | statistic | [2] | unverified → corrected ("up to 2x") |
| 3 | "Guido designed asyncio" | attribution | — | unverified → human-review |

Phase 8 (CoVe) populates the table and flags contradictions. Phase 9 re-fetches sources to assign final statuses.

## Contradiction Resolution

When CoVe contradicts a claim: if the claim has a cited source, escalate to Phase 9 — the source is the tiebreaker between draft and CoVe. If no source, assign `human-review`.

## human-review Triggers

Always assign `human-review` regardless of other results:
- Direct quotes attributed to named individuals (highest fabrication risk)
- Statistics where the source contains a nearby but different number
- Attributions where the source describes a different role
- Any claim with no cited source that CoVe contradicts
