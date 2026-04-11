---
name: Plan Template
description: Copyable skeleton for implementation plans with all required sections
---

# Plan Template

Copy this skeleton when creating a new plan. Fill in each section, then
remove the bracketed instructions.

    ---
    name: [Feature Name]
    description: [One-sentence summary of what this plan achieves]
    type: plan
    status: draft
    related:
      - [path/to/design-doc.md]
    ---

    # [Feature Name]

    **Goal:** [2-3 sentences. State user-visible outcome. Why this matters.]

    **Scope:**

    Must have:
    - [Required deliverable]

    Won't have:
    - [Explicit exclusion]

    **Approach:** [High-level technical strategy. How the goal will be achieved.
    Name key architectural decisions. 2-4 sentences.]

    **File Changes:**
    - Create: `path/to/new-file.py`
    - Modify: `path/to/existing.py` (what changes)
    - Delete: `path/to/removed.py`

    **Branch:** `feat/NNN-feature-name`
    **PR:** TBD

    ---

    ### Task 1: [Outcome-oriented name]

    **Files:**
    - Create: `path/to/file.py`
    - Test: `tests/path/to/test_file.py`

    **Depends on:** Task N  <!-- optional: omit if purely sequential -->

    - [ ] **Step 1:** [Action with specific detail]
    - [ ] **Step 2:** Verify: `[concrete command with expected output]`
    - [ ] **Step 3:** Commit

    ---

    ## Validation

    - [ ] `[concrete command]` — [expected outcome]
    - [ ] `[concrete command]` — [expected outcome]

    ## Notes (optional)
    [Decisions made during execution, scope adjustments, lessons learned]
