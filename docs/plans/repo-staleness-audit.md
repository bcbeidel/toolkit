---
name: Repo Staleness Audit
description: Comprehensive audit of stale documentation, dead code, and outdated references across the WOS repository
created_at: 2026-03-20
---

# Repo Staleness Audit

Audit performed 2026-03-20 after cleaning up all merged and stale branches.

---

## 1. CLAUDE.md Inaccuracies

### Module count is wrong
- **File:** `CLAUDE.md` (Architecture > Package Structure)
- **Issue:** Claims "10 modules + 2 subpackages" but `wos/` now contains 12 modules + 2 subpackages
- **Missing modules:** `discovery.py` and `suffix.py` (added in flexible-layout work, PR #206)
- **Fix:** Update the count and add descriptions for both modules

### Validator count mismatch in docstring
- **File:** `wos/validators.py` (module docstring)
- **Issue:** Docstring says "seven individual checks" but there are 8 — `check_timestamps` is undocumented
- **Fix:** Update docstring to say "eight" and add `check_timestamps` to the list

---

## 2. README.md Inaccuracy

### Validation check count is wrong
- **File:** `README.md`
- **Issue:** Claims "5 validation checks" but CLAUDE.md correctly says 8 and there are 8 check functions
- **Fix:** Update to "8 validation checks"

---

## 3. AGENTS.md Issues

### Missing docs/prompts/ directory
- **File:** `AGENTS.md` (Context Navigation section)
- **Issue:** `docs/prompts/` directory exists with 5 files but is not listed in the navigation section or areas table
- **Fix:** Add `docs/prompts/` to navigation and areas table, or run reindex to regenerate

### "No active" claims are stale
- **File:** `AGENTS.md` (Context Navigation section)
- **Issue:** Claims "No active designs" and "No active plans" but both directories contain files
- **Fix:** Rerun `scripts/reindex.py` to regenerate AGENTS.md from current directory state

---

## 4. Dead Code

### Unused constant `_KNOWN_FIELDS`
- **File:** `wos/document.py` (lines 18-21)
- **Issue:** `_KNOWN_FIELDS` set is defined but never referenced anywhere in the codebase
- **Fix:** Delete the constant

---

## 5. Stale Plans

### Completed plans (4) — consider archiving or deleting
All work is merged. These serve no ongoing purpose:

| File | Status | Merged Via |
|------|--------|------------|
| `2026-03-13-deploy-documentation.plan.md` | Completed | Commits f69f1d2, 59d0ecf, f76f06d |
| `2026-03-13-flexible-layout.plan.md` | Completed | PR #206 |
| `cross-platform-deploy.plan.md` | Completed | Commit 17ffbb2 |
| `timestamps-and-rename.plan.md` | Completed | Commit 8aec4dd |

### Abandoned plan (1) — delete or archive
| File | Status | Issue |
|------|--------|-------|
| `2026-03-13-posttooluse-hooks.plan.md` | Approved (not started) | No branch, no commits, stalled |

---

## 6. Stale Designs

### Completed but still marked "draft" (2)
| File | Actual State |
|------|-------------|
| `2026-03-13-deploy-documentation.design.md` | Work completed and merged |
| `2026-03-13-flexible-layout.design.md` | Work completed and merged (PR #206) |

### Abandoned design (1)
| File | Issue |
|------|-------|
| `2026-03-13-posttooluse-hooks.design.md` | Work never started, no branch |

### Current design (1) — no action needed
| File | Status |
|------|--------|
| `cross-platform-deploy-design.md` | Approved, completed, accurate |

---

## 7. Stale Context/Research References

### ~~`uv run` convention is outdated~~ — NOT STALE
- **Files:**
  - `docs/research/plugin-extension-architecture.md`
  - `docs/context/plugin-extension-architecture.md`
- **Issue:** On closer inspection, these `uv run` references describe Claude Code's platform behavior (how it runs plugins externally), not WOS's project convention. They are factually accurate.
- **Fix:** None needed

---

## 8. Things That Are Fine

- **All 13 skills** — structurally sound, all references valid, no orphaned files
- **All 6 scripts** — present and referenced by skills/tests
- **All test files** — correspond to active modules, no orphaned tests
- **All imports** — no dead imports found
- **All cross-skill references** — valid (`/wos:` references all resolve)
- **All shared reference files** — 17 files in `_shared/references/`, all used
- **Research docs** — no draft markers, valid sources, relevant content
- **plugin.json** — version 0.31.0, matches changelog
- **PRINCIPLES.md** — aligned with CLAUDE.md
- **CONTRIBUTING.md** — accurate

---

## Summary

| Category | Count | Action | Status |
|----------|-------|--------|--------|
| Documentation inaccuracies | 5 | Update CLAUDE.md, README.md, AGENTS.md, validators.py docstring | Done |
| Dead code | 1 | Delete `_KNOWN_FIELDS` from document.py | Done |
| Completed plans to archive/delete | 4 | Deleted | Done |
| Abandoned plan + design | 2 | Deleted (posttooluse-hooks plan + design) | Done |
| Stale design status | 2 | Updated status from draft to completed | Done |
| Outdated references | 0 | `uv run` refs describe platform behavior, not stale | N/A |
| Stale empty directory | 1 | Deleted docs/prompts/ (empty, stale _index.md) | Done |
| **Total items fixed** | **15** | | |
