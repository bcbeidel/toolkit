#!/usr/bin/env python3
"""Tier-1 Makefile variable-discipline checker.

Two sub-checks:
  - assignment-op (WARN): top-level assignments use `:=`, `?=`, or
    `+=`, not bare `=`, unless a `# deferred:` or `# recursive:`
    comment is adjacent (same line, previous non-blank line).
  - top-level-shell (WARN): no `$(shell …)` expansions at top level
    outside an allowlist (`git rev-parse`, `uname`, `pwd`).

Top-level = not inside a recipe (no leading tab) and not an
`export`/`override`/conditional directive line.

Example:
    ./check_variables.py path/to/Makefile
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

EXIT_USAGE = 64
PROG = "check_variables.py"

_ASSIGNMENT_RE = re.compile(
    r"^(?:export\s+|override\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*"
    r"(:=|\?=|\+=|!=|::=|=)"
)
_SHELL_CALL_RE = re.compile(r"\$\(shell\s+([^)]+)\)")
_DEFERRED_COMMENT_RE = re.compile(r"#\s*(deferred|recursive)[:\s]", re.IGNORECASE)
_ALLOWED_SHELL = (
    "git rev-parse",
    "git describe",
    "uname",
    "pwd",
    "id -u",
    "id -g",
)


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


def _prev_non_blank(lines: list[str], idx: int) -> str:
    for i in range(idx - 1, -1, -1):
        if lines[i].strip():
            return lines[i]
    return ""


def _has_deferred_justification(lines: list[str], idx: int) -> bool:
    if _DEFERRED_COMMENT_RE.search(lines[idx]):
        return True
    return bool(_DEFERRED_COMMENT_RE.search(_prev_non_blank(lines, idx)))


def _is_shell_allowed(cmd: str) -> bool:
    cmd = cmd.strip().strip('"').strip("'")
    return any(cmd.startswith(allowed) for allowed in _ALLOWED_SHELL)


def _scan_file(path: Path) -> bool:
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError as err:
        print(f"{PROG}: cannot read {path}: {err}", file=sys.stderr)
        return False

    bare_eq_vars: list[tuple[int, str]] = []
    top_shell: list[tuple[int, str]] = []

    for idx, line in enumerate(lines):
        if line.startswith("\t"):
            continue
        stripped = line.lstrip()
        if stripped.startswith("#") or not stripped:
            continue

        match = _ASSIGNMENT_RE.match(line)
        if match and match.group(2) == "=":
            if not _has_deferred_justification(lines, idx):
                bare_eq_vars.append((idx + 1, match.group(1)))

        for shell_match in _SHELL_CALL_RE.finditer(line):
            cmd = shell_match.group(1)
            if not _is_shell_allowed(cmd):
                top_shell.append((idx + 1, cmd.strip()))

    if bare_eq_vars:
        names = ", ".join(f"{n}(line {ln})" for ln, n in bare_eq_vars)
        print(
            f"WARN  {path} — assignment-op: bare `=` without "
            f"`# deferred:` justification: {names}"
        )
        print(
            "  Recommendation: Change to `:=` (immediate) or `?=` "
            "(overridable). Use `=` only when deferred expansion is "
            "deliberate, and document with `# deferred: <reason>`."
        )

    if top_shell:
        detail = "; ".join(f"line {ln}: $(shell {cmd})" for ln, cmd in top_shell)
        print(
            f"WARN  {path} — top-level-shell: expensive `$(shell …)` "
            f"at parse time: {detail}"
        )
        print(
            "  Recommendation: Move the `$(shell …)` into a recipe "
            "(or use a sentinel file). Top-level `$(shell …)` runs on "
            "every `make` invocation, including `make help`."
        )
    return False


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog=PROG, description="Tier-1 Makefile variable discipline checker."
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
