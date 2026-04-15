#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""Update communication preferences in AGENTS.md.

Usage:
    python scripts/update_preferences.py --root . key=value [key=value ...]

Example:
    python scripts/update_preferences.py --root . directness=blunt verbosity=terse
"""
from __future__ import annotations

import argparse
from pathlib import Path

import _bootstrap  # noqa: F401 — side effect: adds plugin root to sys.path


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

    from wos.agents_md import discover_areas, render_preferences, update_agents_md

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
