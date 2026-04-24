#!/usr/bin/env python3
"""Tier-1 bash safety checker.

Emits findings for three safety violations:
  - eval (FAIL): `eval` invocation without a justification comment on
    the same or immediately preceding line.
  - gnu-flags (WARN): GNU-only coreutils flags without a declared
    `requires: gnu-coreutils` header.
  - tmp-literal (FAIL): hardcoded `/tmp/` or `/var/tmp/` string literals.

Example:
    ./check_safety.py path/to/script.sh path/to/scripts/
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

EXIT_USAGE = 64
EMIT_CAP = 3
HEADER_SCAN_LINES = 20

_BASH_SHEBANGS = ("#!/usr/bin/env bash", "#!/bin/bash", "#!/usr/bin/env -S bash")
_BASH_EXTENSIONS = (".sh", ".bash")

_EVAL_RE = re.compile(r"(?:^|[\s;&|(`])eval\s")
_EVAL_JUSTIFICATIONS = ("shellcheck disable=SC2294", "eval-justified:")

_GNU_COREUTILS_HEADER_RE = re.compile(r"requires:\s*gnu-coreutils", re.IGNORECASE)

_GNU_FLAG_SIMPLE = [
    (re.compile(r"(?:^|\s)grep\s+(?:-[A-Za-z]*)?P(?:\s|$)"), "grep -P"),
    (re.compile(r"(?:^|\s)readlink\s+-f(?:\s|$)"), "readlink -f"),
    (re.compile(r"(?:^|[^A-Za-z])date\s+-d\s"), "date -d"),
    (re.compile(r"(?:^|\s)stat\s+-c\s"), "stat -c"),
    (re.compile(r"(?:^|\s)xargs\s+(?:-[A-Za-z]*)?r(?:\s|$)"), "xargs -r"),
]
_SED_I_RE = re.compile(r"(?:^|\s)sed\s+-i(?:\s+(?![\"'])|$)")

_TMP_LITERAL_RE = re.compile(r"[\"'](/tmp|/var/tmp)/")  # noqa: S108


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
            print(f"check_safety.py: path not found: {target}", file=sys.stderr)
            raise _UsageError
    return files


def _emit(
    severity: str,
    path: Path,
    check: str,
    lineno: int,
    message: str,
    recommendation: str,
) -> None:
    print(f"{severity}  {path} — {check}: line {lineno} {message}")
    print(f"  Recommendation: {recommendation}.")


def _check_eval(path: Path, lines: list[str]) -> bool:
    any_fail = False
    for lineno, line in enumerate(lines, 1):
        if line.lstrip().startswith("#"):
            continue
        if not _EVAL_RE.search(line):
            continue
        prev = lines[lineno - 2] if lineno >= 2 else ""
        if any(j in line or j in prev for j in _EVAL_JUSTIFICATIONS):
            continue
        _emit(
            "FAIL",
            path,
            "eval",
            lineno,
            "uses `eval` without justification comment",
            "Replace with case dispatch, parameter expansion, or array call; "
            "or add `# shellcheck disable=SC2294` or `# eval-justified: <reason>`",
        )
        any_fail = True
    return any_fail


def _check_gnu_flags(path: Path, lines: list[str]) -> None:
    header = "\n".join(lines[:HEADER_SCAN_LINES])
    if _GNU_COREUTILS_HEADER_RE.search(header):
        return
    emitted = 0
    for lineno, line in enumerate(lines, 1):
        if emitted >= EMIT_CAP:
            return
        if line.lstrip().startswith("#"):
            continue
        label: str | None = None
        if _SED_I_RE.search(line):
            label = "sed -i (no backup arg, GNU-only)"
        else:
            for pattern, lbl in _GNU_FLAG_SIMPLE:
                if pattern.search(line):
                    label = lbl
                    break
        if label is None:
            continue
        _emit(
            "WARN",
            path,
            "gnu-flags",
            lineno,
            f"uses GNU-only flag ({label})",
            "Declare `# requires: gnu-coreutils` in the header, "
            "or use a portable form (e.g., `sed -e ... > out && mv out file`)",
        )
        emitted += 1


def _check_tmp_literal(path: Path, lines: list[str]) -> bool:
    any_fail = False
    for lineno, line in enumerate(lines, 1):
        if line.lstrip().startswith("#"):
            continue
        if _TMP_LITERAL_RE.search(line):
            _emit(
                "FAIL",
                path,
                "tmp-literal",
                lineno,
                "has hardcoded /tmp or /var/tmp literal",
                "Use `mktemp` (or `mktemp -d`) and pair with `trap` cleanup",
            )
            any_fail = True
    return any_fail


def _check_file(path: Path) -> bool:
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError as err:
        print(f"check_safety.py: cannot read {path}: {err}", file=sys.stderr)
        return False
    any_fail = False
    any_fail |= _check_eval(path, lines)
    _check_gnu_flags(path, lines)
    any_fail |= _check_tmp_literal(path, lines)
    return any_fail


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="check_safety.py",
        description="Tier-1 bash safety checker (eval, GNU flags, /tmp literals).",
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
    any_fail = False
    try:
        files = _collect_targets(args.paths)
        for f in files:
            if _check_file(f):
                any_fail = True
    except _UsageError:
        return EXIT_USAGE
    except KeyboardInterrupt:
        return 130
    return 1 if any_fail else 0


if __name__ == "__main__":
    sys.exit(main())
