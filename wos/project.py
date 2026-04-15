"""Project aggregate — validates an entire project tree.

Project is the aggregate root for project-level validation: it discovers
documents, runs per-document checks, validates index sync, and checks
project-level configuration files (AGENTS.md, CLAUDE.md).
"""

from __future__ import annotations

from pathlib import Path
from typing import List, Optional

from wos.document import parse_document
from wos.index import check_index_sync, extract_preamble

# ── Per-file helper ────────────────────────────────────────────────


def validate_file(
    path: Path,
    root: Path,
    verify_urls: bool = True,
    context_max_words: int = 800,
    context_min_words: int = 100,
) -> List[dict]:
    """Validate a single markdown file.

    Reads the file, parses it with parse_document(), then calls
    doc.issues(root) with a uniform set of keyword arguments.
    If parsing fails, returns a single parse-error issue.

    Args:
        path: Path to the .md file.
        root: Project root directory.
        verify_urls: If False, skip source URL reachability check.
        context_max_words: Upper word count threshold for context files.
        context_min_words: Lower word count threshold for context files.

    Returns:
        List of issue dicts.
    """
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        return [{
            "file": str(path),
            "issue": f"Cannot read file: {exc}",
            "severity": "fail",
        }]

    try:
        doc = parse_document(str(path), text)
    except ValueError as exc:
        return [{
            "file": str(path),
            "issue": f"Parse error: {exc}",
            "severity": "fail",
        }]

    return doc.issues(
        root,
        verify_urls=verify_urls,
        max_words=context_max_words,
        min_words=context_min_words,
    )


# ── Index checks (standalone, used by validators shim too) ────────


def check_all_indexes(directory: Path) -> List[dict]:
    """Recursively check all _index.md files under a directory.

    Walks all subdirectories and runs check_index_sync() on each.
    Also warns when an _index.md exists but has no preamble.

    Args:
        directory: Root directory to walk.

    Returns:
        List of issue dicts from all index checks.
    """
    issues: List[dict] = []
    if not directory.is_dir():
        return issues

    # Check the directory itself
    issues.extend(check_index_sync(directory))

    # WARN: index exists but has no preamble (area description)
    index_path = directory / "_index.md"
    if index_path.is_file() and extract_preamble(index_path) is None:
        issues.append({
            "file": str(index_path),
            "issue": "Index has no area description (preamble)",
            "severity": "warn",
        })

    # Recurse into subdirectories
    for entry in sorted(directory.iterdir()):
        if entry.is_dir():
            issues.extend(check_all_indexes(entry))

    return issues


# ── Project aggregate ──────────────────────────────────────────────


class Project:
    """Aggregate root for project-level validation."""

    def __init__(self, root: Path) -> None:
        self.root = root

    def validate(
        self,
        verify_urls: bool = True,
        context_max_words: int = 800,
        context_min_words: int = 100,
        exclude_dirs: Optional[frozenset] = None,
    ) -> List[dict]:
        """Validate all managed documents and project configuration.

        Discovers documents by walking the project tree and checking for
        valid frontmatter. Runs index sync checks on directories containing
        managed documents. Also checks project-level files (AGENTS.md,
        CLAUDE.md).

        Args:
            verify_urls: If False, skip source URL reachability checks.
            context_max_words: Upper word count threshold for context files.
            context_min_words: Lower word count threshold for context files.
            exclude_dirs: Top-level directory names to exclude from index
                checks. Defaults to INDEX_EXCLUDED_DIRS. Pass frozenset()
                to include all.

        Returns:
            List of all issue dicts found.
        """
        from wos.discovery import discover_document_dirs, discover_documents

        issues: List[dict] = []
        issues.extend(self.check_project_files())

        for doc in discover_documents(self.root):
            issues.extend(doc.issues(
                self.root,
                verify_urls=verify_urls,
                max_words=context_max_words,
                min_words=context_min_words,
            ))

        for directory in discover_document_dirs(self.root, exclude_dirs=exclude_dirs):
            issues.extend(self.check_indexes(directory))

        return issues

    def check_project_files(self) -> List[dict]:
        """Warn when AGENTS.md or CLAUDE.md are missing or misconfigured.

        Checks:
        - AGENTS.md missing
        - AGENTS.md exists but lacks ``<!-- wos:begin -->`` marker
        - CLAUDE.md missing
        - CLAUDE.md exists but doesn't reference ``@AGENTS.md``

        Returns:
            List of issue dicts. Empty if all checks pass.
        """
        issues: List[dict] = []
        root = self.root

        agents_path = root / "AGENTS.md"
        if not agents_path.is_file():
            issues.append({
                "file": "AGENTS.md",
                "issue": "No AGENTS.md found. Run /wos:setup to initialize.",
                "severity": "warn",
            })
        else:
            try:
                content = agents_path.read_text(encoding="utf-8")
            except OSError:
                content = ""
            if "<!-- wos:begin -->" not in content:
                issues.append({
                    "file": "AGENTS.md",
                    "issue": (
                        "AGENTS.md lacks WOS markers."
                        " Navigation updates won't work."
                    ),
                    "severity": "warn",
                })

        claude_path = root / "CLAUDE.md"
        if not claude_path.is_file():
            issues.append({
                "file": "CLAUDE.md",
                "issue": "No CLAUDE.md found. Run /wos:setup to initialize.",
                "severity": "warn",
            })
        else:
            try:
                content = claude_path.read_text(encoding="utf-8")
            except OSError:
                content = ""
            if "@AGENTS.md" not in content:
                issues.append({
                    "file": "CLAUDE.md",
                    "issue": (
                        "CLAUDE.md doesn't reference @AGENTS.md."
                        " Navigation may not load."
                    ),
                    "severity": "warn",
                })

        return issues

    def check_indexes(self, directory: Optional[Path] = None) -> List[dict]:
        """Recursively check _index.md files under a directory.

        Args:
            directory: Directory to check. Defaults to self.root.

        Returns:
            List of issue dicts from all index checks.
        """
        if directory is None:
            directory = self.root
        return check_all_indexes(directory)


# ── Module-level convenience functions ────────────────────────────


def check_project_files(root: Path) -> List[dict]:
    """Check AGENTS.md and CLAUDE.md configuration. See Project.check_project_files."""
    return Project(root).check_project_files()


def validate_project(
    root: Path,
    verify_urls: bool = True,
    context_max_words: int = 800,
    context_min_words: int = 100,
    exclude_dirs: Optional[frozenset] = None,
) -> List[dict]:
    """Validate all managed documents in a project. See Project.validate."""
    return Project(root).validate(
        verify_urls=verify_urls,
        context_max_words=context_max_words,
        context_min_words=context_min_words,
        exclude_dirs=exclude_dirs,
    )
