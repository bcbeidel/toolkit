"""Tests for wos.discovery — tree walking and document detection."""

from __future__ import annotations

from pathlib import Path

from wos.discovery import (
    _should_skip_dir,
    discover_document_dirs,
    discover_documents,
)

# ── Helper ────────────────────────────────────────────────────


def _write_md(path: Path, name: str, desc: str, extra: str = "") -> None:
    """Write a minimal WOS markdown file with frontmatter."""
    fm = f"---\nname: {name}\ndescription: {desc}\n{extra}---\n\nBody text.\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(fm, encoding="utf-8")


def _write_plain(path: Path, content: str = "no frontmatter here\n") -> None:
    """Write a plain markdown file without frontmatter."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


# ── _should_skip_dir ──────────────────────────────────────────


class TestShouldSkipDir:
    def test_hidden_dirs_skipped(self) -> None:
        assert _should_skip_dir(".git")
        assert _should_skip_dir(".venv")
        assert _should_skip_dir(".mypy_cache")

    def test_known_build_dirs_skipped(self) -> None:
        assert _should_skip_dir("node_modules")
        assert _should_skip_dir("__pycache__")
        assert _should_skip_dir("venv")
        assert _should_skip_dir("build")
        assert _should_skip_dir("dist")

    def test_normal_dirs_not_skipped(self) -> None:
        assert not _should_skip_dir("docs")
        assert not _should_skip_dir("src")
        assert not _should_skip_dir("research")


# ── discover_documents ────────────────────────────────────────


class TestDiscoverDocuments:
    def test_finds_frontmatter_docs(self, tmp_path: Path) -> None:
        _write_md(tmp_path / "docs" / "intro.md", "Intro", "An introduction")
        _write_md(tmp_path / "notes" / "api.md", "API", "API docs")
        docs = discover_documents(tmp_path)
        assert len(docs) == 2
        paths = {d.path for d in docs}
        assert "docs/intro.md" in paths
        assert "notes/api.md" in paths

    def test_skips_no_frontmatter(self, tmp_path: Path) -> None:
        _write_md(tmp_path / "valid.md", "Valid", "Has frontmatter")
        _write_plain(tmp_path / "plain.md")
        docs = discover_documents(tmp_path)
        assert len(docs) == 1
        assert docs[0].name == "Valid"

    def test_skips_index_files(self, tmp_path: Path) -> None:
        _write_md(tmp_path / "docs" / "_index.md", "Index", "Auto-generated")
        _write_md(tmp_path / "docs" / "real.md", "Real", "A real doc")
        docs = discover_documents(tmp_path)
        assert len(docs) == 1
        assert docs[0].name == "Real"

    def test_skips_node_modules(self, tmp_path: Path) -> None:
        _write_md(tmp_path / "visible.md", "Visible", "Should be found")
        _write_md(tmp_path / "node_modules" / "pkg" / "readme.md", "Pkg", "Hidden")
        docs = discover_documents(tmp_path)
        assert len(docs) == 1
        assert docs[0].name == "Visible"

    def test_skips_git_dir(self, tmp_path: Path) -> None:
        git_dir = tmp_path / ".git"
        _write_md(git_dir / "internal.md", "Git", "Internal git file")
        _write_md(tmp_path / "project.md", "Project", "A project doc")
        docs = discover_documents(tmp_path)
        assert len(docs) == 1
        assert docs[0].name == "Project"

    def test_type_from_suffix(self, tmp_path: Path) -> None:
        _write_md(tmp_path / "feature.plan.md", "Feature Plan", "A plan")
        docs = discover_documents(tmp_path)
        assert len(docs) == 1
        assert docs[0].type == "plan"

    def test_type_from_frontmatter(self, tmp_path: Path) -> None:
        _write_md(
            tmp_path / "study.md", "Study", "A study",
            extra="type: research\nsources:\n  - https://example.com\n",
        )
        docs = discover_documents(tmp_path)
        assert len(docs) == 1
        assert docs[0].type == "research"

    def test_frontmatter_type_wins_over_suffix(self, tmp_path: Path) -> None:
        _write_md(
            tmp_path / "notes.plan.md", "Notes", "Has plan suffix",
            extra="type: context\n",
        )
        docs = discover_documents(tmp_path)
        assert len(docs) == 1
        assert docs[0].type == "context"

    def test_empty_project(self, tmp_path: Path) -> None:
        docs = discover_documents(tmp_path)
        assert docs == []

    def test_no_gitignore(self, tmp_path: Path) -> None:
        _write_md(tmp_path / "doc.md", "Doc", "A document")
        docs = discover_documents(tmp_path)
        assert len(docs) == 1


# ── discover_document_dirs ────────────────────────────────────


class TestDiscoverDocumentDirs:
    def test_returns_dirs_with_docs(self, tmp_path: Path) -> None:
        _write_md(tmp_path / "docs" / "intro.md", "Intro", "An intro")
        _write_md(tmp_path / "notes" / "api.md", "API", "API docs")
        _write_md(tmp_path / "root.md", "Root", "Root doc")
        dirs = discover_document_dirs(tmp_path)
        rel_dirs = [str(d.relative_to(tmp_path)) for d in dirs]
        assert "." in rel_dirs
        assert "docs" in rel_dirs
        assert "notes" in rel_dirs

    def test_empty_project(self, tmp_path: Path) -> None:
        dirs = discover_document_dirs(tmp_path)
        assert dirs == []

    def test_skips_dirs_without_managed_docs(self, tmp_path: Path) -> None:
        _write_plain(tmp_path / "random" / "notes.md")
        _write_md(tmp_path / "docs" / "real.md", "Real", "A real doc")
        dirs = discover_document_dirs(tmp_path)
        rel_dirs = [str(d.relative_to(tmp_path)) for d in dirs]
        assert "docs" in rel_dirs
        assert "random" not in rel_dirs
