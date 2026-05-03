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
import sys
from pathlib import Path

# Discover the installed wiki plugin so `from wiki.plan import PlanDocument`
# below resolves when the package was not pip-installed. The script lives at
# plugins/work/skills/start-work/scripts/<file> and the wiki plugin lives at
# plugins/wiki/, so the candidate location is reachable via parents[4]/wiki.
_candidate = Path(__file__).resolve().parents[4] / "wiki"


def _is_legitimate_wiki_plugin(p: Path) -> bool:
    """Strict containment check before sys.path registration.

    Returns True only when the candidate directory has the expected name,
    sits directly under a parent named 'plugins', and exposes the wiki
    package marker file. Any deviation means we refuse to register it,
    blocking import shadowing if the script is relocated to an unexpected
    layout.
    """
    return (
        p.name == "wiki"
        and p.parent.name == "plugins"
        and (p / "src" / "wiki" / "__init__.py").is_file()
    )


if _is_legitimate_wiki_plugin(_candidate) and str(_candidate) not in sys.path:
    sys.path.insert(0, str(_candidate))


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
        default=".plans",
        help="Subdirectory to scan (default: .plans)",
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
