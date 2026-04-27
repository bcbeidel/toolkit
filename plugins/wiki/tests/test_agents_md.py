"""Tests for agents_md.py — AGENTS.md marker-based section manager."""

from __future__ import annotations

from pathlib import Path

# ── discover_areas ─────────────────────────────────────────────


class TestDiscoverAreas:
    def test_discovers_areas_from_disk(self, tmp_path: Path) -> None:
        from wiki.agents_md import discover_areas

        # Create two area directories with docs
        api_dir = tmp_path / "docs" / "context" / "api"
        api_dir.mkdir(parents=True)
        (api_dir / "endpoints.md").write_text(
            "---\nname: Endpoints\ndescription: API endpoints\n---\n"
        )

        testing_dir = tmp_path / "docs" / "context" / "testing"
        testing_dir.mkdir(parents=True)
        (testing_dir / "unit.md").write_text(
            "---\nname: Unit Tests\ndescription: Unit testing\n---\n"
        )

        areas = discover_areas(tmp_path)
        assert len(areas) == 2
        assert areas[0] == {
            "name": "docs/context/api",
            "path": "docs/context/api",
        }
        assert areas[1] == {
            "name": "docs/context/testing",
            "path": "docs/context/testing",
        }

    def test_uses_relative_path_as_name(
        self, tmp_path: Path,
    ) -> None:
        from wiki.agents_md import discover_areas

        area_dir = tmp_path / "docs" / "context" / "my-area"
        area_dir.mkdir(parents=True)
        (area_dir / "topic.md").write_text(
            "---\nname: Topic\ndescription: A topic\n---\n"
        )

        areas = discover_areas(tmp_path)
        assert len(areas) == 1
        assert areas[0]["name"] == "docs/context/my-area"

    def test_returns_empty_when_no_docs(
        self, tmp_path: Path,
    ) -> None:
        from wiki.agents_md import discover_areas

        areas = discover_areas(tmp_path)
        assert areas == []

    def test_discovers_areas_anywhere(self, tmp_path: Path) -> None:
        """discover_areas finds document dirs outside docs/."""
        from wiki.agents_md import discover_areas

        project_dir = tmp_path / "project-x"
        project_dir.mkdir()
        (project_dir / "notes.md").write_text(
            "---\nname: Notes\ndescription: Project notes\n---\n"
        )

        areas = discover_areas(tmp_path)
        assert len(areas) == 1
        assert areas[0]["path"] == "project-x"

    def test_sorted_alphabetically(self, tmp_path: Path) -> None:
        from wiki.agents_md import discover_areas

        for name in ["zebra", "alpha", "middle"]:
            d = tmp_path / "docs" / name
            d.mkdir(parents=True)
            (d / "topic.md").write_text(
                f"---\nname: {name}\ndescription: {name}\n---\n"
            )

        areas = discover_areas(tmp_path)
        paths = [a["path"] for a in areas]
        assert paths == ["docs/alpha", "docs/middle", "docs/zebra"]


# ── render_wiki_section ──────────────────────────────────────────


class TestRenderNavigation:
    def test_renders_resolver_pointer(self) -> None:
        from wiki.agents_md import render_wiki_section

        result = render_wiki_section(areas=[])
        assert "[RESOLVER.md](RESOLVER.md)" in result
        assert "Consult it before filing or loading context." in result

    def test_renders_glob_discovery_convention(self) -> None:
        from wiki.agents_md import render_wiki_section

        result = render_wiki_section(areas=[])
        assert "Glob" in result
        assert "frontmatter" in result

    def test_does_not_render_areas_table_with_or_without_areas(self) -> None:
        from wiki.agents_md import render_wiki_section

        # With areas: still no Areas table.
        areas = [
            {"name": "Python Basics", "path": "docs/context/python-basics"},
        ]
        with_areas = render_wiki_section(areas)
        assert "### Areas" not in with_areas
        assert "| Area | Path |" not in with_areas

        # Without areas: also no Areas table.
        empty = render_wiki_section(areas=[])
        assert "### Areas" not in empty
        assert "| Area | Path |" not in empty

    def test_does_not_render_index_md_cue(self) -> None:
        from wiki.agents_md import render_wiki_section

        result = render_wiki_section(areas=[
            {"name": ".context", "path": ".context"},
        ])
        assert "_index.md" not in result


class TestRenderMetadataFormat:
    def test_renders_metadata_format_section(self) -> None:
        from wiki.agents_md import render_wiki_section

        result = render_wiki_section(areas=[])
        assert "### File Metadata Format" in result
        assert "name: Title" in result
        assert "description: What this covers" in result
        assert "type: research" in result
        assert "sources: []" in result
        assert "related: []" in result


class TestRenderLostInTheMiddleCue:
    def test_renders_navigation_cue(self) -> None:
        from wiki.agents_md import render_wiki_section

        result = render_wiki_section(areas=[])
        # The "lost in the middle" cue: key info at start and end
        assert "## Context Navigation" in result
        assert "Read the `description` field before reading the full file." in result
        assert "Documents put key insights first and last" in result


