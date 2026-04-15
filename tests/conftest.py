"""Pytest configuration: ensure scripts/ is importable for test_deploy.py."""
from __future__ import annotations

import sys
from pathlib import Path

# scripts/ must be on sys.path so `import _bootstrap` works when
# test modules import from scripts.* as packages.
_scripts_dir = str(Path(__file__).parent.parent / "scripts")
if _scripts_dir not in sys.path:
    sys.path.insert(0, _scripts_dir)
