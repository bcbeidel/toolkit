---
name: Build Plugin Skill Quality Audit
description: Audit all 10 skills in plugins/build with check-skill, fix clear-cut issues, file GitHub issues for judgment calls.
type: plan
status: executing
branch: chore/build-skill-quality-audit
related:
  - docs/designs/2026-04-16-build-skill-quality-audit.design.md
---

# Build Plugin Skill Quality Audit

## Goal

Audit all 10 skills in `plugins/build/skills/` using `/build:check-skill`, fix every finding that has an obvious correct answer (clear-cut), and file a GitHub issue for every finding that requires subjective judgment. One commit per skill; all work on one branch.

## Scope

Must have:
- Audit all 10 skills: `build-hook`, `build-rule`, `build-skill`, `build-subagent`, `check-hook`, `check-rule`, `check-skill`, `check-skill-chain`, `check-subagent`, `refine-prompt`
- Fix clear-cut issues: wrong/missing frontmatter fields, stale paths or command names, broken cross-references, structural omissions with an obvious correct value
- File a GitHub issue per judgment-call finding (routing quality, vagueness, workflow ordering, content-quality criteria requiring subjective evaluation)
- One commit per skill

Won't have:
- Fixes for judgment calls (those become open issues)
- Audits of skills outside `plugins/build/`
- Plugin version bump (separate PR after issues are resolved)

## Approach

Ten sequential tasks, one per skill, each following the same protocol: run check-skill → read findings → triage → fix clear-cut issues → file issues for judgment calls → commit. Tasks are ordered alphabetically. No cross-task dependencies.

**Triage guide (reference for executor):**
- **Clear-cut:** missing required frontmatter field with an obvious value, stale skill name reference (`check-work` vs `verify-work`), broken relative path, duplicate frontmatter field, structural section missing with obvious content
- **Judgment call:** routing description quality, vagueness of a rule, workflow step ordering ambiguity, anti-pattern guard completeness, example sufficiency, gate placement

## File Changes

- Modify: `plugins/build/skills/build-hook/SKILL.md` (if findings require it)
- Modify: `plugins/build/skills/build-rule/SKILL.md` (if findings require it)
- Modify: `plugins/build/skills/build-skill/SKILL.md` (if findings require it)
- Modify: `plugins/build/skills/build-subagent/SKILL.md` (if findings require it)
- Modify: `plugins/build/skills/check-hook/SKILL.md` (if findings require it)
- Modify: `plugins/build/skills/check-rule/SKILL.md` (if findings require it)
- Modify: `plugins/build/skills/check-skill/SKILL.md` (if findings require it)
- Modify: `plugins/build/skills/check-skill-chain/SKILL.md` (if findings require it)
- Modify: `plugins/build/skills/check-subagent/SKILL.md` (if findings require it)
- Modify: `plugins/build/skills/refine-prompt/SKILL.md` (if findings require it)

**Branch:** `chore/build-skill-quality-audit`

## Tasks

---

### Task 1: Audit and fix `build-hook`

- [x] Run `/build:check-skill plugins/build/skills/build-hook/SKILL.md`, triage findings, fix clear-cut issues, file GitHub issues for judgment calls, commit <!-- sha:b874061 -->

**Verify:**
```bash
git log --oneline -1  # commit present for build-hook
gh issue list --state open --search "build-hook" --limit 5  # judgment-call issues filed (if any)
```

---

### Task 2: Audit and fix `build-rule`

- [ ] Run `/build:check-skill plugins/build/skills/build-rule/SKILL.md`, triage findings, fix clear-cut issues, file GitHub issues for judgment calls, commit

**Verify:**
```bash
git log --oneline -1
gh issue list --state open --search "build-rule" --limit 5
```

---

### Task 3: Audit and fix `build-skill`

- [ ] Run `/build:check-skill plugins/build/skills/build-skill/SKILL.md`, triage findings, fix clear-cut issues, file GitHub issues for judgment calls, commit

**Verify:**
```bash
git log --oneline -1
gh issue list --state open --search "build-skill" --limit 5
```

---

### Task 4: Audit and fix `build-subagent`

- [ ] Run `/build:check-skill plugins/build/skills/build-subagent/SKILL.md`, triage findings, fix clear-cut issues, file GitHub issues for judgment calls, commit

**Verify:**
```bash
git log --oneline -1
gh issue list --state open --search "build-subagent" --limit 5
```

---

### Task 5: Audit and fix `check-hook`

- [ ] Run `/build:check-skill plugins/build/skills/check-hook/SKILL.md`, triage findings, fix clear-cut issues, file GitHub issues for judgment calls, commit

**Verify:**
```bash
git log --oneline -1
gh issue list --state open --search "check-hook" --limit 5
```

---

### Task 6: Audit and fix `check-rule`

- [ ] Run `/build:check-skill plugins/build/skills/check-rule/SKILL.md`, triage findings, fix clear-cut issues, file GitHub issues for judgment calls, commit

**Verify:**
```bash
git log --oneline -1
gh issue list --state open --search "check-rule" --limit 5
```

---

### Task 7: Audit and fix `check-skill`

- [ ] Run `/build:check-skill plugins/build/skills/check-skill/SKILL.md`, triage findings, fix clear-cut issues, file GitHub issues for judgment calls, commit

**Verify:**
```bash
git log --oneline -1
gh issue list --state open --search "check-skill" --limit 5
```

---

### Task 8: Audit and fix `check-skill-chain`

- [ ] Run `/build:check-skill plugins/build/skills/check-skill-chain/SKILL.md`, triage findings, fix clear-cut issues, file GitHub issues for judgment calls, commit

**Verify:**
```bash
git log --oneline -1
gh issue list --state open --search "check-skill-chain" --limit 5
```

---

### Task 9: Audit and fix `check-subagent`

- [ ] Run `/build:check-skill plugins/build/skills/check-subagent/SKILL.md`, triage findings, fix clear-cut issues, file GitHub issues for judgment calls, commit

**Verify:**
```bash
git log --oneline -1
gh issue list --state open --search "check-subagent" --limit 5
```

---

### Task 10: Audit and fix `refine-prompt`

- [ ] Run `/build:check-skill plugins/build/skills/refine-prompt/SKILL.md`, triage findings, fix clear-cut issues, file GitHub issues for judgment calls, commit

**Verify:**
```bash
git log --oneline -1
gh issue list --state open --search "refine-prompt" --limit 5
```

---

## Validation

1. All 10 skills audited — one commit per skill present in branch history:
   ```bash
   git log --oneline origin/main..HEAD | grep "audit"
   # should show 10 entries
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
