---
name: Composable Pipeline Implementation
description: Implement runtime inline/delegate decisions for research pipeline stages with MANIFEST.md, test fixtures, and mode-conditional heuristics
type: plan
status: executing
related:
  - docs/designs/2026-03-13-composable-pipeline-design.md
  - docs/designs/2026-03-12-pipeline-subagents-design.md
  - skills/research/SKILL.md
  - skills/distill/SKILL.md
  - wos/research/assess_research.py
---

# Composable Pipeline Implementation

**Goal:** Enable the research pipeline orchestrator to run stages inline or
delegate to subagents at runtime, guided by mode-conditional heuristics.
Low-stakes research modes (historical, open-source, landscape) inline 5 of
7 stages, saving 25-40% dispatch overhead and 40-60% startup latency.
High-stakes modes (deep-dive, options, technical) preserve context isolation
where it matters.

**Scope:**

Must have:
- `MANIFEST.md` discovery index in `skills/_shared/references/`
- Standardized frontmatter (`stage`, `pipeline`) on all reference files
- Reference file contract sections (Purpose, Input, Methodology, Output, Gate)
- Test fixtures for each stage entry/exit state
- Gate-based pytest assertions for all fixtures
- Research SKILL.md updated with inline/delegate decision logic
- Mode-conditional heuristics table in SKILL.md
- Inline execution path for evaluator, synthesizer, finalizer
- Conditional inline for challenger (partial vs full challenge modes)
- Conditional inline for verifier (low-stakes vs high-stakes modes)
- Conditional inline for distill-worker (small vs large mappings)
- ~50% context pressure override rule
- Parallelization heuristic documented in SKILL.md
- MANIFEST.md referenced from research and distill SKILL.md frontmatter

Won't have:
- Runtime token counting / dynamic context pressure measurement (static defaults only for now)
- Changes to agent definitions (agents/ files unchanged)
- Changes to gate check logic (assess_research.py unchanged)
- Changes to distill mapper execution (mapper remains always-delegate)
- GitHub Copilot instructions file (.github/copilot-instructions.md — separate effort)
- Automated parity testing harness (manual parity verification during implementation)

**Approach:** Work bottom-up: first standardize the reference files and add
the discovery manifest, then build test fixtures that prove gate checks work
against known stage states, then update the research skill orchestrator with
decision logic and inline execution instructions. Each chunk is independently
verifiable and rolls back cleanly.

**File Changes:**
- Create: `skills/_shared/references/MANIFEST.md`
- Create: `tests/fixtures/research/gatherer_entry.md`
- Create: `tests/fixtures/research/gatherer_exit.md`
- Create: `tests/fixtures/research/evaluator_exit.md`
- Create: `tests/fixtures/research/challenger_exit.md`
- Create: `tests/fixtures/research/synthesizer_exit.md`
- Create: `tests/fixtures/research/verifier_exit.md`
- Create: `tests/fixtures/research/finalizer_exit.md`
- Create: `tests/test_research_gates.py`
- Modify: `skills/_shared/references/research/frame.md` (add frontmatter + contract sections)
- Modify: `skills/_shared/references/research/gather-and-extract.md` (add frontmatter + contract sections)
- Modify: `skills/_shared/references/research/verify-sources.md` (add frontmatter + contract sections)
- Modify: `skills/_shared/references/research/evaluate-sources-sift.md` (add stage/pipeline frontmatter)
- Modify: `skills/_shared/references/research/challenge.md` (add frontmatter + contract sections)
- Modify: `skills/_shared/references/research/synthesize.md` (add frontmatter + contract sections)
- Modify: `skills/_shared/references/research/self-verify-claims.md` (add frontmatter + contract sections)
- Modify: `skills/_shared/references/research/citation-reverify.md` (add stage/pipeline frontmatter)
- Modify: `skills/_shared/references/research/finalize.md` (add frontmatter + contract sections)
- Modify: `skills/_shared/references/research/research-modes.md` (add frontmatter)
- Modify: `skills/_shared/references/research/cli-commands.md` (add frontmatter)
- Modify: `skills/_shared/references/research/resumption.md` (add frontmatter)
- Modify: `skills/_shared/references/distill/distillation-guidelines.md` (add frontmatter)
- Modify: `skills/_shared/references/distill/mapping-guide.md` (add stage/pipeline frontmatter)
- Modify: `skills/research/SKILL.md` (add MANIFEST.md reference, inline/delegate decision logic)
- Modify: `skills/distill/SKILL.md` (add MANIFEST.md reference, conditional worker inline logic)

**Branch:** `feat/composable-pipeline`
**PR:** TBD

---

## Chunk 1: Reference File Standardization

### Task 1: Create MANIFEST.md

**Files:**
- Create: `skills/_shared/references/MANIFEST.md`

- [x] Write MANIFEST.md with stage-to-file mapping tables for research and
      distill pipelines, following the structure in the design doc (Section 3) <!-- sha:95d5bf4 -->
