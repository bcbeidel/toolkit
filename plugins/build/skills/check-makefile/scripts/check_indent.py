#!/usr/bin/env python3
"""Tier-1 Makefile recipe-indent checker.

Scans for recipe lines indented with spaces instead of a real tab.
GNU Make syntactically requires a tab at the start of every recipe
line (unless `.RECIPEPREFIX` is redefined, which is discouraged).

Approach: after every target-definition line, treat subsequent
indented lines as the target's recipe block. A blank line or an
un-indented line ends the block. Within the block, any line whose
leading whitespace contains a space (not a tab) is flagged.

All findings are FAIL — space-indented recipes do not parse.

Example:
    ./check_indent.py path/to/Makefile
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

EXIT_USAGE = 64
PROG = "check_indent.py"

_TARGET_RE = re.compile(r"^([A-Za-z0-9_./$()%-]+)\s*:(?!=)")


class _UsageError(Exception):
    pass


def _is_makefile(path: Path) -> bool:
    return path.name in ("Makefile", "GNUmakefile") or path.suffix == ".mk"


def _collect_targets(paths: list[Path]) -> list[Path]:
    files: list[Path] = []
    for target in paths:
        if target.is_file():
            if _is_makefile(target):
                files.append(target)
        elif target.is_dir():
            for child in sorted(target.iterdir()):
                if child.is_file() and _is_makefile(child):
                    files.append(child)
        else:
            print(f"{PROG}: path not found: {target}", file=sys.stderr)
            raise _UsageError
    return files


def _scan_file(path: Path) -> bool:
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError as err:
        print(f"{PROG}: cannot read {path}: {err}", file=sys.stderr)
        return False

    any_fail = False
    in_recipe = False
    for lineno, line in enumerate(lines, 1):
        if not line.strip():
            in_recipe = False
            continue
        if _TARGET_RE.match(line) and not line.startswith((" ", "\t")):
            in_recipe = True
            continue
        if in_recipe:
            if line.startswith("\t"):
                continue
            if line.startswith(" "):
                print(
                    f"FAIL  {path} — tab-indent: recipe line {lineno} "
                    "starts with spaces, not tab"
                )
                print(
                    "  Recommendation: Replace the leading spaces with a "
                    "single real tab. Make rejects space-indented recipes "
                    "with `missing separator`."
                )
                any_fail = True
                continue
            in_recipe = False
    return any_fail


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog=PROG, description="Tier-1 Makefile recipe-indent checker."
    )
    parser.add_argument(
        "paths",
        nargs="+",
        type=Path,
        metavar="path",
        help="One or more Makefile / *.mk files or directories (non-recursive).",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = get_parser().parse_args(argv)
    any_fail = False
    try:
        for f in _collect_targets(args.paths):
            if _scan_file(f):
                any_fail = True
    except _UsageError:
        return EXIT_USAGE
    except KeyboardInterrupt:
        return 130
    return 1 if any_fail else 0


if __name__ == "__main__":
    sys.exit(main())
