"""Shared marker-based section replacement for managed file sections.

Provides a single function for replacing content between marker comments
in text files. Used by agents_md.py.
"""

from __future__ import annotations


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
