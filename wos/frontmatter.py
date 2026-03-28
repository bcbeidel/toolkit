"""Custom frontmatter parser for WOS documents.

Parses the restricted YAML subset used in WOS frontmatter:
- key: value (scalars, always strings, no type coercion)
- key: (null)
- list items under a key (- item)
- one level of nested dicts (indented key-value pairs under a null-valued key)

No booleans, no numbers, no dates. Nesting limited to one level.
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
) -> Dict[str, Union[str, List[str], Dict[str, Union[str, List[str], None]], None]]:
    """Parse the restricted YAML subset used in frontmatter.

    Handles:
    - key: value -> {"key": "value"} (string, no type coercion)
    - key: -> {"key": None}
    - - item lines after a key -> {"key": ["item1", "item2"]}
    - indented key-value pairs under a null key -> {"key": {"nested": "value"}}
      (one level of nesting only)
    """
    _NestedVal = Union[str, List[str], None]
    _Val = Union[str, List[str], Dict[str, _NestedVal], None]
    result: Dict[str, _Val] = {}
    current_key: Optional[str] = None
    # Nested dict state (one level only)
    nested_key: Optional[str] = None
    nested_dict: Optional[Dict[str, Union[str, List[str], None]]] = None
    nested_current_key: Optional[str] = None

    def _flush_nested() -> None:
        """Write any in-progress nested dict to result."""
        nonlocal nested_key, nested_dict, nested_current_key
        if nested_key is not None and nested_dict is not None:
            result[nested_key] = nested_dict
        nested_key = None
        nested_dict = None
        nested_current_key = None

    for line in yaml_text.split("\n"):
        stripped = line.strip()

        # Skip blank lines and comments
        if not stripped or stripped.startswith("#"):
            continue

        indent = len(line) - len(line.lstrip())

        # ── Inside a nested dict: indented lines belong to it ─────
        if nested_key is not None:
            if indent > 0:
                if stripped.startswith("- "):
                    if nested_current_key is not None and nested_dict is not None:
                        item_value = stripped[2:].strip()
                        if nested_dict.get(nested_current_key) is None:
                            nested_dict[nested_current_key] = []
                        existing = nested_dict[nested_current_key]
                        if isinstance(existing, list):
                            existing.append(item_value)
                    continue
                colon_idx = stripped.find(":")
                if colon_idx != -1 and nested_dict is not None:
                    key = stripped[:colon_idx].strip()
                    raw_value = stripped[colon_idx + 1:]
                    if raw_value.strip():
                        nested_dict[key] = raw_value.strip()
                        nested_current_key = None
                    else:
                        nested_dict[key] = None
                        nested_current_key = key
                continue
            # Non-indented line: exit nested dict, fall through
            _flush_nested()

        # ── Indented line after a null-valued key ─────────────────
        if current_key is not None and indent > 0:
            if stripped.startswith("- "):
                # List item (existing behavior)
                item_value = stripped[2:].strip()
                if current_key not in result or result[current_key] is None:
                    result[current_key] = []
                existing = result[current_key]
                if isinstance(existing, list):
                    existing.append(item_value)
                continue
            # Indented key-value pair: start nested dict
            colon_idx = stripped.find(":")
            if colon_idx != -1:
                nested_key = current_key
                nested_dict = {}
                nested_current_key = None
                current_key = None
                # Remove placeholder None
                if nested_key in result and result[nested_key] is None:
                    del result[nested_key]
                key = stripped[:colon_idx].strip()
                raw_value = stripped[colon_idx + 1:]
                if raw_value.strip():
                    nested_dict[key] = raw_value.strip()
                else:
                    nested_dict[key] = None
                    nested_current_key = key
                continue

        # ── Top-level list item ───────────────────────────────────
        if stripped.startswith("- "):
            if current_key is not None:
                item_value = stripped[2:].strip()
                if current_key not in result or result[current_key] is None:
                    result[current_key] = []
                existing = result[current_key]
                if isinstance(existing, list):
                    existing.append(item_value)
            continue

        # ── Top-level key-value pair ──────────────────────────────
        colon_idx = stripped.find(":")
        if colon_idx == -1:
            continue

        key = stripped[:colon_idx].strip()
        raw_value = stripped[colon_idx + 1:]

        if raw_value.strip():
            result[key] = raw_value.strip()
            current_key = None
        else:
            result[key] = None
            current_key = key

    _flush_nested()

    return result
