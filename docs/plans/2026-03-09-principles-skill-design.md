---
name: "Principles Skill Design"
description: "Design for /wos:principles skill to extract and maintain project principles in PRINCIPLES.md — issue #134"
---

# Principles Skill Design

**Issue:** #134 — Add skill to capture and structure project principles
**Branch:** `feat/principles-skill`
**PR:** #145

## Summary

A `/wos:principles` skill that extracts, structures, and maintains project
principles in a standalone `PRINCIPLES.md` at repo root. Idempotent — first
run creates, re-runs detect drift and propose updates.

## Key Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Where principles live | `PRINCIPLES.md` at repo root | Constitutional-layer visibility, always loaded alongside CLAUDE.md |
| CLAUDE.md integration | Auto-add `@PRINCIPLES.md` reference | Matches init's `@AGENTS.md` pattern |
| Existing principle handling | Extract and propose per-item | User controls what moves from CLAUDE.md; no surprise edits |
| Principle structure | Full (name, statement, rationale, boundary, verification) | Research shows verification criteria improve effectiveness; can compact later |
| Density warnings | Tiered — warn at 10, strong warn at 15+ | Balances guidance with flexibility |
| Drift scan scope | Config files + commits + code patterns | Most thorough; findings presented as suggestions, not assertions |
| Design approach | Single-pass workflow, branch on state | Matches init/distill patterns; simplest to understand and maintain |
| New Python scripts | None | Pure LLM judgment skill; uses existing reindex.py and audit.py |

## Skill Structure

```
skills/principles/
  SKILL.md                           — main skill definition
  references/
    principle-structure.md           — template and authoring criteria
    extraction-heuristics.md         — how to identify implicit principles
    drift-detection.md               — what to scan and how to classify drift
```

### SKILL.md Frontmatter

```yaml
---
name: principles
description: >
  Capture and maintain project principles in PRINCIPLES.md. Use when the
  user wants to "define principles", "extract principles", "review principles",
  "check principle drift", "what are our principles", or "update principles".
  Idempotent — safe to run multiple times.
argument-hint: ""
user-invocable: true
references:
  - ../_shared/references/preflight.md
  - references/principle-structure.md
  - references/extraction-heuristics.md
  - references/drift-detection.md
---
```

## PRINCIPLES.md File Format

```markdown
# Principles

[Optional 1-2 sentence preamble about the project's philosophy]

## [Principle Name]
[One-sentence statement describing the desired outcome]

**Rationale:** [Why this principle matters for this project]
**Boundary:** [When this principle doesn't apply or should yield]
**Verification:** [Concrete way to check compliance — not a vague aspiration]
```

- No frontmatter — constitutional document, not a WOS context file
- H2 per principle — independently linkable and scannable
- Verification must be concrete — skill pushes back on vague criteria
- No numbering — principles aren't ranked

## First-Run Workflow

When `PRINCIPLES.md` does not exist:

### Step 1 — Scan artifacts for implicit principles

Scan in order:

1. **CLAUDE.md** — sections labeled "principles", "philosophy", "values", or
   numbered guideline lists
