"""Tests for scripts/lint.py — LLM-friendly CLI output."""

from __future__ import annotations

import json
import sys
from io import StringIO
from pathlib import Path
from unittest.mock import patch


def _run_audit(*args: str, issues: list[dict] | None = None) -> tuple[str, str, int]:
    """Run lint.main() with given CLI args, returning (stdout, stderr, exitcode)."""
    captured_stdout = StringIO()
    captured_stderr = StringIO()
    exit_code = 0

    mock_target = "wiki.project.validate_project"

    with patch.object(sys, "argv", ["lint.py", *args]):
        with patch("sys.stdout", captured_stdout), patch("sys.stderr", captured_stderr):
            try:
                if issues is not None:
                    with patch(mock_target, return_value=issues):
                        from scripts.lint import main
                        main()
                else:
                    from scripts.lint import main
                    main()
            except SystemExit as exc:
                exit_code = exc.code if exc.code is not None else 0

    return captured_stdout.getvalue(), captured_stderr.getvalue(), exit_code


class TestSummaryLine:
    def test_summary_shows_fail_and_warn_counts(self, tmp_path: Path) -> None:
        root = tmp_path / "project"
        root.mkdir()
        issues = [
            {"file": str(root / "a.md"), "issue": "Problem A", "severity": "fail"},
            {"file": str(root / "b.md"), "issue": "Problem B", "severity": "warn"},
        ]
        stdout, _, _ = _run_audit("--root", str(root), issues=issues)
        assert "1 fail" in stdout
        assert "1 warn" in stdout

    def test_no_issues_shows_all_passed(self, tmp_path: Path) -> None:
        root = tmp_path / "project"
        root.mkdir()
        stdout, _, _ = _run_audit("--root", str(root), issues=[])
        assert "All checks passed." in stdout


class TestTableFormat:
    def test_output_uses_relative_paths(self, tmp_path: Path) -> None:
        root = tmp_path / "project"
        root.mkdir()
        issues = [
            {
                "file": str(root / "docs" / "context" / "api" / "auth.md"),
                "issue": "Frontmatter 'name' is empty",
                "severity": "fail",
            },
        ]
        stdout, _, _ = _run_audit("--root", str(root), issues=issues)
        assert str(root) not in stdout
        assert "docs/context/api/auth.md" in stdout

    def test_table_has_severity_column(self, tmp_path: Path) -> None:
        root = tmp_path / "project"
        root.mkdir()
        issues = [
            {"file": str(root / "a.md"), "issue": "Problem", "severity": "fail"},
            {"file": str(root / "b.md"), "issue": "Drift", "severity": "warn"},
        ]
        stdout, _, _ = _run_audit("--root", str(root), issues=issues)
        assert "fail" in stdout
        assert "warn" in stdout


class TestExitCodes:
    def test_exit_1_on_fail_issues(self, tmp_path: Path) -> None:
        root = tmp_path / "project"
        root.mkdir()
        issues = [
            {"file": str(root / "a.md"), "issue": "Problem", "severity": "fail"},
        ]
        _, _, code = _run_audit("--root", str(root), issues=issues)
        assert code == 1

    def test_exit_0_on_warn_only(self, tmp_path: Path) -> None:
        root = tmp_path / "project"
        root.mkdir()
        issues = [
            {"file": str(root / "a.md"), "issue": "Drift", "severity": "warn"},
        ]
        _, _, code = _run_audit("--root", str(root), issues=issues)
        assert code == 0

    def test_exit_1_on_warn_with_strict(self, tmp_path: Path) -> None:
        root = tmp_path / "project"
        root.mkdir()
        issues = [
            {"file": str(root / "a.md"), "issue": "Drift", "severity": "warn"},
        ]
        _, _, code = _run_audit(
            "--root", str(root), "--strict", issues=issues,
        )
        assert code == 1

    def test_exit_0_on_no_issues(self, tmp_path: Path) -> None:
        root = tmp_path / "project"
        root.mkdir()
        _, _, code = _run_audit("--root", str(root), issues=[])
        assert code == 0


class TestJsonOutput:
    def test_json_output_unchanged(self, tmp_path: Path) -> None:
        root = tmp_path / "project"
        root.mkdir()
        issues = [
            {"file": str(root / "a.md"), "issue": "Problem", "severity": "fail"},
        ]
        stdout, _, _ = _run_audit(
            "--root", str(root), "--json", issues=issues,
        )
        parsed = json.loads(stdout)
        assert isinstance(parsed, list)
        assert len(parsed) == 1


class TestSingleFileMode:
    def test_single_file_validation(self, tmp_path: Path) -> None:
        root = tmp_path / "project"
        root.mkdir()
        md_file = root / "docs" / "context" / "test.md"
        md_file.parent.mkdir(parents=True)
        md_file.write_text(
            "---\nname: Test\ndescription: A test\n---\n# Test\n"
        )
        # Single file mode — mock validate_file instead
        with patch("wiki.project.validate_file", return_value=[]) as mock_vf:
            stdout, _, code = _run_audit(
                "--root", str(root), str(md_file),
            )
        mock_vf.assert_called_once()
        assert code == 0




# ── TestChainAutoDetection ────────────────────────────────────────────


class TestChainAutoDetection:
    def _write_chain_manifest(self, path: Path, goal: str = "") -> None:
        """Write a minimal *.chain.md manifest to path."""
        content = (
            "---\n"
            "name: Test Chain\n"
            "description: A test chain\n"
            "type: chain\n"
            f"goal: {goal}\n"
            "---\n\n"
            "## Steps\n\n"
            "| Step | Skill | Input Contract | Output Contract | Gate |\n"
            "|------|-------|----------------|-----------------|------|\n"
            "| 1 | research | question | research.md | |\n"
        )
        path.write_text(content, encoding="utf-8")

    def test_no_chain_files_validate_chain_not_called(
        self, tmp_path: Path
    ) -> None:
        from unittest.mock import patch as _patch

        root = tmp_path / "project"
        root.mkdir()

        with _patch("wiki.project.validate_project", return_value=[]), \
             _patch("wiki.skill_chain.validate_chain") as mock_chain:
            _run_audit("--root", str(root))

        mock_chain.assert_not_called()

    def test_chain_manifest_issues_surfaced(self, tmp_path: Path) -> None:
        root = tmp_path / "project"
        root.mkdir()

        # Write a chain manifest with an empty goal — triggers termination fail
        self._write_chain_manifest(root / "my.chain.md", goal="")

        with patch("wiki.project.validate_project", return_value=[]):
            stdout, _, exit_code = _run_audit("--root", str(root))

        # termination check produces a fail → exit code 1
        assert exit_code == 1
        assert "chain" in stdout.lower() or "termination" in stdout.lower()

    def test_chain_in_hidden_dir_skipped(self, tmp_path: Path) -> None:
        from unittest.mock import patch as _patch

        root = tmp_path / "project"
        root.mkdir()
        hidden = root / ".git"
        hidden.mkdir()

        # Write chain manifest inside a hidden directory
        self._write_chain_manifest(hidden / "nested.chain.md", goal="some goal")

        with _patch("wiki.project.validate_project", return_value=[]), \
             _patch("wiki.skill_chain.validate_chain") as mock_chain:
            _run_audit("--root", str(root))

        mock_chain.assert_not_called()
