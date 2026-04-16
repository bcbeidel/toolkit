"""Tests for wos/plan/assess_plan.py."""

from __future__ import annotations


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
        from wiki.plan import PlanDocument

        plan = tmp_path / "plan.md"
        self._write_plan(
            plan,
            tasks_content=(
                "- [ ] Task 1: Do stuff\n"
                "- [ ] Task 2: More stuff\n"
            ),
        )
        result = PlanDocument.assess(str(plan))
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
        from wiki.plan import PlanDocument

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
        result = PlanDocument.assess(str(plan))
        assert result["frontmatter"]["status"] == "executing"
        assert result["tasks"]["total"] == 3
        assert result["tasks"]["completed"] == 1
        assert result["tasks"]["pending"] == 2
        assert result["tasks"]["items"][0]["sha"] == "abc1234"
        assert result["readiness"]["status_ok"] is True

    def test_draft_plan_not_ready(self, tmp_path) -> None:
        """Draft plan reports status_ok=False."""
        from wiki.plan import PlanDocument

        plan = tmp_path / "plan.md"
        self._write_plan(plan, status="draft")
        result = PlanDocument.assess(str(plan))
        assert result["readiness"]["status_ok"] is False
        assert any("draft" in i.lower() for i in result["readiness"]["issues"])

    def test_nonexistent_file(self) -> None:
        """Non-existent file returns exists=False."""
        from wiki.plan import PlanDocument

        result = PlanDocument.assess("/nonexistent/plan.md")
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
        from wiki.plan import PlanDocument

        plans_dir = tmp_path / "docs" / "plans"
        plans_dir.mkdir(parents=True)
        self._make_plan(plans_dir / "a.md", "Plan A", status="executing")
        self._make_plan(plans_dir / "b.md", "Plan B", status="draft")
        self._make_plan(plans_dir / "c.md", "Plan C", status="executing")

        result = PlanDocument.scan(str(tmp_path))
        assert len(result["plans"]) == 2
        names = {p["name"] for p in result["plans"]}
        assert names == {"Plan A", "Plan C"}

    def test_empty_directory(self, tmp_path) -> None:
        """Empty plans directory returns empty list."""
        from wiki.plan import PlanDocument

        plans_dir = tmp_path / "docs" / "plans"
        plans_dir.mkdir(parents=True)
        result = PlanDocument.scan(str(tmp_path))
        assert result["plans"] == []

    def test_missing_directory(self, tmp_path) -> None:
        """Missing docs/plans returns empty list."""
        from wiki.plan import PlanDocument

        result = PlanDocument.scan(str(tmp_path))
        assert result["plans"] == []

    def test_skips_non_plan_docs(self, tmp_path) -> None:
        """Non-plan documents are ignored."""
        from wiki.plan import PlanDocument

        plans_dir = tmp_path / "docs" / "plans"
        plans_dir.mkdir(parents=True)
        (plans_dir / "design.md").write_text(
            "---\nname: Design\ndescription: A design\n"
            "type: design\n---\n# Design\n"
        )
        self._make_plan(
            plans_dir / "plan.md", "Real Plan", status="executing",
        )

        result = PlanDocument.scan(str(tmp_path))
        assert len(result["plans"]) == 1

    def test_skips_index_files(self, tmp_path) -> None:
        """Index files are skipped."""
        from wiki.plan import PlanDocument

        plans_dir = tmp_path / "docs" / "plans"
        plans_dir.mkdir(parents=True)
        (plans_dir / "_index.md").write_text("# Plans Index\n")
        result = PlanDocument.scan(str(tmp_path))
        assert result["plans"] == []
