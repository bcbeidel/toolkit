"""Tests for wos/skill_audit.py — skill size auditing."""

from __future__ import annotations

from pathlib import Path


class TestStripFrontmatter:
    def test_removes_yaml_frontmatter(self) -> None:
        from wos.skill_audit import strip_frontmatter

        text = "---\nname: Test\ndescription: A test\n---\n# Content\n"
        result = strip_frontmatter(text)
        assert result.startswith("# Content")

    def test_no_frontmatter_unchanged(self) -> None:
        from wos.skill_audit import strip_frontmatter

        text = "# Content\n\nSome text.\n"
        assert strip_frontmatter(text) == text

    def test_dashes_inside_yaml_value_not_matched(self) -> None:
        from wos.skill_audit import strip_frontmatter

        text = "---\nname: foo---bar\n---\n# Content\n"
        result = strip_frontmatter(text)
        assert result.startswith("# Content")

    def test_unclosed_frontmatter_unchanged(self) -> None:
        from wos.skill_audit import strip_frontmatter

        text = "---\nname: Test\n# Content\n"
        assert strip_frontmatter(text) == text


class TestCountInstructionLines:
    def test_counts_bullet_points(self) -> None:
        from wos.skill_audit import count_instruction_lines

        text = "- bullet one\n- bullet two\n- bullet three\n"
        assert count_instruction_lines(text) == 3

    def test_excludes_blank_lines(self) -> None:
        from wos.skill_audit import count_instruction_lines

        text = "- bullet one\n\n- bullet two\n"
        assert count_instruction_lines(text) == 2

    def test_excludes_headers(self) -> None:
        from wos.skill_audit import count_instruction_lines

        text = "# Header\n## Subheader\n- bullet\n"
        assert count_instruction_lines(text) == 1

    def test_excludes_code_fences(self) -> None:
        from wos.skill_audit import count_instruction_lines

        text = "```python\nprint('hello')\n```\n"
        assert count_instruction_lines(text) == 1

    def test_excludes_table_separators(self) -> None:
        from wos.skill_audit import count_instruction_lines

        text = "| Name | Value |\n|------|-------|\n| foo  | bar   |\n"
        assert count_instruction_lines(text) == 2

    def test_excludes_horizontal_rules(self) -> None:
        from wos.skill_audit import count_instruction_lines

        text = "- bullet one\n---\n- bullet two\n***\n- bullet three\n"
        assert count_instruction_lines(text) == 3

    def test_counts_prose(self) -> None:
        from wos.skill_audit import count_instruction_lines

        text = "This is a sentence.\nThis is another sentence.\n"
        assert count_instruction_lines(text) == 2

    def test_counts_numbered_steps(self) -> None:
        from wos.skill_audit import count_instruction_lines

        text = "1. Step one\n2. Step two\n3. Step three\n"
        assert count_instruction_lines(text) == 3

    def test_counts_table_data_rows(self) -> None:
        from wos.skill_audit import count_instruction_lines

        text = (
            "| Name | Value |\n|------|-------|\n"
            "| foo  | bar   |\n| baz  | qux   |\n"
        )
        assert count_instruction_lines(text) == 3

    def test_empty_text(self) -> None:
        from wos.skill_audit import count_instruction_lines

        assert count_instruction_lines("") == 0


def _create_skill(tmp_path: Path, name: str, skill_content: str,
                  ref_contents: dict[str, str] | None = None) -> None:
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

        _create_skill(tmp_path, "small-skill", "# Small\n\n- Do something\n")
        summaries, issues = check_skill_sizes(tmp_path)
        assert len(summaries) == 1
        assert len(issues) == 0

    def test_skill_over_threshold_warns(self, tmp_path: Path) -> None:
        from wos.skill_audit import check_skill_sizes

        lines = "\n".join(f"- instruction {i}" for i in range(250))
        _create_skill(tmp_path, "big-skill", f"# Big\n\n{lines}\n")
        summaries, issues = check_skill_sizes(tmp_path, max_lines=200)
        assert len(summaries) == 1
        assert len(issues) == 1
        assert issues[0]["severity"] == "warn"

    def test_shared_excluded(self, tmp_path: Path) -> None:
        from wos.skill_audit import check_skill_sizes

        _create_skill(tmp_path, "_shared", "# Shared\n\n- helper\n")
        summaries, issues = check_skill_sizes(tmp_path)
        assert len(summaries) == 0

    def test_no_skills_dir(self, tmp_path: Path) -> None:
        from wos.skill_audit import check_skill_sizes

        nonexistent = tmp_path / "nonexistent"
        summaries, issues = check_skill_sizes(nonexistent)
        assert summaries == []
        assert issues == []

    def test_configurable_threshold(self, tmp_path: Path) -> None:
        from wos.skill_audit import check_skill_sizes

        lines = "\n".join(f"- instruction {i}" for i in range(50))
        _create_skill(tmp_path, "medium-skill", f"# Medium\n\n{lines}\n")
        _, issues_high = check_skill_sizes(tmp_path, max_lines=200)
        _, issues_low = check_skill_sizes(tmp_path, max_lines=10)
        assert len(issues_high) == 0
        assert len(issues_low) == 1

    def test_zero_threshold_disables_warnings(self, tmp_path: Path) -> None:
        from wos.skill_audit import check_skill_sizes

        lines = "\n".join(f"- instruction {i}" for i in range(300))
        _create_skill(tmp_path, "huge-skill", f"# Huge\n\n{lines}\n")
        summaries, issues = check_skill_sizes(tmp_path, max_lines=0)
        assert len(summaries) == 1
        assert len(issues) == 0

    def test_includes_reference_files(self, tmp_path: Path) -> None:
        from wos.skill_audit import check_skill_sizes

        _create_skill(
            tmp_path, "ref-skill", "# Ref Skill\n\n- main instruction\n",
            ref_contents={"guide.md": "- ref instruction one\n- ref instruction two\n"},
        )
        summaries, issues = check_skill_sizes(tmp_path)
        assert len(summaries) == 1
        assert summaries[0]["ref_lines"] > 0

    def test_summary_has_expected_fields(self, tmp_path: Path) -> None:
        from wos.skill_audit import check_skill_sizes

        _create_skill(tmp_path, "field-skill", "# Fields\n\n- one\n")
        summaries, _ = check_skill_sizes(tmp_path)
        assert len(summaries) == 1
        summary = summaries[0]
        expected_keys = {
            "name", "skill_lines", "ref_lines",
            "total_lines", "words", "files",
        }
        assert set(summary.keys()) == expected_keys
