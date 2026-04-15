"""Tests for wos/validators.py — per-file and project-wide validation checks."""

from __future__ import annotations

from pathlib import Path

# ── Helpers ─────────────────────────────────────────────────────


def _md(name: str = "Test", description: str = "A test doc", **extra_fm) -> str:
    """Build a minimal markdown string with frontmatter."""
    lines = ["---", f"name: {name}", f"description: {description}"]
    for key, value in extra_fm.items():
        if isinstance(value, list):
            lines.append(f"{key}:")
            for item in value:
                lines.append(f"  - {item}")
        else:
            lines.append(f"{key}: {value}")
    lines.append("---")
    lines.append(f"# {name}")
    lines.append("")
    return "\n".join(lines) + "\n"


# ── check_all_indexes ──────────────────────────────────────────


class TestCheckAllIndexes:
    def test_synced_index_with_preamble(self, tmp_path: Path) -> None:
        from wos.index import generate_index
        from wos.project import check_all_indexes

        # Create a directory with a file and a synced _index.md with preamble
        area = tmp_path / "context" / "testing"
        area.mkdir(parents=True)
        topic = area / "unit-tests.md"
        topic.write_text(
            "---\nname: Unit Tests\n"
            "description: Unit testing guide\n"
            "---\n# Unit Tests\n"
        )
        index = area / "_index.md"
        index.write_text(generate_index(area, preamble="Testing area."))
        # Also create a synced index for the context root
        context_dir = tmp_path / "context"
        (context_dir / "_index.md").write_text(
            generate_index(context_dir, preamble="All context.")
        )

        issues = check_all_indexes(context_dir)
        assert issues == []

    def test_missing_index(self, tmp_path: Path) -> None:
        from wos.project import check_all_indexes

        # Create a directory with a file but no _index.md
        area = tmp_path / "context" / "testing"
        area.mkdir(parents=True)
        topic = area / "unit-tests.md"
        topic.write_text(
            "---\nname: Unit Tests\n"
            "description: Unit testing guide\n"
            "---\n# Unit Tests\n"
        )

        issues = check_all_indexes(tmp_path / "context")
        assert len(issues) >= 1
        assert any("missing" in i["issue"].lower() for i in issues)


class TestCheckPreamble:
    def test_index_with_preamble_no_warning(self, tmp_path: Path) -> None:
        from wos.index import generate_index
        from wos.project import check_all_indexes

        area = tmp_path / "context" / "api"
        area.mkdir(parents=True)
        (area / "auth.md").write_text(
            "---\nname: Auth\ndescription: Auth docs\n---\n"
        )
        index = generate_index(area, preamble="This area covers the API.")
        (area / "_index.md").write_text(index)
        (tmp_path / "context" / "_index.md").write_text(
            generate_index(tmp_path / "context", preamble="All context.")
        )

        issues = check_all_indexes(tmp_path / "context")
        warn_issues = [i for i in issues if i["severity"] == "warn"]
        assert not any("preamble" in i["issue"].lower() for i in warn_issues)

    def test_index_without_preamble_warns(self, tmp_path: Path) -> None:
        from wos.index import generate_index
        from wos.project import check_all_indexes

        area = tmp_path / "context" / "api"
        area.mkdir(parents=True)
        (area / "auth.md").write_text(
            "---\nname: Auth\ndescription: Auth docs\n---\n"
        )
        # No preamble
        index = generate_index(area)
        (area / "_index.md").write_text(index)
        (tmp_path / "context" / "_index.md").write_text(
            generate_index(tmp_path / "context")
        )

        issues = check_all_indexes(tmp_path / "context")
        warn_issues = [i for i in issues if i["severity"] == "warn"]
        assert any("area description" in i["issue"].lower() for i in warn_issues)


# ── check_project_files ────────────────────────────────────────


