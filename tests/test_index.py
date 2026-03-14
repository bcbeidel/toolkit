"""Tests for wos/index.py — index generator and sync checker."""

from __future__ import annotations

from pathlib import Path

# ── generate_index ─────────────────────────────────────────────


class TestGenerateIndex:
    def test_file_table_with_descriptions_from_frontmatter(
        self, tmp_path: Path
    ) -> None:
        """Files with frontmatter descriptions appear in the file table."""
        from wos.index import generate_index

        (tmp_path / "alpha.md").write_text(
            "---\nname: Alpha\ndescription: First doc\n---\n# Alpha\n"
        )
        (tmp_path / "beta.md").write_text(
            "---\nname: Beta\ndescription: Second doc\n---\n# Beta\n"
        )

        result = generate_index(tmp_path)

        assert "| File | Description |" in result
        assert "[alpha.md](alpha.md)" in result
        assert "First doc" in result
        assert "[beta.md](beta.md)" in result
        assert "Second doc" in result

    def test_subdirectory_table(self, tmp_path: Path) -> None:
        """Subdirectories appear in a separate directory table."""
        from wos.index import generate_index

        sub = tmp_path / "child-dir"
        sub.mkdir()
        (sub / "_index.md").write_text(
            "---\nname: Child Dir\ndescription: A child directory\n---\n"
        )
        # Also add a file so file table is present
        (tmp_path / "doc.md").write_text(
            "---\nname: Doc\ndescription: A document\n---\n# Doc\n"
        )

        result = generate_index(tmp_path)

        assert "| Directory | Description |" in result
        assert "[child-dir/](child-dir/)" in result
        assert "A child directory" in result

    def test_excludes_index_md_from_file_listing(self, tmp_path: Path) -> None:
        """_index.md itself should not appear in the file table."""
        from wos.index import generate_index

        (tmp_path / "_index.md").write_text(
            "---\nname: Old Index\ndescription: Should be excluded\n---\n"
        )
        (tmp_path / "topic.md").write_text(
            "---\nname: Topic\ndescription: A topic\n---\n# Topic\n"
        )

        result = generate_index(tmp_path)

        assert "_index.md" not in result
        assert "[topic.md](topic.md)" in result

    def test_sorted_alphabetically(self, tmp_path: Path) -> None:
        """Files and directories are listed in alphabetical order."""
        from wos.index import generate_index

        (tmp_path / "zebra.md").write_text(
            "---\nname: Zebra\ndescription: Last\n---\n"
        )
        (tmp_path / "apple.md").write_text(
            "---\nname: Apple\ndescription: First\n---\n"
        )
        (tmp_path / "mango.md").write_text(
            "---\nname: Mango\ndescription: Middle\n---\n"
        )

        result = generate_index(tmp_path)
        lines = result.splitlines()

        # Find the rows with file links
        file_rows = [
            line for line in lines if line.startswith("| [") and ".md]" in line
        ]
        assert len(file_rows) == 3
        # apple before mango before zebra
        assert file_rows[0].startswith("| [apple.md]")
        assert file_rows[1].startswith("| [mango.md]")
        assert file_rows[2].startswith("| [zebra.md]")

    def test_heading_uses_directory_name_title_case(self, tmp_path: Path) -> None:
        """Heading replaces hyphens/underscores with spaces and uses title case."""
        from wos.index import generate_index

        d = tmp_path / "my-cool_topic"
        d.mkdir()
        (d / "doc.md").write_text(
            "---\nname: Doc\ndescription: A doc\n---\n"
        )

        result = generate_index(d)

        assert result.startswith("# My Cool Topic\n")

    def test_empty_directory(self, tmp_path: Path) -> None:
        """Empty directory produces heading only, no tables."""
        from wos.index import generate_index

        d = tmp_path / "empty-area"
        d.mkdir()

        result = generate_index(d)

        assert "# Empty Area" in result
        assert "| File |" not in result
        assert "| Directory |" not in result

    def test_file_without_frontmatter_shows_no_description(
        self, tmp_path: Path
    ) -> None:
        """Files without valid frontmatter show '*(no description)*'."""
        from wos.index import generate_index

        (tmp_path / "plain.md").write_text("# Just a heading\n\nNo frontmatter.\n")

        result = generate_index(tmp_path)

        assert "[plain.md](plain.md)" in result
        assert "*(no description)*" in result

    def test_nested_index_generation(self, tmp_path: Path) -> None:
        """Index generation works for nested directories."""
        from wos.index import generate_index

        parent = tmp_path / "context"
        parent.mkdir()
        child = parent / "testing"
        child.mkdir()
        (child / "unit-tests.md").write_text(
            "---\nname: Unit Tests\ndescription: How to unit test\n---\n"
        )

        result = generate_index(child)

        assert "# Testing" in result
        assert "[unit-tests.md](unit-tests.md)" in result
        assert "How to unit test" in result

    def test_subdirectory_without_index_uses_display_name(
        self, tmp_path: Path
    ) -> None:
        """Subdirectories without _index.md use their display name as description."""
        from wos.index import generate_index

        sub = tmp_path / "some-module"
        sub.mkdir()
        # No _index.md in subdirectory

        # Need at least one file or subdir to get a table
        result = generate_index(tmp_path)

        assert "[some-module/](some-module/)" in result


