#!/usr/bin/env python3
"""Deterministic Tier-1 structural checks for Claude Code rule files.

Three independent checks per file:

- **Location** — file must live under ``.claude/rules/`` (project) or
  ``~/.claude/rules/`` (user). FAIL otherwise.
- **Extension** — file must end in ``.md`` with no inner extension
  segment (no ``foo.bar.md``). ``.mdx`` / ``.markdown`` / other
  extensions FAIL.
- **Frontmatter shape** — only ``paths:`` is a documented top-level key.
  Other keys emit INFO (non-failing) findings.

Example:
    ./check_structure.py .claude/rules/
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

EXIT_USAGE = 2
EXIT_INTERRUPTED = 130

TOP_LEVEL_KEY_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_-]*):")
DOCUMENTED_KEYS = frozenset({"paths"})

SCAN_EXTENSIONS = {".md", ".mdx", ".markdown"}


def emit_fail(path: Path, check: str, detail: str, recommendation: str) -> None:
    print(f"FAIL  {path} — {check}: {detail}")
    print(f"  Recommendation: {recommendation}")


def emit_info(path: Path, check: str, detail: str, recommendation: str) -> None:
    print(f"INFO  {path} — {check}: {detail}")
    print(f"  Recommendation: {recommendation}")


def check_location(path: Path) -> bool:
    absolute = path.resolve()
    parts = absolute.parts
    for i in range(len(parts) - 1):
        if parts[i] == ".claude" and parts[i + 1] == "rules":
            return True
    emit_fail(
        path,
        "Location",
        "file not under .claude/rules/ or ~/.claude/rules/",
        "Move the file to .claude/rules/<name>.md",
    )
    return False


def check_extension(path: Path) -> bool:
    name = path.name
    if name.endswith(".mdx") or name.endswith(".markdown"):
        ext = name.rsplit(".", 1)[1]
        emit_fail(
            path,
            "Extension",
            f"file extension is .{ext}, expected .md",
            "Rename to <name>.md",
        )
        return False
    if not name.endswith(".md"):
        emit_fail(
            path,
            "Extension",
            "file has no .md extension",
            "Rename to <name>.md",
        )
        return False
    stem = name[: -len(".md")]
    if "." in stem:
        inner = stem.rsplit(".", 1)[1]
        emit_fail(
            path,
            "Extension",
            f"double extension .{inner}.md",
            "Rename to <name>.md (remove the inner extension segment)",
        )
        return False
    return True


def check_frontmatter_shape(path: Path) -> None:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as err:
        print(f"warn: cannot read {path}: {err}", file=sys.stderr)
        return

    lines = text.splitlines()
    if not lines or lines[0] != "---":
        return

    for idx in range(1, len(lines)):
        if lines[idx] == "---":
            return
        match = TOP_LEVEL_KEY_RE.match(lines[idx])
        if match and match.group(1) not in DOCUMENTED_KEYS:
            emit_info(
                path,
                "Frontmatter shape",
                f"unknown top-level key '{match.group(1)}' at line {idx + 1}",
                "Remove the key, or move its content into the body",
            )


def check_file(path: Path) -> bool:
    ok = True
    if not check_location(path):
        ok = False
    if not check_extension(path):
        ok = False
    check_frontmatter_shape(path)  # INFO only, no exit-code effect
    return ok


def iter_targets(targets: list[Path]) -> list[Path]:
    resolved: list[Path] = []
    for target in targets:
        if target.is_file():
            resolved.append(target)
        elif target.is_dir():
            matched: list[Path] = []
            for ext in SCAN_EXTENSIONS:
                matched.extend(target.rglob(f"*{ext}"))
            resolved.extend(sorted(set(matched)))
        else:
            print(f"error: path not found: {target}", file=sys.stderr)
            raise SystemExit(EXIT_USAGE)
    return resolved


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Structural checks for Claude Code rule files.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "paths",
        nargs="+",
        type=Path,
        help=(
            "Rule files or directories to scan "
            "(directories walked for *.md / *.mdx / *.markdown)."
        ),
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = get_parser().parse_args(argv)
    try:
        all_ok = True
        for file_path in iter_targets(args.paths):
            if not check_file(file_path):
                all_ok = False
        return 0 if all_ok else 1
    except KeyboardInterrupt:
        return EXIT_INTERRUPTED


if __name__ == "__main__":
    sys.exit(main())
