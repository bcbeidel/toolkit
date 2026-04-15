---
name: Simplify Validation Architecture
description: Replace grep-equivalent Python validation with self-contained shell scripts; strip parallel dispatch and table parsing from Python assessment modules; delete /distill and related artifacts; create a clean baseline for the toolkit restructure.
type: plan
status: executing
branch: simplify/validation-architecture
related:
  - docs/plans/2026-04-14-restructure-toolkit-marketplace.plan.md
---

# Simplify Validation Architecture

## Goal

Remove /distill, every cross-skill Python dependency that only does what
grep can do, and all complexity in the assessment modules that goes beyond
section-presence checks. The result: workflow validation is shell scripts,
assessment modules are thin wrappers around string matching, and no skill
calls a script outside its own plugin boundary.

This completes before the toolkit restructure — it is the prerequisite
that makes restructuring safe.

## Scope

**Must have:**
- Delete `/distill` skill and all associated artifacts
- Delete `parallel-dispatch.md` and the parallel execution path from start-work; always sequential
- Delete `research-distill-pipeline.md` from start-work references
- Update all Handoff/Chainable mentions of `distill` across skills
- Simplify `wos/plan/assess_plan.py` — remove file overlap detection, task-to-file mapping, `parallel_eligible`; keep task counting and section presence only
- Simplify `wos/research/assess_research.py` — remove all table parsing helpers; replace table-column gate checks with section-presence and string matching
- Replace `lint.py` + `reindex.py` calls in `finalize.md` with a self-contained shell script
- Remove `get_version.py` and its Phase 3 call in retrospective workflow
- Fix ingest's hardcoded `python scripts/` paths to use `<plugin-scripts-dir>`
- Replace `plan_assess.py` task-completion check in check-work with a shell script
- Add `validate_plan.sh` to plan-work's verification step
- Update tests for all changed and deleted code

**Won't have:**
- Making `reindex.py` or `lint.py` fully self-contained (warrant Python; separate refactor)
- Toolkit restructure itself (covered by `2026-04-14-restructure-toolkit-marketplace.plan.md`)

## Approach

Work in five chunks: **delete first**, then **simplify the Python
modules**, then **create shell scripts**, then **wire skills to use
them**, then **verify clean state**.

**What stays Python and why:**
- `assess_plan.py` — task counting with SHA extraction, section detection,
  status parsing, `scan_plans()` for multi-session resumption. Outputs
  structured JSON the LLM parses. Regex over checkbox lines is cleaner
  in Python than bash.
- `assess_research.py` — phase gate checking with section detection and
  string matching. Outputs structured JSON. Stays Python for the JSON
  output format used by research subagents.
- `reindex.py` — generates formatted `_index.md` from directory contents.
  Requires frontmatter parsing + markdown generation.
- `lint.py` — full project sweep: URL checking, index sync, skill quality
  metrics. Warrants Python.

**What the shell scripts replace:**
- Section existence checks ("does this file have ## Findings?") — grep
- Field presence checks ("is DRAFT marker absent?") — grep
- Task completion checks ("are all `- [ ]` boxes checked?") — grep -c

**Reindex responsibility:** After this plan, reindex is no longer triggered
mid-workflow. `/ingest` handles it after content writes. Research finalize
does not call reindex.

**Simplified gate logic for `assess_research.py`:**
- Gatherer: DRAFT present, Sources section exists, URLs in file, extracts (blockquotes/sub-headings) present
- Evaluator: "Tier" and "Status" appear as text in the sources area (string match, not column parse)
- Challenger: `## Challenge` heading exists
- Synthesizer: `## Findings` heading exists
- Verifier: `## Claims` heading exists AND `unverified` absent from file (whole-file, not column-specific)
- Finalizer: DRAFT absent, `type: research` in frontmatter, sources non-empty

## File Changes