class TestRenderDocumentStandards:
    def test_renders_document_standards_section(self) -> None:
        from wiki.agents_md import render_wiki_section

        result = render_wiki_section(areas=[])
        assert "### Document Standards" in result

    def test_renders_structure_guidance(self) -> None:
        from wiki.agents_md import render_wiki_section

        result = render_wiki_section(areas=[])
        assert "Key insights first" in result
        assert "detail in the middle" in result
        assert "takeaways at the bottom" in result

    def test_renders_word_count_guidance(self) -> None:
        from wiki.agents_md import render_wiki_section

        result = render_wiki_section(areas=[])
        assert "200-800 words" in result

    def test_renders_linking_guidance(self) -> None:
        from wiki.agents_md import render_wiki_section

        result = render_wiki_section(areas=[])
        assert "bidirectional" in result.lower()

    def test_renders_one_concept_per_file(self) -> None:
        from wiki.agents_md import render_wiki_section

        result = render_wiki_section(areas=[])
        assert "one concept per file" in result.lower()


class TestRenderMarkers:
    def test_output_wrapped_in_markers(self) -> None:
        from wiki.agents_md import BEGIN_MARKER, END_MARKER, render_wiki_section

        result = render_wiki_section(areas=[])
        assert result.startswith(BEGIN_MARKER)
        assert result.rstrip().endswith(END_MARKER)


# ── legacy-marker migration ────────────────────────────────────


class TestMigrateLegacyMarkers:
    def test_migrates_legacy_wos_markers(self) -> None:
        from wiki.agents_md import update_agents_md

        legacy = (
            "# AGENTS.md\n"
            "preamble\n"
            "<!-- wos:begin -->\n"
            "<!-- wos:layout: flat -->\n"
            "## Context Navigation\n"
            "old body\n"
            "<!-- wos:end -->\n"
            "epilogue\n"
        )
        result = update_agents_md(legacy, areas=[])
        assert "<!-- wos:begin -->" not in result
        assert "<!-- wos:end -->" not in result
        assert "<!-- wos:layout:" not in result
        assert "<!-- wiki:begin -->" in result
        assert "<!-- wiki:end -->" in result
        assert "<!-- wiki:layout: flat -->" in result
        # Content outside markers preserved
        assert "preamble" in result
        assert "epilogue" in result

    def test_idempotent_on_current_markers(self) -> None:
        from wiki.agents_md import _migrate_legacy_markers

        content = (
            "# AGENTS.md\n"
            "<!-- wiki:begin -->\n"
            "<!-- wiki:layout: separated -->\n"
            "body\n"
            "<!-- wiki:end -->\n"
        )
        assert _migrate_legacy_markers(content) == content


# ── update_agents_md ────────────────────────────────────────────


class TestUpdateReplaceExisting:
    def test_replaces_existing_section(self) -> None:
        from wiki.agents_md import BEGIN_MARKER, END_MARKER, update_agents_md

        content = (
            "# AGENTS.md\n\n"
            f"{BEGIN_MARKER}\nold content\n{END_MARKER}\n\n"
            "## Other Section\n"
        )
        areas = [{"name": "API", "path": "docs/context/api"}]
        result = update_agents_md(content, areas)
        assert "old content" not in result
        assert "[RESOLVER.md](RESOLVER.md)" in result
        assert BEGIN_MARKER in result
        assert END_MARKER in result


class TestUpdateAppendWhenNoMarkers:
    def test_appends_when_no_markers(self) -> None:
        from wiki.agents_md import BEGIN_MARKER, END_MARKER, update_agents_md

        content = "# AGENTS.md\n\nSome existing content.\n"
        areas = [{"name": "API", "path": "docs/context/api"}]
        result = update_agents_md(content, areas)
        assert result.startswith("# AGENTS.md")
        assert "Some existing content." in result
        assert BEGIN_MARKER in result
        assert END_MARKER in result


class TestUpdatePreservesOutsideContent:
    def test_preserves_content_outside_markers(self) -> None:
        from wiki.agents_md import BEGIN_MARKER, END_MARKER, update_agents_md

        content = (
            "# AGENTS.md\n\n"
            "Before section.\n\n"
            f"{BEGIN_MARKER}\nold\n{END_MARKER}\n\n"
            "After section.\n"
        )
        result = update_agents_md(content, areas=[])
        assert "# AGENTS.md" in result
        assert "Before section." in result
        assert "After section." in result
        assert "old" not in result


class TestUpdateAreasNotRendered:
    def test_areas_not_rendered_in_updated_output(self) -> None:
        """`update_agents_md` accepts `areas=` for API compatibility but
        no longer renders an Areas table — directory-level routing lives
        in RESOLVER.md, and per-file discovery uses Glob + frontmatter Read.
        """
        from wiki.agents_md import update_agents_md

        content = "# AGENTS.md\n"
        areas = [
            {"name": "Frontend", "path": "docs/context/frontend"},
            {"name": "Backend", "path": "docs/context/backend"},
        ]
        result = update_agents_md(content, areas)
        assert "### Areas" not in result
        assert "| Frontend | docs/context/frontend |" not in result
        assert "[RESOLVER.md](RESOLVER.md)" in result


