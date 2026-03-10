# Per-Skill Entry Scripts Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add a research assessment entry script that reports structural facts about research documents as JSON, prototyping the per-skill scripts pattern.

**Architecture:** New `wos/research/` subpackage with `assess_research.py` containing two functions (`assess_file`, `scan_directory`). Thin CLI wrapper at `skills/research/scripts/research_assess.py` with PEP 723 metadata. TDD throughout.

**Tech Stack:** Python 3.9+ (stdlib only), pytest, existing `wos.document.parse_document()`

---

### Task 1: Create `wos/research/` package

**Files:**
- Create: `wos/research/__init__.py`

**Step 1: Create empty package init**

```python
"""WOS research skill support modules."""
```

**Step 2: Verify import works**

Run: `uv run python -c "import wos.research; print('ok')"`
Expected: `ok`

**Step 3: Commit**

```bash
git add wos/research/__init__.py
git commit -m "feat: create wos.research subpackage"
```

---

### Task 2: `assess_file` — write failing tests

**Files:**
- Create: `tests/test_research_assess.py`
- Create: `wos/research/assess_research.py`

**Step 1: Write tests for `assess_file`**

```python
"""Tests for wos/research/assess_research.py."""

from __future__ import annotations

import pytest


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
```

**Step 2: Run tests to verify they fail**

Run: `uv run python -m pytest tests/test_research_assess.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'wos.research.assess_research'`

**Step 3: Commit failing tests**

```bash
git add tests/test_research_assess.py
git commit -m "test: add failing tests for assess_file"
```

---

### Task 3: Implement `assess_file`

**Files:**
- Create: `wos/research/assess_research.py`

**Step 1: Write implementation**

```python
"""Research document structural assessment.

Reports observable facts about research documents — word count, draft
markers, section presence, source listing. The model infers phase and
next actions from these facts.
"""

from __future__ import annotations

import os
from typing import Dict, List, Optional

from wos.document import parse_document


def assess_file(path: str) -> dict:
    """Assess structural facts of a single research document.

    Args:
        path: Absolute or relative path to a markdown file.

    Returns:
        Dict with keys: file, exists, frontmatter, content, sources.
        If the file doesn't exist, frontmatter/content/sources are None.
    """
    if not os.path.isfile(path):
        return {
            "file": path,
            "exists": False,
            "frontmatter": None,
            "content": None,
            "sources": None,
        }

    text = _read_file(path)
    doc = parse_document(path, text)

    urls, non_url_count = _classify_sources(doc.sources)
    sections = _detect_sections(doc.content)
    word_count = len(doc.content.split())

    return {
        "file": path,
        "exists": True,
        "frontmatter": {
            "name": doc.name,
            "description": doc.description,
            "type": doc.type,
            "sources_count": len(doc.sources),
            "related_count": len(doc.related),
        },
        "content": {
            "word_count": word_count,
            "draft_marker_present": "<!-- DRAFT -->" in doc.content,
            "has_sections": sections,
        },
        "sources": {
            "total": len(doc.sources),
            "urls": urls,
            "non_url_count": non_url_count,
        },
    }


def _read_file(path: str) -> str:
    """Read file content as UTF-8 text."""
    with open(path, encoding="utf-8") as f:
        return f.read()


def _classify_sources(sources: List[str]) -> tuple:
    """Split sources into URLs and non-URLs.

    Returns:
        Tuple of (url_list, non_url_count).
    """
    urls: List[str] = []
    non_url_count = 0
    for source in sources:
        if source.startswith("http://") or source.startswith("https://"):
            urls.append(source)
        else:
            non_url_count += 1
    return urls, non_url_count


_SECTION_KEYWORDS = {
    "claims": "claims",
    "synthesis": "synthesis",
    "sources": "sources",
    "findings": "findings",
}


def _detect_sections(content: str) -> Dict[str, bool]:
    """Detect presence of key sections by heading text.

    Looks for markdown headings (## or ###) containing known keywords.
    """
    found = {key: False for key in _SECTION_KEYWORDS}
    for line in content.split("\n"):
        stripped = line.strip()
        if not stripped.startswith("#"):
            continue
        # Remove leading # characters and whitespace
        heading_text = stripped.lstrip("#").strip().lower()
        for key, keyword in _SECTION_KEYWORDS.items():
            if keyword in heading_text:
                found[key] = True
    return found
```

**Step 2: Run tests to verify they pass**

Run: `uv run python -m pytest tests/test_research_assess.py -v`
Expected: All 7 tests PASS

**Step 3: Commit**

```bash
git add wos/research/assess_research.py
git commit -m "feat: implement assess_file for research documents"
```

---

### Task 4: `scan_directory` — write failing tests

**Files:**
- Modify: `tests/test_research_assess.py`

**Step 1: Add tests for `scan_directory`**

Append to `tests/test_research_assess.py`:

```python
class TestScanDirectory:
    """Tests for scan_directory() — research directory discovery."""

    def _make_research_doc(self, path, name, draft=False, sources_count=0, word_count_target=100):
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
            research_dir / "2026-03-02-topic-b.md", "Topic B", draft=True, sources_count=7
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
```

**Step 2: Run tests to verify the new ones fail**

Run: `uv run python -m pytest tests/test_research_assess.py::TestScanDirectory -v`
Expected: FAIL — `ImportError: cannot import name 'scan_directory'`

**Step 3: Commit**

```bash
git add tests/test_research_assess.py
git commit -m "test: add failing tests for scan_directory"
```

---

### Task 5: Implement `scan_directory`

