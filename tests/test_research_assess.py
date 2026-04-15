"""Tests for wos/research/assess_research.py."""

from __future__ import annotations

# --- Fixtures for gate check tests -----------------------------------------

# Complete research doc that passes all gates.
_COMPLETE_DOC = """\
---
name: Complete Research
description: A fully completed research document
type: research
sources:
  - https://example.com/source-1
  - https://example.com/source-2
---

# Complete Research

## Findings

### How does X work?

X uses a single-threaded model [1][2]. This differs from Y (HIGH — T1 + T3 converge).

> "Verbatim extract from source 1 about the mechanism."

> "Verbatim extract from source 2 confirming the approach."

### What are the limitations?

Limitation A is documented [1]. Limitation B is suspected (MODERATE — T3 only).

## Challenge

### Assumptions Check

| Assumption | Evidence | Counter | Impact |
|---|---|---|---|
| X is single-threaded | [1][2] | None found | Low |

No disconfirming evidence found for the core claims.

## Claims

| # | Claim | Type | Source | Status |
|---|-------|------|--------|--------|
| 1 | X uses single-threaded model | attribution | [1] | verified |
| 2 | Y uses multi-threaded model | attribution | [2] | verified |
| 3 | X was released in 2020 | statistic | [1] | corrected |

## Sources

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|-----------|------|------|--------|
| 1 | https://example.com/source-1 | Primary doc | Org A | 2024 | T1 | verified |
| 2 | https://example.com/source-2 | Secondary doc | Org B | 2023 | T3 | verified |
"""

# DRAFT doc at gatherer exit: has sources and extracts but no tiers.
_GATHERER_EXIT_DOC = """\
---
name: Draft Research
description: After gathering
type: research
sources:
  - https://example.com/a
---
<!-- DRAFT -->
# Draft Research

### Sub-question 1

> "Extract from source about sub-question 1."

> "Another extract from a different source."

### Sub-question 2

Content about sub-question 2.

## Sources

| # | URL | Title | Author/Org | Date | Status |
|---|-----|-------|-----------|------|--------|
| 1 | https://example.com/a | Source A | Org | 2024 | verified |
"""

# DRAFT doc at evaluator exit: sources have tiers but no challenge.
_EVALUATOR_EXIT_DOC = """\
---
name: Draft Research
description: After evaluation
type: research
sources:
  - https://example.com/a
---
<!-- DRAFT -->
# Draft Research

### Sub-question 1

> "Extract from source."

> "Another extract."

## Sources

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|-----------|------|------|--------|
| 1 | https://example.com/a | Source A | Org | 2024 | T1 | verified |
"""

