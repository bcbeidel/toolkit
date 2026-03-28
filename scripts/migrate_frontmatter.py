#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""Migrate WOS document frontmatter from flat to metadata format.

Moves all fields except name and description under a metadata map,
aligning with the Agent Skills superset convention.

Usage:
    python scripts/migrate_frontmatter.py [--root DIR] [--dry-run] [--check]
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

# Ensure `import wos` works whether pip-installed or run from plugin cache.
_env_root = os.environ.get("CLAUDE_PLUGIN_ROOT", "")
# scripts/ -> plugin root
_plugin_root = (
    Path(_env_root) if _env_root and os.path.isdir(_env_root)
    else Path(__file__).resolve().parent.parent
)
sys.path.insert(0, str(_plugin_root))

from wos.frontmatter import parse_frontmatter  # noqa: E402

# Fields that stay top-level (Agent Skills base fields).
_TOP_LEVEL = {"name", "description"}

# Files to skip (not WOS-managed documents).
_SKIP_NAMES = {"_index.md", "SKILL.md", "AGENTS.md", "CLAUDE.md", "README.md"}


def _serialize_frontmatter(
    top: dict,
    metadata: dict,
) -> str:
    """Serialize frontmatter dict back to YAML string."""
    lines = ["---"]

    for key, value in top.items():
        if value is None:
            lines.append(f"{key}:")
        else:
            lines.append(f"{key}: {value}")

    if metadata:
        lines.append("metadata:")
        for key, value in metadata.items():
            if value is None:
                lines.append(f"  {key}:")
            elif isinstance(value, list):
                lines.append(f"  {key}:")
                for item in value:
                    lines.append(f"    - {item}")
            else:
                lines.append(f"  {key}: {value}")

    lines.append("---")
    return "\n".join(lines) + "\n"


def _needs_migration(fm: dict) -> bool:
    """Check if frontmatter has fields that should be in metadata."""
    # Already migrated: has a metadata dict with content
    if isinstance(fm.get("metadata"), dict) and fm["metadata"]:
        return False
    # Check for top-level fields that belong in metadata
    for key in fm:
        if key not in _TOP_LEVEL and key != "metadata":
            return True
    return False


def migrate_file(path: Path, dry_run: bool = False) -> bool:
    """Migrate a single file's frontmatter. Returns True if changed."""
    text = path.read_text(encoding="utf-8")

    try:
        fm, body = parse_frontmatter(text)
    except ValueError:
        return False

    if not _needs_migration(fm):
        return False

    # Split into top-level and metadata fields
    top = {}
    metadata = {}
    for key, value in fm.items():
        if key in _TOP_LEVEL:
            top[key] = value
        elif key == "metadata":
            # Existing metadata (shouldn't happen if _needs_migration passed)
            if isinstance(value, dict):
                metadata.update(value)
        else:
            metadata[key] = value

    new_text = _serialize_frontmatter(top, metadata) + body

    if not dry_run:
        path.write_text(new_text, encoding="utf-8")

    return True


def discover_files(root: Path) -> list:
    """Find all .md files eligible for migration."""
    files = []
    for md_path in sorted(root.rglob("*.md")):
        if md_path.name in _SKIP_NAMES:
            continue
        # Skip hidden dirs, .git, node_modules, .venv, etc.
        parts = md_path.relative_to(root).parts
        skip_dirs = ("node_modules", "__pycache__")
        if any(p.startswith(".") or p in skip_dirs for p in parts):
            continue
        files.append(md_path)
    return files


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Migrate WOS frontmatter to metadata format."
    )
    parser.add_argument("--root", type=Path, default=Path.cwd(),
                        help="Project root (default: CWD)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print changes without writing")
    parser.add_argument("--check", action="store_true",
                        help="Exit 1 if any files need migration")
    args = parser.parse_args()

    root = args.root.resolve()
    files = discover_files(root)
    changed = []

    for path in files:
        if migrate_file(path, dry_run=args.dry_run or args.check):
            rel = path.relative_to(root)
            changed.append(str(rel))
            if args.dry_run:
                print(f"  would migrate: {rel}")
            elif not args.check:
                print(f"  migrated: {rel}")

    if args.check:
        if changed:
            print(f"{len(changed)} file(s) need migration:")
            for f in changed:
                print(f"  {f}")
            sys.exit(1)
        else:
            print("All files already migrated.")
            sys.exit(0)

    if not changed:
        print("No files needed migration.")
    else:
        verb = "would be" if args.dry_run else ""
        print(f"\n{len(changed)} file(s) {verb} migrated.")


if __name__ == "__main__":
    main()
