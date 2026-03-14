"""Tests for wos/document.py — Document dataclass and parse_document()."""

from __future__ import annotations

import pytest

# ── Document dataclass ──────────────────────────────────────────


class TestDocument:
    def test_minimal_fields(self) -> None:
        from wos.document import Document

        doc = Document(
            path="docs/context/testing/unit-tests.md",
            name="Unit Tests",
            description="Guide to writing unit tests",
            content="# Unit Tests\n\nSome content here.\n",
        )
        assert doc.path == "docs/context/testing/unit-tests.md"
        assert doc.name == "Unit Tests"
        assert doc.description == "Guide to writing unit tests"
        assert doc.content == "# Unit Tests\n\nSome content here.\n"
        assert doc.type is None
        assert doc.sources == []
        assert doc.related == []
        assert doc.status is None
        assert doc.created_at is None
        assert doc.updated_at is None

    def test_all_fields(self) -> None:
        from wos.document import Document

        doc = Document(
            path="docs/research/2026-02-20-api-review.md",
            name="API Review",
            description="Research on REST API patterns",
            content="# API Review\n\nFindings.\n",
            type="research",
            sources=[
                "https://example.com/rest-guide",
                "https://example.com/api-design",
            ],
            related=[
                "docs/context/api/authentication.md",
                "https://github.com/org/repo/issues/42",
            ],
        )
        assert doc.type == "research"
        assert len(doc.sources) == 2
        assert "https://example.com/rest-guide" in doc.sources
        assert len(doc.related) == 2
        assert "docs/context/api/authentication.md" in doc.related


# ── parse_document ──────────────────────────────────────────────


