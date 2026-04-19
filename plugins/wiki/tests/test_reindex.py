"""Tests for scripts/reindex.py."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from wiki.agents_md import BEGIN_MARKER, END_MARKER

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"


def _run(root: Path, *extra: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / "reindex.py"), "--root", str(root), *extra],
        capture_output=True,
        text=True,
    )


def _make_md(path: Path, name: str = "", description: str = "") -> None:
    fm_lines = ["---", f"name: {name}", f"description: {description}", "---", "Body."]
    path.write_text("\n".join(fm_lines) + "\n", encoding="utf-8")


def _agents_with_areas(
    tmp_path: Path, areas: list[tuple[str, str]]
) -> Path:
    """Write AGENTS.md with a managed section listing the given (desc, path) areas."""
    rows = "\n".join(f"| {desc} | {path} |" for desc, path in areas)
    content = (
        f"# AGENTS.md\n\n"
        f"{BEGIN_MARKER}\n"
        f"### Areas\n"
        f"| Area | Path |\n"
        f"|------|------|\n"
        f"{rows}\n"
        f"{END_MARKER}\n"
    )
    p = tmp_path / "AGENTS.md"
    p.write_text(content, encoding="utf-8")
    return p


class TestReindexFromAreasTable:
    """When AGENTS.md has an areas table, only those dirs are indexed."""

    def test_creates_index_for_registered_area(self, tmp_path: Path) -> None:
        docs = tmp_path / "docs" / "context"
        docs.mkdir(parents=True)
        _make_md(docs / "planning.md", name="Planning", description="How we plan")
        _agents_with_areas(tmp_path, [("How we plan context", "docs/context")])

        result = _run(tmp_path)
        assert result.returncode == 0

        index = docs / "_index.md"
        assert index.exists()
        content = index.read_text()
        assert "| [planning.md](planning.md) | How we plan |" in content

    def test_does_not_index_dirs_outside_areas_table(self, tmp_path: Path) -> None:
        registered = tmp_path / "docs" / "context"
        registered.mkdir(parents=True)
        _make_md(registered / "doc.md", name="Doc", description="A doc")

        unregistered = tmp_path / "plugins" / "src"
        unregistered.mkdir(parents=True)
        _make_md(unregistered / "skill.md", name="Skill", description="A skill")

        _agents_with_areas(tmp_path, [("Context", "docs/context")])

        _run(tmp_path)

        # Registered area gets an index
        assert (registered / "_index.md").exists()
        # Unregistered directory does NOT get an index
        assert not (unregistered / "_index.md").exists()

    def test_index_header_uses_relative_path(self, tmp_path: Path) -> None:
        docs = tmp_path / "docs" / "context"
        docs.mkdir(parents=True)
        _make_md(docs / "topic.md", name="Topic", description="A topic")
        _agents_with_areas(tmp_path, [("Context", "docs/context")])

        _run(tmp_path)

        content = (docs / "_index.md").read_text()
        assert "# docs/context" in content

    def test_index_files_sorted_alphabetically(self, tmp_path: Path) -> None:
        docs = tmp_path / "docs"
        docs.mkdir(parents=True)
        _make_md(docs / "zebra.md", name="Zebra", description="Last")
        _make_md(docs / "alpha.md", name="Alpha", description="First")
        _make_md(docs / "middle.md", name="Middle", description="Middle")
        _agents_with_areas(tmp_path, [("Docs", "docs")])

        _run(tmp_path)

        content = (docs / "_index.md").read_text()
        z_pos = content.index("zebra.md")
        a_pos = content.index("alpha.md")
        m_pos = content.index("middle.md")
        assert a_pos < m_pos < z_pos

    def test_no_index_for_area_dir_with_only_index_file(
        self, tmp_path: Path
    ) -> None:
        """A registered area dir that has only _index.md should not be overwritten."""
        docs = tmp_path / "docs"
        docs.mkdir(parents=True)
        existing = docs / "_index.md"
        existing.write_text("# hand-written\n")
        _agents_with_areas(tmp_path, [("Docs", "docs")])

        _run(tmp_path)

        # No other .md files → _write_index does nothing → hand-written is preserved
        assert existing.read_text() == "# hand-written\n"


class TestReindexFirstRunFallback:
    """When AGENTS.md has no areas, fall back to scanning docs/."""

    def test_scans_docs_subtree_when_no_areas(self, tmp_path: Path) -> None:
        docs = tmp_path / "docs" / "context"
        docs.mkdir(parents=True)
        _make_md(docs / "topic.md", name="Topic", description="A topic")

        # AGENTS.md exists but has no areas table
        (tmp_path / "AGENTS.md").write_text(
            f"# AGENTS.md\n\n{BEGIN_MARKER}\nno areas here\n{END_MARKER}\n"
        )

        result = _run(tmp_path)
        assert result.returncode == 0
        assert (docs / "_index.md").exists()

    def test_reports_nothing_when_no_areas_and_no_docs(
        self, tmp_path: Path
    ) -> None:
        (tmp_path / "AGENTS.md").write_text(
            f"# AGENTS.md\n\n{BEGIN_MARKER}\nno areas\n{END_MARKER}\n"
        )
        result = _run(tmp_path)
        assert result.returncode == 0
        assert "nothing to reindex" in result.stdout


class TestReindexWikiMode:
    """Wiki reindex mode is activated when wiki/SCHEMA.md is present."""

    def _make_schema(self, wiki_dir: Path) -> None:
        (wiki_dir / "SCHEMA.md").write_text(
            "## Page Types\n- concept\n\n"
            "## Confidence Tiers\n- high\n\n"
            "## Relationship Types\n- related_to\n",
            encoding="utf-8",
        )

    def test_subdir_gets_flat_index(self, tmp_path: Path) -> None:
        """A wiki subdir with .md files gets its own _index.md."""
        wiki = tmp_path / "wiki"
        wiki.mkdir()
        self._make_schema(wiki)
        subdir = wiki / "patterns"
        subdir.mkdir()
        _make_md(subdir / "caching.md", name="Caching", description="Cache patterns")
        _agents_with_areas(tmp_path, [("Docs", "docs")])
        (tmp_path / "docs").mkdir()

        _run(tmp_path)

        assert (subdir / "_index.md").exists()
        content = (subdir / "_index.md").read_text()
        assert "caching.md" in content

    def test_root_wiki_index_has_subdir_heading(self, tmp_path: Path) -> None:
        """Root wiki/_index.md has a ## heading for each subdirectory."""
        wiki = tmp_path / "wiki"
        wiki.mkdir()
        self._make_schema(wiki)
        subdir = wiki / "patterns"
        subdir.mkdir()
        _make_md(subdir / "caching.md", name="Caching", description="Cache patterns")
        _agents_with_areas(tmp_path, [("Docs", "docs")])
        (tmp_path / "docs").mkdir()

        _run(tmp_path)

        root_index = wiki / "_index.md"
        assert root_index.exists()
        content = root_index.read_text()
        assert "## patterns" in content

    def test_log_md_not_in_any_index(self, tmp_path: Path) -> None:
        """log.md is excluded from all generated _index.md files."""
        wiki = tmp_path / "wiki"
        wiki.mkdir()
        self._make_schema(wiki)
        (wiki / "log.md").write_text("## [2026-01-01] ingest | Source\n")
        subdir = wiki / "patterns"
        subdir.mkdir()
        _make_md(subdir / "caching.md", name="Caching", description="Cache patterns")
        _agents_with_areas(tmp_path, [("Docs", "docs")])
        (tmp_path / "docs").mkdir()

        _run(tmp_path)

        root_content = (wiki / "_index.md").read_text()
        sub_content = (subdir / "_index.md").read_text()
        assert "log.md" not in root_content
        assert "log.md" not in sub_content

    def test_no_schema_wiki_not_touched(self, tmp_path: Path) -> None:
        """Without wiki/SCHEMA.md, reindex does not touch the wiki/ directory."""
        wiki = tmp_path / "wiki"
        wiki.mkdir()
        wiki_index = wiki / "_index.md"
        original = "# Wiki Index\n\n| Page | Description | File |\n"
        wiki_index.write_text(original)

        docs = tmp_path / "docs"
        docs.mkdir()
        _make_md(docs / "topic.md", name="Topic", description="A topic")
        _agents_with_areas(tmp_path, [("Docs", "docs")])

        _run(tmp_path)

        assert wiki_index.read_text() == original

    def test_wiki_mode_output_message(self, tmp_path: Path) -> None:
        """Reindex prints a wiki subdirectory count when wiki mode activates."""
        wiki = tmp_path / "wiki"
        wiki.mkdir()
        self._make_schema(wiki)
        subdir = wiki / "patterns"
        subdir.mkdir()
        _make_md(subdir / "caching.md", name="Caching", description="Cache patterns")
        _agents_with_areas(tmp_path, [("Docs", "docs")])
        (tmp_path / "docs").mkdir()

        result = _run(tmp_path)

        assert "Wiki:" in result.stdout
        assert "subdirector" in result.stdout


