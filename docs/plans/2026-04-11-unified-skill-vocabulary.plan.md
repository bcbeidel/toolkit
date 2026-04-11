---
name: Unified Skill Vocabulary
description: Rename delivery pipeline and meta audit skills to consistent verb-object pairs, restore retrospective as standalone, and update all cross-references and documentation.
type: plan
status: completed
branch: feat/unified-skill-vocabulary
related: []
---

# Unified Skill Vocabulary

## Goal

Replace the ad-hoc mix of skill names (brainstorm, write-plan, execute-plan,
validate-work, audit-skill, audit-chain, …) with a consistent verb-object
vocabulary across the full WOS skill surface. The delivery pipeline becomes
`scope-work → plan-work → start-work → check-work → finish-work`. All
`audit-*` sub-skills become `check-*`, with `audit` (the orchestrator) and
`build-*` unchanged. `retrospective` is restored as an active standalone skill
nudged from `finish-work`. Every cross-reference, doc, and shared reference is
updated in the same branch so no skill name is orphaned at any commit.

## Scope

**Must have:**
- Skill directories renamed via `git mv` (10 renames: 4 pipeline + 6 meta)
- Every renamed `SKILL.md` updated: frontmatter `name`, description, internal
  skill references, announcement lines, handoff sections
- `skills/audit/SKILL.md` updated: all `audit-*` → `check-*` references
- `skills/build-*/SKILL.md` files (5) updated: `audit-*` counterpart → `check-*`
- `skills/finish-work/SKILL.md`: Step 2 script path `execute-plan` → `start-work`;
  Step 6 converted from inline retrospective to nudge toward `/wos:retrospective`
- `skills/retrospective/SKILL.md`: deprecation notice removed, restored as active
- `skills/_shared/references/plan-format.md` and `feedback-loop.md` updated
- Primary docs updated: `WORKFLOW.md`, `OVERVIEW.md`, `CLAUDE.md`, `PRINCIPLES.md`,
  `DEPLOYING.md`, `README.md`
- "chain" → "skill-chain" vocabulary in WORKFLOW.md Section 4, OVERVIEW.md,
  and `check-skill-chain/SKILL.md` — not the Python module or file extension
- `scripts/lint.py --root . --no-urls` clean pass after all changes
- `python -m pytest tests/ -v` clean pass after all changes

**Won't have:**
- Renaming `wos/chain.py`, `validate_chain()`, or any Python function/module
- Changing the `*.chain.md` file extension or `type: chain` frontmatter field
- Updates to completed historical plan documents in `docs/plans/`
- Updates to context or research documents that incidentally mention old names
- New skills, new features, or changes to Python business logic
- Changes to the `/wos:audit` orchestrator skill name or `/wos:finish-work` name

## Approach

All changes on branch `feat/unified-skill-vocabulary` (from main). Each task
ends with a commit to create rollback boundaries.

Order: rename pipeline skills first (each is self-contained), then meta skills,
then update the orchestrator (`audit`) and build counterparts, then retrospective
restore, then documentation. Shared references and validation come last to avoid
chasing moving targets mid-execution.

Reference files inside renamed skill directories (`skills/*/references/`) move
automatically with `git mv`. After each rename, grep the skill's own directory
for old skill names and update them in the same task.

## File Changes

**Skill directory renames:**
- `skills/brainstorm/` → `skills/scope-work/`
- `skills/write-plan/` → `skills/plan-work/`
- `skills/execute-plan/` → `skills/start-work/`
- `skills/validate-work/` → `skills/check-work/`
- `skills/audit-skill/` → `skills/check-skill/`
- `skills/audit-command/` → `skills/check-command/`
- `skills/audit-hook/` → `skills/check-hook/`
- `skills/audit-rule/` → `skills/check-rule/`
- `skills/audit-subagent/` → `skills/check-subagent/`
- `skills/audit-chain/` → `skills/check-skill-chain/`

