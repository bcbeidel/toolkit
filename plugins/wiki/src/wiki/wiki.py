"""Wiki-aware validators for SCHEMA.md-governed wiki directories.

Provides WikiDocument — a Document subclass for wiki pages — and
validate_wiki() which orchestrates validation for a wiki directory.

Each issue dict has keys: file, issue, severity.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

from wiki.document import Document, parse_document


@dataclass
class WikiDocument(Document):
    """A wiki page document with schema conformance validation.

    Overrides ``issues()`` to add: schema type and confidence checks,
    and required wiki frontmatter field presence (confidence, created,
    updated).
    """

    def issues(
        self,
        root: Path,
        schema: Optional[dict] = None,
        **_: object,
    ) -> List[dict]:
        """Return base issues plus wiki-specific checks.

        Adds: page type against schema, confidence tier against schema,
        and required wiki frontmatter field presence.

        Args:
            root: Project root directory (used by base class).
            schema: Schema dict from parse_schema(). If None, attempts
                to load from ``Path(self.path).parent / "SCHEMA.md"``.
                If SCHEMA.md is missing or malformed, schema checks are
                skipped.

        Returns:
            List of issue dicts with keys: file, issue, severity.
        """
        result = super().issues(root)

        if schema is None:
            schema_path = Path(self.path).parent / "SCHEMA.md"
            try:
                schema = parse_schema(schema_path)
            except ValueError:
                schema = None  # skip schema checks if unavailable

        if schema is not None:
            if self.type and self.type not in schema["page_types"]:
                result.append({
                    "file": self.path,
                    "issue": (
                        f"Wiki page type '{self.type}' not in schema page_types:"
                        f" {schema['page_types']}"
                    ),
                    "severity": "fail",
                })
            confidence = self.meta.get("confidence")
            if confidence is not None and confidence not in schema["confidence_tiers"]:
                result.append({
                    "file": self.path,
                    "issue": (
                        f"Wiki confidence '{confidence}' not in schema"
                        f" confidence_tiers: {schema['confidence_tiers']}"
                    ),
                    "severity": "fail",
                })

        for field_name in ("confidence", "created", "updated"):
            if self.meta.get(field_name) is None:
                result.append({
                    "file": self.path,
                    "issue": f"Wiki page missing frontmatter field: '{field_name}'",
                    "severity": "warn",
                })

        return result


# ── Schema parsing ─────────────────────────────────────────────


def parse_schema(schema_path: Path) -> dict:
    """Read SCHEMA.md and extract page_types, confidence_tiers, relationship_types.

    Parses ``## Section Name`` headings followed by ``- value`` list items.
    Required sections: ``Page Types``, ``Confidence Tiers``, ``Relationship Types``.

    Args:
        schema_path: Path to SCHEMA.md.

    Returns:
        Dict with keys ``page_types``, ``confidence_tiers``, ``relationship_types``,
        each a list of strings.

    Raises:
        ValueError: If any required section is missing or the file cannot be read.
    """
    _REQUIRED = {
        "page types": "page_types",
        "confidence tiers": "confidence_tiers",
        "relationship types": "relationship_types",
    }

    try:
        text = schema_path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ValueError(f"Cannot read {schema_path}: {exc}") from exc

    collected: dict = {key: [] for key in _REQUIRED.values()}
    current_key: Optional[str] = None

    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("##"):
            heading = stripped.lstrip("#").strip().lower()
            current_key = _REQUIRED.get(heading)
        elif current_key is not None and stripped.startswith("- "):
            value = stripped[2:].strip()
            if value:
                collected[current_key].append(value)

    missing = [
        label for label, key in _REQUIRED.items()
        if not collected[key]
    ]
    if missing:
        raise ValueError(
            f"SCHEMA.md missing required sections: {', '.join(missing)}"
        )

    return collected


# ── Per-directory checks ───────────────────────────────────────


def check_wiki_orphans(wiki_dir: Path) -> List[dict]:
    """Warn for .md files in wiki_dir not referenced in wiki_dir/_index.md.

    Skips ``_index.md`` and ``SCHEMA.md`` themselves.

    Args:
        wiki_dir: Path to the wiki directory.

    Returns:
        List of issue dicts with severity ``warn``.
    """
    issues: List[dict] = []
    index_path = wiki_dir / "_index.md"

    if not index_path.is_file():
        return issues

    try:
        index_text = index_path.read_text(encoding="utf-8")
    except OSError:
        return issues

    for md_file in sorted(wiki_dir.iterdir()):
        if not md_file.is_file() or md_file.suffix != ".md":
            continue
        if md_file.name in ("_index.md", "SCHEMA.md"):
            continue
        if md_file.name not in index_text:
            issues.append({
                "file": str(md_file),
                "issue": (
                    "Wiki page not in index. "
                    "Add an entry to wiki/_index.md or run /wiki:lint --fix "
                    "to regenerate the index."
                ),
                "severity": "warn",
            })

    return issues


# ── Orchestrator ───────────────────────────────────────────────


def validate_wiki(wiki_dir: Path, schema_path: Path) -> List[dict]:
    """Validate all documents in a wiki directory against its SCHEMA.md.

    Runs WikiDocument.issues() per file and check_wiki_orphans() across
    the directory. If SCHEMA.md is missing or malformed, returns a single
    warn and exits early.

    Args:
        wiki_dir: Path to the wiki directory.
        schema_path: Path to wiki/SCHEMA.md.

    Returns:
        List of issue dicts. Empty on a clean wiki.
    """
    issues: List[dict] = []

    try:
        schema = parse_schema(schema_path)
    except ValueError as exc:
        return [{
            "file": str(schema_path),
            "issue": f"Invalid SCHEMA.md: {exc}",
            "severity": "warn",
        }]

    for md_file in sorted(wiki_dir.iterdir()):
        if not md_file.is_file() or md_file.suffix != ".md":
            continue
        if md_file.name in ("_index.md", "SCHEMA.md"):
            continue
        try:
            text = md_file.read_text(encoding="utf-8")
            base_doc = parse_document(str(md_file), text)
            doc = WikiDocument(
                path=base_doc.path,
                name=base_doc.name,
                description=base_doc.description,
                content=base_doc.content,
                type=base_doc.type,
                meta=base_doc.meta,
            )
        except (OSError, ValueError) as exc:
            issues.append({
                "file": str(md_file),
                "issue": f"Parse error: {exc}",
                "severity": "fail",
            })
            continue
        issues.extend(doc.issues(wiki_dir, schema=schema))

    issues.extend(check_wiki_orphans(wiki_dir))

    return issues
