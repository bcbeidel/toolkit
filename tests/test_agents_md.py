"""Tests for wos/agents_md.py — AGENTS.md marker-based section manager."""

from __future__ import annotations

from pathlib import Path

# ── discover_areas ─────────────────────────────────────────────


class TestDiscoverAreas:
    def test_discovers_areas_from_disk(self, tmp_path: Path) -> None:
        from wos.agents_md import discover_areas

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
        from wos.agents_md import discover_areas

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
        from wos.agents_md import discover_areas

        areas = discover_areas(tmp_path)
        assert areas == []

    def test_discovers_areas_anywhere(self, tmp_path: Path) -> None:
        """discover_areas finds document dirs outside docs/."""
        from wos.agents_md import discover_areas

        project_dir = tmp_path / "project-x"
        project_dir.mkdir()
        (project_dir / "notes.md").write_text(
            "---\nname: Notes\ndescription: Project notes\n---\n"
        )

        areas = discover_areas(tmp_path)
        assert len(areas) == 1
        assert areas[0]["path"] == "project-x"

    def test_sorted_alphabetically(self, tmp_path: Path) -> None:
        from wos.agents_md import discover_areas

        for name in ["zebra", "alpha", "middle"]:
            d = tmp_path / "docs" / name
            d.mkdir(parents=True)
            (d / "topic.md").write_text(
                f"---\nname: {name}\ndescription: {name}\n---\n"
            )

        areas = discover_areas(tmp_path)
        paths = [a["path"] for a in areas]
        assert paths == ["docs/alpha", "docs/middle", "docs/zebra"]


# ── render_wos_section ──────────────────────────────────────────


class TestRenderWithAreas:
    def test_renders_area_table(self) -> None:
        from wos.agents_md import render_wos_section

        areas = [
            {"name": "Python Basics", "path": "docs/context/python-basics"},
            {"name": "Testing", "path": "docs/context/testing"},
        ]
        result = render_wos_section(areas)
        assert "| Area | Path |" in result
        assert "| Python Basics | docs/context/python-basics |" in result
        assert "| Testing | docs/context/testing |" in result

    def test_areas_section_omitted_when_empty(self) -> None:
        from wos.agents_md import render_wos_section

        result = render_wos_section(areas=[])
        assert "### Areas" not in result
        assert "| Area | Path |" not in result


class TestRenderWithPreferences:
    def test_renders_preferences(self) -> None:
        from wos.agents_md import render_wos_section

        prefs = ["Be concise", "Prefer bullet points"]
        result = render_wos_section(areas=[], preferences=prefs)
        assert "### Preferences" in result
        assert "- Be concise" in result
        assert "- Prefer bullet points" in result

    def test_preferences_omitted_when_none(self) -> None:
        from wos.agents_md import render_wos_section

        result = render_wos_section(areas=[], preferences=None)
        assert "### Preferences" not in result

    def test_preferences_omitted_when_empty_list(self) -> None:
        from wos.agents_md import render_wos_section

        result = render_wos_section(areas=[], preferences=[])
        assert "### Preferences" not in result


class TestRenderMetadataFormat:
    def test_renders_metadata_format_section(self) -> None:
        from wos.agents_md import render_wos_section

        result = render_wos_section(areas=[])
        assert "### File Metadata Format" in result
        assert "name: Title" in result
        assert "description: What this covers" in result
        assert "type: research" in result
        assert "sources: []" in result
        assert "related: []" in result


class TestRenderLostInTheMiddleCue:
    def test_renders_navigation_cue(self) -> None:
        from wos.agents_md import render_wos_section

        result = render_wos_section(areas=[])
        # The "lost in the middle" cue: key info at start and end
        assert "## Context Navigation" in result
        assert "Read the `description` field before reading the full file." in result
        assert "Documents put key insights first and last" in result


