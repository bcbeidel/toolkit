#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""Deploy WOS skills to a target project or platform via symlinks.

Platform-level (symlinks into platform's home directory):
    python scripts/deploy.py --platform copilot [--dry-run]

Project-level (symlinks into <target>/.agents/):
    python scripts/deploy.py --target /path/to/project [--dry-run]
"""
from __future__ import annotations

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path

import _bootstrap

_plugin_root = _bootstrap.plugin_root

# Support directories symlinked alongside skills
SUPPORT_DIRS = ["scripts", "wos"]

# Platform registry — (display_name, base_path_relative_to_home)
PLATFORMS: dict[str, tuple[str, str]] = {
    "copilot": ("GitHub Copilot", ".copilot"),
    "cursor": ("Cursor", ".cursor"),
    "claude": ("Claude Code", ".claude"),
    "codex": ("Codex CLI", ".codex"),
    "gemini": ("Gemini CLI", ".gemini"),
    "windsurf": ("Windsurf", os.path.join(".codeium", "windsurf")),
    "opencode": ("OpenCode", os.path.join(".config", "opencode")),
}


def resolve_platform_path(platform: str) -> Path:
    """Resolve a platform name to its base directory under $HOME."""
    _, rel_path = PLATFORMS[platform]
    return Path.home() / rel_path


def discover_skills(plugin_root: Path) -> list[str]:
    """Return sorted list of skill directory names."""
    skills_dir = plugin_root / "skills"
    if not skills_dir.is_dir():
        return []
    return sorted(
        d.name for d in skills_dir.iterdir()
        if d.is_dir() and not d.name.startswith(".")
    )


def _backup_path(path: Path) -> Path:
    """Generate a timestamped backup path."""
    timestamp = datetime.now().strftime("%Y%m%dT%H%M%S")
    return path.with_name(f"{path.name}.backup_{timestamp}")


def _link_dir(src: Path, dst: Path, dry_run: bool) -> str:
    """Create a symlink from dst → src. Returns action description."""
    # Already correctly linked
    if dst.is_symlink() and dst.resolve() == src.resolve():
        return f"skip {dst.name} (already linked)"

    # Back up existing directory or stale symlink
    if dst.exists() or dst.is_symlink():
        backup = _backup_path(dst)
        if not dry_run:
            dst.rename(backup)

    if not dry_run:
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.symlink_to(src, target_is_directory=True)

    return f"link {dst} → {src}"


def deploy(plugin_root: Path, target_dir: Path, dry_run: bool = False) -> list[str]:
    """Deploy WOS via symlinks into target directory.

    Symlinks individual skill directories into <target>/skills/ and
    support directories (scripts, wos) directly into <target>/.

    Returns a list of actions taken (or that would be taken in dry-run mode).
    """
    actions: list[str] = []

    # Symlink support directories
    for dir_name in SUPPORT_DIRS:
        src = plugin_root / dir_name
        if not src.is_dir():
            continue
        dst = target_dir / dir_name
        actions.append(_link_dir(src, dst, dry_run))

    # Symlink individual skill directories
    skills_src = plugin_root / "skills"
    if skills_src.is_dir():
        skills_dst = target_dir / "skills"
        if not dry_run:
            skills_dst.mkdir(parents=True, exist_ok=True)

        for skill_name in discover_skills(plugin_root):
            src = skills_src / skill_name
            dst = skills_dst / skill_name
            actions.append(_link_dir(src, dst, dry_run))

    return actions


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Deploy WOS skills via symlinks to a target project or platform.",
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--target",
        help="Target project directory (deploys into <target>/.agents/)",
    )
    group.add_argument(
        "--platform",
        choices=sorted(PLATFORMS.keys()),
        help="Target platform (deploys into ~/.<platform>/)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without writing",
    )
    args = parser.parse_args()

    if args.platform:
        target_dir = resolve_platform_path(args.platform)
        display_name, _ = PLATFORMS[args.platform]
        label = f"{display_name} ({target_dir})"
    else:
        target = Path(args.target).resolve()
        if not target.is_dir():
            print(
                f"Error: target directory does not exist: {target}",
                file=sys.stderr,
            )
            sys.exit(1)
        target_dir = target / ".agents"
        label = str(target_dir)

    actions = deploy(_plugin_root, target_dir, dry_run=args.dry_run)

    if args.dry_run:
        print(f"Dry run: {len(actions)} actions for {label}")
    else:
        print(f"Deployed to {label}")
    for action in actions:
        print(f"  {action}")


if __name__ == "__main__":
    main()
