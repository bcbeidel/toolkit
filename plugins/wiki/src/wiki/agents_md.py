"""AGENTS.md manager — marker-based managed section rendering and updates.

Renders the managed section for AGENTS.md (context navigation, file
metadata format, document standards) and updates the file content
using marker-based replacement.

Also provides replace_marker_section(), a general utility for replacing
or appending marker-delimited sections in any text file.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List, Optional

# ── Marker utilities ─────────────────────────────────────────────


def replace_marker_section(
    content: str,
    begin_marker: str,
    end_marker: str,
    section: str,
) -> str:
    """Replace or append a marker-delimited section in text content.

    If both markers exist, replaces everything between them (inclusive).
    If markers don't exist, appends the section to the end.

    Args:
        content: The existing file content.
        begin_marker: The opening marker string.
        end_marker: The closing marker string.
        section: The new section content (should include markers if needed).

    Returns:
        Updated content with the new section.
    """
    begin_idx = content.find(begin_marker)
    end_idx = content.find(end_marker)

    if begin_idx != -1 and end_idx != -1:
        end_idx += len(end_marker)
        # Consume trailing newline if present
        if end_idx < len(content) and content[end_idx] == "\n":
            end_idx += 1
        return content[:begin_idx] + section + content[end_idx:]

    # Append
    return content.rstrip("\n") + "\n\n" + section


BEGIN_MARKER = "<!-- wiki:begin -->"
END_MARKER = "<!-- wiki:end -->"

_LAYOUT_RE = re.compile(r"<!--\s*wiki:layout:\s*(\S+)\s*-->")

VALID_LAYOUTS = frozenset({"separated", "co-located", "flat", "none"})

# Legacy markers from the `wos:` naming era. ``update_agents_md`` rewrites
# any occurrence in place so repeat runs of /wiki:setup heal old installs.
_LEGACY_BEGIN_MARKER = "<!-- wos:begin -->"
_LEGACY_END_MARKER = "<!-- wos:end -->"
_LEGACY_LAYOUT_RE = re.compile(r"<!--\s*wos:layout:\s*(\S+)\s*-->")


def _migrate_legacy_markers(content: str) -> str:
    """Rewrite pre-rename ``wos:`` markers to their ``wiki:`` equivalents.

    Idempotent — returns content unchanged when no legacy markers are present.
    """
    if (
        _LEGACY_BEGIN_MARKER not in content
        and _LEGACY_END_MARKER not in content
        and not _LEGACY_LAYOUT_RE.search(content)
    ):
        return content
    content = content.replace(_LEGACY_BEGIN_MARKER, BEGIN_MARKER)
    content = content.replace(_LEGACY_END_MARKER, END_MARKER)
    content = _LEGACY_LAYOUT_RE.sub(
        lambda m: f"<!-- wiki:layout: {m.group(1)} -->", content
    )
    return content


# ── Discovery ────────────────────────────────────────────────────


def discover_areas(root: Path) -> List[Dict[str, str]]:
    """Discover areas by scanning for directories with managed documents.

    Walks the project tree and finds all directories containing non-index
    .md files. Returns them as navigable areas.

    Args:
        root: Project root directory.

    Returns:
        Sorted list of dicts with 'name' and 'path' keys.
    """
    import os

    _SKIP = frozenset({
        "node_modules", "__pycache__", "venv", ".venv",
        "dist", "build", ".tox", ".mypy_cache", ".pytest_cache",
    })
    areas = []
    seen: set[str] = set()
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(
            d for d in dirnames
            if not d.startswith(".") and d not in _SKIP
        )
        if any(f.endswith(".md") and f != "_index.md" for f in filenames):
            try:
                rel = str(Path(dirpath).relative_to(root))
            except ValueError:
                rel = dirpath
            if rel and rel not in seen:
                seen.add(rel)
                areas.append({"name": rel, "path": rel})
    return areas


# ── Layout hint ──────────────────────────────────────────────────


def read_layout_hint(content: str) -> Optional[str]:
    """Extract layout pattern from AGENTS.md managed section.

    Looks for ``<!-- wiki:layout: <pattern> -->`` within the managed
    section.

    Args:
        content: Full AGENTS.md file content.

    Returns:
        Layout pattern string (e.g. 'separated', 'co-located'), or
        None if no hint found.
    """
    begin_idx = content.find(BEGIN_MARKER)
    end_idx = content.find(END_MARKER)
    if begin_idx == -1 or end_idx == -1:
        return None

    section = content[begin_idx:end_idx]
    match = _LAYOUT_RE.search(section)
    if match:
        layout = match.group(1)
        if layout in VALID_LAYOUTS:
            return layout
    return None


# ── Render ───────────────────────────────────────────────────────


def render_wiki_section(
    areas: List[Dict[str, str]],
    layout: Optional[str] = None,
) -> str:
    """Render the managed section for AGENTS.md.

    Args:
        areas: List of dicts with 'name' and 'path' keys.
        layout: Optional layout pattern to include as a hint comment.

    Returns:
        Markdown string wrapped in begin/end markers.
    """
    lines: List[str] = [BEGIN_MARKER]

    # ── Layout hint (if set) ──────────────────────────────────────
    if layout and layout in VALID_LAYOUTS:
        lines.append(f"<!-- wiki:layout: {layout} -->")

    # ── Context Navigation header ────────────────────────────────
    lines.append("## Context Navigation")
    lines.append("")
    lines.append(
        "Directory-level routing lives in [RESOLVER.md](RESOLVER.md). "
        "Consult it before filing or loading context."
    )
    lines.append(
        "Find files in registered directories via Glob on the directory's "
        "naming pattern; read frontmatter `description` to identify the right file."
    )
    lines.append("")

    lines.append(
        "Each `.md` file starts with YAML metadata (between `---` lines)."
    )
    lines.append(
        "Read the `description` field before reading the full file."
    )
    lines.append(
        "Documents put key insights first and last; supplemental detail in the middle."
    )

    # ── File Metadata Format ─────────────────────────────────────
    lines.append("")
    lines.append("### File Metadata Format")
    lines.append("```yaml")
    lines.append("---")
    lines.append("name: Title")
    lines.append("description: What this covers")
    lines.append("type: research       # optional")
    lines.append("sources: []          # required if type is research")
    lines.append("related: []          # optional, file paths from project root")
    lines.append("---")
    lines.append("```")

    # ── Document Standards ────────────────────────────────────────
    lines.append("")
    lines.append("### Document Standards")
    lines.append("")
    lines.append(
        "**Structure:** Key insights first, detailed explanation "
        "in the middle, takeaways at the bottom."
    )
    lines.append(
        "LLMs lose attention mid-document — first and last sections "
        "are what agents retain."
    )
    lines.append("")
    lines.append("**Conventions:**")
    lines.append("- Context files target 200-800 words. Over 800, consider splitting.")
    lines.append(
        "- One concept per file. Multiple distinct topics should be separate files."
    )
    lines.append(
        "- Link bidirectionally — if A references B in `related`, B should reference A."
    )

    lines.append(END_MARKER)
    return "\n".join(lines) + "\n"


# ── Extract areas ────────────────────────────────────────────────


def extract_areas(content: str) -> List[Dict[str, str]]:
    """Extract area entries from an AGENTS.md managed section.

    Parses the ``### Areas`` table between managed markers and returns the
    list of area dicts with 'name' and 'path' keys.  Used to preserve
    human-written area descriptions when rewriting the managed section.

    Args:
        content: Full AGENTS.md file content.

    Returns:
        List of ``{"name": ..., "path": ...}`` dicts, or empty list if
        no markers or no Areas table is found.
    """
    begin_idx = content.find(BEGIN_MARKER)
    end_idx = content.find(END_MARKER)
    if begin_idx == -1 or end_idx == -1:
        return []

    section = content[begin_idx:end_idx]
    lines = section.split("\n")

    in_areas = False
    areas: List[Dict[str, str]] = []
    for line in lines:
        if line.strip() == "### Areas":
            in_areas = True
            continue
        if in_areas:
            if line.startswith("### ") or line.startswith("<!--"):
                break
            # Skip header and separator rows
            if line.startswith("| Area") or line.startswith("|---"):
                continue
            if line.startswith("| "):
                parts = [p.strip() for p in line.strip("|").split("|")]
                if len(parts) >= 2:
                    areas.append({"name": parts[0], "path": parts[1]})

    return areas


# ── Working Agreements detection ─────────────────────────────────


def has_working_agreements(content: str) -> bool:
    """Return True if content contains a ``## Working Agreements`` heading.

    Case-insensitive; trailing whitespace ignored. Does not match
    substrings such as ``## My Working Agreements Notes``. Used by
    ``/wiki:setup`` to keep the Working Agreements capture step
    idempotent — re-running against a project that already has the
    section must be a no-op.
    """
    for line in content.splitlines():
        if line.rstrip().lower() == "## working agreements":
            return True
    return False


# ── Update ───────────────────────────────────────────────────────


def update_agents_md(
    content: str,
    areas: Optional[List[Dict[str, str]]] = None,
    layout: Optional[str] = None,
) -> str:
    """Replace or append the managed section in AGENTS.md content.

    If markers exist, replaces the content between them (inclusive).
    If markers don't exist, appends the section to the end.
    Content outside markers is never touched.

    Preserves existing layout hint if no new layout is specified.
    When ``areas`` is None, extracts existing areas from the current
    content so human-written descriptions are not lost.

    Args:
        content: The existing AGENTS.md content.
        areas: List of dicts with 'name' and 'path' keys.  If None,
            the existing areas table is preserved via ``extract_areas``.
        layout: Optional layout pattern. If None, preserves existing.

    Returns:
        Updated AGENTS.md content with the new managed section.
    """
    # Migrate legacy wos: markers before anything else so downstream
    # extraction and replacement see the canonical wiki: form.
    content = _migrate_legacy_markers(content)

    # Preserve existing areas if not explicitly provided
    if areas is None:
        areas = extract_areas(content)

    # Preserve existing layout if not explicitly provided
    if layout is None:
        layout = read_layout_hint(content)

    section = render_wiki_section(areas, layout=layout)
    return replace_marker_section(content, BEGIN_MARKER, END_MARKER, section)