**Delete:**
- `skills/distill/SKILL.md`
- `skills/distill/_index.md`
- `skills/_shared/references/distill/distillation-guidelines.md`
- `skills/_shared/references/distill/mapping-guide.md`
- `skills/_shared/references/distill/_index.md`
- `skills/start-work/references/parallel-dispatch.md`
- `skills/start-work/references/research-distill-pipeline.md`
- `scripts/get_version.py`
- `tests/test_get_version.py`

**Create:**
- `skills/research/scripts/validate_finalize.sh`
- `skills/start-work/scripts/validate_plan.sh`
- `skills/start-work/scripts/check_tasks_complete.sh`

**Modify:**
- `wos/plan/assess_plan.py` — remove `_extract_file_changes`, `_map_task_files`, `_find_overlaps`, `_FILE_CHANGE_RE`, `_TASK_HEADING_RE`; remove `file_changes` and `parallel_eligible` from output
- `wos/research/assess_research.py` — remove `_find_table_under_heading`, `_table_columns`, `_table_data_rows`; simplify `_check_gatherer_exit`, `_check_evaluator_exit`, `_check_verifier_exit`
- `skills/_shared/references/research/finalize.md` — replace script calls in step 5
- `skills/start-work/SKILL.md` — remove distill section, remove parallel section (step 4), remove both refs from frontmatter
- `skills/research/SKILL.md` — remove `distill` from Chainable to
- `skills/build-skill/SKILL.md` — remove `distill` from Chainable to
- `skills/setup/SKILL.md` — remove `research → distill` example
- `skills/retrospective/references/retrospective-workflow.md` — remove get_version.py call
- `skills/ingest/SKILL.md` — fix hardcoded script paths
- `skills/plan-work/SKILL.md` — add validate_plan.sh to step 5 verification
- `skills/check-work/SKILL.md` — replace plan_assess.py in step 2 with check_tasks_complete.sh
- `tests/test_plan_assess.py` — remove overlap/parallel tests
- `tests/test_research_assess.py` — update for simplified gate checks
- `tests/test_research_gates.py` — rewrite for simplified gates

## Tasks

### Chunk 1: Delete /distill and dead artifacts

- [x] Task 1: Delete the `skills/distill/` directory entirely (SKILL.md + <!-- sha:e8807d8 -->
  _index.md). Update `skills/research/SKILL.md` Handoff — change
  "Chainable to: distill, ingest, plan-work" to "Chainable to: ingest,
  plan-work". Update `skills/build-skill/SKILL.md` Handoff — remove
  "distill (to extract workflow context before drafting)". Update
  `skills/setup/SKILL.md` — remove the "research → distill" example.
  **Verify:** `ls skills/distill/ 2>&1` → "No such file or directory";
  `grep -r "Chainable.*distill" skills/` → no output

- [x] Task 2: Delete the `skills/_shared/references/distill/` directory <!-- sha:be39e21 -->
  (distillation-guidelines.md + mapping-guide.md + _index.md).
  **Verify:** `ls skills/_shared/references/distill/ 2>&1` → "No such file or directory"

- [x] Task 3: Delete `skills/start-work/references/parallel-dispatch.md`. <!-- sha:67cf929 -->
  Delete `skills/start-work/references/research-distill-pipeline.md`.
  From `start-work/SKILL.md` frontmatter `references:` list, remove both
  `- references/parallel-dispatch.md` and
  `- references/research-distill-pipeline.md`.
  **Verify:** `ls skills/start-work/references/parallel-dispatch.md 2>&1` → "No such file or directory";
  `ls skills/start-work/references/research-distill-pipeline.md 2>&1` → "No such file or directory"

- [x] Task 4: Update `skills/start-work/SKILL.md` body: <!-- sha:91f2ce9 -->
  (a) Remove the research-distill pipeline section (5-step phased list,
  currently lines ~96-103). Replace with one line: "For research tasks,
  invoke `/wiki:research` per task; the skill manages its own pipeline
  and validation internally."
  (b) Remove the Parallel execution path from step 4 (Choose Execution
  Mode). Replace the entire step with: "Execute tasks sequentially in
  the order listed."
  **Verify:** `grep -c "distill\|parallel\|Parallel" skills/start-work/SKILL.md` → 0