**Files:**
- Modify: `wos/research/assess_research.py`

**Step 1: Add `scan_directory` function**

Add to `wos/research/assess_research.py` after `assess_file`:

```python
def scan_directory(root: str, subdir: str = "docs/research") -> dict:
    """Scan a directory for research documents and return summaries.

    Args:
        root: Project root directory.
        subdir: Subdirectory relative to root to scan (default: docs/research).

    Returns:
        Dict with keys: directory, documents. Each document has:
        file, name, draft_marker_present, word_count, sources_count.
    """
    scan_path = os.path.join(root, subdir)

    if not os.path.isdir(scan_path):
        return {"directory": scan_path, "documents": []}

    documents: list = []
    for filename in sorted(os.listdir(scan_path)):
        if not filename.endswith(".md") or filename.startswith("_"):
            continue

        file_path = os.path.join(scan_path, filename)
        if not os.path.isfile(file_path):
            continue

        try:
            text = _read_file(file_path)
            doc = parse_document(file_path, text)
        except ValueError:
            continue

        if doc.type != "research":
            continue

        documents.append({
            "file": file_path,
            "name": doc.name,
            "draft_marker_present": "<!-- DRAFT -->" in doc.content,
            "word_count": len(doc.content.split()),
            "sources_count": len(doc.sources),
        })

    return {"directory": scan_path, "documents": documents}
```

**Step 2: Run all tests**

Run: `uv run python -m pytest tests/test_research_assess.py -v`
Expected: All 14 tests PASS

**Step 3: Commit**

```bash
git add wos/research/assess_research.py
git commit -m "feat: implement scan_directory for research doc discovery"
```

---

### Task 6: CLI wrapper script

**Files:**
- Create: `skills/research/scripts/research_assess.py`

**Step 1: Write the CLI wrapper**

```python
#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""Assess research document state for skill resumption.

Usage:
    uv run skills/research/scripts/research_assess.py --file PATH
    uv run skills/research/scripts/research_assess.py --scan [--root DIR] [--subdir PATH]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Ensure `import wos` works whether pip-installed or run from plugin cache.
_plugin_root = Path(__file__).resolve().parent.parent.parent.parent
if str(_plugin_root) not in sys.path:
    sys.path.insert(0, str(_plugin_root))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Assess research document state.",
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--file",
        help="Assess a single research document",
    )
    group.add_argument(
        "--scan",
        action="store_true",
        help="Scan for all research documents",
    )
    parser.add_argument(
        "--root",
        default=".",
        help="Project root directory (default: current directory)",
    )
    parser.add_argument(
        "--subdir",
        default="docs/research",
        help="Subdirectory to scan (default: docs/research)",
    )
    args = parser.parse_args()

    from wos.research.assess_research import assess_file, scan_directory

    if args.file:
        result = assess_file(args.file)
    else:
        root = str(Path(args.root).resolve())
        result = scan_directory(root, subdir=args.subdir)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
```

**Step 2: Test CLI wrapper manually — file mode**

Create a temporary test doc and run the script against it:

Run: `uv run skills/research/scripts/research_assess.py --file /nonexistent/path.md`
Expected: JSON output with `"exists": false`

**Step 3: Test CLI wrapper manually — scan mode**

Run: `uv run skills/research/scripts/research_assess.py --scan --root .`
Expected: JSON output with `"directory"` and `"documents"` keys (documents list may be empty if no research docs exist)

**Step 4: Commit**

```bash
git add skills/research/scripts/research_assess.py
git commit -m "feat: add CLI wrapper for research assessment"
```

---

### Task 7: Update research SKILL.md

**Files:**
- Modify: `skills/research/SKILL.md`

**Step 1: Add preflight reference and entry script guidance**

Add `../_shared/references/preflight.md` to the `references:` list in SKILL.md frontmatter.

Add a new section after the "Mode Detection" section and before "Workflow":

```markdown
## Resumption Assessment

When resuming work on an existing research document, run the assessment
script before proceeding. This reports structural facts (word count, draft
marker, section presence, source count) so you can determine the current
state without re-reading the entire document.

Before running any `uv run` command below, follow the preflight check in
the [preflight reference](../_shared/references/preflight.md).

**Single document (known file):**
```bash
uv run <plugin-skills-dir>/research/scripts/research_assess.py --file <path>
```

**Discovery (what's in progress?):**
```bash
uv run <plugin-skills-dir>/research/scripts/research_assess.py --scan --root .
```

Use the JSON output to determine which phase the document is in and what
actions to take next. Do not re-read the entire document if the assessment
provides sufficient context.
```

**Step 2: Verify the SKILL.md is valid**

Run: `uv run scripts/audit.py --no-urls --root .`
Expected: No new fail-severity issues for `skills/research/SKILL.md`

**Step 3: Commit**

```bash
git add skills/research/SKILL.md
git commit -m "feat: add resumption assessment to research skill"
```

---

### Task 8: Update plan index and run full tests

**Files:**
- Modify: `docs/plans/_index.md` (via reindex)

**Step 1: Regenerate indexes**

Run: `uv run scripts/reindex.py --root .`
Expected: Index files regenerated without errors

**Step 2: Run full test suite**

Run: `uv run python -m pytest tests/ -v`
Expected: All tests pass, including the 14 new research assessment tests

**Step 3: Run audit**

Run: `uv run scripts/audit.py --no-urls --root .`
Expected: No new fail-severity issues

**Step 4: Commit any index changes**

```bash
git add docs/plans/_index.md
git commit -m "chore: regenerate plan index"
```
