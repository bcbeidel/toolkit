"""Tests for scripts/deploy.py — symlink-based skill deployment."""

from __future__ import annotations

from pathlib import Path

from scripts.deploy import (
    PLATFORMS,
    deploy,
    discover_skills,
    resolve_platform_path,
)


class TestDiscoverSkills:
    def test_finds_skill_directories(self) -> None:
        plugin_root = Path(__file__).resolve().parent.parent
        skills = discover_skills(plugin_root)
        assert "audit-wos" in skills
        assert "research" in skills

    def test_excludes_hidden_dirs(self, tmp_path: Path) -> None:
        (tmp_path / "skills" / ".hidden").mkdir(parents=True)
        (tmp_path / "skills" / "visible").mkdir(parents=True)
        skills = discover_skills(tmp_path)
        assert skills == ["visible"]


class TestResolvePlatformPath:
    def test_copilot_path(self) -> None:
        path = resolve_platform_path("copilot")
        assert path == Path.home() / ".copilot"

    def test_all_platforms_resolve(self) -> None:
        for name in PLATFORMS:
            path = resolve_platform_path(name)
            assert path.is_absolute()


class TestDeploy:
    def test_creates_skill_symlinks(self, tmp_path: Path) -> None:
        plugin_root = Path(__file__).resolve().parent.parent
        deploy(plugin_root, tmp_path)

        skills_dir = tmp_path / "skills"
        assert skills_dir.is_dir()
        audit_link = skills_dir / "audit-wos"
        assert audit_link.is_symlink()
        assert audit_link.resolve() == (plugin_root / "skills" / "audit-wos").resolve()
        assert (audit_link / "SKILL.md").exists()

    def test_creates_support_dir_symlinks(self, tmp_path: Path) -> None:
        plugin_root = Path(__file__).resolve().parent.parent
        deploy(plugin_root, tmp_path)

        assert (tmp_path / "scripts").is_symlink()
        assert (tmp_path / "scripts").resolve() == (plugin_root / "scripts").resolve()
        assert (tmp_path / "wos").is_symlink()
        assert (tmp_path / "wos").resolve() == (plugin_root / "wos").resolve()

    def test_idempotent(self, tmp_path: Path) -> None:
        plugin_root = Path(__file__).resolve().parent.parent
        actions1 = deploy(plugin_root, tmp_path)
        actions2 = deploy(plugin_root, tmp_path)
        # Second run should skip all (already linked)
        assert all("skip" in a for a in actions2)
        # But first run should have created links
        assert any("link" in a for a in actions1)

    def test_dry_run_writes_nothing(self, tmp_path: Path) -> None:
        plugin_root = Path(__file__).resolve().parent.parent
        actions = deploy(plugin_root, tmp_path, dry_run=True)

        assert len(actions) > 0
        assert not (tmp_path / "skills").exists()
        assert not (tmp_path / "scripts").exists()

    def test_backs_up_existing_directory(self, tmp_path: Path) -> None:
        plugin_root = Path(__file__).resolve().parent.parent
        # Create a real directory where a symlink will go
        (tmp_path / "scripts").mkdir()
        (tmp_path / "scripts" / "existing.txt").write_text("keep")

        deploy(plugin_root, tmp_path)

        # Original should now be a symlink
        assert (tmp_path / "scripts").is_symlink()
        # Backup should exist
        backups = list(tmp_path.glob("scripts.backup_*"))
        assert len(backups) == 1
        assert (backups[0] / "existing.txt").read_text() == "keep"

    def test_replaces_stale_symlink(self, tmp_path: Path) -> None:
        plugin_root = Path(__file__).resolve().parent.parent
        # Create a symlink pointing to wrong target
        stale_target = tmp_path / "wrong"
        stale_target.mkdir()
        (tmp_path / "scripts").symlink_to(stale_target, target_is_directory=True)

        deploy(plugin_root, tmp_path)

        assert (tmp_path / "scripts").is_symlink()
        assert (tmp_path / "scripts").resolve() == (plugin_root / "scripts").resolve()
