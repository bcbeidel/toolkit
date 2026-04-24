#!/usr/bin/env python3
"""Tier-1 Makefile naming checker.

Two sub-checks:
  - target-name (WARN): public target names (those with a `##`
    description on the definition line) match `^[a-z][a-z0-9-]*$`.
  - helper-prefix (INFO): targets without a `##` description and
    without a `_` prefix and without file indicators (`/`, `.`, `%`,
    `$(`) — likely helpers that should start with `_`.

Example:
    ./check_naming.py path/to/Makefile
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

EXIT_USAGE = 64
PROG = "check_naming.py"

_TARGET_RE = re.compile(r"^([A-Za-z0-9_./$()%-]+)\s*:(?!=)")
_DESC_RE = re.compile(r"^[A-Za-z0-9_./$()%-]+\s*:.*##\s+\S")
_PUBLIC_NAME_RE = re.compile(r"^[a-z][a-z0-9-]*$")
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


def _scan_file(path: Path) -> bool:
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError as err:
        print(f"{PROG}: cannot read {path}: {err}", file=sys.stderr)
        return False

    bad_public: list[str] = []
    unprefixed_helpers: list[str] = []
    seen: set[str] = set()

    for line in lines:
        if line.startswith("\t"):
            continue
        match = _TARGET_RE.match(line)
        if not match:
            continue
        name = match.group(1)
        if name in seen or name.startswith("."):
            continue
        seen.add(name)
        has_desc = bool(_DESC_RE.match(line))
        has_file_indicator = any(ind in name for ind in _FILE_INDICATORS)

        if has_desc:
            if not _PUBLIC_NAME_RE.match(name):
                bad_public.append(name)
        else:
            if not has_file_indicator and not name.startswith("_"):
                unprefixed_helpers.append(name)

    if bad_public:
        names = ", ".join(bad_public)
        print(
            f"WARN  {path} — target-name: public target(s) not "
            f"lowercase-hyphenated: {names}"
        )
        print(
            "  Recommendation: Rename to `^[a-z][a-z0-9-]*$` shape "
            "(e.g., `run-tests`, not `runTheTests`). Muscle memory for "
            "`make test` depends on the convention."
        )

    if unprefixed_helpers:
        names = ", ".join(unprefixed_helpers)
        print(
            f"INFO  {path} — helper-prefix: internal helper(s) not "
            f"prefixed with `_`: {names}"
        )
        print(
            "  Recommendation: Rename to `_<name>` so the target is "
            "hidden from `make help` and readers recognize it as "
            "not-part-of-the-public-API."
        )
    return False


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog=PROG, description="Tier-1 Makefile naming checker."
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
