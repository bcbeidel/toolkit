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

    def test_validation_heading_closes_gate(self) -> None:
        """Checkboxes after Validation heading are excluded."""
        from wos.plan.assess_plan import _parse_tasks

        content = (
            "## Tasks\n"
            "\n"
            "- [ ] Task 1: Real task\n"
            "- [ ] Task 2: Also real\n"
            "\n"
            "## Validation\n"
            "\n"
            "- [ ] pytest passes\n"
            "- [ ] linter clean\n"
        )
        tasks = _parse_tasks(content)
        assert len(tasks) == 2

    def test_chunk_headings_preserved(self) -> None:
        """Chunk sub-headings inside Tasks section do not close the gate."""
        from wos.plan.assess_plan import _parse_tasks

        content = (
            "## Tasks\n"
            "\n"
            "### Chunk 1: First work\n"
            "\n"
            "- [ ] Task 1: Do the first thing\n"
            "\n"
            "### Chunk 2: Second work\n"
            "\n"
            "- [ ] Task 2: Do the second thing\n"
            "\n"
            "## Validation\n"
            "\n"
            "- [ ] Not a task\n"
        )
        tasks = _parse_tasks(content)
        assert len(tasks) == 2
        assert tasks[0]["title"] == "Do the first thing"
        assert tasks[1]["title"] == "Do the second thing"

    def test_non_task_non_chunk_heading_closes_gate(self) -> None:
        """Non-task, non-chunk headings after Tasks section close the gate."""
        from wos.plan.assess_plan import _parse_tasks

        content = (
            "## Goal\n"
            "\n"
            "- [ ] Not a task (in goal)\n"
            "\n"
            "## Tasks\n"
            "\n"
            "- [ ] Task 1: Real task\n"
            "\n"
            "## Notes\n"
            "\n"
            "- [ ] Not a task (in notes)\n"
            "\n"
            "## Validation\n"
            "\n"
            "- [ ] Not a task (in validation)\n"
        )
        tasks = _parse_tasks(content)
        assert len(tasks) == 1
        assert tasks[0]["title"] == "Real task"

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


class TestAssessFile:
    """Tests for assess_file() — full plan assessment."""

    def _write_plan(self, path, status="approved", tasks_content=""):
        """Helper to create a plan file."""
        content = (
            "---\n"
            "name: Test Plan\n"
            "description: A test plan\n"
            "type: plan\n"
            f"status: {status}\n"
            "---\n"
            "\n"
            "## Goal\n\nBuild the thing.\n\n"
            "## Scope\n\nMust/Won't.\n\n"
            "## Approach\n\nHow.\n\n"
            "## File Changes\n\n- Create: foo.py\n\n"
            f"## Tasks\n{tasks_content}\n\n"
            "## Validation\n\n- [ ] pytest passes\n"
        )
        path.write_text(content)

    def test_approved_plan_ready(self, tmp_path) -> None:
        """Approved plan with all sections reports ready."""
        from wos.plan.assess_plan import assess_file

        plan = tmp_path / "plan.md"
        self._write_plan(
            plan,
            tasks_content=(
                "- [ ] Task 1: Do stuff\n"
                "- [ ] Task 2: More stuff\n"
            ),
        )
        result = assess_file(str(plan))
        assert result["exists"] is True
        assert result["frontmatter"]["status"] == "approved"
        assert result["sections"]["all_present"] is True
        assert result["tasks"]["total"] == 2
        assert result["tasks"]["completed"] == 0
        assert result["tasks"]["pending"] == 2
        assert result["readiness"]["status_ok"] is True
        assert result["readiness"]["sections_complete"] is True
        assert result["readiness"]["has_pending_tasks"] is True
        assert "file_changes" not in result
        assert "parallel_eligible" not in result["readiness"]

    def test_executing_plan_with_progress(self, tmp_path) -> None:
        """Executing plan reports correct completed/pending counts."""
        from wos.plan.assess_plan import assess_file

        plan = tmp_path / "plan.md"
        self._write_plan(
            plan,
            status="executing",
            tasks_content=(
                "- [x] Task 1: Done <!-- sha:abc1234 -->\n"
                "- [ ] Task 2: Pending\n"
                "- [ ] Task 3: Also pending\n"
            ),
        )
        result = assess_file(str(plan))
        assert result["frontmatter"]["status"] == "executing"
        assert result["tasks"]["total"] == 3
        assert result["tasks"]["completed"] == 1
        assert result["tasks"]["pending"] == 2
        assert result["tasks"]["items"][0]["sha"] == "abc1234"
        assert result["readiness"]["status_ok"] is True

    def test_draft_plan_not_ready(self, tmp_path) -> None:
        """Draft plan reports status_ok=False."""
        from wos.plan.assess_plan import assess_file

        plan = tmp_path / "plan.md"
        self._write_plan(plan, status="draft")
        result = assess_file(str(plan))
        assert result["readiness"]["status_ok"] is False
        assert any("draft" in i.lower() for i in result["readiness"]["issues"])

    def test_nonexistent_file(self) -> None:
        """Non-existent file returns exists=False."""
        from wos.plan.assess_plan import assess_file

        result = assess_file("/nonexistent/plan.md")
        assert result["exists"] is False
        assert result["frontmatter"] is None


