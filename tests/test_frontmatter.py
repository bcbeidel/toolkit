"""Tests for wos/frontmatter.py — custom YAML frontmatter parser."""

from __future__ import annotations

import pytest

from wos.frontmatter import parse_frontmatter


class TestDelimiters:
    def test_valid_frontmatter_returns_dict_and_body(self) -> None:
        text = "---\nname: Test\ndescription: A test\n---\nBody content.\n"
        fm, body = parse_frontmatter(text)
        assert fm == {"name": "Test", "description": "A test"}
        assert body == "Body content.\n"

    def test_no_opening_delimiter_raises(self) -> None:
        with pytest.raises(ValueError, match="frontmatter"):
            parse_frontmatter("name: Test\n---\n")

    def test_no_closing_delimiter_raises(self) -> None:
        with pytest.raises(ValueError, match="closing"):
            parse_frontmatter("---\nname: Test\n")

    def test_empty_frontmatter_returns_empty_dict(self) -> None:
        fm, body = parse_frontmatter("---\n---\nBody.\n")
        assert fm == {}
        assert body == "Body.\n"

    def test_frontmatter_at_end_of_file_no_body(self) -> None:
        fm, body = parse_frontmatter("---\nname: Test\n---")
        assert fm == {"name": "Test"}
        assert body == ""

    def test_frontmatter_with_trailing_newline_only(self) -> None:
        fm, body = parse_frontmatter("---\nname: Test\n---\n")
        assert fm == {"name": "Test"}
        assert body == ""


class TestScalarValues:
    def test_key_value_pair(self) -> None:
        fm, _ = parse_frontmatter("---\nname: Hello World\n---\n")
        assert fm["name"] == "Hello World"

    def test_key_with_no_value_is_none(self) -> None:
        fm, _ = parse_frontmatter("---\nname: Test\ntype:\n---\n")
        assert fm["type"] is None

    def test_no_type_coercion_numbers_stay_strings(self) -> None:
        fm, _ = parse_frontmatter("---\nname: 42\ndescription: 100\n---\n")
        assert fm["name"] == "42"
        assert fm["description"] == "100"

    def test_no_type_coercion_booleans_stay_strings(self) -> None:
        fm, _ = parse_frontmatter("---\nname: true\ndescription: false\n---\n")
        assert fm["name"] == "true"
        assert fm["description"] == "false"

    def test_value_with_colon_in_it(self) -> None:
        fm, _ = parse_frontmatter("---\nname: http://example.com\n---\n")
        assert fm["name"] == "http://example.com"

    def test_value_with_leading_trailing_spaces_stripped(self) -> None:
        fm, _ = parse_frontmatter("---\nname:   Hello   \n---\n")
        assert fm["name"] == "Hello"


class TestListValues:
    def test_simple_list(self) -> None:
        text = "---\nsources:\n  - https://a.com\n  - https://b.com\n---\n"
        fm, _ = parse_frontmatter(text)
        assert fm["sources"] == ["https://a.com", "https://b.com"]

    def test_list_items_without_indent(self) -> None:
        text = "---\nsources:\n- https://a.com\n- https://b.com\n---\n"
        fm, _ = parse_frontmatter(text)
        assert fm["sources"] == ["https://a.com", "https://b.com"]

    def test_list_item_values_stripped(self) -> None:
        text = "---\nsources:\n  -   https://a.com  \n---\n"
        fm, _ = parse_frontmatter(text)
        assert fm["sources"] == ["https://a.com"]

    def test_key_with_no_value_followed_by_list(self) -> None:
        text = "---\nrelated:\n  - file1.md\n  - file2.md\n---\n"
        fm, _ = parse_frontmatter(text)
        assert fm["related"] == ["file1.md", "file2.md"]

    def test_key_with_null_and_no_list_stays_none(self) -> None:
        text = "---\nsources:\nname: Test\n---\n"
        fm, _ = parse_frontmatter(text)
        assert fm["sources"] is None
        assert fm["name"] == "Test"


class TestEdgeCases:
    def test_blank_lines_in_frontmatter_ignored(self) -> None:
        text = "---\nname: Test\n\ndescription: Desc\n---\n"
        fm, _ = parse_frontmatter(text)
        assert fm["name"] == "Test"
        assert fm["description"] == "Desc"

    def test_comment_lines_ignored(self) -> None:
        text = "---\n# This is a comment\nname: Test\n---\n"
        fm, _ = parse_frontmatter(text)
        assert fm["name"] == "Test"
        assert "#" not in fm

    def test_body_content_preserved_exactly(self) -> None:
        text = "---\nname: Test\n---\n# Heading\n\nParagraph.\n"
        _, body = parse_frontmatter(text)
        assert body == "# Heading\n\nParagraph.\n"

    def test_body_with_dashes_not_confused_for_delimiter(self) -> None:
        text = "---\nname: Test\n---\n# Heading\n\n---\n\nMore content.\n"
        _, body = parse_frontmatter(text)
        assert "---" in body
        assert "More content." in body

    def test_quoted_values_preserve_quotes(self) -> None:
        text = '---\nname: "Quoted Value"\n---\n'
        fm, _ = parse_frontmatter(text)
        # Quotes are part of the string (no YAML quoting semantics)
        assert fm["name"] == '"Quoted Value"'

    def test_inline_empty_list_returns_list(self) -> None:
        # related: [] should parse as an empty list, not the string "[]"
        text = "---\nname: Test\nrelated: []\n---\n"
        fm, _ = parse_frontmatter(text)
        assert fm["related"] == []

    def test_inline_empty_sources_returns_list(self) -> None:
        text = "---\nname: Test\nsources: []\n---\n"
        fm, _ = parse_frontmatter(text)
        assert fm["sources"] == []
