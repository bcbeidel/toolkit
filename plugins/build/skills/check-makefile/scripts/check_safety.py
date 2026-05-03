#!/usr/bin/env python3
"""Tier-1 Makefile safety checker.

Scans recipe lines (tab-indented) plus the first recipe command of
destructive-named targets for five classes of issue:

  - unguarded-rm (FAIL): `rm -rf $(VAR)` lacking a non-empty guard,
    a scoped path (BUILD_DIR, BUILD_ROOT, OUT_DIR, DIST_DIR), or `--`.
  - sudo (FAIL): `sudo` invocation in a recipe.
  - global-install (FAIL): `npm install -g`, unscoped `pip install`,
    `gem install` without `--user-install`.
  - curl-pipe (FAIL): pipe-to-shell pattern (curl piped into sh or bash).
  - destructive-guard (WARN): targets named `deploy`, `publish`,
    `release`, or `prod-*` must begin their recipe with a
    confirmation-variable guard (e.g., `CONFIRM`, `CONFIRMED`, `YES`).

Example:
    ./check_safety.py path/to/Makefile
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

EXIT_USAGE = 64
PROG = "check_safety.py"

_TARGET_RE = re.compile(r"^([A-Za-z0-9_./$()%-]+)\s*:(?!=)")

_RM_RF_RE = re.compile(r"\brm\s+-[rR][fF]?\s+(\S+)")
_SUDO_RE = re.compile(r"(?:^|[\s;|&])sudo\b")
_NPM_G_RE = re.compile(r"\bnpm\s+install[^\n]*\s-g\b|\bnpm\s+i[^\n]*\s-g\b")
_PIP_GLOBAL_RE = re.compile(
    r"\bpip(?:3)?\s+install\b(?!(?:[^\n]*--user|[^\n]*--target|[^\n]*--prefix|[^\n]*-e\s+\.?\S*))"
)
_GEM_GLOBAL_RE = re.compile(r"\bgem\s+install\b(?![^\n]*--user-install)")
_CURL_PIPE_RE = re.compile(r"\bcurl\b[^\n]*\|\s*(?:sudo\s+)?(?:sh|bash)\b")

_SAFE_PATH_HINTS = ("BUILD_DIR", "BUILD_ROOT", "OUT_DIR", "DIST_DIR", "TARGET_DIR")
_DESTRUCTIVE_NAMES = ("deploy", "publish", "release")
_CONFIRM_VARS_RE = re.compile(r"\b(CONFIRM|CONFIRMED|YES|I_REALLY_MEAN_IT)\b")


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


def _rm_is_guarded(lines: list[str], idx: int, operand: str) -> bool:
    # Scoped path literal or known-safe variable name.
    if "--" in lines[idx]:
        return True
    if any(hint in operand for hint in _SAFE_PATH_HINTS):
        return True
    # Preceding recipe line (within ~3 lines) has a non-empty check.
    for back in range(1, 4):
        if idx - back < 0:
            break
        prev = lines[idx - back]
        if not prev.startswith("\t"):
            break
        if "-n " in prev or "-z " in prev or "exit 1" in prev or "|| exit" in prev:
            return True
    return False


def _is_destructive_name(name: str) -> bool:
    if name in _DESTRUCTIVE_NAMES:
        return True
    return name.startswith("prod-") or name.startswith("prod_")


def _recipe_first_line(lines: list[str], target_idx: int) -> str | None:
    for i in range(target_idx + 1, len(lines)):
        line = lines[i]
        if not line.strip():
            continue
        if line.startswith("\t"):
            return line
        return None
    return None


def _scan_file(path: Path) -> bool:
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError as err:
        print(f"{PROG}: cannot read {path}: {err}", file=sys.stderr)
        return False

    any_fail = False

    # Recipe-line scans
    for idx, line in enumerate(lines):
        if not line.startswith("\t"):
            continue
        lineno = idx + 1

        rm_match = _RM_RF_RE.search(line)
        if rm_match and not _rm_is_guarded(lines, idx, rm_match.group(1)):
            print(
                f"FAIL  {path} — unguarded-rm: `rm -rf` without guard on line {lineno}"
            )
            print(
                "  Recommendation: Add a non-empty guard "
                '(`[[ -n "$(VAR)" ]] || exit 1`), scope the path to '
                "`$(BUILD_DIR)`, or include `--` before the argument."
            )
            any_fail = True

        if _SUDO_RE.search(line):
            print(f"FAIL  {path} — sudo: `sudo` in recipe on line {lineno}")
            print(
                "  Recommendation: Remove `sudo`. Dev workflows install "
                "into user-local paths (`--user`, `.venv/`, "
                "`node_modules/`), not system-level."
            )
            any_fail = True

        if _NPM_G_RE.search(line):
            print(f"FAIL  {path} — global-install: `npm install -g` on line {lineno}")
            print(
                "  Recommendation: Install into project-local "
                "`node_modules/` (`npm install --save-dev`) instead of "
                "the global prefix."
            )
            any_fail = True

        if _PIP_GLOBAL_RE.search(line):
            print(
                f"FAIL  {path} — global-install: unscoped "
                f"`pip install` on line {lineno}"
            )
            print(
                "  Recommendation: Use `pip install --user`, a venv "
                "(`.venv/bin/pip`), or editable install in a venv "
                "(`pip install -e .`)."
            )
            any_fail = True

        if _GEM_GLOBAL_RE.search(line):
            print(
                f"FAIL  {path} — global-install: `gem install` "
                f"without `--user-install` on line {lineno}"
            )
            print("  Recommendation: Add `--user-install` or pin to a bundled Gemfile.")
            any_fail = True

        if _CURL_PIPE_RE.search(line):
            print(
                f"FAIL  {path} — curl-pipe: pipe-to-shell pattern on line {lineno}"
            )
            print(
                "  Recommendation: Pin a specific version, verify a "
                "checksum, then install — never pipe arbitrary remote "
                "output into a shell."
            )
            any_fail = True

    # Destructive-guard scan
    for idx, line in enumerate(lines):
        if line.startswith("\t"):
            continue
        match = _TARGET_RE.match(line)
        if not match:
            continue
        name = match.group(1)
        if not _is_destructive_name(name):
            continue
        first = _recipe_first_line(lines, idx)
        if not first or not _CONFIRM_VARS_RE.search(first):
            print(
                f"WARN  {path} — destructive-guard: `{name}` lacks a confirmation guard"
            )
            print(
                "  Recommendation: Make the first recipe command an "
                'explicit check: `@[[ "$${CONFIRM:-0}" = "1" ]] || '
                '{ echo "set CONFIRM=1" >&2; exit 1; }`.'
            )
    return any_fail


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog=PROG, description="Tier-1 Makefile safety checker."
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
