#!/usr/bin/env python3
"""Tier-1 Makefile .PHONY-coverage checker.

Parses target definitions and `.PHONY:` prerequisite lists, then
flags targets that look non-file-producing (no `/`, no `.`, no
variable expansion, no `%` pattern) but are absent from `.PHONY`.

Heuristic: a bare lowercase verb (`build`, `test`, `_helper`) is
phony by convention; a target name containing `/`, `.`, `$(`, or `%`
is presumed file-producing and skipped.

All findings are WARN.

Example:
    ./check_phony.py path/to/Makefile
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

EXIT_USAGE = 64
PROG = "check_phony.py"

_TARGET_RE = re.compile(r"^([A-Za-z0-9_./$()%-]+)\s*:(?!=)")
_PHONY_RE = re.compile(r"^\.PHONY\s*:\s*(.*)$")
_SPECIAL_PREFIXES = (".",)
_FILE_INDICATORS = ("/", ".", "$(", "${", "%")


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


def _looks_phony(name: str) -> bool:
    if name.startswith(_SPECIAL_PREFIXES):
        return False
    if any(ind in name for ind in _FILE_INDICATORS):
        return False
    return True


def _parse(lines: list[str]) -> tuple[list[str], set[str]]:
    """Return (ordered list of target names, set of .PHONY names)."""
    targets: list[str] = []
    phony: set[str] = set()
    for line in lines:
        if line.startswith("\t"):
            continue
        phony_match = _PHONY_RE.match(line)
        if phony_match:
            for name in phony_match.group(1).split():
                phony.add(name)
            continue
        target_match = _TARGET_RE.match(line)
        if target_match:
            targets.append(target_match.group(1))
    return targets, phony


def _scan_file(path: Path) -> bool:
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError as err:
        print(f"{PROG}: cannot read {path}: {err}", file=sys.stderr)
        return False

    targets, phony = _parse(lines)
    missing = []
    seen: set[str] = set()
    for name in targets:
        if name in seen:
            continue
        seen.add(name)
        if _looks_phony(name) and name not in phony:
            missing.append(name)

    if missing:
        names = ", ".join(missing)
        print(
            f"WARN  {path} — phony-coverage: non-file target(s) "
            f"missing from .PHONY: {names}"
        )
        print(
            "  Recommendation: Add the missing target(s) to the "
            "`.PHONY:` list. A file named `<target>` in the repo "
            "silently breaks `make <target>` without the declaration."
        )
    return False


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog=PROG, description="Tier-1 Makefile .PHONY coverage checker."
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
