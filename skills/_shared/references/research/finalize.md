---
name: Finalize
description: Phase 9 — restructure document, format search protocol, remove DRAFT marker, validate
stage: finalize
pipeline: research
---

## Purpose

Restructure the document for optimal readability, format the search protocol, remove the DRAFT marker, and run validation.

## Input

DRAFT document with verified claims table (no unverified entries).

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
5. **Reindex and validate:**

```bash
uv run <plugin-scripts-dir>/reindex.py --root .
uv run <plugin-scripts-dir>/audit.py <file> --root . --no-urls
```

## Output

Final research document with DRAFT marker removed, `type: research` in frontmatter, non-empty `sources`, lost-in-the-middle structure (summary top, detail middle, takeaways bottom), and formatted search protocol table.

### Phase Gate: Phase 9 → Done

`<!-- DRAFT -->` removed, audit passes.

---

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
