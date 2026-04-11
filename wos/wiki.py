"""Wiki-aware validators for SCHEMA.md-governed wiki directories.

Provides four functions for validating wiki page structure and schema
conformance, plus helpers used by validate_wiki() in validators.py.

Each check returns a list of issue dicts with keys: file, issue, severity.
"""

from __future__ import annotations

from pathlib import Path
from typing import List

from wos.document import Document

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
    current_key: str | None = None

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
                "issue": f"Wiki page not referenced in _index.md: {md_file.name}",
                "severity": "warn",
            })

    return issues


# ── Per-document checks ────────────────────────────────────────


def check_wiki_schema_violations(doc: Document, schema: dict) -> List[dict]:
    """Fail issues for schema-invalid type or confidence values.

    Checks ``doc.type`` against ``schema['page_types']``. Checks
    ``doc.meta.get('confidence')`` against ``schema['confidence_tiers']``
    only when the field is present — missing confidence is a frontmatter
    issue, not a schema violation.

    Args:
        doc: A parsed Document instance.
        schema: Dict from parse_schema() with page_types, confidence_tiers,
            relationship_types lists.

    Returns:
        List of issue dicts with severity ``fail``.
    """
    issues: List[dict] = []

    if doc.type and doc.type not in schema["page_types"]:
        issues.append({
            "file": doc.path,
            "issue": (
                f"Wiki page type '{doc.type}' not in schema page_types:"
                f" {schema['page_types']}"
            ),
            "severity": "fail",
        })

    confidence = doc.meta.get("confidence")
    if confidence is not None and confidence not in schema["confidence_tiers"]:
        issues.append({
            "file": doc.path,
            "issue": (
                f"Wiki confidence '{confidence}' not in schema confidence_tiers:"
                f" {schema['confidence_tiers']}"
            ),
            "severity": "fail",
        })

    return issues


def check_wiki_frontmatter(doc: Document) -> List[dict]:
    """Warn for missing wiki-specific frontmatter fields.

    Checks that ``confidence``, ``created``, and ``updated`` are present
    in ``doc.meta``.

    Args:
        doc: A parsed Document instance.

    Returns:
        List of issue dicts with severity ``warn``.
    """
    issues: List[dict] = []

    for field_name in ("confidence", "created", "updated"):
        if doc.meta.get(field_name) is None:
            issues.append({
                "file": doc.path,
                "issue": f"Wiki page missing frontmatter field: '{field_name}'",
                "severity": "warn",
            })

    return issues
