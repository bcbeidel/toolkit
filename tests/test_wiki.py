"""Tests for wos/wiki.py — wiki schema parsing and validator functions."""

from __future__ import annotations

from pathlib import Path

import pytest  # noqa: F401

from wos.document import Document  # noqa: F401

# ── Helpers ──────────────────────────────────────────────────────


def _schema_md(
    page_types: list[str] | None = None,
    confidence_tiers: list[str] | None = None,
    relationship_types: list[str] | None = None,
) -> str:
    """Build a SCHEMA.md string with the given sections."""
    page_types = page_types if page_types is not None else ["concept", "entity"]
    confidence_tiers = (
        confidence_tiers if confidence_tiers is not None else ["high", "medium", "low"]
    )
    relationship_types = (
        relationship_types if relationship_types is not None else ["related_to", "uses"]
    )

    lines = ["# SCHEMA.md", ""]
    if page_types is not None:
        lines += ["## Page Types"] + [f"- {t}" for t in page_types] + [""]
    if confidence_tiers is not None:
        lines += (
            ["## Confidence Tiers"] + [f"- {t}" for t in confidence_tiers] + [""]
        )
    if relationship_types is not None:
        lines += (
            ["## Relationship Types"] + [f"- {r}" for r in relationship_types] + [""]
        )
    return "\n".join(lines)


def _wiki_doc(
    tmp_path: Path,
    name: str = "Test Page",
    description: str = "A wiki page",
    doc_type: str = "concept",
    confidence: str = "high",
    created: str = "2026-01-01",
    updated: str = "2026-01-01",
    filename: str = "test-page.md",
) -> tuple[Path, Document]:
    """Write a wiki page to tmp_path and return (path, Document)."""
    from wos.document import parse_document

    fm_lines = [
        "---",
        f"name: {name}",
        f"description: {description}",
        f"type: {doc_type}",
        f"confidence: {confidence}",
        f"created: {created}",
        f"updated: {updated}",
        "---",
        f"# {name}",
        "",
    ]
    content = "\n".join(fm_lines)
    path = tmp_path / filename
    path.write_text(content, encoding="utf-8")
    doc = parse_document(str(path), content)
    return path, doc


def _default_schema() -> dict:
    return {
        "page_types": ["concept", "entity"],
        "confidence_tiers": ["high", "medium", "low"],
        "relationship_types": ["related_to", "uses"],
    }


# ── test_parse_schema_valid ───────────────────────────────────────


class TestParseSchemaValid:
    def test_returns_correct_lists(self, tmp_path: Path) -> None:
        from wos.wiki import parse_schema

        schema_file = tmp_path / "SCHEMA.md"
        schema_file.write_text(_schema_md(), encoding="utf-8")

        schema = parse_schema(schema_file)

        assert schema["page_types"] == ["concept", "entity"]
        assert schema["confidence_tiers"] == ["high", "medium", "low"]
        assert schema["relationship_types"] == ["related_to", "uses"]

    def test_extra_sections_ignored(self, tmp_path: Path) -> None:
        from wos.wiki import parse_schema

        content = _schema_md() + "\n## Lint Rules\n- staleness: 90 days\n"
        schema_file = tmp_path / "SCHEMA.md"
        schema_file.write_text(content, encoding="utf-8")

        schema = parse_schema(schema_file)

        assert set(schema.keys()) == {
            "page_types", "confidence_tiers", "relationship_types"
        }


# ── test_parse_schema_missing_section ────────────────────────────


class TestParseSchemaMissingSection:
    def test_missing_confidence_tiers_raises(self, tmp_path: Path) -> None:
        from wos.wiki import parse_schema

        content = (
            "# SCHEMA.md\n\n## Page Types\n- concept\n\n"
            "## Relationship Types\n- related_to\n"
        )
        schema_file = tmp_path / "SCHEMA.md"
        schema_file.write_text(content, encoding="utf-8")

        with pytest.raises(ValueError, match="confidence tiers"):
            parse_schema(schema_file)

    def test_missing_page_types_raises(self, tmp_path: Path) -> None:
        from wos.wiki import parse_schema

        content = (
            "# SCHEMA.md\n\n## Confidence Tiers\n- high\n\n"
            "## Relationship Types\n- related_to\n"
        )
        schema_file = tmp_path / "SCHEMA.md"
        schema_file.write_text(content, encoding="utf-8")

        with pytest.raises(ValueError, match="page types"):
            parse_schema(schema_file)


# ── test_check_wiki_orphans ───────────────────────────────────────


class TestCheckWikiOrphans:
    def test_unindexed_file_returns_warn(self, tmp_path: Path) -> None:
        from wos.wiki import check_wiki_orphans

        orphan = tmp_path / "orphan.md"
        orphan.write_text("---\nname: Orphan\ndescription: unindexed\n---\nbody\n")
        index = tmp_path / "_index.md"
        index.write_text("# Index\n\nNo files listed.\n")

        issues = check_wiki_orphans(tmp_path)

        assert len(issues) == 1
        assert issues[0]["severity"] == "warn"
        assert "orphan.md" in issues[0]["issue"]

    def test_indexed_file_no_issue(self, tmp_path: Path) -> None:
        from wos.wiki import check_wiki_orphans

        page = tmp_path / "my-page.md"
        page.write_text("---\nname: Page\ndescription: indexed\n---\nbody\n")
        index = tmp_path / "_index.md"
        index.write_text("# Index\n\n- [my-page.md](my-page.md) — indexed\n")

        issues = check_wiki_orphans(tmp_path)

        assert issues == []

    def test_schema_and_index_skipped(self, tmp_path: Path) -> None:
        from wos.wiki import check_wiki_orphans

        (tmp_path / "SCHEMA.md").write_text("## Page Types\n- concept\n")
        (tmp_path / "_index.md").write_text("# Index\n")

        issues = check_wiki_orphans(tmp_path)

        assert issues == []


