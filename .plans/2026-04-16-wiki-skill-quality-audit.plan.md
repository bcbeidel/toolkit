---
name: Wiki Plugin Skill Quality Audit
description: Audit all 4 skills in plugins/wiki with check-skill, fix clear-cut issues, file GitHub issues for judgment calls.
type: plan
status: completed
branch: chore/wiki-skill-quality-audit
related:
  - docs/designs/2026-04-16-build-skill-quality-audit.design.md
---

# Wiki Plugin Skill Quality Audit

## Goal

Audit all 4 skills in `plugins/wiki/skills/` using `/build:check-skill`, fix every finding that has an obvious correct answer (clear-cut), and file a GitHub issue for every finding that requires subjective judgment. One commit per skill; all work on one branch.

## Scope

Must have:
- Audit all 4 skills: `ingest`, `lint`, `research`, `setup`
- Fix clear-cut issues: wrong/missing frontmatter fields, stale paths or command names, broken cross-references, structural omissions with an obvious correct value
- File a GitHub issue per judgment-call finding (routing quality, vagueness, workflow ordering, content-quality criteria requiring subjective evaluation)
- One commit per skill

Won't have:
- Fixes for judgment calls (those become open issues)
- Audits of skills outside `plugins/wiki/`
- Plugin version bump (separate PR after issues are resolved)

## Approach

Four sequential tasks, one per skill, each following the same protocol: run check-skill → read findings → triage → fix clear-cut issues → file issues for judgment calls → commit. Tasks are ordered alphabetically. No cross-task dependencies.

**Triage guide (reference for executor):**
- **Clear-cut:** missing required frontmatter field with an obvious value, stale skill name reference, broken relative path, duplicate frontmatter field, structural section missing with obvious content
- **Judgment call:** routing description quality, vagueness of a rule, workflow step ordering ambiguity, anti-pattern guard completeness, example sufficiency, gate placement

## File Changes

- Modify: `plugins/wiki/skills/ingest/SKILL.md` (if findings require it)
- Modify: `plugins/wiki/skills/lint/SKILL.md` (if findings require it)
- Modify: `plugins/wiki/skills/research/SKILL.md` (if findings require it)
- Modify: `plugins/wiki/skills/setup/SKILL.md` (if findings require it)

**Branch:** `chore/wiki-skill-quality-audit`

## Tasks

---

### Task 1: Audit and fix `ingest`

- [x] Run `/build:check-skill plugins/wiki/skills/ingest/SKILL.md`, triage findings, fix clear-cut issues, file GitHub issues for judgment calls, commit <!-- sha:408f45a -->

**Verify:**
```bash
git log --oneline -1  # commit present for ingest
gh issue list --state open --search "ingest" --limit 5  # judgment-call issues filed (if any)
```

---

### Task 2: Audit and fix `lint`

- [x] Run `/build:check-skill plugins/wiki/skills/lint/SKILL.md`, triage findings, fix clear-cut issues, file GitHub issues for judgment calls, commit <!-- sha:e9fde3b -->

**Verify:**
```bash
git log --oneline -1
gh issue list --state open --search "wiki lint" --limit 5
```

---

### Task 3: Audit and fix `research`

- [x] Run `/build:check-skill plugins/wiki/skills/research/SKILL.md`, triage findings, fix clear-cut issues, file GitHub issues for judgment calls, commit <!-- sha:02c4dd5 -->

**Verify:**
```bash
git log --oneline -1
gh issue list --state open --search "research" --limit 5
```

---

### Task 4: Audit and fix `setup`

- [x] Run `/build:check-skill plugins/wiki/skills/setup/SKILL.md`, triage findings, fix clear-cut issues, file GitHub issues for judgment calls, commit <!-- sha:62d4328 -->

**Verify:**
```bash
git log --oneline -1
gh issue list --state open --search "wiki setup" --limit 5
```

---

## Validation

1. All 4 skills audited — one commit per skill present in branch history:
   ```bash
   git log --oneline origin/main..HEAD | grep "audit"
   # should show 4 entries
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