class TestReindexUpdatesAgentsMd:
    def test_preserves_existing_human_descriptions(self, tmp_path: Path) -> None:
        docs = tmp_path / "docs" / "context"
        docs.mkdir(parents=True)
        _make_md(docs / "topic.md", name="Topic", description="A topic")

        human_desc = "How LLM agents plan and execute tasks"
        agents = _agents_with_areas(tmp_path, [(human_desc, "docs/context")])

        _run(tmp_path)

        assert human_desc in agents.read_text()

    def test_skips_areas_update_when_no_agents_md(self, tmp_path: Path) -> None:
        docs = tmp_path / "docs"
        docs.mkdir()
        _make_md(docs / "topic.md", name="Topic", description="A topic")

        result = _run(tmp_path)
        assert result.returncode == 0
        assert "skipping areas update" in result.stdout
        assert not (tmp_path / "AGENTS.md").exists()


class TestReindexOutput:
    def test_reports_count_of_indexed_directories(self, tmp_path: Path) -> None:
        for name in ("alpha", "beta"):
            d = tmp_path / "docs" / name
            d.mkdir(parents=True)
            _make_md(d / "doc.md", name="Doc", description="A doc")
        _agents_with_areas(
            tmp_path,
            [("Alpha", "docs/alpha"), ("Beta", "docs/beta")],
        )

        result = _run(tmp_path)
        assert result.returncode == 0
        assert "2 director" in result.stdout  # "directories"
