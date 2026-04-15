"""Document base class for WOS documents.

Provides a Document base class. Document.parse() is the single factory —
it routes to the right subclass based on frontmatter type and file suffix
using lazy imports to avoid circular dependencies. parse_document is kept
as a module-level alias for backwards compatibility.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

from wos.frontmatter import parse_frontmatter
from wos.suffix import type_from_path

_VALID_STATUSES = frozenset({
    "draft", "approved", "executing", "completed", "abandoned"
})
_KNOWN_KEYS = frozenset({"name", "description", "type", "sources", "related", "status"})


# ── Base class ────────────────────────────────────────────────────


@dataclass
class Document:
    """Base class for all WOS documents.

    Holds common frontmatter fields and implements base validation
    (non-empty name/description, related paths exist on disk).
    Typed subclasses add structured fields and type-specific validation.
    """

    path: str
    name: str
    description: str
    content: str
    type: Optional[str] = None
    sources: List[str] = field(default_factory=list)
    related: List[str] = field(default_factory=list)
    status: Optional[str] = None
    meta: dict = field(default_factory=dict)

    # ── Properties ────────────────────────────────────────────────

    @property
    def word_count(self) -> int:
        """Number of words in body content."""
        return len(self.content.split())

    def has_section(self, keyword: str) -> bool:
        """Return True if any heading line contains keyword (case-insensitive)."""
        for line in self.content.splitlines():
            stripped = line.strip()
            heading_text = stripped.lstrip("#").strip().lower()
            if stripped.startswith("#") and keyword in heading_text:
                return True
        return False

    # ── Validation ────────────────────────────────────────────────

    def issues(self, root: Path) -> List[dict]:
        """Return validation issues common to all documents.

        Checks that name and description are non-empty, and that all
        local file paths in ``related`` exist on disk.

        Args:
            root: Project root directory for resolving relative paths.

        Returns:
            List of issue dicts with keys: file, issue, severity.
        """
        result: List[dict] = []

        if not self.name or not self.name.strip():
            result.append({
                "file": self.path,
                "issue": "Frontmatter 'name' is empty",
                "severity": "fail",
            })
        if not self.description or not self.description.strip():
            result.append({
                "file": self.path,
                "issue": "Frontmatter 'description' is empty",
                "severity": "fail",
            })

        for rel in self.related:
            if rel.startswith("http://") or rel.startswith("https://"):
                continue
            if not (root / rel).exists():
                result.append({
                    "file": self.path,
                    "issue": f"Related path does not exist: {rel}",
                    "severity": "fail",
                })

        return result

    def is_valid(self, root: Path) -> bool:
        """Return True if issues() contains no fail-severity entries.

        Args:
            root: Project root directory.

        Returns:
            True if the document has no fail-severity issues.
        """
        return not any(i["severity"] == "fail" for i in self.issues(root))

    # ── Factory ───────────────────────────────────────────────────

    @classmethod
    def parse(cls, path: str, text: str) -> Document:
        """Parse a markdown document and return the appropriate subclass.

        Extracts YAML frontmatter between ``---`` delimiters. Routes to
        ResearchDocument, PlanDocument, ChainDocument, or WikiDocument
        based on the resolved type. Unknown types return a base Document.

        Args:
            path: File path for the document (used in error messages).
            text: Raw markdown text including frontmatter.

        Returns:
            A Document instance (or typed subclass) with parsed metadata.

        Raises:
            ValueError: If frontmatter is missing, required fields are
                absent, or status is not a recognised value.
        """
        try:
            fm, content = parse_frontmatter(text)
        except ValueError as exc:
            raise ValueError(f"{path}: {exc}") from exc

        if "name" not in fm:
            raise ValueError(f"{path}: frontmatter missing required field 'name'")
        if "description" not in fm:
            raise ValueError(
                f"{path}: frontmatter missing required field 'description'"
            )

        name: str = str(fm["name"]) if fm["name"] is not None else ""
        description: str = (
            str(fm["description"]) if fm["description"] is not None else ""
        )
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

        if status is not None and status not in _VALID_STATUSES:
            raise ValueError(
                f"{path}: invalid status '{status}', "
                f"must be one of: {', '.join(sorted(_VALID_STATUSES))}"
            )

        meta = {k: v for k, v in fm.items() if k not in _KNOWN_KEYS}

        kwargs = dict(
            path=path,
            name=name,
            description=description,
            content=content,
            type=doc_type,
            sources=sources,
            related=related,
            status=status,
            meta=meta,
        )

        if doc_type == "research":
            from wos.research import ResearchDocument
            return ResearchDocument(**kwargs)
        if doc_type == "plan":
            from wos.plan import PlanDocument
            return PlanDocument(**kwargs)
        if doc_type == "context":
            from wos.context import ContextDocument
            return ContextDocument(**kwargs)
        if doc_type == "chain":
            from wos.chain import ChainDocument
            return ChainDocument(**kwargs)
        if doc_type == "wiki":
            from wos.wiki import WikiDocument
            return WikiDocument(**kwargs)
        return Document(**kwargs)


# ── Module-level alias ─────────────────────────────────────────────

#: Backwards-compatible alias — prefer Document.parse() in new code.
parse_document = Document.parse
