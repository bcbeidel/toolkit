---
name: "Audit Validation Enhancements Implementation Plan"
description: "TDD implementation plan for #132 (min word count) and #133 (skill density reporting)"
related:
  - docs/plans/2026-03-06-audit-validation-enhancements-design.md
  - docs/research/2026-03-05-skill-density-threshold.md
---

# Audit Validation Enhancements Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add minimum word count warning for context files (#132) and skill instruction density reporting (#133) to the WOS audit system.

**Architecture:** #132 extends the existing `check_content()` function in `wos/validators.py` with a `min_words` parameter. #133 adds a new module `wos/skill_audit.py` with three functions for measuring skill instruction density, called from `scripts/audit.py`. Both follow TDD: write failing test, implement, verify, commit.

**Tech Stack:** Python 3.9, stdlib only, pytest

**Branch:** `feat/132-133-audit-validation-enhancements`
**PR:** #139

---

- [x] Task 1: Create branch
- [x] Task 2: Add min_words failing tests (#132)
- [x] Task 3: Implement min_words in check_content (#132)
- [x] Task 4: Add --context-min-words CLI flag (#132)
- [x] Task 5: Write failing tests for strip_frontmatter (#133)
- [x] Task 6: Implement strip_frontmatter (#133)
- [x] Task 7: Write failing tests for count_instruction_lines (#133)
- [x] Task 8: Implement count_instruction_lines (#133)
- [x] Task 9: Write failing tests for check_skill_sizes (#133)
- [x] Task 10: Implement check_skill_sizes (#133)
- [x] Task 11: Integrate skill density into audit script (#133)
- [x] Task 12: Update CLAUDE.md and design doc
- [x] Task 13: Run full validation and create PR

---

## Task 1: Create branch

**Step 1: Create and switch to feature branch**

Run: `git checkout -b feat/132-133-audit-validation-enhancements`

**Step 2: Push branch**

Run: `git push -u origin feat/132-133-audit-validation-enhancements`

---

## Task 2: Add min_words failing tests (#132)

**Files:**
- Modify: `tests/test_validators.py` (add tests to `TestCheckContent` class, after line 201)

**Step 1: Write failing tests**

Add these tests to the `TestCheckContent` class in `tests/test_validators.py`:

```python
def test_below_min_words_warns(self) -> None:
    from wos.validators import check_content

    doc = _make_doc(
        path="docs/context/api/auth.md",
        content="Word " * 50,
    )
    issues = check_content(doc)
    assert len(issues) == 1
    assert issues[0]["severity"] == "warn"
    assert "50" in issues[0]["issue"]

def test_above_min_words_no_warning(self) -> None:
    from wos.validators import check_content

    doc = _make_doc(
        path="docs/context/api/auth.md",
        content="Word " * 200,
    )
    issues = check_content(doc)
    assert issues == []

def test_exactly_at_min_threshold_no_warning(self) -> None:
    from wos.validators import check_content

    doc = _make_doc(
        path="docs/context/api/auth.md",
        content="Word " * 100,
    )
    issues = check_content(doc)
    assert issues == []

def test_custom_min_words(self) -> None:
    from wos.validators import check_content

    doc = _make_doc(
        path="docs/context/api/auth.md",
        content="Word " * 150,
    )
    issues = check_content(doc, min_words=200)
    assert len(issues) == 1

def test_artifact_file_no_min_warning(self) -> None:
    from wos.validators import check_content

    doc = _make_doc(
        path="docs/research/topic.md",
        content="Word " * 10,
    )
    issues = check_content(doc)
    assert issues == []

def test_index_file_excluded_from_min_check(self) -> None:
    from wos.validators import check_content

    doc = _make_doc(
        path="docs/context/api/_index.md",
        content="Word " * 10,
    )
    issues = check_content(doc)
    assert issues == []
```

**Step 2: Run tests to verify they fail**

Run: `uv run python -m pytest tests/test_validators.py::TestCheckContent -v`

Expected: `test_below_min_words_warns` and `test_custom_min_words` FAIL (no min_words check yet). Others should PASS (they don't trigger the new behavior).

---

## Task 3: Implement min_words in check_content (#132)

**Files:**
- Modify: `wos/validators.py:78-108` (update `check_content()` function)

**Step 1: Add min_words parameter and check**

Update `check_content()` signature and add the min check after the max check:

```python
def check_content(
    doc: Document,
    context_path: str = "docs/context",
    max_words: int = 800,
    min_words: int = 100,
) -> List[dict]:
    """Warn when context files exceed or fall below word count thresholds.

    Only checks files under context_path. Non-context files and _index.md
    files are excluded.

    Args:
        doc: A parsed Document instance.
        context_path: Path prefix for context files.
        max_words: Upper word count threshold (default 800).
        min_words: Lower word count threshold (default 100).

    Returns:
        List of issue dicts. Empty if within thresholds.
    """
    if not doc.path.startswith(context_path + "/"):
        return []
    if doc.path.endswith("_index.md"):
        return []

    word_count = len(doc.content.split())
    if word_count > max_words:
        return [{
            "file": doc.path,
            "issue": f"Context file is {word_count} words (threshold: {max_words})",
            "severity": "warn",
        }]
    if word_count < min_words:
        return [{
            "file": doc.path,
            "issue": f"Context file is {word_count} words (minimum: {min_words})",
            "severity": "warn",
        }]
    return []
```

**Step 2: Run tests to verify they pass**

Run: `uv run python -m pytest tests/test_validators.py::TestCheckContent -v`

Expected: All PASS

**Step 3: Run full test suite**

Run: `uv run python -m pytest tests/ -v`

Expected: All PASS

**Step 4: Commit**

```bash
git add wos/validators.py tests/test_validators.py
git commit -m "feat: add min_words warning to check_content (#132)"
```

---

## Task 4: Add --context-min-words CLI flag (#132)

**Files:**
- Modify: `scripts/audit.py:71-76` (add new argument after `--context-max-words`)

**Step 1: Add the argument**

Add after the `--context-max-words` argument block (after line 76):

```python
parser.add_argument(
    "--context-min-words",
    type=int,
    default=100,
    help="Minimum word count for context file warnings (default: 100)",
)
```

**Step 2: Update the usage docstring**

Update line 9 to include the new flag:

```python
"""Run WOS validation checks on a project.

Usage:
    uv run scripts/audit.py [FILE] [--root DIR] [--no-urls] [--json]
                            [--fix] [--strict] [--context-max-words N]
                            [--context-min-words N]
"""
```

**Step 3: Verify --help shows the new flag**

Run: `uv run scripts/audit.py --help`

Expected: `--context-min-words` appears in output

Note: The CLI flag is added for completeness, but `check_content()` is
currently called from `validate_file()` which doesn't pass through CLI
args for min/max words. This matches the existing pattern — `--context-max-words`
is also defined but not yet wired through `validate_file()`. Both flags
are available for direct script usage and future wiring.

**Step 4: Commit**

```bash
git add scripts/audit.py
git commit -m "feat: add --context-min-words CLI flag (#132)"
```

---

## Task 5: Write failing tests for strip_frontmatter (#133)

**Files:**
- Create: `tests/test_skill_audit.py`

**Step 1: Write tests**

```python
"""Tests for wos/skill_audit.py — skill instruction density measurement."""

from __future__ import annotations


# ── strip_frontmatter ─────────────────────────────────────────


class TestStripFrontmatter:
    def test_removes_yaml_frontmatter(self) -> None:
        from wos.skill_audit import strip_frontmatter

        text = "---\nname: Test\ndescription: A test\n---\n# Content\n"
        result = strip_frontmatter(text)
        assert result.strip() == "# Content"

    def test_no_frontmatter_unchanged(self) -> None:
        from wos.skill_audit import strip_frontmatter

        text = "# Content\n\nSome text.\n"
        result = strip_frontmatter(text)
        assert result == text

    def test_unclosed_frontmatter_unchanged(self) -> None:
        from wos.skill_audit import strip_frontmatter

        text = "---\nname: Test\n# Content\n"
        result = strip_frontmatter(text)
        assert result == text
```

**Step 2: Run tests to verify they fail**

Run: `uv run python -m pytest tests/test_skill_audit.py::TestStripFrontmatter -v`

Expected: FAIL with `ModuleNotFoundError: No module named 'wos.skill_audit'`

---

## Task 6: Implement strip_frontmatter (#133)

**Files:**
- Create: `wos/skill_audit.py`

**Step 1: Create module with strip_frontmatter**

```python
"""Skill instruction density measurement.

Measures instruction line counts and word counts per skill directory.
Used by the audit script to report skill sizes and warn when skills
exceed configurable thresholds.
"""

from __future__ import annotations


def strip_frontmatter(text: str) -> str:
    """Remove YAML frontmatter (--- delimited) from text."""
    if not text.startswith("---"):
        return text
    end = text.find("---", 3)
    if end == -1:
        return text
    return text[end + 3:]
```

**Step 2: Run tests to verify they pass**

Run: `uv run python -m pytest tests/test_skill_audit.py::TestStripFrontmatter -v`

Expected: All PASS

**Step 3: Commit**

```bash
git add wos/skill_audit.py tests/test_skill_audit.py
git commit -m "feat: add strip_frontmatter to skill_audit module (#133)"
```

---

## Task 7: Write failing tests for count_instruction_lines (#133)

**Files:**
- Modify: `tests/test_skill_audit.py` (add new test class)

**Step 1: Write tests**

Append to `tests/test_skill_audit.py`:

```python
# ── count_instruction_lines ───────────────────────────────────


class TestCountInstructionLines:
    def test_counts_bullet_points(self) -> None:
        from wos.skill_audit import count_instruction_lines

        text = "- First instruction\n- Second instruction\n- Third\n"
        assert count_instruction_lines(text) == 3

    def test_excludes_blank_lines(self) -> None:
        from wos.skill_audit import count_instruction_lines

        text = "- First\n\n- Second\n\n"
        assert count_instruction_lines(text) == 2

    def test_excludes_headers(self) -> None:
        from wos.skill_audit import count_instruction_lines

        text = "# Header\n## Subheader\n- Instruction\n"
        assert count_instruction_lines(text) == 1

    def test_excludes_code_fences(self) -> None:
        from wos.skill_audit import count_instruction_lines

        text = "```python\nprint('hello')\n```\n"
        assert count_instruction_lines(text) == 1  # print line counts

    def test_excludes_table_separators(self) -> None:
        from wos.skill_audit import count_instruction_lines

        text = "| Name | Value |\n|------|-------|\n| a | 1 |\n"
        assert count_instruction_lines(text) == 2  # header row + data row

    def test_excludes_horizontal_rules(self) -> None:
        from wos.skill_audit import count_instruction_lines

        text = "- First\n---\n- Second\n***\n- Third\n"
        assert count_instruction_lines(text) == 3

    def test_counts_prose(self) -> None:
        from wos.skill_audit import count_instruction_lines

        text = "This is a paragraph of text.\nAnother sentence here.\n"
        assert count_instruction_lines(text) == 2

    def test_counts_numbered_steps(self) -> None:
        from wos.skill_audit import count_instruction_lines

        text = "1. First step\n2. Second step\n3. Third step\n"
        assert count_instruction_lines(text) == 3

    def test_counts_table_data_rows(self) -> None:
        from wos.skill_audit import count_instruction_lines

        text = "| col1 | col2 |\n| --- | --- |\n| data | data |\n| more | more |\n"
        assert count_instruction_lines(text) == 3  # header + 2 data rows

    def test_empty_text(self) -> None:
        from wos.skill_audit import count_instruction_lines

        assert count_instruction_lines("") == 0
```

**Step 2: Run tests to verify they fail**

Run: `uv run python -m pytest tests/test_skill_audit.py::TestCountInstructionLines -v`

Expected: FAIL with `ImportError` (function doesn't exist yet)

---

## Task 8: Implement count_instruction_lines (#133)

**Files:**
- Modify: `wos/skill_audit.py` (add function)

**Step 1: Add count_instruction_lines**

Append to `wos/skill_audit.py`:

```python
def count_instruction_lines(text: str) -> int:
    """Count lines that carry instructional content.

    Excludes blank lines, markdown headers, code fences,
    table separators, and horizontal rules.
    """
    count = 0
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("#"):
            continue
        if stripped.startswith("```"):
            continue
        if stripped.startswith("|") and set(stripped) <= set("|-: "):
            continue
        if set(stripped) <= set("-* _"):
            continue
        count += 1
    return count
```

**Step 2: Run tests to verify they pass**

Run: `uv run python -m pytest tests/test_skill_audit.py::TestCountInstructionLines -v`

Expected: All PASS

**Step 3: Commit**

```bash
git add wos/skill_audit.py tests/test_skill_audit.py
git commit -m "feat: add count_instruction_lines to skill_audit (#133)"
```

---

## Task 9: Write failing tests for check_skill_sizes (#133)

**Files:**
- Modify: `tests/test_skill_audit.py` (add new test class)

**Step 1: Write tests**

Append to `tests/test_skill_audit.py`:

```python
from pathlib import Path


# ── check_skill_sizes ─────────────────────────────────────────


def _create_skill(
    tmp_path: Path,
    name: str,
    skill_content: str,
    ref_contents: dict[str, str] | None = None,
) -> None:
    """Helper to create a skill directory with SKILL.md and optional refs."""
    skill_dir = tmp_path / name
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_text(skill_content, encoding="utf-8")
    if ref_contents:
        refs_dir = skill_dir / "references"
        refs_dir.mkdir()
        for filename, content in ref_contents.items():
            (refs_dir / filename).write_text(content, encoding="utf-8")


class TestCheckSkillSizes:
    def test_skill_under_threshold_no_issues(self, tmp_path: Path) -> None:
        from wos.skill_audit import check_skill_sizes

        _create_skill(tmp_path, "small", "---\nname: S\n---\n- Do thing\n")
        summaries, issues = check_skill_sizes(tmp_path)
        assert len(summaries) == 1
        assert issues == []

    def test_skill_over_threshold_warns(self, tmp_path: Path) -> None:
        from wos.skill_audit import check_skill_sizes

        lines = "\n".join(f"- Instruction {i}" for i in range(250))
        _create_skill(tmp_path, "big", f"---\nname: B\n---\n{lines}\n")
        summaries, issues = check_skill_sizes(tmp_path, max_lines=200)
        assert len(issues) == 1
        assert issues[0]["severity"] == "warn"
        assert "big" in issues[0]["file"]

    def test_shared_excluded(self, tmp_path: Path) -> None:
        from wos.skill_audit import check_skill_sizes

        _create_skill(tmp_path, "_shared", "---\nname: S\n---\n- Shared ref\n")
        summaries, issues = check_skill_sizes(tmp_path)
        assert len(summaries) == 0
        assert issues == []

    def test_no_skills_dir(self, tmp_path: Path) -> None:
        from wos.skill_audit import check_skill_sizes

        nonexistent = tmp_path / "nope"
        summaries, issues = check_skill_sizes(nonexistent)
        assert summaries == []
        assert issues == []

    def test_configurable_threshold(self, tmp_path: Path) -> None:
        from wos.skill_audit import check_skill_sizes

        lines = "\n".join(f"- Instruction {i}" for i in range(50))
        _create_skill(tmp_path, "medium", f"---\nname: M\n---\n{lines}\n")
        _, issues_high = check_skill_sizes(tmp_path, max_lines=200)
        _, issues_low = check_skill_sizes(tmp_path, max_lines=10)
        assert issues_high == []
        assert len(issues_low) == 1

    def test_zero_threshold_disables_warnings(self, tmp_path: Path) -> None:
        from wos.skill_audit import check_skill_sizes

        lines = "\n".join(f"- Instruction {i}" for i in range(500))
        _create_skill(tmp_path, "huge", f"---\nname: H\n---\n{lines}\n")
        summaries, issues = check_skill_sizes(tmp_path, max_lines=0)
        assert len(summaries) == 1  # still measured
        assert issues == []  # but no warnings

    def test_includes_reference_files(self, tmp_path: Path) -> None:
        from wos.skill_audit import check_skill_sizes

        _create_skill(
            tmp_path,
            "with-refs",
            "---\nname: W\n---\n- Main instruction\n",
            ref_contents={"guide.md": "---\nname: G\n---\n- Ref line\n"},
        )
        summaries, issues = check_skill_sizes(tmp_path)
        assert len(summaries) == 1
        assert summaries[0]["ref_lines"] > 0

    def test_summary_has_expected_fields(self, tmp_path: Path) -> None:
        from wos.skill_audit import check_skill_sizes

        _create_skill(
            tmp_path,
            "complete",
            "---\nname: C\n---\n- One\n- Two\n",
            ref_contents={"ref.md": "---\nname: R\n---\n- Ref\n"},
        )
        summaries, _ = check_skill_sizes(tmp_path)
        s = summaries[0]
        assert s["name"] == "complete"
        assert "skill_lines" in s
        assert "ref_lines" in s
        assert "total_lines" in s
        assert "words" in s
        assert "files" in s
```

**Step 2: Run tests to verify they fail**

Run: `uv run python -m pytest tests/test_skill_audit.py::TestCheckSkillSizes -v`

Expected: FAIL with `ImportError` (function doesn't exist yet)

---

## Task 10: Implement check_skill_sizes (#133)

**Files:**
- Modify: `wos/skill_audit.py` (add function and Path import)

**Step 1: Add import and function**

Add `from pathlib import Path` and `from typing import List, Tuple` to the
imports at the top, then append:

```python
def check_skill_sizes(
    skills_dir: Path,
    max_lines: int = 200,
) -> Tuple[List[dict], List[dict]]:
    """Measure instruction density per skill and warn if over threshold.

    Walks skills_dir, measures each skill (SKILL.md + references/*.md).
    Directories starting with '_' (e.g., _shared) are excluded.

    Args:
        skills_dir: Path to the skills/ directory.
        max_lines: Instruction line threshold for warnings (default 200).
            Set to 0 to disable warnings while still measuring.

    Returns:
        Tuple of (summaries, issues):
        - summaries: list of dicts with name, skill_lines, ref_lines,
          total_lines, words, files
        - issues: list of issue dicts for skills over threshold
    """
    summaries: List[dict] = []
    issues: List[dict] = []

    if not skills_dir.is_dir():
        return summaries, issues

    for entry in sorted(skills_dir.iterdir()):
        if not entry.is_dir():
            continue
        if entry.name.startswith("_"):
            continue

        skill_md = entry / "SKILL.md"
        if not skill_md.is_file():
            continue

        # Measure SKILL.md
        raw = skill_md.read_text(encoding="utf-8")
        content = strip_frontmatter(raw)
        skill_lines = count_instruction_lines(content)
        total_words = len(content.split())
        file_count = 1

        # Measure references
        ref_lines = 0
        refs_dir = entry / "references"
        if refs_dir.is_dir():
            for ref_file in sorted(refs_dir.rglob("*.md")):
                raw = ref_file.read_text(encoding="utf-8")
                content = strip_frontmatter(raw)
                ref_lines += count_instruction_lines(content)
                total_words += len(content.split())
                file_count += 1

        total_lines = skill_lines + ref_lines
        summaries.append({
            "name": entry.name,
            "skill_lines": skill_lines,
            "ref_lines": ref_lines,
            "total_lines": total_lines,
            "words": total_words,
            "files": file_count,
        })

        if max_lines > 0 and total_lines > max_lines:
            issues.append({
                "file": f"skills/{entry.name}",
                "issue": (
                    f"Skill has {total_lines} instruction lines"
                    f" (threshold: {max_lines})"
                ),
                "severity": "warn",
            })

    return summaries, issues
```

**Step 2: Run tests to verify they pass**

Run: `uv run python -m pytest tests/test_skill_audit.py -v`

Expected: All PASS

**Step 3: Run full test suite**

Run: `uv run python -m pytest tests/ -v`

Expected: All PASS

**Step 4: Commit**

```bash
git add wos/skill_audit.py tests/test_skill_audit.py
git commit -m "feat: add check_skill_sizes to skill_audit (#133)"
```

---

## Task 11: Integrate skill density into audit script (#133)

**Files:**
- Modify: `scripts/audit.py`

**Step 1: Add --skill-max-lines argument**

Add after the `--context-min-words` argument block:

```python
parser.add_argument(
    "--skill-max-lines",
    type=int,
    default=200,
    help=(
        "Instruction line threshold for skill density warnings"
        " (default: 200, 0 to disable)"
    ),
)
```

**Step 2: Add skill density check and summary output**

After the `--fix` block (after line 115) and before the severity counting
(before line 117), add:

```python
# Skill instruction density reporting
from wos.skill_audit import check_skill_sizes

skills_dir = root / "skills"
if skills_dir.is_dir():
    summaries, skill_issues = check_skill_sizes(
        skills_dir, max_lines=args.skill_max_lines,
    )
    issues.extend(skill_issues)

    if summaries and not args.json_output:
        print("Skill Instruction Density:", file=sys.stderr)
        for s in sorted(summaries, key=lambda x: -x["total_lines"]):
            flag = "  [warn]" if (
                args.skill_max_lines > 0
                and s["total_lines"] > args.skill_max_lines
            ) else ""
            print(
                f"  {s['name']:<20}"
                f" {s['skill_lines']:>4} (SKILL)"
                f" + {s['ref_lines']:>4} (refs)"
                f" = {s['total_lines']:>4} lines,"
                f" {s['words']:>5} words{flag}",
                file=sys.stderr,
            )
        print(file=sys.stderr)
```

**Step 3: Update the usage docstring**

```python
"""Run WOS validation checks on a project.

Usage:
    uv run scripts/audit.py [FILE] [--root DIR] [--no-urls] [--json]
                            [--fix] [--strict] [--context-max-words N]
                            [--context-min-words N] [--skill-max-lines N]
"""
```

**Step 4: Run the audit on this repo to verify output**

Run: `uv run scripts/audit.py --root . --no-urls`

Expected: Skill Instruction Density table appears on stderr with all 7
skills listed. `research` and `refine-prompt` show `[warn]` flags.

**Step 5: Verify JSON mode doesn't print summary table**

Run: `uv run scripts/audit.py --root . --no-urls --json | python3 -m json.tool | head -20`

Expected: Valid JSON output, no stderr summary table.

**Step 6: Verify --skill-max-lines 0 disables warnings**

Run: `uv run scripts/audit.py --root . --no-urls --skill-max-lines 0`

Expected: Summary table still prints, but no `[warn]` flags and no
skill-related issues in the output.

**Step 7: Commit**

```bash
git add scripts/audit.py
git commit -m "feat: integrate skill density reporting into audit (#133)"
```

---

## Task 12: Update CLAUDE.md and design doc

**Files:**
- Modify: `CLAUDE.md` (update validator count and check descriptions)
- Modify: `docs/plans/2026-03-06-audit-validation-enhancements-design.md` (add branch/PR)

**Step 1: Update CLAUDE.md**

In the Validation section, the check count and descriptions should reflect
the new capabilities. Update the `check_content` description to mention
min/max, and add `skill_audit.py` to the package structure list.

In the Package Structure section, add:
```
  - `skill_audit.py` — skill instruction density measurement
```

**Step 2: Update design doc header**

Fill in the Branch and PR fields at the top of the design doc.

**Step 3: Commit**

```bash
git add CLAUDE.md docs/plans/2026-03-06-audit-validation-enhancements-design.md
git commit -m "docs: update CLAUDE.md and design doc for #132, #133"
```

---

## Task 13: Run full validation and create PR

**Step 1: Run full test suite**

Run: `uv run python -m pytest tests/ -v`

Expected: All PASS

**Step 2: Run the audit on this repo**

Run: `uv run scripts/audit.py --root . --no-urls`

Expected: Clean output with skill density table on stderr

**Step 3: Create pull request**

Run:
```bash
gh pr create --title "feat: add min word count warning and skill density reporting (#132, #133)" --body "$(cat <<'EOF'
## Summary

- **#132:** Add `min_words` parameter to `check_content()` (default 100, severity warn) for context files that are too short
- **#133:** Add `wos/skill_audit.py` module with instruction line counting and `check_skill_sizes()`. Audit prints skill density summary to stderr and warns for skills exceeding configurable threshold (default 200 instruction lines)

## Research

- Threshold anchored on Claude Code's documented 200-line guidance for instruction files
- IFScale provides directional support (more directives = worse compliance) but units are incommensurable
- Du et al. shows raw context size degrades performance independently

## Test plan

- [ ] `uv run python -m pytest tests/ -v` — all pass
- [ ] `uv run scripts/audit.py --root . --no-urls` — skill density table appears
- [ ] `uv run scripts/audit.py --root . --no-urls --skill-max-lines 0` — no warnings
- [ ] `uv run scripts/audit.py --root . --no-urls --json` — valid JSON, no summary table

Closes #132, closes #133

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

**Step 4: Record PR URL in design doc**
