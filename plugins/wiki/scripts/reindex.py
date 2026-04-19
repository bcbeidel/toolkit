#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""Create _index.md files for managed areas and the wiki/ subtree.

Reads directories from the AGENTS.md areas table and creates a
<dir>/_index.md listing all managed documents with their descriptions.
Also refreshes the AGENTS.md areas table, preserving existing descriptions.

First-run fallback: if AGENTS.md has no areas table, scans the docs/
subtree to discover directories.

Wiki mode (auto-activated when wiki/SCHEMA.md is present):
Walks the wiki/ subtree recursively. For each subdirectory with .md files,
writes a flat _index.md. Writes a tree-view root wiki/_index.md with a
heading per subdirectory. Skips log.md, SCHEMA.md, and _index.md.

Usage:
    python3 scripts/reindex.py --root .
"""
from __future__ import annotations

import argparse
import os
from pathlib import Path

import _bootstrap  # noqa: F401 — side effect: adds src/ to sys.path  # isort: skip


_SKIP = frozenset({
    "node_modules", "__pycache__", "venv", ".venv",
    "dist", "build", ".tox", ".mypy_cache", ".pytest_cache",
})

_WIKI_SKIP = frozenset({"_index.md", "SCHEMA.md", "log.md"})


def _read_frontmatter_field(path: Path, field: str) -> str:
    """Read a single scalar field from YAML frontmatter (stdlib-only)."""
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return ""
    if not text.startswith("---"):
        return ""
    end = text.find("---", 3)
    if end == -1:
        return ""
    fm = text[3:end]
    for line in fm.splitlines():
        if line.startswith(f"{field}:"):
            value = line[len(field) + 1:].strip()
            if len(value) >= 2 and value[0] in ('"', "'") and value[-1] == value[0]:
                value = value[1:-1]
            return value
    return ""


def _write_index(directory: Path, root: Path) -> None:
    """Write <directory>/_index.md listing all .md files with descriptions."""
    md_files = sorted(
        f for f in directory.iterdir()
        if f.is_file() and f.suffix == ".md" and f.name != "_index.md"
    )
    if not md_files:
        return

    try:
        rel_dir = str(directory.relative_to(root))
    except ValueError:
        rel_dir = str(directory)

    lines = [
        f"# {rel_dir}",
        "",
        "| File | Description |",
        "|------|-------------|",
    ]
    for f in md_files:
        desc = _read_frontmatter_field(f, "description") or ""
        lines.append(f"| [{f.name}]({f.name}) | {desc} |")

    (directory / "_index.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def _scan_docs_subtree(root: Path) -> list[Path]:
    """Fallback: scan docs/ for directories that contain .md files."""
    docs_root = root / "docs"
    if not docs_root.is_dir():
        return []
    dirs: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(docs_root):
        dirnames[:] = sorted(
            d for d in dirnames
            if not d.startswith(".") and d not in _SKIP
        )
        if any(f.endswith(".md") and f != "_index.md" for f in filenames):
            dirs.append(Path(dirpath))
    return dirs


def _reindex_wiki(wiki_dir: Path, root: Path) -> None:
    """Generate _index.md files for the wiki/ subtree.

    For each subdirectory with .md files, writes a flat _index.md (via
    _write_index). Writes a tree-view root wiki/_index.md with one
    ``## dirname`` heading per subdirectory. Skips log.md, SCHEMA.md,
    and _index.md throughout.
    """
    root_pages: list[Path] = []
    subdir_entries: list[tuple[str, list[Path]]] = []
    subdir_count = 0

    for dirpath, dirnames, filenames in os.walk(wiki_dir):
        dirnames[:] = sorted(d for d in dirnames if not d.startswith("."))
        current = Path(dirpath)
        md_files = sorted(
            current / f for f in filenames
            if f.endswith(".md") and f not in _WIKI_SKIP
        )
        if not md_files:
            continue

        if current == wiki_dir:
            root_pages = md_files
        else:
            # Write per-subdirectory flat _index.md
            _write_index(current, root)
            rel_name = current.relative_to(wiki_dir).parts[0]
            subdir_entries.append((rel_name, md_files))
            subdir_count += 1

    # Write root wiki/_index.md as a tree view
    lines: list[str] = ["# wiki", ""]

    for subdir_name, pages in sorted(subdir_entries):
        lines.append(f"## {subdir_name}")
        lines.append("")
        lines.append("| File | Description |")
        lines.append("|------|-------------|")
        for p in sorted(pages):
            desc = _read_frontmatter_field(p, "description") or ""
            rel = p.relative_to(wiki_dir / subdir_name)
            lines.append(f"| [{rel}]({subdir_name}/{rel}) | {desc} |")
        lines.append("")

    if root_pages:
        if subdir_entries:
            lines.append("## (root)")
            lines.append("")
        lines.append("| File | Description |")
        lines.append("|------|-------------|")
        for p in root_pages:
            desc = _read_frontmatter_field(p, "description") or ""
            lines.append(f"| [{p.name}]({p.name}) | {desc} |")
        lines.append("")

    if subdir_entries or root_pages:
        (wiki_dir / "_index.md").write_text(
            "\n".join(lines) + "\n", encoding="utf-8"
        )

    print(
        f"Wiki: reindexed {subdir_count} "
        f"subdirector{'y' if subdir_count == 1 else 'ies'}"
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Create _index.md files for managed areas and refresh "
            "the AGENTS.md areas table."
        ),
    )
    parser.add_argument(
        "--root",
        default=".",
        help="Project root directory (default: current directory)",
    )
    args = parser.parse_args()

    from wiki.agents_md import extract_areas, update_agents_md

    root = Path(args.root).resolve()
    agents_path = root / "AGENTS.md"

    # Read existing areas (descriptions) from AGENTS.md
    existing_desc: dict[str, str] = {}
    agents_content: str = ""
    if agents_path.is_file():
        agents_content = agents_path.read_text(encoding="utf-8")
        for area in extract_areas(agents_content):
            existing_desc[area["path"]] = area["name"]

    # Determine which directories to index
    if existing_desc:
        # Option B: only index directories already registered as managed areas
        dirs = [
            root / rel for rel in existing_desc
            if (root / rel).is_dir()
        ]
    else:
        # First-run fallback: scan docs/ subtree
        dirs = _scan_docs_subtree(root)
        if not dirs:
            print("No areas in AGENTS.md and no docs/ directory — nothing to reindex")
            return

    # Create _index.md for each area directory
    for d in dirs:
        _write_index(d, root)

    # Refresh AGENTS.md areas table (preserving human descriptions)
    if agents_path.is_file():
        refreshed: list[dict[str, str]] = []
        for d in dirs:
            try:
                rel = str(d.relative_to(root))
            except ValueError:
                continue
            name = existing_desc.get(rel, rel)
            refreshed.append({"name": name, "path": rel})

        updated = update_agents_md(agents_content, areas=refreshed)
        agents_path.write_text(updated, encoding="utf-8")
        print(f"Updated {len(refreshed)} area(s) in {agents_path}")
    else:
        print(f"AGENTS.md not found at {agents_path} — skipping areas update")

    n = len(dirs)
    print(f"Reindexed {n} director{'y' if n == 1 else 'ies'}")

    # Wiki mode — auto-activated when wiki/SCHEMA.md is present
    wiki_dir = root / "wiki"
    if (wiki_dir / "SCHEMA.md").is_file():
        _reindex_wiki(wiki_dir, root)


if __name__ == "__main__":
    main()
