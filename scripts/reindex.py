#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""Regenerate all _index.md files and update AGENTS.md areas in a WOS project.

Usage:
    python scripts/reindex.py [--root DIR]
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
        description="Regenerate _index.md files and update AGENTS.md areas.",
    )
    parser.add_argument(
        "--root",
        default=".",
        help="Project root directory (default: current directory)",
    )
    parser.add_argument(
        "--all-dirs",
        action="store_true",
        help="Include all directories (skip default exclusions)",
    )
    args = parser.parse_args()

    # Deferred imports — keeps --help fast
    from wos.discovery import (
        INDEX_EXCLUDED_DIRS,
        discover_document_dirs,
    )
    from wos.index import extract_preamble, generate_index

    root = Path(args.root).resolve()

    # Discover directories containing managed documents
    exclude = frozenset() if args.all_dirs else None
    doc_dirs = discover_document_dirs(root, exclude_dirs=exclude)

    if not doc_dirs:
        print("No managed documents found.", file=sys.stderr)

    count = 0
    active_excludes = frozenset() if args.all_dirs else INDEX_EXCLUDED_DIRS

    # Also collect parent directories that contain doc_dirs as subdirs
    all_dirs = set(doc_dirs)
    for d in doc_dirs:
        parent = d.parent
        while parent != root and parent != parent.parent:
            try:
                rel = parent.relative_to(root)
            except ValueError:
                break
            if rel.parts and rel.parts[0] in active_excludes:
                break
            all_dirs.add(parent)
            parent = parent.parent

    for directory in sorted(all_dirs):
        if _reindex_directory(directory, generate_index, extract_preamble):
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
