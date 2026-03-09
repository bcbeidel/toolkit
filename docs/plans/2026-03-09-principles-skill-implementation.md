# Principles Skill Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Create a `/wos:principles` skill that extracts, structures, and maintains project principles in a standalone `PRINCIPLES.md` at repo root.

**Architecture:** Pure LLM judgment skill — no new Python scripts. Four files: `SKILL.md` + three reference files. Uses existing `reindex.py` and `audit.py` for integration. Follows init/distill patterns for idempotent detect-and-branch workflow.

**Tech Stack:** Markdown skill files only. Existing Python tooling (`wos/skill_audit.py` validates skill quality, `scripts/audit.py` for integration checks).

**Design doc:** `docs/plans/2026-03-09-principles-skill-design.md`
**Issue:** #134
**Branch:** `feat/principles-skill`
**PR:** #145

---

### Task 1: Create branch

**Step 1: Create feature branch**

Run: `git checkout -b feat/principles-skill`

**Step 2: Verify branch**

Run: `git branch --show-current`
Expected: `feat/principles-skill`

---

### Task 2: Create `references/principle-structure.md`

Build bottom-up: references first, then SKILL.md.

**Files:**
- Create: `skills/principles/references/principle-structure.md`

**Step 1: Create directory structure**

Run: `mkdir -p skills/principles/references`

**Step 2: Write `principle-structure.md`**

This reference defines the template and authoring criteria for each principle. Content based on the design doc's "PRINCIPLES.md File Format" and "Five-criteria filter" sections.

```markdown
# Principle Structure

## File Format

`PRINCIPLES.md` lives at the repo root with no frontmatter — it is a
constitutional document loaded via `@PRINCIPLES.md`, not a WOS context file.

```markdown
# Principles

