"""Tests for wos/chain.py — chain manifest parsing and validator functions."""

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
        from wos.chain import parse_chain

        path = tmp_path / "my.chain.md"
        path.write_text(_chain_md(), encoding="utf-8")

        manifest = parse_chain(path)

        assert manifest["name"] == "Test Chain"
        assert manifest["description"] == "A test chain"
        assert manifest["type"] == "chain"
        assert manifest["goal"] == "Produce updated wiki pages"
        assert manifest["negative_scope"] == "Does not handle auth"

    def test_returns_steps_list_with_correct_keys(self, tmp_path: Path) -> None:
        from wos.chain import parse_chain

        path = tmp_path / "my.chain.md"
        path.write_text(_chain_md(), encoding="utf-8")

        manifest = parse_chain(path)

        assert len(manifest["steps"]) == 2
        step = manifest["steps"][0]
        expected_keys = {"step", "skill", "input_contract", "output_contract", "gate"}
        assert set(step.keys()) == expected_keys
        assert step["step"] == "1"
        assert step["skill"] == "research"
        assert step["input_contract"] == "user question"
        assert step["output_contract"] == "research.md file"

    def test_missing_steps_section_raises_value_error(self, tmp_path: Path) -> None:
        from wos.chain import parse_chain

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

        with pytest.raises(ValueError, match="Steps"):
            parse_chain(path)

    def test_empty_goal_parsed_as_empty_string(self, tmp_path: Path) -> None:
        from wos.chain import parse_chain

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

        manifest = parse_chain(path)

        assert manifest["goal"] == ""


# ── TestCheckChainSkillsExist ─────────────────────────────────────────


class TestCheckChainSkillsExist:
    def _make_skills_dir(self, tmp_path: Path, skill_names: list[str]) -> Path:
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()
        for name in skill_names:
            (skills_dir / name).mkdir()
        return skills_dir

    def test_declared_skill_found_no_issues(self, tmp_path: Path) -> None:
        from wos.chain import check_chain_skills_exist

        skills_dir = self._make_skills_dir(tmp_path, ["research", "distill"])
        manifest = {
            "path": str(tmp_path / "my.chain.md"),
            "steps": [
                {"step": "1", "skill": "research", "input_contract": "q",
                 "output_contract": "r", "gate": ""},
                {"step": "2", "skill": "distill", "input_contract": "r",
                 "output_contract": "c", "gate": "approval"},
            ],
        }

        issues = check_chain_skills_exist(manifest, [skills_dir])

        assert issues == []

    def test_declared_skill_absent_returns_one_fail(self, tmp_path: Path) -> None:
        from wos.chain import check_chain_skills_exist

        skills_dir = self._make_skills_dir(tmp_path, ["research"])
        manifest = {
            "path": str(tmp_path / "my.chain.md"),
            "steps": [
                {"step": "1", "skill": "ghost-skill", "input_contract": "q",
                 "output_contract": "r", "gate": ""},
            ],
        }

        issues = check_chain_skills_exist(manifest, [skills_dir])

        assert len(issues) == 1
        assert issues[0]["severity"] == "fail"
        assert "ghost-skill" in issues[0]["issue"]

    def test_multiple_missing_skills_multiple_fails(self, tmp_path: Path) -> None:
        from wos.chain import check_chain_skills_exist

        skills_dir = self._make_skills_dir(tmp_path, [])
        manifest = {
            "path": str(tmp_path / "my.chain.md"),
            "steps": [
                {"step": "1", "skill": "missing-a", "input_contract": "x",
                 "output_contract": "y", "gate": ""},
                {"step": "2", "skill": "missing-b", "input_contract": "y",
                 "output_contract": "z", "gate": "approval"},
            ],
        }

        issues = check_chain_skills_exist(manifest, [skills_dir])

        assert len(issues) == 2
        assert all(i["severity"] == "fail" for i in issues)


