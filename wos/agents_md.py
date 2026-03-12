"""AGENTS.md manager — marker-based WOS section rendering and updates.

Renders the WOS-managed section for AGENTS.md (context navigation,
areas table, file metadata format, preferences) and updates the file
content using marker-based replacement.
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional

# ── Markers ──────────────────────────────────────────────────────

BEGIN_MARKER = "<!-- wos:begin -->"
END_MARKER = "<!-- wos:end -->"


# ── Discovery ────────────────────────────────────────────────────


def discover_areas(root: Path) -> List[Dict[str, str]]:
    """Discover areas by scanning docs/context/ subdirectories.

    Walks ``docs/context/`` under *root*, reads each subdirectory's
    ``_index.md`` preamble as the area description, and returns a
    sorted list of area dicts suitable for ``render_wos_section()``.

    Args:
        root: Project root directory.

    Returns:
        Sorted list of dicts with 'name' and 'path' keys.
    """
    from wos.index import extract_preamble

    context_dir = root / "docs" / "context"
    if not context_dir.is_dir():
        return []

    areas: List[Dict[str, str]] = []
    for entry in sorted(context_dir.iterdir()):
        if not entry.is_dir():
            continue
        index_path = entry / "_index.md"
        preamble = extract_preamble(index_path)
        name = preamble if preamble else entry.name
        rel_path = str(entry.relative_to(root))
        areas.append({"name": name, "path": rel_path})

    return areas


# ── Render ───────────────────────────────────────────────────────


def render_wos_section(
    areas: List[Dict[str, str]],
    preferences: Optional[List[str]] = None,
) -> str:
    """Render the WOS-managed section for AGENTS.md.

    Args:
        areas: List of dicts with 'name' and 'path' keys.
        preferences: Optional list of preference strings.

    Returns:
        Markdown string wrapped in begin/end markers.
    """
    lines: List[str] = [BEGIN_MARKER]

    # ── Context Navigation header ────────────────────────────────
    lines.append("## Context Navigation")
    lines.append("")
    lines.append(
        "Each directory has an `_index.md` listing all files with descriptions."
    )
    lines.append("- `docs/context/_index.md` -- all topic areas")
    lines.append("- `docs/plans/_index.md` -- plans")
    lines.append("- `docs/designs/_index.md` -- designs")
    lines.append("- `docs/research/_index.md` -- research")
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
) -> str:
    """Replace or append the WOS section in AGENTS.md content.

    If markers exist, replaces the content between them (inclusive).
    If markers don't exist, appends the section to the end.
    Content outside markers is never touched.

    Args:
        content: The existing AGENTS.md content.
        areas: List of dicts with 'name' and 'path' keys.
        preferences: Optional list of preference strings.

    Returns:
        Updated AGENTS.md content with the new WOS section.
    """
    from wos.markers import replace_marker_section

    section = render_wos_section(areas, preferences)
    return replace_marker_section(content, BEGIN_MARKER, END_MARKER, section)
