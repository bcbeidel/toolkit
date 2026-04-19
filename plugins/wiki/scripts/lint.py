#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""Run validation checks on a project.

Usage:
    python scripts/lint.py [FILE] [--root DIR] [--no-urls] [--json]
                           [--strict] [--context-max-words N]
                           [--context-min-words N] [--skill-max-lines N]
"""
from __future__ import annotations

import argparse
import json
import sys
import warnings
from pathlib import Path

import _bootstrap  # noqa: F401 — side effect: adds plugin root to sys.path


def _relative_path(file_path: str, root: Path) -> str:
    """Return file_path relative to root, falling back to the original."""
    try:
        return str(Path(file_path).relative_to(root))
    except ValueError:
        return file_path


def main() -> None:
    warnings.filterwarnings("ignore")
    parser = argparse.ArgumentParser(
        description="Run validation checks on a project.",
    )
    parser.add_argument(
        "file",
        nargs="?",
        default=None,
        help="Optional: validate a single file instead of the whole project",
    )
    parser.add_argument(
        "--root",
        default=".",
        help="Project root directory (default: current directory)",
    )
    parser.add_argument(
        "--no-urls",
        action="store_true",
        help="Skip URL reachability checks",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        dest="json_output",
        help="Output issues as JSON",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit 1 on any issue (including warnings)",
    )
    args = parser.parse_args()

    # Deferred imports — keeps --help fast
    from wiki.project import validate_file, validate_project

    root = Path(args.root).resolve()

    # Single-file or project mode
    if args.file:
        file_path = Path(args.file).resolve()
        issues = validate_file(file_path, root, verify_urls=not args.no_urls)
    else:
        issues = validate_project(root, verify_urls=not args.no_urls)

    # Wiki validation — auto-activated when wiki/SCHEMA.md is present
    wiki_schema = root / "wiki" / "SCHEMA.md"
    if wiki_schema.is_file():
        from wiki.wiki import validate_wiki
        issues.extend(validate_wiki(root / "wiki", wiki_schema))

    # Chain validation — auto-activated when *.chain.md files are present
    chain_manifests = [
        p for p in root.rglob("*.chain.md")
        if not any(part.startswith(".") for part in p.parts)
    ]
    if chain_manifests:
        from wiki.skill_chain import validate_chain
        chain_skills_dirs = [root / "skills"] if (root / "skills").is_dir() else []
        for manifest_path in sorted(chain_manifests):
            issues.extend(validate_chain(manifest_path, chain_skills_dirs))

    # Count by severity
    fail_count = sum(1 for i in issues if i["severity"] == "fail")
    warn_count = sum(1 for i in issues if i["severity"] == "warn")

    # Output
    if args.json_output:
        print(json.dumps(issues, indent=2))
    elif issues:
        # Count unique files
        file_count = len({i["file"] for i in issues})
        print(f"{fail_count} fail, {warn_count} warn across {file_count} files")
        print()
        print(f"{'file':<40} | {'sev':<4} | issue")
        for issue in issues:
            rel = _relative_path(issue["file"], root)
            sev = issue["severity"]
            print(f"{rel:<40} | {sev:<4} | {issue['issue']}")
    else:
        print("All checks passed.")

    # Exit code: 1 if any fail, or if --strict and any issue
    has_failures = fail_count > 0
    has_any = len(issues) > 0
    sys.exit(1 if has_failures or (args.strict and has_any) else 0)


if __name__ == "__main__":
    main()
