"""Project aggregate — validates an entire project tree.

Project is the aggregate root for project-level validation: it discovers
documents, runs per-document checks, and checks project-level configuration
files (AGENTS.md, CLAUDE.md).
"""

from __future__ import annotations

from pathlib import Path
from typing import List

from wiki.document import parse_document

_AMBIENT_DIRS = frozenset({
    ".git", ".github", ".claude", ".claude-plugin", ".resolver",
    ".venv", ".cache", ".pytest_cache", ".ruff_cache", ".mypy_cache",
    ".eggs", "__pycache__", "node_modules", "dist", "build", "target",
})

_CONVENTION_SUFFIXES = (
    ".context.md", ".plan.md", ".design.md", ".research.md",
)

_RESOLVER_THRESHOLD = 3

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
        from wiki.document import Document

        issues: List[dict] = []
        issues.extend(self.check_project_files())

        for doc in Document.scan(str(self.root)):
            issues.extend(doc.issues(self.root, verify_urls=verify_urls))

        return issues

    def check_project_files(self) -> List[dict]:
        """Warn when AGENTS.md or CLAUDE.md are missing or misconfigured.

        Checks:
        - AGENTS.md missing
        - AGENTS.md exists but lacks the managed-section begin marker
        - CLAUDE.md missing
        - CLAUDE.md exists but doesn't reference ``@AGENTS.md``

        Returns:
            List of issue dicts. Empty if all checks pass.
        """
        from wiki.agents_md import _LEGACY_BEGIN_MARKER, BEGIN_MARKER

        issues: List[dict] = []
        root = self.root

        agents_path = root / "AGENTS.md"
        if not agents_path.is_file():
            issues.append({
                "file": "AGENTS.md",
                "issue": "No AGENTS.md found. Run /wiki:setup to initialize.",
                "severity": "warn",
            })
        else:
            try:
                content = agents_path.read_text(encoding="utf-8")
            except OSError:
                content = ""
            if BEGIN_MARKER not in content and _LEGACY_BEGIN_MARKER not in content:
                issues.append({
                    "file": "AGENTS.md",
                    "issue": (
                        "AGENTS.md lacks managed-section markers."
                        " Navigation updates won't work."
                    ),
                    "severity": "warn",
                })

        claude_path = root / "CLAUDE.md"
        if not claude_path.is_file():
            issues.append({
                "file": "CLAUDE.md",
                "issue": "No CLAUDE.md found. Run /wiki:setup to initialize.",
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

        issues.extend(check_resolver_recommendation(root))
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


# ── Resolver recommendation ───────────────────────────────────────


def _conventionful_dirs(root: Path) -> List[str]:
    """Return names of top-level directories that follow a filing convention.

    A directory counts when it contains ≥2 markdown files whose name ends in
    one of the canonical filing suffixes (`.context.md`, `.plan.md`,
    `.design.md`, `.research.md`). Walks the subtree but skips ambient
    directory names at any depth.
    """
    found: List[str] = []
    try:
        children = sorted(root.iterdir())
    except OSError:
        return found

    for child in children:
        if not child.is_dir() or child.name in _AMBIENT_DIRS:
            continue
        count = 0
        for md in child.rglob("*.md"):
            if any(part in _AMBIENT_DIRS for part in md.parts):
                continue
            if md.name.endswith(_CONVENTION_SUFFIXES):
                count += 1
                if count >= 2:
                    found.append(child.name)
                    break
    return found


def check_resolver_recommendation(root: Path) -> List[dict]:
    """Warn when the repo crosses the resolver threshold but lacks RESOLVER.md.

    The threshold mirrors `/build:build-resolver`'s primitive check: ≥3
    top-level directories whose contents follow a filing convention.
    """
    if (root / "RESOLVER.md").is_file():
        return []
    dirs = _conventionful_dirs(root)
    if len(dirs) < _RESOLVER_THRESHOLD:
        return []
    return [{
        "file": "RESOLVER.md",
        "issue": (
            f"No RESOLVER.md, but {len(dirs)} directories follow filing"
            f" conventions ({', '.join(dirs)})."
            " Run /build:build-resolver to scaffold a routing table."
        ),
        "severity": "warn",
    }]
