"""Assumption-to-document matching for the /wos:challenge skill."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Callable, List

from wos.document import Document, parse_document


def discover_related(artifact_path: str, project_root: str) -> List[Document]:
    """Parse an artifact's related frontmatter and return linked documents.

    Resolves each path in the ``related`` field relative to project_root.
    Skips paths that don't exist or fail to parse.

    Args:
        artifact_path: Path to the artifact file.
        project_root: Project root for resolving relative paths.

    Returns:
        List of parsed Document instances for valid related paths.
    """
    if not os.path.isfile(artifact_path):
        return []

    with open(artifact_path, encoding="utf-8") as f:
        text = f.read()

    try:
        doc = parse_document(artifact_path, text)
    except ValueError:
        return []

    if not doc.related:
        return []

    results: List[Document] = []
    root = Path(project_root)
    for rel_path in doc.related:
        full = root / rel_path
        if not full.is_file():
            continue
        try:
            related_doc = parse_document(str(rel_path), full.read_text(encoding="utf-8"))
            results.append(related_doc)
        except ValueError:
            continue

    return results


def keyword_score(assumption: str, text: str) -> float:
    """Score relevance of text to an assumption via keyword overlap.

    Tokenizes both strings, filters tokens under 3 characters, and
    returns the fraction of assumption tokens found in text. Returns 0.0
    if the assumption has no usable tokens.

    This is the default scorer. The interface (assumption, text) -> float
    is swappable for more sophisticated matching later.

    Args:
        assumption: The assumption claim text.
        text: The document text to match against (typically name + description).

    Returns:
        Float between 0.0 and 1.0 inclusive.
    """
    assumption_tokens = [
        t for t in assumption.lower().split() if len(t) >= 3
    ]
    if not assumption_tokens:
        return 0.0
    text_lower = text.lower()
    matched = sum(1 for t in assumption_tokens if t in text_lower)
    return matched / len(assumption_tokens)
