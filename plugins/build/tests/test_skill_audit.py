"""Tests for wos/skill.py — skill size auditing."""

from __future__ import annotations

from pathlib import Path


class TestStripFrontmatter:
    def test_removes_yaml_frontmatter(self) -> None:
        from check.skill import strip_frontmatter

        text = "---\nname: Test\ndescription: A test\n---\n# Content\n"
        result = strip_frontmatter(text)
        assert result.startswith("# Content")

    def test_no_frontmatter_unchanged(self) -> None:
        from check.skill import strip_frontmatter

        text = "# Content\n\nSome text.\n"
        assert strip_frontmatter(text) == text

    def test_dashes_inside_yaml_value_not_matched(self) -> None:
        from check.skill import strip_frontmatter

        text = "---\nname: foo---bar\n---\n# Content\n"
        result = strip_frontmatter(text)
        assert result.startswith("# Content")

    def test_unclosed_frontmatter_unchanged(self) -> None:
        from check.skill import strip_frontmatter

        text = "---\nname: Test\n# Content\n"
        assert strip_frontmatter(text) == text


class TestCountInstructionLines:
    def test_counts_bullet_points(self) -> None:
        from check.skill import count_instruction_lines

        text = "- bullet one\n- bullet two\n- bullet three\n"
        assert count_instruction_lines(text) == 3

    def test_excludes_blank_lines(self) -> None:
        from check.skill import count_instruction_lines

        text = "- bullet one\n\n- bullet two\n"
        assert count_instruction_lines(text) == 2

    def test_excludes_headers(self) -> None:
        from check.skill import count_instruction_lines

        text = "# Header\n## Subheader\n- bullet\n"
        assert count_instruction_lines(text) == 1

    def test_excludes_code_fences(self) -> None:
        from check.skill import count_instruction_lines

        text = "```python\nprint('hello')\n```\n"
        assert count_instruction_lines(text) == 1

    def test_excludes_table_separators(self) -> None:
        from check.skill import count_instruction_lines

        text = "| Name | Value |\n|------|-------|\n| foo  | bar   |\n"
        assert count_instruction_lines(text) == 2

    def test_excludes_horizontal_rules(self) -> None:
        from check.skill import count_instruction_lines

        text = "- bullet one\n---\n- bullet two\n***\n- bullet three\n"
        assert count_instruction_lines(text) == 3

    def test_counts_prose(self) -> None:
        from check.skill import count_instruction_lines

        text = "This is a sentence.\nThis is another sentence.\n"
        assert count_instruction_lines(text) == 2

    def test_counts_numbered_steps(self) -> None:
        from check.skill import count_instruction_lines

        text = "1. Step one\n2. Step two\n3. Step three\n"
        assert count_instruction_lines(text) == 3

    def test_counts_table_data_rows(self) -> None:
        from check.skill import count_instruction_lines

        text = (
            "| Name | Value |\n|------|-------|\n"
            "| foo  | bar   |\n| baz  | qux   |\n"
        )
        assert count_instruction_lines(text) == 3

    def test_empty_text(self) -> None:
        from check.skill import count_instruction_lines

        assert count_instruction_lines("") == 0


def _create_skill(tmp_path: Path, name: str, skill_content: str,
                  ref_contents: dict[str, str] | None = None) -> None:
    skill_dir = tmp_path / name
    skill_dir.mkdir()
    # Prepend minimal frontmatter if content lacks it (required for SkillDocument.parse)
    if not skill_content.startswith("---"):
        skill_content = (
            f"---\nname: {name}\ndescription: A test skill.\n---\n{skill_content}"
        )
    (skill_dir / "SKILL.md").write_text(skill_content, encoding="utf-8")
    if ref_contents:
        refs_dir = skill_dir / "references"
        refs_dir.mkdir()
        for filename, content in ref_contents.items():
            (refs_dir / filename).write_text(content, encoding="utf-8")


