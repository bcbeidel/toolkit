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

        # Create AGENTS.md with managed-section markers
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

    def test_preserves_existing_area_descriptions(self, tmp_path: Path) -> None:
        # AGENTS.md already has a human-written Areas table
        existing_area_desc = "How agents plan tasks and decompose work"
        agents_path = tmp_path / "AGENTS.md"
        agents_path.write_text(
            f"# AGENTS.md\n\n"
            f"{BEGIN_MARKER}\n"
            f"### Areas\n"
            f"| Area | Path |\n"
            f"|------|------|\n"
            f"| {existing_area_desc} | docs/context/planning |\n"
            f"{END_MARKER}\n"
        )

        # A directory exists on disk that is NOT in the existing AGENTS.md
        extra_dir = tmp_path / "docs" / "context" / "api"
        extra_dir.mkdir(parents=True)
        (extra_dir / "endpoints.md").write_text(
            "---\nname: Endpoints\ndescription: API endpoints\n---\n"
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
        # Human-written description preserved
        assert existing_area_desc in content
        assert "**Directness:**" in content
        # Directory on disk that wasn't in AGENTS.md should NOT be added
        assert "docs/context/api" not in content

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
