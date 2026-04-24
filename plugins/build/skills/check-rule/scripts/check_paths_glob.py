#!/usr/bin/env python3
"""Validate `paths:` globs in Claude Code rule-file frontmatter.

Each entry is checked for: empty pattern, unbalanced ``{...}``,
unbalanced ``[...]``, and control characters. Supports single-line
inline lists (``paths: ["a", "b"]``) and block lists
(``paths:\\n  - "a"\\n  - "b"``). Files without frontmatter or
without a ``paths:`` key are skipped silently.

Example:
    ./check_paths_glob.py .claude/rules/
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

EXIT_USAGE = 2
EXIT_INTERRUPTED = 130

CONTROL_CHAR_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")
INLINE_RE = re.compile(r"^paths:\s*\[(?P<body>.*)\]\s*$")
BLOCK_HEADER_RE = re.compile(r"^paths:\s*$")
BLOCK_ITEM_RE = re.compile(r"^\s+-\s+(?P<value>.*\S)\s*$")


def emit_fail(path: Path, detail: str, recommendation: str) -> None:
    print(f"FAIL  {path} — paths glob validity: {detail}")
    print(f"  Recommendation: {recommendation}")


def strip_quotes(s: str) -> str:
    if len(s) >= 2 and s[0] == s[-1] and s[0] in ("'", '"'):
        return s[1:-1]
    return s


def split_top_level(body: str) -> list[str]:
    """Split a comma-separated inline list, respecting brace/bracket depth."""
    items: list[str] = []
    depth = 0
    start = 0
    for i, ch in enumerate(body):
        if ch in "{[":
            depth += 1
        elif ch in "}]":
            depth -= 1
        elif ch == "," and depth == 0:
            items.append(body[start:i])
            start = i + 1
    items.append(body[start:])
    return [strip_quotes(item.strip()) for item in items]


def extract_paths_entries(lines: list[str]) -> list[tuple[int, str]]:
    """Return (line_number, entry) tuples for every `paths:` glob."""
    if not lines or lines[0].rstrip("\n") != "---":
        return []

    end = next(
        (i for i in range(1, len(lines)) if lines[i].rstrip("\n") == "---"),
        None,
    )
    if end is None:
        return []

    entries: list[tuple[int, str]] = []
    in_block = False

    for idx in range(1, end):
        line = lines[idx].rstrip("\n")
        inline = INLINE_RE.match(line)
        if inline:
            in_block = False
            for item in split_top_level(inline["body"]):
                entries.append((idx + 1, item))
            continue
        if BLOCK_HEADER_RE.match(line):
            in_block = True
            continue
        if in_block:
            item = BLOCK_ITEM_RE.match(line)
            if item:
                entries.append((idx + 1, strip_quotes(item["value"].strip())))
                continue
            if line.strip() == "":
                continue
            in_block = False
    return entries


def validate_entry(path: Path, line_no: int, entry: str) -> bool:
    ok = True
    stripped = entry.strip()

    if not stripped:
        emit_fail(
            path,
            f"empty pattern at line {line_no}",
            "Remove the empty entry or replace with a valid glob",
        )
        return False

    if CONTROL_CHAR_RE.search(entry):
        emit_fail(
            path,
            f"control character in pattern at line {line_no}",
            "Remove non-printable characters from the pattern",
        )
        ok = False

    if entry.count("{") != entry.count("}"):
        emit_fail(
            path,
            f'unclosed brace in "{entry}" at line {line_no}',
            'Close the brace (e.g., "src/**/*.{ts,tsx}")',
        )
        ok = False

    if entry.count("[") != entry.count("]"):
        emit_fail(
            path,
            f'unclosed bracket in "{entry}" at line {line_no}',
            'Close the bracket (e.g., "src/**/*.[ch]")',
        )
        ok = False

    return ok


def check_file(path: Path) -> bool:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as err:
        print(f"warn: cannot read {path}: {err}", file=sys.stderr)
        return True

    lines = text.splitlines(keepends=True)
    all_ok = True
    for line_no, entry in extract_paths_entries(lines):
        if not validate_entry(path, line_no, entry):
            all_ok = False
    return all_ok


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
        description="Validate paths: globs in Claude Code rule frontmatter.",
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
        files = iter_targets(args.paths)
        all_ok = True
        for file_path in files:
            if not check_file(file_path):
                all_ok = False
        return 0 if all_ok else 1
    except KeyboardInterrupt:
        return EXIT_INTERRUPTED


if __name__ == "__main__":
    sys.exit(main())