[Optional 1-2 sentence preamble about the project's philosophy]

## [Principle Name]
[One-sentence statement describing the desired outcome]

**Rationale:** [Why this principle matters for this project]
**Boundary:** [When this principle doesn't apply or should yield]
**Verification:** [Concrete way to check compliance — not a vague aspiration]
```

## Authoring Criteria

Each principle should satisfy at least 3 of these 5 criteria:

1. **Outcome-focused** — states a desired quality, not a procedure
2. **Testable** — can be evaluated as satisfied or violated in specific code
3. **Rationale-based** — there's a documentable "why" behind it
4. **Stable** — wouldn't change if you swapped frameworks or languages
5. **Ambiguity-scoped** — guides choices when multiple valid approaches exist

Candidates passing 0-2 criteria are rules or preferences, not principles.

## Component Guidelines

### Name
Short, memorable phrase. Imperative or noun form. No numbering — principles
aren't ranked.

Examples: "Convention over configuration", "Bottom line up front",
"Depend on nothing"

### Statement
One sentence. Describes the desired outcome or behavior. Stands alone
without the rationale.

Good: "Document patterns, don't enforce them."
Bad: "We should try to document patterns when possible."

### Rationale
Why this principle exists for *this project*. Not a generic argument — tie
it to the project's specific context, constraints, or history.

### Boundary
When this principle doesn't apply or should yield to another concern.
Every principle has limits. If you can't articulate a boundary, the
principle may be too vague.

Good: "When safety-critical behavior requires enforcement, use hooks
instead of documentation."
Bad: "Sometimes this doesn't apply."

### Verification
A concrete way to check whether code or decisions comply. The research
finding: principles with embedded verification criteria outperform pure
declarative principles.

Good: "No class inherits more than one concrete class."
Good: "Every script runs via `uv run` with PEP 723 metadata."
Bad: "Code should feel simple."

## Density Guidance

| Count | Assessment |
|-------|-----------|
| 3-10 | Healthy range for reliable agent adherence |
| 11-15 | Review whether some items are rules or preferences |
| 16+ | Agents likely to drop or conflate principles — consolidate |

Research basis: ~150-200 effective instructions per agent session, with
system prompts consuming roughly a third. Principles compete for the
remaining attention budget.
```

**Step 3: Verify file exists**

Run: `cat skills/principles/references/principle-structure.md | head -5`
Expected: Shows the `# Principle Structure` header.

**Step 4: Commit**

```bash
git add skills/principles/references/principle-structure.md
git commit -m "feat(principles): add principle structure reference"
```

---

### Task 3: Create `references/extraction-heuristics.md`

**Files:**
- Create: `skills/principles/references/extraction-heuristics.md`

**Step 1: Write `extraction-heuristics.md`**

This reference tells the LLM how to identify implicit principles in project artifacts. Content based on the design doc's "Extraction Heuristics" section.

```markdown
# Extraction Heuristics

How to identify implicit principles in project artifacts and classify
them as principles, rules, or preferences.

## Scan Sources (in order)

1. **CLAUDE.md** — sections labeled "principles", "philosophy", "values",
   or numbered guideline lists
2. **AGENTS.md** — convention statements beyond operational instructions
3. **ADRs / docs/plans/** — recurring rationale patterns ("we chose X
   because Y" repeated across documents)
4. **Recent commits (~50)** — patterns like "prefer X over Y",
   "always/never do Z" in commit messages
5. **Code patterns** — repeated structural conventions in key files
   (e.g., every module uses composition, all errors use stdlib exceptions)

## Signal Patterns

| Signal | Likely Classification | Example |
|--------|----------------------|---------|
| "Prefer X over Y" | Principle | "Prefer composition over inheritance" |
| "Always/never do X" | Rule | "Never use default exports" |
| "We use X" / "Use X" | Rule or preference | "Use ruff for linting" |
| Repeated rationale across commits/PRs | Principle candidate | 5 PRs cite "keeping it simple" |
| Numbered philosophy/values list | Principles | CLAUDE.md "Design Principles" section |
| Glob/file-specific instruction | Rule | "*.test.ts files use vitest" |
| Style/formatting guidance | Preference | "Use single quotes" |

## Classification

For each candidate, apply the five-criteria filter from the principle
structure reference. Show reasoning for each classification:

- **Principle** (3+ criteria met) — outcome-focused, guides judgment
  under ambiguity, stable across tech changes
- **Rule** (0-2 criteria met, procedural) — prescribes a specific action,
  may be tech-specific
- **Preference** (0-2 criteria met, stylistic) — not architectural,
  affects presentation not behavior

## Confidence Levels

Convergence across multiple sources is a confidence signal:

| Sources | Confidence |
|---------|-----------|
| CLAUDE.md + commits + code patterns | HIGH |
| Two sources converge (e.g., CLAUDE.md + commits) | MODERATE |
| Single source only (e.g., one commit message) | LOW |

## Presentation Format

Present extraction results as a table for user review:

```
| # | Candidate | Source | Classification | Confidence |
|---|-----------|--------|----------------|------------|
| 1 | Convention over configuration | CLAUDE.md:L32 | principle | HIGH |
| 2 | Use ValueError + stdlib only | CLAUDE.md:L78 | rule | HIGH |
| 3 | Prefer composition over inheritance | 12 commits | principle | MODERATE |
```

User approves, rejects, or reclassifies each row. Only approved
principles proceed to articulation.

Rules and preferences are noted but stay where they are — do not move
them to PRINCIPLES.md.
```

**Step 2: Commit**

```bash
git add skills/principles/references/extraction-heuristics.md
git commit -m "feat(principles): add extraction heuristics reference"
```

---

### Task 4: Create `references/drift-detection.md`

**Files:**
- Create: `skills/principles/references/drift-detection.md`

**Step 1: Write `drift-detection.md`**

This reference tells the LLM how to detect drift on re-runs. Content based on the design doc's "Re-Run Workflow" section.

```markdown
# Drift Detection

How to detect when practice has diverged from stated principles on
re-runs of the principles skill.

## When to Use

This workflow runs when `PRINCIPLES.md` already exists. The skill loads
current principles and scans for three types of drift.

## Drift Types

### A. New Implicit Principles

Patterns in artifacts not yet captured in `PRINCIPLES.md`:

- New CLAUDE.md sections that read like principles (apply the five-criteria
  filter from the extraction heuristics reference)
- Recurring rationale in commits/PRs since `PRINCIPLES.md` was last
  modified (check git log with `--after` date filter)
- Code patterns suggesting unstated conventions not captured as principles

### B. Stale Principles

Principles in `PRINCIPLES.md` no longer reflected in practice:

- Code patterns that consistently violate a stated principle
- CLAUDE.md rules that contradict a principle
- Recent commits that actively work against a principle

A single violation does not make a principle stale — look for a pattern
of 3+ instances suggesting the team has moved on.

### C. Principle Evolution

Principles where wording no longer matches how the team applies them:

- Boundary cases that have shifted (the exception became the norm)
- Verification criteria that no longer make sense given current tooling
- The spirit is still followed but the letter has drifted

## Scan Process

1. Read `PRINCIPLES.md` and build an inventory: name, statement,
   verification criteria for each principle
2. Check the last-modified date of `PRINCIPLES.md` via git log
3. Scan CLAUDE.md and AGENTS.md for new principle-like content
4. Scan recent commits since last modification (~50 or since last
   modified, whichever is fewer)
5. Sample key code files for patterns that confirm, contradict, or
   extend existing principles
6. Classify each finding as type A, B, or C

## Presentation Format

Present a drift report with three sections:

```
## Drift Report

### New candidates (not yet captured)
| # | Candidate | Source | Confidence |
|---|-----------|--------|------------|

### Potentially stale
| # | Principle | Evidence | Confidence |
|---|-----------|----------|------------|

### Wording drift
| # | Principle | Current | Suggested Revision | Evidence |
|---|-----------|---------|-------------------|----------|

No changes needed: N of M principles remain current.
```

Each proposed change is independent — user approves, rejects, or edits
per item. New candidates go through the full articulation process
(name, statement, rationale, boundary, verification).

## Confidence for Drift Findings

- **HIGH** — 5+ instances of consistent pattern across multiple sources
- **MODERATE** — 2-4 instances or pattern in a single source type
- **LOW** — 1 instance, possibly incidental

Present LOW confidence findings separately, clearly marked as
"possible drift — may not warrant action."
```

**Step 2: Commit**

```bash
git add skills/principles/references/drift-detection.md
git commit -m "feat(principles): add drift detection reference"
```

---

### Task 5: Create `skills/principles/SKILL.md`

**Files:**
- Create: `skills/principles/SKILL.md`

**Step 1: Write SKILL.md**

The main skill file. Follows the init/distill pattern: numbered workflow
steps, branches on state detection, references for detail. Keep the body
concise — detailed guidance lives in references.

```markdown
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
3. Run: `uv run <plugin-scripts-dir>/audit.py --root . --no-urls`
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
```

**Step 2: Count instruction lines to verify under threshold**

Run: `uv run python -c "
from wos.skill_audit import strip_frontmatter, count_instruction_lines
from pathlib import Path
text = Path('skills/principles/SKILL.md').read_text()
body = strip_frontmatter(text)
print(f'Instruction lines: {count_instruction_lines(body)}')
print(f'Non-blank lines: {sum(1 for l in body.splitlines() if l.strip())}')
"`

Expected: Instruction lines under 200, non-blank lines under 500.

**Step 3: Commit**

```bash
git add skills/principles/SKILL.md
git commit -m "feat(principles): add main SKILL.md for /wos:principles"
```

---

### Task 6: Update CLAUDE.md

**Files:**
- Modify: `CLAUDE.md` — skills table (line 88-98) and skill count (line 88)

**Step 1: Update skills table**

Add the principles skill to the table at line 88-98 of CLAUDE.md. The
table currently lists 7 skills. Add:

```markdown
| `/wos:principles` | Capture and maintain project principles |
```

**Step 2: Update skill count**

Change line 88 from `7 skills:` to `8 skills:`.

**Step 3: Verify the edit**

Read CLAUDE.md and confirm the table has 8 rows and the count says `8 skills`.

**Step 4: Commit**

```bash
git add CLAUDE.md
git commit -m "docs: register /wos:principles skill in CLAUDE.md"
```

---

### Task 7: Run audit and fix any issues

**Step 1: Run skill audit**

Run: `uv run python -m pytest tests/ -v -k skill`
Expected: All existing tests pass.

**Step 2: Run full audit on the new skill**

Run: `uv run scripts/audit.py --root . --no-urls`
Expected: No `fail` issues related to the new skill. Warnings are
acceptable but review each one.

**Step 3: Fix any issues found**

If the audit flags issues with the new skill files (name format,
description length, instruction density, etc.), fix them.

**Step 4: Commit fixes if needed**

```bash
git add -A
git commit -m "fix: address audit findings for principles skill"
```

---

### Task 8: Final review and PR preparation

**Step 1: Review all changes**

Run: `git log --oneline main..feat/principles-skill`
Expected: 5-6 commits (branch, 3 references, SKILL.md, CLAUDE.md update,
optional audit fix).

**Step 2: Verify file structure**

Run: `find skills/principles -type f | sort`
Expected:
```
skills/principles/SKILL.md
skills/principles/references/drift-detection.md
skills/principles/references/extraction-heuristics.md
skills/principles/references/principle-structure.md
```

**Step 3: Update design doc checklist**

Mark completed items in `docs/plans/2026-03-09-principles-skill-design.md`.

**Step 4: Commit checklist update**

```bash
git add docs/plans/2026-03-09-principles-skill-design.md
git commit -m "docs: update implementation checklist progress"
```

**Step 5: Create PR**

```bash
gh pr create --title "feat: add /wos:principles skill (#134)" --body "$(cat <<'EOF'
## Summary

- Adds `/wos:principles` skill for capturing and maintaining project principles
- Creates `PRINCIPLES.md` at repo root (constitutional layer, loaded via `@PRINCIPLES.md`)
- Idempotent: first run extracts implicit principles, re-runs detect drift
- Three reference files: principle structure, extraction heuristics, drift detection
- No new Python scripts — pure LLM judgment skill using existing tooling

Closes #134

## Files

- `skills/principles/SKILL.md` — main skill definition
- `skills/principles/references/principle-structure.md` — template and authoring criteria
- `skills/principles/references/extraction-heuristics.md` — identification and classification
- `skills/principles/references/drift-detection.md` — re-run scan and reporting
- `CLAUDE.md` — updated skills table (7 → 8 skills)
- `docs/plans/2026-03-09-principles-skill-design.md` — design document

## Test plan

- [ ] Run `uv run scripts/audit.py --root . --no-urls` — no fail issues
- [ ] Run `uv run python -m pytest tests/ -v` — all tests pass
- [ ] Verify skill instruction lines under 200 threshold
- [ ] Verify SKILL.md body under 500 non-blank lines
- [ ] Manual test: invoke `/wos:principles` in a test project

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```
