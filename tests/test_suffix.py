"""Tests for wos.suffix — typed file suffix utilities."""

from pathlib import Path

from wos.suffix import is_markdown, stem_name, type_from_path


class TestTypeFromPath:
    """type_from_path extracts type from compound suffixes."""

    def test_research_suffix(self):
        assert type_from_path(Path("api-latency.research.md")) == "research"

    def test_plan_suffix(self):
        assert type_from_path(Path("2026-03-13-deploy.plan.md")) == "plan"

    def test_design_suffix(self):
        assert type_from_path(Path("composable-pipeline.design.md")) == "design"

    def test_context_suffix(self):
        assert type_from_path(Path("architecture.context.md")) == "context"

    def test_prompt_suffix(self):
        assert type_from_path(Path("refine-instructions.prompt.md")) == "prompt"

    def test_plain_md_returns_none(self):
        assert type_from_path(Path("plain-document.md")) is None

    def test_non_markdown_returns_none(self):
        assert type_from_path(Path("notes.txt")) is None

    def test_unknown_compound_suffix_returns_none(self):
        assert type_from_path(Path("data.csv.md")) is None

    def test_full_path_uses_name_only(self):
        assert type_from_path(Path("docs/research/api.research.md")) == "research"

    def test_index_file_returns_none(self):
        assert type_from_path(Path("_index.md")) is None


class TestIsMarkdown:
    """is_markdown recognizes both plain and compound suffixes."""

    def test_plain_md(self):
        assert is_markdown(Path("readme.md")) is True

    def test_compound_md(self):
        assert is_markdown(Path("api.research.md")) is True

    def test_non_markdown(self):
        assert is_markdown(Path("script.py")) is False

    def test_index_file(self):
        assert is_markdown(Path("_index.md")) is True


class TestStemName:
    """stem_name strips .md and .type.md suffixes."""

    def test_plain_md(self):
        assert stem_name(Path("plain-document.md")) == "plain-document"

    def test_research_suffix(self):
        assert stem_name(Path("api-latency.research.md")) == "api-latency"

    def test_plan_suffix(self):
        assert stem_name(Path("2026-03-13-deploy.plan.md")) == "2026-03-13-deploy"

    def test_unknown_compound_keeps_middle(self):
        assert stem_name(Path("data.csv.md")) == "data.csv"

    def test_date_prefixed(self):
        path = Path("2026-03-13-cross-platform.design.md")
        assert stem_name(path) == "2026-03-13-cross-platform"
