"""Tests for wos/research/assess_research.py."""

from __future__ import annotations


class TestAssessFile:
    """Tests for assess_file() — single document assessment."""

    def test_assess_minimal_research_doc(self, tmp_path) -> None:
        """Minimal research doc returns expected structural facts."""
        from wos.research.assess_research import assess_file

        doc = tmp_path / "test.md"
        doc.write_text(
            "---\n"
            "name: Test Research\n"
            "description: A test research document\n"
            "type: research\n"
            "sources:\n"
            "  - https://example.com/source-1\n"
            "  - https://example.com/source-2\n"
            "---\n"
            "# Test Research\n"
            "\n"
            "Some content here about the topic.\n"
        )
        result = assess_file(str(doc))

        assert result["file"] == str(doc)
        assert result["exists"] is True
        assert result["frontmatter"]["name"] == "Test Research"
        assert result["frontmatter"]["description"] == "A test research document"
        assert result["frontmatter"]["type"] == "research"
        assert result["frontmatter"]["sources_count"] == 2
        assert result["frontmatter"]["related_count"] == 0
        assert result["content"]["word_count"] > 0
        assert result["content"]["draft_marker_present"] is False
        assert result["sources"]["total"] == 2
        assert "https://example.com/source-1" in result["sources"]["urls"]

    def test_assess_doc_with_draft_marker(self, tmp_path) -> None:
        """Draft marker is detected in content."""
        from wos.research.assess_research import assess_file

        doc = tmp_path / "draft.md"
        doc.write_text(
            "---\n"
            "name: Draft Research\n"
            "description: A draft\n"
            "type: research\n"
            "---\n"
            "<!-- DRAFT -->\n"
            "# Draft Research\n"
            "\n"
            "Work in progress.\n"
        )
        result = assess_file(str(doc))
        assert result["content"]["draft_marker_present"] is True

    def test_assess_doc_with_sections(self, tmp_path) -> None:
        """Section detection finds claims, synthesis, sources, findings headings."""
        from wos.research.assess_research import assess_file

        doc = tmp_path / "full.md"
        doc.write_text(
            "---\n"
            "name: Full Research\n"
            "description: Complete research\n"
            "type: research\n"
            "sources:\n"
            "  - https://example.com/a\n"
            "---\n"
            "# Full Research\n"
            "\n"
            "## Findings\n"
            "\n"
            "Some findings here.\n"
            "\n"
            "## Claims\n"
            "\n"
            "| Claim | Status |\n"
            "| claim 1 | verified |\n"
            "\n"
            "## Sources\n"
            "\n"
            "Source list here.\n"
        )
        result = assess_file(str(doc))
        assert result["content"]["has_sections"]["findings"] is True
        assert result["content"]["has_sections"]["claims"] is True
        assert result["content"]["has_sections"]["sources"] is True
        assert result["content"]["has_sections"]["synthesis"] is False

    def test_assess_doc_with_synthesis_section(self, tmp_path) -> None:
        """Synthesis section is detected."""
        from wos.research.assess_research import assess_file

        doc = tmp_path / "synth.md"
        doc.write_text(
            "---\n"
            "name: Synth Research\n"
            "description: Has synthesis\n"
            "type: research\n"
            "---\n"
            "## Synthesis\n"
            "\n"
            "Synthesized findings.\n"
        )
        result = assess_file(str(doc))
        assert result["content"]["has_sections"]["synthesis"] is True

    def test_assess_nonexistent_file(self) -> None:
        """Non-existent file returns exists=False with null fields."""
        from wos.research.assess_research import assess_file

        result = assess_file("/nonexistent/path/doc.md")
        assert result["file"] == "/nonexistent/path/doc.md"
        assert result["exists"] is False
        assert result["frontmatter"] is None
        assert result["content"] is None
        assert result["sources"] is None

    def test_assess_doc_with_related(self, tmp_path) -> None:
        """Related field count is reported."""
        from wos.research.assess_research import assess_file

        doc = tmp_path / "related.md"
        doc.write_text(
            "---\n"
            "name: Related Research\n"
            "description: Has related docs\n"
            "type: research\n"
            "related:\n"
            "  - docs/research/other.md\n"
            "  - docs/context/topic.md\n"
            "---\n"
            "# Related Research\n"
            "\n"
            "Content.\n"
        )
        result = assess_file(str(doc))
        assert result["frontmatter"]["related_count"] == 2

    def test_assess_doc_with_non_url_sources(self, tmp_path) -> None:
        """Sources that aren't URLs are counted separately."""
        from wos.research.assess_research import assess_file

        doc = tmp_path / "mixed.md"
        doc.write_text(
            "---\n"
            "name: Mixed Sources\n"
            "description: Has URL and non-URL sources\n"
            "type: research\n"
            "sources:\n"
            "  - https://example.com/url-source\n"
            "  - Book: Some Reference Book\n"
            "---\n"
            "# Mixed Sources\n"
            "\n"
            "Content.\n"
        )
        result = assess_file(str(doc))
        assert result["sources"]["total"] == 2
        assert result["sources"]["urls"] == ["https://example.com/url-source"]
        assert result["sources"]["non_url_count"] == 1