class TestRenderDocumentStandards:
    def test_renders_document_standards_section(self) -> None:
        from wos.agents_md import render_wos_section

        result = render_wos_section(areas=[])
        assert "### Document Standards" in result

    def test_renders_structure_guidance(self) -> None:
        from wos.agents_md import render_wos_section

        result = render_wos_section(areas=[])
        assert "Key insights first" in result
        assert "detail in the middle" in result
        assert "takeaways at the bottom" in result

    def test_renders_word_count_guidance(self) -> None:
        from wos.agents_md import render_wos_section

        result = render_wos_section(areas=[])
        assert "200-800 words" in result

    def test_renders_linking_guidance(self) -> None:
        from wos.agents_md import render_wos_section

        result = render_wos_section(areas=[])
        assert "bidirectional" in result.lower()

    def test_renders_one_concept_per_file(self) -> None:
        from wos.agents_md import render_wos_section

        result = render_wos_section(areas=[])
        assert "one concept per file" in result.lower()


class TestExtractPreferences:
    def test_extracts_preferences_from_wos_section(self) -> None:
        from wos.agents_md import extract_preferences, render_wos_section

        prefs = ["**Directness:** Be direct.", "**Tone:** Keep it casual."]
        content = f"# AGENTS.md\n\n{render_wos_section(areas=[], preferences=prefs)}"
        result = extract_preferences(content)
        assert result == prefs

    def test_returns_empty_when_no_markers(self) -> None:
        from wos.agents_md import extract_preferences

        result = extract_preferences("# AGENTS.md\n\nNo WOS section here.\n")
        assert result == []

    def test_returns_empty_when_no_preferences_section(self) -> None:
        from wos.agents_md import extract_preferences, render_wos_section

        content = render_wos_section(areas=[], preferences=None)
        result = extract_preferences(content)
        assert result == []

    def test_preserves_preference_content_exactly(self) -> None:
        from wos.agents_md import extract_preferences, render_wos_section

        prefs = [
            "**Directness:** Be direct. State problems and disagreements "
            "plainly without hedging or softening."
        ]
        content = render_wos_section(areas=[], preferences=prefs)
        result = extract_preferences(content)
        assert result == prefs


class TestRenderMarkers:
    def test_output_wrapped_in_markers(self) -> None:
        from wos.agents_md import BEGIN_MARKER, END_MARKER, render_wos_section

        result = render_wos_section(areas=[])
        assert result.startswith(BEGIN_MARKER)
        assert result.rstrip().endswith(END_MARKER)


# ── update_agents_md ────────────────────────────────────────────


class TestUpdateReplaceExisting:
    def test_replaces_existing_section(self) -> None:
        from wos.agents_md import BEGIN_MARKER, END_MARKER, update_agents_md

        content = (
            "# AGENTS.md\n\n"
            f"{BEGIN_MARKER}\nold content\n{END_MARKER}\n\n"
            "## Other Section\n"
        )
        areas = [{"name": "API", "path": "docs/context/api"}]
        result = update_agents_md(content, areas)
        assert "old content" not in result
        assert "| API | docs/context/api |" in result
        assert BEGIN_MARKER in result
        assert END_MARKER in result


class TestUpdateAppendWhenNoMarkers:
    def test_appends_when_no_markers(self) -> None:
        from wos.agents_md import BEGIN_MARKER, END_MARKER, update_agents_md

        content = "# AGENTS.md\n\nSome existing content.\n"
        areas = [{"name": "API", "path": "docs/context/api"}]
        result = update_agents_md(content, areas)
        assert result.startswith("# AGENTS.md")
        assert "Some existing content." in result
        assert BEGIN_MARKER in result
        assert END_MARKER in result


class TestUpdatePreservesOutsideContent:
    def test_preserves_content_outside_markers(self) -> None:
        from wos.agents_md import BEGIN_MARKER, END_MARKER, update_agents_md

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


class TestUpdateAreasAppearInOutput:
    def test_areas_in_updated_output(self) -> None:
        from wos.agents_md import update_agents_md

        content = "# AGENTS.md\n"
        areas = [
            {"name": "Frontend", "path": "docs/context/frontend"},
            {"name": "Backend", "path": "docs/context/backend"},
        ]
        result = update_agents_md(content, areas)
        assert "| Frontend | docs/context/frontend |" in result
        assert "| Backend | docs/context/backend |" in result


class TestUpdatePreferencesPreserved:
    def test_preferences_in_updated_output(self) -> None:
        from wos.agents_md import update_agents_md

        content = "# AGENTS.md\n"
        prefs = ["Keep it short", "Use examples"]
        result = update_agents_md(content, areas=[], preferences=prefs)
        assert "### Preferences" in result
        assert "- Keep it short" in result
        assert "- Use examples" in result


