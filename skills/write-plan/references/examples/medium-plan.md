---
name: Medium Plan Example
description: Example plan adapted from a real implementation — new skill with references, 4 tasks
---

# Medium Plan Example

This example is adapted from a real completed plan (brainstorm skill
implementation). It demonstrates the format at medium scale: new skill
directory with SKILL.md and reference files, broader scope, 4 tasks,
audit-based validation.

    ---
    name: Brainstorm Skill Implementation
    description: Create wos:brainstorm skill with SKILL.md and two reference files
    metadata:
      type: plan
      status: draft
      related:
        - skills/_shared/references/plan-format.md
    ---

    # Brainstorm Skill Implementation

    **Goal:** Ship the brainstorm skill — a structured exploration tool
    that produces design documents through divergent-then-convergent
    thinking. This bridges the gap between user intent and implementation
    planning by ensuring designs are explored before plans are written.

    **Scope:**

    Must have:
    - `skills/brainstorm/SKILL.md` under 500 body lines
    - `skills/brainstorm/references/spec-format-guide.md`
    - `skills/brainstorm/references/exploration-patterns.md`
    - Triggers on "brainstorm", "explore", "design"
    - Hard gate: produces design docs, not plans or code
    - 2-3 approach exploration before convergence
    - Design doc output with `type: design` frontmatter

    Won't have:
    - Visual companion (CLI-focused)
    - Subagent dispatch for spec review
    - Scripts or Python code (pure markdown skill)
    - New validators or document model changes

    **Approach:** Create three markdown files. SKILL.md defines a 6-step
    workflow (understand → diverge → converge → write spec → review →
    hand off). Reference files distill research into concise scaffolds:
    spec-format-guide covers section format and depth calibration,
    exploration-patterns provides question templates and approach
    comparison format.

    **File Changes:**
    - Create: `skills/brainstorm/SKILL.md`
    - Create: `skills/brainstorm/references/spec-format-guide.md`
    - Create: `skills/brainstorm/references/exploration-patterns.md`

    **Branch:** `feat/158-brainstorm-skill`

    ---

    ### Task 1: Create SKILL.md

    **Files:**
    - Create: `skills/brainstorm/SKILL.md`

    - [ ] Create directory: `mkdir -p skills/brainstorm/references`
    - [ ] Write SKILL.md with frontmatter, 6-step workflow, key instructions,
          anti-pattern guards, output format
    - [ ] Verify line count: `wc -l skills/brainstorm/SKILL.md` (under 500)
    - [ ] Commit

    ### Task 2: Create spec-format-guide.md

    **Files:**
    - Create: `skills/brainstorm/references/spec-format-guide.md`

    - [ ] Write guide covering: required frontmatter, spec sections table,
          writing principles, depth calibration table
    - [ ] Verify line count: `wc -l` (under 80)
    - [ ] Commit

    ### Task 3: Create exploration-patterns.md

    **Files:**
    - Create: `skills/brainstorm/references/exploration-patterns.md`

    - [ ] Write guide covering: question format (multiple-choice preferred),
          approach comparison table template, scope decomposition signals,
          convergence checklist
    - [ ] Verify line count: `wc -l` (under 80)
    - [ ] Commit

    ### Task 4: Run validation

    Depends on: Tasks 1-3

    - [ ] Run test suite: `python python -m pytest tests/ -v` — all pass
    - [ ] Run skill audit: `python scripts/audit.py --root .` — no failures
          for brainstorm skill
    - [ ] Fix any audit findings and re-run
    - [ ] Commit fixes (if any)

    ---

    ## Validation

    - [ ] `python python -m pytest tests/ -v` — all tests pass (no regressions)
    - [ ] `python scripts/audit.py --root .` — no failures for brainstorm skill
    - [ ] `skills/brainstorm/SKILL.md` exists and is under 500 body lines
    - [ ] SKILL.md frontmatter has name, description, user-invocable, references
    - [ ] Hard gate text present in SKILL.md body