2. **AGENTS.md** — convention statements beyond operational instructions
3. **ADRs / docs/plans/** — recurring rationale patterns
4. **Recent commits (~50)** — patterns like "prefer X over Y", "always/never Z"
5. **Code patterns** — repeated structural conventions in key files

Classify each candidate:
- **Principle** — outcome-focused, guides judgment under ambiguity, stable
- **Rule** — procedural, prescribes specific action, may be tech-specific
- **Preference** — stylistic, not architectural

Only principles advance. Rules and preferences noted for user.

### Step 2 — Present extraction results

```
| # | Candidate | Source | Classification | Confidence |
|---|-----------|--------|----------------|------------|
| 1 | Convention over configuration | CLAUDE.md:L45 | principle | HIGH |
| 2 | Use ValueError + stdlib only | CLAUDE.md:L78 | rule | HIGH |
| 3 | Prefer composition over inheritance | 12 commits | principle | MODERATE |
```

User approves, rejects, or reclassifies each row.

### Step 3 — Articulate each principle

Draft full structure for each approved principle:

```markdown
## [Name]
[One-sentence statement]

**Rationale:** [Why this matters]
**Boundary:** [When it doesn't apply]
**Verification:** [How to check compliance]
```

Present each for user review/editing before writing.

### Step 4 — Validate

- **Density:** Warn at 10, strong warn at 15+
- **Conflicts:** Flag contradictions, tensions, and redundancies
- **Completeness:** Flag principles missing boundary cases or verification

### Step 5 — Write & Integrate

1. Write `PRINCIPLES.md` with header and approved principles
2. Add `@PRINCIPLES.md` to CLAUDE.md if not present
3. Run `reindex.py` and `audit.py --no-urls` to verify

### Step 6 — Propose cleanup

Show overlapping content in source artifacts. Propose per-item: move to
PRINCIPLES.md (remove from source), keep in both, or leave as-is.
User decides each one.

## Re-Run Workflow (Drift Detection)

When `PRINCIPLES.md` already exists:

### Step 1 — Load current principles

Parse `PRINCIPLES.md` and build inventory (name, statement, verification).

### Step 2 — Scan for drift

Three types:

**A. New implicit principles** — patterns in artifacts not captured in
`PRINCIPLES.md`:
- New CLAUDE.md sections that read like principles
- Recurring rationale in commits/PRs since last modification
- Code patterns suggesting unstated conventions

**B. Stale principles** — no longer reflected in practice:
- Code patterns consistently violating a stated principle
- CLAUDE.md rules contradicting a principle
- Recent commits actively working against a principle

**C. Principle evolution** — wording no longer matches practice:
- Boundary cases that shifted (exception became the norm)
- Verification criteria no longer sensible given current tooling

### Step 3 — Present drift report

```
## Drift Report

### New candidates (not yet captured)
| # | Candidate | Source | Confidence |
|---|-----------|--------|------------|
| 1 | Prefer stdlib-only dependencies | 8 recent commits | HIGH |

### Potentially stale
| # | Principle | Evidence | Confidence |
|---|-----------|----------|------------|
| 1 | "Always use composition" | 3 recent PRs use inheritance | MODERATE |

### Wording drift
| # | Principle | Current | Suggested revision | Evidence |
|---|-----------|---------|-------------------|----------|
| 1 | "Keep it simple" | "No frameworks" | "Minimal frameworks when justified" | Framework X added in PR #42 |

No changes needed: 7 of 10 principles remain current.
```

### Step 4 — User approves changes

Each change is independent. New candidates go through full articulation.

### Step 5 — Write & validate

Update `PRINCIPLES.md` with approved changes only. Run `audit.py --no-urls`.
Report what changed.

## Density Warnings

| Count | Severity | Message |
|-------|----------|---------|
| 1-10 | none | — |
| 11-15 | warn | "You have {n} principles. Research suggests 3-10 for reliable agent adherence. Consider whether some are rules or preferences that belong in CLAUDE.md." |
| 16+ | strong warn | "You have {n} principles. At this density, agents are likely to drop or conflate principles. Strongly recommend consolidating." |

## Conflict Detection

Three types, all heuristic (LLM judgment, not deterministic):

1. **Direct contradiction** — two principles can't both be satisfied
2. **Tension** — principles pull different directions but can coexist with
   boundary cases. Flagged as tensions, not conflicts — propose boundary
   case additions.
3. **Redundancy** — two principles say the same thing differently. Propose
   merging.

## Extraction Heuristics

### Signal patterns

| Signal | Likely classification | Example |
|--------|----------------------|---------|
| "Prefer X over Y" | Principle | "Prefer composition over inheritance" |
| "Always/never do X" | Rule | "Never use default exports" |
| "We use X" / "Use X" | Rule or preference | "Use ruff for linting" |
| Repeated rationale across commits/PRs | Principle candidate | 5 PRs say "keeping it simple" as justification |
| Numbered philosophy/values list | Principles | CLAUDE.md "Design Principles" section |
| Glob/file-specific instruction | Rule | "*.test.ts files use vitest" |
| Style/formatting guidance | Preference | "Use single quotes" |

### Five-criteria filter

Each candidate must pass at least 3 of 5 to qualify as a principle:

1. **Outcome-focused** — states a desired quality, not a procedure
2. **Testable** — can be evaluated as satisfied or violated
3. **Rationale-based** — there's a "why" behind it
4. **Stable** — wouldn't change if you swapped frameworks or languages
5. **Ambiguity-scoped** — guides choices when multiple valid approaches exist

Candidates passing 0-2 classified as rules or preferences. Skill shows
reasoning for each classification so user can override.

### Source priority

Convergence across multiple sources is a confidence signal:
- CLAUDE.md + commits + code → HIGH confidence
- Single commit message only → LOW confidence

## Explicit Non-Goals

1. **No enforcement** — writes PRINCIPLES.md, doesn't add linting/hooks/CI
2. **No auto-modification of CLAUDE.md content** — only auto-change is adding
   `@PRINCIPLES.md`; content moves require user approval per-item
3. **No new Python scripts** — pure LLM judgment; uses existing tooling
4. **No scoring/grading** — checks criteria and flags gaps, no quality scores
5. **No cross-project sharing** — operates on one repo at a time
6. **No principle hierarchy** — principles are flat, no dependencies or
   meta-principles

## Research Basis

Design grounded in research from
`docs/research/2026-03-05-principle-based-development.md` (in notes repo):

- **Constitutional AI** — natural-language principles guide self-critique
- **Five authoring criteria** — outcome-focused, testable, rationale-based,
  stable, ambiguity-scoped
- **Principles + checkpoints** outperform pure declarative principles (RAIF,
  Spec Kit gates)
- **Three-layer architecture** — constitutional (principles), operational
  (rules/skills), mechanical (hooks)
- **Instruction budget** — ~150-200 effective instructions per session;
  principles offer higher leverage per slot than rules
- **Tiered density** — 3-10 principles for reliable adherence

## Implementation Checklist

- [x] Create `skills/principles/SKILL.md`
- [x] Create `skills/principles/references/principle-structure.md`
- [x] Create `skills/principles/references/extraction-heuristics.md`
- [x] Create `skills/principles/references/drift-detection.md`
- [x] Register skill in CLAUDE.md architecture table
- [x] Update CLAUDE.md skill count and table
- [x] Add tests for any new Python if needed (currently none planned)
- [x] Run audit to verify skill quality checks pass
