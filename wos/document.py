"""Document base class and typed subclasses for WOS documents.

Provides a Document base class and typed subclasses (ResearchDocument,
PlanDocument, ChainDocument, WikiDocument). Document.parse() is the
single factory — it routes to the right subclass based on frontmatter
type and file suffix. parse_document is kept as a module-level alias
for backwards compatibility.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

from wos.frontmatter import parse_frontmatter
from wos.suffix import type_from_path
from wos.url_checker import check_urls

_VALID_STATUSES = frozenset({
    "draft", "approved", "executing", "completed", "abandoned"
})
_KNOWN_KEYS = frozenset({"name", "description", "type", "sources", "related", "status"})

_TASK_RE = re.compile(
    r"^- \[([ xX])\] "
    r"(?:Task \d+:\s*)?"
    r"(.+?)"
    r"(?:\s*<!--\s*sha:(\w+)\s*-->)?"
    r"\s*$",
)


def _parse_tasks(content: str) -> List[dict]:
    """Extract top-level checkbox items from plan content.

    Parses ``- [ ] Task N: title`` and ``- [x] Task N: title <!-- sha:abc -->``
    patterns. Indented checkboxes are ignored. Parsing is restricted to
    headings containing "task" or "chunk" and stops at a "validation" heading.

    Returns:
        List of dicts with keys: index, title, completed, sha.
    """
    has_tasks_heading = any(
        "task" in line.lstrip("#").strip().lower()
        or "chunk" in line.lstrip("#").strip().lower()
        for line in content.split("\n")
        if line.strip().startswith("#")
    )

    tasks: List[dict] = []
    index = 0
    in_tasks = not has_tasks_heading
    for line in content.split("\n"):
        stripped = line.strip()
        if stripped.startswith("#") and has_tasks_heading:
            heading = stripped.lstrip("#").strip().lower()
            if "task" in heading or "chunk" in heading:
                in_tasks = True
            else:
                in_tasks = False
            continue
        if not in_tasks:
            continue
        match = _TASK_RE.match(line)
        if not match:
            continue
        index += 1
        tasks.append({
            "index": index,
            "title": match.group(2).strip(),
            "completed": match.group(1).lower() == "x",
            "sha": match.group(3),
        })

    return tasks


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
            return ResearchDocument(**kwargs)
        if doc_type == "plan":
            return PlanDocument(**kwargs)
        if doc_type == "context":
            return ContextDocument(**kwargs)
        if doc_type == "chain":
            from wos.chain import ChainDocument
            return ChainDocument(**kwargs)
        if doc_type == "wiki":
            from wos.wiki import WikiDocument
            return WikiDocument(**kwargs)
        return Document(**kwargs)


# ── Typed subclasses ───────────────────────────────────────────────


@dataclass
class ResearchDocument(Document):
    """A research document with source URL and draft-marker validation."""

    def issues(self, root: Path, verify_urls: bool = True) -> List[dict]:
        """Return base issues plus research-specific checks.

        Adds: sources required, sources-as-dicts warning, draft marker
        warning, and source URL reachability (fail/warn).

        Args:
            root: Project root directory.
            verify_urls: If False, skip HTTP reachability checks.

        Returns:
            List of issue dicts with keys: file, issue, severity.
        """
        result = super().issues(root)

        if not self.sources:
            result.append({
                "file": self.path,
                "issue": "Research document has no sources",
                "severity": "fail",
            })

        for idx, source in enumerate(self.sources):
            if isinstance(source, dict):
                result.append({
                    "file": self.path,
                    "issue": f"sources[{idx}] is a dict, expected a URL string",
                    "severity": "warn",
                })

        if "<!-- DRAFT -->" in self.content:
            result.append({
                "file": self.path,
                "issue": "Research document contains <!-- DRAFT --> marker",
                "severity": "warn",
            })

        if verify_urls and self.sources:
            urls = []
            for s in self.sources:
                if isinstance(s, dict):
                    urls.append(s.get("url", s.get("href", "")))
                else:
                    urls.append(str(s))
            for url_result in check_urls(urls):
                if not url_result.reachable:
                    if url_result.status in (403, 429):
                        result.append({
                            "file": self.path,
                            "issue": (
                                f"URL returned {url_result.status}"
                                f" (site may block automated checks):"
                                f" {url_result.url}"
                            ),
                            "severity": "warn",
                        })
                    else:
                        reason = (
                            f" ({url_result.reason})" if url_result.reason else ""
                        )
                        result.append({
                            "file": self.path,
                            "issue": (
                                f"Source URL unreachable:"
                                f" {url_result.url}{reason}"
                            ),
                            "severity": "fail",
                        })

        return result


@dataclass
class PlanDocument(Document):
    """A plan document with parsed task list and completion tracking."""

    tasks: List[dict] = field(default_factory=list, init=False)

    def __post_init__(self) -> None:
        self.tasks = _parse_tasks(self.content)

    def tasks_complete(self) -> bool:
        """Return True if all tasks are marked completed."""
        return bool(self.tasks) and all(t["completed"] for t in self.tasks)

    def completion_stats(self) -> dict:
        """Return task completion counts."""
        total = len(self.tasks)
        done = sum(1 for t in self.tasks if t["completed"])
        return {"total": total, "done": done, "remaining": total - done}


@dataclass
class ContextDocument(Document):
    """A context document with word count and related-field validation."""

    def issues(
        self,
        root: Path,
        max_words: int = 800,
        min_words: int = 100,
    ) -> List[dict]:
        """Return base issues plus context-specific checks.

        Adds: missing related-fields warning, and word count threshold
        warnings (skipped for _index.md files).

        Args:
            root: Project root directory.
            max_words: Upper word count threshold (default 800).
            min_words: Lower word count threshold (default 100).

        Returns:
            List of issue dicts with keys: file, issue, severity.
        """
        result = super().issues(root)

        if not self.related:
            result.append({
                "file": self.path,
                "issue": "Context file has no related fields",
                "severity": "warn",
            })

        if not self.path.endswith("_index.md"):
            word_count = self.word_count
            if word_count > max_words:
                result.append({
                    "file": self.path,
                    "issue": (
                        f"Context file is {word_count} words"
                        f" (threshold: {max_words})"
                    ),
                    "severity": "warn",
                })
            elif word_count < min_words:
                result.append({
                    "file": self.path,
                    "issue": (
                        f"Context file is {word_count} words"
                        f" (minimum: {min_words})"
                    ),
                    "severity": "warn",
                })

        return result


# ── Module-level alias ─────────────────────────────────────────────

#: Backwards-compatible alias — prefer Document.parse() in new code.
parse_document = Document.parse
