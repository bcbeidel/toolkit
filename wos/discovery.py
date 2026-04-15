"""Document discovery via project tree walking.

Walks the project tree from root, skipping hidden directories and known
build/tooling directories, and identifies WOS-managed documents by
frontmatter presence.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import List, Optional

from wos.document import Document, parse_document

# Directories excluded from _index.md generation by default.
# These contain plugin/tooling files, not user content.
# Pass exclude_dirs=set() to discover_document_dirs() to include all.
INDEX_EXCLUDED_DIRS = frozenset({".agents", "scripts", "skills", "tests"})

# Directories always skipped during discovery — hidden dirs (starting with ".")
# are handled separately in _should_skip_dir().
_SKIP_DIRS = frozenset({
    "node_modules", "__pycache__", "venv", ".venv",
    "dist", "build", ".tox", ".mypy_cache", ".pytest_cache",
})


def _should_skip_dir(name: str) -> bool:
    """Return True if a directory should be excluded from discovery."""
    return name in _SKIP_DIRS or name.startswith(".")


# ── Document discovery ────────────────────────────────────────


def discover_documents(root: Path) -> List[Document]:
    """Walk the project tree and find all WOS-managed documents.

    A managed document is any ``.md`` file with valid WOS frontmatter
    (``name`` and ``description`` fields). ``_index.md`` files are
    excluded (they are generated artifacts).

    Skips hidden directories (starting with ```.```) and common build /
    tooling directories (``node_modules``, ``__pycache__``, etc.).

    Args:
        root: Project root directory.

    Returns:
        List of parsed Document instances, sorted by path.
    """
    documents: List[Document] = []

    for dirpath, dirnames, filenames in os.walk(root):
        # Filter out skipped directories in-place (prevents os.walk descent)
        dirnames[:] = sorted(d for d in dirnames if not _should_skip_dir(d))

        for filename in sorted(filenames):
            if not filename.endswith(".md") or filename == "_index.md":
                continue
            doc = _try_parse(Path(dirpath) / filename, root)
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


def filter_documents(
    root: Path,
    doc_type: str,
    subdir: str = "",
    status: str = "",
) -> tuple[str, List[Document]]:
    """Discover documents filtered by type, optional status, and optional subdir.

    Args:
        root: Project root directory.
        doc_type: Required document type (e.g. 'research', 'plan').
        subdir: Optional path prefix to restrict results (relative to root).
        status: Optional status value to filter on (e.g. 'executing').

    Returns:
        Tuple of (label, docs) where label is the scanned path string and
        docs is the filtered list of Document instances.
    """
    docs = discover_documents(root)
    docs = [d for d in docs if d.type == doc_type]
    if status:
        docs = [d for d in docs if d.status == status]
    if subdir:
        docs = [
            d for d in docs
            if d.path.startswith(subdir + "/") or d.path.startswith(subdir)
        ]
    label = os.path.join(str(root), subdir) if subdir else str(root)
    return label, docs


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
