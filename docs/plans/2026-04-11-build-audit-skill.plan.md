---
name: build-skill and audit-skill
description: Two skills for the skill development lifecycle — /wos:build-skill scaffolds new SKILL.md files, /wos:audit-skill quality-audits existing ones
type: plan
status: executing
branch: feat/build-audit-skill
pr: ~
related:
  - docs/context/instruction-file-authoring-anti-patterns.context.md
  - docs/context/instruction-file-extraction-techniques.context.md
  - docs/context/instruction-file-non-inferable-specificity.context.md
  - docs/context/instruction-capacity-and-context-file-length.context.md
  - docs/context/skill-progressive-loading-and-routing.context.md
  - docs/context/skill-handoff-contracts-and-state-design.context.md
  - docs/context/agent-facing-document-structure.context.md
  - docs/plans/2026-04-10-roadmap-v036-v039.plan.md
---

# /wos:build-skill + /wos:audit-skill

**Goal:** Users can scaffold valid SKILL.md files from a description and handoff contracts (`/wos:build-skill`), and quality-audit existing skills against research-backed criteria with opt-in repair (`/wos:audit-skill`). These two skills complete the build/audit pair for the WOS skill primitive, closing bcbeidel/wos#226.

**Scope:**

Must have:
- `skills/build-skill/SKILL.md` — scaffold a new skill from name + description + I/O contract
- `skills/audit-skill/SKILL.md` — audit a skill (or all skills) against ten quality criteria
- Both skills pass `scripts/lint.py` with no new failures or warnings
- `/wos:audit-skill` output format matches `scripts/lint.py` style (file, issue, severity)
- `/wos:audit-skill` opt-in improvement loop: propose a targeted edit per finding, apply on per-change confirmation

Won't have:
- New Python validators or changes to `wos/skill_audit.py` — audit checks are LLM-level judgments, not new static analysis
- Reference sub-files (`skills/build-skill/references/` or `skills/audit-skill/references/`) — single SKILL.md is sufficient for both
- Automated test coverage for the skills (skills are LLM instructions, not Python code)
- Deprecation of any existing skill

**Approach:** Both tasks are pure SKILL.md authoring — no Python changes. `/wos:build-skill` elicits name, description, I/O contract, and won't-haves (explicit negative rules prevent anti-pattern #8); reads relevant context files; runs the specificity test on each drafted rule; runs `scripts/lint.py`; and presents for approval. `/wos:audit-skill` runs ten checks per skill — eight LLM-level checks (structural + the HIGH-evidence content-quality anti-patterns from research) plus the two static checks already in `wos/skill_audit.py` — then offers an opt-in repair loop. Both skills are lean — target under 120 instruction lines each.

**File Changes:**
- Create: `skills/build-skill/SKILL.md`
- Create: `skills/audit-skill/SKILL.md`
- Modify: `docs/plans/2026-04-10-roadmap-v036-v039.plan.md` (check off Task 10 with merge SHA)

**Branch:** `feat/build-audit-skill`
**PR:** TBD

---

### Task 1: `skills/build-skill/SKILL.md`

**Files:**
- Create: `skills/build-skill/SKILL.md`

- [x] **Step 1:** Read for authoring context: <!-- sha:fbdabbe -->
  - `docs/context/instruction-file-authoring-anti-patterns.context.md`
  - `docs/context/instruction-file-non-inferable-specificity.context.md`
  - `docs/context/instruction-capacity-and-context-file-length.context.md`
  - `docs/context/skill-progressive-loading-and-routing.context.md`
  - One reference skill with good structure (e.g., `skills/write-plan/SKILL.md`) for structural reference

