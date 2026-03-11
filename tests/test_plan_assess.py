"""Tests for wos/plan/assess_plan.py."""

from __future__ import annotations


class TestParseTasks:
    """Tests for _parse_tasks() — checkbox extraction."""

    def test_unchecked_tasks(self) -> None:
        """Unchecked tasks parsed with completed=False."""
        from wos.plan.assess_plan import _parse_tasks

        content = (
            "### Tasks\n"
            "\n"
            "- [ ] Task 1: Create package structure\n"
            "- [ ] Task 2: Write tests\n"
        )
        tasks = _parse_tasks(content)
        assert len(tasks) == 2
        assert tasks[0] == {
            "index": 1,
            "title": "Create package structure",
            "completed": False,
            "sha": None,
        }
        assert tasks[1] == {
            "index": 2,
            "title": "Write tests",
            "completed": False,
            "sha": None,
        }

    def test_checked_tasks_with_sha(self) -> None:
        """Checked tasks with SHA annotation parsed correctly."""
        from wos.plan.assess_plan import _parse_tasks

        content = (
            "- [x] Task 1: Create package <!-- sha:a1b2c3d -->\n"
            "- [x] Task 2: Write tests <!-- sha:e4f5g6h -->\n"
            "- [ ] Task 3: Implement parser\n"
        )
        tasks = _parse_tasks(content)
        assert len(tasks) == 3
        assert tasks[0]["completed"] is True
        assert tasks[0]["sha"] == "a1b2c3d"
        assert tasks[1]["sha"] == "e4f5g6h"
        assert tasks[2]["completed"] is False
        assert tasks[2]["sha"] is None

    def test_checked_tasks_without_sha(self) -> None:
        """Checked tasks without SHA have sha=None."""
        from wos.plan.assess_plan import _parse_tasks

        content = "- [x] Task 1: Create package\n"
        tasks = _parse_tasks(content)
        assert tasks[0]["completed"] is True
        assert tasks[0]["sha"] is None

    def test_empty_content(self) -> None:
        """No checkboxes returns empty list."""
        from wos.plan.assess_plan import _parse_tasks

        assert _parse_tasks("# Just a heading\n\nSome text.\n") == []

    def test_nested_checkboxes_ignored(self) -> None:
        """Indented sub-checkboxes (step-level) are not treated as tasks."""
        from wos.plan.assess_plan import _parse_tasks

        content = (
            "- [ ] Task 1: Create package\n"
            "  - [ ] Step 1a: Write init file\n"
            "  - [ ] Step 1b: Add docstring\n"
            "- [ ] Task 2: Write tests\n"
        )
        tasks = _parse_tasks(content)
        assert len(tasks) == 2

    def test_title_without_task_prefix(self) -> None:
        """Checkboxes without 'Task N:' prefix use full text as title."""
        from wos.plan.assess_plan import _parse_tasks

        content = "- [ ] Create package structure\n- [ ] Write tests\n"
        tasks = _parse_tasks(content)
        assert tasks[0]["title"] == "Create package structure"
        assert tasks[1]["title"] == "Write tests"


class TestDetectSections:
    """Tests for _detect_sections() — required section detection."""

    def test_all_sections_present(self) -> None:
        """All 6 required sections detected."""
        from wos.plan.assess_plan import _detect_sections

        content = (
            "## Goal\n\nBuild the thing.\n\n"
            "## Scope\n\nMust/Won't.\n\n"
            "## Approach\n\nHow.\n\n"
            "## File Changes\n\n- Create: foo.py\n\n"
            "## Tasks\n\n- [ ] Do stuff\n\n"
            "## Validation\n\n- [ ] pytest passes\n"
        )
        result = _detect_sections(content)
        assert result == {
            "goal": True,
            "scope": True,
            "approach": True,
            "file_changes": True,
            "tasks": True,
            "validation": True,
            "all_present": True,
        }

    def test_missing_sections(self) -> None:
        """Missing sections reported as False, all_present is False."""
        from wos.plan.assess_plan import _detect_sections

        content = "## Goal\n\nBuild it.\n\n## Tasks\n\n- [ ] Do it\n"
        result = _detect_sections(content)
        assert result["goal"] is True
        assert result["tasks"] is True
        assert result["scope"] is False
        assert result["approach"] is False
        assert result["file_changes"] is False
        assert result["validation"] is False
        assert result["all_present"] is False

    def test_heading_level_insensitive(self) -> None:
        """Detects sections at any heading level."""
        from wos.plan.assess_plan import _detect_sections

        content = "### Goal\n\n#### Scope\n\n# Approach\n\n"
        result = _detect_sections(content)
        assert result["goal"] is True
        assert result["scope"] is True
        assert result["approach"] is True

    def test_file_changes_with_spaces(self) -> None:
        """'File Changes' heading detected (two words)."""
        from wos.plan.assess_plan import _detect_sections

        content = "## File Changes\n\n- Modify: foo.py\n"
        result = _detect_sections(content)
        assert result["file_changes"] is True

    def test_empty_content(self) -> None:
        """Empty content returns all False."""
        from wos.plan.assess_plan import _detect_sections

        result = _detect_sections("")
        assert result["all_present"] is False
        assert all(v is False for k, v in result.items() if k != "all_present")
