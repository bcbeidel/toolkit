#!/usr/bin/env python3
"""Tier-1 Makefile secrets scanner.

Scans Makefile / GNUmakefile / *.mk for committed credentials:
  - Named API key patterns (AWS, GitHub, OpenAI, Anthropic, Stripe).
  - Credential-shaped variable assignments (TOKEN, SECRET, PASSWORD,
    API_KEY) with obvious placeholders ($VAR, {TEMPLATE}, "your-...")
    skipped.

All findings are FAIL. A FAIL excludes the file from Tier-2 judgment.

Example:
    ./check_secrets.py path/to/Makefile path/to/mk/
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

EXIT_USAGE = 64
PROG = "check_secrets.py"

_NAMED_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("AWS access key", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("GitHub personal access token", re.compile(r"ghp_[A-Za-z0-9]{36}")),
    ("GitHub fine-grained PAT", re.compile(r"github_pat_[A-Za-z0-9_]{82}")),
    ("OpenAI API key", re.compile(r"sk-[A-Za-z0-9]{48}")),
    ("Anthropic API key", re.compile(r"sk-ant-[A-Za-z0-9_-]{80,}")),
    ("Stripe live key", re.compile(r"sk_live_[A-Za-z0-9]{24}")),
]

_CREDENTIAL_VAR_RE = re.compile(
    r"(password|secret|token|api_key|access_key|private_key)"
    r"\s*[:?+]?=\s*(?P<value>[^\s#]+)",
    re.IGNORECASE,
)

_PLACEHOLDER_VALUE_PREFIXES = (
    "$",
    "{",
    "<",
    "your-",
    "your_",
    "example",
    "redacted",
    "null",
    "none",
    "undefined",
    "placeholder",
    "todo",
    "fixme",
    "xxx",
    "changeme",
    "change-me",
    "change_me",
    "foo",
    "bar",
    "baz",
    '"',
    "'",
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


def _is_placeholder(value: str) -> bool:
    lowered = value.lower().strip('"').strip("'")
    return lowered.startswith(_PLACEHOLDER_VALUE_PREFIXES) or not lowered


def _emit(path: Path, pattern_name: str, lineno: int) -> None:
    print(f"FAIL  {path} — secret: {pattern_name} at line {lineno}")
    print(
        "  Recommendation: Remove the secret and read it from a "
        "`.env` include or environment variable instead; rotate the "
        "credential if it was committed."
    )


def _scan_file(path: Path) -> bool:
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError as err:
        print(f"{PROG}: cannot read {path}: {err}", file=sys.stderr)
        return False
    any_fail = False
    for lineno, line in enumerate(lines, 1):
        for name, pattern in _NAMED_PATTERNS:
            if pattern.search(line):
                _emit(path, name, lineno)
                any_fail = True
        match = _CREDENTIAL_VAR_RE.search(line)
        if match and not _is_placeholder(match.group("value")):
            _emit(path, "credential variable assignment", lineno)
            any_fail = True
    return any_fail


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog=PROG,
        description="Tier-1 Makefile secrets scanner.",
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