- [x] **Step 2:** Write `skills/build-skill/SKILL.md` with these sections: <!-- sha:fbdabbe -->
  - **Frontmatter:** `name: build-skill`, description front-loads the trigger phrase in the first sentence (Claude Code truncates descriptions at 250 chars — routing depends on the first sentence; use: "Scaffold a new SKILL.md from a description and I/O contract. Use when..."), `argument-hint: "[skill name and description]"`, `user-invocable: true`
  - **Handoff:** Receives (skill name + description + I/O contract from user); Produces (`skills/<name>/SKILL.md`); Chainable-to (`audit-skill`, `execute-plan`)
  - **Workflow:**
    1. **Elicit** — name, description, what it receives, what it produces, what it explicitly won't do (negative rules prevent anti-pattern #8 "missing negative rules"), and any context files to consult
    2. **Read context** — `docs/context/instruction-file-authoring-anti-patterns.context.md`, `docs/context/instruction-file-non-inferable-specificity.context.md`, and any user-specified context files
    3. **Draft SKILL.md** with all required sections (frontmatter, Handoff, Workflow, Anti-Pattern Guards, Key Instructions); apply the specificity test to each drafted rule: "Would removing this line cause the agent to make a mistake?" — cut rules that fail
    4. **Run lint** — `python scripts/lint.py --root <project-root>` and show any skill quality findings
    5. **Present for approval** — show draft to user; iterate on feedback
    6. **Write file** to `skills/<name>/SKILL.md` on approval; run reindex
  - **Anti-Pattern Guards:** (a) Writing the skill file before lint verification; (b) Skipping elicitation and guessing the I/O contract; (c) XML tags in description or body — use plain markdown; (d) Prescribing implementation instead of observable outcomes in Workflow steps; (e) Omitting won't-haves — missing negative rules are a documented anti-pattern; (f) Persona framing ("act as a senior X expert") — prefer specific rules over identity framing
  - **Key Instructions:** Scope is one skill per invocation. Do not create reference sub-files unless the skill body would exceed ~120 instruction lines. Description must front-load the primary trigger phrase — Claude Code routing depends on the first sentence (250-char truncation). Defer to existing lint thresholds — do not modify `scripts/lint.py`.

- [x] **Step 3:** Verify: `python scripts/lint.py --root . --no-urls 2>&1 | grep -A2 "build-skill"` — no failures; `wc -l skills/build-skill/SKILL.md` — under 150 lines <!-- sha:fbdabbe -->

- [x] **Step 4:** Commit: `git commit -m "feat: add /wos:build-skill SKILL.md"` <!-- sha:fbdabbe -->

---

### Task 2: `skills/audit-skill/SKILL.md`

**Files:**
- Create: `skills/audit-skill/SKILL.md`

- [x] **Step 1:** Read: <!-- sha:99b20d9 -->
  - `wos/skill_audit.py` — confirm which checks static analysis already covers (ALL-CAPS density ≥ 3, body >500 lines, description voice, name format); these are the baseline
  - `docs/context/instruction-file-authoring-anti-patterns.context.md` — the ranked anti-patterns drive checks 8–10
  - `docs/context/instruction-file-non-inferable-specificity.context.md` — the specificity test and removal test are the core quality filters

