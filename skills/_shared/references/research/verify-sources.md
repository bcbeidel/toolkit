---
name: Verify Sources
description: Phase 3 — check URL reachability, drop unreachable sources, update document
---

# Phase 3: Verify Sources

Collect URLs from frontmatter. Run URL verification:

```bash
uv run <plugin-scripts-dir>/check_url.py URL1 URL2 ...
```

Result handling:
- **404 or status 0 (DNS failure):** Drop from source list.
- **403 or 5xx:** Keep source, note access issue.
- **All sources removed:** Stop and gather new sources before proceeding.

Update document on disk: remove failed URLs from `sources:`, update
sources table statuses.

**Example — Phase 3→4 progression:**

| # | URL | Title | Status | Tier |
|---|-----|-------|--------|------|
| 1 | https://docs.python.org/... | asyncio docs | verified → | T1 |
| 2 | https://blog.example.com/... | My Tips | removed (404) → | — |
| 3 | https://realpython.com/... | Async Guide | verified (403) → | T3 |

Phase 3 updates the Status column. Phase 4 adds the Tier column.

### Phase Gate: Phase 3 → Phase 4

URLs checked, unreachable removed from frontmatter.
