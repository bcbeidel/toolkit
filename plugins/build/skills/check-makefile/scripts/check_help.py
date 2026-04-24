#!/usr/bin/env python3
"""Tier-1 Makefile help-target checker.

Three sub-checks:
  - help-target (WARN): a `help` target is defined.
  - help-auto (WARN): the `help` recipe references `$(MAKEFILE_LIST)`
    and `##` (i.e., parses descriptions rather than hand-listing).
  - help-desc (WARN): every public target (in `.PHONY` and not
    `_`-prefixed) has a `## description` suffix on its definition
    line.

Example:
    ./check_help.py path/to/Makefile
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

EXIT_USAGE = 64
PROG = "check_help.py"

_TARGET_RE = re.compile(r"^([A-Za-z0-9_./$()%-]+)\s*:(?!=)")
_PHONY_RE = re.compile(r"^\.PHONY\s*:\s*(.*)$")
_DESC_RE = re.compile(r"^[A-Za-z0-9_./$()%-]+\s*:.*##\s+\S")


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


def _find_help_recipe(lines: list[str]) -> list[str] | None:
    """Return the recipe lines of the `help:` target, or None."""
    in_help = False
    recipe: list[str] = []
    for line in lines:
        if in_help:
            if line.startswith("\t"):
                recipe.append(line)
                continue
            if not line.strip():
                continue
            break
        match = _TARGET_RE.match(line)
        if match and match.group(1) == "help":
            in_help = True
    return recipe if in_help else None


def _scan_file(path: Path) -> bool:
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError as err:
        print(f"{PROG}: cannot read {path}: {err}", file=sys.stderr)
        return False

    phony: set[str] = set()
    target_lines: list[tuple[str, str]] = []  # (name, full line)
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
            target_lines.append((target_match.group(1), line))

    # help-target
    help_recipe = _find_help_recipe(lines)
    if help_recipe is None:
        print(f"WARN  {path} — help-target: no `help` target defined")
        print(
            "  Recommendation: Add a `help` target that parses "
            "`## description` comments from `$(MAKEFILE_LIST)`."
        )
    else:
        # help-auto
        recipe_text = "\n".join(help_recipe)
        if "$(MAKEFILE_LIST)" not in recipe_text or "##" not in recipe_text:
            print(
                f"WARN  {path} — help-auto: `help` recipe does not "
                "parse `##` from `$(MAKEFILE_LIST)`"
            )
            print(
                "  Recommendation: Replace a hand-maintained echo list "
                "with an awk parse of `$(MAKEFILE_LIST)` so new targets "
                "auto-surface in `make help`."
            )

    # help-desc — every public target needs ## description
    seen: set[str] = set()
    missing = []
    for name, full in target_lines:
        if name in seen:
            continue
        seen.add(name)
        if name.startswith("_") or name.startswith("."):
            continue
        if name not in phony:
            continue
        if name == "help":
            continue
        if not _DESC_RE.match(full):
            missing.append(name)
    if missing:
        names = ", ".join(missing)
        print(
            f"WARN  {path} — help-desc: public target(s) missing "
            f"`## description`: {names}"
        )
        print(
            "  Recommendation: Add a `## <one-line description>` suffix "
            "to each public target definition line. Targets without "
            "`##` are invisible to the parsed `make help` output."
        )
    return False


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog=PROG, description="Tier-1 Makefile help-target checker."
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