class TestScanDirectory:
    """Tests for scan_directory() — research directory discovery."""

    def _make_research_doc(
        self, path, name, draft=False,
        sources_count=0, word_count_target=100,
    ):
        """Helper to create a research doc with controlled properties."""
        sources = "".join(
            f"  - https://example.com/source-{i}\n"
            for i in range(sources_count)
        )
        sources_block = f"sources:\n{sources}" if sources_count > 0 else ""
        draft_marker = "<!-- DRAFT -->\n" if draft else ""
        words = " ".join(["word"] * word_count_target)
        path.write_text(
            f"---\n"
            f"name: {name}\n"
            f"description: Research about {name}\n"
            f"type: research\n"
            f"{sources_block}"
            f"---\n"
            f"{draft_marker}"
            f"# {name}\n"
            f"\n"
            f"{words}\n"
        )

    def test_scan_finds_research_docs(self, tmp_path) -> None:
        """Scan returns all type:research docs in the directory."""
        from wos.research.assess_research import scan_directory

        research_dir = tmp_path / "docs" / "research"
        research_dir.mkdir(parents=True)
        self._make_research_doc(
            research_dir / "2026-03-01-topic-a.md", "Topic A", sources_count=3
        )
        self._make_research_doc(
            research_dir / "2026-03-02-topic-b.md", "Topic B",
            draft=True, sources_count=7,
        )

        result = scan_directory(str(tmp_path))

        assert result["directory"] == str(research_dir)
        assert len(result["documents"]) == 2
        names = {d["name"] for d in result["documents"]}
        assert names == {"Topic A", "Topic B"}

    def test_scan_skips_non_research_docs(self, tmp_path) -> None:
        """Scan ignores documents without type:research."""
        from wos.research.assess_research import scan_directory

        research_dir = tmp_path / "docs" / "research"
        research_dir.mkdir(parents=True)
        self._make_research_doc(
            research_dir / "2026-03-01-topic.md", "Topic", sources_count=1
        )
        # Non-research doc
        (research_dir / "not-research.md").write_text(
            "---\n"
            "name: Not Research\n"
            "description: A context doc\n"
            "type: context\n"
            "---\n"
            "# Not Research\n"
        )

        result = scan_directory(str(tmp_path))
        assert len(result["documents"]) == 1
        assert result["documents"][0]["name"] == "Topic"

    def test_scan_skips_index_files(self, tmp_path) -> None:
        """Scan ignores _index.md files."""
        from wos.research.assess_research import scan_directory

        research_dir = tmp_path / "docs" / "research"
        research_dir.mkdir(parents=True)
        self._make_research_doc(
            research_dir / "2026-03-01-topic.md", "Topic", sources_count=1
        )
        (research_dir / "_index.md").write_text(
            "# Research Index\n\nAuto-generated.\n"
        )

        result = scan_directory(str(tmp_path))
        assert len(result["documents"]) == 1

    def test_scan_empty_directory(self, tmp_path) -> None:
        """Scan of empty directory returns empty documents list."""
        from wos.research.assess_research import scan_directory

        research_dir = tmp_path / "docs" / "research"
        research_dir.mkdir(parents=True)

        result = scan_directory(str(tmp_path))
        assert result["documents"] == []

    def test_scan_missing_directory(self, tmp_path) -> None:
        """Scan when docs/research doesn't exist returns empty documents list."""
        from wos.research.assess_research import scan_directory

        result = scan_directory(str(tmp_path))
        assert result["documents"] == []

    def test_scan_custom_subdir(self, tmp_path) -> None:
        """Scan with custom subdir parameter."""
        from wos.research.assess_research import scan_directory

        custom_dir = tmp_path / "custom" / "path"
        custom_dir.mkdir(parents=True)
        self._make_research_doc(
            custom_dir / "2026-03-01-topic.md", "Custom Topic", sources_count=2
        )

        result = scan_directory(str(tmp_path), subdir="custom/path")
        assert len(result["documents"]) == 1
        assert result["documents"][0]["name"] == "Custom Topic"

    def test_scan_document_summary_fields(self, tmp_path) -> None:
        """Scan returns correct summary fields per document."""
        from wos.research.assess_research import scan_directory

        research_dir = tmp_path / "docs" / "research"
        research_dir.mkdir(parents=True)
        self._make_research_doc(
            research_dir / "2026-03-01-topic.md",
            "Topic",
            draft=True,
            sources_count=5,
            word_count_target=200,
        )

        result = scan_directory(str(tmp_path))
        doc = result["documents"][0]
        assert doc["name"] == "Topic"
        assert doc["draft_marker_present"] is True
        assert doc["word_count"] > 0
        assert doc["sources_count"] == 5
        assert "file" in doc
