---
name: Skill-Pair Audit Dimensions
description: The scoreable rubric for check-skill-pair. One entry per dimension — what it checks, pass/fail criteria, severity, and the principles-doc section it enforces.
---

# Skill-Pair Audit Dimensions

Dimensions are grouped by tier: Tier-1 (existence), Tier-2 (content),
Tier-3 (cross-reference). A `fail` in Tier-1 blocks nothing but is
reported first — Tier-2/3 skip reads against missing artifacts and
the report aggregates what was auditable.

Severity:
- **fail** — the pair is broken in a way that violates its contract.
- **warn** — a documented convention is missing; the pair works but
  drifts from the rubric.
- **info** — advisory dogfood recommendation; not enforced.

## Tier-1: Existence

### principles-doc-presence

**What it checks:** `<SHARED_REF_DIR>/<primitive>-best-practices.md` exists and is a non-empty file.
**Pass:** file exists with at least one H1.
**Fail:** file is missing or empty.
**Severity:** fail.
**Principles section:** *Anatomy* — the principles doc is one of the six slots.

### build-skill-presence

**What it checks:** `<SKILL_ROOT>/build-<primitive>/SKILL.md` exists.
**Pass:** file exists with valid YAML frontmatter (`name` present).
**Fail:** file is missing, empty, or lacks frontmatter.
**Severity:** fail.
**Principles section:** *Anatomy* — the scaffold half.

### check-skill-presence

**What it checks:** `<SKILL_ROOT>/check-<primitive>/SKILL.md` exists.
**Pass:** file exists with valid YAML frontmatter (`name` present).
**Fail:** file is missing, empty, or lacks frontmatter.
**Severity:** fail.
**Principles section:** *Anatomy* — the audit half.

### audit-dimensions-presence

**What it checks:** `<SKILL_ROOT>/check-<primitive>/references/audit-dimensions.md` exists.
**Pass:** file exists with at least one dimension entry.
**Fail:** file is missing or has no dimensions.
**Severity:** fail.
**Principles section:** *Anatomy* — the scoreable rubric.

### repair-playbook-presence

**What it checks:** `<SKILL_ROOT>/check-<primitive>/references/repair-playbook.md` exists.
**Pass:** file exists with at least one repair entry.
**Fail:** file is missing or has no repair entries.
**Severity:** fail.
**Principles section:** *Anatomy* — the fix recipes.

### routing-registration-presence

**What it checks:** `<SHARED_REF_DIR>/primitive-routing.md` contains both route lines: `/build:build-<primitive>` and `/build:check-<primitive>`.
**Pass:** both route lines appear as literal strings in the doc.
**Fail:** both route lines are absent.
**Severity:** fail (both missing) / warn (one missing).
**Principles section:** *Patterns That Work — Pair registered in `primitive-routing.md`*.

## Tier-2: Content

### principles-doc-structure

**What it checks:** The principles doc carries the required H2 sections — `## What a Good`, `## Anatomy`, `## Patterns That Work`, `## Anti-Patterns`, `## Safety & Maintenance`.
**Pass:** all five H2 headings present (the *What a Good* heading is a prefix match).
**Warn:** any required H2 is missing — the rubric is structurally incomplete.
**Severity:** warn.
**Principles section:** *Anatomy* — structural requirements for the principles doc.

### dimension-coverage-alignment

**What it checks:** The dimension name sets extracted from `audit-dimensions.md` and `repair-playbook.md` agree.
**Pass:** both sides list the same dimension names (ignoring order).
**Fail:** dimensions in audit-dimensions but not in repair-playbook — findings with no fix recipe.
**Warn:** dimensions in repair-playbook but not in audit-dimensions — fix recipes for findings the audit cannot surface.
**Severity:** fail (audit orphans) / warn (playbook orphans).
**Principles section:** *Patterns That Work — audit-dimensions parallels repair-playbook*.

### audit-dimensions-required-fields

**What it checks:** Each dimension entry in `audit-dimensions.md` carries six fields — *name*, *what it checks*, *pass criteria*, *fail criteria*, *severity*, *principles-doc section*.
**Pass:** every dimension has all six fields, labeled (`**Pass:**`) or clearly inferred.
**Warn:** three or more fields missing in any dimension.
**Severity:** warn.
**Principles section:** *Anatomy* — structural requirements for the audit rubric.

## Tier-3: Cross-Reference

### shared-principles-path

**What it checks:** The `references:` field in both SKILL.md frontmatters resolves to the same absolute path for the principles doc (after normalizing relative paths).
**Pass:** both halves reference the same `_shared/references/<primitive>-best-practices.md`.
**Fail:** the two halves reference different principles docs — the pair has silently split.
**Severity:** fail.
**Principles section:** *Patterns That Work — Single shared principles doc*.

### check-frontmatter-references

**What it checks:** `check-<primitive>/SKILL.md` frontmatter `references:` lists both `audit-dimensions.md` and `repair-playbook.md`.
**Pass:** both files appear in the references list (relative paths into the check half's own `references/`).
**Warn:** either file is missing from the references list.
**Severity:** warn.
**Principles section:** *Anatomy* — the audit half cites its rubric files up front.

### build-to-check-handoff

**What it checks:** `build-<primitive>/SKILL.md` mentions `/build:check-<primitive>` — either in the Handoff section's Chainable-to field or in the final workflow step.
**Pass:** the check-command string appears somewhere in the build SKILL body.
**Warn:** absent.
**Severity:** warn.
**Principles section:** *What a Good Skill-Pair Does — the pair is chainable by design*.

### dogfood-script-audit

**What it checks:** If `check-<primitive>/scripts/` exists, the user should run `/build:check-bash-script` or `/build:check-python-script` against those scripts (language picked per *Language Selection* in `primitive-routing.md`).
**Pass:** N/A — this is advisory.
**Info:** `scripts/` directory exists; the audit recommends running the appropriate script-checker.
**Severity:** info.
**Principles section:** *Safety & Maintenance* — the meta-skill dogfoods its own routing.
