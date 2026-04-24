#!/usr/bin/env python3
"""Deterministic Tier-1 prose pre-check for Claude Code rule files.

Flags high-confidence candidates for three Tier-2 dimensions:

- Specificity — hedged phrasing (``prefer``, ``generally``, ``usually``,
  ``consider``, ``where appropriate``, ``as appropriate``,
  ``where it makes sense``).
- Framing — prohibition-only openers (``Don't`` / ``Never`` / ``Avoid``
  at the start of the rule statement).
- Example Realism — synthetic placeholders inside fenced code blocks
  (``foo``+``bar`` pair, ``myFunction``/``myClass``/...,
  ``Widget``/``SomeClass``, ``placeholder``, ``example_*``).

All findings emit at WARN severity. WARN does not exit non-zero —
these are heuristics with legitimate exceptions (e.g., "Never log PII"
is a valid prohibition-only rule). Tier-2 remains the judgment layer.

Example:
    ./check_prose.py .claude/rules/
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

EXIT_USAGE = 2
EXIT_INTERRUPTED = 130

HEDGE_WORD_RE = re.compile(r"\b(prefer|generally|usually|consider)\b", re.IGNORECASE)
HEDGE_PHRASE_RE = re.compile(
    r"\b(where appropriate|as appropriate|where it makes sense)\b",
    re.IGNORECASE,
)
PROHIBITION_RE = re.compile(r"^(Don'?t|Never|Avoid)(\s|$)")
MARKDOWN_PREFIX_RE = re.compile(r"^(\s*(#+|[*-]|>|\*\*)\s*)+")

FOO_RE = re.compile(r"(?<![A-Za-z_])foo(?![A-Za-z_])", re.IGNORECASE)
BAR_RE = re.compile(r"(?<![A-Za-z_])bar(?![A-Za-z_])", re.IGNORECASE)
MY_IDENT_RE = re.compile(
    r"(?<![A-Za-z_])(myFunction|myClass|myObject|myVariable|myComponent)(?![A-Za-z_])"
)
GENERIC_CLASS_RE = re.compile(
    r"(?<![A-Za-z_])(Widget|MyWidget|SomeClass|SomeThing)(?![A-Za-z_])"
)
PLACEHOLDER_RE = re.compile(
    r"(?<![A-Za-z_])(placeholder|example_[A-Za-z_]+)(?![A-Za-z_])"
)

SYNTHETIC_RECOMMENDATION = (
    "Replace with real code from the codebase "
    "(actual table names, function names, module paths)"
)


def emit_warn(path: Path, detail: str, recommendation: str) -> None:
    print(f"WARN  {path} — prose: {detail}")
    print(f"  Recommendation: {recommendation}")


def frontmatter_bounds(lines: list[str]) -> tuple[int, int]:
    """Return (start, end_exclusive) indices of the frontmatter block, or (0, 0)."""
    if not lines or lines[0].rstrip("\n") != "---":
        return (0, 0)
    for i in range(1, len(lines)):
        if lines[i].rstrip("\n") == "---":
            return (0, i + 1)
    return (0, 0)


def scan_code_line(path: Path, line_no: int, line: str) -> None:
    if FOO_RE.search(line) and BAR_RE.search(line):
        emit_warn(
            path,
            f"synthetic identifier (foo/bar) in code example at line {line_no}",
            SYNTHETIC_RECOMMENDATION,
        )
    if MY_IDENT_RE.search(line):
        emit_warn(
            path,
            f"placeholder identifier (my*) in code example at line {line_no}",
            SYNTHETIC_RECOMMENDATION,
        )
    if GENERIC_CLASS_RE.search(line):
        emit_warn(
            path,
            f"placeholder class (Widget/SomeClass) in code example at line {line_no}",
            SYNTHETIC_RECOMMENDATION,
        )
    if PLACEHOLDER_RE.search(line):
        emit_warn(
            path,
            f"placeholder token in code example at line {line_no}",
            SYNTHETIC_RECOMMENDATION,
        )


def scan_prose_line(path: Path, line_no: int, line: str) -> None:
    hedge = HEDGE_WORD_RE.search(line)
    if hedge:
        emit_warn(
            path,
            f'hedged phrasing "{hedge.group(1).lower()}" at line {line_no}',
            "State the rule directly; if there are exceptions, "
            "list them in a **Exception:** line",
        )
    if HEDGE_PHRASE_RE.search(line):
        emit_warn(
            path,
            f"hedged phrase at line {line_no}",
            "Replace with a specific condition or remove the hedge",
        )

    stripped = MARKDOWN_PREFIX_RE.sub("", line)
    opener = PROHIBITION_RE.match(stripped)
    if opener:
        word = opener.group(1)
        emit_warn(
            path,
            f'prohibition-only opener "{word}" at line {line_no}',
            'Restate as a positive action ("Use X") unless '
            "no clean positive counterpart exists",
        )


def scan_file(path: Path) -> None:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as err:
        print(f"warn: cannot read {path}: {err}", file=sys.stderr)
        return

    lines = text.splitlines()
    _, fm_end = frontmatter_bounds([line + "\n" for line in lines])

    in_code = False
    for idx, line in enumerate(lines, start=1):
        if idx <= fm_end:
            continue
        if line.startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            scan_code_line(path, idx, line)
        else:
            scan_prose_line(path, idx, line)


def iter_targets(targets: list[Path]) -> list[Path]:
    resolved: list[Path] = []
    for target in targets:
        if target.is_file():
            resolved.append(target)
        elif target.is_dir():
            resolved.extend(sorted(target.rglob("*.md")))
        else:
            print(f"error: path not found: {target}", file=sys.stderr)
            raise SystemExit(EXIT_USAGE)
    return resolved


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Prose pre-check for Claude Code rule files (WARN only).",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "paths",
        nargs="+",
        type=Path,
        help="Rule files or directories to scan (directories walked for *.md).",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = get_parser().parse_args(argv)
    try:
        for file_path in iter_targets(args.paths):
            scan_file(file_path)
        return 0
    except KeyboardInterrupt:
        return EXIT_INTERRUPTED


if __name__ == "__main__":
    sys.exit(main())
