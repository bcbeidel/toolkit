"""Typed file suffix utilities.

Extracts document type from compound markdown suffixes like
``foo.research.md`` → ``"research"``, and provides helpers for
markdown file discovery that recognize compound suffixes.

Known type suffixes: research, plan, design, context, prompt.
Files without a type suffix (plain ``.md``) return None.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

# Recognized document-type suffixes (the part before .md)
KNOWN_TYPE_SUFFIXES = frozenset({
    "research",
    "plan",
    "design",
    "context",
    "prompt",
})


def type_from_path(path: Path) -> Optional[str]:
    """Extract document type from a compound suffix.

    Examples:
        >>> type_from_path(Path("api-latency.research.md"))
        'research'
        >>> type_from_path(Path("2026-03-13-cross-platform.plan.md"))
        'plan'
        >>> type_from_path(Path("plain-document.md"))
        >>> type_from_path(Path("notes.txt"))

    Args:
        path: File path (only the name is inspected).

    Returns:
        The type string if a known type suffix is present, else None.
    """
    suffixes = path.suffixes  # e.g. ['.research', '.md'] or ['.md']
    if len(suffixes) >= 2 and suffixes[-1] == ".md":
        candidate = suffixes[-2].lstrip(".")  # '.research' → 'research'
        if candidate in KNOWN_TYPE_SUFFIXES:
            return candidate
    return None


def is_markdown(path: Path) -> bool:
    """Check if a file is a markdown file (plain or compound suffix).

    Recognizes both ``foo.md`` and ``foo.research.md``.

    Args:
        path: File path to check.

    Returns:
        True if the file ends with ``.md``.
    """
    return path.name.endswith(".md")


def stem_name(path: Path) -> str:
    """Get the base name without any .md or .type.md suffix.

    Examples:
        >>> stem_name(Path("api-latency.research.md"))
        'api-latency'
        >>> stem_name(Path("plain-document.md"))
        'plain-document'
        >>> stem_name(Path("2026-03-13-cross-platform.plan.md"))
        '2026-03-13-cross-platform'

    Args:
        path: File path.

    Returns:
        The filename with all markdown-related suffixes removed.
    """
    name = path.name
    if name.endswith(".md"):
        name = name[:-3]  # strip .md
    # Check if the remaining part ends with a known type suffix
    for suffix in KNOWN_TYPE_SUFFIXES:
        if name.endswith("." + suffix):
            name = name[:-(len(suffix) + 1)]
            break
    return name
