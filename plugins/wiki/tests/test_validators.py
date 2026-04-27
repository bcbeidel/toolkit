"""Tests for validators.py — per-file and project-wide validation checks."""

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


# ── check_project_files ────────────────────────────────────────


class TestCheckProjectFiles:
    def test_no_agents_md_warns(self, tmp_path: Path) -> None:
        from wiki.project import check_project_files

        issues = check_project_files(tmp_path)
        agents_issues = [i for i in issues if i["file"] == "AGENTS.md"]
        assert any("No AGENTS.md" in i["issue"] for i in agents_issues)

    def test_agents_md_without_markers_warns(self, tmp_path: Path) -> None:
        from wiki.project import check_project_files

        (tmp_path / "AGENTS.md").write_text("# Agents\n\nSome content.\n")
        issues = check_project_files(tmp_path)
        agents_issues = [i for i in issues if i["file"] == "AGENTS.md"]
        assert any("markers" in i["issue"].lower() for i in agents_issues)

    def test_agents_md_with_markers_clean(self, tmp_path: Path) -> None:
        from wiki.project import check_project_files

        (tmp_path / "AGENTS.md").write_text(
            "# Agents\n\n<!-- wiki:begin -->\nmanaged content\n<!-- wiki:end -->\n"
        )
        issues = check_project_files(tmp_path)
        agents_issues = [i for i in issues if i["file"] == "AGENTS.md"]
        assert agents_issues == []

    def test_no_claude_md_warns(self, tmp_path: Path) -> None:
        from wiki.project import check_project_files

        issues = check_project_files(tmp_path)
        claude_issues = [i for i in issues if i["file"] == "CLAUDE.md"]
        assert any("No CLAUDE.md" in i["issue"] for i in claude_issues)

    def test_claude_md_without_agents_ref_warns(self, tmp_path: Path) -> None:
        from wiki.project import check_project_files

        (tmp_path / "CLAUDE.md").write_text("# Project\n\nSome instructions.\n")
        issues = check_project_files(tmp_path)
        claude_issues = [i for i in issues if i["file"] == "CLAUDE.md"]
        assert any("@AGENTS.md" in i["issue"] for i in claude_issues)

    def test_claude_md_with_agents_ref_clean(self, tmp_path: Path) -> None:
        from wiki.project import check_project_files

        (tmp_path / "CLAUDE.md").write_text(
            "# Project\n\n@AGENTS.md\n\nSome instructions.\n"
        )
        issues = check_project_files(tmp_path)
        claude_issues = [i for i in issues if i["file"] == "CLAUDE.md"]
        assert claude_issues == []


# ── check_resolver_recommendation ──────────────────────────────


def _seed_conventionful_dirs(root: Path, dirs: list[str]) -> None:
    """Create the given top-level dirs, each with two convention files."""
    suffix_for = {
        ".context": ".context.md",
        ".plans": ".plan.md",
        ".designs": ".design.md",
        ".research": ".research.md",
        "context": ".context.md",
        "plans": ".plan.md",
        "designs": ".design.md",
        "research": ".research.md",
    }
    for name in dirs:
        d = root / name
        d.mkdir(parents=True, exist_ok=True)
        suffix = suffix_for.get(name, ".context.md")
        (d / f"a{suffix}").write_text(_md("A"))
        (d / f"b{suffix}").write_text(_md("B"))


class TestCheckResolverRecommendation:
    def test_no_recommendation_when_resolver_present(self, tmp_path: Path) -> None:
        from wiki.project import check_resolver_recommendation

        (tmp_path / "RESOLVER.md").write_text("# RESOLVER.md\n")
        _seed_conventionful_dirs(tmp_path, [".context", ".plans", ".designs"])
        assert check_resolver_recommendation(tmp_path) == []

    def test_no_recommendation_below_threshold(self, tmp_path: Path) -> None:
        from wiki.project import check_resolver_recommendation

        _seed_conventionful_dirs(tmp_path, [".context", ".plans"])
        assert check_resolver_recommendation(tmp_path) == []

    def test_warns_at_threshold(self, tmp_path: Path) -> None:
        from wiki.project import check_resolver_recommendation

        _seed_conventionful_dirs(tmp_path, [".context", ".plans", ".designs"])
        issues = check_resolver_recommendation(tmp_path)
        assert len(issues) == 1
        assert issues[0]["severity"] == "warn"
        assert issues[0]["file"] == "RESOLVER.md"
        assert "/build:build-resolver" in issues[0]["issue"]

    def test_ignores_dir_with_only_one_frontmatter_file(self, tmp_path: Path) -> None:
        from wiki.project import check_resolver_recommendation

        # Three dirs but one only has a single frontmatter file → 2 qualify, no warn
        _seed_conventionful_dirs(tmp_path, [".context", ".plans"])
        thin = tmp_path / ".designs"
        thin.mkdir()
        (thin / "lone.design.md").write_text(_md("Lone"))
        assert check_resolver_recommendation(tmp_path) == []

    def test_ignores_files_without_frontmatter(self, tmp_path: Path) -> None:
        from wiki.project import check_resolver_recommendation

        # Three dirs but the files have no frontmatter → none qualify, no warn
        for name in ("notes", "drafts", "ideas"):
            d = tmp_path / name
            d.mkdir()
            (d / "a.md").write_text("# Plain markdown\n\nNo frontmatter here.\n")
            (d / "b.md").write_text("# Another\n\nAlso plain.\n")
        assert check_resolver_recommendation(tmp_path) == []

    def test_accepts_generic_naming(self, tmp_path: Path) -> None:
        from wiki.project import check_resolver_recommendation

        # Frontmatter-bearing files with arbitrary names — no canonical
        # suffixes — should still trigger the warning.
        for name in ("notebooks", "specs", "guides"):
            d = tmp_path / name
            d.mkdir()
            (d / "first.md").write_text(_md("First"))
            (d / "second.md").write_text(_md("Second"))
        issues = check_resolver_recommendation(tmp_path)
        assert len(issues) == 1
        assert issues[0]["severity"] == "warn"

    def test_ignores_ambient_dirs(self, tmp_path: Path) -> None:
        from wiki.project import check_resolver_recommendation

        for name in (".git", "node_modules", ".venv"):
            d = tmp_path / name
            d.mkdir()
            (d / "a.context.md").write_text(_md("A"))
            (d / "b.context.md").write_text(_md("B"))
        assert check_resolver_recommendation(tmp_path) == []

    def test_check_project_files_includes_recommendation(self, tmp_path: Path) -> None:
        from wiki.project import check_project_files

        _seed_conventionful_dirs(tmp_path, [".context", ".plans", ".designs"])
        issues = check_project_files(tmp_path)
        resolver_issues = [i for i in issues if i["file"] == "RESOLVER.md"]
        assert len(resolver_issues) == 1


