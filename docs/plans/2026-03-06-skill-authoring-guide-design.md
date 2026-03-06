# Extend /wos:audit with Skill Evaluation + Authoring Guide

**Goal:** When audit encounters a skill directory, apply skill-specific rubric
checks — deterministic checks in Python, judgment checks guided by a reference
file that doubles as the human-readable skill authoring guide.

**Branch:** `feat/128-skill-authoring-guide`
**Issue:** #128

## Architecture

Two layers, following P2 ("structure in code, quality in skills"):

1. **Python layer** (`skill_audit.py`) — deterministic checks, fast, CI-friendly
2. **Skill layer** (`skills/audit/`) — judgment checks guided by reference file

### Python Changes: `skill_audit.py`

Extend the existing `check_skill_sizes()` or add new functions for 7 checks:

| Check | Severity | Logic |
|-------|----------|-------|
| `name` format: lowercase + hyphens only | fail | regex `^[a-z0-9-]+$` |
| `name` length ≤64 chars | fail | `len(name) <= 64` |
| `name` no reserved words | fail | substring check for "anthropic", "claude" |
| `description` ≤1024 chars | warn | `len(description) <= 1024` |
| `description` no XML tags | warn | regex for `<[a-zA-Z]` |
| `description` third-person heuristic | warn | flag patterns like "I can", "You can", "This skill should be used when" |
| SKILL.md raw line count ≤500 | warn | line count after frontmatter |

Entry point: `scripts/audit.py` already calls `check_skill_sizes()`. New
checks integrate into the same flow, returning issues in the standard
`list[dict]` format with `file`, `issue`, `severity` keys.

### Skill Changes: `skills/audit/`

| File | Change |
|------|--------|
| `skills/audit/SKILL.md` | Add "Skill Evaluation" section |
| `skills/audit/references/skill-authoring-guide.md` | New — guide + rubric |

**Detection:** When audit's target path contains a `SKILL.md`, or during
whole-project scan when `skills/*/SKILL.md` directories exist, Claude reads
the guide and applies judgment criteria.

**Guide structure (`skill-authoring-guide.md`):**

1. The Loading Model — L1/L2/L3 progressive disclosure
2. Required Frontmatter — `name`, `description` conventions + examples
3. Writing the Description — third person, what + when, ≤1024 chars
4. SKILL.md Body — ≤500 lines, imperative voice, freedom ↔ fragility
5. Reference Files — one level deep, TOC for >100 lines
6. Conciseness Test — "Does Claude need this?"
7. Examples Beat Explanations — concrete > verbose
8. Canonical Example — `distill` walkthrough
9. Evaluation Criteria — checklist table for self-check and Claude evaluation

**Judgment checks (Claude applies from guide):**

| Check | What Claude evaluates |
|-------|---------------------|
| Description triggers | Does description include both what + when? |
| Freedom ↔ fragility | Do guardrail vs. guidance levels match? |
| Unnecessary context | Does the skill explain things Claude already knows? |
| Examples quality | Are examples concrete and demonstrate expected depth? |
| Terminology consistency | Is vocabulary consistent throughout? |
| Reference depth | Are references truly one level deep from SKILL.md? |

## What This Does NOT Include

- No new CLI script — extends existing `audit.py` + `skill_audit.py`
- No new skill directory — extends existing `skills/audit/`
- No changes to `validators.py` — skill checks stay in `skill_audit.py`

## Acceptance Criteria (#128)

- [ ] Guide covers required frontmatter fields with examples
- [ ] Reference file convention (L1/L2/L3) documented
- [ ] `distill` skill referenced as canonical example
- [ ] Guide is concise (P6)
- [ ] 7 new deterministic checks in `skill_audit.py` with tests
- [ ] Existing 230 tests still pass
- [ ] Audit detects and evaluates skill directories
