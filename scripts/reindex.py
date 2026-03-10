#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""Regenerate all _index.md files and update AGENTS.md areas in a WOS project.

Usage:
    uv run scripts/reindex.py [--root DIR]
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
_plugin_root = Path(_env_root) if _env_root and os.path.isdir(_env_root) else Path(__file__).resolve().parent.parent
if str(_plugin_root) not in sys.path:
    sys.path.insert(0, str(_plugin_root))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Regenerate _index.md files and update AGENTS.md areas.",
    )
    parser.add_argument(
        "--root",
        default=".",
        help="Project root directory (default: current directory)",
    )
    args = parser.parse_args()

    # Deferred import — keeps --help fast
    from wos.index import extract_preamble, generate_index

    root = Path(args.root).resolve()

    # Check that the docs/ directory exists with content subdirectories
    docs_dir = root / "docs"

    if not docs_dir.is_dir():
        print(
            f"No docs/ directory found under {root}",
            file=sys.stderr,
        )
        sys.exit(1)

    count = 0

    for subdir in sorted(docs_dir.iterdir()):
        if not subdir.is_dir():
            continue

        # Also index the top-level subdir itself
        if _reindex_directory(subdir, generate_index, extract_preamble):
            count += 1

        # Walk all subdirectories
        for dirpath in sorted(subdir.rglob("*")):
            if not dirpath.is_dir():
                continue
            if _reindex_directory(dirpath, generate_index, extract_preamble):
                count += 1

    print(f"Wrote {count} _index.md files.")

    # ── Update AGENTS.md areas table ────────────────────────────
    _update_agents_md_areas(root)


def _reindex_directory(directory: Path, generate_index_fn, extract_preamble_fn) -> bool:
    """Regenerate _index.md for a single directory if it has content.

    A directory has content if it contains .md files (other than _index.md)
    or subdirectories. Preserves any existing preamble text.

    Returns:
        True if _index.md was written, False if skipped.
    """
    has_md_files = any(
        f.suffix == ".md" and f.name != "_index.md"
        for f in directory.iterdir()
        if f.is_file()
    )
    has_subdirs = any(d.is_dir() for d in directory.iterdir())

    if not has_md_files and not has_subdirs:
        return False

    index_path = directory / "_index.md"
    preamble = extract_preamble_fn(index_path)
    content = generate_index_fn(directory, preamble=preamble)
    index_path.write_text(content, encoding="utf-8")
    print(index_path)
    return True


def _update_agents_md_areas(root: Path) -> None:
    """Auto-update the AGENTS.md areas table from disk state."""
    from wos.agents_md import discover_areas, extract_preferences, update_agents_md

    agents_path = root / "AGENTS.md"
    if not agents_path.is_file():
        return

    areas = discover_areas(root)
    content = agents_path.read_text(encoding="utf-8")
    preferences = extract_preferences(content)
    updated = update_agents_md(content, areas, preferences=preferences or None)
    if updated != content:
        agents_path.write_text(updated, encoding="utf-8")
        print(f"Updated AGENTS.md areas table ({len(areas)} areas).")
    else:
        print("AGENTS.md areas table already up to date.")


if __name__ == "__main__":
    main()
