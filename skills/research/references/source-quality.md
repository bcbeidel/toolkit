# Source Quality Reference

Used during Phase 3 (Verify Sources) and Phase 4 (Evaluate Sources).

## URL Verification (Phase 3)

Verify all source URLs are reachable before evaluation:

```bash
uv run <plugin-scripts-dir>/check_url.py URL1 URL2 ...
```

- **404 or status 0 (DNS failure):** Drop from source list.
- **403 or 5xx:** Keep source, note access issue.
- **All sources removed:** Stop and gather new sources before proceeding.

**Example — Phase 3→4 progression:**

| # | URL | Title | Status | Tier |
|---|-----|-------|--------|------|
| 1 | https://docs.python.org/... | asyncio docs | verified → | T1 |
| 2 | https://blog.example.com/... | My Tips | removed (404) → | — |
| 3 | https://realpython.com/... | Async Guide | verified (403) → | T3 |

Phase 3 updates the Status column. Phase 4 adds the Tier column.

## SIFT Steps (Phase 4)

Apply SIFT (Stop, Investigate, Find better, Trace) to each source:

1. **Stop** — Flag as "unverified" until remaining steps complete.
2. **Investigate** — Check domain authority, author credentials, publication reliability. Classify into tier (see Source Hierarchy below).
3. **Find better** — For key claims, search for higher-tier sources. If found, upgrade. Note claims with limited sourcing.
4. **Trace** — For critical claims, follow citation chains to primary source. Verify claim matches original context.

After evaluation: drop sources below T5, never cite T6.

## SIFT Intensity by Mode

| Mode | Stop | Investigate | Find Better | Trace |
|------|------|-------------|-------------|-------|
| deep-dive | Always | Full | Full | Key claims |
| landscape | Always | Domain only | Top 3 claims | Skip |
| technical | Always | Full | Full | All claims |
| feasibility | Always | Domain only | Key claims | Skip |
| competitive | Always | Full | Key claims | Skip |
| options | Always | Full | Full | Key claims |
| historical | Always | Domain only | Key claims | Key claims |
| open-source | Always | Repo metrics | Key claims | Skip |

## Source Hierarchy (T1-T6)

- **T1 — Official docs:** Project documentation, standards bodies (W3C, IETF), original author writings
- **T2 — Institutional research:** University departments, think tanks, industry consortia (CNCF)
- **T3 — Peer-reviewed:** Journals, conference proceedings, published books by domain experts
- **T4 — Expert practitioners:** Recognized experts in their domain, core maintainer blogs, conference talks
- **T5 — Community content:** High-voted Stack Overflow, community blogs, forum consensus
- **T6 — AI-generated:** LLM outputs without primary source verification. Never cite as a source.

## Authority Annotation

Annotate tiers in the document body, not the frontmatter:

```
- https://docs.python.org/3/library/asyncio.html (T1: official docs)
- https://martinfowler.com/articles/microservices.html (T4: expert practitioner)
```

## Red Flags

- No author or organization identified
- Circular sourcing — multiple sources citing the same unverified origin
- Outdated information relative to domain currency
- Conflict of interest — vendor-sponsored research about own product
- Survivorship bias — only success stories, no failures