- [x] Include frontmatter: `name`, `description` <!-- sha:95d5bf4 -->
- [x] Verify: file exists and contains both `Research Pipeline References` and
      `Distill Pipeline References` tables <!-- sha:95d5bf4 -->
- [x] Commit <!-- sha:95d5bf4 -->

### Task 2: Add frontmatter to reference files missing it

**Files:**
- Modify: all 12 research reference files + 2 distill reference files

Currently only 3 of 14 reference files have frontmatter. Add `name`,
`description`, `stage`, and `pipeline` fields to all reference files.
For files that already have frontmatter (citation-reverify.md,
evaluate-sources-sift.md, mapping-guide.md), add the missing `stage`
and `pipeline` fields.

- [x] Add/update frontmatter on all 14 reference files with `name`,
      `description`, `stage`, `pipeline` fields <!-- sha:9982c79 -->
- [x] Verify: every `.md` file in `skills/_shared/references/research/` and
      `skills/_shared/references/distill/` starts with `---` frontmatter
      containing all four fields <!-- sha:9982c79 -->
- [x] Commit <!-- sha:9982c79 -->

### Task 3: Add contract sections to reference files

**Files:**
- Modify: reference files that serve as stage methodology (frame.md,
  gather-and-extract.md, verify-sources.md, evaluate-sources-sift.md,
  challenge.md, synthesize.md, self-verify-claims.md, citation-reverify.md,
  finalize.md)

Add Purpose, Input, Output, and Gate sections where missing. Do NOT
restructure existing Methodology content — only add the framing sections
around existing content. Supporting references (research-modes.md,
resumption.md, cli-commands.md) get Purpose sections only since they
are not standalone stages.

- [x] Add Purpose, Input, Output, Gate sections to each stage reference file
      (9 files). Preserve all existing methodology content verbatim. <!-- sha:a2ea89e -->
- [x] Add Purpose section to supporting reference files (research-modes.md,
      resumption.md, cli-commands.md, distillation-guidelines.md) <!-- sha:a2ea89e -->
- [x] Verify: no methodology content was removed or summarized (word count
      of methodology sections should not decrease) <!-- sha:a2ea89e -->
- [x] Commit <!-- sha:a2ea89e -->

### Task 4: Reference MANIFEST.md from skills

**Files:**
- Modify: `skills/research/SKILL.md` (add MANIFEST.md to references list)
- Modify: `skills/distill/SKILL.md` (add MANIFEST.md to references list)

- [x] Add `../_shared/references/MANIFEST.md` to the `references:` frontmatter
      in both SKILL.md files <!-- sha:b793868 -->
- [x] Verify: `grep -c MANIFEST skills/research/SKILL.md` returns 1 <!-- sha:b793868 -->
- [x] Verify: `grep -c MANIFEST skills/distill/SKILL.md` returns 1 <!-- sha:b793868 -->
- [x] Commit <!-- sha:b793868 -->

---

## Chunk 2: Test Fixtures and Gate Assertions

### Task 5: Create stage entry/exit test fixtures

**Files:**
- Create: `tests/fixtures/research/gatherer_entry.md`
- Create: `tests/fixtures/research/gatherer_exit.md`
- Create: `tests/fixtures/research/evaluator_exit.md`
- Create: `tests/fixtures/research/challenger_exit.md`
- Create: `tests/fixtures/research/synthesizer_exit.md`
- Create: `tests/fixtures/research/verifier_exit.md`
- Create: `tests/fixtures/research/finalizer_exit.md`

Each fixture is a minimal DRAFT research document at the expected state
for that stage boundary. Entry fixtures are the exit fixture of the
previous stage (evaluator_entry = gatherer_exit, etc.).

- [x] Write `gatherer_entry.md`: DRAFT marker, approved brief with
      sub-questions, no extracts, no sources table <!-- sha:091484f -->
- [x] Write `gatherer_exit.md`: DRAFT marker, sources table with URL column,
      extracts (blockquotes) for sub-questions <!-- sha:091484f -->
- [x] Write `evaluator_exit.md`: same as gatherer_exit + Tier and Status
      columns in sources table <!-- sha:091484f -->
- [x] Write `challenger_exit.md`: same as evaluator_exit + `## Challenge`
      section <!-- sha:091484f -->
- [x] Write `synthesizer_exit.md`: same as challenger_exit + `## Findings`
      section <!-- sha:091484f -->
- [x] Write `verifier_exit.md`: same as synthesizer_exit + `## Claims` table
      with rows, no `unverified` cells <!-- sha:091484f -->
- [x] Write `finalizer_exit.md`: DRAFT marker removed, `type: research` in
      frontmatter, non-empty `sources` <!-- sha:091484f -->
- [x] Verify: all 7 fixture files exist in `tests/fixtures/research/` <!-- sha:091484f -->
- [x] Commit <!-- sha:091484f -->

### Task 6: Write gate-based pytest assertions

**Files:**
- Create: `tests/test_research_gates.py`

One test per gate: load the exit fixture, run the corresponding gate check,
assert it passes. Also test that entry fixtures fail the exit gate (negative
test).