# ── check_index_sync ───────────────────────────────────────────


class TestCheckIndexSync:
    def test_in_sync_returns_empty(self, tmp_path: Path) -> None:
        """When _index.md matches current directory contents, returns empty list."""
        from wos.index import check_index_sync, generate_index

        (tmp_path / "doc.md").write_text(
            "---\nname: Doc\ndescription: A document\n---\n# Doc\n"
        )
        index_content = generate_index(tmp_path)
        (tmp_path / "_index.md").write_text(index_content)

        issues = check_index_sync(tmp_path)

        assert issues == []

    def test_missing_index(self, tmp_path: Path) -> None:
        """Missing _index.md returns an issue with 'missing' in the message."""
        from wos.index import check_index_sync

        (tmp_path / "doc.md").write_text(
            "---\nname: Doc\ndescription: A doc\n---\n"
        )

        issues = check_index_sync(tmp_path)

        assert len(issues) == 1
        assert "missing" in issues[0]["issue"].lower()
        assert issues[0]["severity"] == "fail"
        assert issues[0]["file"] == str(tmp_path / "_index.md")

    def test_file_added_after_generation(self, tmp_path: Path) -> None:
        """Adding a file after generation causes 'out of sync' issue."""
        from wos.index import check_index_sync, generate_index

        (tmp_path / "existing.md").write_text(
            "---\nname: Existing\ndescription: Was here\n---\n"
        )
        index_content = generate_index(tmp_path)
        (tmp_path / "_index.md").write_text(index_content)

        # Add a new file after index was generated
        (tmp_path / "newcomer.md").write_text(
            "---\nname: Newcomer\ndescription: Just arrived\n---\n"
        )

        issues = check_index_sync(tmp_path)

        assert len(issues) == 1
        assert "out of sync" in issues[0]["issue"].lower()
        assert issues[0]["severity"] == "fail"

    def test_file_removed_after_generation(self, tmp_path: Path) -> None:
        """Removing a file after generation causes 'out of sync' issue."""
        from wos.index import check_index_sync, generate_index

        (tmp_path / "keeper.md").write_text(
            "---\nname: Keeper\ndescription: Stays\n---\n"
        )
        (tmp_path / "goner.md").write_text(
            "---\nname: Goner\ndescription: Will be removed\n---\n"
        )
        index_content = generate_index(tmp_path)
        (tmp_path / "_index.md").write_text(index_content)

        # Remove the file after index was generated
        (tmp_path / "goner.md").unlink()

        issues = check_index_sync(tmp_path)

        assert len(issues) == 1
        assert "out of sync" in issues[0]["issue"].lower()
        assert issues[0]["severity"] == "fail"


# ── Preamble support ──────────────────────────────────────────


class TestPreamble:
    def test_extract_preamble_returns_text_between_heading_and_table(
        self, tmp_path: Path
    ) -> None:
        from wos.index import extract_preamble

        index = tmp_path / "_index.md"
        index.write_text(
            "# My Area\n\nThis area covers authentication.\n\n"
            "| File | Description |\n| --- | --- |\n| [a.md](a.md) | Doc A |\n"
        )
        assert extract_preamble(index) == "This area covers authentication."

    def test_extract_preamble_returns_none_when_no_preamble(
        self, tmp_path: Path
    ) -> None:
        from wos.index import extract_preamble

        index = tmp_path / "_index.md"
        index.write_text(
            "# My Area\n\n| File | Description |\n| --- | --- |\n"
        )
        assert extract_preamble(index) is None

    def test_extract_preamble_returns_none_for_missing_file(
        self, tmp_path: Path
    ) -> None:
        from wos.index import extract_preamble

        assert extract_preamble(tmp_path / "nonexistent.md") is None

    def test_generate_index_includes_preamble(self, tmp_path: Path) -> None:
        from wos.index import generate_index

        (tmp_path / "doc.md").write_text(
            "---\nname: Doc\ndescription: A document\n---\n# Doc\n"
        )
        result = generate_index(tmp_path, preamble="This area covers testing.")
        lines = result.splitlines()
        # Preamble should be between heading and table
        assert lines[0].startswith("# ")
        assert "This area covers testing." in result
        heading_idx = 0
        table_idx = next(
            i for i, line in enumerate(lines) if line.startswith("| File")
        )
        preamble_idx = next(
            i for i, line in enumerate(lines)
            if "This area covers testing." in line
        )
        assert heading_idx < preamble_idx < table_idx

    def test_generate_index_without_preamble_unchanged(
        self, tmp_path: Path
    ) -> None:
        from wos.index import generate_index

        (tmp_path / "doc.md").write_text(
            "---\nname: Doc\ndescription: A doc\n---\n"
        )
        result = generate_index(tmp_path)
        lines = result.splitlines()
        # No blank line with text between heading and table
        assert lines[0].startswith("# ")
        # Next non-empty line should be table header
        non_empty = [line for line in lines[1:] if line.strip()]
        assert non_empty[0].startswith("| File")

    def test_preamble_preserved_during_regeneration(
        self, tmp_path: Path
    ) -> None:
        from wos.index import extract_preamble, generate_index

        (tmp_path / "doc.md").write_text(
            "---\nname: Doc\ndescription: A document\n---\n# Doc\n"
        )
        # Write initial index with preamble
        initial = generate_index(tmp_path, preamble="My area description.")
        (tmp_path / "_index.md").write_text(initial)

        # Extract preamble and regenerate
        preamble = extract_preamble(tmp_path / "_index.md")
        regenerated = generate_index(tmp_path, preamble=preamble)

        assert "My area description." in regenerated
        assert initial == regenerated


