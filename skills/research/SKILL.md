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
  - ../_shared/references/MANIFEST.md
---

# Research Skill

Conduct structured investigations using the SIFT framework (Stop,
Investigate the source, Find better coverage, Trace claims). Produces
research documents with verified sources and structured findings.
Save location follows the project's layout hint in AGENTS.md.

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

## Execution Mode

Each stage in the research chain can run **inline** (orchestrator executes
the methodology directly) or **delegate** (dispatch the named subagent).
Gate checks run identically in both paths. The decision is based on research
mode — effort matches stakes.

### Decision Rules (ordered by priority)

1. **Effort matches stakes.** High-stakes modes justify delegation overhead
   for accuracy-sensitive stages. Low-stakes modes inline aggressively.
2. **External I/O → delegate.** Stages using WebSearch/WebFetch benefit
   from dedicated context (gatherer, full-mode challenger).
3. **User approval gate → delegate.** Framer output goes to user review.
4. **Context dependency → inline.** Stages that benefit from prior context
   (evaluator, synthesizer) should run inline.
5. **Context pressure >~50% → delegate.** If context feels heavy after
   inline stages, switch remaining stages to delegate.
6. **Parallelization opportunity → delegate.** When concurrent execution
   is available, delegation enables parallel work.
7. **Methodology weight.** <80 lines → inline candidate. >100 lines → delegate.

### Mode Defaults

| Research Mode | Inline Stages | Delegated Stages |
|--------------|---------------|------------------|
| deep-dive | evaluator, synthesizer, finalizer | framer, gatherer, challenger, verifier |
| landscape | evaluator, challenger, synthesizer, verifier, finalizer | framer, gatherer |
| technical | evaluator, synthesizer, finalizer | framer, gatherer, challenger, verifier |
| feasibility | evaluator, synthesizer, finalizer | framer, gatherer, challenger, verifier |
| competitive | evaluator, synthesizer, finalizer | framer, gatherer, challenger, verifier |
| options | evaluator, synthesizer, finalizer | framer, gatherer, challenger, verifier |
| historical | evaluator, challenger, synthesizer, verifier, finalizer | framer, gatherer |
| open-source | evaluator, challenger, synthesizer, verifier, finalizer | framer, gatherer |

### Per-Stage Override Conditions

| Stage | Default | Override |
|-------|---------|---------|
| framer | delegate | — |
| gatherer | delegate | — |
| evaluator | inline | delegate if >15 sources |
| challenger | conditional | inline for partial challenge (landscape, historical, open-source); delegate for full challenge requiring WebSearch |
| synthesizer | inline | delegate if >8 sub-questions |
| verifier | conditional | delegate for high-stakes (deep-dive, options, technical, feasibility, competitive); inline for low-stakes (historical, open-source, landscape) |
| finalizer | inline | delegate if context pressure >~50% |

## Resumption Assessment

When resuming work on an existing research document, run the assessment
script before proceeding. This reports structural facts (word count, draft
marker, section presence, source count) so you can determine the current
state without re-reading the entire document.

**Single document (known file):**
```bash
python <plugin-skills-dir>/research/scripts/research_assess.py --file <path>
```

**Discovery (what's in progress?):**
```bash
python <plugin-skills-dir>/research/scripts/research_assess.py --scan --root .
```

Use the JSON output to determine which phase the document is in and what
actions to take next. Do not re-read the entire document if the assessment
provides sufficient context.

## Workflow

All modes follow the same workflow. The skill executes a chain of stages
(inline or delegated), running gate checks between each to validate
handoffs. All dispatch is foreground, sequential (no-nesting constraint).

### Step 1: Accept Research Question

Receive the research question from the user. Detect the research mode
(see Mode Detection above).

### Step 2: Compose and Dispatch Framer

Read the framer stage's reference files (per MANIFEST.md: frame.md,
research-modes.md). Compose the dispatch prompt using the prompt
composition pattern: role from MANIFEST.md, input (research question,
detected mode, project root), methodology from reference files, output
contract and constraints from frame.md. Dispatch with tools: Read, Glob,
Grep (per MANIFEST.md). The framer returns a structured brief (question,
mode, SIFT rigor, sub-questions, search strategy, suggested output
path).

### Step 3: Brief Approval

Present the brief to the user. If rejected, re-compose and dispatch
the framer with the user's feedback. Do not proceed without approval.

### Step 4: Execute Research Chain

Execute stages sequentially with gate validation between each. For each
stage, consult the Mode Defaults table (see Execution Mode above) to
determine whether to run inline or delegate. Gate checks are identical
in both paths.

**For each stage in the chain:**

1. **Check execution mode** — look up the stage in the Mode Defaults
   table for the detected research mode. Apply override conditions
   (e.g., >15 sources forces evaluator to delegate).
2. **Execute the stage:**
   - **Delegate:** Read the stage's reference files (per MANIFEST.md).
     Compose the dispatch prompt (role + entry gate + input + methodology
     + output + constraints from reference files). Dispatch with the
     tools listed in MANIFEST.md for that stage. The subagent starts
     with a fresh context.
   - **Inline:** Read the stage's reference files (per MANIFEST.md),
     then execute the methodology directly in-thread. Write results
     to the DRAFT file on disk, same as a delegated agent would.
