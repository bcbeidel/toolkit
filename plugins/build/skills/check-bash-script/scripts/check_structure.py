#!/usr/bin/env python3
"""Tier-1 bash structural checker.

Runs seven orthogonal structural sub-checks against each target:
  - shebang (FAIL): must be `#!/usr/bin/env bash` or `#!/bin/bash`.
  - strict-mode (FAIL): `set -euo pipefail` in prologue.
  - header-comment (WARN): >=3 comment lines in first 10 lines.
  - main-fn (WARN): a `main` function is defined.
  - main-guard (WARN): BASH_SOURCE sourceable guard present.
  - readonly-config (WARN): top-level constants declared `readonly`.
  - mktemp-trap (WARN): every mktemp preceded by a `trap ... EXIT`.

Example:
    ./check_structure.py path/to/script.sh path/to/scripts/
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

EXIT_USAGE = 64
HEADER_WINDOW = 10
MIN_HEADER_COMMENTS = 3
STRICT_MODE_WINDOW = 20

_BASH_SHEBANGS = ("#!/usr/bin/env bash", "#!/bin/bash", "#!/usr/bin/env -S bash")
_BASH_EXTENSIONS = (".sh", ".bash")

_STRICT_MODE_REGEXES = (
    re.compile(r"set\s+-[Ee]?[Eaeux]*o?\s+pipefail"),
    re.compile(r"set\s+-o\s+errexit"),
)

_MAIN_FN_RE = re.compile(r"^(?:function\s+)?main\s*\(\s*\)")
_MAIN_GUARD_RE = re.compile(
    r"\$\{BASH_SOURCE\[0\]\}.*==.*\$\{?0\}?"
    r"|\$\{?0\}?.*==.*\$\{BASH_SOURCE\[0\]\}"
)
_UPPERCASE_ASSIGN_RE = re.compile(r"^[A-Z][A-Z0-9_]+=")
_READONLY_DECL_RE = re.compile(r"^readonly\s")
_MKTEMP_RE = re.compile(r"(?:^|[\s;|])mktemp(?:\s|$)")
_TRAP_EXIT_RE = re.compile(r"^\s*trap\s+.*EXIT")


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
            print(f"check_structure.py: path not found: {target}", file=sys.stderr)
            raise _UsageError
    return files


def _emit(
    severity: str,
    path: Path,
    check: str,
    message: str,
    recommendation: str,
) -> None:
    print(f"{severity}  {path} — {check}: {message}")
    print(f"  Recommendation: {recommendation}.")


def _check_shebang(path: Path, lines: list[str]) -> bool:
    first = lines[0] if lines else ""
    if first in ("#!/usr/bin/env bash", "#!/bin/bash") or first.startswith(
        "#!/usr/bin/env -S bash"
    ):
        return False
    _emit(
        "FAIL",
        path,
        "shebang",
        f"first line is {first!r}, expected a bash shebang",
        "Replace the first line with `#!/usr/bin/env bash`",
    )
    return True


def _check_strict_mode(path: Path, lines: list[str]) -> bool:
    count = 0
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        count += 1
        if any(r.search(line) for r in _STRICT_MODE_REGEXES):
            return False
        if count >= STRICT_MODE_WINDOW:
            break
    _emit(
        "FAIL",
        path,
        "strict-mode",
        "`set -euo pipefail` not found in prologue",
        "Add `set -euo pipefail` immediately after the shebang",
    )
    return True


def _check_header_comment(path: Path, lines: list[str]) -> None:
    window = lines[1:HEADER_WINDOW]
    comment_count = sum(1 for ln in window if ln.lstrip().startswith("#"))
    if comment_count >= MIN_HEADER_COMMENTS:
        return
    _emit(
        "WARN",
        path,
        "header-comment",
        "no purpose/usage block in first 10 lines",
        "Add a header block: purpose, usage, deps, exit codes",
    )


def _check_main_fn(path: Path, lines: list[str]) -> None:
    if any(_MAIN_FN_RE.match(ln) for ln in lines):
        return
    _emit(
        "WARN",
        path,
        "main-fn",
        "no `main` function defined",
        "Wrap execution in main() and call from the sourceable guard",
    )


def _check_main_guard(path: Path, lines: list[str]) -> None:
    if any(_MAIN_GUARD_RE.search(ln) for ln in lines):
        return
    _emit(
        "WARN",
        path,
        "main-guard",
        "missing BASH_SOURCE-equals-0 sourceable guard",
        "Add the canonical BASH_SOURCE guard calling main at EOF",
    )


def _check_readonly_config(path: Path, lines: list[str]) -> None:
    upper_assigns = sum(1 for ln in lines if _UPPERCASE_ASSIGN_RE.match(ln))
    readonly_decls = sum(1 for ln in lines if _READONLY_DECL_RE.match(ln))
    if upper_assigns >= 2 and readonly_decls == 0:
        _emit(
            "WARN",
            path,
            "readonly-config",
            "top-level UPPERCASE constants not readonly",
            "Declare top-level constants readonly to prevent reassignment",
        )


def _check_mktemp_trap(path: Path, lines: list[str]) -> None:
    first_mktemp: int | None = None
    for lineno, line in enumerate(lines, 1):
        if line.lstrip().startswith("#"):
            continue
        if _MKTEMP_RE.search(line):
            first_mktemp = lineno
            break
    if first_mktemp is None:
        return
    first_trap: int | None = None
    for lineno, line in enumerate(lines, 1):
        if _TRAP_EXIT_RE.search(line):
            first_trap = lineno
            break
    if first_trap is None or first_trap > first_mktemp:
        _emit(
            "WARN",
            path,
            "mktemp-trap-pairing",
            f"mktemp at line {first_mktemp} without prior trap EXIT",
            "Add `trap 'rm -rf \"${tmpdir}\"' EXIT INT TERM` immediately after mktemp",
        )


def _check_file(path: Path) -> bool:
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError as err:
        print(f"check_structure.py: cannot read {path}: {err}", file=sys.stderr)
        return False
    any_fail = False
    any_fail |= _check_shebang(path, lines)
    any_fail |= _check_strict_mode(path, lines)
    _check_header_comment(path, lines)
    _check_main_fn(path, lines)
    _check_main_guard(path, lines)
    _check_readonly_config(path, lines)
    _check_mktemp_trap(path, lines)
    return any_fail


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="check_structure.py",
        description="Tier-1 bash structural checker (7 sub-checks).",
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
