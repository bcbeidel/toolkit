"""AGENTS.md manager — marker-based WOS section rendering and updates.

Renders the WOS-managed section for AGENTS.md (context navigation,
areas table, file metadata format, preferences) and updates the file
content using marker-based replacement.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List, Optional

# ── Markers ──────────────────────────────────────────────────────

BEGIN_MARKER = "<!-- wos:begin -->"
END_MARKER = "<!-- wos:end -->"

_LAYOUT_RE = re.compile(r"<!--\s*wos:layout:\s*(\S+)\s*-->")

VALID_LAYOUTS = frozenset({"separated", "co-located", "flat", "none"})


# ── Discovery ────────────────────────────────────────────────────


def discover_areas(root: Path) -> List[Dict[str, str]]:
    """Discover areas by scanning for directories with managed documents.

    Walks the project tree using the discovery module, finds all
    directories containing managed documents, and returns them as
    navigable areas with ``_index.md`` preambles as descriptions.

    Args:
        root: Project root directory.

    Returns:
        Sorted list of dicts with 'name' and 'path' keys.
    """
    from wos.discovery import discover_document_dirs
    from wos.index import extract_preamble

    doc_dirs = discover_document_dirs(root)
    if not doc_dirs:
        return []

    areas: List[Dict[str, str]] = []
    for directory in doc_dirs:
        index_path = directory / "_index.md"
        preamble = extract_preamble(index_path)
        name = preamble if preamble else directory.name
        try:
            rel_path = str(directory.relative_to(root))
        except ValueError:
            rel_path = str(directory)
        areas.append({"name": name, "path": rel_path})

    return areas


# ── Layout hint ──────────────────────────────────────────────────


def read_layout_hint(content: str) -> Optional[str]:
    """Extract layout pattern from AGENTS.md WOS section.

    Looks for ``<!-- wos:layout: <pattern> -->`` within the WOS-managed
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

    wos_section = content[begin_idx:end_idx]
    match = _LAYOUT_RE.search(wos_section)
    if match:
        layout = match.group(1)
        if layout in VALID_LAYOUTS:
            return layout
    return None


def write_layout_hint(layout: str) -> str:
    """Return the comment marker string for a layout pattern.

    Args:
        layout: One of 'separated', 'co-located', 'flat', 'none'.

    Returns:
        HTML comment string like ``<!-- wos:layout: co-located -->``.
    """
    return f"<!-- wos:layout: {layout} -->"


# ── Render ───────────────────────────────────────────────────────


def render_wos_section(
    areas: List[Dict[str, str]],
    preferences: Optional[List[str]] = None,
    layout: Optional[str] = None,
) -> str:
    """Render the WOS-managed section for AGENTS.md.

    Args:
        areas: List of dicts with 'name' and 'path' keys.
        preferences: Optional list of preference strings.
        layout: Optional layout pattern to include as a hint comment.

    Returns:
        Markdown string wrapped in begin/end markers.
    """
    lines: List[str] = [BEGIN_MARKER]

    # ── Layout hint (if set) ──────────────────────────────────────
    if layout and layout in VALID_LAYOUTS:
        lines.append(write_layout_hint(layout))

    # ── Context Navigation header ────────────────────────────────
    lines.append("## Context Navigation")
    lines.append("")
    lines.append(
        "Each directory has an `_index.md` listing all files with descriptions."
    )

    # Dynamic navigation: list areas with _index.md links
    if areas:
        for area in areas:
            path = area["path"]
            lines.append(f"- `{path}/_index.md` -- {area['name']}")
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

    # ── Areas table ──────────────────────────────────────────────
    if areas:
        lines.append("")
        lines.append("### Areas")
        lines.append("| Area | Path |")
        lines.append("|------|------|")
        for area in areas:
            lines.append(f"| {area['name']} | {area['path']} |")

    # ── File Metadata Format ─────────────────────────────────────
    lines.append("")
    lines.append("### File Metadata Format")
    lines.append("```yaml")
    lines.append("---")
    lines.append("name: Title")
    lines.append("description: What this covers")
    lines.append("metadata:")
    lines.append("  type: research       # optional")
    lines.append("  sources: []          # required if type is research")
    lines.append("  related: []          # optional, file paths from project root")
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

    # ── Preferences ──────────────────────────────────────────────
    if preferences is not None and len(preferences) > 0:
        lines.append("")
        lines.append("### Preferences")
        for pref in preferences:
            lines.append(f"- {pref}")

    lines.append(END_MARKER)
    return "\n".join(lines) + "\n"


# ── Extract ─────────────────────────────────────────────────────


def extract_preferences(content: str) -> List[str]:
    """Extract preference strings from an AGENTS.md WOS section.

    Parses the ``### Preferences`` subsection between WOS markers and
    returns the list of preference strings (without ``- `` bullet prefix).
    Used by reindex and update_preferences to preserve existing preferences.

    Args:
        content: Full AGENTS.md file content.

    Returns:
        List of preference strings, or empty list if none found.
    """
    begin_idx = content.find(BEGIN_MARKER)
    end_idx = content.find(END_MARKER)
    if begin_idx == -1 or end_idx == -1:
        return []

    wos_section = content[begin_idx:end_idx]
    lines = wos_section.split("\n")

    in_preferences = False
    prefs: List[str] = []
    for line in lines:
        if line.strip() == "### Preferences":
            in_preferences = True
            continue
        if in_preferences:
            if line.startswith("### ") or line.startswith("<!--"):
                break
            if line.startswith("- "):
                prefs.append(line[2:])

    return prefs


# ── Update ───────────────────────────────────────────────────────


def update_agents_md(
    content: str,
    areas: List[Dict[str, str]],
    preferences: Optional[List[str]] = None,
    layout: Optional[str] = None,
) -> str:
    """Replace or append the WOS section in AGENTS.md content.

    If markers exist, replaces the content between them (inclusive).
    If markers don't exist, appends the section to the end.
    Content outside markers is never touched.

    Preserves existing layout hint if no new layout is specified.

    Args:
        content: The existing AGENTS.md content.
        areas: List of dicts with 'name' and 'path' keys.
        preferences: Optional list of preference strings.
        layout: Optional layout pattern. If None, preserves existing.

    Returns:
        Updated AGENTS.md content with the new WOS section.
    """
    from wos.markers import replace_marker_section

    # Preserve existing layout if not explicitly provided
    if layout is None:
        layout = read_layout_hint(content)

    section = render_wos_section(areas, preferences, layout=layout)
    return replace_marker_section(content, BEGIN_MARKER, END_MARKER, section)
