"""Tests for replace_marker_section — shared marker replacement utility."""

from __future__ import annotations


class TestReplaceMarkerSection:
    def test_replaces_between_existing_markers(self) -> None:
        from wiki.agents_md import replace_marker_section

        content = (
            "Before.\n\n"
            "<!-- begin -->\nold stuff\n<!-- end -->\n\n"
            "After.\n"
        )
        result = replace_marker_section(
            content, "<!-- begin -->", "<!-- end -->", "new stuff\n"
        )
        assert "old stuff" not in result
        assert "new stuff" in result
        assert "Before." in result
        assert "After." in result

    def test_appends_when_no_markers(self) -> None:
        from wiki.agents_md import replace_marker_section

        content = "# Header\n\nExisting content.\n"
        result = replace_marker_section(
            content, "<!-- begin -->", "<!-- end -->", "new section\n"
        )
        assert "# Header" in result
        assert "Existing content." in result
        assert "new section" in result

    def test_consumes_trailing_newline_after_end_marker(self) -> None:
        from wiki.agents_md import replace_marker_section

        content = "Before.\n<!-- begin -->\nold\n<!-- end -->\nAfter.\n"
        result = replace_marker_section(
            content, "<!-- begin -->", "<!-- end -->", "new\n"
        )
        # Should not produce double newlines where marker was
        assert "new\nAfter." in result

    def test_handles_empty_content(self) -> None:
        from wiki.agents_md import replace_marker_section

        result = replace_marker_section(
            "", "<!-- begin -->", "<!-- end -->", "section\n"
        )
        assert "section" in result
