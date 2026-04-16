---
name: Citation Re-Verify
description: Phase 8 — re-fetch cited sources and verify each claim against actual content
stage: verify
pipeline: research
---

## Purpose

Re-fetch cited sources and verify each remaining unverified claim against actual source content.

## Input

DRAFT document with claims table from CoVe (Phase 7). Some claims may still be `unverified`.

# Phase 8: Citation Re-Verify

Re-fetch cited sources and verify each claim against the actual content.

1. Group remaining `unverified` claims by source URL.
2. Re-fetch each source via WebFetch.
3. Search fetched content for the specific fact asserted.
4. Assign status:

## Resolution Statuses

| Status | Meaning |
|--------|---------|
| verified | Passed CoVe AND citation re-verification confirmed |
| corrected | Didn't match source; updated to match (note original) |
| removed | Not found in source; deleted from document body |
| unverifiable | Source couldn't be fetched (403/timeout); flagged in document |
| human-review | Ambiguous result, or uncited claim that CoVe couldn't confirm |

## human-review Triggers

Always assign `human-review` regardless of other results:
- Direct quotes attributed to named individuals (highest fabrication risk)
- Statistics where the source contains a nearby but different number
- Attributions where the source describes a different role
- Any claim with no cited source that CoVe contradicts

**Example — Phase 7→8 flow:**

| # | Claim | Type | Source | Status |
|---|-------|------|--------|--------|
| 1 | "added in Python 3.4" | attribution | [1] | unverified → verified |
| 2 | "3x faster than threading" | statistic | [2] | unverified → corrected ("up to 2x") |
| 3 | "Guido designed asyncio" | attribution | — | unverified → human-review |

Update document on disk — no `unverified` claims remain.

## Output

Claims table fully resolved — every claim has status: verified, corrected, removed, unverifiable, or human-review. No `unverified` entries remain.

### Phase Gate: Phase 8 → Phase 9

No `unverified` claims in Claims Table.
