---
name: /wos:audit Orchestrator
description: Create the /wos:audit skill as the top-level project health orchestrator combining lint, audit-skill, audit-rule, audit-chain, and wiki validation into a prioritized report
type: plan
status: completed
branch: feat/audit-orchestrator
pr: TBD
related:
  - docs/plans/2026-04-10-roadmap-v036-v039.plan.md
---

# /wos:audit Orchestrator

**Goal:** Add `/wos:audit` as the top-level project health skill. It orchestrates `scripts/lint.py` (deterministic structural checks) with LLM-judgment from the audit family — audit-skill, audit-rule, audit-chain, and wiki validation — and produces a single prioritized health report. This closes the self-improvement loop: lint catches broken structure, `/wos:audit` catches degraded quality.

**Scope:**

Must have:
- `skills/audit/SKILL.md` implementing the full five-step orchestration workflow
- Severity mapping: lint failures → Critical; skill/rule findings → High/Medium; chain/wiki findings → Medium/Low
- Conditional steps: audit-chain only when `*.chain.md` files exist; wiki validation only when `wiki/SCHEMA.md` exists
- Consolidated report with Critical/High/Medium/Low tiers
- Opt-in repair offer after the report ("address findings in priority order")
- `OVERVIEW.md` updated with the new `/wos:audit` row

Won't have:
- New Python scripts or changes to `wos/validators.py`
- Changes to any existing skill SKILL.md
- Automated fix application without user interaction (the repair offer is opt-in)
- Execution of sub-audits in parallel (sequential is sufficient; avoids interleaved output)

**Approach:** One new SKILL.md that orchestrates existing primitives. The skill dispatches to `scripts/lint.py` first (fast, deterministic), then calls audit-skill, audit-rule, audit-chain (conditional), and wiki validation (conditional) in sequence. Each sub-audit's findings are tagged with a severity tier before being merged into the consolidated report. No new Python code required — this is entirely a skill-layer orchestration.

**Severity mapping:**

| Source | Finding tier |
|--------|-------------|
| `scripts/lint.py` fail | Critical |
| `scripts/lint.py` warn | High |
| audit-skill fail/warn | High/Medium |
| audit-rule fail/warn | High/Medium |
| audit-chain fail/warn | Medium/High |
| wiki fail/warn | Medium/Low |

**File Changes:**
- Create: `skills/audit/SKILL.md`
- Modify: `OVERVIEW.md` (add `/wos:audit` row to skills reference table)

**Branch:** `feat/audit-orchestrator`
**PR:** TBD

---

### Task 1: Create `skills/audit/SKILL.md`

**Files:**
- Create: `skills/audit/SKILL.md`

- [x] **Step 1:** Create `skills/audit/` directory and write `SKILL.md` with the following structure: <!-- sha:25f393e -->
  - Frontmatter: `name: audit`, description, `argument-hint`, `user-invocable: true`
  - **Announce step:** instruct skill to announce "I'm using the `/wos:audit` skill..."
  - **Step 1 — Structural check:** run `python <plugin-scripts-dir>/lint.py --root . --no-urls`; collect all findings; tag lint `fail` as Critical, lint `warn` as High
  - **Step 2 — Skill quality:** run `/wos:audit-skill` (no argument = all skills); collect findings; tag skill `fail` as High, skill `warn` as Medium
  - **Step 3 — Rule quality:** discover rules (`docs/rules/*.rule.md`, `.cursor/rules/*.mdc`, `CLAUDE.md ## Rule:` sections); if any exist, run `/wos:audit-rule`; tag rule `fail` as High, rule `warn` as Medium; if none, skip and note
  - **Step 4 — Chain health (conditional):** check for `*.chain.md` files; if present, run `/wos:audit-chain` on each; tag chain `fail` as High, chain `warn` as Medium; if none, skip and note
  - **Step 5 — Wiki health (conditional):** check for `wiki/SCHEMA.md`; if present run wiki validation via `python <plugin-scripts-dir>/lint.py --root . --no-urls` (wiki checks run automatically); tag wiki `fail` as Medium, wiki `warn` as Low; if absent, skip and note
  - **Step 6 — Consolidated report:** emit report with four tiers (Critical / High / Medium / Low); each finding includes the source sub-check and file reference; "No critical issues found" when Critical tier is empty; "All checks passed." when all four tiers are empty
  - **Step 7 — Repair offer:** ask "Would you like to address these findings now? I'll work through them in priority order." If yes, start at Critical, call the relevant sub-audit skill's repair loop for each finding tier
  - `## Anti-Pattern Guards` section (at least: don't run LLM checks before lint; don't auto-apply fixes; don't run audit-chain/wiki when no files exist)
  - `## Handoff` section: Receives (project root; defaults to CWD), Produces (prioritized health report; optionally triggers sub-skill repair loops), Chainable-to (lint, audit-skill, audit-rule, audit-chain)

- [x] **Step 2:** Verify: `python scripts/lint.py --root . --no-urls 2>&1 | grep "audit/"` — no `fail` findings for the new skill; `warn` count does not increase <!-- sha:25f393e -->
- [x] **Step 3:** Commit: `git add skills/audit/SKILL.md && git commit -m "feat: add /wos:audit orchestrator skill"` <!-- sha:25f393e -->

---

### Task 2: Update `OVERVIEW.md` skills reference table

**Files:**
- Modify: `OVERVIEW.md`

**Depends on:** Task 1 committed

- [x] **Step 1:** Open `OVERVIEW.md` and locate the `## Skills Reference` table. Add a row for `/wos:audit` above `/wos:lint` (it is the highest-level entry point): <!-- sha:f68da33 -->

  ```
  | `/wos:audit` | Full project health check — orchestrates lint, audit-skill, audit-rule, audit-chain, and wiki validation into a prioritized report |
  ```

- [x] **Step 2:** Verify: `grep "/wos:audit" OVERVIEW.md` → matches; `python scripts/lint.py --root . --no-urls` → clean pass (no new failures) <!-- sha:f68da33 -->
- [x] **Step 3:** Commit: `git add OVERVIEW.md && git commit -m "docs: add /wos:audit to OVERVIEW.md skills reference"` <!-- sha:f68da33 -->

---

## Validation

- [ ] `ls skills/audit/SKILL.md` — file exists
- [ ] `python scripts/lint.py --root . --no-urls 2>&1 | tail -5` — no new `fail` findings; overall pass
- [ ] `grep "name: audit" skills/audit/SKILL.md` — frontmatter name field is `audit`
- [ ] `grep "Handoff" skills/audit/SKILL.md` — `## Handoff` section present
- [ ] `grep "Anti-Pattern" skills/audit/SKILL.md` — `## Anti-Pattern Guards` section present
- [ ] `grep "/wos:audit" OVERVIEW.md` — skill appears in overview table
- [ ] On a clean project: invoking `/wos:audit` reports "No critical issues found" (or "All checks passed.")
- [ ] On a project with a skill missing `## Handoff`: invoking `/wos:audit` surfaces the finding at Medium severity in the Health Report

## Notes

- `scripts/lint.py` already runs wiki validation automatically when `wiki/SCHEMA.md` is present — Step 5 doesn't need a separate invocation; just parse the lint output for wiki-related findings
- The repair offer (Step 7) delegates to each sub-audit skill's own repair loop — this skill does not implement repair logic itself
- When Task 17 in `docs/plans/2026-04-10-roadmap-v036-v039.plan.md` is complete, mark the checkbox and add the merge commit SHA
