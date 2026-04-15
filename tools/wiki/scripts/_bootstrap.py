"""Bootstrap helper: insert the plugin root into sys.path.

Import as a side effect before importing from wiki or check:

    import _bootstrap  # noqa: F401

When run as ``python tools/wiki/scripts/<name>.py``, Python adds
``tools/wiki/scripts/`` to sys.path[0], so ``import _bootstrap`` finds
this file. It resolves the plugin root and inserts it so that editable
installs of ``wiki`` and ``check`` are importable.

The resolved root is also exposed as ``plugin_root`` for scripts that
need a reference to it at runtime.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

_env_root = os.environ.get("CLAUDE_PLUGIN_ROOT", "")
# tools/wiki/scripts/ → tools/wiki/ (plugin root)
plugin_root: Path = (
    Path(_env_root) if _env_root and os.path.isdir(_env_root)
    else Path(__file__).resolve().parent.parent
)
if str(plugin_root) not in sys.path:
    sys.path.insert(0, str(plugin_root))
