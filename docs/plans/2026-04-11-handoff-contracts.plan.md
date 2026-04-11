---
name: Add Handoff Contracts to All Skills
description: Add a standardized ## Handoff section (Receives / Produces / Chainable-to) to every existing SKILL.md — prerequisite for audit-chain
type: plan
status: executing
branch: feat/skill-refresh
pr: TBD
related:
  - docs/context/skill-handoff-contracts-and-state-design.context.md
  - docs/plans/2026-04-10-roadmap-v036-v039.plan.md
---

# Add Handoff Contracts to All Skills

**Goal:** Add a `## Handoff` section to all 14 existing SKILL.md files. Each section declares what the skill receives as input, what it produces as output, and which skills it naturally chains to. This makes chain design and audit tractable — `/wos:audit-chain` (Task 11) requires these contracts before it can verify chain consistency.

**Scope:**

Must have:
- `## Handoff` section in all 14 existing SKILL.md files
- All three fields present in each: `**Receives:**`, `**Produces:**`, `**Chainable to:**`
- Chainable-to values reference only valid existing skill names (or `—` for terminal)
- `python scripts/lint.py --root .` passes with no new warnings

Won't have:
- Changes to any non-SKILL.md files
- New skills (those come in Tasks 10–14 of the roadmap)
- New lint validation logic checking Handoff presence (that's in `wos/chain.py`, Task 9)
- Content changes to existing skill workflow or instruction text

**Approach:** Append a `## Handoff` section to each SKILL.md. Content is derived from each skill's existing workflow description and the chain table in issue #222. Skills are grouped into two logical chunks — the delivery chain and the knowledge/utility skills — each committed separately to create rollback boundaries. No code changes required.

**File Changes:**
- Modify: `skills/brainstorm/SKILL.md` (add `## Handoff`)
- Modify: `skills/write-plan/SKILL.md` (add `## Handoff`)
- Modify: `skills/execute-plan/SKILL.md` (add `## Handoff`)
- Modify: `skills/validate-work/SKILL.md` (add `## Handoff`)
- Modify: `skills/finish-work/SKILL.md` (add `## Handoff`)
- Modify: `skills/research/SKILL.md` (add `## Handoff`)
- Modify: `skills/distill/SKILL.md` (add `## Handoff`)
- Modify: `skills/ingest/SKILL.md` (add `## Handoff`)
- Modify: `skills/refine-prompt/SKILL.md` (add `## Handoff`)
- Modify: `skills/lint/SKILL.md` (add `## Handoff`)
- Modify: `skills/setup/SKILL.md` (add `## Handoff`)
- Modify: `skills/check-rules/SKILL.md` (add `## Handoff`)
- Modify: `skills/extract-rules/SKILL.md` (add `## Handoff`)
- Modify: `skills/retrospective/SKILL.md` (add `## Handoff`)

**Branch:** `feat/skill-refresh`
**PR:** TBD

---

## Chunk 1: Delivery Chain Skills

### Task 1: Add Handoff contracts — brainstorm, write-plan, execute-plan, validate-work, finish-work

**Files:**
- Modify: `skills/brainstorm/SKILL.md`
- Modify: `skills/write-plan/SKILL.md`
- Modify: `skills/execute-plan/SKILL.md`
- Modify: `skills/validate-work/SKILL.md`
- Modify: `skills/finish-work/SKILL.md`

- [x] **Step 1:** Read all five SKILL.md files to confirm current end-of-file structure and identify insertion point.
- [x] **Step 2:** Add to `skills/brainstorm/SKILL.md`:
  ```markdown
  ## Handoff

  **Receives:** User-described topic or problem to explore; optional seed research or constraints
  **Produces:** Design document saved to `docs/designs/` with structured requirements and scope boundaries
  **Chainable to:** write-plan, research
  ```
- [ ] **Step 3:** Add to `skills/write-plan/SKILL.md`:
  ```markdown
  ## Handoff

  **Receives:** Design doc path or feature description; optional issue number and roadmap context
  **Produces:** Implementation plan document saved to `docs/plans/` with tasks, file changes, and validation criteria
  **Chainable to:** execute-plan
  ```
- [ ] **Step 4:** Add to `skills/execute-plan/SKILL.md`:
  ```markdown
  ## Handoff

  **Receives:** Plan file path (`.plan.md`) with `status: approved`
  **Produces:** Implemented code and files per plan; plan tasks marked `[x]` with commit SHAs
  **Chainable to:** validate-work
  ```
- [ ] **Step 5:** Add to `skills/validate-work/SKILL.md`:
  ```markdown
  ## Handoff

  **Receives:** Plan file path (optional); validates current working state against plan criteria
  **Produces:** Validation report with pass/fail verdict per criterion
  **Chainable to:** finish-work (on pass), execute-plan (on fail)
  ```
- [ ] **Step 6:** Add to `skills/finish-work/SKILL.md`:
  ```markdown
  ## Handoff

  **Receives:** Plan file path; completed, validated implementation on a feature branch
  **Produces:** PR opened or merge completed; branch cleaned up; roadmap checkbox updated
  **Chainable to:** —
  ```
- [x] **Step 7:** Verify: `grep -L "## Handoff" skills/brainstorm/SKILL.md skills/write-plan/SKILL.md skills/execute-plan/SKILL.md skills/validate-work/SKILL.md skills/finish-work/SKILL.md` → empty output
- [x] **Step 8:** Commit: `git commit -m "feat: add Handoff contracts to delivery-chain skills"` <!-- sha:1d07916 -->

---

## Chunk 2: Knowledge Chain and Utility Skills

### Task 2: Add Handoff contracts — research, distill, ingest

**Files:**
- Modify: `skills/research/SKILL.md`
- Modify: `skills/distill/SKILL.md`
- Modify: `skills/ingest/SKILL.md`

- [x] **Step 1:** Read all three SKILL.md files to confirm current end-of-file structure.
- [x] **Step 2:** Add to `skills/research/SKILL.md`:
  ```markdown
  ## Handoff

  **Receives:** Topic or question to investigate; optional scope constraints or prior context files
  **Produces:** Verified research document saved to `docs/research/` with sources, findings, and confidence ratings
  **Chainable to:** distill, ingest, write-plan
  ```
- [x] **Step 3:** Add to `skills/distill/SKILL.md`:
  ```markdown
  ## Handoff

  **Receives:** Path to one or more research artifacts in `docs/research/`
  **Produces:** Focused context documents saved to `docs/context/`
  **Chainable to:** ingest, write-plan
  ```
- [x] **Step 4:** Add to `skills/ingest/SKILL.md`:
  ```markdown
  ## Handoff

  **Receives:** URL, file path, or pasted text representing an external source
  **Produces:** One or more wiki context pages added or updated under `docs/context/`
  **Chainable to:** lint
  ```
- [x] **Step 5:** Verify: `grep -L "## Handoff" skills/research/SKILL.md skills/distill/SKILL.md skills/ingest/SKILL.md` → empty output
- [x] **Step 6:** Commit: `git commit -m "feat: add Handoff contracts to knowledge-chain skills"` <!-- sha:868ce49 -->

### Task 3: Add Handoff contracts — refine-prompt, lint, setup, check-rules, extract-rules, retrospective

**Files:**
- Modify: `skills/refine-prompt/SKILL.md`
- Modify: `skills/lint/SKILL.md`
- Modify: `skills/setup/SKILL.md`
- Modify: `skills/check-rules/SKILL.md`
- Modify: `skills/extract-rules/SKILL.md`
- Modify: `skills/retrospective/SKILL.md`

- [x] **Step 1:** Read all six SKILL.md files to confirm current end-of-file structure.
- [x] **Step 2:** Add to `skills/refine-prompt/SKILL.md`:
  ```markdown
  ## Handoff

  **Receives:** Prompt text or file path to refine; optional target use-case context
  **Produces:** Refined prompt with assessment scores and improvement rationale; optionally saved to `docs/prompts/`
  **Chainable to:** (context-dependent)
  ```
- [x] **Step 3:** Add to `skills/lint/SKILL.md`:
  ```markdown
  ## Handoff

  **Receives:** Project root path (defaults to CWD); optional flags (--no-urls, --strict, --fix)
  **Produces:** Validation report listing warnings and failures by file; read-only — no modifications made
  **Chainable to:** —
  ```
- [x] **Step 4:** Add to `skills/setup/SKILL.md`:
  ```markdown
  ## Handoff

  **Receives:** Project root path (new or existing); optional communication preferences
  **Produces:** Initialized WOS project structure — AGENTS.md, docs/ directories, `_index.md` files
  **Chainable to:** lint
  ```
- [x] **Step 5:** Add to `skills/check-rules/SKILL.md`:
  ```markdown
  ## Handoff

  **Receives:** File path, directory, or list of git-changed files to check against project rules
  **Produces:** Rule compliance report listing violations with file and rule references
  **Chainable to:** —
  ```
- [x] **Step 6:** Add to `skills/extract-rules/SKILL.md`:
  ```markdown
  ## Handoff

  **Receives:** Convention description, code examples, or style-guide text to formalize
  **Produces:** Structured rule files saved to `docs/rules/`
  **Chainable to:** check-rules
  ```
- [x] **Step 7:** Add to `skills/retrospective/SKILL.md`:
  ```markdown
  ## Handoff

  **Receives:** Optional focus area or session context
  **Produces:** Structured feedback submitted as a GitHub Issue
  **Chainable to:** —
  ```
- [x] **Step 8:** Verify: `grep -L "## Handoff" skills/refine-prompt/SKILL.md skills/lint/SKILL.md skills/setup/SKILL.md skills/check-rules/SKILL.md skills/extract-rules/SKILL.md skills/retrospective/SKILL.md` → empty output
- [x] **Step 9:** Commit: `git commit -m "feat: add Handoff contracts to utility skills"` <!-- sha:dac0eb7 -->

---

### Task 4: Validate, update index, and finalize

- [x] **Step 1:** `grep -L "## Handoff" skills/*/SKILL.md` → empty output (all 14 covered)
- [x] **Step 2:** `grep -c "## Handoff" skills/*/SKILL.md | grep -v ":1"` → empty output (no duplicates)
- [x] **Step 3:** `python scripts/lint.py --root . --no-urls` → no new warnings or failures vs. pre-task baseline (index resync for new plan file)
- [ ] **Step 4:** Update roadmap checkbox: in `docs/plans/2026-04-10-roadmap-v036-v039.plan.md`, mark Task 6 complete with merge commit SHA once PR merges
- [x] **Step 5:** Commit <!-- sha:67767cc -->

---

## Validation

- [ ] `grep -L "## Handoff" skills/*/SKILL.md` — empty output (all 14 skills have the section)
- [ ] `python scripts/lint.py --root . --no-urls` — zero new failures or warnings vs. pre-change baseline
- [ ] Each Handoff section contains all three fields: `**Receives:**`, `**Produces:**`, `**Chainable to:**`
- [ ] `grep -c "## Handoff" skills/*/SKILL.md | grep -v ":1"` — empty output (exactly one section per file)

## Notes

- This plan is part of the `feat/skill-refresh` branch shared with Task 7 (skill refresh against v0.35.0 research). Task 7 must follow this task on the same branch.
- `distill` is not in the issue #222 chain table but exists on disk and must have a Handoff section per the acceptance criteria ("all SKILL.md files").
- `check-rules` and `extract-rules` are slated for deprecation in v0.38.0 (Task 12) but still exist and need contracts now.
- `retrospective` is also slated for deprecation in v0.38.0 (Task 15) but needs a contract for the same reason.