- [x] **Step 2:** Write `skills/audit-skill/SKILL.md` with these sections: <!-- sha:99b20d9 -->
  - **Frontmatter:** `name: audit-skill`, description front-loads the trigger phrase (e.g., "Audit an existing SKILL.md for quality issues. Use when..."), `argument-hint: "[path/to/SKILL.md or omit for all skills]"`, `user-invocable: true`
  - **Handoff:** Receives (path to SKILL.md, or no argument for all-skills audit); Produces (structured findings list in `scripts/lint.py` format); Chainable-to (`build-skill` for remediation, `execute-plan` for bulk repair)
  - **Input handling:** single path → audit that skill only; no argument → walk `skills/` and audit all non-`_shared` skills
  - **Ten checks** — run `scripts/lint.py` first for static checks; then LLM-level checks on the body:

    *Static (via `scripts/lint.py`):*
    1. **Body length** — warn if >500 instruction lines
    2. **ALL-CAPS directive density** — warn if ≥3 MUST/NEVER/ALWAYS/etc.; note that newer frontier models are more responsive to normal prompting — aggressive emphasis causes overtriggering

    *Structural (LLM-level):*
    3. **Handoff completeness** — `## Handoff` section present; all three fields (Receives / Produces / Chainable-to) populated
    4. **Anti-pattern guards** — `## Anti-Pattern Guards` section present with at least one guard
    5. **Gate checks** — at least one explicit gate (user approval, lint verification, precondition check) before a consequential step
    6. **Examples** — at least one concrete example (illustrative invocation, sample output, or table row with a real case)
    7. **Description routing quality** — first sentence front-loads the primary trigger phrase (Claude Code truncates at 250 chars); flag second-person or passive constructions

    *Content quality (LLM-level, from HIGH-evidence research anti-patterns):*
    8. **Vagueness** — each rule must produce a consistent decision; flag rules where two developers would make different choices in the same situation (anti-pattern #1, HIGH evidence)
    9. **Removal test** — for each significant rule, ask: "Would removing this line cause the agent to make a mistake?" Flag rules that fail — they are noise that dilutes compliance with the rules that matter (anti-pattern #3, HIGH evidence)
    10. **Persona framing** — flag "act as X" or "you are a senior X expert" constructions; prefer specific rules over identity framing (anti-pattern #9, MODERATE evidence; OpenSSF 2025 found persona framing reduces performance on the tasks it intends to improve)

  - **Output format:** findings table with columns: File | Issue | Severity. Severity summary (N fail, N warn) at top. Sort: fail before warn; structural before content-quality.
  - **Opt-in improvement loop:** after presenting findings, ask "Apply fixes? (y/n or comma-separated numbers)". For each selected finding, read the relevant section, propose a minimal specific edit, show the diff, and write the change only on confirmation. Re-run lint after each applied fix.
  - **Anti-Pattern Guards:** (a) Running LLM checks before `scripts/lint.py` — static checks run first, always; (b) Applying all fixes at once without per-change confirmation; (c) Silently skipping `skills/_shared/` — it is intentionally excluded
  - **Key Instructions:** Exclude `skills/_shared/` from all-skill audits. Do not modify `wos/skill_audit.py`. When proposing edits, fix the finding minimally — do not restructure surrounding content.

- [x] **Step 3:** Verify: `python scripts/lint.py --root . --no-urls 2>&1 | grep -A2 "audit-skill"` — no failures; `grep "## Handoff" skills/audit-skill/SKILL.md` — match found; `grep "## Anti-Pattern" skills/audit-skill/SKILL.md` — match found <!-- sha:99b20d9 -->

- [x] **Step 4:** Commit: `git commit -m "feat: add /wos:audit-skill SKILL.md"` <!-- sha:99b20d9 -->

---

### Task 3: Reindex and final validation

**Files:**
- Modify: `skills/_index.md` (auto-regenerated)

- [ ] **Step 1:** Run `python scripts/reindex.py --root .` to regenerate all `_index.md` files.

- [ ] **Step 2:** Verify: `python scripts/lint.py --root . --no-urls` — zero failures; no new warnings relative to pre-existing baseline

- [ ] **Step 3:** Verify: `grep "build-skill\|audit-skill" skills/_index.md` — both skills appear in the index

- [ ] **Step 4:** Commit: `git commit -m "chore: reindex after adding build-skill and audit-skill"`

---

## Validation

- [ ] `python scripts/lint.py --root . --no-urls` — zero failures, zero new warnings from `build-skill` or `audit-skill`
- [ ] `grep "## Handoff" skills/build-skill/SKILL.md skills/audit-skill/SKILL.md` — two matches (one per file)
- [ ] `grep "## Anti-Pattern" skills/build-skill/SKILL.md skills/audit-skill/SKILL.md` — two matches
- [ ] `grep "build-skill\|audit-skill" skills/_index.md` — both skills listed in the index
- [ ] `python -m pytest tests/ -v` — all existing tests pass (no regressions from reindex)

## Notes

- Closes bcbeidel/wos#226. When the PR merges, update Task 10 in `docs/plans/2026-04-10-roadmap-v036-v039.plan.md` with the merge commit SHA.
- No Python module changes. If future work wants static checks for handoff completeness or anti-pattern guards, that belongs in `wos/skill_audit.py`, not here.
- Parallel with Task 9 (chain infrastructure, `wos/chain.py`) — no file overlap. Both can merge to main independently before Task 11 depends on both.
