#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""Run WOS validation checks on a project.

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
        description="Run WOS validation checks on a project.",
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
    parser.add_argument(
        "--skill-max-lines",
        type=int,
        default=500,
        help=(
            "Instruction line threshold for skill density warnings"
            " (default: 500, 0 to disable)"
        ),
    )
    args = parser.parse_args()

    # Deferred imports — keeps --help fast
    from wos.project import validate_file, validate_project

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
        from wos.wiki import validate_wiki
        issues.extend(validate_wiki(root / "wiki", wiki_schema))

    # Chain validation — auto-activated when *.chain.md files are present
    chain_manifests = [
        p for p in root.rglob("*.chain.md")
        if not any(part.startswith(".") for part in p.parts)
    ]
    if chain_manifests:
        from wos.skill_chain import validate_chain
        chain_skills_dirs = [root / "skills"] if (root / "skills").is_dir() else []
        for manifest_path in sorted(chain_manifests):
            issues.extend(validate_chain(manifest_path, chain_skills_dirs))

    # Skill instruction density reporting
    from wos.skill import check_skill_meta, check_skill_sizes

    skills_dir = root / "skills"
    if skills_dir.is_dir():
        summaries, skill_issues = check_skill_sizes(
            skills_dir, max_lines=args.skill_max_lines,
        )
        issues.extend(skill_issues)

        for entry in sorted(skills_dir.iterdir()):
            if not entry.is_dir() or entry.name.startswith("_"):
                continue
            if (entry / "SKILL.md").exists():
                issues.extend(check_skill_meta(entry))

        if summaries and not args.json_output:
            print("Skill Instruction Density:", file=sys.stderr)
            for s in sorted(summaries, key=lambda x: -x["total_lines"]):
                flag = "  [warn]" if (
                    args.skill_max_lines > 0
                    and s["total_lines"] > args.skill_max_lines
                ) else ""
                print(
                    f"  {s['name']:<20}"
                    f" {s['skill_lines']:>4} (SKILL)"
                    f" + {s['ref_lines']:>4} (refs)"
                    f" = {s['total_lines']:>4} lines,"
                    f" {s['words']:>5} words{flag}",
                    file=sys.stderr,
                )
            print(file=sys.stderr)

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
