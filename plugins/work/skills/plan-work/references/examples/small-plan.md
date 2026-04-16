---
name: Small Plan Example
description: Example plan adapted from a real implementation — single-module, 3 tasks
---

# Small Plan Example

This example is adapted from a real completed plan (plan-document-format
implementation). It demonstrates the format at small scale: one module,
focused scope, 3 tasks with TDD verification.

    ---
    name: Status Field Implementation
    description: Add status field to Document model with parse-time validation
    type: plan
    status: draft
    related:
      - docs/designs/2026-03-11-status-field.design.md
    ---

    # Status Field Implementation

    **Goal:** Add lifecycle status tracking to plan documents so that
    downstream skills (start-work, check-work) can query plan state.
    Plans currently have no machine-readable status.

    **Scope:**

    Must have:
    - `status` field on Document dataclass (Optional[str], default None)
    - Parse-time extraction from frontmatter
    - Enum validation (draft, approved, executing, completed, abandoned)
    - Tests for all valid and invalid values

    Won't have:
    - Status transition validation (deferred)
    - Plan-specific audit checks (separate issue)
    - Required-section validation

    **Approach:** Extend the Document dataclass with one optional field.
    Add extraction logic to parse_document() alongside existing field
    handling. Validate against a closed set of strings — plain membership
    check, no Python enum type.

    **File Changes:**
    - Modify: `wos/document.py` (add field to dataclass, parse + validate in parse_document)
    - Modify: `tests/test_document.py` (add status tests, update test_unknown_fields_ignored)

    **Branch:** `feat/157-plan-document-format`

    ---

    ### Task 1: Add status field to Document dataclass

    **Files:**
    - Modify: `wos/document.py`
    - Test: `tests/test_document.py`

    - [ ] Write failing test: Document accepts `status` kwarg, defaults to None
    - [ ] Run test — expected: FAIL (unexpected keyword argument)
    - [ ] Add `status: Optional[str] = None` to Document, add "status" to _KNOWN_FIELDS
    - [ ] Run test — expected: PASS
    - [ ] Commit

    ### Task 2: Parse and validate status from frontmatter

    **Files:**
    - Modify: `wos/document.py`
    - Test: `tests/test_document.py`

    - [ ] Write failing test: parse_document extracts status from frontmatter
    - [ ] Write failing test: invalid status raises ValueError
    - [ ] Run tests — expected: both FAIL
    - [ ] Add status extraction and validation to parse_document()
    - [ ] Run tests — expected: both PASS
    - [ ] Commit

    ### Task 3: Update existing test for status recognition

    **Files:**
    - Modify: `tests/test_document.py`

    - [ ] Update test_unknown_fields_ignored to expect doc.status == "draft"
    - [ ] Run full test suite — expected: ALL PASS
    - [ ] Commit

    ---

    ## Validation

    - [ ] `python python -m pytest tests/test_document.py -v` — all status tests pass
    - [ ] `python python -c "from wiki.document import parse_document; ..."` — parses status from real plan file
