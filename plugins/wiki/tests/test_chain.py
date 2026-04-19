"""Tests for chain.py — SkillChainDocument parsing and validation."""

from __future__ import annotations

from pathlib import Path

import pytest  # noqa: F401

# ── Helpers ──────────────────────────────────────────────────────────


def _chain_md(
    name: str = "Test Chain",
    description: str = "A test chain",
    goal: str = "Produce updated wiki pages",
    negative_scope: str = "Does not handle auth",
    steps: list[dict] | None = None,
) -> str:
    """Build a valid *.chain.md manifest string."""
    if steps is None:
        steps = [
            {
                "step": "1",
                "skill": "research",
                "input_contract": "user question",
                "output_contract": "research.md file",
                "gate": "",
            },
            {
                "step": "2",
                "skill": "distill",
                "input_contract": "research.md file",
                "output_contract": "context files updated",
                "gate": "user approves summary",
            },
        ]

    fm = "\n".join([
        "---",
        f"name: {name}",
        f"description: {description}",
        "type: chain",
        f"goal: {goal}",
        f"negative-scope: {negative_scope}",
        "---",
        "",
    ])

    table_header = "| Step | Skill | Input Contract | Output Contract | Gate |"
    table_sep = "|------|-------|----------------|-----------------|------|"
    rows = []
    for s in steps:
        rows.append(
            f"| {s['step']} | {s['skill']} | {s['input_contract']}"
            f" | {s['output_contract']} | {s['gate']} |"
        )

    body = "\n".join([
        "## Steps",
        "",
        table_header,
        table_sep,
        *rows,
        "",
    ])

    return fm + body


# ── TestParseChain ────────────────────────────────────────────────────


class TestParseChain:
    def test_returns_correct_frontmatter_fields(self, tmp_path: Path) -> None:
        from wiki.skill_chain import parse_chain

        path = tmp_path / "my.chain.md"
        path.write_text(_chain_md(), encoding="utf-8")

        doc = parse_chain(path)

        assert doc.name == "Test Chain"
        assert doc.description == "A test chain"
        assert doc.type == "chain"
        assert doc.goal == "Produce updated wiki pages"
        assert doc.negative_scope == "Does not handle auth"

    def test_returns_steps_list_with_correct_keys(self, tmp_path: Path) -> None:
        from wiki.skill_chain import parse_chain

        path = tmp_path / "my.chain.md"
        path.write_text(_chain_md(), encoding="utf-8")

        doc = parse_chain(path)

        assert len(doc.steps) == 2
        step = doc.steps[0]
        expected_keys = {"step", "skill", "input_contract", "output_contract", "gate"}
        assert set(step.keys()) == expected_keys
        assert step["step"] == "1"
        assert step["skill"] == "research"
        assert step["input_contract"] == "user question"
        assert step["output_contract"] == "research.md file"

    def test_missing_steps_section_records_error(self, tmp_path: Path) -> None:
        from wiki.skill_chain import parse_chain

        content = (
            "---\n"
            "name: Broken Chain\n"
            "description: Missing steps\n"
            "type: chain\n"
            "goal: Something\n"
            "negative-scope: Nothing\n"
            "---\n\n"
            "No steps table here.\n"
        )
        path = tmp_path / "broken.chain.md"
        path.write_text(content, encoding="utf-8")

        doc = parse_chain(path)

        # Parse succeeds but steps error is surfaced via issues()
        assert doc.steps == []
        issues = doc.issues(tmp_path)
        assert any("Steps" in i["issue"] for i in issues)

    def test_empty_goal_parsed_as_empty_string(self, tmp_path: Path) -> None:
        from wiki.skill_chain import parse_chain

        content = (
            "---\n"
            "name: No Goal\n"
            "description: Missing goal\n"
            "type: chain\n"
            "---\n\n"
            "## Steps\n\n"
            "| Step | Skill | Input Contract | Output Contract | Gate |\n"
            "|------|-------|----------------|-----------------|------|\n"
            "| 1 | research | question | result | |\n"
        )
        path = tmp_path / "nogoal.chain.md"
        path.write_text(content, encoding="utf-8")

        doc = parse_chain(path)

        assert doc.goal == ""

    def test_wrong_type_raises_value_error(self, tmp_path: Path) -> None:
        from wiki.skill_chain import parse_chain

        content = (
            "---\n"
            "name: Not A Chain\n"
            "description: Wrong type\n"
            "type: research\n"
            "sources:\n"
            "  - https://example.com\n"
            "---\n\nSome content.\n"
        )
        path = tmp_path / "wrong.chain.md"
        path.write_text(content, encoding="utf-8")

        with pytest.raises(ValueError, match="expected type 'chain'"):
            parse_chain(path)