**SKILL.md content edits (post-rename):**
- `skills/scope-work/SKILL.md` — name, description, handoff → `/wos:plan-work`
- `skills/plan-work/SKILL.md` — name, description, handoffs → `/wos:start-work`, infeasibility → `/wos:scope-work`
- `skills/start-work/SKILL.md` — name, announcement, handoff → `/wos:check-work`
- `skills/check-work/SKILL.md` — name, announcement
- `skills/check-skill/SKILL.md` — name, description
- `skills/check-command/SKILL.md` — name, description
- `skills/check-hook/SKILL.md` — name, description
- `skills/check-rule/SKILL.md` — name, description
- `skills/check-subagent/SKILL.md` — name, description
- `skills/check-skill-chain/SKILL.md` — name, description, skill-chain vocab, handoff → `/wos:start-work`
- `skills/audit/SKILL.md` — `audit-skill` → `check-skill`, `audit-rule` → `check-rule`, `audit-chain` → `check-skill-chain`
- `skills/build-skill/SKILL.md` — `audit-skill` → `check-skill`
- `skills/build-command/SKILL.md` — `audit-command` → `check-command`
- `skills/build-hook/SKILL.md` — `audit-hook` → `check-hook`
- `skills/build-rule/SKILL.md` — `audit-rule` → `check-rule`
- `skills/build-subagent/SKILL.md` — `audit-subagent` → `check-subagent`
- `skills/finish-work/SKILL.md` — Step 2 path → `start-work/scripts/plan_assess.py`; Step 6 → nudge to `/wos:retrospective`
- `skills/retrospective/SKILL.md` — remove deprecation blockquote + emit-notice; restore as active skill

**Reference files (review and update within renamed skills):**
- Any file under `skills/scope-work/references/` referencing `write-plan` → `plan-work`
- Any file under `skills/plan-work/references/` referencing `execute-plan` → `start-work` or `brainstorm` → `scope-work`
- Any file under `skills/start-work/references/` referencing `validate-work` → `check-work`
- `skills/start-work/scripts/plan_assess.py` — update path comment: `execute-plan` → `start-work`

**Shared references:**
- `skills/_shared/references/plan-format.md` — `write-plan` → `plan-work`, `execute-plan` → `start-work`, `validate-work` → `check-work`
- `skills/_shared/references/feedback-loop.md` — `brainstorm` → `scope-work`, `write-plan` → `plan-work`

**Documentation:**
- `OVERVIEW.md` — mermaid diagram, layer descriptions, skills table; restore retrospective as active
- `WORKFLOW.md` — all five sections; "chain" → "skill-chain" in Section 4; skill name updates throughout
- `CLAUDE.md` — pipeline description in Architecture section; WORKFLOW.md inline reference
- `PRINCIPLES.md` — pipeline description
- `DEPLOYING.md` — `brainstorm/` path reference → `scope-work/`
- `README.md` — skill count (currently "12 active + 1 deprecated" → 13 active)

## Tasks

## Chunk 1: Pipeline Skill Renames

### Task 1: Rename `brainstorm` → `scope-work`

- [x] **Step 1:** `git mv skills/brainstorm skills/scope-work` <!-- sha:de6ce71 -->
- [x] **Step 2:** Update `skills/scope-work/SKILL.md` <!-- sha:de6ce71 -->
- [x] **Step 3:** Grep and update cross-references inside the skill directory <!-- sha:de6ce71 -->
- [x] **Step 4:** Verify <!-- sha:de6ce71 -->
- [x] **Step 5:** Lint check <!-- sha:de6ce71 -->
- [x] **Step 6:** Commit <!-- sha:de6ce71 -->

---

### Task 2: Rename `write-plan` → `plan-work`

- [x] **Step 1–6:** Complete <!-- sha:8a7a15b -->

---

### Task 3: Rename `execute-plan` → `start-work`

- [x] **Step 1–7:** Complete <!-- sha:74a9a10 -->

---

### Task 4: Rename `validate-work` → `check-work`

- [x] **Step 1–6:** Complete <!-- sha:aeebd76 -->

---

## Chunk 2: Meta Skill Renames

### Task 5: Rename `audit-skill`, `audit-command`, `audit-hook`

- [x] **Step 1–5:** Complete <!-- sha:cde6e87 -->

---

### Task 6: Rename `audit-rule`, `audit-subagent`

- [x] **Step 1–5:** Complete <!-- sha:0e6a186 -->

---

### Task 7: Rename `audit-chain` → `check-skill-chain`

