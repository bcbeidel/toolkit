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

    mock_target = "wos.validators.validate_project"

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
        stdout, _, _ = _run_audit("--root", str(root), "--no-urls", issues=issues)
        assert "1 fail" in stdout
        assert "1 warn" in stdout

    def test_no_issues_shows_all_passed(self, tmp_path: Path) -> None:
        root = tmp_path / "project"
        root.mkdir()
        stdout, _, _ = _run_audit("--root", str(root), "--no-urls", issues=[])
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
        stdout, _, _ = _run_audit("--root", str(root), "--no-urls", issues=issues)
        assert str(root) not in stdout
        assert "docs/context/api/auth.md" in stdout

    def test_table_has_severity_column(self, tmp_path: Path) -> None:
        root = tmp_path / "project"
        root.mkdir()
        issues = [
            {"file": str(root / "a.md"), "issue": "Problem", "severity": "fail"},
            {"file": str(root / "b.md"), "issue": "Drift", "severity": "warn"},
        ]
        stdout, _, _ = _run_audit("--root", str(root), "--no-urls", issues=issues)
        assert "fail" in stdout
        assert "warn" in stdout


class TestExitCodes:
    def test_exit_1_on_fail_issues(self, tmp_path: Path) -> None:
        root = tmp_path / "project"
        root.mkdir()
        issues = [
            {"file": str(root / "a.md"), "issue": "Problem", "severity": "fail"},
        ]
        _, _, code = _run_audit("--root", str(root), "--no-urls", issues=issues)
        assert code == 1

    def test_exit_0_on_warn_only(self, tmp_path: Path) -> None:
        root = tmp_path / "project"
        root.mkdir()
        issues = [
            {"file": str(root / "a.md"), "issue": "Drift", "severity": "warn"},
        ]
        _, _, code = _run_audit("--root", str(root), "--no-urls", issues=issues)
        assert code == 0

    def test_exit_1_on_warn_with_strict(self, tmp_path: Path) -> None:
        root = tmp_path / "project"
        root.mkdir()
        issues = [
            {"file": str(root / "a.md"), "issue": "Drift", "severity": "warn"},
        ]
        _, _, code = _run_audit(
            "--root", str(root), "--no-urls", "--strict", issues=issues,
        )
        assert code == 1

    def test_exit_0_on_no_issues(self, tmp_path: Path) -> None:
        root = tmp_path / "project"
        root.mkdir()
        _, _, code = _run_audit("--root", str(root), "--no-urls", issues=[])
        assert code == 0


class TestJsonOutput:
    def test_json_output_unchanged(self, tmp_path: Path) -> None:
        root = tmp_path / "project"
        root.mkdir()
        issues = [
            {"file": str(root / "a.md"), "issue": "Problem", "severity": "fail"},
        ]
        stdout, _, _ = _run_audit(
            "--root", str(root), "--no-urls", "--json", issues=issues,
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
        with patch("wos.validators.validate_file", return_value=[]) as mock_vf:
            stdout, _, code = _run_audit(
                "--root", str(root), "--no-urls", str(md_file),
            )
        mock_vf.assert_called_once()
        assert code == 0


class TestFixOutput:
    def test_fix_messages_use_relative_paths(self, tmp_path: Path) -> None:
        root = tmp_path / "project"
        idx_dir = root / "docs" / "plans"
        idx_dir.mkdir(parents=True)
        idx_file = idx_dir / "_index.md"
        idx_file.write_text("")
        issues = [
            {
                "file": str(idx_file),
                "issue": "_index.md is out of sync with directory contents",
                "severity": "fail",
            },
        ]
        with patch("wos.validators.validate_project", return_value=issues):
            _, stderr, _ = _run_audit("--root", str(root), "--no-urls", "--fix")
        assert str(root) not in stderr
        assert "docs/plans/_index.md" in stderr

    def test_fix_preserves_preamble(self, tmp_path: Path) -> None:
        """--fix should preserve existing preambles in _index.md files."""
        from wos.index import generate_index

        root = tmp_path / "project"
        idx_dir = root / "docs" / "context"
        idx_dir.mkdir(parents=True)
        # Create a doc file and generate index with preamble
        (idx_dir / "auth.md").write_text(
            "---\nname: Auth\ndescription: Authentication guide\n---\n# Auth\n"
        )
        idx_file = idx_dir / "_index.md"
        preamble_text = "This area covers authentication and authorization."
        initial = generate_index(idx_dir, preamble=preamble_text)
        idx_file.write_text(initial)

        # Add a new file so index is out of sync
        (idx_dir / "tokens.md").write_text(
            "---\nname: Tokens\ndescription: Token handling\n---\n# Tokens\n"
        )

        issues = [
            {
                "file": str(idx_file),
                "issue": "_index.md is out of sync with directory contents",
                "severity": "fail",
            },
        ]
        with patch("wos.validators.validate_project", return_value=issues):
            _run_audit("--root", str(root), "--no-urls", "--fix")

        result = idx_file.read_text(encoding="utf-8")
        assert preamble_text in result
        assert "tokens.md" in result
