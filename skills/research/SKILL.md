---
name: research
description: >
  This skill should be used when the user wants to "investigate",
  "research", "look into", "what do we know about", "compare options",
  "evaluate feasibility", "analyze the landscape", "find out about",
  "deep dive into", "explore alternatives", or any request to conduct
  a structured investigation and produce a research document.
argument-hint: "[topic or question to investigate]"
user-invocable: true
compatibility: "Requires Python 3 (stdlib only), WOS plugin (audit, reindex), WebSearch, WebFetch"
references:
  - references/research-workflow.md
  - references/sift-framework.md
  - references/source-evaluation.md
  - references/source-verification.md
  - references/challenge-phase.md
  - references/research-modes.md
  - references/python-utilities.md
  - references/claim-verification.md
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

## Workflow

All modes follow the same workflow with varying SIFT intensity.
See `references/research-workflow.md` for the full 8-phase process.

## Phase Gates (Mandatory)

Each phase ends with a checkpoint. Do not proceed until the gate is met.

| Phase | Gate | How to Verify |
|-------|------|---------------|
| 1. Frame -> 2. Gather | User confirmed sub-questions | User said "yes" or equivalent |
| 2. Gather -> 3. Verify | DRAFT file exists on disk with `<!-- DRAFT -->` marker | Read the file |
| 3. Verify -> 4. Challenge | Sources table has Tier + Status columns | Read the file |
| 4. Challenge -> 5. Synthesize | `## Challenge` section exists on disk | Read the file |
| 5. Synthesize -> 5.5a. Self-Verify | `## Findings` section exists on disk | Read the file |
| 5.5a. Self-Verify -> 5.5b. Citation Re-Verify | `## Claims` table populated, CoVe complete | Read the file |
| 5.5b. Citation Re-Verify -> 6. Finalize | No `unverified` claims in Claims Table | Read the file |
| 6. Finalize -> Done | `<!-- DRAFT -->` removed, audit passes | Run audit |

STOP at each gate. If the condition is not met, complete it before proceeding.

## Common Deviations (Do Not)

- **Do not write the entire document in one pass at the end.** Each phase
  writes to disk. If you haven't written to disk since Phase 2, you've
  skipped checkpoints.
- **Do not skip sub-questions.** They structure Phase 5 synthesis. Without
  them, findings will organize by whatever taxonomy emerges from searching.
- **Do not SIFT "in your head."** Use the SIFT evaluation log in the
  sources table. If there's no visible per-source tier annotation, SIFT
  didn't happen.
- **Do not skip `url_checker`.** Fetching content via WebFetch verifies
  content; `url_checker` verifies the URL itself (catches 404s, hallucinated
  URLs).

## Output Document Format

The final research document is placed at `docs/research/{date}-{slug}.md`
with simplified YAML frontmatter:

```yaml
---
name: "Title of the investigation"
description: "One-sentence summary of findings"
type: research
sources:
  - https://example.com/primary-source
  - https://example.com/another-source
related:
  - docs/research/2026-01-15-related-topic.md
---
```

Write the document directly, then run reindex and validate
(see `references/python-utilities.md`).

## Document Standards

Follow the document standards in AGENTS.md for structure and frontmatter.

## Examples

<example>
**Sources table after Phase 3 (Verify & Evaluate):**

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|-----------|------|------|--------|
| 1 | https://docs.python.org/3/library/asyncio.html | asyncio — Asynchronous I/O | Python Software Foundation | 2024 | T1 | verified |
| 2 | https://realpython.com/async-io-python/ | Async IO in Python | Real Python / Brad Solomon | 2023 | T3 | verified |
| 3 | https://blog.example.com/asyncio-tips | My Asyncio Tips | unknown | 2022 | T5 | verified (403) |
</example>

<example>
**Findings excerpt (Phase 5) for sub-question "How does asyncio handle concurrency?":**

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
**Claims table (Phase 5.5) with mixed resolution statuses:**

| # | Claim | Type | Source | Status |
|---|-------|------|--------|--------|
| 1 | "asyncio was added in Python 3.4" | attribution | [1] | verified |
| 2 | "3x faster than threading for I/O" | statistic | [2] | corrected (source says "up to 2x") |
| 3 | "Guido van Rossum designed asyncio" | attribution | — | human-review |
</example>

## Key Rules

- **SIFT every source.** No source enters the document unverified.
  See `references/sift-framework.md`.
- **Source hierarchy matters.** Prefer official docs over blog posts.
  See `references/source-evaluation.md`.
- **Counter-evidence is required** for deep-dive, options, and technical modes.
  Actively search for disagreement.
- **Output is a research document.** Write the final artifact directly with
  `type: research` frontmatter, then run reindex and validate.
- **Authority annotations.** Each source in the final document should note
  its tier in the source hierarchy.
- **Challenge before synthesis.** Never skip the Challenge phase. Assumptions
  check and premortem run on every mode. ACH runs on deep-dive, options,
  competitive, and feasibility. See `references/challenge-phase.md`.
- **Log search protocol.** Record every search during Phase 2 (Gather).
  Format as a markdown table and include in the final document.
  See `references/research-workflow.md` Phase 2.
- **Confidence levels on every finding.** Annotate each finding as HIGH,
  MODERATE, or LOW based on source convergence and tier. See
  `references/research-workflow.md` Phase 5.
- **Verify claims before finalizing.** Every quote, statistic, attribution,
  and superlative must be registered and verified. See
  `references/claim-verification.md`.
