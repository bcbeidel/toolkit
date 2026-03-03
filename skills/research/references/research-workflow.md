# Research Workflow

Six-phase investigation process. All research modes follow these phases,
with SIFT intensity and Challenge sub-steps varying by mode (see
research-modes.md).

The research document is created in Phase 2 and built progressively —
each phase writes its output to disk so work survives context resets.

## Resuming After Context Reset

If a document already exists at `docs/research/{date}-{slug}.md` with
`<!-- DRAFT -->` near the top, a previous session started this investigation.
Read the document to determine which phases are complete:

- Has `sources:` in frontmatter but no tier annotations in body → resume at Phase 3
- Has tier annotations but no `## Challenge` section → resume at Phase 4
- Has `## Challenge` section but no `## Findings` section → resume at Phase 5
- Has `## Findings` section but still has `<!-- DRAFT -->` → resume at Phase 6

When resuming, read the document fully to recover context before continuing.

## Phase 1: Frame the Question

1. Restate the user's question in a precise, answerable form
2. Identify the research mode from question framing (see SKILL.md)
3. Break the question into 2-4 sub-questions
4. Confirm scope with the user: "I'll investigate [question] by looking at
   [sub-questions]. Sound right?"
5. Note any constraints (time period, domain, technology stack)
6. **Declare search protocol:** State which sources you plan to search
   (e.g., Google, Google Scholar, GitHub, specific documentation sites)
   and what terms you'll use. Initialize the search protocol JSON:

```json
{"entries": [], "not_searched": []}
```

> **Source diversity:** `WebSearch` routes through a single search engine. To
> improve source diversity: (1) vary query terms to surface different source
> types, (2) fetch known database URLs directly (e.g., PubMed, Semantic
> Scholar) when relevant, (3) log `"google"` as the source honestly — this is
> expected. The `not_searched` field should list sources you chose not to
> search, not sources the tool can't access.

## Phase 2: Gather Sources

1. Conduct breadth-first web searches across the sub-questions
2. Aim for 10-20 candidate sources (more for deep-dive, fewer for historical)
3. For each candidate, record: URL, title, publication date, author/org
4. Flag all sources as **unverified** at this stage
5. Prioritize diversity — different organizations, perspectives, source types
6. **Log each search** — after every web search, append to the protocol:

```json
{
  "query": "the search terms used",
  "source": "google|scholar|github|docs|...",
  "date_range": "2024-2026 or null",
  "results_found": 12,
  "results_used": 3
}
```

7. After gathering is complete, record sources you considered but did
   not search in `not_searched` as strings with a brief reason:

```json
"not_searched": [
  "Google Scholar - covered by direct source fetching",
  "PubMed - topic is not biomedical"
]
```

> **Handling fetch failures:** When parallel `WebFetch` calls fail, a single
> failure can cascade to sibling calls ("Sibling tool call errored"). Retry
> failed URLs individually. Common failure modes:
> - **403** — bot protection; source exists but can't be fetched. Retain if
>   from a published venue.
> - **303/301** — redirect; retry with the redirect URL.
> - **Timeout** — retry once, then skip. Do not drop sources solely because
>   fetching failed — assess based on URL verification status.

8. **Write the initial document to disk.** Create the file at
   `docs/research/{date}-{slug}.md` with a `<!-- DRAFT -->` marker,
   frontmatter containing all gathered source URLs, and a sources table:

```yaml
---
name: "Concise summary of the investigation"
description: "One-sentence summary (update in Phase 5)"
type: research
sources:
  - https://gathered-source-1.example.com
  - https://gathered-source-2.example.com
related: []
---
<!-- DRAFT — investigation in progress -->

# [Title]

## Sources

| # | URL | Title | Author/Org | Date | Status |
|---|-----|-------|-----------|------|--------|
| 1 | ... | ...   | ...       | ...  | unverified |

## Search Protocol (WIP)

<!-- search-protocol
{"entries": [], "not_searched": []}
-->

Update this section after each search. Replace the JSON in the comment
above with the current accumulated protocol.
```

The search protocol JSON is stored in the document itself (inside the
`<!-- search-protocol ... -->` comment), not in agent memory. After each
search, update the comment with the accumulated JSON. This ensures the
protocol survives context resets alongside the source list.

This checkpoint means the source list survives a context reset.

## Phase 3: Verify & Evaluate

Mechanical URL verification followed by SIFT evaluation in a single phase.

### URL Verification

1. Collect all source URLs from the document's frontmatter
2. Use `wos.url_checker.check_urls()` to verify reachability:

   ```bash
   uv run <plugin-scripts-dir>/check_url.py \
       'https://example.com/source-1' \
       'https://example.com/source-2'
   ```

   (Full reference: `references/source-verification.md`)
3. Review the results:
   - Remove sources where `reachable=False` with status 404 or 0
   - Keep sources where `reachable=False` with status 403/5xx but note issues
4. If all sources removed, gather new sources before proceeding
5. Report verification results to the user before continuing

### SIFT Evaluation

Apply SIFT framework (see `references/sift-framework.md`) at the mode's
intensity level.

For each source:

