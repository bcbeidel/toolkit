"""Pytest configuration: ensure plugins/wiki/ is on sys.path for script imports."""
from __future__ import annotations

import sys
from pathlib import Path

# plugins/wiki/ must be on sys.path so `from scripts.lint import main` works
# in test_lint.py (namespace package import against the scripts/ directory).
_wiki_root = str(Path(__file__).parent.parent)
if _wiki_root not in sys.path:
    sys.path.insert(0, _wiki_root)

# Also add plugins/wiki/scripts/ so `import _bootstrap` works in subprocesses.
_scripts_dir = str(Path(__file__).parent.parent / "scripts")
if _scripts_dir not in sys.path:
    sys.path.insert(0, _scripts_dir)
