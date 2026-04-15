"""Tests for wos/document.py — Document base class, subclasses, and Document.parse()."""

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

    def test_all_fields(self) -> None:
        from wos.document import Document

        doc = Document(
            path="docs/research/api-review.md",
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


# ── Document.parse (factory) ────────────────────────────────────


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
        doc = parse_document("docs/research/api-review.md", text)
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
        doc = parse_document("docs/plans/deploy.plan.md", text)
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
        doc = parse_document("docs/designs/feature.design.md", text)
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


# ── Document.word_count ──────────────────────────────────────────


class TestWordCount:
    def test_counts_words_in_content(self) -> None:
        from wos.document import Document

        doc = Document(path="a.md", name="A", description="D",
                       content="one two three four five")
        assert doc.word_count == 5

    def test_empty_content_is_zero(self) -> None:
        from wos.document import Document

        doc = Document(path="a.md", name="A", description="D", content="")
        assert doc.word_count == 0


# ── Document.has_section ─────────────────────────────────────────


class TestHasSection:
    def test_finds_matching_heading(self) -> None:
        from wos.document import Document

        doc = Document(path="a.md", name="A", description="D",
                       content="## Findings\n\nSome text.\n")
        assert doc.has_section("findings") is True

    def test_returns_false_when_absent(self) -> None:
        from wos.document import Document

        doc = Document(path="a.md", name="A", description="D",
                       content="## Goals\n\nSome text.\n")
        assert doc.has_section("findings") is False

    def test_case_insensitive(self) -> None:
        from wos.document import Document

        doc = Document(path="a.md", name="A", description="D",
                       content="## FINDINGS\n\nText.\n")
        assert doc.has_section("findings") is True

    def test_any_heading_level(self) -> None:
        from wos.document import Document

        doc = Document(path="a.md", name="A", description="D",
                       content="#### File Changes\n\nText.\n")
        assert doc.has_section("file changes") is True

    def test_keyword_in_body_not_heading_is_false(self) -> None:
        from wos.document import Document

        doc = Document(path="a.md", name="A", description="D",
                       content="Some findings in a paragraph.\n")
        assert doc.has_section("findings") is False

    def test_empty_content_is_false(self) -> None:
        from wos.document import Document

        doc = Document(path="a.md", name="A", description="D", content="")
        assert doc.has_section("findings") is False


# ── Document.issues + is_valid ───────────────────────────────────


class TestDocumentIssues:
    def test_valid_document_no_issues(self, tmp_path) -> None:
        from wos.document import Document

        doc = Document(path="a.md", name="Valid", description="Desc", content="")
        assert doc.issues(tmp_path) == []

    def test_empty_name_is_fail(self, tmp_path) -> None:
        from wos.document import Document

        doc = Document(path="a.md", name="", description="Desc", content="")
        result = doc.issues(tmp_path)
        assert any(i["severity"] == "fail" and "name" in i["issue"] for i in result)

    def test_whitespace_name_is_fail(self, tmp_path) -> None:
        from wos.document import Document

        doc = Document(path="a.md", name="   ", description="Desc", content="")
        result = doc.issues(tmp_path)
        assert any(i["severity"] == "fail" and "name" in i["issue"] for i in result)

    def test_empty_description_is_fail(self, tmp_path) -> None:
        from wos.document import Document

        doc = Document(path="a.md", name="Name", description="", content="")
        result = doc.issues(tmp_path)
        assert any(
            i["severity"] == "fail" and "description" in i["issue"] for i in result
        )

    def test_missing_related_path_is_fail(self, tmp_path) -> None:
        from wos.document import Document

        doc = Document(
            path="a.md", name="N", description="D", content="",
            related=["docs/context/missing.md"],
        )
        result = doc.issues(tmp_path)
        assert any(
            i["severity"] == "fail" and "missing.md" in i["issue"] for i in result
        )

    def test_existing_related_path_no_issue(self, tmp_path) -> None:
        from wos.document import Document

        target = tmp_path / "docs" / "context" / "present.md"
        target.parent.mkdir(parents=True)
        target.write_text("exists")
        doc = Document(
            path="a.md", name="N", description="D", content="",
            related=["docs/context/present.md"],
        )
        assert doc.issues(tmp_path) == []

    def test_url_in_related_skipped(self, tmp_path) -> None:
        from wos.document import Document

        doc = Document(
            path="a.md", name="N", description="D", content="",
            related=["https://example.com/ref"],
        )
        assert doc.issues(tmp_path) == []


class TestDocumentIsValid:
    def test_valid_doc_returns_true(self, tmp_path) -> None:
        from wos.document import Document

        doc = Document(path="a.md", name="N", description="D", content="")
        assert doc.is_valid(tmp_path) is True

    def test_fail_issue_returns_false(self, tmp_path) -> None:
        from wos.document import Document

        doc = Document(path="a.md", name="", description="D", content="")
        assert doc.is_valid(tmp_path) is False


# ── Factory routing ──────────────────────────────────────────────


class TestFactoryRouting:
    def test_research_type_returns_research_document(self) -> None:
        from wos.document import ResearchDocument, parse_document

        text = (
            "---\nname: T\ndescription: D\ntype: research\n"
            "sources:\n- https://example.com\n---\nbody\n"
        )
        doc = parse_document("x.md", text)
        assert isinstance(doc, ResearchDocument)

    def test_plan_type_returns_plan_document(self) -> None:
        from wos.document import PlanDocument, parse_document

        text = (
            "---\nname: T\ndescription: D\ntype: plan\nstatus: draft\n---\n"
            "## Tasks\n\n- [ ] Task 1: Do thing\n"
        )
        doc = parse_document("x.md", text)
        assert isinstance(doc, PlanDocument)

    def test_unknown_type_returns_base_document(self) -> None:
        from wos.document import Document, parse_document

        text = "---\nname: T\ndescription: D\ntype: custom\n---\nbody\n"
        doc = parse_document("x.md", text)
        assert type(doc) is Document

    def test_no_type_returns_base_document(self) -> None:
        from wos.document import Document, parse_document

        text = "---\nname: T\ndescription: D\n---\nbody\n"
        doc = parse_document("x.md", text)
        assert type(doc) is Document

    def test_parse_classmethod_equivalent_to_alias(self) -> None:
        from wos.document import Document, parse_document

        text = "---\nname: T\ndescription: D\n---\nbody\n"
        assert Document.parse("x.md", text) is not None
        assert type(parse_document("x.md", text)) is type(Document.parse("x.md", text))

    def test_research_suffix_returns_research_document(self) -> None:
        from wos.document import ResearchDocument, parse_document

        text = (
            "---\nname: T\ndescription: D\n"
            "sources:\n- https://example.com\n---\nbody\n"
        )
        doc = parse_document("x.research.md", text)
        assert isinstance(doc, ResearchDocument)


# ── ResearchDocument ─────────────────────────────────────────────


class TestResearchDocumentIssues:
    def test_no_sources_is_fail(self, tmp_path) -> None:
        from wos.document import ResearchDocument

        doc = ResearchDocument(
            path="a.md", name="N", description="D",
            content="body", type="research",
        )
        result = doc.issues(tmp_path, verify_urls=False)
        assert any(i["severity"] == "fail" and "sources" in i["issue"] for i in result)

    def test_draft_marker_is_warn(self, tmp_path) -> None:
        from wos.document import ResearchDocument

        doc = ResearchDocument(
            path="a.md", name="N", description="D",
            content="<!-- DRAFT -->\nbody", type="research",
            sources=["https://example.com"],
        )
        result = doc.issues(tmp_path, verify_urls=False)
        assert any(i["severity"] == "warn" and "DRAFT" in i["issue"] for i in result)

    def test_dict_source_is_warn(self, tmp_path) -> None:
        from wos.document import ResearchDocument

        doc = ResearchDocument(
            path="a.md", name="N", description="D",
            content="body", type="research",
            sources=[{"url": "https://example.com"}],
        )
        result = doc.issues(tmp_path, verify_urls=False)
        assert any(i["severity"] == "warn" and "dict" in i["issue"] for i in result)

    def test_valid_research_doc_no_issues(self, tmp_path) -> None:
        from wos.document import ResearchDocument

        doc = ResearchDocument(
            path="a.md", name="N", description="D",
            content="body", type="research",
            sources=["https://example.com"],
        )
        result = doc.issues(tmp_path, verify_urls=False)
        assert result == []

    def test_inherits_base_related_path_check(self, tmp_path) -> None:
        from wos.document import ResearchDocument

        doc = ResearchDocument(
            path="a.md", name="N", description="D",
            content="body", type="research",
            sources=["https://example.com"],
            related=["missing/path.md"],
        )
        result = doc.issues(tmp_path, verify_urls=False)
        assert any("missing/path.md" in i["issue"] for i in result)


# ── PlanDocument ─────────────────────────────────────────────────


class TestPlanDocument:
    def test_tasks_parsed_from_content(self) -> None:
        from wos.document import PlanDocument

        content = (
            "## Tasks\n\n"
            "- [ ] Task 1: First thing\n"
            "- [x] Task 2: Done thing\n"
        )
        doc = PlanDocument(
            path="p.md", name="N", description="D",
            content=content, type="plan", status="draft",
        )
        assert len(doc.tasks) == 2
        assert doc.tasks[0]["completed"] is False
        assert doc.tasks[1]["completed"] is True

    def test_tasks_complete_all_done(self) -> None:
        from wos.document import PlanDocument

        content = "## Tasks\n\n- [x] Task 1: Done\n- [x] Task 2: Also done\n"
        doc = PlanDocument(
            path="p.md", name="N", description="D",
            content=content, type="plan", status="draft",
        )
        assert doc.tasks_complete() is True

    def test_tasks_complete_some_pending(self) -> None:
        from wos.document import PlanDocument

        content = "## Tasks\n\n- [ ] Task 1: Not done\n- [x] Task 2: Done\n"
        doc = PlanDocument(
            path="p.md", name="N", description="D",
            content=content, type="plan", status="draft",
        )
        assert doc.tasks_complete() is False

    def test_completion_stats(self) -> None:
        from wos.document import PlanDocument

        content = (
            "## Tasks\n\n"
            "- [x] Task 1: Done\n"
            "- [ ] Task 2: Pending\n"
            "- [ ] Task 3: Pending\n"
        )
        doc = PlanDocument(
            path="p.md", name="N", description="D",
            content=content, type="plan", status="draft",
        )
        stats = doc.completion_stats()
        assert stats == {"total": 3, "done": 1, "remaining": 2}

    def test_factory_returns_plan_document_with_tasks(self) -> None:
        from wos.document import PlanDocument, parse_document

        text = (
            "---\nname: My Plan\ndescription: A plan\n"
            "type: plan\nstatus: draft\n---\n"
            "## Tasks\n\n- [ ] Task 1: Do it\n"
        )
        doc = parse_document("plan.md", text)
        assert isinstance(doc, PlanDocument)
        assert len(doc.tasks) == 1


# ── ContextDocument ───────────────────────────────────────────────


class TestContextDocument:
    def _make_context(self, tmp_path, content="body", related=None, path=None):
        from wos.document import ContextDocument
        return ContextDocument(
            path=str(path or (tmp_path / "notes.md")),
            name="N",
            description="D",
            content=content,
            type="context",
            related=related or [],
        )

    # word count checks

    def test_within_range_no_issues(self, tmp_path) -> None:
        doc = self._make_context(tmp_path, content="Word " * 200)
        issues = [i for i in doc.issues(tmp_path) if "word" in i["issue"].lower()]
        assert issues == []

    def test_over_max_warns(self, tmp_path) -> None:
        doc = self._make_context(tmp_path, content="Word " * 900)
        issues = doc.issues(tmp_path)
        word_issues = [i for i in issues if "900" in i["issue"]]
        assert len(word_issues) == 1
        assert word_issues[0]["severity"] == "warn"

    def test_under_min_warns(self, tmp_path) -> None:
        doc = self._make_context(tmp_path, content="Word " * 50)
        issues = doc.issues(tmp_path)
        word_issues = [i for i in issues if "50" in i["issue"]]
        assert len(word_issues) == 1
        assert word_issues[0]["severity"] == "warn"

    def test_exactly_at_max_no_warning(self, tmp_path) -> None:
        doc = self._make_context(tmp_path, content="Word " * 800)
        issues = [i for i in doc.issues(tmp_path) if "threshold" in i["issue"]]
        assert issues == []

    def test_exactly_at_min_no_warning(self, tmp_path) -> None:
        doc = self._make_context(tmp_path, content="Word " * 100)
        issues = [i for i in doc.issues(tmp_path) if "minimum" in i["issue"]]
        assert issues == []

    def test_custom_max_words(self, tmp_path) -> None:
        doc = self._make_context(tmp_path, content="Word " * 500)
        issues = doc.issues(tmp_path, max_words=400)
        assert any("500" in i["issue"] for i in issues)

    def test_custom_min_words(self, tmp_path) -> None:
        doc = self._make_context(tmp_path, content="Word " * 150)
        issues = doc.issues(tmp_path, min_words=200)
        assert any("150" in i["issue"] for i in issues)

    def test_index_file_skips_word_count(self, tmp_path) -> None:
        doc = self._make_context(
            tmp_path, content="Word " * 2000,
            path=tmp_path / "_index.md",
        )
        word_issues = [i for i in doc.issues(tmp_path) if "words" in i["issue"]]
        assert word_issues == []

    # related field checks

    def test_no_related_warns(self, tmp_path) -> None:
        doc = self._make_context(tmp_path, related=[])
        issues = doc.issues(tmp_path)
        assert any("related" in i["issue"].lower() and i["severity"] == "warn"
                   for i in issues)

    def test_with_related_no_warn(self, tmp_path) -> None:
        ref = tmp_path / "ref.md"
        ref.write_text("exists")
        doc = self._make_context(tmp_path, related=["ref.md"])
        issues = doc.issues(tmp_path)
        assert not any("related" in i["issue"].lower() for i in issues)

    # factory routing

    def test_factory_routes_context_type(self) -> None:
        from wos.document import ContextDocument, parse_document

        text = (
            "---\nname: T\ndescription: D\ntype: context\n"
            "related:\n  - https://example.com\n---\nbody\n"
        )
        doc = parse_document("notes.md", text)
        assert isinstance(doc, ContextDocument)

    def test_factory_routes_context_suffix(self) -> None:
        from wos.document import ContextDocument, parse_document

        text = "---\nname: T\ndescription: D\n---\nbody\n"
        doc = parse_document("notes.context.md", text)
        assert isinstance(doc, ContextDocument)

