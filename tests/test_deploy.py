"""Tests for scripts/deploy.py — cross-platform skill deployment."""

from __future__ import annotations

from pathlib import Path

from scripts.deploy import (
    deploy,
    discover_files,
    should_exclude,
    transform_markdown,
)


class TestShouldExclude:
    def test_excludes_check_runtime(self) -> None:
        assert should_exclude(Path("scripts/check_runtime.py"))

    def test_excludes_preflight(self) -> None:
        assert should_exclude(Path("skills/_shared/references/preflight.md"))

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

    def test_excludes_check_runtime(self) -> None:
        plugin_root = Path(__file__).resolve().parent.parent
        files = discover_files(plugin_root)
        names = {f.name for f in files}
        assert "check_runtime.py" not in names

    def test_excludes_preflight(self) -> None:
        plugin_root = Path(__file__).resolve().parent.parent
        files = discover_files(plugin_root)
        paths = {str(f) for f in files}
        assert not any("preflight.md" in p for p in paths)


class TestTransformMarkdown:
    def test_rewrites_uv_run(self) -> None:
        content = "```bash\nuv run scripts/audit.py --root .\n```"
        result = transform_markdown(content)
        assert "uv run" not in result
        assert "python scripts/audit.py --root ." in result

    def test_preserves_uv_in_non_run_context(self) -> None:
        content = "Install uv with curl"
        result = transform_markdown(content)
        assert "Install uv with curl" in result

    def test_strips_preflight_reference_from_frontmatter(self) -> None:
        content = (
            "---\nreferences:\n"
            "  - ../_shared/references/preflight.md\n"
            "  - references/guide.md\n---\n"
        )
        result = transform_markdown(content)
        assert "preflight.md" not in result
        assert "references/guide.md" in result

    def test_strips_preflight_instruction_lines(self) -> None:
        content = (
            "# Skill\n\n"
            "Run the preflight check (per `preflight.md`), then the entry script:\n\n"
            "```bash\nuv run scripts/audit.py\n```\n"
        )
        result = transform_markdown(content)
        assert "preflight check" not in result
        assert "python scripts/audit.py" in result


class TestDeploy:
    def test_creates_agents_directory_structure(self, tmp_path: Path) -> None:
        plugin_root = Path(__file__).resolve().parent.parent
        deploy(plugin_root, tmp_path)

        agents = tmp_path / ".agents"
        assert (agents / "wos" / "__init__.py").exists()
        assert (agents / "scripts" / "audit.py").exists()
        assert (agents / "skills" / "audit" / "SKILL.md").exists()

    def test_excludes_check_runtime_and_preflight(self, tmp_path: Path) -> None:
        plugin_root = Path(__file__).resolve().parent.parent
        deploy(plugin_root, tmp_path)

        agents = tmp_path / ".agents"
        all_files = [f.name for f in agents.rglob("*") if f.is_file()]
        assert "check_runtime.py" not in all_files
        assert "preflight.md" not in all_files

    def test_no_uv_run_in_deployed_markdown(self, tmp_path: Path) -> None:
        plugin_root = Path(__file__).resolve().parent.parent
        deploy(plugin_root, tmp_path)

        agents = tmp_path / ".agents"
        for md_file in agents.rglob("*.md"):
            content = md_file.read_text(encoding="utf-8")
            assert "uv run" not in content, f"uv run found in {md_file}"

    def test_no_preflight_in_deployed_skill_frontmatter(self, tmp_path: Path) -> None:
        plugin_root = Path(__file__).resolve().parent.parent
        deploy(plugin_root, tmp_path)

        agents = tmp_path / ".agents"
        for skill_md in agents.glob("skills/*/SKILL.md"):
            content = skill_md.read_text(encoding="utf-8")
            assert "preflight" not in content, f"preflight found in {skill_md}"

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
