"""Tests for wos/wiki.py — WikiDocument and wiki validation."""

from __future__ import annotations

from pathlib import Path

import pytest  # noqa: F401

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
):
    """Write a wiki page to tmp_path and return (path, WikiDocument)."""
    from wos.wiki import WikiDocument

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
    doc = WikiDocument(
        path=str(path),
        name=name,
        description=description,
        content=content,
        type=doc_type,
        meta={"confidence": confidence, "created": created, "updated": updated},
    )
    return path, doc


def _default_schema() -> dict:
    return {
        "page_types": ["concept", "entity"],
        "confidence_tiers": ["high", "medium", "low"],
        "relationship_types": ["related_to", "uses"],
    }


# ── TestParseSchemaValid ───────────────────────────────────────────


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


# ── TestParseSchemaMissingSection ─────────────────────────────────


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


# ── TestCheckWikiOrphans ──────────────────────────────────────────


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


# ── TestWikiDocumentIssues ────────────────────────────────────────


class TestWikiDocumentSchemaViolations:
    def test_unrecognized_type_returns_fail(self, tmp_path: Path) -> None:
        _, doc = _wiki_doc(tmp_path, doc_type="unknown-type")
        schema = _default_schema()

        issues = doc.issues(tmp_path, schema=schema)

        type_issues = [i for i in issues if "page_types" in i["issue"]]
        assert len(type_issues) == 1
        assert type_issues[0]["severity"] == "fail"
        assert "unknown-type" in type_issues[0]["issue"]

    def test_unrecognized_confidence_returns_fail(self, tmp_path: Path) -> None:
        _, doc = _wiki_doc(tmp_path, doc_type="concept", confidence="extreme")
        schema = _default_schema()

        issues = doc.issues(tmp_path, schema=schema)

        conf_issues = [i for i in issues if "confidence_tiers" in i["issue"]]
        assert len(conf_issues) == 1
        assert conf_issues[0]["severity"] == "fail"
        assert "extreme" in conf_issues[0]["issue"]

    def test_valid_doc_no_schema_violations(self, tmp_path: Path) -> None:
        _, doc = _wiki_doc(tmp_path, doc_type="concept", confidence="high")
        schema = _default_schema()

        issues = doc.issues(tmp_path, schema=schema)

        schema_issues = [
            i for i in issues
            if "page_types" in i["issue"] or "confidence_tiers" in i["issue"]
        ]
        assert schema_issues == []

    def test_missing_confidence_not_a_schema_violation(self, tmp_path: Path) -> None:
        """Missing confidence is a frontmatter warn, not a schema violation."""
        from wos.wiki import WikiDocument

        doc = WikiDocument(
            path=str(tmp_path / "page.md"),
            name="P",
            description="D",
            content="body",
            type="concept",
            meta={},  # no confidence key at all
        )
        schema = _default_schema()

        issues = doc.issues(tmp_path, schema=schema)

        schema_issues = [i for i in issues if "confidence_tiers" in i["issue"]]
        assert schema_issues == []


class TestWikiDocumentFrontmatter:
    def test_missing_all_fields_returns_three_warns(self, tmp_path: Path) -> None:
        from wos.wiki import WikiDocument

        doc = WikiDocument(
            path=str(tmp_path / "page.md"),
            name="P",
            description="D",
            content="body",
            type="concept",
            meta={},
        )

        issues = doc.issues(tmp_path, schema=_default_schema())

        fm_issues = [i for i in issues if "missing frontmatter" in i["issue"]]
        assert len(fm_issues) == 3
        field_names = {i["issue"] for i in fm_issues}
        assert any("confidence" in f for f in field_names)
        assert any("created" in f for f in field_names)
        assert any("updated" in f for f in field_names)
        assert all(i["severity"] == "warn" for i in fm_issues)

    def test_all_fields_present_no_frontmatter_issues(self, tmp_path: Path) -> None:
        _, doc = _wiki_doc(tmp_path)

        issues = doc.issues(tmp_path, schema=_default_schema())

        fm_issues = [i for i in issues if "missing frontmatter" in i["issue"]]
        assert fm_issues == []

    def test_no_schema_skips_schema_checks(self, tmp_path: Path) -> None:
        """When no SCHEMA.md exists and schema=None, skip schema violation checks."""
        from wos.wiki import WikiDocument

        # No SCHEMA.md in tmp_path — auto-load will fail, checks are skipped
        doc = WikiDocument(
            path=str(tmp_path / "page.md"),
            name="P",
            description="D",
            content="body",
            type="unknown-type-that-would-fail",
            meta={
                "confidence": "high", "created": "2026-01-01", "updated": "2026-01-01"
            },
        )

        issues = doc.issues(tmp_path, schema=None)

        schema_issues = [i for i in issues if "page_types" in i["issue"]]
        assert schema_issues == []


# ── TestValidateWikiClean ─────────────────────────────────────────


class TestValidateWikiClean:
    def test_clean_wiki_no_issues(self, tmp_path: Path) -> None:
        from wos.index import generate_index
        from wos.wiki import validate_wiki

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


# ── TestValidateWikiWithViolations ────────────────────────────────


class TestValidateWikiWithViolations:
    def test_invalid_type_surfaces_fail(self, tmp_path: Path) -> None:
        from wos.wiki import validate_wiki

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
        from wos.wiki import validate_wiki

        schema_path = tmp_path / "SCHEMA.md"
        schema_path.write_text(
            "# SCHEMA.md\n\n## Page Types\n- concept\n", encoding="utf-8"
        )

        issues = validate_wiki(tmp_path, schema_path)

        assert len(issues) == 1
        assert issues[0]["severity"] == "warn"
        assert "Invalid SCHEMA.md" in issues[0]["issue"]