# ── extract_areas ───────────────────────────────────────────────


class TestExtractAreas:
    def test_preserves_human_descriptions(self) -> None:
        """Human-written descriptions (col1 != col2) are preserved as-is."""
        from wiki.agents_md import BEGIN_MARKER, END_MARKER, extract_areas

        content = (
            f"{BEGIN_MARKER}\n"
            "### Areas\n"
            "| Area | Path |\n"
            "|------|------|\n"
            "| How LLM agents decompose tasks into steps | docs/context/planning |\n"
            "| API endpoint reference | docs/context/api |\n"
            f"{END_MARKER}\n"
        )
        result = extract_areas(content)
        assert result == [
            {
                "name": "How LLM agents decompose tasks into steps",
                "path": "docs/context/planning",
            },
            {"name": "API endpoint reference", "path": "docs/context/api"},
        ]

    def test_returns_empty_when_no_markers(self) -> None:
        from wiki.agents_md import extract_areas

        result = extract_areas("# AGENTS.md\n\nNo managed section here.\n")
        assert result == []

    def test_returns_empty_when_no_areas_table(self) -> None:
        from wiki.agents_md import extract_areas, render_wiki_section

        content = render_wiki_section(areas=[])
        result = extract_areas(content)
        assert result == []


class TestUpdateAgentsMdAreasNone:
    def test_areas_table_in_existing_content_is_removed_on_update(self) -> None:
        """A pre-existing Areas table inside the managed region is dropped on
        re-render — directory-level routing now lives in RESOLVER.md."""
        from wiki.agents_md import BEGIN_MARKER, END_MARKER, update_agents_md

        content = (
            "# AGENTS.md\n\n"
            f"{BEGIN_MARKER}\n"
            "### Areas\n"
            "| Area | Path |\n"
            "|------|------|\n"
            "| How LLM agents decompose tasks | docs/context/planning |\n"
            f"{END_MARKER}\n"
        )
        result = update_agents_md(content)  # areas=None by default
        assert "### Areas" not in result
        assert "[RESOLVER.md](RESOLVER.md)" in result

    def test_produces_no_areas_section_when_none_exist(self) -> None:
        """When no Areas table is present, output also has none."""
        from wiki.agents_md import render_wiki_section, update_agents_md

        base = render_wiki_section(areas=[])
        content = f"# AGENTS.md\n\n{base}"
        result = update_agents_md(content)
        assert "### Areas" not in result

    def test_explicit_areas_still_no_table_rendered(self) -> None:
        """Passing areas= is accepted for API compatibility but no table is rendered."""
        from wiki.agents_md import update_agents_md

        areas = [{"name": "Backend", "path": "docs/context/backend"}]
        result = update_agents_md("# AGENTS.md\n", areas=areas)
        assert "### Areas" not in result
        assert "| Backend | docs/context/backend |" not in result


# ── has_working_agreements ─────────────────────────────────────


class TestHasWorkingAgreements:
    def test_detects_heading(self) -> None:
        from wiki.agents_md import has_working_agreements

        content = "# AGENTS.md\n\n## Working Agreements\n\n- Codify repetition.\n"
        assert has_working_agreements(content) is True

    def test_detects_heading_with_trailing_whitespace(self) -> None:
        from wiki.agents_md import has_working_agreements

        content = "## Working Agreements   \n"
        assert has_working_agreements(content) is True

    def test_detects_heading_inside_managed_markers(self) -> None:
        from wiki.agents_md import has_working_agreements

        content = (
            "# AGENTS.md\n"
            "<!-- wiki:begin -->\n"
            "## Working Agreements\n"
            "- Codify repetition.\n"
            "<!-- wiki:end -->\n"
        )
        assert has_working_agreements(content) is True

    def test_detects_heading_outside_managed_markers(self) -> None:
        from wiki.agents_md import has_working_agreements

        content = (
            "# AGENTS.md\n"
            "<!-- wiki:begin -->\n"
            "## Context Navigation\n"
            "<!-- wiki:end -->\n"
            "\n"
            "## Working Agreements\n"
            "- Codify repetition.\n"
        )
        assert has_working_agreements(content) is True

    def test_case_insensitive(self) -> None:
        from wiki.agents_md import has_working_agreements

        assert has_working_agreements("## working agreements\n") is True
        assert has_working_agreements("## WORKING AGREEMENTS\n") is True

    def test_does_not_match_substring(self) -> None:
        from wiki.agents_md import has_working_agreements

        assert has_working_agreements("## My Working Agreements Notes\n") is False
        assert has_working_agreements("### Working Agreements\n") is False

    def test_empty_string(self) -> None:
        from wiki.agents_md import has_working_agreements

        assert has_working_agreements("") is False

    def test_no_section(self) -> None:
        from wiki.agents_md import has_working_agreements

        content = (
            "# AGENTS.md\n"
            "<!-- wiki:begin -->\n"
            "## Context Navigation\n"
            "<!-- wiki:end -->\n"
        )
        assert has_working_agreements(content) is False