- [x] Task 5: Delete `scripts/get_version.py` and `tests/test_get_version.py`. <!-- sha:dc7c2aa -->
  Update `skills/retrospective/references/retrospective-workflow.md` Phase 3
  — remove `python <plugin-scripts-dir>/get_version.py`; replace with:
  "Read `<plugin-root>/plugin.json` and extract the `version` field."
  **Verify:** `ls scripts/get_version.py 2>&1` → "No such file or directory";
  `grep "get_version" skills/retrospective/references/retrospective-workflow.md` → no output

### Chunk 2: Simplify Python assessment modules

- [x] Task 6: Simplify `wos/plan/assess_plan.py`. Remove the three <!-- sha:07043f0 -->
  file-overlap functions and their supporting regexes:
  - Delete `_extract_file_changes()`, `_map_task_files()`, `_find_overlaps()`
  - Delete `_FILE_CHANGE_RE` and `_TASK_HEADING_RE` constants
  - Remove `file_changes` dict entirely from `assess_file()` return value
  - Remove `parallel_eligible` from `readiness` dict in `assess_file()`
  Keep: `_parse_tasks()`, `_detect_sections()`, `assess_file()` (simplified),
  `scan_plans()`. Update `tests/test_plan_assess.py` — delete all tests
  for `_extract_file_changes`, `_map_task_files`, `_find_overlaps`, and
  `parallel_eligible`; remaining tests should pass unchanged.
  **Verify:** `python -m pytest tests/test_plan_assess.py -v` → all pass;
  `grep -c "parallel_eligible\|overlapping_tasks\|file_changes" wos/plan/assess_plan.py` → 0

- [x] Task 7: Simplify `wos/research/assess_research.py`. Remove the three <!-- sha:ef351b7 -->
  table parsing helpers:
  - Delete `_find_table_under_heading()`, `_table_columns()`, `_table_data_rows()`
  Replace the three table-dependent gate checks with string/section matching:
  - `_check_gatherer_exit()`: DRAFT present + `## Sources` heading exists +
    file contains `http` + `_has_extracts()` still applies (keep that helper)
  - `_check_evaluator_exit()`: file contains the text "Tier" AND "Status"
    within the document (whole-file string match, not column parse)
  - `_check_verifier_exit()`: `## Claims` heading exists AND `"unverified"`
    absent from the entire file (whole-file, case-insensitive)
  Leave `_check_challenger_exit`, `_check_synthesizer_exit`,
  `_check_finalizer_exit` unchanged (already simple).
  Rewrite `tests/test_research_gates.py` and update `tests/test_research_assess.py`
  to reflect the simplified gate logic.
  **Verify:** `python -m pytest tests/test_research_assess.py tests/test_research_gates.py -v` → all pass;
  `grep -c "_find_table_under_heading\|_table_columns\|_table_data_rows" wos/research/assess_research.py` → 0

### Chunk 3: Research self-contained validation

- [x] Task 8: Create `skills/research/scripts/validate_finalize.sh`. Accepts <!-- sha:be0c1d9 -->
  a single file path argument; exits 1 printing which check failed:
  1. `name:` present in frontmatter
  2. `description:` present in frontmatter
  3. `type: research` in frontmatter
  4. Sources block contains at least one URL
  5. `<!-- DRAFT -->` marker absent
  Exit 0 with "OK: research document valid" on all pass. Make executable.
  **Verify:** Run against a valid `.research.md` → exit 0;
  run against a file containing `<!-- DRAFT -->` → exit 1 with message

- [x] Task 9: Update `skills/_shared/references/research/finalize.md` step 5. <!-- sha:pending -->
  Replace:
  ```bash
  python <plugin-scripts-dir>/reindex.py --root .
  python <plugin-scripts-dir>/lint.py <file> --root . --no-urls
  ```
  with:
  ```bash
  bash <plugin-skills-dir>/research/scripts/validate_finalize.sh <file>
  ```
  Add note: "Reindex is no longer triggered here. Run `/wiki:ingest` after a
  research session to sync `_index.md` files."
  **Verify:** `grep -c "reindex\|lint\.py" skills/_shared/references/research/finalize.md` → 0

