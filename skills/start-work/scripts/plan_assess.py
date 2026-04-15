#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""Assess plan document state for skill execution and resumption.

Usage:
    python skills/start-work/scripts/plan_assess.py --file PATH
    python skills/start-work/scripts/plan_assess.py --scan [--root DIR] [--subdir PATH]
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

# Ensure `import wos` works whether pip-installed or run from plugin cache.
# Prefer CLAUDE_PLUGIN_ROOT env var (set by Claude Code for hooks/MCP);
# fall back to navigating from __file__ (required for skill-invoked scripts).
_env_root = os.environ.get("CLAUDE_PLUGIN_ROOT", "")
# skills/start-work/scripts/ → skills/start-work/ → skills/ → plugin root
_plugin_root = (
    Path(_env_root) if _env_root and os.path.isdir(_env_root)
    else Path(__file__).resolve().parent.parent.parent.parent
)
if str(_plugin_root) not in sys.path:
    sys.path.insert(0, str(_plugin_root))


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

    from wos.plan import assess_file, scan_plans

    if args.file:
        result = assess_file(args.file)
    else:
        root = str(Path(args.root).resolve())
        result = scan_plans(root, subdir=args.subdir)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
