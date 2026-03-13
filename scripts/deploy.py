#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""Deploy WOS skills to a target project's .agents/ directory.

Copies skills, scripts, and the wos package into <target>/.agents/ for use
with GitHub Copilot and other Agent Skills-compatible copilots.

Usage:
    python scripts/deploy.py --target /path/to/project [--dry-run]
"""
from __future__ import annotations

import argparse
import os
import shutil
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

# Directories to copy from plugin root into <target>/.agents/
SOURCE_DIRS = ["skills", "scripts", "wos"]

# Directories and extensions to exclude from the deployed output
EXCLUDE_DIRS = {"__pycache__"}
EXCLUDE_EXTENSIONS = {".pyc"}


def should_exclude(path: Path) -> bool:
    """Return True if the path should be excluded from deployment."""
    if path.suffix in EXCLUDE_EXTENSIONS:
        return True
    for part in path.parts:
        if part in EXCLUDE_DIRS:
            return True
    return False


def discover_files(plugin_root: Path) -> list[Path]:
    """Walk source directories and return list of files to deploy."""
    files: list[Path] = []
    for dir_name in SOURCE_DIRS:
        source_dir = plugin_root / dir_name
        if not source_dir.is_dir():
            continue
        for root, _dirs, filenames in os.walk(source_dir):
            for filename in filenames:
                abs_path = Path(root) / filename
                rel_path = abs_path.relative_to(plugin_root)
                if not should_exclude(rel_path):
                    files.append(rel_path)
    return sorted(files)


def deploy(plugin_root: Path, target: Path, dry_run: bool = False) -> list[str]:
    """Deploy WOS files to target/.agents/.

    Returns a list of actions taken (or that would be taken in dry-run mode).
    """
    agents_dir = target / ".agents"
    files = discover_files(plugin_root)
    actions: list[str] = []

    for rel_path in files:
        src = plugin_root / rel_path
        dst = agents_dir / rel_path

        action = f"copy {rel_path} → {dst.relative_to(target)}"
        actions.append(action)

        if dry_run:
            continue

        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(str(src), str(dst))

    return actions


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Deploy WOS skills to a target project's .agents/ directory.",
    )
    parser.add_argument(
        "--target",
        required=True,
        help="Target project directory",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be copied without writing",
    )
    args = parser.parse_args()

    target = Path(args.target).resolve()
    if not target.is_dir():
        print(f"Error: target directory does not exist: {target}", file=sys.stderr)
        sys.exit(1)

    actions = deploy(_plugin_root, target, dry_run=args.dry_run)

    if args.dry_run:
        print(f"Dry run: {len(actions)} files would be deployed to {target / '.agents'}")
        for action in actions:
            print(f"  {action}")
    else:
        print(f"Deployed {len(actions)} files to {target / '.agents'}")


if __name__ == "__main__":
    main()
