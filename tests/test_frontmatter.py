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


class TestNestedDicts:
    def test_metadata_with_scalar_values(self) -> None:
        text = (
            "---\n"
            "name: Test\n"
            "description: A test\n"
            "metadata:\n"
            "  type: plan\n"
            "  status: draft\n"
            "---\n"
        )
        fm, _ = parse_frontmatter(text)
        assert fm["name"] == "Test"
        assert fm["metadata"] == {"type": "plan", "status": "draft"}

    def test_metadata_with_list_values(self) -> None:
        text = (
            "---\n"
            "name: Test\n"
            "description: A test\n"
            "metadata:\n"
            "  sources:\n"
            "    - https://a.com\n"
            "    - https://b.com\n"
            "---\n"
        )
        fm, _ = parse_frontmatter(text)
        assert fm["metadata"] == {"sources": ["https://a.com", "https://b.com"]}

    def test_metadata_with_mixed_scalars_and_lists(self) -> None:
        text = (
            "---\n"
            "name: Test\n"
            "description: A test\n"
            "metadata:\n"
            "  type: research\n"
            "  sources:\n"
            "    - https://a.com\n"
            "    - https://b.com\n"
            "  related:\n"
            "    - docs/context/foo.md\n"
            "---\n"
        )
        fm, _ = parse_frontmatter(text)
        assert fm["metadata"] == {
            "type": "research",
            "sources": ["https://a.com", "https://b.com"],
            "related": ["docs/context/foo.md"],
        }

    def test_metadata_with_null_values(self) -> None:
        text = (
            "---\n"
            "name: Test\n"
            "description: A test\n"
            "metadata:\n"
            "  type: plan\n"
            "  optional_field:\n"
            "---\n"
        )
        fm, _ = parse_frontmatter(text)
        assert fm["metadata"] == {"type": "plan", "optional_field": None}

    def test_non_metadata_nested_key(self) -> None:
        """Nesting works for any key, not just 'metadata'."""
        text = (
            "---\n"
            "name: Test\n"
            "description: A test\n"
            "config:\n"
            "  setting: value\n"
            "  debug: true\n"
            "---\n"
        )
        fm, _ = parse_frontmatter(text)
        assert fm["config"] == {"setting": "value", "debug": "true"}

    def test_nested_dict_followed_by_top_level_key(self) -> None:
        text = (
            "---\n"
            "name: Test\n"
            "metadata:\n"
            "  type: plan\n"
            "description: A test\n"
            "---\n"
        )
        fm, _ = parse_frontmatter(text)
        assert fm["metadata"] == {"type": "plan"}
        assert fm["description"] == "A test"

    def test_null_key_without_nested_content_stays_none(self) -> None:
        """A null-valued key followed by another top-level key stays None."""
        text = (
            "---\n"
            "metadata:\n"
            "name: Test\n"
            "description: A test\n"
            "---\n"
        )
        fm, _ = parse_frontmatter(text)
        assert fm["metadata"] is None
        assert fm["name"] == "Test"

    def test_nested_dict_at_end_of_frontmatter(self) -> None:
        text = (
            "---\n"
            "name: Test\n"
            "description: A test\n"
            "metadata:\n"
            "  type: context\n"
            "---\n"
            "Body content.\n"
        )
        fm, body = parse_frontmatter(text)
        assert fm["metadata"] == {"type": "context"}
        assert body == "Body content.\n"

    def test_metadata_with_colon_in_value(self) -> None:
        text = (
            "---\n"
            "name: Test\n"
            "description: A test\n"
            "metadata:\n"
            "  source_url: https://example.com/path\n"
            "---\n"
        )
        fm, _ = parse_frontmatter(text)
        assert fm["metadata"] == {"source_url": "https://example.com/path"}
