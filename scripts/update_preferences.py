#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""Update communication preferences in AGENTS.md.

Usage:
    uv run scripts/update_preferences.py --root . key=value [key=value ...]

Example:
    uv run scripts/update_preferences.py --root . directness=blunt verbosity=terse
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

# Ensure `import wos` works whether pip-installed or run from plugin cache.
# Prefer CLAUDE_PLUGIN_ROOT env var (set by Claude Code for hooks/MCP);
# fall back to navigating from __file__ (required for skill-invoked scripts).
_env_root = os.environ.get("CLAUDE_PLUGIN_ROOT", "")
# scripts/ → plugin root
_plugin_root = (
    Path(_env_root) if _env_root and os.path.isdir(_env_root)
    else Path(__file__).resolve().parent.parent
)
if str(_plugin_root) not in sys.path:
    sys.path.insert(0, str(_plugin_root))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Update communication preferences in AGENTS.md.",
    )
    parser.add_argument(
        "--root",
        default=".",
        help="Project root directory (default: current directory)",
    )
    parser.add_argument(
        "preferences",
        nargs="+",
        metavar="key=value",
        help="Preference key=value pairs (e.g., directness=blunt)",
    )
    args = parser.parse_args()

    from wos.agents_md import discover_areas, update_agents_md
    from wos.preferences import render_preferences

    root = Path(args.root).resolve()

    prefs = {}
    for arg in args.preferences:
        if "=" not in arg:
            parser.error(f"Invalid preference: {arg!r} (expected key=value)")
        key, value = arg.split("=", 1)
        prefs[key] = value

    rendered = render_preferences(prefs)
    areas = discover_areas(root)

    agents_path = root / "AGENTS.md"
    if agents_path.is_file():
        content = agents_path.read_text(encoding="utf-8")
    else:
        content = "# AGENTS.md\n"

    updated = update_agents_md(content, areas, preferences=rendered)
    agents_path.write_text(updated, encoding="utf-8")
    print(f"Updated preferences in {agents_path}")


if __name__ == "__main__":
    main()
