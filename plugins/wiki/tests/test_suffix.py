"""Tests for Document.type_from_path — typed file suffix utilities."""

from pathlib import Path

from wiki.document import Document


class TestTypeFromPath:
    """type_from_path extracts type from compound suffixes."""

    def test_research_suffix(self):
        assert Document.type_from_path(Path("api-latency.research.md")) == "research"

    def test_plan_suffix(self):
        assert Document.type_from_path(Path("deploy.plan.md")) == "plan"

    def test_design_suffix(self):
        assert Document.type_from_path(
            Path("composable-pipeline.design.md")
        ) == "design"

    def test_prompt_suffix(self):
        assert Document.type_from_path(
            Path("refine-instructions.prompt.md")
        ) == "prompt"

    def test_plain_md_returns_none(self):
        assert Document.type_from_path(Path("plain-document.md")) is None

    def test_non_markdown_returns_none(self):
        assert Document.type_from_path(Path("notes.txt")) is None

    def test_unknown_compound_suffix_returns_none(self):
        assert Document.type_from_path(Path("data.csv.md")) is None

    def test_full_path_uses_name_only(self):
        assert Document.type_from_path(
            Path("docs/research/api.research.md")
        ) == "research"

    def test_index_file_returns_none(self):
        assert Document.type_from_path(Path("_index.md")) is None