class TestParseDocument:
    def test_minimal_frontmatter(self) -> None:
        from wos.document import parse_document

        text = (
            "---\n"
            "name: Unit Tests\n"
            "description: Guide to writing unit tests\n"
            "---\n"
            "# Unit Tests\n"
            "\n"
            "Content here.\n"
        )
        doc = parse_document("docs/context/testing/unit-tests.md", text)
        assert doc.path == "docs/context/testing/unit-tests.md"
        assert doc.name == "Unit Tests"
        assert doc.description == "Guide to writing unit tests"
        assert doc.type is None
        assert doc.sources == []
        assert doc.related == []

    def test_research_doc_with_type_and_sources(self) -> None:
        from wos.document import parse_document

        text = (
            "---\n"
            "name: API Review\n"
            "description: Research on REST API patterns\n"
            "type: research\n"
            "sources:\n"
            "  - https://example.com/rest-guide\n"
            "  - https://example.com/api-design\n"
            "---\n"
            "# API Review\n"
            "\n"
            "Research findings.\n"
        )
        doc = parse_document("docs/research/2026-02-20-api-review.md", text)
        assert doc.type == "research"
        assert doc.sources == [
            "https://example.com/rest-guide",
            "https://example.com/api-design",
        ]

    def test_related_field(self) -> None:
        from wos.document import parse_document

        text = (
            "---\n"
            "name: Authentication\n"
            "description: Auth patterns\n"
            "related:\n"
            "  - docs/context/api/tokens.md\n"
            "  - https://github.com/org/repo/issues/42\n"
            "---\n"
            "# Authentication\n"
        )
        doc = parse_document("docs/context/api/authentication.md", text)
        assert doc.related == [
            "docs/context/api/tokens.md",
            "https://github.com/org/repo/issues/42",
        ]

    def test_plan_with_status(self) -> None:
        from wos.document import parse_document

        text = (
            "---\n"
            "name: My Plan\n"
            "description: A plan with status\n"
            "type: plan\n"
            "status: draft\n"
            "---\n"
            "# My Plan\n"
        )
        doc = parse_document("docs/plans/test.md", text)
        assert doc.status == "draft"
        assert doc.type == "plan"

    def test_raises_on_invalid_status(self) -> None:
        from wos.document import parse_document

        text = (
            "---\n"
            "name: Bad Plan\n"
            "description: A plan with invalid status\n"
            "type: plan\n"
            "status: done\n"
            "---\n"
            "# Bad Plan\n"
        )
        with pytest.raises(ValueError, match="status"):
            parse_document("docs/plans/bad.md", text)

    def test_all_valid_statuses(self) -> None:
        from wos.document import parse_document

        for status in ("draft", "approved", "executing", "completed", "abandoned"):
            text = (
                "---\n"
                f"name: Plan {status}\n"
                f"description: A plan with status {status}\n"
                "type: plan\n"
                f"status: {status}\n"
                "---\n"
                "# Plan\n"
            )
            doc = parse_document("docs/plans/test.md", text)
            assert doc.status == status

    def test_unknown_fields_ignored(self) -> None:
        from wos.document import parse_document

        text = (
            "---\n"
            "name: Custom Doc\n"
            "description: A document with extra fields\n"
            "status: draft\n"
            "priority: high\n"
            "tags:\n"
            "  - python\n"
            "  - testing\n"
            "---\n"
            "# Custom Doc\n"
        )
        doc = parse_document("docs/context/misc/custom.md", text)
        assert doc.name == "Custom Doc"
        assert doc.description == "A document with extra fields"
        assert doc.status == "draft"  # status is now a known field
        # Truly unknown fields are not stored
        assert not hasattr(doc, "priority")

    def test_raises_on_no_frontmatter(self) -> None:
        from wos.document import parse_document

        text = "# Just a heading\n\nNo frontmatter here.\n"
        with pytest.raises(ValueError, match="frontmatter"):
            parse_document("docs/no-frontmatter.md", text)

    def test_raises_on_missing_name(self) -> None:
        from wos.document import parse_document

        text = (
            "---\n"
            "description: Has description but no name\n"
            "---\n"
            "# Content\n"
        )
        with pytest.raises(ValueError, match="name"):
            parse_document("docs/missing-name.md", text)

    def test_raises_on_missing_description(self) -> None:
        from wos.document import parse_document

        text = (
            "---\n"
            "name: Has name but no description\n"
            "---\n"
            "# Content\n"
        )
        with pytest.raises(ValueError, match="description"):
            parse_document("docs/missing-desc.md", text)

    def test_content_excludes_frontmatter(self) -> None:
        from wos.document import parse_document

        text = (
            "---\n"
            "name: Test Doc\n"
            "description: Testing content separation\n"
            "---\n"
            "# Body\n"
            "\n"
            "This is the body.\n"
        )
        doc = parse_document("test.md", text)
        assert "---" not in doc.content
        assert "name:" not in doc.content
        assert "description:" not in doc.content
        assert "# Body" in doc.content
        assert "This is the body." in doc.content

    def test_raises_on_empty_frontmatter(self) -> None:
        from wos.document import parse_document

        text = "---\n---\n# Content\n"
        with pytest.raises(ValueError, match="name"):
            parse_document("docs/empty-fm.md", text)

    def test_content_with_no_body(self) -> None:
        """Document with frontmatter but no content after it."""
        from wos.document import parse_document

        text = (
            "---\n"
            "name: Empty Body\n"
            "description: No content after frontmatter\n"
            "---\n"
        )
        doc = parse_document("test.md", text)
        assert doc.content == ""

    def test_content_preserves_leading_newline(self) -> None:
        """Content starts exactly after the closing --- delimiter."""
        from wos.document import parse_document

        text = (
            "---\n"
            "name: Test\n"
            "description: Desc\n"
            "---\n"
            "\n"
            "Paragraph.\n"
        )
        doc = parse_document("test.md", text)
        assert doc.content.startswith("\n")

    def test_yaml_null_sources_and_related_default_to_empty_list(self) -> None:
        """sources: and related: with no value parse as YAML null (None).

        The parser should coerce None to [] rather than propagating it.
        """
        from wos.document import parse_document

        text = (
            "---\n"
            "name: Null Fields\n"
            "description: Sources and related are YAML null\n"
            "sources:\n"
            "related:\n"
            "---\n"
            "# Content\n"
        )
        doc = parse_document("test.md", text)
        assert doc.sources == []
        assert doc.related == []

    def test_type_inferred_from_compound_suffix(self) -> None:
        """When frontmatter has no type, infer from .research.md suffix."""
        from wos.document import parse_document

        text = (
            "---\n"
            "name: API Review\n"
            "description: Research on REST API patterns\n"
            "sources:\n"
            "  - https://example.com/rest-guide\n"
            "---\n"
            "# API Review\n"
        )
        doc = parse_document("docs/research/api-review.research.md", text)
        assert doc.type == "research"

    def test_type_inferred_from_plan_suffix(self) -> None:
        """When frontmatter has no type, infer from .plan.md suffix."""
        from wos.document import parse_document

        text = (
            "---\n"
            "name: Deploy Plan\n"
            "description: Deployment plan\n"
            "status: draft\n"
            "---\n"
            "# Deploy Plan\n"
        )
        doc = parse_document("docs/plans/2026-03-13-deploy.plan.md", text)
        assert doc.type == "plan"

    def test_frontmatter_type_takes_precedence_over_suffix(self) -> None:
        """Explicit frontmatter type wins over suffix inference."""
        from wos.document import parse_document

        text = (
            "---\n"
            "name: Overridden\n"
            "description: Frontmatter type should win\n"
            "type: custom\n"
            "---\n"
            "# Content\n"
        )
        doc = parse_document("docs/research/overridden.research.md", text)
        assert doc.type == "custom"

    def test_plain_md_no_type_stays_none(self) -> None:
        """Plain .md with no frontmatter type remains None."""
        from wos.document import parse_document

        text = (
            "---\n"
            "name: Plain\n"
            "description: No type anywhere\n"
            "---\n"
            "# Content\n"
        )
        doc = parse_document("docs/context/plain.md", text)
        assert doc.type is None

    def test_raises_valueerror_on_missing_closing_delimiter(self) -> None:
        """Missing closing delimiter must raise ValueError."""
        from wos.document import parse_document

        text = (
            "---\n"
            "name: Unclosed\n"
            "description: No closing delimiter\n"
        )
        with pytest.raises(ValueError, match="closing"):
            parse_document("test.md", text)

    def test_numeric_name_and_description_coerced_to_str(self) -> None:
        """name: 42 and description: 100 should be coerced to strings."""
        from wos.document import parse_document

        text = (
            "---\n"
            "name: 42\n"
            "description: 100\n"
            "---\n"
            "# Content\n"
        )
        doc = parse_document("test.md", text)
        assert doc.name == "42"
        assert doc.description == "100"
        assert isinstance(doc.name, str)
        assert isinstance(doc.description, str)

    def test_type_inferred_from_design_suffix(self) -> None:
        """When frontmatter has no type, infer from .design.md suffix."""
        from wos.document import parse_document

        text = (
            "---\n"
            "name: Feature Design\n"
            "description: Design for feature X\n"
            "---\n"
            "# Feature Design\n"
        )
        doc = parse_document("docs/designs/2026-03-13-feature.design.md", text)
        assert doc.type == "design"

    def test_type_inferred_from_context_suffix(self) -> None:
        """When frontmatter has no type, infer from .context.md suffix."""
        from wos.document import parse_document

        text = (
            "---\n"
            "name: Event Loop Model\n"
            "description: How asyncio event loop works\n"
            "---\n"
            "# Event Loop Model\n"
        )
        doc = parse_document("docs/context/async/event-loop.context.md", text)
        assert doc.type == "context"

    def test_type_inferred_from_prompt_suffix(self) -> None:
        """When frontmatter has no type, infer from .prompt.md suffix."""
        from wos.document import parse_document

        text = (
            "---\n"
            "name: Code Review Prompt\n"
            "description: Prompt for reviewing pull requests\n"
            "---\n"
            "# Code Review Prompt\n"
        )
        doc = parse_document("docs/prompts/code-review.prompt.md", text)
        assert doc.type == "prompt"

    def test_timestamps_parsed(self) -> None:
        """created_at and updated_at are extracted from frontmatter."""
        from wos.document import parse_document

        text = (
            "---\n"
            "name: Timestamped\n"
            "description: Has timestamps\n"
            "created_at: 2026-03-13\n"
            "updated_at: 2026-03-14\n"
            "---\n"
            "# Content\n"
        )
        doc = parse_document("test.md", text)
        assert doc.created_at == "2026-03-13"
        assert doc.updated_at == "2026-03-14"

    def test_timestamps_optional(self) -> None:
        """Documents without timestamps default to None."""
        from wos.document import parse_document

        text = (
            "---\n"
            "name: No Timestamps\n"
            "description: No timestamp fields\n"
            "---\n"
            "# Content\n"
        )
        doc = parse_document("test.md", text)
        assert doc.created_at is None
        assert doc.updated_at is None

    def test_created_at_only(self) -> None:
        """Only created_at without updated_at works."""
        from wos.document import parse_document

        text = (
            "---\n"
            "name: Created Only\n"
            "description: Has only created_at\n"
            "created_at: 2026-01-15\n"
            "---\n"
            "# Content\n"
        )
        doc = parse_document("test.md", text)
        assert doc.created_at == "2026-01-15"
        assert doc.updated_at is None
