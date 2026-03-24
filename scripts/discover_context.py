#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""Discover context and research documents relevant to a set of assumptions.

Outputs JSON mapping each assumption to ranked document matches.
Used by the /wos:challenge skill during Phase 2 (Layered Search).
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
# scripts/ -> plugin root
_plugin_root = (
    Path(_env_root) if _env_root and os.path.isdir(_env_root)
    else Path(__file__).resolve().parent.parent
)
if str(_plugin_root) not in sys.path:
    sys.path.insert(0, str(_plugin_root))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Discover documents relevant to assumptions."
    )
    parser.add_argument(
        "--assumptions",
        nargs="+",
        required=True,
        help="One or more assumption claim strings.",
    )
    parser.add_argument(
        "--root",
        default=".",
        help="Project root directory (default: cwd).",
    )
    parser.add_argument(
        "--artifact",
        default=None,
        help="Path to an artifact file for explicit-layer search.",
    )
    args = parser.parse_args()

    from wos.challenge.discover import (
        discover_by_relevance,
        discover_related,
        keyword_score,
    )

    root = str(Path(args.root).resolve())

    # Broad layer: scan all docs
    broad = discover_by_relevance(args.assumptions, root)

    # Explicit layer: if artifact provided, get related docs
    related_docs = []
    if args.artifact:
        related_docs = discover_related(args.artifact, root)

    # Build output
    output = []
    for assumption in args.assumptions:
        # Merge explicit + broad, dedup by path, explicit first
        seen_paths: set = set()
        matches = []

        # Explicit layer matches: score each related doc against assumption
        for doc in related_docs:
            text = f"{doc.name} {doc.description}"
            score = keyword_score(assumption, text)
            if doc.path not in seen_paths:
                seen_paths.add(doc.path)
                matches.append({
                    "path": doc.path,
                    "name": doc.name,
                    "description": doc.description,
                    "score": round(score, 3),
                    "layer": "explicit",
                })

        # Broad layer matches
        for doc in broad.get(assumption, []):
            if doc.path not in seen_paths:
                seen_paths.add(doc.path)
                text = f"{doc.name} {doc.description}"
                score = keyword_score(assumption, text)
                matches.append({
                    "path": doc.path,
                    "name": doc.name,
                    "description": doc.description,
                    "score": round(score, 3),
                    "layer": "broad",
                })

        # Sort by score descending
        matches.sort(key=lambda m: m["score"], reverse=True)
        output.append({"assumption": assumption, "matches": matches})

    json.dump(output, sys.stdout, indent=2)
    print()  # trailing newline


if __name__ == "__main__":
    main()