# ── validate_file ──────────────────────────────────────────────


class TestValidateFile:
    def test_valid_file(self, tmp_path: Path) -> None:
        from wiki.project import validate_file

        md_file = tmp_path / "docs" / "context" / "testing" / "unit-tests.md"
        md_file.parent.mkdir(parents=True)
        md_file.write_text(_md("Unit Tests", "Guide to unit tests"))

        issues = validate_file(md_file, tmp_path, verify_urls=False)
        assert issues == []

    def test_file_without_frontmatter(self, tmp_path: Path) -> None:
        from wiki.project import validate_file

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
        from wiki.project import validate_project

        # Set up a document under docs/
        area = tmp_path / "docs" / "context" / "testing"
        area.mkdir(parents=True)
        topic = area / "unit-tests.md"
        topic.write_text(_md("Unit Tests", "Guide to unit tests"))
        # Create AGENTS.md with managed-section markers and CLAUDE.md with @AGENTS.md
        (tmp_path / "AGENTS.md").write_text(
            "# Agents\n\n<!-- wiki:begin -->\nmanaged\n<!-- wiki:end -->\n"
        )
        (tmp_path / "CLAUDE.md").write_text(
            "# Project\n\n@AGENTS.md\n"
        )

        issues = validate_project(tmp_path, verify_urls=False)
        assert issues == []

    def test_discovers_docs_outside_docs_dir(self, tmp_path: Path) -> None:
        """validate_project finds documents anywhere in the tree."""
        from wiki.project import validate_project

        # Put a research doc outside docs/
        research = tmp_path / "project-x" / "study.research.md"
        research.parent.mkdir(parents=True)
        research.write_text(_md(
            "Study", "A research study",
            type="research",
            sources=["https://example.com"],
        ))
        (tmp_path / "AGENTS.md").write_text(
            "# Agents\n\n<!-- wiki:begin -->\nmanaged\n<!-- wiki:end -->\n"
        )
        (tmp_path / "CLAUDE.md").write_text("# Project\n\n@AGENTS.md\n")

        issues = validate_project(tmp_path, verify_urls=False)
        # Should find the doc with no frontmatter errors
        frontmatter_issues = [
            i for i in issues if "frontmatter" in i["issue"].lower()
        ]
        assert frontmatter_issues == []


# ── Compound suffix integration ───────────────────────────────


class TestCompoundSuffixValidation:
    def test_validate_file_with_compound_suffix(self, tmp_path: Path) -> None:
        """validate_file works on compound suffix files."""
        from wiki.project import validate_file

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
        from wiki.project import validate_file

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
        from wiki.project import validate_file

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
        from wiki.document import parse_document

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
        from wiki.project import validate_project

        # Set up research area with a compound suffix file
        research_dir = tmp_path / "docs" / "research"
        research_dir.mkdir(parents=True)
        (research_dir / "api.research.md").write_text(_md(
            "API Research", "Research on APIs",
            type="research",
            sources=["https://example.com/api"],
        ))
        # Create AGENTS.md and CLAUDE.md
        (tmp_path / "AGENTS.md").write_text(
            "# Agents\n\n<!-- wiki:begin -->\nmanaged\n<!-- wiki:end -->\n"
        )
        (tmp_path / "CLAUDE.md").write_text("# Project\n\n@AGENTS.md\n")

        issues = validate_project(tmp_path, verify_urls=False)
        assert issues == []

