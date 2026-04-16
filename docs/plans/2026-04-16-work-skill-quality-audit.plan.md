---
name: Work Plugin Skill Quality Audit
description: Audit all 5 skills in plugins/work with check-skill, fix clear-cut issues, file GitHub issues for judgment calls.
type: plan
status: completed
branch: chore/work-skill-quality-audit
related:
  - docs/designs/2026-04-16-build-skill-quality-audit.design.md
---

# Work Plugin Skill Quality Audit

## Goal

Audit all 5 skills in `plugins/work/skills/` using `/build:check-skill`, fix every finding that has an obvious correct answer (clear-cut), and file a GitHub issue for every finding that requires subjective judgment. One commit per skill; all work on one branch.

## Scope

Must have:
- Audit all 5 skills: `finish-work`, `plan-work`, `scope-work`, `start-work`, `verify-work`
- Fix clear-cut issues: wrong/missing frontmatter fields, stale paths or command names, broken cross-references, structural omissions with an obvious correct value
- File a GitHub issue per judgment-call finding (routing quality, vagueness, workflow ordering, content-quality criteria requiring subjective evaluation)
- One commit per skill

Won't have:
- Fixes for judgment calls (those become open issues)
- Audits of skills outside `plugins/work/`
- Plugin version bump (separate PR after issues are resolved)

## Approach

Five sequential tasks, one per skill, each following the same protocol: run check-skill → read findings → triage → fix clear-cut issues → file issues for judgment calls → commit. Tasks are ordered alphabetically. No cross-task dependencies.

**Triage guide (reference for executor):**
- **Clear-cut:** missing required frontmatter field with an obvious value, stale skill name reference (`check-work` vs `verify-work`), broken relative path, duplicate frontmatter field, structural section missing with obvious content
- **Judgment call:** routing description quality, vagueness of a rule, workflow step ordering ambiguity, anti-pattern guard completeness, example sufficiency, gate placement

## File Changes

- Modify: `plugins/work/skills/finish-work/SKILL.md` (if findings require it)
- Modify: `plugins/work/skills/plan-work/SKILL.md` (if findings require it)
- Modify: `plugins/work/skills/scope-work/SKILL.md` (if findings require it)
- Modify: `plugins/work/skills/start-work/SKILL.md` (if findings require it)
- Modify: `plugins/work/skills/verify-work/SKILL.md` (if findings require it)

**Branch:** `chore/work-skill-quality-audit`

## Tasks

---

### Task 1: Audit and fix `finish-work`

- [x] Run `/build:check-skill plugins/work/skills/finish-work/SKILL.md`, triage findings, fix clear-cut issues, file GitHub issues for judgment calls, commit <!-- sha:6f320db -->

**Verify:**
```bash
git log --oneline -1  # commit present for finish-work
gh issue list --state open --search "finish-work" --limit 5  # judgment-call issues filed (if any)
```

---

### Task 2: Audit and fix `plan-work`

- [x] Run `/build:check-skill plugins/work/skills/plan-work/SKILL.md`, triage findings, fix clear-cut issues, file GitHub issues for judgment calls, commit <!-- sha:8ddb84c -->

**Verify:**
```bash
git log --oneline -1
gh issue list --state open --search "plan-work" --limit 5
```

---

### Task 3: Audit and fix `scope-work`

- [x] Run `/build:check-skill plugins/work/skills/scope-work/SKILL.md`, triage findings, fix clear-cut issues, file GitHub issues for judgment calls, commit <!-- sha:964ea53 -->

**Verify:**
```bash
git log --oneline -1
gh issue list --state open --search "scope-work" --limit 5
```

---

### Task 4: Audit and fix `start-work`

- [x] Run `/build:check-skill plugins/work/skills/start-work/SKILL.md`, triage findings, fix clear-cut issues, file GitHub issues for judgment calls, commit <!-- sha:facb753 -->

**Verify:**
```bash
git log --oneline -1
gh issue list --state open --search "start-work" --limit 5
```

---

### Task 5: Audit and fix `verify-work`

- [x] Run `/build:check-skill plugins/work/skills/verify-work/SKILL.md`, triage findings, fix clear-cut issues, file GitHub issues for judgment calls, commit <!-- sha:c425f5d -->

**Verify:**
```bash
git log --oneline -1
gh issue list --state open --search "verify-work" --limit 5
```

---

## Validation

1. All 5 skills audited — one commit per skill present in branch history:
   ```bash
   git log --oneline origin/main..HEAD | grep "audit"
   # should show 5 entries
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
