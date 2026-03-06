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

    def test_unclosed_frontmatter_unchanged(self) -> None:
        from wos.skill_audit import strip_frontmatter

        text = "---\nname: Test\n# Content\n"
        assert strip_frontmatter(text) == text
