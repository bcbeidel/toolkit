---
name: Finalize
description: Phase 9 — restructure document, format search protocol, remove DRAFT marker, validate
stage: finalize
pipeline: research
tools: [Read, Write, Edit, Glob, Grep, Bash]
---

## Purpose

Restructure the document for optimal readability, format the search protocol, remove the DRAFT marker, and run validation.

## Input

- **Path to DRAFT document** with all claims verified

# Phase 9: Finalize

1. **Restructure** for lost-in-the-middle convention:
   - Top: summary with key findings (annotated with confidence) and
     search protocol summary
   - Middle: detailed analysis by sub-question, evidence, Challenge output
   - Bottom: key takeaways, limitations, follow-ups, full search protocol
     table

2. **Format search protocol.** Extract JSON from
   `<!-- search-protocol ... -->`, render as:

| Query | Source | Date Range | Found | Used |
|-------|--------|------------|-------|------|

Include summary line: `N searches across M sources, X found, Y used`.

3. **Remove `<!-- DRAFT -->`** marker.
4. **Verify claims.** No `unverified` in Claims Table. `unverifiable` and
   `human-review` annotated in body.
5. **Validate:**

```bash
bash <plugin-skills-dir>/research/scripts/validate_finalize.sh <file>
```

Note: Reindex is no longer triggered here. Run `/wiki:ingest` after a
research session to sync `_index.md` files.

## Output

The research document must:
- Have `<!-- DRAFT -->` marker removed
- Have `type: research` in frontmatter
- Have non-empty `sources:` in frontmatter
- Pass audit validation

### Phase Gate: Phase 9 → Done

`<!-- DRAFT -->` removed, audit passes.

---

## Constraints

- Do not search for new sources (no WebSearch or WebFetch).
- Do not modify findings substance — structural changes only.
- Do not prompt the user for input.

## Quality Checklist

Before removing `<!-- DRAFT -->`, verify each gate:

- [ ] Phase 2: DRAFT file on disk with structured extracts for all sub-questions
- [ ] Phase 3: URLs verified, unreachable removed
- [ ] Phase 4: Tiers assigned to all sources
- [ ] Phase 5: Challenge section written
- [ ] Phase 6: Findings section written
- [ ] Phase 7: Claims extracted, CoVe complete
- [ ] Phase 8: No unverified claims remain
- [ ] Phase 9: DRAFT removed, audit passes