# ── TestSkillChainDocumentIssues ───────────────────────────────────────────


class TestSkillChainDocumentIssues:
    def _make_skills_dir(self, tmp_path: Path, skill_names: list[str]) -> Path:
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()
        for name in skill_names:
            (skills_dir / name).mkdir()
        return skills_dir

    # skill existence checks

    def test_declared_skill_found_no_skill_issues(self, tmp_path: Path) -> None:
        from wiki.skill_chain import parse_chain

        skills_dir = self._make_skills_dir(tmp_path, ["research", "distill"])
        path = tmp_path / "my.chain.md"
        path.write_text(_chain_md(), encoding="utf-8")

        doc = parse_chain(path)
        issues = doc.issues(tmp_path, skills_dirs=[skills_dir])

        skill_issues = [i for i in issues if "does not exist" in i["issue"]]
        assert skill_issues == []

    def test_declared_skill_absent_returns_one_fail(self, tmp_path: Path) -> None:
        from wiki.skill_chain import parse_chain

        skills_dir = self._make_skills_dir(tmp_path, ["research"])
        path = tmp_path / "my.chain.md"
        path.write_text(
            _chain_md(
                steps=[
                    {"step": "1", "skill": "ghost-skill",
                     "input_contract": "q", "output_contract": "r", "gate": ""},
                ]
            ),
            encoding="utf-8",
        )

        doc = parse_chain(path)
        issues = doc.issues(tmp_path, skills_dirs=[skills_dir])

        skill_issues = [i for i in issues if "does not exist" in i["issue"]]
        assert len(skill_issues) == 1
        assert skill_issues[0]["severity"] == "fail"
        assert "ghost-skill" in skill_issues[0]["issue"]

    def test_multiple_missing_skills_multiple_fails(self, tmp_path: Path) -> None:
        from wiki.skill_chain import parse_chain

        skills_dir = self._make_skills_dir(tmp_path, [])
        path = tmp_path / "my.chain.md"
        path.write_text(
            _chain_md(
                steps=[
                    {"step": "1", "skill": "missing-a",
                     "input_contract": "x", "output_contract": "y", "gate": ""},
                    {"step": "2", "skill": "missing-b",
                     "input_contract": "y", "output_contract": "z", "gate": ""},
                ]
            ),
            encoding="utf-8",
        )

        doc = parse_chain(path)
        issues = doc.issues(tmp_path, skills_dirs=[skills_dir])

        skill_issues = [i for i in issues if "does not exist" in i["issue"]]
        assert len(skill_issues) == 2
        assert all(i["severity"] == "fail" for i in skill_issues)

    # termination condition checks

    def test_empty_goal_returns_fail(self, tmp_path: Path) -> None:
        from wiki.skill_chain import parse_chain

        path = tmp_path / "my.chain.md"
        path.write_text(
            _chain_md(goal="", steps=[]),
            encoding="utf-8",
        )

        doc = parse_chain(path)
        issues = doc.issues(tmp_path)

        term_issues = [i for i in issues if "termination" in i["issue"]]
        assert len(term_issues) == 1
        assert term_issues[0]["severity"] == "fail"

    def test_nonempty_goal_no_termination_issue(self, tmp_path: Path) -> None:
        from wiki.skill_chain import parse_chain

        skills_dir = self._make_skills_dir(tmp_path, ["research", "distill"])
        path = tmp_path / "my.chain.md"
        path.write_text(_chain_md(), encoding="utf-8")

        doc = parse_chain(path)
        issues = doc.issues(tmp_path, skills_dirs=[skills_dir])

        term_issues = [i for i in issues if "termination" in i["issue"]]
        assert term_issues == []

    # cycle / step-order checks

    def test_step_numbers_out_of_order_returns_fail(self, tmp_path: Path) -> None:
        from wiki.skill_chain import parse_chain

        path = tmp_path / "my.chain.md"
        path.write_text(
            _chain_md(
                steps=[
                    {"step": "1", "skill": "research",
                     "input_contract": "q", "output_contract": "r", "gate": ""},
                    {"step": "3", "skill": "distill",
                     "input_contract": "r", "output_contract": "c", "gate": ""},
                    {"step": "2", "skill": "ingest",
                     "input_contract": "c", "output_contract": "pages", "gate": ""},
                ]
            ),
            encoding="utf-8",
        )

        doc = parse_chain(path)
        issues = doc.issues(tmp_path)

        assert any(
            i["severity"] == "fail" and "strictly increasing" in i["issue"]
            for i in issues
        )

    def test_same_skill_consecutive_steps_returns_fail(self, tmp_path: Path) -> None:
        from wiki.skill_chain import parse_chain

        path = tmp_path / "my.chain.md"
        path.write_text(
            _chain_md(
                steps=[
                    {"step": "1", "skill": "research",
                     "input_contract": "q", "output_contract": "r", "gate": ""},
                    {"step": "2", "skill": "research",
                     "input_contract": "r", "output_contract": "r2", "gate": ""},
                ]
            ),
            encoding="utf-8",
        )

        doc = parse_chain(path)
        issues = doc.issues(tmp_path)

        assert any(
            i["severity"] == "fail" and "direct loop" in i["issue"]
            for i in issues
        )

    def test_valid_step_sequence_no_cycle_issues(self, tmp_path: Path) -> None:
        from wiki.skill_chain import parse_chain

        skills_dir = self._make_skills_dir(tmp_path, ["research", "distill", "ingest"])
        path = tmp_path / "my.chain.md"
        path.write_text(
            _chain_md(
                steps=[
                    {"step": "1", "skill": "research",
                     "input_contract": "q", "output_contract": "r", "gate": ""},
                    {"step": "2", "skill": "distill",
                     "input_contract": "r", "output_contract": "c",
                     "gate": "approval"},
                    {"step": "3", "skill": "ingest",
                     "input_contract": "c", "output_contract": "pages updated",
                     "gate": "lint passes"},
                ]
            ),
            encoding="utf-8",
        )

        doc = parse_chain(path)
        issues = doc.issues(tmp_path, skills_dirs=[skills_dir])

        cycle_issues = [
            i for i in issues
            if "strictly increasing" in i["issue"] or "direct loop" in i["issue"]
        ]
        assert cycle_issues == []


