#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""One-off migration: add wiki schema fields to docs/context/*.context.md files.

Adds confidence, created, updated, and updates type for each context file.

Usage:
    python scripts/migrate_context.py [--root PATH] [--dry-run]
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path
from typing import Optional

# ── Plugin root discovery ──────────────────────────────────────────────────────
# Prefer CLAUDE_PLUGIN_ROOT env var (forward-compatible with Claude Code),
# fall back to __file__ parent chain: scripts/ → plugin root
_plugin_root = os.environ.get("CLAUDE_PLUGIN_ROOT")
if _plugin_root:
    sys.path.insert(0, _plugin_root)
else:
    sys.path.insert(0, str(Path(__file__).parent.parent))  # scripts/ → plugin root

from wos.frontmatter import parse_frontmatter  # noqa: E402

# ── Constants ──────────────────────────────────────────────────────────────────

COMPARISON_KEYWORDS = [
    "vs-", "-vs-", "tradeoff", "tradeoffs", "comparison", "versus",
]

ENTITY_FILES = {
    "dbt-layered-architecture-and-testing-patterns.context.md",
    "dbt-three-layer-transformation-model.context.md",
}

FALLBACK_DATE = "2026-04-07"

# Field order for rewritten frontmatter (known fields in desired output order)
_FIELD_ORDER = [
    "name", "description", "type", "confidence", "created", "updated",
    "sources", "related", "status",
]


# ── Helpers ────────────────────────────────────────────────────────────────────


def count_sources(fm: dict) -> int:
    """Return count of non-empty string sources in frontmatter."""
    sources = fm.get("sources") or []
    if not isinstance(sources, list):
        return 0
    return sum(1 for s in sources if isinstance(s, str) and s.strip())


def derive_confidence(n_sources: int) -> str:
    if n_sources >= 3:
        return "high"
    if n_sources >= 1:
        return "medium"
    return "low"


def git_dates(filepath: Path) -> tuple[str, str]:
    """Return (created, updated) ISO dates from git log.

    created = date of first (oldest) commit touching the file
    updated = date of last (newest) commit touching the file
    Falls back to FALLBACK_DATE if git log returns nothing.
    """
    try:
        result = subprocess.run(
            ["git", "log", "--follow", "--format=%as", "--", str(filepath)],
            capture_output=True,
            text=True,
            timeout=10,
        )
        lines = [ln.strip() for ln in result.stdout.splitlines() if ln.strip()]
    except Exception:
        lines = []

    if not lines:
        return FALLBACK_DATE, FALLBACK_DATE

    updated = lines[0]   # newest commit is first
    created = lines[-1]  # oldest commit is last
    return created, updated


def infer_type(filename: str, current_type: Optional[str]) -> str:
    """Return wiki page type. Only updates if current_type is 'context'."""
    if current_type != "context":
        return current_type or "concept"

    if filename in ENTITY_FILES:
        return "entity"
    if any(kw in filename for kw in COMPARISON_KEYWORDS):
        return "comparison"
    return "concept"


def render_frontmatter(fm: dict) -> str:
    """Render frontmatter dict back to YAML string (between --- delimiters).

    Uses a simple string-based approach to avoid adding a YAML dependency.
    Preserves field order per _FIELD_ORDER; extra fields appended at end.
    """
    lines = ["---"]

    def emit(key: str, value: object) -> None:
        if value is None:
            return
        if isinstance(value, list):
            if not value:
                lines.append(f"{key}: []")
            else:
                lines.append(f"{key}:")
                for item in value:
                    item_str = str(item)
                    lines.append(f"  - {item_str}")
        elif isinstance(value, str):
            # parse_frontmatter preserves YAML quotes as part of the string value.
            # If already quoted, emit as-is to avoid double-quoting.
            is_quoted = (
                (value.startswith('"') and value.endswith('"') and len(value) >= 2)
                or (value.startswith("'") and value.endswith("'") and len(value) >= 2)
            )
            if is_quoted:
                lines.append(f"{key}: {value}")
            else:
                # Quote if value contains YAML-special chars or reserved words
                needs_quote = (
                    any(c in value for c in (':', '#', '[', ']', '{', '}', ',', '`'))
                    or value in ("true", "false", "null", "yes", "no")
                    or value.startswith(("- ", "* "))
                )
                if needs_quote:
                    escaped = value.replace('"', '\\"')
                    lines.append(f'{key}: "{escaped}"')
                else:
                    lines.append(f"{key}: {value}")
        else:
            lines.append(f"{key}: {value}")

    # Emit in canonical field order
    seen = set()
    for field in _FIELD_ORDER:
        if field in fm:
            emit(field, fm[field])
            seen.add(field)

    # Emit any remaining fields not in canonical order
    for key, value in fm.items():
        if key not in seen:
            emit(key, value)

    lines.append("---")
    return "\n".join(lines)


def migrate_file(filepath: Path, dry_run: bool = False) -> dict:
    """Migrate a single context file. Returns a summary dict."""
    text = filepath.read_text(encoding="utf-8")

    try:
        fm, body = parse_frontmatter(text)
    except ValueError as exc:
        return {"file": filepath.name, "status": "error", "reason": str(exc)}

    n_sources = count_sources(fm)
    confidence = derive_confidence(n_sources)
    created, updated = git_dates(filepath)
    new_type = infer_type(filepath.name, fm.get("type"))

    # Apply changes
    fm["confidence"] = confidence
    fm["created"] = created
    fm["updated"] = updated
    fm["type"] = new_type

    summary = {
        "file": filepath.name,
        "status": "dry-run" if dry_run else "ok",
        "type": new_type,
        "confidence": confidence,
        "created": created,
        "updated": updated,
        "sources": n_sources,
    }

    if dry_run:
        print(render_frontmatter(fm), file=sys.stderr)
        return summary

    new_text = render_frontmatter(fm) + "\n" + body.lstrip("\n")
    filepath.write_text(new_text, encoding="utf-8")
    return summary


# ── Entry point ────────────────────────────────────────────────────────────────


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Migrate docs/context/*.context.md files to wiki schema."
    )
    parser.add_argument("--root", default=".", help="Project root (default: CWD)")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print would-be frontmatter without writing files.",
    )
    parser.add_argument(
        "--file",
        help="Migrate a single file instead of all context files.",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    context_dir = root / "docs" / "context"

    if not context_dir.is_dir():
        print(f"ERROR: {context_dir} does not exist", file=sys.stderr)
        sys.exit(1)

    if args.file:
        files = [Path(args.file).resolve()]
    else:
        files = sorted(context_dir.glob("*.context.md"))

    errors = []
    by_type: dict[str, int] = {}
    by_conf: dict[str, int] = {}

    for filepath in files:
        result = migrate_file(filepath, dry_run=args.dry_run)
        label = result.get("type", "?")
        conf = result.get("confidence", "?")
        status = result.get("status", "?")
        by_type[label] = by_type.get(label, 0) + 1
        by_conf[conf] = by_conf.get(conf, 0) + 1
        print(
            f"[{label:<12}] [{conf:<6}] {result['file']}",
            file=sys.stderr,
        )
        if status == "error":
            errors.append(result)

    print(f"\n--- Summary ({len(files)} files) ---", file=sys.stderr)
    print(f"Types:      {dict(sorted(by_type.items()))}", file=sys.stderr)
    print(f"Confidence: {dict(sorted(by_conf.items()))}", file=sys.stderr)
    if errors:
        print(f"\nERRORS ({len(errors)}):", file=sys.stderr)
        for e in errors:
            print(f"  {e['file']}: {e['reason']}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
