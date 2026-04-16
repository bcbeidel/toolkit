"""Tests for scripts/update_preferences.py."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from wiki.agents_md import BEGIN_MARKER, END_MARKER

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"


class TestUpdatePreferencesHelp:
    def test_no_args_shows_usage(self, tmp_path: Path) -> None:
        result = subprocess.run(
            [sys.executable, str(SCRIPTS_DIR / "update_preferences.py")],
            capture_output=True,
            text=True,
            cwd=str(tmp_path),
        )
        assert result.returncode != 0
        assert "usage" in result.stderr.lower()


class TestUpdatePreferencesWritesAgentsMd:
    def test_writes_preferences_to_agents_md(self, tmp_path: Path) -> None:
        # Set up minimal project structure
        docs_dir = tmp_path / "docs" / "context"
        docs_dir.mkdir(parents=True)

        # Create AGENTS.md with WOS markers
        agents_path = tmp_path / "AGENTS.md"
        agents_path.write_text(
            f"# AGENTS.md\n\n{BEGIN_MARKER}\nold\n{END_MARKER}\n"
        )

        result = subprocess.run(
            [
                sys.executable, str(SCRIPTS_DIR / "update_preferences.py"),
                "--root", str(tmp_path),
                "directness=blunt", "tone=casual",
            ],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0

        content = agents_path.read_text()
        assert "### Preferences" in content
        assert "**Directness:**" in content
        assert "**Tone:**" in content
        assert BEGIN_MARKER in content
        assert END_MARKER in content

    def test_preserves_areas(self, tmp_path: Path) -> None:
        # Set up project with an area containing a managed doc
        area_dir = tmp_path / "docs" / "context" / "api"
        area_dir.mkdir(parents=True)
        (area_dir / "endpoints.md").write_text(
            "---\nname: Endpoints\ndescription: API endpoints\n---\n"
        )

        agents_path = tmp_path / "AGENTS.md"
        agents_path.write_text(
            f"# AGENTS.md\n\n{BEGIN_MARKER}\nold\n{END_MARKER}\n"
        )

        result = subprocess.run(
            [
                sys.executable, str(SCRIPTS_DIR / "update_preferences.py"),
                "--root", str(tmp_path),
                "directness=blunt",
            ],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0

        content = agents_path.read_text()
        assert "docs/context/api" in content
        assert "**Directness:**" in content

    def test_creates_agents_md_if_missing(self, tmp_path: Path) -> None:
        docs_dir = tmp_path / "docs" / "context"
        docs_dir.mkdir(parents=True)

        result = subprocess.run(
            [
                sys.executable, str(SCRIPTS_DIR / "update_preferences.py"),
                "--root", str(tmp_path),
                "verbosity=terse",
            ],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0

        agents_path = tmp_path / "AGENTS.md"
        assert agents_path.exists()
        content = agents_path.read_text()
        assert "**Verbosity:**" in content
        assert BEGIN_MARKER in content