- [x] **Step 1–5:** Complete <!-- sha:9137c5a -->

---

## Chunk 3: Orchestrator and Build Cross-References

### Task 8: Update `/wos:audit` orchestrator

- [x] **Step 1–4:** Complete <!-- sha:892292e -->

---

### Task 9: Update `build-*` skill cross-references

- [x] **Step 1–4:** Complete <!-- sha:3f8c162 -->

---

## Chunk 4: Retrospective and Finish-Work

### Task 10: Restore `retrospective` as active standalone skill

- [x] **Step 1–3:** Complete <!-- sha:bd8dd08 -->

---

### Task 11: Update `finish-work` — script path and Step 6 nudge

- [x] **Step 1–4:** Complete <!-- sha:959f0eb -->

---

## Chunk 5: Shared References

### Task 12: Update shared reference files

- [x] **Step 1–5:** Complete <!-- sha:6e768b9 -->

---

## Chunk 6: Primary Documentation

### Task 13: Update `OVERVIEW.md`

- [x] **Step 1–6:** Complete <!-- sha:0500715 -->

---

### Task 14: Update `WORKFLOW.md`

- [x] **Step 1–7:** Complete <!-- sha:1542764 -->

---

### Task 15: Update `CLAUDE.md`, `PRINCIPLES.md`, `DEPLOYING.md`, `README.md`

- [x] **Step 1–6:** Complete <!-- sha:13bdca7 -->

---

## Chunk 7: Validation

### Task 16: Full validation pass

- [x] **Step 1:** lint — 1 pre-existing fail (fixture), 7 pre-existing warns <!-- sha:ec03402 -->
- [x] **Step 2:** 441 tests pass, 0 failures <!-- sha:ec03402 -->
- [x] **Step 3:** Spot-check grep — additional refs found and fixed (check-rule, check-skill, check-subagent, distill, research, setup, OVERVIEW.md) <!-- sha:ec03402 -->
- [x] **Step 4:** Reindex — `_index.md` files regenerated <!-- sha:ec03402 -->
- [x] **Step 5:** Post-reindex lint — clean <!-- sha:ec03402 -->
- [x] **Step 6:** Commit <!-- sha:ec03402 -->

---

## Validation

```bash
# 1. No old pipeline skill names remain in active files
grep -r 'brainstorm\|write-plan\|execute-plan\|validate-work' \
  skills/*/SKILL.md WORKFLOW.md OVERVIEW.md CLAUDE.md README.md PRINCIPLES.md DEPLOYING.md
# Expected: 0 matches

# 2. No old audit-* sub-skill names remain in active files
grep -r 'audit-skill\|audit-command\|audit-hook\|audit-rule\|audit-subagent\|audit-chain' \
  skills/*/SKILL.md WORKFLOW.md OVERVIEW.md CLAUDE.md README.md PRINCIPLES.md DEPLOYING.md
# Expected: 0 matches

# 3. All renamed skill directories present
ls skills/scope-work/SKILL.md skills/plan-work/SKILL.md skills/start-work/SKILL.md \
   skills/check-work/SKILL.md skills/check-skill/SKILL.md skills/check-command/SKILL.md \
   skills/check-hook/SKILL.md skills/check-rule/SKILL.md skills/check-subagent/SKILL.md \
   skills/check-skill-chain/SKILL.md
# Expected: all 10 exist

# 4. Old skill directories absent
ls skills/brainstorm skills/write-plan skills/execute-plan skills/validate-work \
   skills/audit-skill skills/audit-command skills/audit-hook skills/audit-rule \
   skills/audit-subagent skills/audit-chain 2>&1 | grep 'No such'
# Expected: all 10 "No such file" errors

# 5. Retrospective has no deprecation markers
grep -c 'Deprecated\|deprecated' skills/retrospective/SKILL.md
# Expected: 0

# 6. finish-work references start-work path and nudges retrospective
grep 'start-work/scripts/plan_assess.py' skills/finish-work/SKILL.md
grep '/wos:retrospective' skills/finish-work/SKILL.md
# Expected: 1 match each

# 7. Full lint pass
python scripts/lint.py --root . --no-urls
# Expected: zero failures

# 8. Full test suite
python -m pytest tests/ -v
# Expected: all pass
```
