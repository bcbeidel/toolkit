#!/usr/bin/env python3
"""Tier-1 Makefile structural checker.

Seven orthogonal structural sub-checks against each target:
  - shell-pin (FAIL): `SHELL := bash` (or `/bin/bash`).
  - shellflags (FAIL): `.SHELLFLAGS` has `-e`, `-o pipefail`, `-c`.
  - warn-undefined (WARN): `MAKEFLAGS += --warn-undefined-variables`.
  - no-builtin-rules (WARN): `MAKEFLAGS += --no-builtin-rules` or
    a bare `.SUFFIXES:` line.
  - delete-on-error (WARN): `.DELETE_ON_ERROR:` present.
  - default-goal (WARN): `.DEFAULT_GOAL := help` or `help` is the
    first non-pattern target.
  - header-comment (WARN): comment block in first 5 non-blank lines
    naming project / requirements.

Example:
    ./check_structure.py path/to/Makefile
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

EXIT_USAGE = 64
PROG = "check_structure.py"

HEADER_WINDOW = 5
MIN_HEADER_COMMENTS = 2

_SHELL_RE = re.compile(r"^SHELL\s*[:?]?=\s*(?:/bin/)?bash\b")
_SHELLFLAGS_RE = re.compile(r"^\.SHELLFLAGS\s*[:?]?=\s*(.+)$")
_WARN_UNDEF_RE = re.compile(r"MAKEFLAGS\s*\+?=.*--warn-undefined-variables")
_NO_BUILTIN_RE = re.compile(r"MAKEFLAGS\s*\+?=.*--no-builtin-rules")
_SUFFIXES_RE = re.compile(r"^\.SUFFIXES\s*:\s*$")
_DELETE_ON_ERROR_RE = re.compile(r"^\.DELETE_ON_ERROR\s*:")
_DEFAULT_GOAL_HELP_RE = re.compile(r"^\.DEFAULT_GOAL\s*:?=\s*help\b")
_TARGET_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_./$()%-]*)\s*:(?!=)")


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


def _emit(severity: str, path: Path, check: str, detail: str, rec: str) -> None:
    print(f"{severity}  {path} — {check}: {detail}")
    print(f"  Recommendation: {rec}")


def _shellflags_ok(rhs: str) -> bool:
    return "-e" in rhs and "pipefail" in rhs and "-c" in rhs


def _first_non_pattern_target(lines: list[str]) -> str | None:
    for line in lines:
        if line.startswith("\t") or line.startswith("#") or not line.strip():
            continue
        if line.startswith("."):
            continue
        match = _TARGET_RE.match(line)
        if match:
            name = match.group(1)
            if "%" not in name:
                return name
    return None


def _header_has_comments(lines: list[str]) -> bool:
    count = 0
    seen = 0
    for line in lines:
        if not line.strip():
            continue
        seen += 1
        if line.lstrip().startswith("#"):
            count += 1
        if seen >= HEADER_WINDOW:
            break
    return count >= MIN_HEADER_COMMENTS


def _scan_file(path: Path) -> bool:
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError as err:
        print(f"{PROG}: cannot read {path}: {err}", file=sys.stderr)
        return False

    any_fail = False

    # SHELL
    if not any(_SHELL_RE.match(line) for line in lines):
        _emit(
            "FAIL",
            path,
            "shell-pin",
            "`SHELL := bash` missing",
            "Add `SHELL := bash` near the top of the file.",
        )
        any_fail = True

    # SHELLFLAGS
    shellflags_match = next(
        (_SHELLFLAGS_RE.match(line) for line in lines if _SHELLFLAGS_RE.match(line)),
        None,
    )
    if not shellflags_match:
        _emit(
            "FAIL",
            path,
            "shellflags",
            "`.SHELLFLAGS` assignment missing",
            "Add `.SHELLFLAGS := -eu -o pipefail -c`.",
        )
        any_fail = True
    elif not _shellflags_ok(shellflags_match.group(1)):
        _emit(
            "FAIL",
            path,
            "shellflags",
            "`.SHELLFLAGS` missing -e / -o pipefail / -c",
            "Set `.SHELLFLAGS := -eu -o pipefail -c`.",
        )
        any_fail = True

    # WARN-undefined
    if not any(_WARN_UNDEF_RE.search(line) for line in lines):
        _emit(
            "WARN",
            path,
            "warn-undefined",
            "`MAKEFLAGS += --warn-undefined-variables` missing",
            "Add `MAKEFLAGS += --warn-undefined-variables` to catch "
            "typos that would otherwise expand to empty.",
        )

    # No-builtin-rules OR .SUFFIXES:
    has_nobuiltin = any(_NO_BUILTIN_RE.search(line) for line in lines)
    has_suffixes = any(_SUFFIXES_RE.match(line) for line in lines)
    if not (has_nobuiltin or has_suffixes):
        _emit(
            "WARN",
            path,
            "no-builtin-rules",
            "`--no-builtin-rules` and `.SUFFIXES:` both missing",
            "Add `MAKEFLAGS += --no-builtin-rules` and/or a bare "
            "`.SUFFIXES:` line to disable legacy inference rules.",
        )

    # .DELETE_ON_ERROR:
    if not any(_DELETE_ON_ERROR_RE.match(line) for line in lines):
        _emit(
            "WARN",
            path,
            "delete-on-error",
            "`.DELETE_ON_ERROR:` missing",
            "Add `.DELETE_ON_ERROR:` so failed recipes do not leave "
            "partial outputs on disk.",
        )

    # .DEFAULT_GOAL := help OR help first
    has_default_goal = any(_DEFAULT_GOAL_HELP_RE.match(line) for line in lines)
    first_target = _first_non_pattern_target(lines)
    if not has_default_goal and first_target != "help":
        _emit(
            "WARN",
            path,
            "default-goal",
            "`.DEFAULT_GOAL := help` missing and `help` is not the first target",
            "Add `.DEFAULT_GOAL := help` or reorder `help` to be the "
            "first non-pattern target.",
        )

    # header-comment
    if not _header_has_comments(lines):
        _emit(
            "WARN",
            path,
            "header-comment",
            "no project/requirements comment in first 5 non-blank lines",
            "Add a header comment naming the project and environment "
            "requirements (e.g., GNU Make >= 4.0, bash).",
        )

    return any_fail


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog=PROG, description="Tier-1 Makefile structure checker."
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