# ── TestCheckChainInternalConsistency ────────────────────────────────


class TestCheckChainInternalConsistency:
    def test_empty_input_contract_returns_warn(self, tmp_path: Path) -> None:
        from wos.chain import check_chain_internal_consistency

        manifest = {
            "path": str(tmp_path / "my.chain.md"),
            "steps": [
                {"step": "1", "skill": "research", "input_contract": "",
                 "output_contract": "research.md", "gate": ""},
            ],
        }

        issues = check_chain_internal_consistency(manifest)

        assert any(i["severity"] == "warn" and "input contract" in i["issue"]
                   for i in issues)

    def test_empty_output_contract_returns_warn(self, tmp_path: Path) -> None:
        from wos.chain import check_chain_internal_consistency

        manifest = {
            "path": str(tmp_path / "my.chain.md"),
            "steps": [
                {"step": "1", "skill": "research", "input_contract": "question",
                 "output_contract": "", "gate": ""},
            ],
        }

        issues = check_chain_internal_consistency(manifest)

        assert any(i["severity"] == "warn" and "output contract" in i["issue"]
                   for i in issues)

    def test_contracts_no_shared_words_returns_warn(self, tmp_path: Path) -> None:
        from wos.chain import check_chain_internal_consistency

        manifest = {
            "path": str(tmp_path / "my.chain.md"),
            "steps": [
                {"step": "1", "skill": "research", "input_contract": "user question",
                 "output_contract": "orange apple banana", "gate": ""},
                {"step": "2", "skill": "distill",
                 "input_contract": "totally unrelated xyz",
                 "output_contract": "context pages", "gate": "approval"},
            ],
        }

        issues = check_chain_internal_consistency(manifest)

        assert any("shares no terms" in i["issue"] for i in issues)

    def test_matching_contracts_no_issues(self, tmp_path: Path) -> None:
        from wos.chain import check_chain_internal_consistency

        manifest = {
            "path": str(tmp_path / "my.chain.md"),
            "steps": [
                {"step": "1", "skill": "research", "input_contract": "user question",
                 "output_contract": "research.md file", "gate": ""},
                {"step": "2", "skill": "distill", "input_contract": "research.md path",
                 "output_contract": "context files updated", "gate": "approval"},
            ],
        }

        issues = check_chain_internal_consistency(manifest)

        assert issues == []


# ── TestCheckChainGates ───────────────────────────────────────────────


class TestCheckChainGates:
    def test_consequential_step_without_gate_returns_warn(self, tmp_path: Path) -> None:
        from wos.chain import check_chain_gates

        manifest = {
            "path": str(tmp_path / "my.chain.md"),
            "steps": [
                {"step": "1", "skill": "ingest", "input_contract": "data",
                 "output_contract": "pages updated", "gate": ""},
            ],
        }

        issues = check_chain_gates(manifest)

        assert len(issues) == 1
        assert issues[0]["severity"] == "warn"
        assert "ingest" in issues[0]["issue"]

    def test_research_step_without_gate_no_warn(self, tmp_path: Path) -> None:
        from wos.chain import check_chain_gates

        manifest = {
            "path": str(tmp_path / "my.chain.md"),
            "steps": [
                {"step": "1", "skill": "research", "input_contract": "question",
                 "output_contract": "research.md", "gate": ""},
            ],
        }

        issues = check_chain_gates(manifest)

        assert issues == []

    def test_gate_present_no_issues(self, tmp_path: Path) -> None:
        from wos.chain import check_chain_gates

        manifest = {
            "path": str(tmp_path / "my.chain.md"),
            "steps": [
                {"step": "1", "skill": "ingest", "input_contract": "data",
                 "output_contract": "pages updated", "gate": "user approves"},
            ],
        }

        issues = check_chain_gates(manifest)

        assert issues == []


# ── TestCheckChainTermination ─────────────────────────────────────────


