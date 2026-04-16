---
name: Build Plugin Skill Quality Audit
description: Run check-skill against all 10 skills in plugins/build, fix clear-cut issues, file follow-up issues for judgment calls.
type: design
status: approved
related: []
---

# Build Plugin Skill Quality Audit

## Purpose

Run `/build:check-skill` against all 10 skills in `plugins/build/skills/`, triage each finding, fix what is clearly broken, and file follow-up issues for anything requiring judgment. All work lands on one branch.

## Scope

In scope:
- All 10 skills: `build-hook`, `build-rule`, `build-skill`, `build-subagent`, `check-hook`, `check-rule`, `check-skill`, `check-skill-chain`, `check-subagent`, `refine-prompt`
- Fix **clear-cut** issues: missing/wrong frontmatter fields, stale paths or command names, broken cross-references, structural omissions with an obvious correct value
- File a GitHub issue for each **judgment-call** finding: routing quality, vagueness assessments, workflow step ordering, content-quality criteria requiring subjective evaluation
- One commit per skill; one branch for all 10

Won't do:
- Fix judgment calls (those become open issues)
- Audit skills outside `plugins/build/`
- Bump plugin version (separate PR after issues are resolved)

## Acceptance Criteria

- All 10 skills have been audited with `/build:check-skill`
- Every clear-cut finding is resolved and committed
- Every judgment-call finding has a corresponding open GitHub issue
- No regressions: existing wiki tests still pass after any source changes
