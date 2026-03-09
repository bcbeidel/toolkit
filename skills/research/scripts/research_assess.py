#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""Assess research document state for skill resumption.

Usage:
    uv run skills/research/scripts/research_assess.py --file PATH
    uv run skills/research/scripts/research_assess.py --scan [--root DIR] [--subdir PATH]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Ensure `import wos` works whether pip-installed or run from plugin cache.
_plugin_root = Path(__file__).resolve().parent.parent.parent.parent
if str(_plugin_root) not in sys.path:
    sys.path.insert(0, str(_plugin_root))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Assess research document state.",
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--file",
        help="Assess a single research document",
    )
    group.add_argument(
        "--scan",
        action="store_true",
        help="Scan for all research documents",
    )
    parser.add_argument(
        "--root",
        default=".",
        help="Project root directory (default: current directory)",
    )
    parser.add_argument(
        "--subdir",
        default="docs/research",
        help="Subdirectory to scan (default: docs/research)",
    )
    args = parser.parse_args()

    from wos.research.assess_research import assess_file, scan_directory

    if args.file:
        result = assess_file(args.file)
    else:
        root = str(Path(args.root).resolve())
        result = scan_directory(root, subdir=args.subdir)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
