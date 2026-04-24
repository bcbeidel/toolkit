#!/usr/bin/env python3
"""Tier-1 Makefile recipe-hygiene checker.

Four sub-checks scanning recipe lines (tab-indented):
  - literal-make (WARN): bare `make` (not `$(MAKE)`) as a command
    token.
  - at-discipline (WARN): `@`-prefix only on `echo`, `printf`, `:`.
  - or-true-guard (WARN): `|| true` without an adjacent explanatory
    comment (same line or previous non-blank line).
  - recipe-length (WARN): any target's recipe exceeds 10 lines.

Example:
    ./check_recipes.py path/to/Makefile
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

EXIT_USAGE = 64
PROG = "check_recipes.py"
MAX_RECIPE_LINES = 10

_TARGET_RE = re.compile(r"^([A-Za-z0-9_./$()%-]+)\s*:(?!=)")
_LITERAL_MAKE_RE = re.compile(r"(?:^|[;&|\s])make(?!FLAGS|FILE)\b")
_AT_PREFIX_RE = re.compile(r"^\t@(\S+)")
_OR_TRUE_RE = re.compile(r"\|\|\s*true\b")
_INLINE_COMMENT_RE = re.compile(r"#[^\n]*")

_AT_ALLOWED_CMDS = ("echo", "printf", ":", "true", "#", "awk", "sed")


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


def _has_adjacent_comment(lines: list[str], idx: int) -> bool:
    if _INLINE_COMMENT_RE.search(lines[idx]):
        return True
    for i in range(idx - 1, -1, -1):
        if not lines[i].strip():
            continue
        return bool(_INLINE_COMMENT_RE.search(lines[i]))
    return False


def _scan_file(path: Path) -> bool:
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError as err:
        print(f"{PROG}: cannot read {path}: {err}", file=sys.stderr)
        return False

    literal_make: list[int] = []
    at_discipline: list[tuple[int, str]] = []
    or_true: list[int] = []

    current_target: str | None = None
    recipe_count = 0
    long_recipes: list[tuple[str, int]] = []

    for idx, line in enumerate(lines):
        lineno = idx + 1

        # Track target boundaries
        if not line.startswith("\t"):
            if current_target is not None and recipe_count > MAX_RECIPE_LINES:
                long_recipes.append((current_target, recipe_count))
            if not line.strip():
                current_target = None
                recipe_count = 0
                continue
            match = _TARGET_RE.match(line)
            if match and not line.startswith("."):
                current_target = match.group(1)
                recipe_count = 0
            else:
                current_target = None
            continue

        if current_target is not None:
            recipe_count += 1

        # Strip comments before matching literal-make (avoid false hits in `# run make`)
        stripped = _INLINE_COMMENT_RE.sub("", line)

        # literal-make: avoid $(MAKE) / $(MAKE)
        probe = stripped.replace("$(MAKE)", "").replace("${MAKE}", "")
        if _LITERAL_MAKE_RE.search(probe):
            literal_make.append(lineno)

        at_match = _AT_PREFIX_RE.match(line)
        if at_match:
            cmd = at_match.group(1).strip()
            cmd_head = cmd.split("$", 1)[0]  # strip $(VAR) suffixes
            cmd_head = cmd_head.split("(", 1)[0] or cmd_head
            if not any(cmd_head.startswith(allowed) for allowed in _AT_ALLOWED_CMDS):
                at_discipline.append((lineno, cmd[:40]))

        if _OR_TRUE_RE.search(stripped) and not _has_adjacent_comment(lines, idx):
            or_true.append(lineno)

    # Flush trailing target
    if current_target is not None and recipe_count > MAX_RECIPE_LINES:
        long_recipes.append((current_target, recipe_count))

    if literal_make:
        detail = ", ".join(f"line {ln}" for ln in literal_make[:3])
        extra = "" if len(literal_make) <= 3 else f" (+{len(literal_make) - 3} more)"
        print(f"WARN  {path} — literal-make: bare `make` in recipe: {detail}{extra}")
        print(
            "  Recommendation: Replace bare `make` with `$(MAKE)`. "
            "`$(MAKE)` propagates `-j`, `-s`, and MAKEFLAGS; bare "
            "`make` does not."
        )

    if at_discipline:
        detail = ", ".join(f"line {ln} ({cmd})" for ln, cmd in at_discipline[:3])
        print(f"WARN  {path} — at-discipline: `@` on non-echo/printf command: {detail}")
        print(
            "  Recommendation: Remove `@` unless the command is `echo`, "
            "`printf`, or `:`. Hiding commands obscures failures; "
            "`make -s` is the right tool for quiet output."
        )

    if or_true:
        detail = ", ".join(f"line {ln}" for ln in or_true[:3])
        print(f"WARN  {path} — or-true-guard: `|| true` without explanation: {detail}")
        print(
            "  Recommendation: Either remove `|| true` or annotate with "
            "a comment explaining why failure is acceptable. Silent "
            "error suppression is how broken builds ship."
        )

    if long_recipes:
        detail = ", ".join(f"{name} ({n} lines)" for name, n in long_recipes[:3])
        print(
            f"WARN  {path} — recipe-length: recipe(s) exceed "
            f"{MAX_RECIPE_LINES} lines: {detail}"
        )
        print(
            "  Recommendation: Extract the recipe body into "
            "`scripts/<name>.sh` and invoke from the target. Make is "
            "a poor scripting language."
        )
    return False


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog=PROG, description="Tier-1 Makefile recipe-hygiene checker."
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
