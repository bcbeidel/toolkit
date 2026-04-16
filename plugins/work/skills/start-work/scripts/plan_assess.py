#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""Assess plan document state for skill execution and resumption.

Usage:
    python plugins/work/skills/start-work/scripts/plan_assess.py --file PATH
    python plugins/work/skills/start-work/scripts/plan_assess.py \\
        --scan [--root DIR] [--subdir PATH]
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Assess plan document state.",
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--file",
        help="Assess a single plan document",
    )
    group.add_argument(
        "--scan",
        action="store_true",
        help="Find all executing plans",
    )
    parser.add_argument(
        "--root",
        default=".",
        help="Project root directory (default: current directory)",
    )
    parser.add_argument(
        "--subdir",
        default="docs/plans",
        help="Subdirectory to scan (default: docs/plans)",
    )
    args = parser.parse_args()

    from wiki.plan import PlanDocument

    if args.file:
        result = PlanDocument.assess(args.file)
    else:
        root = str(Path(args.root).resolve())
        result = PlanDocument.scan(root, subdir=args.subdir)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