# ── test_check_wiki_schema_violations ────────────────────────────


class TestCheckWikiSchemaViolations:
    def test_unrecognized_type_returns_fail(self, tmp_path: Path) -> None:
        from wos.wiki import check_wiki_schema_violations

        _, doc = _wiki_doc(tmp_path, doc_type="unknown-type")
        schema = _default_schema()

        issues = check_wiki_schema_violations(doc, schema)

        assert len(issues) == 1
        assert issues[0]["severity"] == "fail"
        assert "unknown-type" in issues[0]["issue"]

    def test_unrecognized_confidence_returns_fail(self, tmp_path: Path) -> None:
        from wos.wiki import check_wiki_schema_violations

        _, doc = _wiki_doc(tmp_path, doc_type="concept", confidence="extreme")
        schema = _default_schema()

        issues = check_wiki_schema_violations(doc, schema)

        assert len(issues) == 1
        assert issues[0]["severity"] == "fail"
        assert "extreme" in issues[0]["issue"]

    def test_valid_doc_no_violations(self, tmp_path: Path) -> None:
        from wos.wiki import check_wiki_schema_violations

        _, doc = _wiki_doc(tmp_path, doc_type="concept", confidence="high")
        schema = _default_schema()

        issues = check_wiki_schema_violations(doc, schema)

        assert issues == []

    def test_missing_confidence_not_a_violation(self, tmp_path: Path) -> None:
        """Missing confidence is a frontmatter issue, not a schema violation."""
        from wos.document import parse_document
        from wos.wiki import check_wiki_schema_violations

        content = "---\nname: P\ndescription: D\ntype: concept\n---\nbody\n"
        path = tmp_path / "page.md"
        path.write_text(content)
        doc = parse_document(str(path), content)
        schema = _default_schema()

        issues = check_wiki_schema_violations(doc, schema)

        assert issues == []


# ── test_check_wiki_frontmatter ──────────────────────────────────


class TestCheckWikiFrontmatter:
    def test_missing_all_fields_returns_three_warns(self, tmp_path: Path) -> None:
        from wos.document import parse_document
        from wos.wiki import check_wiki_frontmatter

        content = "---\nname: P\ndescription: D\ntype: concept\n---\nbody\n"
        path = tmp_path / "page.md"
        path.write_text(content)
        doc = parse_document(str(path), content)

        issues = check_wiki_frontmatter(doc)

        assert len(issues) == 3
        field_names = {i["issue"] for i in issues}
        assert any("confidence" in f for f in field_names)
        assert any("created" in f for f in field_names)
        assert any("updated" in f for f in field_names)
        assert all(i["severity"] == "warn" for i in issues)

    def test_all_fields_present_no_issues(self, tmp_path: Path) -> None:
        from wos.wiki import check_wiki_frontmatter

        _, doc = _wiki_doc(tmp_path)

        issues = check_wiki_frontmatter(doc)

        assert issues == []


# ── test_validate_wiki_clean ──────────────────────────────────────


class TestValidateWikiClean:
    def test_clean_wiki_no_issues(self, tmp_path: Path) -> None:
        from wos.index import generate_index
        from wos.validators import validate_wiki

        # Write SCHEMA.md
        schema_path = tmp_path / "SCHEMA.md"
        schema_path.write_text(_schema_md(), encoding="utf-8")

        # Write a valid wiki page
        page_path = tmp_path / "my-concept.md"
        page_content = (
            "---\nname: My Concept\ndescription: A concept page\n"
            "type: concept\nconfidence: high\n"
            "created: 2026-01-01\nupdated: 2026-01-01\n"
            "---\n# My Concept\n\nContent here.\n"
        )
        page_path.write_text(page_content, encoding="utf-8")

        # Write a generated _index.md so check_index_sync passes
        index_path = tmp_path / "_index.md"
        index_path.write_text(generate_index(tmp_path), encoding="utf-8")

        issues = validate_wiki(tmp_path, schema_path)

        failures = [i for i in issues if i["severity"] == "fail"]
        assert failures == [], failures


# ── test_validate_wiki_with_violations ───────────────────────────


class TestValidateWikiWithViolations:
    def test_invalid_type_surfaces_fail(self, tmp_path: Path) -> None:
        from wos.validators import validate_wiki

        schema_path = tmp_path / "SCHEMA.md"
        schema_path.write_text(_schema_md(), encoding="utf-8")

        page_path = tmp_path / "bad-page.md"
        page_content = (
            "---\nname: Bad Page\ndescription: Has wrong type\n"
            "type: unknown-type\nconfidence: high\n"
            "created: 2026-01-01\nupdated: 2026-01-01\n"
            "---\n# Bad Page\n"
        )
        page_path.write_text(page_content, encoding="utf-8")

        (tmp_path / "_index.md").write_text(
            "| [bad-page.md](bad-page.md) | Has wrong type |\n",
        )

        issues = validate_wiki(tmp_path, schema_path)

        failures = [i for i in issues if i["severity"] == "fail"]
        assert len(failures) >= 1
        assert any("unknown-type" in i["issue"] for i in failures)

    def test_malformed_schema_returns_single_warn(self, tmp_path: Path) -> None:
        from wos.validators import validate_wiki

        schema_path = tmp_path / "SCHEMA.md"
        schema_path.write_text(
            "# SCHEMA.md\n\n## Page Types\n- concept\n", encoding="utf-8"
        )

        issues = validate_wiki(tmp_path, schema_path)

        assert len(issues) == 1
        assert issues[0]["severity"] == "warn"
        assert "Invalid SCHEMA.md" in issues[0]["issue"]
