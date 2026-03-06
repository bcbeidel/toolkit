"""Skill size auditing — measure instruction density of skill files.

Provides functions to strip frontmatter, count instruction lines, and
check skill directories for size thresholds.
"""

from __future__ import annotations


def strip_frontmatter(text: str) -> str:
    """Remove YAML frontmatter (--- delimited) from text.

    If text starts with ``---``, finds the next ``---`` after position 3
    and returns everything after it.  If no closing delimiter is found,
    returns the text unchanged.
    """
    if not text.startswith("---"):
        return text
    close = text.find("---", 3)
    if close == -1:
        return text
    # Skip past the closing --- and the newline that follows it
    after = close + 3
    if after < len(text) and text[after] == "\n":
        after += 1
    return text[after:]
