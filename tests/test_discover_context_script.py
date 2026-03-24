"""Tests for scripts/discover_context.py CLI."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

_CONTEXT_DOC = """\
---
name: Auth Patterns
description: OAuth authentication patterns for the project
---

## OAuth

We use OAuth 2.0.
"""

_ARTIFACT_DOC = """\
---
name: Design Spec
description: A design document
related:
  - docs/context/auth.md
---

## Design

Uses OAuth.
"""


def test_discover_context_json_output(tmp_path):
    """Script outputs valid JSON with assumption-to-match mapping."""
    ctx = tmp_path / "docs" / "context"
    ctx.mkdir(parents=True)
    (ctx / "auth.md").write_text(_CONTEXT_DOC)

    script = Path(__file__).resolve().parent.parent / "scripts" / "discover_context.py"
    result = subprocess.run(
        [
            sys.executable, str(script),
            "--assumptions", "OAuth authentication",
            "--root", str(tmp_path),
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    data = json.loads(result.stdout)
    assert len(data) == 1
    assert data[0]["assumption"] == "OAuth authentication"
    assert len(data[0]["matches"]) > 0
    assert "score" in data[0]["matches"][0]
    assert "path" in data[0]["matches"][0]
    assert "name" in data[0]["matches"][0]


def test_discover_context_with_artifact(tmp_path):
    """--artifact flag includes explicit layer results."""
    ctx = tmp_path / "docs" / "context"
    ctx.mkdir(parents=True)
    (ctx / "auth.md").write_text(_CONTEXT_DOC)

    artifact = tmp_path / "design.md"
    artifact.write_text(_ARTIFACT_DOC)

    script = Path(__file__).resolve().parent.parent / "scripts" / "discover_context.py"
    result = subprocess.run(
        [
            sys.executable, str(script),
            "--assumptions", "OAuth authentication",
            "--root", str(tmp_path),
            "--artifact", str(artifact),
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    data = json.loads(result.stdout)
    assert len(data) == 1
    # Should have matches from both explicit (related) and broad layers
    assert len(data[0]["matches"]) > 0


def test_discover_context_no_matches(tmp_path):
    """Assumptions with no matches return empty match lists."""
    # Empty docs directory
    (tmp_path / "docs" / "context").mkdir(parents=True)

    script = Path(__file__).resolve().parent.parent / "scripts" / "discover_context.py"
    result = subprocess.run(
        [
            sys.executable, str(script),
            "--assumptions", "Quantum entanglement",
            "--root", str(tmp_path),
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    data = json.loads(result.stdout)
    assert data[0]["matches"] == []