# DRAFT with unverified claims.
_UNVERIFIED_CLAIMS_DOC = """\
---
name: Draft Research
description: Has unverified claims
type: research
sources:
  - https://example.com/a
---
<!-- DRAFT -->
# Draft Research

### Sub-question 1

> "Extract."

> "Another extract."

## Challenge

Assumptions tested.

## Findings

Key finding here.

## Claims

| # | Claim | Type | Source | Status |
|---|-------|------|--------|--------|
| 1 | Claim A | attribution | [1] | verified |
| 2 | Claim B | statistic | [1] | unverified |

## Sources

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|-----------|------|------|--------|
| 1 | https://example.com/a | Source A | Org | 2024 | T1 | verified |
"""


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
            research_dir / "topic-a.md", "Topic A", sources_count=3
        )
        self._make_research_doc(
            research_dir / "topic-b.md", "Topic B",
            draft=True, sources_count=7,
        )

        result = scan_directory(str(tmp_path))

        assert result["directory"] == str(tmp_path)
        assert len(result["documents"]) == 2
        names = {d["name"] for d in result["documents"]}
        assert names == {"Topic A", "Topic B"}

    def test_scan_skips_non_research_docs(self, tmp_path) -> None:
        """Scan ignores documents without type:research."""
        from wos.research.assess_research import scan_directory

        research_dir = tmp_path / "docs" / "research"
        research_dir.mkdir(parents=True)
        self._make_research_doc(
            research_dir / "topic.md", "Topic", sources_count=1
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
            research_dir / "topic.md", "Topic", sources_count=1
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
            custom_dir / "topic.md", "Custom Topic", sources_count=2
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
            research_dir / "topic.md",
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


class TestCheckGates:
    """Tests for check_gates() — deterministic phase gate validation."""

    def test_complete_doc_passes_all_gates(self, tmp_path) -> None:
        """A fully completed research doc passes all 6 gates."""
        from wos.research.assess_research import check_gates

        doc = tmp_path / "complete.md"
        doc.write_text(_COMPLETE_DOC)
        result = check_gates(str(doc))

        assert result["current_phase"] == "done"
        for gate_name, gate in result["gates"].items():
            assert gate["pass"] is True, f"{gate_name} should pass"

    def test_gatherer_exit_passes_at_gatherer_stage(self, tmp_path) -> None:
        """Doc at gatherer exit passes gatherer gate, fails evaluator."""
        from wos.research.assess_research import check_gates

        doc = tmp_path / "gathered.md"
        doc.write_text(_GATHERER_EXIT_DOC)
        result = check_gates(str(doc))

        assert result["gates"]["gatherer_exit"]["pass"] is True
        assert result["gates"]["evaluator_exit"]["pass"] is False
        assert result["current_phase"] == "evaluator"

    def test_evaluator_exit_passes_at_evaluator_stage(self, tmp_path) -> None:
        """Doc at evaluator exit passes evaluator gate, fails challenger."""
        from wos.research.assess_research import check_gates

        doc = tmp_path / "evaluated.md"
        doc.write_text(_EVALUATOR_EXIT_DOC)
        result = check_gates(str(doc))

        assert result["gates"]["gatherer_exit"]["pass"] is True
        assert result["gates"]["evaluator_exit"]["pass"] is True
        assert result["gates"]["challenger_exit"]["pass"] is False
        assert result["current_phase"] == "challenger"

    def test_unverified_claims_fail_verifier_gate(self, tmp_path) -> None:
        """Doc with unverified claims fails verifier exit gate."""
        from wos.research.assess_research import check_gates

        doc = tmp_path / "unverified.md"
        doc.write_text(_UNVERIFIED_CLAIMS_DOC)
        result = check_gates(str(doc))

        verifier = result["gates"]["verifier_exit"]
        assert verifier["pass"] is False
        assert verifier["checks"]["no_unverified_claims"] is False
        assert verifier["checks"]["claims_section_exists"] is True

    def test_nonexistent_file_fails_all_gates(self) -> None:
        """Non-existent file fails every gate, current_phase is gatherer."""
        from wos.research.assess_research import check_gates

        result = check_gates("/nonexistent/doc.md")

        assert result["current_phase"] == "gatherer"
        for gate_name, gate in result["gates"].items():
            assert gate["pass"] is False, f"{gate_name} should fail"

    def test_current_phase_stops_at_first_failure(self, tmp_path) -> None:
        """current_phase reflects the phase after the highest passing gate."""
        from wos.research.assess_research import check_gates

        # Doc with challenge but no findings → stops at synthesizer.
        doc = tmp_path / "challenged.md"
        doc.write_text(
            "---\n"
            "name: Challenged\n"
            "description: Has challenge section\n"
            "type: research\n"
            "sources:\n"
            "  - https://example.com/a\n"
            "---\n"
            "<!-- DRAFT -->\n"
            "### Sub-question 1\n\n"
            "> Extract 1\n\n"
            "> Extract 2\n\n"
            "## Sources\n\n"
            "| # | URL | Title | Org | Date | Tier | Status |\n"
            "|---|-----|-------|-----|------|------|--------|\n"
            "| 1 | https://example.com/a | A | Org | 2024 | T1 | verified |\n\n"
            "## Challenge\n\n"
            "Assumptions tested. No counter-evidence found.\n"
        )
        result = check_gates(str(doc))

        assert result["gates"]["gatherer_exit"]["pass"] is True
        assert result["gates"]["evaluator_exit"]["pass"] is True
        assert result["gates"]["challenger_exit"]["pass"] is True
        assert result["gates"]["synthesizer_exit"]["pass"] is False
        assert result["current_phase"] == "synthesizer"

    def test_gatherer_exit_checks_detail(self, tmp_path) -> None:
        """Gatherer exit gate checks individual conditions."""
        from wos.research.assess_research import check_gates

        # Minimal doc with no sources table or extracts.
        doc = tmp_path / "empty.md"
        doc.write_text(
            "---\n"
            "name: Empty\n"
            "description: No content\n"
            "type: research\n"
            "---\n"
            "# Empty\n\n"
            "Just a paragraph.\n"
        )
        result = check_gates(str(doc))

        gatherer = result["gates"]["gatherer_exit"]
        assert gatherer["pass"] is False
        assert gatherer["checks"]["sources_section_present"] is False
        assert gatherer["checks"]["sources_have_urls"] is False
        assert gatherer["checks"]["extracts_present"] is False


class TestCheckSingleGate:
    """Tests for check_single_gate() — individual gate queries."""

    def test_single_gate_returns_specific_result(self, tmp_path) -> None:
        """check_single_gate returns just the requested gate."""
        from wos.research.assess_research import check_single_gate

        doc = tmp_path / "complete.md"
        doc.write_text(_COMPLETE_DOC)
        result = check_single_gate(str(doc), "evaluator_exit")

        assert result["gate"] == "evaluator_exit"
        assert result["pass"] is True
        assert "checks" in result
        assert "current_phase" in result

    def test_single_gate_all_returns_full_result(self, tmp_path) -> None:
        """check_single_gate with 'all' returns the full gates dict."""
        from wos.research.assess_research import check_single_gate

        doc = tmp_path / "complete.md"
        doc.write_text(_COMPLETE_DOC)
        result = check_single_gate(str(doc), "all")

        assert "gates" in result
        assert len(result["gates"]) == 6

    def test_unknown_gate_returns_error(self, tmp_path) -> None:
        """Unknown gate name returns an error dict."""
        from wos.research.assess_research import check_single_gate

        doc = tmp_path / "complete.md"
        doc.write_text(_COMPLETE_DOC)
        result = check_single_gate(str(doc), "bogus_gate")

        assert "error" in result
        assert "valid_gates" in result
