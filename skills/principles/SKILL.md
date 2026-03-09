---
name: principles
description: >
  Capture and maintain project principles in PRINCIPLES.md. Use when the
  user wants to "define principles", "extract principles", "review
  principles", "check principle drift", "what are our principles", or
  "update principles". Idempotent — safe to run multiple times.
argument-hint: ""
user-invocable: true
references:
  - ../_shared/references/preflight.md
  - references/principle-structure.md
  - references/extraction-heuristics.md
  - references/drift-detection.md
---

# Principles

Capture and maintain project principles in `PRINCIPLES.md` at the repo root.
Idempotent — first run extracts and creates, re-runs detect drift and
propose updates.

**Prerequisite:** Before running any `uv run` command below, follow the
preflight check in the [preflight reference](../_shared/references/preflight.md).

## Workflow

### 1. Detect state

Check whether `PRINCIPLES.md` exists at the repo root.

- **If it does not exist** → follow the First Run workflow (steps 2-7)
- **If it exists** → follow the Re-Run workflow (steps 8-12)

---

## First Run

### 2. Scan for implicit principles

Follow the scan process in [extraction-heuristics.md](references/extraction-heuristics.md).
Scan CLAUDE.md, AGENTS.md, docs/plans/, recent commits, and code patterns.
Classify each candidate as principle, rule, or preference.

### 3. Present extraction results

Show the extraction table to the user. Include all candidates (principles,
rules, preferences) with classification and confidence. User approves,
rejects, or reclassifies each row. Only approved principles proceed.

### 4. Articulate each principle

For each approved principle, draft the full structure defined in
[principle-structure.md](references/principle-structure.md):
name, statement, rationale, boundary, verification.

Present each principle to the user for review. Push back on vague
verification criteria — every principle needs a concrete check.

### 5. Validate

Before writing, check:

- **Density:** Count principles. Warn at 11-15, strongly warn at 16+.
  See density guidance in [principle-structure.md](references/principle-structure.md).
- **Conflicts:** Review all pairs for direct contradictions, tensions,
  or redundancy. Flag with explanation.
- **Completeness:** Flag any principles missing boundary cases or
  verification criteria.

### 6. Write and integrate

1. Write `PRINCIPLES.md` at the repo root using the format in
   [principle-structure.md](references/principle-structure.md)
2. If CLAUDE.md exists but does not contain `@PRINCIPLES.md`, add the
   reference (at the top, next to `@AGENTS.md` if present)
3. Run: `uv run <plugin-scripts-dir>/reindex.py --root .`
4. Run: `uv run <plugin-scripts-dir>/audit.py --root . --no-urls`
   to verify the skill produced valid output

### 7. Propose cleanup

Show the user which source artifacts (CLAUDE.md sections, ADRs, etc.)
have content that overlaps with the new `PRINCIPLES.md`. For each item,
propose: move to PRINCIPLES.md (remove from source), keep in both, or
leave as-is. User decides each one. Do not modify source files without
explicit per-item approval.

---

## Re-Run (Drift Detection)

### 8. Load current principles

Read `PRINCIPLES.md` and inventory each principle: name, statement,
verification criteria.

### 9. Scan for drift

Follow the scan process in [drift-detection.md](references/drift-detection.md).
Look for three drift types: new implicit principles, stale principles,
and principle evolution.

### 10. Present drift report

Show the drift report table. Include "no changes needed" count for
principles that remain current. Each finding is independent.

### 11. User approves changes

User approves, rejects, or edits each proposed change independently.
New candidates go through the full articulation step (step 4).

### 12. Write and validate

Update `PRINCIPLES.md` with approved changes only. Do not touch
unapproved principles. Run:
`uv run <plugin-scripts-dir>/audit.py --root . --no-urls`

Report what changed and what remained unchanged.

## Examples

<example>
**Extraction table (step 3):**

| # | Candidate | Source | Classification | Confidence |
|---|-----------|--------|----------------|------------|
| 1 | Convention over configuration | CLAUDE.md:L32 + 8 commits | principle | HIGH |
| 2 | Use ValueError only | CLAUDE.md:L78 | rule | HIGH |
| 3 | Prefer composition over inheritance | 12 commits | principle | MODERATE |
| 4 | Use single quotes | .editorconfig | preference | LOW |
</example>

<example>
**Articulated principle (step 4):**

## Depend on nothing
Stdlib-only core; scripts isolate their own dependencies.

**Rationale:** Eliminates version conflicts and supply-chain risk. Users
install one tool, not a dependency tree.
**Boundary:** Dev dependencies (pytest, ruff) are acceptable. Scripts may
use PEP 723 inline metadata for their own isolated deps.
**Verification:** `wos/` imports nothing outside stdlib. `scripts/` use
only PEP 723 `[tool.uv]` dependencies.
</example>

<example>
**Drift report (step 10):**

## Drift Report

### New candidates (not yet captured)
| # | Candidate | Source | Confidence |
|---|-----------|--------|------------|
| 1 | Bottom line up front | 6 recent PRs lead with summary | HIGH |

### Potentially stale
| # | Principle | Evidence | Confidence |
|---|-----------|----------|------------|
| 1 | "No frameworks" | Added FastAPI in PR #87 | MODERATE |

No changes needed: 8 of 9 principles remain current.
</example>
