#!/usr/bin/env python3
"""Tier-1 bash idiom checker (WARN-only style findings).

Emits WARN findings for three bash style anti-patterns:
  - bracket-test: `[ ... ]` tests where `[[ ... ]]` is preferred.
  - printf-over-echo: `echo -e`/`echo -n`/escape-laden echo (prefer printf).
  - var-braces: unbraced `$var` of 3+ chars where `${var}` is clearer.

Per-file emission is capped at 3 findings per sub-check. Only WARN findings
are produced; exit 0 unless a usage error occurs.

Example:
    ./check_idioms.py path/to/script.sh path/to/scripts/
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

EXIT_USAGE = 64
EMIT_CAP = 3

_BASH_SHEBANGS = ("#!/usr/bin/env bash", "#!/bin/bash", "#!/usr/bin/env -S bash")
_BASH_EXTENSIONS = (".sh", ".bash")

_DOUBLE_BRACKET_RE = re.compile(r"\[\[")
_SINGLE_BRACKET_RE = re.compile(r"(?:^|[\s;&|(])\[\s")
_ECHO_ANTI_RE = re.compile(r"(?:^|[\s;&|(])echo\s+(?:-[en]+|\S*\\[ntr\\])")
_UNBRACED_VAR_RE = re.compile(r"(?<!\$\{)(?<!\\)\$[a-zA-Z_][a-zA-Z0-9_]{2,}")


class _UsageError(Exception):
    pass


def _is_bash_script(path: Path) -> bool:
    if path.suffix in _BASH_EXTENSIONS:
        return True
    try:
        first = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return False
    if not first:
        return False
    return any(first[0] == s or first[0].startswith(s) for s in _BASH_SHEBANGS)


def _collect_targets(paths: list[Path]) -> list[Path]:
    files: list[Path] = []
    for target in paths:
        if target.is_file():
            if _is_bash_script(target):
                files.append(target)
        elif target.is_dir():
            for child in sorted(target.iterdir()):
                if child.is_file() and _is_bash_script(child):
                    files.append(child)
        else:
            print(f"check_idioms.py: path not found: {target}", file=sys.stderr)
            raise _UsageError
    return files


def _emit(
    path: Path,
    check: str,
    lineno: int,
    message: str,
    recommendation: str,
) -> None:
    print(f"WARN  {path} — {check}: line {lineno} {message}")
    print(f"  Recommendation: {recommendation}.")


def _scan(
    path: Path,
    lines: list[str],
    check: str,
    pattern: re.Pattern[str],
    message: str,
    recommendation: str,
    skip_if: re.Pattern[str] | None = None,
) -> None:
    emitted = 0
    for lineno, line in enumerate(lines, 1):
        if emitted >= EMIT_CAP:
            return
        if line.lstrip().startswith("#"):
            continue
        if skip_if is not None and skip_if.search(line):
            continue
        if pattern.search(line):
            _emit(path, check, lineno, message, recommendation)
            emitted += 1


def _check_file(path: Path) -> None:
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError as err:
        print(f"check_idioms.py: cannot read {path}: {err}", file=sys.stderr)
        return
    _scan(
        path,
        lines,
        "bracket-test",
        _SINGLE_BRACKET_RE,
        "uses `[ ... ]`; prefer `[[ ... ]]` in bash",
        "Use double-bracket tests (no word-splitting, pattern matching)",
        skip_if=_DOUBLE_BRACKET_RE,
    )
    _scan(
        path,
        lines,
        "printf-over-echo",
        _ECHO_ANTI_RE,
        "non-trivial output; prefer printf",
        "Use printf for portable output with flags or escape sequences",
    )
    _scan(
        path,
        lines,
        "var-braces",
        _UNBRACED_VAR_RE,
        "has bare-dollar expansion next to identifier chars",
        "Brace the expansion when it abuts identifier characters",
    )


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="check_idioms.py",
        description="Tier-1 bash idiom checker (WARN-only style findings).",
    )
    parser.add_argument(
        "paths",
        nargs="+",
        type=Path,
        metavar="path",
        help="One or more .sh/.bash files or directories (non-recursive).",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = get_parser().parse_args(argv)
    try:
        files = _collect_targets(args.paths)
        for f in files:
            _check_file(f)
    except _UsageError:
        return EXIT_USAGE
    except KeyboardInterrupt:
        return 130
    return 0


if __name__ == "__main__":
    sys.exit(main())