- [x] Write test file importing `check_single_gate` from
      `wos.research.assess_research` <!-- sha:d335d5b -->
- [x] Add parametrized test: for each `(gate_name, exit_fixture)` pair,
      verify `check_single_gate(fixture_path, gate_name)` returns
      `{"pass": True}` <!-- sha:d335d5b -->
- [x] Add negative test: `gatherer_entry.md` fails `gatherer_exit` gate <!-- sha:d335d5b -->
- [x] Run: `uv run python -m pytest tests/test_research_gates.py -v` — all pass <!-- sha:d335d5b -->
- [x] Commit <!-- sha:d335d5b -->

---

## Chunk 3: Inline Execution Logic

### Task 7: Add decision heuristics to research SKILL.md

**Files:**
- Modify: `skills/research/SKILL.md`

Add a new section between "Mode Detection" and "Workflow" that documents
the inline/delegate decision rules and the per-mode defaults table from the
design doc (Section 2). This gives the orchestrator the information it needs
to decide at runtime.

- [x] Add `## Execution Mode` section with:
      - Decision rules (ordered by priority): effort matches stakes,
        external I/O, user approval gate, context dependency benefit,
        token budget pressure (~50%), parallelization opportunity,
        methodology weight
      - Per-mode defaults table (which stages inline vs delegate per mode)
      - Override conditions per stage <!-- sha:99d6f57 -->
- [x] Verify: section contains the mode defaults table with all 8 research modes <!-- sha:99d6f57 -->
- [x] Verify: verifier row shows conditional (not always-delegate) <!-- sha:99d6f57 -->
- [x] Commit <!-- sha:99d6f57 -->

### Task 8: Update research workflow for inline execution path

**Files:**
- Modify: `skills/research/SKILL.md`

Update the Step 4 (Dispatch Research Chain) section to describe both
execution paths. When the mode decision says "inline", the orchestrator
reads the reference files listed in MANIFEST.md for that stage and
executes the methodology directly. When "delegate", dispatch the agent
as before. Gate checks run identically in both paths.

- [x] Update Step 4 to show both inline and delegate paths <!-- sha:994b776 -->
- [x] Add instructions for inline execution: read reference files for the
      stage (per MANIFEST.md), execute methodology in-thread, write results
      to DRAFT on disk, then run gate check <!-- sha:994b776 -->
- [x] Add the ~50% context pressure override: if context feels heavy after
      inline stages, switch remaining stages to delegate <!-- sha:994b776 -->
- [x] Add parallelization heuristic note: delegation is acceptable when
      parallel execution opportunities exist <!-- sha:994b776 -->
- [x] Verify: Step 4 mentions both "inline" and "delegate" execution paths <!-- sha:994b776 -->
- [x] Verify: gate check instructions are identical for both paths <!-- sha:994b776 -->
- [x] Commit <!-- sha:994b776 -->

### Task 8b: Add conditional worker inline to distill SKILL.md

**Files:**
- Modify: `skills/distill/SKILL.md`

Add execution mode logic to the distill skill. Mapper always delegates
(read-only, user approval gate). Worker is conditional: inline for small
mappings (1-3 context files) where the mapper's context carries useful
research understanding, delegate for large mappings (>3 files) where
write volume benefits from fresh context.

- [x] Add `## Execution Mode` section with worker decision heuristic <!-- sha:da76b65 -->
- [x] Update workflow step for worker dispatch to show both inline and
      delegate paths based on mapping size <!-- sha:da76b65 -->
- [x] Verify: section documents the 1-3 file threshold for inline <!-- sha:da76b65 -->
- [x] Commit <!-- sha:da76b65 -->

---

## Chunk 4: Validation

### Task 9: Run full test suite and audit

**Depends on:** Tasks 1-8

- [x] Run: `uv run python -m pytest tests/ -v` — all 317 tests pass
- [x] Run: `uv run scripts/audit.py --root .` — no new failures (5 pre-existing)
- [x] Verify SKILL.md body line count: `wc -l skills/research/SKILL.md` — 330 lines (under 500)
- [x] Read through the updated SKILL.md workflow to confirm inline/delegate
      paths are clear and unambiguous
- [x] No issues found, no fixes needed

---

## Validation

- [ ] `uv run python -m pytest tests/ -v` — all tests pass (no regressions)
- [ ] `uv run python -m pytest tests/test_research_gates.py -v` — all gate
      fixture tests pass
- [ ] `uv run scripts/audit.py --root .` — no failures
- [ ] `skills/_shared/references/MANIFEST.md` exists with both pipeline tables
- [ ] All 14 reference files have `stage` and `pipeline` in frontmatter
- [ ] `skills/research/SKILL.md` contains Execution Mode section with
      mode defaults table and inline/delegate workflow
- [ ] `skills/research/SKILL.md` references MANIFEST.md
- [ ] `skills/distill/SKILL.md` references MANIFEST.md and contains worker
      inline/delegate heuristic
- [ ] No changes to `agents/` directory (agent definitions unchanged)
- [ ] No changes to `wos/research/assess_research.py` (gate logic unchanged)
