# Claim Verification

Fact-check specific claims in research documents by registering high-risk
claims and verifying them against sources before finalization.

## Claim Types (4)

Register these claim types — they map to observed fabrication failure modes.

| Type | Definition | Example |
|------|-----------|---------|
| quote | Verbatim text attributed to a person/source | "Software is eating the world" — Andreessen |
| statistic | Specific number, percentage, or quantity | "30+ integrations available" |
| attribution | Action or role attributed to a person/org | "Chesky founded Airbnb" |
| superlative | Claim of primacy, extremity, or uniqueness | "the first company to achieve..." |

General observations, trend descriptions, and methodology notes do NOT need
registration. Only register claims that assert a specific, verifiable fact.

## Claims Table Format

Add a `## Claims` section to the research document during Phase 5.5a.

| # | Claim | Type | Source | Status |
|---|-------|------|--------|--------|
| 1 | "Software is eating the world" | quote | [1] | unverified |
| 2 | 30+ integrations | statistic | [3] | unverified |
| 3 | Chesky founded Airbnb | attribution | [2] | unverified |

- `Source` references map to the numbered Sources table (e.g., `[1]` = first source)
- All claims start as `unverified`
- Claims without a citeable source should still be registered with source marked `—`

## Resolution Statuses (5)

| Status | Meaning |
|--------|---------|
| verified | Passed CoVe self-check AND citation re-verification confirmed source support |
| corrected | Didn't match source; updated to match (note original claim in parentheses) |
| removed | Not found in source; claim removed from document body |
| unverifiable | Source couldn't be fetched (403/timeout); claim kept but flagged in document |
| human-review | Ambiguous automated result, or uncited claim that CoVe couldn't confirm |

## Phase 5.5a: Self-Verify (CoVe)

Chain-of-Verification catches fabrication from parametric knowledge.

**Procedure:**
1. Scan the Findings section for all quotes, statistics, attributions, and
   superlatives. Extract each into the Claims Table with status `unverified`.
2. For each claim, generate a verification question:
   - quote: "What exact words did [person] say about [topic]?"
   - statistic: "What is the actual number for [metric]?"
   - attribution: "What role did [person] play in [event]?"
   - superlative: "Which [entity] was actually the first/largest/most [claim]?"
3. Answer each verification question in a **separate LLM call without the
   draft document in context**. This prevents confirmation bias.
4. Compare CoVe answers to registered claims. For each:
   - CoVe agrees → leave `unverified`, advance to Phase 5.5b for citation check
   - CoVe contradicts → route through contradiction resolution (below)
   - CoVe uncertain → leave `unverified`, advance to Phase 5.5b

**Gate out:** Claims Table populated. All claims processed through CoVe.
Contradictions routed to 5.5b or resolved.

## Phase 5.5b: Citation Re-Verification

Cross-check claims against their cited source content.

**Procedure:**
1. Group remaining `unverified` claims by source URL.
2. For each source URL: re-fetch via WebFetch.
3. For each claim citing that source: search the fetched content for the
   specific fact asserted by the claim.
4. Assign final status:
   - Source confirms the claim exactly → `verified`
   - Source contains different information → `corrected` (update claim to
     match source, note original in parentheses)
   - Source doesn't mention the claim at all → `removed` (delete from
     document body, keep row in Claims Table with `removed` status)
   - Source can't be fetched (403/timeout) → `unverifiable`
   - Source is ambiguous (mentions topic but doesn't clearly support or
     contradict) → `human-review`

**Gate out:** No `unverified` claims remain in the Claims Table.

## Contradiction Resolution

When CoVe contradicts a claim, follow this uniform procedure (all claim types):

```
CoVe contradicts claim
  → Does the claim have a cited source?
    → YES: Escalate to Phase 5.5b (citation re-verification)
           Source confirms CoVe answer → corrected, update claim, note diff
           Source confirms original claim → verified
           Source is ambiguous → human-review
           Source can't be fetched → human-review
    → NO: human-review
```

The source is always the tiebreaker between the draft and CoVe. When there
is no source, escalate to the human.

## human-review Triggers

These cases always get `human-review` regardless of CoVe/citation results:
- Direct quotes attributed to named individuals (highest fabrication risk)
- Statistics where the source contains a nearby but different number
- Attributions where the source describes a different role or action
- Any claim with no cited source that CoVe contradicts
