#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""Run WOS validation checks on a project.

Usage:
    uv run scripts/audit.py [FILE] [--root DIR] [--no-urls] [--json]
                            [--fix] [--strict] [--context-max-words N]
                            [--context-min-words N] [--skill-max-lines N]
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import warnings
from pathlib import Path

# Ensure `import wos` works whether pip-installed or run from plugin cache.
# Prefer CLAUDE_PLUGIN_ROOT env var (set by Claude Code for hooks/MCP);
# fall back to navigating from __file__ (required for skill-invoked scripts).
_env_root = os.environ.get("CLAUDE_PLUGIN_ROOT", "")
# scripts/ → plugin root
_plugin_root = (
    Path(_env_root) if _env_root and os.path.isdir(_env_root)
    else Path(__file__).resolve().parent.parent
)
if str(_plugin_root) not in sys.path:
    sys.path.insert(0, str(_plugin_root))


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
        "--fix",
        action="store_true",
        help="Regenerate out-of-sync or missing _index.md files",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit 1 on any issue (including warnings)",
    )
    parser.add_argument(
        "--context-max-words",
        type=int,
        default=800,
        help="Word count threshold for context file warnings (default: 800)",
    )
    parser.add_argument(
        "--context-min-words",
        type=int,
        default=100,
        help="Minimum word count for context file warnings (default: 100)",
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
    from wos.index import extract_preamble, generate_index
    from wos.validators import validate_file, validate_project

    root = Path(args.root).resolve()

    # Single-file or project mode
    if args.file:
        file_path = Path(args.file).resolve()
        issues = validate_file(
            file_path, root,
            verify_urls=not args.no_urls,
            context_max_words=args.context_max_words,
            context_min_words=args.context_min_words,
        )
    else:
        issues = validate_project(
            root,
            verify_urls=not args.no_urls,
            context_max_words=args.context_max_words,
            context_min_words=args.context_min_words,
        )

    # --fix: regenerate _index.md files that are out of sync or missing
    if args.fix:
        fixed: list[str] = []
        remaining: list[dict] = []
        for issue in issues:
            file_path_str = issue["file"]
            msg = issue["issue"]
            if (
                file_path_str.endswith("_index.md")
                and ("out of sync" in msg or "missing" in msg)
            ):
                idx_path = Path(file_path_str)
                directory = idx_path.parent
                preamble = extract_preamble(idx_path)
                content = generate_index(directory, preamble=preamble)
                idx_path.write_text(content, encoding="utf-8")
                fixed.append(file_path_str)
                print(
                    f"Fixed: {_relative_path(file_path_str, root)}",
                    file=sys.stderr,
                )
            else:
                remaining.append(issue)
        issues = remaining

    # Skill instruction density reporting
    from wos.skill_audit import check_skill_meta, check_skill_sizes

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
