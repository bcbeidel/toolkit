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


class TestExtractFileChanges:
    """Tests for _extract_file_changes() — file path extraction."""

    def test_extracts_paths_from_file_changes_section(self) -> None:
        """Paths extracted from Create/Modify/Delete/Test lines."""
        from wos.plan.assess_plan import _extract_file_changes

        content = (
            "## File Changes\n"
            "- Create: `wos/plan/__init__.py`\n"
            "- Create: `wos/plan/assess_plan.py`\n"
            "- Modify: `wos/document.py`\n"
            "- Test: `tests/test_plan_assess.py`\n"
            "\n"
            "## Tasks\n"
            "- [ ] Task 1\n"
        )
        files = _extract_file_changes(content)
        assert "wos/plan/__init__.py" in files
        assert "wos/plan/assess_plan.py" in files
        assert "wos/document.py" in files
        assert "tests/test_plan_assess.py" in files

    def test_no_file_changes_section(self) -> None:
        """Returns empty list when no File Changes section exists."""
        from wos.plan.assess_plan import _extract_file_changes

        content = "## Goal\n\nBuild it.\n\n## Tasks\n\n- [ ] Do it\n"
        assert _extract_file_changes(content) == []

    def test_paths_without_backticks(self) -> None:
        """Paths without backticks still extracted."""
        from wos.plan.assess_plan import _extract_file_changes

        content = (
            "## File Changes\n"
            "- Create: wos/plan/__init__.py\n"
            "- Modify: wos/document.py\n"
            "\n"
            "## Tasks\n"
        )
        files = _extract_file_changes(content)
        assert "wos/plan/__init__.py" in files
        assert "wos/document.py" in files

    def test_stops_at_next_section(self) -> None:
        """Only parses files within File Changes section."""
        from wos.plan.assess_plan import _extract_file_changes

        content = (
            "## File Changes\n"
            "- Create: `wos/plan/assess_plan.py`\n"
            "\n"
            "## Tasks\n"
            "- Create: `not/a/file/change.py`\n"
        )
        files = _extract_file_changes(content)
        assert files == ["wos/plan/assess_plan.py"]

    def test_line_with_colon_and_range(self) -> None:
        """Paths with line ranges like 'file.py:123-145' extract just path."""
        from wos.plan.assess_plan import _extract_file_changes

        content = (
            "## File Changes\n"
            "- Modify: `wos/document.py:72-81`\n"
        )
        files = _extract_file_changes(content)
        assert files == ["wos/document.py"]


class TestMapTaskFiles:
    """Tests for _map_task_files() — task-to-file mapping."""

    def test_maps_files_under_task_headings(self) -> None:
        """Files listed under task headings mapped to those tasks."""
        from wos.plan.assess_plan import _map_task_files

        tasks = [
            {"index": 1, "title": "Create package", "completed": False, "sha": None},
            {"index": 2, "title": "Write tests", "completed": False, "sha": None},
        ]
        file_changes = [
            "wos/plan/__init__.py",
            "wos/plan/assess_plan.py",
            "tests/test_plan_assess.py",
        ]
        content = (
            "### Task 1: Create package\n"
            "\n"
            "**Files:**\n"
            "- Create: `wos/plan/__init__.py`\n"
            "- Create: `wos/plan/assess_plan.py`\n"
            "\n"
            "### Task 2: Write tests\n"
            "\n"
            "**Files:**\n"
            "- Create: `tests/test_plan_assess.py`\n"
        )
        result = _map_task_files(tasks, file_changes, content)
        assert result["1"] == ["wos/plan/__init__.py", "wos/plan/assess_plan.py"]
        assert result["2"] == ["tests/test_plan_assess.py"]

    def test_flat_file_list_assigns_all(self) -> None:
        """Without per-task grouping, all files assigned to all tasks."""
        from wos.plan.assess_plan import _map_task_files

        tasks = [
            {"index": 1, "title": "Task A", "completed": False, "sha": None},
            {"index": 2, "title": "Task B", "completed": False, "sha": None},
        ]
        file_changes = ["foo.py", "bar.py"]
        content = (
            "## File Changes\n"
            "- Create: `foo.py`\n"
            "- Create: `bar.py`\n"
            "\n"
            "## Tasks\n"
            "- [ ] Task A\n"
            "- [ ] Task B\n"
        )
        result = _map_task_files(tasks, file_changes, content)
        assert result["1"] == ["foo.py", "bar.py"]
        assert result["2"] == ["foo.py", "bar.py"]

    def test_empty_tasks(self) -> None:
        """No tasks returns empty map."""
        from wos.plan.assess_plan import _map_task_files

        assert _map_task_files([], ["foo.py"], "content") == {}


