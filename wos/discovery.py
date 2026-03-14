"""Document discovery via project tree walking.

Walks the project tree from root, respects .gitignore patterns,
and identifies WOS-managed documents by frontmatter presence.
"""

from __future__ import annotations

import fnmatch
import os
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

from wos.document import Document, parse_document

# Directories excluded from _index.md generation by default.
# These contain plugin/tooling files, not user content.
# Pass exclude_dirs=set() to discover_document_dirs() to include all.
INDEX_EXCLUDED_DIRS = frozenset({".agents", "scripts", "skills", "tests"})

# ── Gitignore parsing ─────────────────────────────────────────


@dataclass
class _GitignorePattern:
    """A parsed .gitignore pattern."""

    pattern: str
    negated: bool
    dir_only: bool


def load_gitignore(root: Path) -> List[_GitignorePattern]:
    """Read root/.gitignore and return parsed patterns.

    Returns empty list if no .gitignore exists.

    Args:
        root: Project root directory.

    Returns:
        List of parsed gitignore patterns.
    """
    gitignore_path = root / ".gitignore"
    if not gitignore_path.is_file():
        return []

    try:
        text = gitignore_path.read_text(encoding="utf-8")
    except OSError:
        return []

    patterns: List[_GitignorePattern] = []
    for line in text.splitlines():
        line = line.strip()
        # Skip blank lines and comments
        if not line or line.startswith("#"):
            continue

        negated = False
        if line.startswith("!"):
            negated = True
            line = line[1:]

        dir_only = False
        if line.endswith("/"):
            dir_only = True
            line = line.rstrip("/")

        if not line:
            continue

        patterns.append(_GitignorePattern(
            pattern=line,
            negated=negated,
            dir_only=dir_only,
        ))

    return patterns


def is_ignored(
    path: Path,
    root: Path,
    patterns: List[_GitignorePattern],
) -> bool:
    """Check if a path should be ignored based on gitignore patterns.

    Always ignores ``.git/`` regardless of patterns.

    Args:
        path: Absolute or relative path to check.
        root: Project root directory.
        patterns: Parsed gitignore patterns from load_gitignore().

    Returns:
        True if the path should be ignored.
    """
    try:
        rel = path.relative_to(root)
    except ValueError:
        return False

    rel_str = str(rel)
    parts = rel.parts

    # .git/ is always ignored
    if parts and parts[0] == ".git":
        return True

    is_dir = path.is_dir()

    # Check each path component individually against patterns
    # (gitignore patterns match at any directory level by default)
    matched = False
    for pat in patterns:
        if pat.dir_only and not is_dir:
            # Directory-only patterns only match directories, but we also
            # check if any parent component matches
            for i, part in enumerate(parts):
                if fnmatch.fnmatch(part, pat.pattern):
                    # This component is a directory (all but last are dirs)
                    if i < len(parts) - 1:
                        if pat.negated:
                            matched = False
                        else:
                            matched = True
                        break
            continue

        # Check if pattern contains a slash (path-based match)
        if "/" in pat.pattern:
            # Match against the full relative path
            if fnmatch.fnmatch(rel_str, pat.pattern):
                matched = not pat.negated
        else:
            # Match against any path component or the filename
            component_match = any(
                fnmatch.fnmatch(part, pat.pattern) for part in parts
            )
            if component_match:
                matched = not pat.negated

    return matched


# ── Document discovery ────────────────────────────────────────


def discover_documents(root: Path) -> List[Document]:
    """Walk the project tree and find all WOS-managed documents.

    A managed document is any ``.md`` file with valid WOS frontmatter
    (``name`` and ``description`` fields). ``_index.md`` files are
    excluded (they are generated artifacts).

    Respects ``.gitignore`` patterns and always skips ``.git/``.

    Args:
        root: Project root directory.

    Returns:
        List of parsed Document instances, sorted by path.
    """
    patterns = load_gitignore(root)
    documents: List[Document] = []

    for dirpath, dirnames, filenames in os.walk(root):
        dp = Path(dirpath)

        # Filter out ignored directories in-place (prevents os.walk descent)
        dirnames[:] = [
            d for d in dirnames
            if not is_ignored(dp / d, root, patterns)
        ]
        dirnames.sort()

        for filename in sorted(filenames):
            if not filename.endswith(".md"):
                continue
            if filename == "_index.md":
                continue

            file_path = dp / filename
            if is_ignored(file_path, root, patterns):
                continue

            doc = _try_parse(file_path, root)
            if doc is not None:
                documents.append(doc)

    return documents


def discover_document_dirs(
    root: Path,
    exclude_dirs: Optional[frozenset] = None,
) -> List[Path]:
    """Find directories containing at least one managed document.

    Directories whose top-level component matches an excluded name
    are filtered out by default. Pass ``exclude_dirs=frozenset()``
    to include all directories.

    Args:
        root: Project root directory.
        exclude_dirs: Top-level directory names to exclude.
            Defaults to INDEX_EXCLUDED_DIRS.

    Returns:
        Sorted list of absolute directory Paths containing managed documents.
    """
    if exclude_dirs is None:
        exclude_dirs = INDEX_EXCLUDED_DIRS

    docs = discover_documents(root)
    dirs: set[Path] = set()
    for doc in docs:
        d = (root / doc.path).parent
        try:
            rel = d.relative_to(root)
        except ValueError:
            dirs.add(d)
            continue
        if rel.parts and rel.parts[0] in exclude_dirs:
            continue
        dirs.add(d)
    return sorted(dirs)


def _try_parse(file_path: Path, root: Path) -> Optional[Document]:
    """Attempt to parse a file as a WOS document.

    Returns None if the file cannot be read, lacks frontmatter,
    or is missing required fields (name, description).
    """
    try:
        text = file_path.read_text(encoding="utf-8")
    except OSError:
        return None

    # Use relative path for document path
    try:
        rel_path = str(file_path.relative_to(root))
    except ValueError:
        rel_path = str(file_path)

    try:
        return parse_document(rel_path, text)
    except ValueError:
        return None