- [x] Task 10: Update `skills/ingest/SKILL.md` Post-Ingest section. Fix: <!-- sha:pending -->
  - `python scripts/lint.py` → `python <plugin-scripts-dir>/lint.py`
  - `python scripts/reindex.py` → `python <plugin-scripts-dir>/reindex.py`
  **Verify:** `grep -c "python scripts/" skills/ingest/SKILL.md` → 0

### Chunk 4: Work chain shell validation

- [ ] Task 11: Create `skills/start-work/scripts/validate_plan.sh`. Checks that
  all 6 required headings exist (Goal, Scope, Approach, File Changes, Tasks,
  Validation) and that a `status:` field is in the frontmatter. Prints each
  missing item with "MISSING:" prefix. Exit 1 if any fail; exit 0 with
  "OK: plan structure valid". Make executable.
  **Verify:** Run against this plan file → exit 0;
  run against a file missing `## Validation` → exit 1 with "MISSING: Validation"

- [ ] Task 12: Create `skills/start-work/scripts/check_tasks_complete.sh`.
  Counts `^- \[ \]` lines. Exit 0 with "OK: all tasks complete" if count is 0.
  Exit 1 with the count and each open task line if any remain. Make executable.
  **Verify:** Run against this plan file → exit 1 with open task list;
  run against a file with all `[x]` boxes → exit 0

- [ ] Task 13: Update `skills/plan-work/SKILL.md` step 5 (Review with User) —
  add a pre-check: "Run `bash <plugin-skills-dir>/start-work/scripts/validate_plan.sh
  <plan-file>` to confirm all required sections are present before presenting."
  **Verify:** `grep -q "validate_plan.sh" skills/plan-work/SKILL.md`

- [ ] Task 14: Update `skills/check-work/SKILL.md` step 2 (Plan Preconditions) —
  replace the `plan_assess.py` call with:
  ```bash
  bash <plugin-skills-dir>/start-work/scripts/check_tasks_complete.sh <path>
  ```
  Update surrounding prose: script exits 1 and prints open task lines if
  tasks remain; exit 0 means all complete. Remove JSON parsing instruction.
  `plan_assess.py` remains in start-work step 1 (task counting, status,
  section detection for orchestration) — do not touch that call.
  **Verify:** `grep -c "plan_assess.py" skills/check-work/SKILL.md` → 0

### Chunk 5: Tests and clean state

- [ ] Task 15: Run `python scripts/reindex.py --root .` to regenerate `_index.md`
  files after all deletions. Run the full test suite.
  **Verify:** `python -m pytest tests/ -v` → 0 failures

- [ ] Task 16: Run the full lint check to confirm zero structural regressions.
  **Verify:** `python scripts/lint.py --root . --no-urls` → 0 fail findings

## Validation

1. `ls skills/distill/ 2>&1` → "No such file or directory"
2. `ls skills/_shared/references/distill/ 2>&1` → "No such file or directory"
3. `grep -r "Chainable.*distill" skills/` → no output
4. `grep -c "parallel_eligible\|overlapping_tasks" wos/plan/assess_plan.py` → 0
5. `grep -c "_find_table_under_heading\|_table_columns\|_table_data_rows" wos/research/assess_research.py` → 0
6. `bash skills/research/scripts/validate_finalize.sh <valid-research-doc>` → exit 0
7. `bash skills/research/scripts/validate_finalize.sh <file-with-DRAFT>` → exit 1 with message
8. `bash skills/start-work/scripts/check_tasks_complete.sh <plan-with-open-tasks>` → exit 1
9. `python -m pytest tests/ -v` → 0 failures
10. `python scripts/lint.py --root . --no-urls` → 0 fail findings
