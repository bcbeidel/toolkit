#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""Assess research document state for skill resumption.

Usage:
    python plugins/wiki/skills/research/scripts/research_assess.py --file PATH
    python plugins/wiki/skills/research/scripts/research_assess.py \\
        --file PATH --gate all
    python plugins/wiki/skills/research/scripts/research_assess.py \\
        --file PATH --gate evaluator_exit
    python plugins/wiki/skills/research/scripts/research_assess.py \\
        --scan [--root DIR] [--subdir PATH]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Locate the wiki plugin root via fixed `__file__` navigation.
# plugins/wiki/skills/research/scripts/ → research/ → skills/ → plugins/wiki/
_plugin_root = Path(__file__).resolve().parent.parent.parent.parent
# Defense-in-depth: only insert the resolved root into sys.path if it
# actually looks like the wiki plugin. Marker check is the import-shadowing
# guardrail.
_wiki_marker = _plugin_root / "src" / "wiki" / "__init__.py"
if _wiki_marker.is_file() and str(_plugin_root) not in sys.path:
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
        default=".research",
        help="Subdirectory to scan (default: .research)",
    )
    parser.add_argument(
        "--gate",
        help="Check phase gate(s). Use with --file. "
             "Values: all, gatherer_exit, evaluator_exit, "
             "challenger_exit, synthesizer_exit, verifier_exit, "
             "finalizer_exit",
    )
    args = parser.parse_args()

    from wiki.research import ResearchDocument

    if args.gate and not args.file:
        parser.error("--gate requires --file")

    if args.file and args.gate:
        result = ResearchDocument.check_single_gate(args.file, args.gate)
    elif args.file:
        result = ResearchDocument.assess(args.file)
    else:
        root = str(Path(args.root).resolve())
        result = ResearchDocument.scan(root, subdir=args.subdir)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
