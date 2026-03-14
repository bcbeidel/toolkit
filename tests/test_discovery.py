"""Tests for wos.discovery — tree walking and document detection."""

from __future__ import annotations

from pathlib import Path

from wos.discovery import (
    _GitignorePattern,
    discover_document_dirs,
    discover_documents,
    is_ignored,
    load_gitignore,
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


# ── Gitignore parsing ────────────────────────────────────────


class TestLoadGitignore:
    def test_no_gitignore(self, tmp_path: Path) -> None:
        patterns = load_gitignore(tmp_path)
        assert patterns == []

    def test_basic_globs(self, tmp_path: Path) -> None:
        (tmp_path / ".gitignore").write_text("*.pyc\nbuild/\n")
        patterns = load_gitignore(tmp_path)
        assert len(patterns) == 2
        assert patterns[0].pattern == "*.pyc"
        assert not patterns[0].negated
        assert not patterns[0].dir_only
        assert patterns[1].pattern == "build"
        assert patterns[1].dir_only

    def test_negation(self, tmp_path: Path) -> None:
        (tmp_path / ".gitignore").write_text("*.md\n!keep.md\n")
        patterns = load_gitignore(tmp_path)
        assert len(patterns) == 2
        assert not patterns[0].negated
        assert patterns[1].negated
        assert patterns[1].pattern == "keep.md"

    def test_comments_and_blank_lines(self, tmp_path: Path) -> None:
        (tmp_path / ".gitignore").write_text("# comment\n\n*.pyc\n  \n")
        patterns = load_gitignore(tmp_path)
        assert len(patterns) == 1
        assert patterns[0].pattern == "*.pyc"


# ── is_ignored ────────────────────────────────────────────────


class TestIsIgnored:
    def test_git_dir_always_ignored(self, tmp_path: Path) -> None:
        git_dir = tmp_path / ".git"
        git_dir.mkdir()
        assert is_ignored(git_dir, tmp_path, [])

    def test_git_subpath_always_ignored(self, tmp_path: Path) -> None:
        git_path = tmp_path / ".git" / "objects"
        git_path.mkdir(parents=True)
        assert is_ignored(git_path, tmp_path, [])

    def test_glob_pattern_matches_file(self, tmp_path: Path) -> None:
        patterns = [_GitignorePattern("*.pyc", negated=False, dir_only=False)]
        f = tmp_path / "module.pyc"
        f.touch()
        assert is_ignored(f, tmp_path, patterns)

    def test_glob_pattern_no_match(self, tmp_path: Path) -> None:
        patterns = [_GitignorePattern("*.pyc", negated=False, dir_only=False)]
        f = tmp_path / "module.py"
        f.touch()
        assert not is_ignored(f, tmp_path, patterns)

    def test_negation_overrides(self, tmp_path: Path) -> None:
        patterns = [
            _GitignorePattern("*.md", negated=False, dir_only=False),
            _GitignorePattern("keep.md", negated=True, dir_only=False),
        ]
        ignored = tmp_path / "notes.md"
        ignored.touch()
        kept = tmp_path / "keep.md"
        kept.touch()
        assert is_ignored(ignored, tmp_path, patterns)
        assert not is_ignored(kept, tmp_path, patterns)

    def test_dir_only_pattern(self, tmp_path: Path) -> None:
        patterns = [_GitignorePattern("build", negated=False, dir_only=True)]
        build_dir = tmp_path / "build"
        build_dir.mkdir()
        # File inside build dir
        f = tmp_path / "build" / "output.md"
        f.touch()
        assert is_ignored(build_dir, tmp_path, patterns)
        assert is_ignored(f, tmp_path, patterns)

    def test_nested_component_match(self, tmp_path: Path) -> None:
        patterns = [_GitignorePattern("node_modules", negated=False, dir_only=False)]
        nested = tmp_path / "frontend" / "node_modules" / "pkg" / "readme.md"
        nested.parent.mkdir(parents=True)
        nested.touch()
        assert is_ignored(nested, tmp_path, patterns)


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

    def test_respects_gitignore(self, tmp_path: Path) -> None:
        (tmp_path / ".gitignore").write_text("ignored/\n")
        _write_md(tmp_path / "visible.md", "Visible", "Should be found")
        ignored_dir = tmp_path / "ignored"
        _write_md(ignored_dir / "hidden.md", "Hidden", "Should be ignored")
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
