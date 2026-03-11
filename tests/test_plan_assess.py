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
