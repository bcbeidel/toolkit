"""Tests for scripts/deploy.py — cross-platform skill deployment."""

from __future__ import annotations

from pathlib import Path

from scripts.deploy import (
    deploy,
    discover_files,
    should_exclude,
)


class TestShouldExclude:
    def test_excludes_pycache_dir(self) -> None:
        assert should_exclude(Path("wos/__pycache__/document.cpython-39.pyc"))

    def test_excludes_pyc_files(self) -> None:
        assert should_exclude(Path("wos/document.pyc"))

    def test_allows_normal_python(self) -> None:
        assert not should_exclude(Path("scripts/audit.py"))

    def test_allows_normal_markdown(self) -> None:
        assert not should_exclude(Path("skills/audit/SKILL.md"))


class TestDiscoverFiles:
    def test_finds_expected_source_files(self) -> None:
        plugin_root = Path(__file__).resolve().parent.parent
        files = discover_files(plugin_root)
        names = {f.name for f in files}
        assert "audit.py" in names
        assert "SKILL.md" in names
        assert "__init__.py" in names


class TestDeploy:
    def test_creates_agents_directory_structure(self, tmp_path: Path) -> None:
        plugin_root = Path(__file__).resolve().parent.parent
        deploy(plugin_root, tmp_path)

        agents = tmp_path / ".agents"
        assert (agents / "wos" / "__init__.py").exists()
        assert (agents / "scripts" / "audit.py").exists()
        assert (agents / "skills" / "audit" / "SKILL.md").exists()

    def test_idempotent(self, tmp_path: Path) -> None:
        plugin_root = Path(__file__).resolve().parent.parent
        actions1 = deploy(plugin_root, tmp_path)
        actions2 = deploy(plugin_root, tmp_path)
        assert actions1 == actions2

    def test_dry_run_writes_nothing(self, tmp_path: Path) -> None:
        plugin_root = Path(__file__).resolve().parent.parent
        actions = deploy(plugin_root, tmp_path, dry_run=True)

        assert len(actions) > 0
        assert not (tmp_path / ".agents").exists()

    def test_preserves_directory_structure(self, tmp_path: Path) -> None:
        plugin_root = Path(__file__).resolve().parent.parent
        deploy(plugin_root, tmp_path)

        agents = tmp_path / ".agents"
        # skills/, scripts/, wos/ should be siblings under .agents/
        assert (agents / "skills").is_dir()
        assert (agents / "scripts").is_dir()
        assert (agents / "wos").is_dir()

    def test_deployed_source_matches_original(self, tmp_path: Path) -> None:
        """Verify deployed files are identical copies (no transforms)."""
        plugin_root = Path(__file__).resolve().parent.parent
        deploy(plugin_root, tmp_path)

        agents = tmp_path / ".agents"
        skill_src = plugin_root / "skills" / "audit" / "SKILL.md"
        skill_dst = agents / "skills" / "audit" / "SKILL.md"
        assert skill_src.read_text() == skill_dst.read_text()
