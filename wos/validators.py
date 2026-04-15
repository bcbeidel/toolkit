"""Backwards-compatible re-exports from wos.project.

All project-level logic has moved to wos.project. This module
re-exports the public API so existing callers (scripts/lint.py,
tests) continue to work without modification.
"""

from __future__ import annotations

from pathlib import Path
from typing import List, Optional

from wos.project import Project, check_all_indexes, validate_file  # noqa: F401


def check_project_files(root: Path) -> List[dict]:
    """Backwards-compatible wrapper — delegates to Project.check_project_files()."""
    return Project(root).check_project_files()


def validate_project(
    root: Path,
    verify_urls: bool = True,
    context_max_words: int = 800,
    context_min_words: int = 100,
    exclude_dirs: Optional[frozenset] = None,
) -> List[dict]:
    """Backwards-compatible wrapper — delegates to Project.validate()."""
    return Project(root).validate(
        verify_urls=verify_urls,
        context_max_words=context_max_words,
        context_min_words=context_min_words,
        exclude_dirs=exclude_dirs,
    )
