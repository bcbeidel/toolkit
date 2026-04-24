#!/usr/bin/env python3
"""Tier-1 bash secrets scanner.

Scans .sh/.bash files for committed credentials:
  - Named API key patterns (AWS, GitHub, OpenAI, Anthropic, Stripe).
  - Credential-shaped variable assignments (PASSWORD=, TOKEN=, etc.),
    with obvious placeholders ($VAR, {TEMPLATE}, "your-...", etc.) skipped.

All findings are FAIL. A FAIL excludes the file from Tier-2 judgment.

Example:
    ./check_secrets.py path/to/script.sh path/to/scripts/
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

EXIT_USAGE = 64

_BASH_SHEBANGS = ("#!/usr/bin/env bash", "#!/bin/bash", "#!/usr/bin/env -S bash")
_BASH_EXTENSIONS = (".sh", ".bash")

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
    r"\s*=\s*(?P<q>[\"'])(?P<value>[^\"']+)(?P=q)",
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
    "abc",
    "xyz",
)


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
            print(f"check_secrets.py: path not found: {target}", file=sys.stderr)
            raise _UsageError
    return files


def _emit(path: Path, pattern_name: str, lineno: int) -> None:
    print(f"FAIL  {path} — secret: {pattern_name} at line {lineno}")
    print(
        "  Recommendation: Remove the secret, rotate the credential, "
        'and read it from "${VAR:?VAR required}" instead.'
    )


def _is_placeholder(value: str) -> bool:
    return value.lower().startswith(_PLACEHOLDER_VALUE_PREFIXES)


def _scan_file(path: Path) -> bool:
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError as err:
        print(f"check_secrets.py: cannot read {path}: {err}", file=sys.stderr)
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
        prog="check_secrets.py",
        description=(
            "Tier-1 bash secrets scanner (named API keys + credential assignments)."
        ),
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
            if _scan_file(f):
                any_fail = True
    except _UsageError:
        return EXIT_USAGE
    except KeyboardInterrupt:
        return 130
    return 1 if any_fail else 0


if __name__ == "__main__":
    sys.exit(main())
