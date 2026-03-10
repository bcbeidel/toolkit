#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""Check URL reachability using wos.url_checker.

Usage:
    uv run scripts/check_url.py URL [URL ...]
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
# scripts/ → plugin root
_plugin_root = Path(_env_root) if _env_root and os.path.isdir(_env_root) else Path(__file__).resolve().parent.parent
if str(_plugin_root) not in sys.path:
    sys.path.insert(0, str(_plugin_root))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Check URL reachability via HTTP HEAD/GET.",
    )
    parser.add_argument(
        "urls",
        nargs="+",
        metavar="URL",
        help="One or more URLs to check",
    )
    args = parser.parse_args()

    from wos.url_checker import check_urls

    results = check_urls(args.urls)
    for r in results:
        print(json.dumps({
            "url": r.url,
            "reachable": r.reachable,
            "status": r.status,
            "reason": r.reason,
        }))


if __name__ == "__main__":
    main()