# ── _extract_description ───────────────────────────────────────


class TestExtractDescription:
    def test_extracts_description_from_frontmatter(self, tmp_path: Path) -> None:
        from wos.index import _extract_description

        f = tmp_path / "doc.md"
        f.write_text(
            "---\nname: Doc\ndescription: A fine description\n---\n# Doc\n"
        )

        assert _extract_description(f) == "A fine description"

    def test_returns_none_without_frontmatter(self, tmp_path: Path) -> None:
        from wos.index import _extract_description

        f = tmp_path / "plain.md"
        f.write_text("# Just markdown\n\nNo frontmatter.\n")

        assert _extract_description(f) is None

    def test_returns_none_without_description_field(self, tmp_path: Path) -> None:
        from wos.index import _extract_description

        f = tmp_path / "no-desc.md"
        f.write_text("---\nname: Missing Desc\n---\n# Content\n")

        assert _extract_description(f) is None


# ── Compound suffix support ──────────────────────────────────


class TestCompoundSuffixIndex:
    def test_compound_suffix_files_included_in_index(
        self, tmp_path: Path
    ) -> None:
        """Files with compound suffixes (.research.md) appear in index."""
        from wos.index import generate_index

        (tmp_path / "api.research.md").write_text(
            "---\nname: API Research\ndescription: API investigation\n---\n"
        )
        (tmp_path / "plain.md").write_text(
            "---\nname: Plain\ndescription: A plain doc\n---\n"
        )

        result = generate_index(tmp_path)

        assert "[api.research.md]" in result
        assert "API investigation" in result
        assert "[plain.md]" in result

    def test_compound_suffix_mixed_with_plain_sorted(
        self, tmp_path: Path
    ) -> None:
        """Compound suffix files sort correctly among plain .md files."""
        from wos.index import generate_index

        (tmp_path / "beta.plan.md").write_text(
            "---\nname: Beta Plan\ndescription: A plan\n---\n"
        )
        (tmp_path / "alpha.md").write_text(
            "---\nname: Alpha\ndescription: First\n---\n"
        )

        result = generate_index(tmp_path)
        lines = result.splitlines()
        file_rows = [
            line for line in lines if line.startswith("| [") and ".md]" in line
        ]
        assert len(file_rows) == 2
        assert file_rows[0].startswith("| [alpha.md]")
        assert file_rows[1].startswith("| [beta.plan.md]")

    def test_compound_suffix_sync_check(self, tmp_path: Path) -> None:
        """Index sync works with compound suffix files."""
        from wos.index import check_index_sync, generate_index

        (tmp_path / "topic.design.md").write_text(
            "---\nname: Design\ndescription: A design\n---\n"
        )
        index_content = generate_index(tmp_path)
        (tmp_path / "_index.md").write_text(index_content)

        issues = check_index_sync(tmp_path)
        assert issues == []

    def test_compound_suffix_added_causes_desync(self, tmp_path: Path) -> None:
        """Adding a compound suffix file after generation causes desync."""
        from wos.index import check_index_sync, generate_index

        (tmp_path / "existing.md").write_text(
            "---\nname: Existing\ndescription: Was here\n---\n"
        )
        index_content = generate_index(tmp_path)
        (tmp_path / "_index.md").write_text(index_content)

        (tmp_path / "new-topic.context.md").write_text(
            "---\nname: New Topic\ndescription: Just arrived\n---\n"
        )

        issues = check_index_sync(tmp_path)
        assert len(issues) == 1
        assert "out of sync" in issues[0]["issue"].lower()
