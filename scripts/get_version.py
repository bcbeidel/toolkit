#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""Print the WOS plugin version.

Usage:
    uv run scripts/get_version.py
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
        description="Print the WOS plugin version from plugin.json.",
    )
    parser.parse_args()

    plugin_json = _plugin_root / ".claude-plugin" / "plugin.json"
    if not plugin_json.exists():
        print("plugin.json not found", file=sys.stderr)
        sys.exit(1)

    with open(plugin_json) as f:
        data = json.load(f)
    print(data["version"])


if __name__ == "__main__":
    main()
