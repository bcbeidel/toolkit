# Research Workflow

Nine-phase process. Each phase writes to disk so work survives context
resets.

## Resuming After Context Reset

If `docs/research/{date}-{slug}.md` exists with `<!-- DRAFT -->`, read
it to determine the current phase:

- Has `sources:` in frontmatter but no tier annotations → resume at Phase 3
- Has tier annotations but no `## Challenge` section → resume at Phase 5
- Has `## Challenge` but no `## Findings` → resume at Phase 6
- Has `## Findings` but no `## Claims` → resume at Phase 7
- Has `## Claims` with `unverified` entries → resume at Phase 8
- Has `## Claims` fully resolved, still `<!-- DRAFT -->` → resume at Phase 9

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

## Phase 2: Gather Sources

1. Breadth-first web searches across sub-questions. Aim for 10-20 candidates.
2. For each candidate: record URL, title, publication date, author/org. Flag as **unverified**.
3. Log each search:

```json
{"query": "terms", "source": "google", "date_range": "2024-2026", "results_found": 12, "results_used": 3}
```

4. After gathering, record skipped sources in `not_searched` with reasons.

> **Fetch failures:** Retry failed `WebFetch` calls individually. Retry
> 3xx with redirect URL. Keep 403 if from published venue. Retry timeouts
> once, then skip. Do not drop sources solely because fetching failed.

5. **Write to disk.** Create `docs/research/{date}-{slug}.md` with `type: research` frontmatter, a `<!-- DRAFT -->` marker, a sources table (# | URL | Title | Author/Org | Date | Status), and a `<!-- search-protocol ... -->` comment containing the accumulated JSON.

## Phase 3: Verify Sources

Collect URLs from frontmatter. Run URL verification (see
source-quality.md for command and result handling). Update document on
disk: remove failed URLs from `sources:`, update sources table statuses.

## Phase 4: Evaluate Sources

Apply SIFT at the mode's intensity level (see source-quality.md for
steps, intensity table, and tier definitions). Classify each source
T1-T6. Drop below T5, never cite T6. Update document on disk with tier
annotations in the sources table.

## Phase 5: Challenge

Run challenge sub-steps based on mode (see challenge.md for procedures
and output templates, research-modes.md for which sub-steps apply).
Update document on disk with `## Challenge` section.

## Phase 6: Synthesize

Organize findings by sub-question. Annotate each finding with a
confidence level (see synthesis-guide.md for criteria). If mode
requires counter-evidence, include a dedicated section. Connect
findings to the user's context, identify gaps, suggest follow-ups.
Update document on disk with `## Findings` section. Update frontmatter
`description:` to reflect actual findings.

## Phase 7: Self-Verify Claims (CoVe)

Extract every quote, statistic, attribution, and superlative from
Findings into a `## Claims` table. Run Chain-of-Verification **without
the draft document in context** (see claim-verification.md for claim
types, table format, and CoVe procedure). Update document on disk.

## Phase 8: Citation Re-Verify

Re-fetch cited sources. For each claim, search fetched content for
the specific fact (see claim-verification.md for procedure and
statuses). Update document on disk — no `unverified` claims remain.

## Phase 9: Finalize

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

Before removing `<!-- DRAFT -->`, verify each phase gate was met (see SKILL.md phase gates table). Run the audit to catch any remaining issues.
