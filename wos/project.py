"""Project aggregate — validates an entire project tree.

Project is the aggregate root for project-level validation: it discovers
documents, runs per-document checks, and checks project-level configuration
files (AGENTS.md, CLAUDE.md).
"""

from __future__ import annotations

from pathlib import Path
from typing import List

from wos.document import parse_document

# ── Per-file helper ────────────────────────────────────────────────


def validate_file(
    path: Path,
    root: Path,
    verify_urls: bool = True,
) -> List[dict]:
    """Validate a single markdown file.

    Reads the file, parses it with parse_document(), then calls
    doc.issues(root). If parsing fails, returns a single parse-error issue.

    Args:
        path: Path to the .md file.
        root: Project root directory.
        verify_urls: If False, skip source URL reachability check.

    Returns:
        List of issue dicts.
    """
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        return [{
            "file": str(path),
            "issue": f"Cannot read file: {exc}",
            "severity": "fail",
        }]

    try:
        doc = parse_document(str(path), text)
    except ValueError as exc:
        return [{
            "file": str(path),
            "issue": f"Parse error: {exc}",
            "severity": "fail",
        }]

    return doc.issues(root, verify_urls=verify_urls)


# ── Project aggregate ──────────────────────────────────────────────


class Project:
    """Aggregate root for project-level validation."""

    def __init__(self, root: Path) -> None:
        self.root = root

    def validate(
        self,
        verify_urls: bool = True,
    ) -> List[dict]:
        """Validate all managed documents and project configuration.

        Discovers documents by walking the project tree and checking for
        valid frontmatter. Also checks project-level files (AGENTS.md,
        CLAUDE.md).

        Args:
            verify_urls: If False, skip source URL reachability checks.

        Returns:
            List of all issue dicts found.
        """
        from wos.document import Document

        issues: List[dict] = []
        issues.extend(self.check_project_files())

        for doc in Document.scan(str(self.root)):
            issues.extend(doc.issues(self.root, verify_urls=verify_urls))

        return issues

    def check_project_files(self) -> List[dict]:
        """Warn when AGENTS.md or CLAUDE.md are missing or misconfigured.

        Checks:
        - AGENTS.md missing
        - AGENTS.md exists but lacks ``<!-- wos:begin -->`` marker
        - CLAUDE.md missing
        - CLAUDE.md exists but doesn't reference ``@AGENTS.md``

        Returns:
            List of issue dicts. Empty if all checks pass.
        """
        issues: List[dict] = []
        root = self.root

        agents_path = root / "AGENTS.md"
        if not agents_path.is_file():
            issues.append({
                "file": "AGENTS.md",
                "issue": "No AGENTS.md found. Run /wos:setup to initialize.",
                "severity": "warn",
            })
        else:
            try:
                content = agents_path.read_text(encoding="utf-8")
            except OSError:
                content = ""
            if "<!-- wos:begin -->" not in content:
                issues.append({
                    "file": "AGENTS.md",
                    "issue": (
                        "AGENTS.md lacks WOS markers."
                        " Navigation updates won't work."
                    ),
                    "severity": "warn",
                })

        claude_path = root / "CLAUDE.md"
        if not claude_path.is_file():
            issues.append({
                "file": "CLAUDE.md",
                "issue": "No CLAUDE.md found. Run /wos:setup to initialize.",
                "severity": "warn",
            })
        else:
            try:
                content = claude_path.read_text(encoding="utf-8")
            except OSError:
                content = ""
            if "@AGENTS.md" not in content:
                issues.append({
                    "file": "CLAUDE.md",
                    "issue": (
                        "CLAUDE.md doesn't reference @AGENTS.md."
                        " Navigation may not load."
                    ),
                    "severity": "warn",
                })

        return issues

# ── Module-level convenience functions ────────────────────────────


def check_project_files(root: Path) -> List[dict]:
    """Check AGENTS.md and CLAUDE.md configuration. See Project.check_project_files."""
    return Project(root).check_project_files()


def validate_project(
    root: Path,
    verify_urls: bool = True,
) -> List[dict]:
    """Validate all managed documents in a project. See Project.validate."""
    return Project(root).validate(verify_urls=verify_urls)