class TestCheckSkillSizes:
    def test_skill_under_threshold_no_issues(self, tmp_path: Path) -> None:
        from check.skill import check_skill_sizes

        _create_skill(tmp_path, "small-skill", "# Small\n\n- Do something\n")
        summaries, issues = check_skill_sizes(tmp_path)
        assert len(summaries) == 1
        assert len(issues) == 0

    def test_skill_over_threshold_warns(self, tmp_path: Path) -> None:
        from check.skill import check_skill_sizes

        lines = "\n".join(f"- instruction {i}" for i in range(250))
        _create_skill(tmp_path, "big-skill", f"# Big\n\n{lines}\n")
        summaries, issues = check_skill_sizes(tmp_path, max_lines=200)
        assert len(summaries) == 1
        assert len(issues) == 1
        assert issues[0]["severity"] == "warn"

    def test_shared_excluded(self, tmp_path: Path) -> None:
        from check.skill import check_skill_sizes

        _create_skill(tmp_path, "_shared", "# Shared\n\n- helper\n")
        summaries, issues = check_skill_sizes(tmp_path)
        assert len(summaries) == 0

    def test_no_skills_dir(self, tmp_path: Path) -> None:
        from check.skill import check_skill_sizes

        nonexistent = tmp_path / "nonexistent"
        summaries, issues = check_skill_sizes(nonexistent)
        assert summaries == []
        assert issues == []

    def test_configurable_threshold(self, tmp_path: Path) -> None:
        from check.skill import check_skill_sizes

        lines = "\n".join(f"- instruction {i}" for i in range(50))
        _create_skill(tmp_path, "medium-skill", f"# Medium\n\n{lines}\n")
        _, issues_high = check_skill_sizes(tmp_path, max_lines=200)
        _, issues_low = check_skill_sizes(tmp_path, max_lines=10)
        assert len(issues_high) == 0
        assert len(issues_low) == 1

    def test_zero_threshold_disables_warnings(self, tmp_path: Path) -> None:
        from check.skill import check_skill_sizes

        lines = "\n".join(f"- instruction {i}" for i in range(300))
        _create_skill(tmp_path, "huge-skill", f"# Huge\n\n{lines}\n")
        summaries, issues = check_skill_sizes(tmp_path, max_lines=0)
        assert len(summaries) == 1
        assert len(issues) == 0

    def test_includes_reference_files(self, tmp_path: Path) -> None:
        from check.skill import check_skill_sizes

        _create_skill(
            tmp_path, "ref-skill", "# Ref Skill\n\n- main instruction\n",
            ref_contents={"guide.md": "- ref instruction one\n- ref instruction two\n"},
        )
        summaries, issues = check_skill_sizes(tmp_path)
        assert len(summaries) == 1
        assert summaries[0]["ref_lines"] > 0

    def test_summary_has_expected_fields(self, tmp_path: Path) -> None:
        from check.skill import check_skill_sizes

        _create_skill(tmp_path, "field-skill", "# Fields\n\n- one\n")
        summaries, _ = check_skill_sizes(tmp_path)
        assert len(summaries) == 1
        summary = summaries[0]
        expected_keys = {
            "name", "skill_lines", "ref_lines",
            "total_lines", "words", "files",
        }
        assert set(summary.keys()) == expected_keys


class TestParseSkillMeta:
    def test_extracts_name_and_description(self, tmp_path: Path) -> None:
        from check.skill import SkillDocument

        skill_dir = tmp_path / "my-skill"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text(
            "---\nname: my-skill\ndescription: Does something useful\n---\n# Body\n"
        )
        skill = SkillDocument.parse(skill_dir)
        assert skill.name == "my-skill"
        assert skill.description == "Does something useful"

    def test_multiline_description_with_fold(self, tmp_path: Path) -> None:
        from check.skill import SkillDocument

        skill_dir = tmp_path / "my-skill"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text(
            "---\n"
            "name: my-skill\n"
            "description: >\n"
            "  First line of description\n"
            "  second line of description.\n"
            "argument-hint: something\n"
            "---\n"
            "# Body\n"
        )
        skill = SkillDocument.parse(skill_dir)
        assert skill.name == "my-skill"
        assert "First line" in skill.description
        assert "second line" in skill.description

    def test_missing_name_returns_none(self, tmp_path: Path) -> None:
        from check.skill import SkillDocument

        skill_dir = tmp_path / "my-skill"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text(
            "---\ndescription: Does something\n---\n# Body\n"
        )
        skill = SkillDocument.parse(skill_dir)
        assert skill is None

    def test_missing_description_returns_none(self, tmp_path: Path) -> None:
        from check.skill import SkillDocument

        skill_dir = tmp_path / "my-skill"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text(
            "---\nname: my-skill\n---\n# Body\n"
        )
        skill = SkillDocument.parse(skill_dir)
        assert skill is None

    def test_no_frontmatter_returns_none(self, tmp_path: Path) -> None:
        from check.skill import SkillDocument

        skill_dir = tmp_path / "my-skill"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text("# Just a body\n")
        skill = SkillDocument.parse(skill_dir)
        assert skill is None


