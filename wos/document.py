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

# Known frontmatter fields extracted into Document attributes.
_KNOWN_FIELDS = {
    "name", "description", "type", "sources", "related", "status",
    "created_at", "updated_at",
}


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


def parse_document(path: str, text: str) -> Document:
    """Parse a markdown document with YAML frontmatter.

    Extracts frontmatter between ``---`` delimiters. Known fields
    (name, description, type, sources, related) become Document
    attributes; unknown fields are ignored.

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

    # ── Validate required fields ───────────────────────────────
    if "name" not in fm:
        raise ValueError(f"{path}: frontmatter missing required field 'name'")
    if "description" not in fm:
        raise ValueError(
            f"{path}: frontmatter missing required field 'description'"
        )

    # ── Extract known fields ───────────────────────────────────
    name: str = str(fm["name"]) if fm["name"] is not None else ""
    description: str = str(fm["description"]) if fm["description"] is not None else ""
    doc_type: Optional[str] = fm.get("type")
    if not isinstance(doc_type, str) and doc_type is not None:
        doc_type = str(doc_type)
    if doc_type is None:
        doc_type = type_from_path(Path(path))
    sources: List[str] = fm.get("sources") or []
    related: List[str] = fm.get("related") or []
    status: Optional[str] = fm.get("status")
    if not isinstance(status, str) and status is not None:
        status = str(status)

    _VALID_STATUSES = {"draft", "approved", "executing", "completed", "abandoned"}
    if status is not None and status not in _VALID_STATUSES:
        raise ValueError(
            f"{path}: invalid status '{status}', "
            f"must be one of: {', '.join(sorted(_VALID_STATUSES))}"
        )

    created_at: Optional[str] = fm.get("created_at")
    if not isinstance(created_at, str) and created_at is not None:
        created_at = str(created_at)
    updated_at: Optional[str] = fm.get("updated_at")
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
