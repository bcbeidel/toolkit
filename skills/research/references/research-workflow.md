# Research Workflow

Ten-phase process. Each phase writes to disk so work survives context
resets.

## Resuming After Context Reset

If `docs/research/{date}-{slug}.md` exists with `<!-- DRAFT -->`, read
it to determine the current phase:

- Has `sources:` in frontmatter with `unverified` statuses → resume at Phase 3 (check if extracts are present; if raw content remains, extract first)
- Has sources with updated statuses (verified/removed) but no tier annotations → resume at Phase 5
- Has tier annotations but no `## Challenge` section → resume at Phase 6
- Has `## Challenge` but no `## Findings` → resume at Phase 7
- Has `## Findings` but no `## Claims` → resume at Phase 8
- Has `## Claims` with `unverified` entries → resume at Phase 9
- Has `## Claims` fully resolved, still `<!-- DRAFT -->` → resume at Phase 10

Read the document fully to recover context before continuing.

## Phase 1: Frame the Question

1. Restate the user's question in a precise, answerable form
2. Identify the research mode (see research-modes.md)
3. Break into 2-4 sub-questions
4. Confirm with user: "I'll investigate [question] by looking at [sub-questions]. Sound right?"
5. Note constraints (time period, domain, technology stack)
6. Declare search protocol — state which sources you'll search and initial terms. Initialize:

```json
{"entries": [], "not_searched": []}
```

> **Source diversity:** `WebSearch` routes through a single engine. Vary
> query terms to surface different source types. Fetch known database URLs
> directly when relevant. Log `"google"` as the source honestly. The
> `not_searched` field lists sources you chose not to search, not sources
> the tool can't access.

7. **Write a research brief.** After confirming sub-questions, write a
   1-paragraph first-person brief that becomes the opening of the DRAFT
   document:
   - State the question from the user's perspective
   - List all stated constraints (time period, domain, stack, etc.)
   - Mark unstated dimensions as explicitly open-ended
   - Specify preferred source types: official docs for technical questions,
     peer-reviewed for scientific, primary sources for historical

## Phase 2: Gather Sources

> **Search budgets by SIFT rigor:**
>
> | SIFT Rigor | Searches per sub-question | Total budget |
> |------------|---------------------------|--------------|
> | Low        | 2-3                       | 5-10         |
> | Medium     | 3-5                       | 10-15        |
> | High       | 5-8                       | 15-25        |

For each sub-question, repeat until coverage is sufficient or budget is
exhausted:

1. Execute a search. Aim for 10-20 candidates total across all sub-questions.
2. For each candidate: record URL, title, publication date, author/org. Flag as **unverified**.
3. Log the search:

```json
{"query": "terms", "source": "google", "date_range": "2024-2026", "results_found": 12, "results_used": 3}
```

4. **Reflect.** After every 2-3 searches, assess: which sub-questions have
   coverage? Are results converging? Continue, shift to another sub-question,
   or stop.

> **Fetch failures:** Retry failed `WebFetch` calls individually. Retry
> 3xx with redirect URL. Keep 403 if from published venue. Retry timeouts
> once, then skip. Do not drop sources solely because fetching failed.

After the loop completes:

5. Record skipped sources in `not_searched` with reasons.
6. **Write to disk.** Create `docs/research/{date}-{slug}.md` with `type: research` frontmatter, a `<!-- DRAFT -->` marker, a sources table (# | URL | Title | Author/Org | Date | Status), and a `<!-- search-protocol ... -->` comment containing the accumulated JSON.

## Phase 3: Extract Source Content

For each fetched source, extract relevant content verbatim and discard
boilerplate (navigation, ads, sidebars, unrelated content). This is
**lossless extraction**, not summarization — Phases 8-9 need original
source content for claim verification.

Update the DRAFT document with structured extracts. Format per source:

```markdown
### Source [1]: asyncio — Asynchronous I/O
- **URL:** https://docs.python.org/3/library/asyncio.html
- **Author/Org:** Python Software Foundation | **Date:** 2024

**Re: How does asyncio handle concurrency?**
> "The library provides a foundation for writing single-threaded concurrent
> code using coroutines, multiplexing I/O access over sockets and other
> resources, running network clients and servers, and other related
> primitives." (Introduction, para 1)

**Re: What are the performance characteristics?**
> "Running an asyncio Program... This function always creates a new event
> loop and closes it at the end." (Runners section, para 1)
```

Each extract links to its sub-question, preserves exact wording, and
notes location within the source for Phase 4+ verification.

## Phase 4: Verify Sources

Collect URLs from frontmatter. Run URL verification (see
source-quality.md for command and result handling). Update document on
disk: remove failed URLs from `sources:`, update sources table statuses.

## Phase 5: Evaluate Sources

Apply SIFT at the mode's intensity level (see source-quality.md for
steps, intensity table, and tier definitions). Classify each source
T1-T6. Drop below T5, never cite T6. Update document on disk with tier
annotations in the sources table.

## Phase 6: Challenge

Run challenge sub-steps based on mode (see challenge.md for procedures
and output templates, research-modes.md for which sub-steps apply).
Update document on disk with `## Challenge` section.

## Phase 7: Synthesize

Organize findings by sub-question. Annotate each finding with a
confidence level (see synthesis-guide.md for criteria). If mode
requires counter-evidence, include a dedicated section. Connect
findings to the user's context, identify gaps, suggest follow-ups.
Update document on disk with `## Findings` section. Update frontmatter
`description:` to reflect actual findings.

## Phase 8: Self-Verify Claims (CoVe)

Extract every quote, statistic, attribution, and superlative from
Findings into a `## Claims` table. Run Chain-of-Verification **without
the draft document in context** (see claim-verification.md for claim
types, table format, and CoVe procedure). Update document on disk.

## Phase 9: Citation Re-Verify

Re-fetch cited sources. For each claim, search fetched content for
the specific fact (see claim-verification.md for procedure and
statuses). Update document on disk — no `unverified` claims remain.

## Phase 10: Finalize

1. **Restructure** for lost-in-the-middle convention:
   - Top: summary with key findings (annotated with confidence) and search protocol summary
   - Middle: detailed analysis by sub-question, evidence, Challenge output
   - Bottom: key takeaways, limitations, follow-ups, full search protocol table

2. **Format search protocol.** Extract JSON from `<!-- search-protocol ... -->`, render as:

| Query | Source | Date Range | Found | Used |
|-------|--------|------------|-------|------|

Include summary line: `N searches across M sources, X found, Y used`.

3. **Remove `<!-- DRAFT -->`** marker.
4. **Verify claims.** No `unverified` in Claims Table. `unverifiable` and `human-review` annotated in body.
5. **Reindex and validate:**

```bash
uv run <plugin-scripts-dir>/reindex.py --root .
uv run <plugin-scripts-dir>/audit.py <file> --root . --no-urls
```

## Quality Check

Before removing `<!-- DRAFT -->`, verify each gate:

- [ ] Phase 1: Sub-questions confirmed by user, research brief written
- [ ] Phase 2: DRAFT file on disk
- [ ] Phase 3: Source content extracted, boilerplate discarded
- [ ] Phase 4: URLs verified, unreachable removed
- [ ] Phase 5: Tiers assigned to all sources
- [ ] Phase 6: Challenge section written
- [ ] Phase 7: Findings section written
- [ ] Phase 8: Claims extracted, CoVe complete
- [ ] Phase 9: No unverified claims remain
- [ ] Phase 10: DRAFT removed, audit passes