class TestFindOverlaps:
    """Tests for _find_overlaps() — file overlap detection."""

    def test_no_overlaps(self) -> None:
        """Tasks with disjoint files return empty overlap list."""
        from wos.plan.assess_plan import _find_overlaps

        task_file_map = {"1": ["foo.py"], "2": ["bar.py"], "3": ["baz.py"]}
        assert _find_overlaps(task_file_map) == []

    def test_overlapping_tasks(self) -> None:
        """Tasks sharing files detected as overlapping pairs."""
        from wos.plan.assess_plan import _find_overlaps

        task_file_map = {
            "1": ["foo.py", "bar.py"],
            "2": ["bar.py"],
            "3": ["baz.py"],
        }
        overlaps = _find_overlaps(task_file_map)
        assert len(overlaps) == 1
        assert overlaps[0] == {"tasks": ["1", "2"], "shared_files": ["bar.py"]}

    def test_multiple_overlaps(self) -> None:
        """Multiple overlap pairs all reported."""
        from wos.plan.assess_plan import _find_overlaps

        task_file_map = {
            "1": ["a.py"],
            "2": ["a.py", "b.py"],
            "3": ["b.py"],
        }
        overlaps = _find_overlaps(task_file_map)
        assert len(overlaps) == 2

    def test_empty_map(self) -> None:
        """Empty map returns empty list."""
        from wos.plan.assess_plan import _find_overlaps

        assert _find_overlaps({}) == []


class TestAssessFile:
    """Tests for assess_file() — full plan assessment."""

    def _write_plan(
        self, path, status="approved", tasks_content="",
        file_changes_content="",
    ):
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
            f"## File Changes\n{file_changes_content}\n\n"
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
            file_changes_content="- Create: `foo.py`\n",
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

    def test_parallel_eligibility(self, tmp_path) -> None:
        """Plan with 3+ non-overlapping tasks is parallel eligible."""
        from wos.plan.assess_plan import assess_file

        plan = tmp_path / "plan.md"
        content = (
            "---\n"
            "name: Parallel Plan\n"
            "description: A parallel plan\n"
            "type: plan\n"
            "status: approved\n"
            "---\n"
            "\n## Goal\n\nBuild.\n\n## Scope\n\nAll.\n\n"
            "## Approach\n\nParallel.\n\n"
            "## File Changes\n"
            "- Create: `a.py`\n- Create: `b.py`\n- Create: `c.py`\n\n"
            "### Task 1: A\n\n**Files:**\n- Create: `a.py`\n\n"
            "- [ ] Do A\n\n"
            "### Task 2: B\n\n**Files:**\n- Create: `b.py`\n\n"
            "- [ ] Do B\n\n"
            "### Task 3: C\n\n**Files:**\n- Create: `c.py`\n\n"
            "- [ ] Do C\n\n"
            "## Validation\n\n- [ ] Works\n"
        )
        plan.write_text(content)
        result = assess_file(str(plan))
        assert result["readiness"]["parallel_eligible"] is True
        assert result["file_changes"]["overlapping_tasks"] == []

    def test_not_parallel_with_overlaps(self, tmp_path) -> None:
        """Plan with overlapping files is not parallel eligible."""
        from wos.plan.assess_plan import assess_file

        plan = tmp_path / "plan.md"
        content = (
            "---\n"
            "name: Overlap Plan\n"
            "description: Overlapping\n"
            "type: plan\n"
            "status: approved\n"
            "---\n"
            "\n## Goal\n\nBuild.\n\n## Scope\n\nAll.\n\n"
            "## Approach\n\nSequential.\n\n"
            "## File Changes\n"
            "- Modify: `shared.py`\n- Create: `b.py`\n"
            "- Create: `c.py`\n\n"
            "### Task 1: A\n\n**Files:**\n- Modify: `shared.py`\n\n"
            "- [ ] Do A\n\n"
            "### Task 2: B\n\n**Files:**\n"
            "- Modify: `shared.py`\n- Create: `b.py`\n\n"
            "- [ ] Do B\n\n"
            "### Task 3: C\n\n**Files:**\n- Create: `c.py`\n\n"
            "- [ ] Do C\n\n"
            "## Validation\n\n- [ ] Works\n"
        )
        plan.write_text(content)
        result = assess_file(str(plan))
        assert result["readiness"]["parallel_eligible"] is False
        assert len(result["file_changes"]["overlapping_tasks"]) > 0


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