1. **Stop** — Is this source known to me? Flag as unverified if not.
2. **Investigate** — Check domain authority, author credentials, bias.
   Classify into source hierarchy tier (T1-T6, see `references/source-evaluation.md`).
3. **Find better** — For key claims, search for the same information from a
   higher-tier source. Upgrade when found.
4. **Trace** — For critical claims, follow the citation chain to the primary
   source. Verify the claim matches the original context.

After evaluation:
- Drop sources below T5 unless no better source exists
- Never cite T6 (AI-generated) as a source
- Annotate remaining sources with their tier

5. **Update the document on disk.** Remove failed URLs from the `sources:`
   frontmatter list. Update the sources table with verification status and
   tier annotations:

```
| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|-----------|------|------|--------|
| 1 | ... | ...   | ...       | ...  | T2   | verified |
| 2 | ... | ...   | ...       | ...  | T4   | verified (403) |
```

## Phase 4: Challenge

Stress-test reasoning before synthesis. See `references/challenge-phase.md`
for full procedures.

Three sub-steps, applied based on research mode (see research-modes.md):

1. **Assumptions check** (all modes) — List 3-5 key assumptions, check
   evidence for/against each, assess impact if false
2. **ACH** (deep-dive, options, competitive, feasibility) — Generate
   competing hypotheses, build evidence matrix, select hypothesis with
   fewest inconsistencies
3. **Premortem** (all modes) — Imagine main conclusion is wrong, generate
   3 failure reasons, assess plausibility

4. **Update the document on disk.** Append a `## Challenge` section with
   the assumptions check, ACH matrix (if applicable), and premortem results.

## Phase 5: Synthesize

1. Organize findings by sub-question
2. For each sub-question, note:
   - Points of agreement across sources (strong evidence)
   - Points of disagreement (contested or uncertain)
   - Gaps where evidence is missing
3. **Annotate each finding with a confidence level:**

| Level | Criteria |
|-------|----------|
| HIGH | Multiple independent T1-T3 sources converge; methodology sound |
| MODERATE | Credible sources support; primary evidence not directly verified |
| LOW | Single source; unverified; some counter-evidence exists |

4. If mode requires counter-evidence: dedicate a section to arguments,
   evidence, or perspectives that challenge the main findings
5. Connect findings to the user's context and decisions
6. Identify actionable insights
7. Note limitations — what couldn't be determined and why
8. Suggest follow-up questions if the investigation revealed new unknowns
9. **Writing constraint for claims:** When writing findings, ensure every
   quote, statistic, attribution, and superlative is traceable to a cited
   source. If you cannot point to a specific source for a factual claim,
   do not include it. General observations and trend descriptions are fine
   without specific citations.

10. **Update the document on disk.** Add a `## Findings` section organized
   by sub-question with confidence levels, counter-evidence (if applicable),
   and a connections/implications section. Update the `description:` in
   frontmatter to reflect actual findings.

## Phase 6: Finalize Research Document

The document already exists on disk with content from Phases 2-5. This phase
restructures it for the final reader and runs validation.

1. **Restructure for lost-in-the-middle convention:**
   - **Top:** Summary with key findings (each annotated with confidence level)
     and search protocol summary line
   - **Middle:** Detailed analysis by sub-question, evidence, Challenge phase
     output (assumptions, ACH if applicable, premortem), counter-evidence
   - **Bottom:** Key takeaways, limitations, follow-up questions, and full
     search protocol table

2. **Format the search protocol.** Extract the search protocol JSON from
   the `<!-- search-protocol ... -->` comment in the document. Format it
   as a markdown table directly in the document. Use this format:

```markdown
| Query | Source | Date Range | Found | Used |
|-------|--------|------------|-------|------|
| search terms | google | 2024-2026 | 12 | 3 |
```

   Include a one-line summary near the top: `N searches across M sources, X results found, Y used`

   Replace the `## Search Protocol (WIP)` section and its
   `<!-- search-protocol ... -->` comment with the rendered markdown table
   under a final `## Search Protocol` heading (drop the "(WIP)" suffix).

3. **Remove the `<!-- DRAFT -->` marker** from the document.

4. **Regenerate index files:**

```bash
uv run <plugin-scripts-dir>/reindex.py --root .
```

5. **Validate the document:**

```bash
uv run <plugin-scripts-dir>/audit.py <file> --root . --no-urls
```

## Quality Checklist

Before removing the `<!-- DRAFT -->` marker, verify:
- [ ] All sources passed URL verification
- [ ] All sources have been SIFT-evaluated at the mode's intensity
- [ ] Sources are annotated with hierarchy tiers
- [ ] Challenge phase completed (assumptions + premortem at minimum)
- [ ] ACH included if mode requires it
- [ ] Every finding annotated with confidence level (HIGH/MODERATE/LOW)
- [ ] Counter-evidence section present (if mode requires it)
- [ ] No T6 (AI-generated) sources cited
- [ ] Search protocol section present with all searches logged
- [ ] Implications connected to the user's context
- [ ] Document passes validation:
  `uv run <plugin-scripts-dir>/audit.py <file> --root . --no-urls`
