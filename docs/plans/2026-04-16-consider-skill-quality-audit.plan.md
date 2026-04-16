---
name: Consider Plugin Skill Quality Audit
description: Audit all 17 skills in plugins/consider with check-skill, fix clear-cut issues, file GitHub issues for judgment calls.
type: plan
status: completed
branch: chore/consider-skill-quality-audit
related:
  - docs/designs/2026-04-16-build-skill-quality-audit.design.md
---

# Consider Plugin Skill Quality Audit

## Goal

Audit all 17 skills in `plugins/consider/skills/` using `/build:check-skill`, fix every finding that has an obvious correct answer (clear-cut), and file a GitHub issue for every finding that requires subjective judgment. One commit per skill; all work on one branch.

## Scope

Must have:
- Audit all 17 skills: `10-10-10`, `5-whys`, `circle-of-competence`, `consider`, `eisenhower-matrix`, `first-principles`, `hanlons-razor`, `inversion`, `map-vs-territory`, `occams-razor`, `one-thing`, `opportunity-cost`, `pareto`, `reversibility`, `second-order`, `swot`, `via-negativa`
- Fix clear-cut issues: wrong/missing frontmatter fields, stale paths or command names, broken cross-references, structural omissions with an obvious correct value
- File a GitHub issue per judgment-call finding (routing quality, vagueness, workflow ordering, content-quality criteria requiring subjective evaluation)
- One commit per skill

Won't have:
- Fixes for judgment calls (those become open issues)
- Audits of skills outside `plugins/consider/`
- Plugin version bump (separate PR after issues are resolved)

## Approach

Seventeen sequential tasks, one per skill, each following the same protocol: run check-skill → read findings → triage → fix clear-cut issues → file issues for judgment calls → commit. Tasks are ordered alphabetically. No cross-task dependencies.

**Triage guide (reference for executor):**
- **Clear-cut:** missing required frontmatter field with an obvious value, stale skill name reference, broken relative path, duplicate frontmatter field, structural section missing with obvious content
- **Judgment call:** routing description quality, vagueness of a rule, workflow step ordering ambiguity, anti-pattern guard completeness, example sufficiency, gate placement

## File Changes

- Modify: `plugins/consider/skills/10-10-10/SKILL.md` (if findings require it)
- Modify: `plugins/consider/skills/5-whys/SKILL.md` (if findings require it)
- Modify: `plugins/consider/skills/circle-of-competence/SKILL.md` (if findings require it)
- Modify: `plugins/consider/skills/consider/SKILL.md` (if findings require it)
- Modify: `plugins/consider/skills/eisenhower-matrix/SKILL.md` (if findings require it)
- Modify: `plugins/consider/skills/first-principles/SKILL.md` (if findings require it)
- Modify: `plugins/consider/skills/hanlons-razor/SKILL.md` (if findings require it)
- Modify: `plugins/consider/skills/inversion/SKILL.md` (if findings require it)
- Modify: `plugins/consider/skills/map-vs-territory/SKILL.md` (if findings require it)
- Modify: `plugins/consider/skills/occams-razor/SKILL.md` (if findings require it)
- Modify: `plugins/consider/skills/one-thing/SKILL.md` (if findings require it)
- Modify: `plugins/consider/skills/opportunity-cost/SKILL.md` (if findings require it)
- Modify: `plugins/consider/skills/pareto/SKILL.md` (if findings require it)
- Modify: `plugins/consider/skills/reversibility/SKILL.md` (if findings require it)
- Modify: `plugins/consider/skills/second-order/SKILL.md` (if findings require it)
- Modify: `plugins/consider/skills/swot/SKILL.md` (if findings require it)
- Modify: `plugins/consider/skills/via-negativa/SKILL.md` (if findings require it)

**Branch:** `chore/consider-skill-quality-audit`

## Tasks

---

### Task 1: Audit and fix `10-10-10`

- [x] Run `/build:check-skill plugins/consider/skills/10-10-10/SKILL.md`, triage findings, fix clear-cut issues, file GitHub issues for judgment calls, commit <!-- sha:0bdd583 -->

**Verify:**
```bash
git log --oneline -1  # commit present for 10-10-10
gh issue list --state open --search "10-10-10" --limit 5  # judgment-call issues filed (if any)
```

---

### Task 2: Audit and fix `5-whys`

- [x] Run `/build:check-skill plugins/consider/skills/5-whys/SKILL.md`, triage findings, fix clear-cut issues, file GitHub issues for judgment calls, commit <!-- sha:bf7e029 -->

**Verify:**
```bash
git log --oneline -1
gh issue list --state open --search "5-whys" --limit 5
```

---

### Task 3: Audit and fix `circle-of-competence`

- [x] Run `/build:check-skill plugins/consider/skills/circle-of-competence/SKILL.md`, triage findings, fix clear-cut issues, file GitHub issues for judgment calls, commit <!-- sha:6cc9b27 -->

**Verify:**
```bash
git log --oneline -1
gh issue list --state open --search "circle-of-competence" --limit 5
```

---

### Task 4: Audit and fix `consider`

- [x] Run `/build:check-skill plugins/consider/skills/consider/SKILL.md`, triage findings, fix clear-cut issues, file GitHub issues for judgment calls, commit <!-- sha:b067dcf -->

**Verify:**
```bash
git log --oneline -1
gh issue list --state open --search "consider" --limit 5
```

---

