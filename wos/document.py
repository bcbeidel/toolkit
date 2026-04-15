"""Document base class for WOS documents.

Provides a Document base class. Document.parse() is the single factory —
it routes to the right subclass based on frontmatter type and file suffix
using a type registry. Subclasses self-register via @Document.register().
parse_document is kept as a module-level alias for backwards compatibility.
"""

from __future__ import annotations

import dataclasses
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import ClassVar, List, Optional

from wos.frontmatter import parse_frontmatter

_VALID_STATUSES = frozenset({
    "draft", "approved", "executing", "completed", "abandoned"
})
_KNOWN_KEYS = frozenset({"name", "description", "type", "sources", "related", "status"})

# Registry mapping type name strings to subclasses.
# Populated by @Document.register() decorators on subclasses.
_REGISTRY: dict[str, type[Document]] = {}


# ── Base class ────────────────────────────────────────────────────


@dataclass
class Document:
    """Base class for all WOS documents.

    Holds common frontmatter fields and implements base validation
    (non-empty name/description). Typed subclasses add structured fields
    and type-specific validation.

    The base class is aligned with the agentskills.io specification:
    required ``name`` and ``description`` fields, plus ``meta`` for
    arbitrary key-value pairs. Type-specific fields (sources, related,
    status) live on the subclasses that need them.
    """

    TYPE_SUFFIXES: ClassVar[frozenset] = frozenset({
        "research", "plan", "design", "prompt",
    })

    path: str
    name: str
    description: str
    content: str
    type: Optional[str] = None
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

    @staticmethod
    def type_from_path(path: Path) -> Optional[str]:
        """Extract document type from a compound suffix.

        Example: ``foo.research.md`` → ``'research'``.
        """
        suffixes = path.suffixes
        if len(suffixes) >= 2 and suffixes[-1] == ".md":
            candidate = suffixes[-2].lstrip(".")
            if candidate in Document.TYPE_SUFFIXES:
                return candidate
        return None

    # ── Validation ────────────────────────────────────────────────

    def issues(self, root: Path, **_: object) -> List[dict]:
        """Return validation issues common to all documents.

        Checks that name and description are non-empty.

        Args:
            root: Project root directory.
            **_: Absorbs extra kwargs so all callers can pass a uniform
                set of keyword arguments regardless of document type.

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

        return result

    def is_valid(self, root: Path, **_: object) -> bool:
        """Return True if issues() contains no fail-severity entries."""
        return not any(i["severity"] == "fail" for i in self.issues(root))

    # ── Scan ──────────────────────────────────────────────────────

    @classmethod
    def scan(
        cls,
        root: str,
        subdir: str = "",
        status: Optional[str] = None,
    ) -> List[Document]:
        """Walk the project tree and return documents of this type.

        Uses isinstance(doc, cls) to filter by type, so subclasses
        automatically restrict to their own type:
            Document.scan(root)                          # all documents
            ResearchDocument.scan(root)                  # research only
            PlanDocument.scan(root, status="executing")  # executing plans

        Skips hidden directories, common build/tool directories,
        ``_index.md`` files, and ``SKILL.md`` files.

        Args:
            root: Project root directory (string path).
            subdir: Optional subdirectory to restrict search (relative to root).
            status: Optional status value to filter on (e.g. 'executing').
                    Matched against ``doc.status`` via getattr (duck-typed).

        Returns:
            List of parsed Document instances (or subclass instances).
        """
        _SKIP = frozenset({
            "node_modules", "__pycache__", "venv", ".venv",
            "dist", "build", ".tox", ".mypy_cache", ".pytest_cache",
        })

        root_path = Path(root)
        search_path = root_path / subdir if subdir else root_path
        docs: List[Document] = []

        for dirpath, dirnames, filenames in os.walk(search_path):
            dirnames[:] = sorted(
                d for d in dirnames
                if not d.startswith(".") and d not in _SKIP
            )
            for filename in sorted(filenames):
                if not filename.endswith(".md"):
                    continue
                if filename in ("_index.md", "SKILL.md"):
                    continue
                path = Path(dirpath) / filename
                try:
                    rel = str(path.relative_to(root_path))
                    doc = Document.parse(rel, path.read_text(encoding="utf-8"))
                except (OSError, ValueError):
                    continue
                if not isinstance(doc, cls):
                    continue
                if status and getattr(doc, "status", None) != status:
                    continue
                docs.append(doc)

        return docs

    # ── Registry ──────────────────────────────────────────────────

    @classmethod
    def register(cls, *type_names: str):
        """Decorator: register a subclass for one or more type name strings."""
        def decorator(subclass: type[Document]) -> type[Document]:
            for name in type_names:
                _REGISTRY[name] = subclass
            return subclass
        return decorator

    # ── Factory ───────────────────────────────────────────────────

    @classmethod
    def parse(cls, path: str, text: str) -> Document:
        """Parse a markdown document and return the appropriate subclass.

        Extracts YAML frontmatter between ``---`` delimiters. Routes to
        the registered subclass based on the resolved type. Unknown types
        return a base Document.

        Each subclass declares only the fields it needs; parse() filters
        the extracted kwargs via dataclasses.fields() so subclasses never
        receive kwargs they don't accept.

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
            doc_type = cls.type_from_path(Path(path))

        # Filename-based routing: SKILL.md → "skill"
        if doc_type is None and Path(path).name == "SKILL.md":
            doc_type = "skill"

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

        all_kwargs = dict(
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

        subclass = _REGISTRY.get(doc_type, Document)

        # Filter to only the fields declared on the target subclass
        accepted = {f.name for f in dataclasses.fields(subclass)}
        filtered = {k: v for k, v in all_kwargs.items() if k in accepted}

        return subclass(**filtered)


# ── Module-level alias ─────────────────────────────────────────────

#: Backwards-compatible alias — prefer Document.parse() in new code.
parse_document = Document.parse
