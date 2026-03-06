"""Tests for wos/validators.py — per-file and project-wide validation checks."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

from wos.document import Document

# ── Helpers ─────────────────────────────────────────────────────


def _make_doc(**overrides) -> Document:
    """Build a minimal valid Document, applying overrides."""
    defaults = {
        "path": "docs/context/testing/unit-tests.md",
        "name": "Unit Tests",
        "description": "Guide to writing unit tests",
        "content": "# Unit Tests\n\nSome content.\n",
    }
    defaults.update(overrides)
    return Document(**defaults)


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


# ── check_frontmatter ──────────────────────────────────────────


class TestCheckFrontmatter:
    def test_valid_doc_no_issues(self) -> None:
        from wos.validators import check_frontmatter

        doc = _make_doc(
            path="docs/research/topic.md",
            name="Valid",
            description="A valid document",
        )
        issues = check_frontmatter(doc)
        assert issues == []

    def test_empty_name(self) -> None:
        from wos.validators import check_frontmatter

        doc = _make_doc(path="docs/research/topic.md", name="")
        issues = check_frontmatter(doc)
        assert len(issues) == 1
        assert issues[0]["severity"] == "fail"
        assert "name" in issues[0]["issue"].lower()
        assert issues[0]["file"] == doc.path

    def test_empty_description(self) -> None:
        from wos.validators import check_frontmatter

        doc = _make_doc(path="docs/research/topic.md", description="")
        issues = check_frontmatter(doc)
        assert len(issues) == 1
        assert issues[0]["severity"] == "fail"
        assert "description" in issues[0]["issue"].lower()
        assert issues[0]["file"] == doc.path

    def test_research_without_sources_fail(self) -> None:
        from wos.validators import check_frontmatter

        doc = _make_doc(type="research", sources=[])
        issues = check_frontmatter(doc)
        assert any(
            i["severity"] == "fail" and "sources" in i["issue"].lower()
            for i in issues
        )

    def test_research_with_sources_no_source_issue(self) -> None:
        from wos.validators import check_frontmatter

        doc = _make_doc(
            type="research",
            sources=["https://example.com/source"],
        )
        issues = check_frontmatter(doc)
        assert not any("sources" in i["issue"].lower() for i in issues)

    def test_non_research_without_sources_ok(self) -> None:
        from wos.validators import check_frontmatter

        doc = _make_doc(type="topic", sources=[])
        issues = check_frontmatter(doc)
        assert not any("sources" in i["issue"].lower() for i in issues)

    def test_dict_source_warns(self) -> None:
        from wos.validators import check_frontmatter

        doc = _make_doc(sources=[
            {"url": "https://example.com", "title": "A"},
        ])
        issues = check_frontmatter(doc)
        assert any(i["severity"] == "warn" for i in issues)
        assert any("dict" in i["issue"].lower() for i in issues)

    def test_context_file_without_related_warns(self) -> None:
        from wos.validators import check_frontmatter

        doc = _make_doc(
            path="docs/context/api/auth.md",
            related=[],
        )
        issues = check_frontmatter(doc)
        assert any(
            i["severity"] == "warn" and "related" in i["issue"].lower()
            for i in issues
        )

    def test_artifact_file_without_related_no_warn(self) -> None:
        from wos.validators import check_frontmatter

        doc = _make_doc(
            path="docs/research/topic.md",
            related=[],
        )
        issues = check_frontmatter(doc)
        assert not any("related" in i["issue"].lower() for i in issues)


# ── check_content ─────────────────────────────────────────────


class TestCheckContent:
    def test_short_context_file_no_warning(self) -> None:
        from wos.validators import check_content

        doc = _make_doc(
            path="docs/context/api/auth.md",
            content="Word " * 200,
        )
        issues = check_content(doc)
        assert issues == []

    def test_long_context_file_warns(self) -> None:
        from wos.validators import check_content

        doc = _make_doc(
            path="docs/context/api/auth.md",
            content="Word " * 900,
        )
        issues = check_content(doc)
        assert len(issues) == 1
        assert issues[0]["severity"] == "warn"
        assert "900" in issues[0]["issue"]

    def test_artifact_file_no_warning(self) -> None:
        from wos.validators import check_content

        doc = _make_doc(
            path="docs/research/topic.md",
            content="Word " * 2000,
        )
        issues = check_content(doc)
        assert issues == []

    def test_index_file_excluded(self) -> None:
        from wos.validators import check_content

        doc = _make_doc(
            path="docs/context/api/_index.md",
            content="Word " * 2000,
        )
        issues = check_content(doc)
        assert issues == []

    def test_custom_max_words(self) -> None:
        from wos.validators import check_content

        doc = _make_doc(
            path="docs/context/api/auth.md",
            content="Word " * 500,
        )
        issues = check_content(doc, max_words=400)
        assert len(issues) == 1

    def test_exactly_at_threshold_no_warning(self) -> None:
        from wos.validators import check_content

        doc = _make_doc(
            path="docs/context/api/auth.md",
            content="Word " * 800,
        )
        issues = check_content(doc)
        assert issues == []

    def test_below_min_words_warns(self) -> None:
        from wos.validators import check_content

        doc = _make_doc(
            path="docs/context/api/auth.md",
            content="Word " * 50,
        )
        issues = check_content(doc)
        assert len(issues) == 1
        assert issues[0]["severity"] == "warn"
        assert "50" in issues[0]["issue"]

    def test_above_min_words_no_warning(self) -> None:
        from wos.validators import check_content

        doc = _make_doc(
            path="docs/context/api/auth.md",
            content="Word " * 200,
        )
        issues = check_content(doc)
        assert issues == []

    def test_exactly_at_min_threshold_no_warning(self) -> None:
        from wos.validators import check_content

        doc = _make_doc(
            path="docs/context/api/auth.md",
            content="Word " * 100,
        )
        issues = check_content(doc)
        assert issues == []

    def test_custom_min_words(self) -> None:
        from wos.validators import check_content

        doc = _make_doc(
            path="docs/context/api/auth.md",
            content="Word " * 150,
        )
        issues = check_content(doc, min_words=200)
        assert len(issues) == 1

    def test_artifact_file_no_min_warning(self) -> None:
        from wos.validators import check_content

        doc = _make_doc(
            path="docs/research/topic.md",
            content="Word " * 10,
        )
        issues = check_content(doc)
        assert issues == []

    def test_index_file_excluded_from_min_check(self) -> None:
        from wos.validators import check_content

        doc = _make_doc(
            path="docs/context/api/_index.md",
            content="Word " * 10,
        )
        issues = check_content(doc)
        assert issues == []


# ── check_draft_markers ────────────────────────────────────────


class TestCheckDraftMarkers:
    def test_research_with_draft_marker_warns(self) -> None:
        from wos.validators import check_draft_markers

        doc = _make_doc(
            type="research",
            content="# Topic\n\n<!-- DRAFT -->\n\nSome content.\n",
        )
        issues = check_draft_markers(doc)
        assert len(issues) == 1
        assert issues[0]["severity"] == "warn"
        assert "DRAFT" in issues[0]["issue"]

    def test_research_without_draft_marker_clean(self) -> None:
        from wos.validators import check_draft_markers

        doc = _make_doc(
            type="research",
            content="# Topic\n\nFinal content.\n",
        )
        issues = check_draft_markers(doc)
        assert issues == []

    def test_non_research_with_draft_marker_clean(self) -> None:
        from wos.validators import check_draft_markers

        doc = _make_doc(
            type="reference",
            content="# Topic\n\n<!-- DRAFT -->\n\nSome content.\n",
        )
        issues = check_draft_markers(doc)
        assert issues == []


# ── check_source_urls ──────────────────────────────────────────


class TestCheckSourceUrls:
    def test_all_reachable(self) -> None:
        from wos.url_checker import UrlCheckResult
        from wos.validators import check_source_urls

        doc = _make_doc(sources=["https://example.com/a", "https://example.com/b"])

        mock_results = [
            UrlCheckResult(url="https://example.com/a", status=200, reachable=True),
            UrlCheckResult(url="https://example.com/b", status=200, reachable=True),
        ]
        with patch("wos.validators.check_urls", return_value=mock_results):
            issues = check_source_urls(doc)
        assert issues == []

    def test_unreachable_url(self) -> None:
        from wos.url_checker import UrlCheckResult
        from wos.validators import check_source_urls

        doc = _make_doc(sources=["https://example.com/missing"])

        mock_results = [
            UrlCheckResult(
                url="https://example.com/missing",
                status=404,
                reachable=False,
                reason="HTTP 404",
            ),
        ]
        with patch("wos.validators.check_urls", return_value=mock_results):
            issues = check_source_urls(doc)
        assert len(issues) == 1
        assert issues[0]["severity"] == "fail"
        assert "https://example.com/missing" in issues[0]["issue"]

    def test_403_downgraded_to_warn(self) -> None:
        from wos.url_checker import UrlCheckResult
        from wos.validators import check_source_urls

        doc = _make_doc(sources=["https://example.com/blocked"])

        mock_results = [
            UrlCheckResult(
                url="https://example.com/blocked",
                status=403,
                reachable=False,
                reason="HTTP 403",
            ),
        ]
        with patch("wos.validators.check_urls", return_value=mock_results):
            issues = check_source_urls(doc)
        assert len(issues) == 1
        assert issues[0]["severity"] == "warn"
        assert "403" in issues[0]["issue"]

    def test_429_downgraded_to_warn(self) -> None:
        from wos.url_checker import UrlCheckResult
        from wos.validators import check_source_urls

        doc = _make_doc(sources=["https://example.com/ratelimited"])

        mock_results = [
            UrlCheckResult(
                url="https://example.com/ratelimited",
                status=429,
                reachable=False,
                reason="HTTP 429",
            ),
        ]
        with patch("wos.validators.check_urls", return_value=mock_results):
            issues = check_source_urls(doc)
        assert len(issues) == 1
        assert issues[0]["severity"] == "warn"
        assert "429" in issues[0]["issue"]

    def test_404_remains_fail(self) -> None:
        from wos.url_checker import UrlCheckResult
        from wos.validators import check_source_urls

        doc = _make_doc(sources=["https://example.com/gone"])

        mock_results = [
            UrlCheckResult(
                url="https://example.com/gone",
                status=404,
                reachable=False,
                reason="HTTP 404",
            ),
        ]
        with patch("wos.validators.check_urls", return_value=mock_results):
            issues = check_source_urls(doc)
        assert len(issues) == 1
        assert issues[0]["severity"] == "fail"

    def test_connection_error_remains_fail(self) -> None:
        from wos.url_checker import UrlCheckResult
        from wos.validators import check_source_urls

        doc = _make_doc(sources=["https://example.com/error"])

        mock_results = [
            UrlCheckResult(
                url="https://example.com/error",
                status=0,
                reachable=False,
                reason="Connection refused",
            ),
        ]
        with patch("wos.validators.check_urls", return_value=mock_results):
            issues = check_source_urls(doc)
        assert len(issues) == 1
        assert issues[0]["severity"] == "fail"

    def test_no_sources_no_check_called(self) -> None:
        from wos.validators import check_source_urls

        doc = _make_doc(sources=[])

        with patch("wos.validators.check_urls") as mock_check:
            issues = check_source_urls(doc)
        mock_check.assert_not_called()
        assert issues == []

    def test_dict_format_sources(self) -> None:
        """Dict-format sources should be normalized to URL strings (#61)."""
        from wos.url_checker import UrlCheckResult
        from wos.validators import check_source_urls

        doc = _make_doc(sources=[
            {"url": "https://example.com/a", "title": "Source A"},
            {"url": "https://example.com/b", "title": "Source B"},
        ])

        mock_results = [
            UrlCheckResult(url="https://example.com/a", status=200, reachable=True),
            UrlCheckResult(url="https://example.com/b", status=200, reachable=True),
        ]
        with patch(
            "wos.validators.check_urls", return_value=mock_results,
        ) as mock_check:
            issues = check_source_urls(doc)
        # Should pass URL strings, not dicts
        mock_check.assert_called_once_with(
            ["https://example.com/a", "https://example.com/b"],
        )
        assert issues == []

    def test_mixed_format_sources(self) -> None:
        """Mix of plain URLs and dict-format sources should work (#61)."""
        from wos.url_checker import UrlCheckResult
        from wos.validators import check_source_urls

        doc = _make_doc(sources=[
            "https://example.com/plain",
            {"url": "https://example.com/dict", "title": "Dict Source"},
        ])

        mock_results = [
            UrlCheckResult(url="https://example.com/plain", status=200, reachable=True),
            UrlCheckResult(url="https://example.com/dict", status=200, reachable=True),
        ]
        with patch(
            "wos.validators.check_urls", return_value=mock_results,
        ) as mock_check:
            issues = check_source_urls(doc)
        mock_check.assert_called_once_with(
            ["https://example.com/plain", "https://example.com/dict"],
        )
        assert issues == []


# ── check_related_paths ────────────────────────────────────────


class TestCheckRelatedPaths:
    def test_existing_paths_ok(self, tmp_path: Path) -> None:
        from wos.validators import check_related_paths

        # Create a file on disk
        related_file = tmp_path / "docs" / "context" / "api" / "auth.md"
        related_file.parent.mkdir(parents=True)
        related_file.write_text("# Auth\n")

        doc = _make_doc(related=["docs/context/api/auth.md"])
        issues = check_related_paths(doc, tmp_path)
        assert issues == []

    def test_missing_path_fail(self, tmp_path: Path) -> None:
        from wos.validators import check_related_paths

        doc = _make_doc(related=["docs/context/api/nonexistent.md"])
        issues = check_related_paths(doc, tmp_path)
        assert len(issues) == 1
        assert issues[0]["severity"] == "fail"
        assert "nonexistent.md" in issues[0]["issue"]

    def test_urls_skipped(self, tmp_path: Path) -> None:
        from wos.validators import check_related_paths

        doc = _make_doc(
            related=[
                "https://github.com/org/repo/issues/42",
                "http://example.com/page",
            ]
        )
        issues = check_related_paths(doc, tmp_path)
        assert issues == []

    def test_no_related_no_issues(self, tmp_path: Path) -> None:
        from wos.validators import check_related_paths

        doc = _make_doc(related=[])
        issues = check_related_paths(doc, tmp_path)
        assert issues == []


# ── check_all_indexes ──────────────────────────────────────────


class TestCheckAllIndexes:
    def test_synced_index_with_preamble(self, tmp_path: Path) -> None:
        from wos.index import generate_index
        from wos.validators import check_all_indexes

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
        from wos.validators import check_all_indexes

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
        from wos.validators import check_all_indexes

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
        from wos.validators import check_all_indexes

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
        from wos.validators import check_project_files

        issues = check_project_files(tmp_path)
        agents_issues = [i for i in issues if i["file"] == "AGENTS.md"]
        assert any("No AGENTS.md" in i["issue"] for i in agents_issues)

    def test_agents_md_without_markers_warns(self, tmp_path: Path) -> None:
        from wos.validators import check_project_files

        (tmp_path / "AGENTS.md").write_text("# Agents\n\nSome content.\n")
        issues = check_project_files(tmp_path)
        agents_issues = [i for i in issues if i["file"] == "AGENTS.md"]
        assert any("markers" in i["issue"].lower() for i in agents_issues)

    def test_agents_md_with_markers_clean(self, tmp_path: Path) -> None:
        from wos.validators import check_project_files

        (tmp_path / "AGENTS.md").write_text(
            "# Agents\n\n<!-- wos:begin -->\nWOS content\n<!-- wos:end -->\n"
        )
        issues = check_project_files(tmp_path)
        agents_issues = [i for i in issues if i["file"] == "AGENTS.md"]
        assert agents_issues == []

    def test_no_claude_md_warns(self, tmp_path: Path) -> None:
        from wos.validators import check_project_files

        issues = check_project_files(tmp_path)
        claude_issues = [i for i in issues if i["file"] == "CLAUDE.md"]
        assert any("No CLAUDE.md" in i["issue"] for i in claude_issues)

    def test_claude_md_without_agents_ref_warns(self, tmp_path: Path) -> None:
        from wos.validators import check_project_files

        (tmp_path / "CLAUDE.md").write_text("# Project\n\nSome instructions.\n")
        issues = check_project_files(tmp_path)
        claude_issues = [i for i in issues if i["file"] == "CLAUDE.md"]
        assert any("@AGENTS.md" in i["issue"] for i in claude_issues)

    def test_claude_md_with_agents_ref_clean(self, tmp_path: Path) -> None:
        from wos.validators import check_project_files

        (tmp_path / "CLAUDE.md").write_text(
            "# Project\n\n@AGENTS.md\n\nSome instructions.\n"
        )
        issues = check_project_files(tmp_path)
        claude_issues = [i for i in issues if i["file"] == "CLAUDE.md"]
        assert claude_issues == []


# ── validate_file ──────────────────────────────────────────────


class TestValidateFile:
    def test_valid_file(self, tmp_path: Path) -> None:
        from wos.validators import validate_file

        md_file = tmp_path / "docs" / "context" / "testing" / "unit-tests.md"
        md_file.parent.mkdir(parents=True)
        md_file.write_text(_md("Unit Tests", "Guide to unit tests"))

        issues = validate_file(md_file, tmp_path, verify_urls=False)
        assert issues == []

    def test_file_without_frontmatter(self, tmp_path: Path) -> None:
        from wos.validators import validate_file

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
        from wos.validators import validate_project

        # Set up context area under docs/
        area = tmp_path / "docs" / "context" / "testing"
        area.mkdir(parents=True)
        topic = area / "unit-tests.md"
        topic.write_text(_md("Unit Tests", "Guide to unit tests"))
        # Create synced index with preambles for the area
        (area / "_index.md").write_text(
            generate_index(area, preamble="Testing area.")
        )
        # Create synced index with preamble for context root
        context_dir = tmp_path / "docs" / "context"
        (context_dir / "_index.md").write_text(
            generate_index(context_dir, preamble="All context.")
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
