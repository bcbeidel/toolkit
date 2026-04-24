#!/usr/bin/env python3
"""Scan Claude Code rule files for committed-secret patterns.

Tier-1 "Secrets Safety" check. Scans rule-file bodies (frontmatter
skipped) for six well-known API-key shapes and for credential-shaped
variable assignments. Obvious placeholder values (``your-``,
``example``, ``placeholder``, ``todo``, ``foo``/``bar``/``baz``, etc.)
are excluded from the generic credential match.

Example:
    ./scan_secrets.py .claude/rules/
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

EXIT_USAGE = 2
EXIT_INTERRUPTED = 130

KNOWN_PATTERNS: dict[str, re.Pattern[str]] = {
    "AWS access key": re.compile(r"AKIA[0-9A-Z]{16}"),
    "GitHub personal access token": re.compile(r"ghp_[A-Za-z0-9]{36}"),
    "GitHub fine-grained PAT": re.compile(r"github_pat_[A-Za-z0-9_]{82}"),
    "OpenAI API key": re.compile(r"sk-[A-Za-z0-9]{48}"),
    "Anthropic API key": re.compile(r"sk-ant-[A-Za-z0-9_-]{80,}"),
    "Stripe live key": re.compile(r"sk_live_[A-Za-z0-9]{24}"),
}

CRED_VAR_RE = re.compile(
    r"(?P<name>password|secret|token|api_key|access_key|private_key)"
    r"\s*[=:]\s*"
    r"(?P<quote>[\"'])(?P<value>[^\"']+)(?P=quote)",
    re.IGNORECASE,
)

PLACEHOLDER_VALUE_RE = re.compile(
    r"^\s*("
    r"your[-_]|example|redacted|null|none|undefined|placeholder|todo|fixme|"
    r"xxx|changeme|change[-_]me|foo|bar|baz|abc|xyz"
    r")",
    re.IGNORECASE,
)
PLACEHOLDER_PREFIX_CHARS = ("$", "{", "<")


def emit_finding(path: Path, name: str, line_no: int) -> None:
    print(f"FAIL  {path} — Secrets Safety: {name} at line {line_no}")
    print(
        "  Recommendation: Remove the secret, rotate the credential, "
        "and reference it via env var name instead."
    )


def frontmatter_end_line(lines: list[str]) -> int:
    """1-based line number of the closing ``---`` of frontmatter, else 0."""
    if not lines or lines[0] != "---":
        return 0
    for i in range(1, len(lines)):
        if lines[i] == "---":
            return i + 1
    return 0


def looks_like_placeholder(value: str) -> bool:
    if not value:
        return True
    if value[0] in PLACEHOLDER_PREFIX_CHARS:
        return True
    return bool(PLACEHOLDER_VALUE_RE.match(value))


def scan_file(path: Path) -> bool:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as err:
        print(f"warn: cannot read {path}: {err}", file=sys.stderr)
        return True

    lines = text.splitlines()
    fm_end = frontmatter_end_line(lines)

    found_any = False
    for idx, line in enumerate(lines, start=1):
        if idx <= fm_end:
            continue
        for name, pattern in KNOWN_PATTERNS.items():
            if pattern.search(line):
                emit_finding(path, name, idx)
                found_any = True
        for match in CRED_VAR_RE.finditer(line):
            if looks_like_placeholder(match.group("value")):
                continue
            emit_finding(path, "credential variable assignment", idx)
            found_any = True
    return not found_any


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
        description="Scan Claude Code rule files for committed secrets.",
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
        all_clean = True
        for file_path in iter_targets(args.paths):
            if not scan_file(file_path):
                all_clean = False
        return 0 if all_clean else 1
    except KeyboardInterrupt:
        return EXIT_INTERRUPTED


if __name__ == "__main__":
    sys.exit(main())
