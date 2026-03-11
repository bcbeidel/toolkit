---
name: Plan Document Format Implementation
description: Add status field to Document model, create plan-format reference, and retrofit existing plans — issue #157
type: plan
status: completed
related:
  - docs/plans/2026-03-11-plan-document-format-design.md
---

# Plan Document Format Implementation

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development
> (if subagents available) or superpowers:executing-plans to implement this plan.
> Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship the plan document format spec (#157) — add `status` to the
Document model with parse-time validation, create a self-contained reference
doc for downstream skills, and retrofit existing plans.

**Architecture:** Three changes: (1) extend Document dataclass with `status`
field + enum validation in `parse_document()`, (2) create
`skills/_shared/references/plan-format.md` as the canonical format reference,
(3) add `type: plan` and `status` frontmatter to the one existing plan with
checkboxes.

**Tech Stack:** Python 3.9 (stdlib only), pytest

**Branch:** `feat/157-plan-document-format`
**PR:** TBD

---

### Task 1: Add `status` field to Document dataclass

**Files:**
- Modify: `wos/document.py:16` (`_KNOWN_FIELDS`)
- Modify: `wos/document.py:19-30` (Document dataclass)
- Test: `tests/test_document.py`

- [x] **Step 1: Write failing test — status field exists on Document**

```python
# In tests/test_document.py, add to TestDocument class:
def test_status_field_default(self) -> None:
    from wos.document import Document

    doc = Document(
        path="docs/plans/test.md",
        name="Test",
        description="A test plan",
        content="# Test\n",
    )
    assert doc.status is None
```

- [x] **Step 2: Run test to verify it fails**

Run: `uv run python -m pytest tests/test_document.py::TestDocument::test_status_field_default -v`
Expected: FAIL — `Document.__init__() got an unexpected keyword argument` or `has no attribute 'status'`

- [x] **Step 3: Add status field to Document dataclass and _KNOWN_FIELDS**

In `wos/document.py`:

```python
# Line 16: update _KNOWN_FIELDS
_KNOWN_FIELDS = {"name", "description", "type", "sources", "related", "status"}

# In Document dataclass, after related field (line 29):
    status: Optional[str] = None
```

- [x] **Step 4: Run test to verify it passes**

Run: `uv run python -m pytest tests/test_document.py::TestDocument::test_status_field_default -v`
Expected: PASS

- [x] **Step 5: Commit**

```bash
git add wos/document.py tests/test_document.py
git commit -m "feat: add status field to Document dataclass"
```

---

### Task 2: Parse `status` from frontmatter in `parse_document()`

**Files:**
- Modify: `wos/document.py:63-80` (parse_document extraction and return)
- Test: `tests/test_document.py`

- [x] **Step 1: Write failing test — status parsed from frontmatter**

```python
# In tests/test_document.py, add to TestParseDocument class:
def test_plan_with_status(self) -> None:
    from wos.document import parse_document

    text = (
        "---\n"
        "name: My Plan\n"
        "description: A plan with status\n"
        "type: plan\n"
        "status: draft\n"
        "---\n"
        "# My Plan\n"
    )
    doc = parse_document("docs/plans/test.md", text)
    assert doc.status == "draft"
    assert doc.type == "plan"
```

- [x] **Step 2: Run test to verify it fails**

Run: `uv run python -m pytest tests/test_document.py::TestParseDocument::test_plan_with_status -v`
Expected: FAIL — `doc.status` is `None` because `parse_document` doesn't extract it yet

- [x] **Step 3: Add status extraction to parse_document()**

In `wos/document.py`, in the "Extract known fields" section (after line 70):

```python
    status: Optional[str] = fm.get("status")
    if not isinstance(status, str) and status is not None:
        status = str(status)
```

And update the return statement to include `status=status`.

- [x] **Step 4: Run test to verify it passes**

Run: `uv run python -m pytest tests/test_document.py::TestParseDocument::test_plan_with_status -v`
Expected: PASS

- [x] **Step 5: Commit**

```bash
git add wos/document.py tests/test_document.py
git commit -m "feat: parse status field from frontmatter"
```

---

### Task 3: Add status enum validation in `parse_document()`

**Files:**
- Modify: `wos/document.py:63-80` (add validation after extraction)
- Test: `tests/test_document.py`

- [x] **Step 1: Write failing test — invalid status raises ValueError**

```python
# In tests/test_document.py, add to TestParseDocument class:
def test_raises_on_invalid_status(self) -> None:
    from wos.document import parse_document

    text = (
        "---\n"
        "name: Bad Plan\n"
        "description: A plan with invalid status\n"
        "type: plan\n"
        "status: done\n"
        "---\n"
        "# Bad Plan\n"
    )
    with pytest.raises(ValueError, match="status"):
        parse_document("docs/plans/bad.md", text)
```

- [x] **Step 2: Write test — all valid statuses accepted**

```python
def test_all_valid_statuses(self) -> None:
    from wos.document import parse_document

    for status in ("draft", "approved", "executing", "completed", "abandoned"):
        text = (
            "---\n"
            f"name: Plan {status}\n"
            f"description: A plan with status {status}\n"
            "type: plan\n"
            f"status: {status}\n"
            "---\n"
            "# Plan\n"
        )
        doc = parse_document("docs/plans/test.md", text)
        assert doc.status == status
```

- [x] **Step 3: Run tests to verify they fail**

Run: `uv run python -m pytest tests/test_document.py::TestParseDocument::test_raises_on_invalid_status tests/test_document.py::TestParseDocument::test_all_valid_statuses -v`
Expected: `test_raises_on_invalid_status` FAILS (no ValueError raised), `test_all_valid_statuses` PASSES

- [x] **Step 4: Add status validation to parse_document()**

In `wos/document.py`, after status extraction, before the return statement:

```python
    _VALID_STATUSES = {"draft", "approved", "executing", "completed", "abandoned"}
    if status is not None and status not in _VALID_STATUSES:
        raise ValueError(
            f"{path}: invalid status '{status}', "
            f"must be one of: {', '.join(sorted(_VALID_STATUSES))}"
        )
```

- [x] **Step 5: Run all tests to verify they pass**

Run: `uv run python -m pytest tests/test_document.py -v`
Expected: ALL PASS

- [x] **Step 6: Commit**

```bash
git add wos/document.py tests/test_document.py
git commit -m "feat: validate status against allowed values"
```

---

### Task 4: Update existing test for status field recognition

**Files:**
- Modify: `tests/test_document.py:119-139` (`test_unknown_fields_ignored`)

- [x] **Step 1: Update test_unknown_fields_ignored**

The test currently asserts `not hasattr(doc, "status")`. Since `status` is now
a known field, update it:

```python
def test_unknown_fields_ignored(self) -> None:
    from wos.document import parse_document

    text = (
        "---\n"
        "name: Custom Doc\n"
        "description: A document with extra fields\n"
        "status: draft\n"
        "priority: high\n"
        "tags:\n"
        "  - python\n"
        "  - testing\n"
        "---\n"
        "# Custom Doc\n"
    )
    doc = parse_document("docs/context/misc/custom.md", text)
    assert doc.name == "Custom Doc"
    assert doc.description == "A document with extra fields"
    assert doc.status == "draft"  # status is now a known field
    # Truly unknown fields are not stored
    assert not hasattr(doc, "priority")
```

- [x] **Step 2: Run test to verify it passes**

Run: `uv run python -m pytest tests/test_document.py::TestParseDocument::test_unknown_fields_ignored -v`
Expected: PASS

- [x] **Step 3: Run full test suite**

Run: `uv run python -m pytest tests/ -v`
Expected: ALL PASS

- [x] **Step 4: Commit**

```bash
git add tests/test_document.py
git commit -m "test: update test_unknown_fields_ignored for status field"
```

---

### Task 5: Create plan-format reference document

**Files:**
- Create: `skills/_shared/references/plan-format.md`

- [x] **Step 1: Write the reference document**

Create `skills/_shared/references/plan-format.md` with the full self-contained
spec from the design doc: frontmatter schema, required sections table,
lifecycle state machine with transitions, task decomposition rules, and design
justification table. This is the canonical reference for downstream skills
(write-plan, execute-plan, validate-plan).

- [x] **Step 2: Verify the file reads correctly**

Visually verify it's well-formatted and self-contained. No broken references.

- [x] **Step 3: Commit**

```bash
git add skills/_shared/references/plan-format.md
git commit -m "docs: add plan-format reference for downstream skills"
```

---

### Task 6: Retrofit existing plan with type and status

**Files:**
- Modify: `docs/plans/2026-03-06-audit-validation-enhancements-plan.md` (frontmatter)

- [x] **Step 1: Add type: plan and status: completed to frontmatter**

This is the only existing plan with checkboxes (13/13 checked). Add:

```yaml
type: plan
status: completed
```

- [x] **Step 2: Verify the document still parses correctly**

Run: `uv run python -c "from wos.document import parse_document; import pathlib; t = pathlib.Path('docs/plans/2026-03-06-audit-validation-enhancements-plan.md').read_text(); d = parse_document('test', t); print(d.status, d.type)"`
Expected: `completed plan`

- [x] **Step 3: Commit**

```bash
git add docs/plans/2026-03-06-audit-validation-enhancements-plan.md
git commit -m "chore: retrofit plan with type and status frontmatter"
```

---

### Task 7: Update this plan's status to executing

**Files:**
- Modify: `docs/plans/2026-03-11-plan-document-format-implementation.md` (this file)

- [x] **Step 1: Change status from draft to executing**

Update the frontmatter of this plan file to `status: executing` now that
execution has begun. This validates the lifecycle transition.

- [x] **Step 2: Commit**

```bash
git add docs/plans/2026-03-11-plan-document-format-implementation.md
git commit -m "chore: transition plan status to executing"
```

---

## Validation

- [x] `uv run python -m pytest tests/ -v` — all tests pass
- [x] `uv run python -m pytest tests/test_document.py -v` — status-specific tests pass
- [x] `skills/_shared/references/plan-format.md` exists and is self-contained
- [x] At least one existing plan has `type: plan` and `status: completed`
- [x] This plan file itself uses the new format (`type: plan`, `status`)