class TestCheckSkillMeta:
    def test_valid_skill_no_issues(self, tmp_path: Path) -> None:
        from check.skill import check_skill_meta
        _create_skill(
            tmp_path, "good-skill",
            "---\nname: good-skill\n"
            "description: Performs good actions. Use when asked.\n"
            "---\n# Good Skill\n\n- Do good\n",
        )
        issues = check_skill_meta(tmp_path / "good-skill")
        assert len(issues) == 0

    def test_name_uppercase_fails(self, tmp_path: Path) -> None:
        from check.skill import check_skill_meta
        _create_skill(
            tmp_path, "BadName",
            "---\nname: BadName\ndescription: Valid description here.\n---\n# X\n",
        )
        issues = check_skill_meta(tmp_path / "BadName")
        assert any("lowercase" in i["issue"] for i in issues)
        assert any(i["severity"] == "fail" for i in issues)

    def test_name_too_long_fails(self, tmp_path: Path) -> None:
        from check.skill import check_skill_meta
        long_name = "a" * 65
        _create_skill(
            tmp_path, long_name,
            f"---\nname: {long_name}\ndescription: Valid.\n---\n# X\n",
        )
        issues = check_skill_meta(tmp_path / long_name)
        assert any("64 characters" in i["issue"] for i in issues)

    def test_name_reserved_word_fails(self, tmp_path: Path) -> None:
        from check.skill import check_skill_meta
        _create_skill(
            tmp_path, "claude-helper",
            "---\nname: claude-helper\ndescription: Valid.\n---\n# X\n",
        )
        issues = check_skill_meta(tmp_path / "claude-helper")
        assert any("reserved" in i["issue"] for i in issues)

    def test_description_too_long_warns(self, tmp_path: Path) -> None:
        from check.skill import check_skill_meta
        long_desc = "x " * 600
        _create_skill(
            tmp_path, "verbose",
            f"---\nname: verbose\ndescription: {long_desc}\n---\n# X\n",
        )
        issues = check_skill_meta(tmp_path / "verbose")
        assert any("1024" in i["issue"] for i in issues)
        assert any(i["severity"] == "warn" for i in issues)

    def test_description_xml_tags_warns(self, tmp_path: Path) -> None:
        from check.skill import check_skill_meta
        _create_skill(
            tmp_path, "xml-desc",
            "---\nname: xml-desc\ndescription: Use <b>bold</b> text.\n---\n# X\n",
        )
        issues = check_skill_meta(tmp_path / "xml-desc")
        assert any("XML" in i["issue"] for i in issues)

    def test_description_second_person_warns(self, tmp_path: Path) -> None:
        from check.skill import check_skill_meta
        _create_skill(
            tmp_path, "voice",
            "---\nname: voice\n"
            "description: You can use this to process files.\n"
            "---\n# X\n",
        )
        issues = check_skill_meta(tmp_path / "voice")
        assert any("third person" in i["issue"].lower() for i in issues)

    def test_raw_line_count_over_500_warns(self, tmp_path: Path) -> None:
        from check.skill import check_skill_meta
        lines = "\n".join(f"line {i}" for i in range(510))
        _create_skill(
            tmp_path, "long-skill",
            f"---\nname: long-skill\ndescription: Valid skill.\n---\n{lines}\n",
        )
        issues = check_skill_meta(tmp_path / "long-skill")
        assert any("500" in i["issue"] for i in issues)

    def test_rigid_directives_under_threshold_no_warn(self, tmp_path: Path) -> None:
        from check.skill import check_skill_meta
        _create_skill(
            tmp_path, "mild-skill",
            "---\nname: mild-skill\ndescription: Valid skill.\n---\n"
            "# Mild\n\nMUST do X.\nNEVER do Y.\n",
        )
        issues = check_skill_meta(tmp_path / "mild-skill")
        assert not any("directives" in i["issue"] for i in issues)

    def test_rigid_directives_at_threshold_warns(self, tmp_path: Path) -> None:
        from check.skill import check_skill_meta
        _create_skill(
            tmp_path, "rigid-skill",
            "---\nname: rigid-skill\ndescription: Valid skill.\n---\n"
            "# Rigid\n\nMUST do X.\nNEVER do Y.\nALWAYS do Z.\n",
        )
        issues = check_skill_meta(tmp_path / "rigid-skill")
        directive_issues = [i for i in issues if "directives" in i["issue"]]
        assert len(directive_issues) == 1
        assert directive_issues[0]["severity"] == "warn"

    def test_rigid_directives_ignores_lowercase(self, tmp_path: Path) -> None:
        from check.skill import check_skill_meta
        _create_skill(
            tmp_path, "lowercase-skill",
            "---\nname: lowercase-skill\ndescription: Valid skill.\n---\n"
            "# Lowercase\n\nYou must do X.\nNever do Y.\nAlways do Z.\n"
            "This is required.\nThis is forbidden.\n",
        )
        issues = check_skill_meta(tmp_path / "lowercase-skill")
        assert not any("directives" in i["issue"] for i in issues)

    def test_no_skill_md_returns_empty(self, tmp_path: Path) -> None:
        from check.skill import check_skill_meta
        (tmp_path / "empty-dir").mkdir()
        issues = check_skill_meta(tmp_path / "empty-dir")
        assert issues == []