class TestCheckProjectFiles:
    def test_no_agents_md_warns(self, tmp_path: Path) -> None:
        from wos.project import check_project_files

        issues = check_project_files(tmp_path)
        agents_issues = [i for i in issues if i["file"] == "AGENTS.md"]
        assert any("No AGENTS.md" in i["issue"] for i in agents_issues)

    def test_agents_md_without_markers_warns(self, tmp_path: Path) -> None:
        from wos.project import check_project_files

        (tmp_path / "AGENTS.md").write_text("# Agents\n\nSome content.\n")
        issues = check_project_files(tmp_path)
        agents_issues = [i for i in issues if i["file"] == "AGENTS.md"]
        assert any("markers" in i["issue"].lower() for i in agents_issues)

    def test_agents_md_with_markers_clean(self, tmp_path: Path) -> None:
        from wos.project import check_project_files

        (tmp_path / "AGENTS.md").write_text(
            "# Agents\n\n<!-- wos:begin -->\nWOS content\n<!-- wos:end -->\n"
        )
        issues = check_project_files(tmp_path)
        agents_issues = [i for i in issues if i["file"] == "AGENTS.md"]
        assert agents_issues == []

    def test_no_claude_md_warns(self, tmp_path: Path) -> None:
        from wos.project import check_project_files

        issues = check_project_files(tmp_path)
        claude_issues = [i for i in issues if i["file"] == "CLAUDE.md"]
        assert any("No CLAUDE.md" in i["issue"] for i in claude_issues)

    def test_claude_md_without_agents_ref_warns(self, tmp_path: Path) -> None:
        from wos.project import check_project_files

        (tmp_path / "CLAUDE.md").write_text("# Project\n\nSome instructions.\n")
        issues = check_project_files(tmp_path)
        claude_issues = [i for i in issues if i["file"] == "CLAUDE.md"]
        assert any("@AGENTS.md" in i["issue"] for i in claude_issues)

    def test_claude_md_with_agents_ref_clean(self, tmp_path: Path) -> None:
        from wos.project import check_project_files

        (tmp_path / "CLAUDE.md").write_text(
            "# Project\n\n@AGENTS.md\n\nSome instructions.\n"
        )
        issues = check_project_files(tmp_path)
        claude_issues = [i for i in issues if i["file"] == "CLAUDE.md"]
        assert claude_issues == []


# ── validate_file ──────────────────────────────────────────────


class TestValidateFile:
    def test_valid_file(self, tmp_path: Path) -> None:
        from wos.project import validate_file

        md_file = tmp_path / "docs" / "context" / "testing" / "unit-tests.md"
        md_file.parent.mkdir(parents=True)
        md_file.write_text(_md("Unit Tests", "Guide to unit tests"))

        issues = validate_file(md_file, tmp_path, verify_urls=False)
        assert issues == []

    def test_file_without_frontmatter(self, tmp_path: Path) -> None:
        from wos.project import validate_file

        md_file = tmp_path / "docs" / "context" / "testing" / "bad.md"
        md_file.parent.mkdir(parents=True)
        md_file.write_text("# No Frontmatter\n\nJust content.\n")

        issues = validate_file(md_file, tmp_path, verify_urls=False)
        assert len(issues) == 1
        assert issues[0]["severity"] == "fail"
        msg = issues[0]["issue"].lower()
        assert "parse" in msg or "frontmatter" in msg


# ── validate_project ───────────────────────────────────────────


class TestValidateProject:
    def test_valid_project(self, tmp_path: Path) -> None:
        from wos.index import generate_index
        from wos.project import validate_project

        # Set up a document under docs/
        area = tmp_path / "docs" / "context" / "testing"
        area.mkdir(parents=True)
        topic = area / "unit-tests.md"
        topic.write_text(_md("Unit Tests", "Guide to unit tests"))
        # Create synced index with preambles for the area
        (area / "_index.md").write_text(
            generate_index(area, preamble="Testing area.")
        )
        # Create AGENTS.md with WOS markers and CLAUDE.md with @AGENTS.md
        (tmp_path / "AGENTS.md").write_text(
            "# Agents\n\n<!-- wos:begin -->\nWOS\n<!-- wos:end -->\n"
        )
        (tmp_path / "CLAUDE.md").write_text(
            "# Project\n\n@AGENTS.md\n"
        )

        issues = validate_project(tmp_path, verify_urls=False)
        assert issues == []

    def test_discovers_docs_outside_docs_dir(self, tmp_path: Path) -> None:
        """validate_project finds documents anywhere in the tree."""
        from wos.project import validate_project

        # Put a research doc outside docs/
        research = tmp_path / "project-x" / "study.research.md"
        research.parent.mkdir(parents=True)
        research.write_text(_md(
            "Study", "A research study",
            type="research",
            sources=["https://example.com"],
        ))
        (tmp_path / "AGENTS.md").write_text(
            "# Agents\n\n<!-- wos:begin -->\nWOS\n<!-- wos:end -->\n"
        )
        (tmp_path / "CLAUDE.md").write_text("# Project\n\n@AGENTS.md\n")

        issues = validate_project(tmp_path, verify_urls=False)
        # Should find the doc (no frontmatter errors) but may have
        # index sync issues — that's expected
        frontmatter_issues = [
            i for i in issues if "frontmatter" in i["issue"].lower()
        ]
        assert frontmatter_issues == []


# ── Compound suffix integration ───────────────────────────────