class TestScanPlans:
    """Tests for scan_plans() — find executing plans."""

    def _make_plan(self, path, name, status="draft"):
        path.write_text(
            f"---\nname: {name}\ndescription: A plan\n"
            f"type: plan\nstatus: {status}\n---\n"
            "## Goal\n\nDo it.\n"
        )

    def test_finds_executing_plans(self, tmp_path) -> None:
        """Scan returns only plans with status: executing."""
        from wos.plan.assess_plan import scan_plans

        plans_dir = tmp_path / "docs" / "plans"
        plans_dir.mkdir(parents=True)
        self._make_plan(plans_dir / "a.md", "Plan A", status="executing")
        self._make_plan(plans_dir / "b.md", "Plan B", status="draft")
        self._make_plan(plans_dir / "c.md", "Plan C", status="executing")

        result = scan_plans(str(tmp_path))
        assert len(result["plans"]) == 2
        names = {p["name"] for p in result["plans"]}
        assert names == {"Plan A", "Plan C"}

    def test_empty_directory(self, tmp_path) -> None:
        """Empty plans directory returns empty list."""
        from wos.plan.assess_plan import scan_plans

        plans_dir = tmp_path / "docs" / "plans"
        plans_dir.mkdir(parents=True)
        result = scan_plans(str(tmp_path))
        assert result["plans"] == []

    def test_missing_directory(self, tmp_path) -> None:
        """Missing docs/plans returns empty list."""
        from wos.plan.assess_plan import scan_plans

        result = scan_plans(str(tmp_path))
        assert result["plans"] == []

    def test_skips_non_plan_docs(self, tmp_path) -> None:
        """Non-plan documents are ignored."""
        from wos.plan.assess_plan import scan_plans

        plans_dir = tmp_path / "docs" / "plans"
        plans_dir.mkdir(parents=True)
        (plans_dir / "design.md").write_text(
            "---\nname: Design\ndescription: A design\n"
            "type: design\n---\n# Design\n"
        )
        self._make_plan(
            plans_dir / "plan.md", "Real Plan", status="executing",
        )

        result = scan_plans(str(tmp_path))
        assert len(result["plans"]) == 1

    def test_skips_index_files(self, tmp_path) -> None:
        """Index files are skipped."""
        from wos.plan.assess_plan import scan_plans

        plans_dir = tmp_path / "docs" / "plans"
        plans_dir.mkdir(parents=True)
        (plans_dir / "_index.md").write_text("# Plans Index\n")
        result = scan_plans(str(tmp_path))
        assert result["plans"] == []