# ── TestValidateChain ─────────────────────────────────────────────────


class TestValidateChain:
    def test_clean_manifest_with_skills_no_failures(self, tmp_path: Path) -> None:
        from wiki.skill_chain import validate_chain

        # Create skills directory with the two skills used
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()
        (skills_dir / "research").mkdir()
        (skills_dir / "distill").mkdir()

        manifest_path = tmp_path / "my.chain.md"
        manifest_path.write_text(_chain_md(), encoding="utf-8")

        issues = validate_chain(manifest_path, [skills_dir])

        failures = [i for i in issues if i["severity"] == "fail"]
        assert failures == [], failures

    def test_manifest_missing_skills_surfaces_failures(self, tmp_path: Path) -> None:
        from wiki.skill_chain import validate_chain

        # Empty skills directory — no skills defined
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()

        manifest_path = tmp_path / "my.chain.md"
        manifest_path.write_text(_chain_md(), encoding="utf-8")

        issues = validate_chain(manifest_path, [skills_dir])

        failures = [i for i in issues if i["severity"] == "fail"]
        assert len(failures) >= 1
        assert any("research" in i["issue"] or "distill" in i["issue"]
                   for i in failures)

    def test_malformed_manifest_returns_single_warn(self, tmp_path: Path) -> None:
        from wiki.skill_chain import validate_chain

        # Missing frontmatter — will fail to parse
        manifest_path = tmp_path / "bad.chain.md"
        manifest_path.write_text("No frontmatter here.\n", encoding="utf-8")

        issues = validate_chain(manifest_path, [])

        assert len(issues) == 1
        assert issues[0]["severity"] == "warn"
        assert "Invalid chain manifest" in issues[0]["issue"]
