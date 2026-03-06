"""Per-file and project-wide validation checks.

Provides seven individual checks (frontmatter, content length, draft
markers, source URLs, related paths, index sync, project files) and two
composite functions (validate_file, validate_project) that orchestrate
them.

Each check returns a list of issue dicts with keys: file, issue, severity.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import List

from wos.document import Document, parse_document
from wos.index import check_index_sync, extract_preamble
from wos.url_checker import check_urls

# ── Individual checks ──────────────────────────────────────────


def check_frontmatter(doc: Document, context_path: str = "docs/context") -> List[dict]:
    """Check frontmatter fields: required fields, research sources, type issues.

    Args:
        doc: A parsed Document instance.
        context_path: Path prefix for context files (for related-field check).

    Returns:
        List of issue dicts with severity 'fail' or 'warn'.
    """
    issues: List[dict] = []

    # FAIL: required fields
    if not doc.name or not doc.name.strip():
        issues.append({
            "file": doc.path,
            "issue": "Frontmatter 'name' is empty",
            "severity": "fail",
        })
    if not doc.description or not doc.description.strip():
        issues.append({
            "file": doc.path,
            "issue": "Frontmatter 'description' is empty",
            "severity": "fail",
        })

    # FAIL: research documents must have sources
    if doc.type == "research" and not doc.sources:
        issues.append({
            "file": doc.path,
            "issue": "Research document has no sources",
            "severity": "fail",
        })

    # WARN: source items should be strings, not dicts
    for idx, source in enumerate(doc.sources):
        if isinstance(source, dict):
            issues.append({
                "file": doc.path,
                "issue": f"sources[{idx}] is a dict, expected a URL string",
                "severity": "warn",
            })

    # WARN: context files should have related fields
    if doc.path.startswith(context_path + "/") and not doc.related:
        issues.append({
            "file": doc.path,
            "issue": "Context file has no related fields",
            "severity": "warn",
        })

    return issues


def check_content(
    doc: Document,
    context_path: str = "docs/context",
    max_words: int = 800,
    min_words: int = 100,
) -> List[dict]:
    """Warn when context files exceed or fall below word count thresholds.

    Only checks files under context_path. Non-context files and _index.md
    files are excluded.

    Args:
        doc: A parsed Document instance.
        context_path: Path prefix for context files.
        max_words: Upper word count threshold (default 800).
        min_words: Lower word count threshold (default 100).

    Returns:
        List of issue dicts. Empty if within thresholds.
    """
    if not doc.path.startswith(context_path + "/"):
        return []
    if doc.path.endswith("_index.md"):
        return []

    word_count = len(doc.content.split())
    if word_count > max_words:
        return [{
            "file": doc.path,
            "issue": f"Context file is {word_count} words (threshold: {max_words})",
            "severity": "warn",
        }]
    if word_count < min_words:
        return [{
            "file": doc.path,
            "issue": f"Context file is {word_count} words (minimum: {min_words})",
            "severity": "warn",
        }]
    return []


def check_source_urls(doc: Document) -> List[dict]:
    """Check that all URLs in doc.sources are reachable.

    Calls check_urls() from wos.url_checker. If the document has no
    sources, the check is skipped entirely (check_urls is not called).

    Args:
        doc: A parsed Document instance.

    Returns:
        List of issue dicts. Empty if all sources are reachable.
    """
    if not doc.sources:
        return []

    # Normalize: sources may be plain URL strings or dicts with a "url" key.
    urls = []
    for s in doc.sources:
        if isinstance(s, dict):
            urls.append(s.get("url", s.get("href", "")))
        else:
            urls.append(str(s))

    results = check_urls(urls)
    issues: List[dict] = []
    for result in results:
        if not result.reachable:
            if result.status in (403, 429):
                msg = (
                    f"URL returned {result.status}"
                    f" (site may block automated checks):"
                    f" {result.url}"
                )
                issues.append({
                    "file": doc.path,
                    "issue": msg,
                    "severity": "warn",
                })
            else:
                reason = f" ({result.reason})" if result.reason else ""
                issues.append({
                    "file": doc.path,
                    "issue": f"Source URL unreachable: {result.url}{reason}",
                    "severity": "fail",
                })
    return issues


def check_draft_markers(doc: Document) -> List[dict]:
    """Warn when research documents contain DRAFT markers.

    Only applies to documents with type: research. A ``<!-- DRAFT -->``
    marker indicates an incomplete workflow.

    Args:
        doc: A parsed Document instance.

    Returns:
        List of issue dicts. Empty if no marker found.
    """
    if doc.type != "research":
        return []
    if "<!-- DRAFT -->" in doc.content:
        return [{
            "file": doc.path,
            "issue": "Research document contains <!-- DRAFT --> marker",
            "severity": "warn",
        }]
    return []


def check_related_paths(doc: Document, root: Path) -> List[dict]:
    """Check that file paths in doc.related exist on disk.

    URLs (http:// or https://) are skipped — only local file paths
    are validated.

    Args:
        doc: A parsed Document instance.
        root: Project root directory for resolving relative paths.

    Returns:
        List of issue dicts. Empty if all paths exist.
    """
    issues: List[dict] = []
    for rel in doc.related:
        # Skip URLs
        if rel.startswith("http://") or rel.startswith("https://"):
            continue
        full_path = root / rel
        if not full_path.exists():
            issues.append({
                "file": doc.path,
                "issue": f"Related path does not exist: {rel}",
                "severity": "fail",
            })
    return issues


def check_all_indexes(directory: Path) -> List[dict]:
    """Recursively check all _index.md files under a directory.

    Walks all subdirectories and runs check_index_sync() on each.
    Also warns when an _index.md exists but has no preamble.

    Args:
        directory: Root directory to walk.

    Returns:
        List of issue dicts from all index checks.
    """
    issues: List[dict] = []
    if not directory.is_dir():
        return issues

    # Check the directory itself
    issues.extend(check_index_sync(directory))

    # WARN: index exists but has no preamble (area description)
    index_path = directory / "_index.md"
    if index_path.is_file() and extract_preamble(index_path) is None:
        issues.append({
            "file": str(index_path),
            "issue": "Index has no area description (preamble)",
            "severity": "warn",
        })

    # Recurse into subdirectories
    for entry in sorted(directory.iterdir()):
        if entry.is_dir():
            issues.extend(check_all_indexes(entry))

    return issues


# ── Composite functions ────────────────────────────────────────


def validate_file(
    path: Path,
    root: Path,
    verify_urls: bool = True,
    context_max_words: int = 800,
    context_min_words: int = 100,
) -> List[dict]:
    """Validate a single markdown file.

    Reads the file, parses it with parse_document(), then runs
    checks 1-4 (frontmatter, research sources, source URLs, related
    paths). If parsing fails, returns a single parse-error issue.

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

    issues: List[dict] = []
    issues.extend(check_frontmatter(doc))
    issues.extend(check_content(
        doc, max_words=context_max_words, min_words=context_min_words,
    ))
    issues.extend(check_draft_markers(doc))
    if verify_urls:
        issues.extend(check_source_urls(doc))
    issues.extend(check_related_paths(doc, root))
    return issues


def check_project_files(root: Path) -> List[dict]:
    """Warn when AGENTS.md or CLAUDE.md are missing or misconfigured.

    Checks:
    - AGENTS.md missing
    - AGENTS.md exists but lacks ``<!-- wos:begin -->`` marker
    - CLAUDE.md missing
    - CLAUDE.md exists but doesn't reference ``@AGENTS.md``

    Args:
        root: Project root directory.

    Returns:
        List of issue dicts. Empty if all checks pass.
    """
    issues: List[dict] = []

    agents_path = root / "AGENTS.md"
    if not agents_path.is_file():
        issues.append({
            "file": "AGENTS.md",
            "issue": "No AGENTS.md found. Run /wos:init to initialize.",
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
                "issue": "AGENTS.md lacks WOS markers. Navigation updates won't work.",
                "severity": "warn",
            })

    claude_path = root / "CLAUDE.md"
    if not claude_path.is_file():
        issues.append({
            "file": "CLAUDE.md",
            "issue": "No CLAUDE.md found. Run /wos:init to initialize.",
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


def validate_project(
    root: Path,
    verify_urls: bool = True,
    context_max_words: int = 800,
    context_min_words: int = 100,
) -> List[dict]:
    """Validate all markdown files in a project.

    Walks the docs/ subtree under root. Runs index sync checks on
    each directory, and per-file checks on each .md file (excluding
    _index.md files). Also checks project-level files (AGENTS.md,
    CLAUDE.md).

    Args:
        root: Project root directory.
        verify_urls: If False, skip source URL reachability checks.

    Returns:
        List of all issue dicts found.
    """
    issues: List[dict] = []

    # Project-level checks
    issues.extend(check_project_files(root))

    docs_dir = root / "docs"
    if not docs_dir.is_dir():
        return issues

    for subdir in sorted(docs_dir.iterdir()):
        if not subdir.is_dir():
            continue

        # Index sync checks (recursive)
        issues.extend(check_all_indexes(subdir))

        # Per-file checks on all .md files (excluding _index.md)
        for dirpath, _dirnames, filenames in os.walk(subdir):
            for filename in sorted(filenames):
                if filename == "_index.md":
                    continue
                if not filename.endswith(".md"):
                    continue
                file_path = Path(dirpath) / filename
                issues.extend(validate_file(
                    file_path, root,
                    verify_urls=verify_urls,
                    context_max_words=context_max_words,
                    context_min_words=context_min_words,
                ))

    return issues
