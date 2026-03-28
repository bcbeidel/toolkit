"""Document dataclass and frontmatter parser.

Provides a single Document dataclass representing any WOS document
(topic, overview, research, plan) and a parse_document() function
that extracts YAML frontmatter into structured fields.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

from wos.frontmatter import parse_frontmatter
from wos.suffix import type_from_path

# Fields that can live under ``metadata`` or at top level.
_METADATA_FIELDS = frozenset({
    "type", "sources", "related", "status", "created_at", "updated_at",
})


@dataclass
class Document:
    """A parsed WOS document with frontmatter metadata and body content."""

    path: str
    name: str
    description: str
    content: str
    type: Optional[str] = None
    sources: List[str] = field(default_factory=list)
    related: List[str] = field(default_factory=list)
    status: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


def _resolve(fm: dict, key: str, default: object = None) -> object:
    """Resolve a field from metadata (preferred) or top-level (fallback).

    Checks ``fm["metadata"][key]`` first, then ``fm[key]``.  Returns
    *default* if neither location has a non-None value.
    """
    meta = fm.get("metadata")
    if isinstance(meta, dict):
        val = meta.get(key)
        if val is not None:
            return val
    val = fm.get(key)
    if val is not None:
        return val
    return default


def parse_document(path: str, text: str) -> Document:
    """Parse a markdown document with YAML frontmatter.

    Extracts frontmatter between ``---`` delimiters. Known fields
    (name, description, type, sources, related) become Document
    attributes; unknown fields are ignored.

    Fields may appear at top level (flat format) or nested under a
    ``metadata`` map (Agent Skills superset format).  ``metadata``
    takes precedence when both are present.

    Args:
        path: File path for the document.
        text: Raw markdown text including frontmatter.

    Returns:
        A Document instance with parsed metadata and body content.

    Raises:
        ValueError: If frontmatter is missing, or required fields
            (name, description) are absent.
    """
    try:
        fm, content = parse_frontmatter(text)
    except ValueError as exc:
        raise ValueError(f"{path}: {exc}") from exc

    # ── Validate required fields (always top-level) ───────────
    if "name" not in fm:
        raise ValueError(f"{path}: frontmatter missing required field 'name'")
    if "description" not in fm:
        raise ValueError(
            f"{path}: frontmatter missing required field 'description'"
        )

    # ── Extract known fields ───────────────────────────────────
    name: str = str(fm["name"]) if fm["name"] is not None else ""
    description: str = str(fm["description"]) if fm["description"] is not None else ""
    doc_type: Optional[str] = _resolve(fm, "type")
    if not isinstance(doc_type, str) and doc_type is not None:
        doc_type = str(doc_type)
    if doc_type is None:
        doc_type = type_from_path(Path(path))
    sources: List[str] = _resolve(fm, "sources") or []
    related: List[str] = _resolve(fm, "related") or []
    status: Optional[str] = _resolve(fm, "status")
    if not isinstance(status, str) and status is not None:
        status = str(status)

    _VALID_STATUSES = {"draft", "approved", "executing", "completed", "abandoned"}
    if status is not None and status not in _VALID_STATUSES:
        raise ValueError(
            f"{path}: invalid status '{status}', "
            f"must be one of: {', '.join(sorted(_VALID_STATUSES))}"
        )

    created_at: Optional[str] = _resolve(fm, "created_at")
    if not isinstance(created_at, str) and created_at is not None:
        created_at = str(created_at)
    updated_at: Optional[str] = _resolve(fm, "updated_at")
    if not isinstance(updated_at, str) and updated_at is not None:
        updated_at = str(updated_at)

    return Document(
        path=path,
        name=name,
        description=description,
        content=content,
        type=doc_type,
        sources=sources,
        related=related,
        status=status,
        created_at=created_at,
        updated_at=updated_at,
    )
