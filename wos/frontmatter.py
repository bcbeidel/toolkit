"""Custom frontmatter parser for WOS documents.

Parses the restricted YAML subset used in WOS frontmatter:
- key: value (scalars, always strings, no type coercion)
- key: (null)
- list items under a key (- item)

No nested dicts, no booleans, no numbers, no dates.
"""

from __future__ import annotations

from typing import Dict, List, Optional, Tuple, Union


def parse_frontmatter(text: str) -> Tuple[Dict[str, Union[str, List[str], None]], str]:
    """Parse YAML frontmatter from markdown text.

    Args:
        text: Raw markdown text, expected to start with '---'.

    Returns:
        Tuple of (frontmatter_dict, body_content).

    Raises:
        ValueError: If frontmatter delimiters are missing or malformed.
    """
    if not text.startswith("---\n"):
        raise ValueError("No YAML frontmatter found (file must start with '---')")

    # Find closing delimiter
    close_idx = text.find("\n---\n", 3)
    if close_idx != -1:
        yaml_region = text[4:close_idx]
        body = text[close_idx + 5:]
    else:
        close_idx = text.find("\n---", 3)
        if close_idx != -1 and close_idx + 4 >= len(text):
            yaml_region = text[4:close_idx]
            body = ""
        else:
            raise ValueError("No closing frontmatter delimiter found")

    fm = _parse_yaml_subset(yaml_region)
    return fm, body


def _parse_yaml_subset(
    yaml_text: str,
) -> Dict[str, Union[str, List[str], None]]:
    """Parse the restricted YAML subset used in frontmatter.

    Handles:
    - key: value -> {"key": "value"} (string, no type coercion)
    - key: -> {"key": None}
    - - item lines after a key -> {"key": ["item1", "item2"]}
    - key: > (or |, >-, |-) -> block scalar, indented lines joined with spaces
    """
    result: Dict[str, Union[str, List[str], None]] = {}
    current_key: Optional[str] = None
    collecting_block: bool = False
    block_parts: List[str] = []

    for line in yaml_text.split("\n"):
        if collecting_block:
            if line and not line[0].isspace():
                # End of block scalar — flush accumulated lines
                result[current_key] = " ".join(block_parts)
                collecting_block = False
                block_parts = []
                current_key = None
                # Fall through to parse this line as a new key-value
            else:
                stripped = line.strip()
                if stripped:
                    block_parts.append(stripped)
                # Skip blank lines inside block scalar
                continue

        stripped = line.strip()

        # Skip blank lines and comments
        if not stripped or stripped.startswith("#"):
            continue

        # List item: "- value" or "  - value"
        if stripped.startswith("- "):
            if current_key is not None:
                item_value = stripped[2:].strip()
                if current_key not in result or result[current_key] is None:
                    result[current_key] = []
                existing = result[current_key]
                if isinstance(existing, list):
                    existing.append(item_value)
            continue

        # Key-value pair: "key: value" or "key:"
        colon_idx = stripped.find(":")
        if colon_idx == -1:
            continue

        key = stripped[:colon_idx].strip()
        raw_value = stripped[colon_idx + 1:]

        value_stripped = raw_value.strip()
        if value_stripped == "[]":
            result[key] = []
            current_key = None
        elif value_stripped in (">", "|", ">-", "|-"):
            # Block scalar — collect indented lines that follow
            result[key] = None
            current_key = key
            collecting_block = True
            block_parts = []
        elif value_stripped:
            result[key] = value_stripped
            current_key = None
        else:
            result[key] = None
            current_key = key

    # Flush any pending block scalar at end of input
    if collecting_block and current_key is not None:
        result[current_key] = " ".join(block_parts)

    return result