class TestCompoundSuffixValidation:
    def test_validate_file_with_compound_suffix(self, tmp_path: Path) -> None:
        """validate_file works on compound suffix files."""
        from wos.project import validate_file

        md_file = tmp_path / "docs" / "research" / "api.research.md"
        md_file.parent.mkdir(parents=True)
        md_file.write_text(_md(
            "API Research", "Research on API patterns",
            type="research",
            sources=["https://example.com/source"],
        ))

        issues = validate_file(md_file, tmp_path, verify_urls=False)
        assert issues == []

    def test_compound_suffix_infers_type_for_research_validation(
        self, tmp_path: Path
    ) -> None:
        """Research file with compound suffix (no frontmatter type) triggers
        research-specific validation (sources required)."""
        from wos.project import validate_file

        md_file = tmp_path / "docs" / "research" / "topic.research.md"
        md_file.parent.mkdir(parents=True)
        # No type in frontmatter, no sources — should fail because
        # suffix infers type=research, and research requires sources
        md_file.write_text(_md("Topic", "A research topic"))

        issues = validate_file(md_file, tmp_path, verify_urls=False)
        assert any(
            "sources" in i["issue"].lower() and i["severity"] == "fail"
            for i in issues
        )

    def test_compound_suffix_research_with_sources_passes(
        self, tmp_path: Path
    ) -> None:
        """Research file with compound suffix and sources passes validation."""
        from wos.project import validate_file

        md_file = tmp_path / "docs" / "research" / "topic.research.md"
        md_file.parent.mkdir(parents=True)
        # No explicit type — inferred from suffix; has sources
        md_file.write_text(_md(
            "Topic", "A research topic",
            sources=["https://example.com/src"],
        ))

        issues = validate_file(md_file, tmp_path, verify_urls=False)
        assert not any("sources" in i["issue"].lower() for i in issues)

    def test_compound_suffix_draft_marker_check(self, tmp_path: Path) -> None:
        """Draft marker surfaced via doc.issues() on ResearchDocument."""
        from wos.document import parse_document

        text = (
            "---\n"
            "name: Draft Research\n"
            "description: In-progress research\n"
            "sources:\n"
            "  - https://example.com/src\n"
            "---\n"
            "# Research\n\n<!-- DRAFT -->\n\nContent.\n"
        )
        doc = parse_document("docs/research/topic.research.md", text)
        assert doc.type == "research"
        issues = doc.issues(tmp_path, verify_urls=False)
        assert any("DRAFT" in i["issue"] for i in issues)

    def test_validate_project_includes_compound_suffix_files(
        self, tmp_path: Path
    ) -> None:
        """validate_project discovers and validates compound suffix files."""
        from wos.index import generate_index
        from wos.project import validate_project

        # Set up research area with a compound suffix file
        research_dir = tmp_path / "docs" / "research"
        research_dir.mkdir(parents=True)
        (research_dir / "api.research.md").write_text(_md(
            "API Research", "Research on APIs",
            type="research",
            sources=["https://example.com/api"],
        ))
        (research_dir / "_index.md").write_text(
            generate_index(research_dir, preamble="Research area.")
        )
        # Create AGENTS.md and CLAUDE.md
        (tmp_path / "AGENTS.md").write_text(
            "# Agents\n\n<!-- wos:begin -->\nWOS\n<!-- wos:end -->\n"
        )
        (tmp_path / "CLAUDE.md").write_text("# Project\n\n@AGENTS.md\n")

        issues = validate_project(tmp_path, verify_urls=False)
        # Filter out index issues — we only care about document validation
        doc_issues = [i for i in issues if "index" not in i["issue"].lower()]
        assert doc_issues == []

    def test_context_type_no_related_warns(self, tmp_path: Path) -> None:
        """Context file without related fields warns via validate_file."""
        from wos.project import validate_file

        md_file = tmp_path / "auth.context.md"
        md_file.write_text(_md(
            "Auth Patterns",
            "Auth implementation patterns",
            type="context",
        ))

        issues = validate_file(md_file, tmp_path, verify_urls=False)
        assert any(
            i["severity"] == "warn" and "related" in i["issue"].lower()
            for i in issues
        )

    def test_context_type_with_related_no_warn(self, tmp_path: Path) -> None:
        """Context file with related field has no related-field warning."""
        from wos.project import validate_file

        related_file = tmp_path / "ref.md"
        related_file.write_text("---\nname: Ref\ndescription: Ref\n---\nbody\n")
        md_file = tmp_path / "auth.context.md"
        md_file.write_text(_md(
            "Auth Patterns",
            "Auth implementation patterns",
            type="context",
            related=["ref.md"],
        ))

        issues = validate_file(md_file, tmp_path, verify_urls=False)
        assert not any("related" in i["issue"].lower() for i in issues)
