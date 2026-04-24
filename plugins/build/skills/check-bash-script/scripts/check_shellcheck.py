#!/usr/bin/env python3
"""Tier-1 bash lint check wrapping `shellcheck`.

Runs shellcheck on each target with a curated rule selector, parses the
JSON output, maps each finding's rule code to FAIL or WARN, and emits
findings in the toolkit's fixed lint format.

shellcheck is optional — when absent, emits a single INFO line and
exits 0. Other Tier-1 scripts continue to run.

Example:
    ./check_shellcheck.py path/to/script.sh path/to/scripts/
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

EXIT_USAGE = 64
SHELLCHECK_CMD = "shellcheck"

_BASH_SHEBANGS = ("#!/usr/bin/env bash", "#!/bin/bash", "#!/usr/bin/env -S bash")
_BASH_EXTENSIONS = (".sh", ".bash")

_FAIL_CODES = frozenset(
    {
        "SC2086",
        "SC2046",
        "SC2068",
        "SC2294",
        "SC2010",
        "SC2012",
        "SC2045",
    }
)

_INCLUDED_CODES = (
    "SC2086",
    "SC2046",
    "SC2068",
    "SC2294",
    "SC2010",
    "SC2012",
    "SC2045",
    "SC2154",
    "SC2155",
    "SC2006",
    "SC2013",
    "SC2162",
    "SC2038",
    "SC2164",
    "SC2002",
)

_RECOMMENDATIONS = {
    "SC2086": 'Quote the expansion: "${var}" or "$(cmd)".',
    "SC2046": 'Quote the expansion: "${var}" or "$(cmd)".',
    "SC2068": 'Use "$@" to forward arguments — never unquoted $@.',
    "SC2294": 'Invoke the array directly: "${arr[@]}" — never call eval on it.',
    "SC2154": (
        "Assign the variable, set a default ${var:-x}, or guard with ${var:?msg}."
    ),
    "SC2155": (
        'Split: `local x` then `x="$(cmd)"` to preserve the substitution exit status.'
    ),
    "SC2006": "Replace backticks with $(...) — nestable and readable.",
    "SC2010": "Do not parse ls — use globs or find -print0 | xargs -0.",
    "SC2012": "Do not parse ls — use globs or find -print0 | xargs -0.",
    "SC2045": "Do not parse ls — use globs or find -print0 | xargs -0.",
    "SC2013": "Use while IFS= read -r line; do ...; done < file for iteration.",
    "SC2162": "Use while IFS= read -r line; do ...; done < file for iteration.",
    "SC2038": "Use find -print0 | xargs -0 or -exec {} + for filename safety.",
    "SC2164": "Add `|| exit` after `cd`, or rely on `set -e` and document.",
    "SC2002": "Pipe directly: cmd file instead of cat file | cmd (style-only).",
}

_INSTALL_HINT = (
    "Install shellcheck — 'brew install shellcheck' (macOS), "
    "'apt install shellcheck' (Debian/Ubuntu), 'dnf install ShellCheck' (Fedora)."
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
            print(f"check_shellcheck.py: path not found: {target}", file=sys.stderr)
            raise _UsageError
    return files


def _severity_for(code: str) -> str:
    return "FAIL" if code in _FAIL_CODES else "WARN"


def _recommendation_for(code: str) -> str:
    return _RECOMMENDATIONS.get(
        code,
        f"See https://www.shellcheck.net/wiki/{code} for details.",
    )


def _run_shellcheck(target: Path) -> list[dict]:
    include = ",".join(_INCLUDED_CODES)
    try:
        result = subprocess.run(
            [SHELLCHECK_CMD, f"--include={include}", "--format=json", str(target)],
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError as err:
        print(f"check_shellcheck.py: cannot exec shellcheck: {err}", file=sys.stderr)
        return []
    if not result.stdout.strip():
        return []
    try:
        parsed = json.loads(result.stdout)
    except json.JSONDecodeError as err:
        print(
            f"check_shellcheck.py: malformed shellcheck output for {target}: {err}",
            file=sys.stderr,
        )
        return []
    return parsed if isinstance(parsed, list) else []


def _check_file(target: Path) -> bool:
    any_fail = False
    for finding in _run_shellcheck(target):
        code_num = finding.get("code")
        if code_num is None:
            continue
        code = f"SC{code_num}"
        message = finding.get("message", "").rstrip()
        lineno = finding.get("line", 0)
        col = finding.get("column", 0)
        severity = _severity_for(code)
        print(f"{severity}  {target} — {code}: {message} (line {lineno}:{col})")
        print(f"  Recommendation: {_recommendation_for(code)}")
        if severity == "FAIL":
            any_fail = True
    return any_fail


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="check_shellcheck.py",
        description="Tier-1 bash lint check via shellcheck (curated rule set).",
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
    if shutil.which(SHELLCHECK_CMD) is None:
        print(
            f"INFO  <{SHELLCHECK_CMD}> — tool-missing: shellcheck not installed; "
            f"{len(_INCLUDED_CODES)} rule codes skipped"
        )
        print(f"  Recommendation: {_INSTALL_HINT}")
        return 0
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