### Task 5: Audit and fix `eisenhower-matrix`

- [x] Run `/build:check-skill plugins/consider/skills/eisenhower-matrix/SKILL.md`, triage findings, fix clear-cut issues, file GitHub issues for judgment calls, commit <!-- sha:01124d8 -->

**Verify:**
```bash
git log --oneline -1
gh issue list --state open --search "eisenhower-matrix" --limit 5
```

---

### Task 6: Audit and fix `first-principles`

- [x] Run `/build:check-skill plugins/consider/skills/first-principles/SKILL.md`, triage findings, fix clear-cut issues, file GitHub issues for judgment calls, commit <!-- sha:f8e19e6 -->

**Verify:**
```bash
git log --oneline -1
gh issue list --state open --search "first-principles" --limit 5
```

---

### Task 7: Audit and fix `hanlons-razor`

- [x] Run `/build:check-skill plugins/consider/skills/hanlons-razor/SKILL.md`, triage findings, fix clear-cut issues, file GitHub issues for judgment calls, commit <!-- sha:e1462eb -->

**Verify:**
```bash
git log --oneline -1
gh issue list --state open --search "hanlons-razor" --limit 5
```

---

### Task 8: Audit and fix `inversion`

- [x] Run `/build:check-skill plugins/consider/skills/inversion/SKILL.md`, triage findings, fix clear-cut issues, file GitHub issues for judgment calls, commit <!-- sha:4d4f08d -->

**Verify:**
```bash
git log --oneline -1
gh issue list --state open --search "inversion" --limit 5
```

---

### Task 9: Audit and fix `map-vs-territory`

- [x] Run `/build:check-skill plugins/consider/skills/map-vs-territory/SKILL.md`, triage findings, fix clear-cut issues, file GitHub issues for judgment calls, commit <!-- sha:2e603a0 -->

**Verify:**
```bash
git log --oneline -1
gh issue list --state open --search "map-vs-territory" --limit 5
```

---

### Task 10: Audit and fix `occams-razor`

- [x] Run `/build:check-skill plugins/consider/skills/occams-razor/SKILL.md`, triage findings, fix clear-cut issues, file GitHub issues for judgment calls, commit <!-- sha:9c8df0b -->

**Verify:**
```bash
git log --oneline -1
gh issue list --state open --search "occams-razor" --limit 5
```

---

### Task 11: Audit and fix `one-thing`

- [x] Run `/build:check-skill plugins/consider/skills/one-thing/SKILL.md`, triage findings, fix clear-cut issues, file GitHub issues for judgment calls, commit <!-- sha:e7c6df9 -->

**Verify:**
```bash
git log --oneline -1
gh issue list --state open --search "one-thing" --limit 5
```

---

### Task 12: Audit and fix `opportunity-cost`

- [x] Run `/build:check-skill plugins/consider/skills/opportunity-cost/SKILL.md`, triage findings, fix clear-cut issues, file GitHub issues for judgment calls, commit <!-- sha:59abdee -->

**Verify:**
```bash
git log --oneline -1
gh issue list --state open --search "opportunity-cost" --limit 5
```

---

### Task 13: Audit and fix `pareto`

- [x] Run `/build:check-skill plugins/consider/skills/pareto/SKILL.md`, triage findings, fix clear-cut issues, file GitHub issues for judgment calls, commit <!-- sha:003cb7d -->

**Verify:**
```bash
git log --oneline -1
gh issue list --state open --search "pareto" --limit 5
```

---

### Task 14: Audit and fix `reversibility`

- [x] Run `/build:check-skill plugins/consider/skills/reversibility/SKILL.md`, triage findings, fix clear-cut issues, file GitHub issues for judgment calls, commit <!-- sha:78a1845 -->

**Verify:**
```bash
git log --oneline -1
gh issue list --state open --search "reversibility" --limit 5
```

---

### Task 15: Audit and fix `second-order`

- [x] Run `/build:check-skill plugins/consider/skills/second-order/SKILL.md`, triage findings, fix clear-cut issues, file GitHub issues for judgment calls, commit <!-- sha:8c30222 -->

**Verify:**
```bash
git log --oneline -1
gh issue list --state open --search "second-order" --limit 5
```

---

### Task 16: Audit and fix `swot`

- [x] Run `/build:check-skill plugins/consider/skills/swot/SKILL.md`, triage findings, fix clear-cut issues, file GitHub issues for judgment calls, commit <!-- sha:9dee919 -->

**Verify:**
```bash
git log --oneline -1
gh issue list --state open --search "swot" --limit 5
```

---

### Task 17: Audit and fix `via-negativa`

- [x] Run `/build:check-skill plugins/consider/skills/via-negativa/SKILL.md`, triage findings, fix clear-cut issues, file GitHub issues for judgment calls, commit <!-- sha:b4392ea -->

**Verify:**
```bash
git log --oneline -1
gh issue list --state open --search "via-negativa" --limit 5
```

---

## Validation

1. All 17 skills audited — one commit per skill present in branch history:
   ```bash
   git log --oneline origin/main..HEAD | grep "audit"
   # should show 17 entries
   ```
2. No regressions:
   ```bash
   python3 -m pytest plugins/wiki/tests/ -q
   # 269 passed (or more)
   ```
3. Open issues filed for judgment calls:
   ```bash
   gh issue list --state open --limit 30
   # judgment-call findings appear as issues
   ```