class TestCheckChainTermination:
    def test_empty_goal_returns_fail(self, tmp_path: Path) -> None:
        from wos.chain import check_chain_termination

        manifest = {
            "path": str(tmp_path / "my.chain.md"),
            "goal": "",
            "steps": [],
        }

        issues = check_chain_termination(manifest)

        assert len(issues) == 1
        assert issues[0]["severity"] == "fail"

    def test_missing_goal_key_returns_fail(self, tmp_path: Path) -> None:
        from wos.chain import check_chain_termination

        manifest = {
            "path": str(tmp_path / "my.chain.md"),
            "steps": [],
        }

        issues = check_chain_termination(manifest)

        assert len(issues) == 1
        assert issues[0]["severity"] == "fail"

    def test_nonempty_goal_no_issues(self, tmp_path: Path) -> None:
        from wos.chain import check_chain_termination

        manifest = {
            "path": str(tmp_path / "my.chain.md"),
            "goal": "All wiki pages updated and indexed",
            "steps": [],
        }

        issues = check_chain_termination(manifest)

        assert issues == []


# ── TestCheckChainCycles ──────────────────────────────────────────────


class TestCheckChainCycles:
    def test_step_numbers_out_of_order_returns_fail(self, tmp_path: Path) -> None:
        from wos.chain import check_chain_cycles

        manifest = {
            "path": str(tmp_path / "my.chain.md"),
            "steps": [
                {"step": "1", "skill": "research", "input_contract": "q",
                 "output_contract": "r", "gate": ""},
                {"step": "3", "skill": "distill", "input_contract": "r",
                 "output_contract": "c", "gate": ""},
                {"step": "2", "skill": "ingest", "input_contract": "c",
                 "output_contract": "pages", "gate": ""},
            ],
        }

        issues = check_chain_cycles(manifest)

        assert any(i["severity"] == "fail" and "strictly increasing" in i["issue"]
                   for i in issues)

    def test_same_skill_consecutive_steps_returns_fail(self, tmp_path: Path) -> None:
        from wos.chain import check_chain_cycles

        manifest = {
            "path": str(tmp_path / "my.chain.md"),
            "steps": [
                {"step": "1", "skill": "research", "input_contract": "q",
                 "output_contract": "r", "gate": ""},
                {"step": "2", "skill": "research", "input_contract": "r",
                 "output_contract": "r2", "gate": ""},
            ],
        }

        issues = check_chain_cycles(manifest)

        assert any(i["severity"] == "fail" and "direct loop" in i["issue"]
                   for i in issues)

    def test_valid_step_sequence_no_issues(self, tmp_path: Path) -> None:
        from wos.chain import check_chain_cycles

        manifest = {
            "path": str(tmp_path / "my.chain.md"),
            "steps": [
                {"step": "1", "skill": "research", "input_contract": "q",
                 "output_contract": "r", "gate": ""},
                {"step": "2", "skill": "distill", "input_contract": "r",
                 "output_contract": "c", "gate": "approval"},
                {"step": "3", "skill": "ingest", "input_contract": "c",
                 "output_contract": "pages updated", "gate": "lint passes"},
            ],
        }

        issues = check_chain_cycles(manifest)

        assert issues == []


# ── TestValidateChain ─────────────────────────────────────────────────


class TestValidateChain:
    def test_clean_manifest_with_skills_no_failures(self, tmp_path: Path) -> None:
        from wos.validators import validate_chain

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
        from wos.validators import validate_chain

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
        from wos.validators import validate_chain

        # Missing frontmatter — will fail to parse
        manifest_path = tmp_path / "bad.chain.md"
        manifest_path.write_text("No frontmatter here.\n", encoding="utf-8")

        issues = validate_chain(manifest_path, [])

        assert len(issues) == 1
        assert issues[0]["severity"] == "warn"
        assert "Invalid chain manifest" in issues[0]["issue"]