3. **Run gate check:** `research_assess.py --file <path> --gate <stage>_exit`
4. **Proceed or retry** (see Step 5 for error handling).

```
DELEGATE gatherer (brief fields + output path)
  → Gate: research_assess.py --file <path> --gate gatherer_exit

INLINE or DELEGATE evaluator (path to DRAFT)
  → Gate: research_assess.py --file <path> --gate evaluator_exit

INLINE or DELEGATE challenger (path to DRAFT)
  → Gate: research_assess.py --file <path> --gate challenger_exit

INLINE or DELEGATE synthesizer (path to DRAFT)
  → Gate: research_assess.py --file <path> --gate synthesizer_exit

INLINE or DELEGATE verifier (path to DRAFT)
  → Gate: research_assess.py --file <path> --gate verifier_exit

INLINE or DELEGATE finalizer (path to DRAFT)
  → Gate: research_assess.py --file <path> --gate finalizer_exit
```

**Inline execution:** When running a stage inline, read the reference
files listed in MANIFEST.md for that stage. Follow the methodology
exactly as written — the reference file is the instruction set. Write
all output to the DRAFT file on disk. The gate check verifies the
result is structurally identical to what a delegated agent would produce.

**Context pressure override:** If context feels heavy after inline
stages (~50% utilization), switch remaining stages to delegate mode.
Do not force inline when context pressure risks degrading output quality.

**Parallelization note:** Delegation is also acceptable when parallel
execution opportunities exist — a delegated stage can run in a worktree
or background context while other work proceeds.

Announce each execution and gate result as the chain progresses:
```
Executing evaluator inline...
  → evaluator_exit gate: PASS (2/2 checks)
Delegating challenger...
  → challenger_exit gate: PASS (1/1 checks)
```

### Step 5: Error Handling Between Dispatches

After each stage completes, classify the gate check result:

| Result | Classification | Action |
|--------|---------------|--------|
| Gate PASS | Success | Dispatch next agent |
| Gate FAIL | Correctable | Re-dispatch with gate check JSON as context (max 2 retries, 3 total) |
| File unmodified | Structural | Escalate to user immediately |
| Agent returned error | Transient then correctable | Retry once without mutation, then with error context, then escalate |

On exhaustion (3 attempts), present to user:
- Agent name and phase
- Gate check output (which checks failed)
- Attempt history (what was tried)
- Suggested action: "Re-dispatch with guidance" or "skip and complete
  manually"

### Step 6: Completion

Present completion status to the user. The research document is at the
path selected during framing.

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

The final research document is saved with a `{date}-{slug}.research.md`
filename. Save location depends on the project's layout hint (read from
AGENTS.md `<!-- wos:layout: ... -->` comment):
- **separated**: `docs/research/`
- **co-located**: same directory as related documents
- **flat**: `docs/`
- **none** or missing: ask the user where to save
- User can always override the suggested location.

Frontmatter follows the document standards in AGENTS.md:

```yaml
---
name: "Title of the investigation"
description: "One-sentence summary of findings"
type: research
sources:
  - https://example.com/primary-source
related:
  - docs/research/2026-01-15-related-topic.research.md
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

## Key Instructions

- **Won't proceed without brief approval** — the Step 3 user approval gate is mandatory; no research stages execute until the user confirms the framing brief
- **Won't finalize without claim verification** — statistics, attributions, and superlatives must be traced to source before `<!-- DRAFT -->` is removed
- **Won't skip SIFT** — every source requires tier classification; un-tiered sources do not enter the document

## Key Rules

- **SIFT every source** — no source enters the document without tier classification. See `evaluate-sources-sift.md`.
- **Counter-evidence is required** for deep-dive, options, and technical modes. See `research-modes.md`.
- **Log every search** during Phase 2 and include the protocol in the final document.
- **Confidence levels on every finding** — HIGH, MODERATE, or LOW. See `synthesize.md`.
- **Verify all claims** before finalizing — quotes, statistics, attributions, superlatives. See `self-verify-claims.md` and `citation-reverify.md`.

## Anti-Pattern Guards

1. **Self-referential verification only** — CoVe (Chain-of-Verification) uses the same model that generated the error to check it. It is a first-pass filter, not a substitute for tool-based URL resolution. Every cited URL must be verified via HEAD request; CoVe alone is not sufficient for novel claims or post-cutoff information.
2. **Skipping the search protocol log** — research without a logged query trail cannot be reproduced or updated. Every search query, database, date, and result count must appear in the final document's protocol section. "I searched the web" is not a protocol.
3. **Omitting counter-evidence** — for deep-dive, options, and technical modes, a document with no counter-evidence signals incomplete coverage, not consensus. If no counter-evidence was found, state that explicitly with the searches attempted.
4. **Treating tier classification as final** — a T3 source can become T1 if it cites a primary study; a T1 source can be unreliable if the paper has been retracted. Tier is assigned at time of evaluation; claim confidence reflects the source tier at that moment, not the source's permanent standing.
5. **Finalizing without claim verification** — statistics, attributions, and superlatives ("the fastest", "the only") are the highest-risk claim types. Every such claim must be traced to its original source and verified to say what the document claims it says.

## Handoff

**Receives:** Topic or question to investigate; optional scope constraints or prior context files
**Produces:** Verified research document saved to `docs/research/` with sources, findings, and confidence ratings
**Chainable to:** distill, ingest, plan-work
