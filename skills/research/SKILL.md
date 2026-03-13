---
name: research
description: >
  Conducts structured investigations using the SIFT framework and
  produces verified research documents. Use when the user wants to
  "investigate", "research", "look into", "what do we know about",
  "compare options", "evaluate feasibility", "analyze the landscape",
  "find out about", "deep dive into", "explore alternatives", or any
  request to conduct a structured investigation.
argument-hint: "[topic or question to investigate]"
user-invocable: true
compatibility: "Requires Python 3 (stdlib only), WOS plugin (audit, reindex), WebSearch, WebFetch"
references:
  - ../_shared/references/research/frame.md
  - ../_shared/references/research/resumption.md
  - ../_shared/references/research/gather-and-extract.md
  - ../_shared/references/research/verify-sources.md
  - ../_shared/references/research/evaluate-sources-sift.md
  - ../_shared/references/research/challenge.md
  - ../_shared/references/research/synthesize.md
  - ../_shared/references/research/self-verify-claims.md
  - ../_shared/references/research/citation-reverify.md
  - ../_shared/references/research/finalize.md
  - ../_shared/references/research/research-modes.md
  - ../_shared/references/research/cli-commands.md
  - ../_shared/references/preflight.md
---

# Research Skill

Conduct structured investigations using the SIFT framework (Stop,
Investigate the source, Find better coverage, Trace claims). Produces
research documents in `/docs/research/` with verified sources
and structured findings.

## Mode Detection

Detect the research mode from the question framing:

| Question pattern | Mode | Intensity |
|-----------------|------|-----------|
| "What do we know about X?" | deep-dive | High |
| "What's the landscape for X?" | landscape | Medium |
| "How does X work technically?" | technical | High |
| "Can we do X with our constraints?" | feasibility | Medium |
| "How does X compare to competitors?" | competitive | Medium |
| "Should we use A or B?" | options | High |
| "How did X evolve / what's the history?" | historical | Low |
| "What open source options exist for X?" | open-source | Medium |

If ambiguous, ask: "What kind of investigation would be most useful?
A **deep dive** (comprehensive), **options comparison**, or
**feasibility study**?"

## Resumption Assessment

When resuming work on an existing research document, run the assessment
script before proceeding. This reports structural facts (word count, draft
marker, section presence, source count) so you can determine the current
state without re-reading the entire document.

Before running any `uv run` command below, follow the preflight check in
the [preflight reference](../_shared/references/preflight.md).

**Single document (known file):**
```bash
uv run <plugin-skills-dir>/research/scripts/research_assess.py --file <path>
```

**Discovery (what's in progress?):**
```bash
uv run <plugin-skills-dir>/research/scripts/research_assess.py --scan --root .
```

Use the JSON output to determine which phase the document is in and what
actions to take next. Do not re-read the entire document if the assessment
provides sufficient context.

## Workflow

All modes follow the same 9-phase workflow with varying intensity.
See the shared research references for the full process.

## Phase Gates (Mandatory)

Each phase ends with a checkpoint. Do not proceed until the gate is met.

| Phase | Gate | How to Verify |
|-------|------|---------------|
| 1. Frame → 2. Gather and Extract | User confirmed sub-questions, research brief written | User said "yes" or equivalent |
| 2. Gather and Extract → 3. Verify Sources | DRAFT file exists with structured extracts for all sub-questions | Read the file |
| 3. Verify Sources → 4. Evaluate Sources | URLs checked, unreachable removed from frontmatter | Read the file |
| 4. Evaluate Sources → 5. Challenge | Sources table has Tier + Status columns | Read the file |
| 5. Challenge → 6. Synthesize | `## Challenge` section exists on disk | Read the file |
| 6. Synthesize → 7. Self-Verify Claims | `## Findings` section exists on disk | Read the file |
| 7. Self-Verify Claims → 8. Citation Re-Verify | `## Claims` table populated, CoVe complete | Read the file |
| 8. Citation Re-Verify → 9. Finalize | No `unverified` claims in Claims Table | Read the file |
| 9. Finalize → Done | `<!-- DRAFT -->` removed, audit passes | Run audit |

STOP at each gate. If the condition is not met, complete it before proceeding.

## Common Deviations (Do Not)

- **Do not write the entire document in one pass at the end.** Each phase
  writes to disk. If you haven't written to disk since Phase 2, you've
  skipped checkpoints.
- **Do not skip sub-questions.** They structure Phase 6 synthesis. Without
  them, findings will organize by whatever taxonomy emerges from searching.
- **Do not SIFT "in your head."** Use the SIFT evaluation log in the
  sources table. If there's no visible per-source tier annotation, SIFT
  didn't happen.
- **Do not skip `url_checker`.** Fetching content via WebFetch verifies
  content; `url_checker` verifies the URL itself (catches 404s, hallucinated
  URLs).

## Output Document Format

The final research document is placed at `docs/research/{date}-{slug}.md`
with frontmatter following the document standards in AGENTS.md:

```yaml
---
name: "Title of the investigation"
description: "One-sentence summary of findings"
type: research
sources:
  - https://example.com/primary-source
related:
  - docs/research/2026-01-15-related-topic.md
---
```

## Examples

<example>
**Sources table after Phase 4 (Evaluate Sources):**

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|-----------|------|------|--------|
| 1 | https://docs.python.org/3/library/asyncio.html | asyncio — Asynchronous I/O | Python Software Foundation | 2024 | T1 | verified |
| 2 | https://realpython.com/async-io-python/ | Async IO in Python | Real Python / Brad Solomon | 2023 | T3 | verified |
| 3 | https://blog.example.com/asyncio-tips | My Asyncio Tips | unknown | 2022 | T5 | verified (403) |
</example>

<example>
**Findings excerpt (Phase 6) for sub-question "How does asyncio handle concurrency?":**

### How does asyncio handle concurrency?

Asyncio uses a single-threaded event loop with cooperative multitasking [1][2].
Tasks yield control at `await` points, allowing other tasks to run (HIGH —
T1 + T3 sources converge). This differs from threading: no shared-state
race conditions, but CPU-bound work blocks the loop (MODERATE — T3 source
only, not directly confirmed in T1 docs).

**Counter-evidence:** One source [3] claims asyncio supports true parallelism
via `loop.run_in_executor()`, but this delegates to a thread pool — the event
loop itself remains single-threaded (HIGH).
</example>

<example>
**Claims table (Phase 7) with mixed resolution statuses:**

| # | Claim | Type | Source | Status |
|---|-------|------|--------|--------|
| 1 | "asyncio was added in Python 3.4" | attribution | [1] | verified |
| 2 | "3x faster than threading for I/O" | statistic | [2] | corrected (source says "up to 2x") |
| 3 | "Guido van Rossum designed asyncio" | attribution | — | human-review |
</example>

## Key Rules

- **SIFT every source** — no source enters the document without tier classification. See `evaluate-sources-sift.md`.
- **Counter-evidence is required** for deep-dive, options, and technical modes. See `research-modes.md`.
- **Log every search** during Phase 2 and include the protocol in the final document.
- **Confidence levels on every finding** — HIGH, MODERATE, or LOW. See `synthesize.md`.
- **Verify all claims** before finalizing — quotes, statistics, attributions, superlatives. See `self-verify-claims.md` and `citation-reverify.md`.
