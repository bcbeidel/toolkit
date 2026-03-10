"""Research document structural assessment.

Reports observable facts about research documents — word count, draft
markers, section presence, source listing. The model infers phase and
next actions from these facts.
"""

from __future__ import annotations

import os
from typing import Dict, List, Tuple

from wos.document import parse_document


def assess_file(path: str) -> dict:
    """Assess structural facts of a single research document.

    Args:
        path: Absolute or relative path to a markdown file.

    Returns:
        Dict with keys: file, exists, frontmatter, content, sources.
        If the file doesn't exist, frontmatter/content/sources are None.
    """
    if not os.path.isfile(path):
        return {
            "file": path,
            "exists": False,
            "frontmatter": None,
            "content": None,
            "sources": None,
        }

    text = _read_file(path)
    doc = parse_document(path, text)

    urls, non_url_count = _classify_sources(doc.sources)
    sections = _detect_sections(doc.content)
    word_count = len(doc.content.split())

    return {
        "file": path,
        "exists": True,
        "frontmatter": {
            "name": doc.name,
            "description": doc.description,
            "type": doc.type,
            "sources_count": len(doc.sources),
            "related_count": len(doc.related),
        },
        "content": {
            "word_count": word_count,
            "draft_marker_present": "<!-- DRAFT -->" in doc.content,
            "has_sections": sections,
        },
        "sources": {
            "total": len(doc.sources),
            "urls": urls,
            "non_url_count": non_url_count,
        },
    }


def scan_directory(root: str, subdir: str = "docs/research") -> dict:
    """Scan a directory for research documents and return summaries.

    Args:
        root: Project root directory.
        subdir: Subdirectory relative to root to scan (default: docs/research).

    Returns:
        Dict with keys: directory, documents. Each document has:
        file, name, draft_marker_present, word_count, sources_count.
    """
    scan_path = os.path.join(root, subdir)

    if not os.path.isdir(scan_path):
        return {"directory": scan_path, "documents": []}

    documents: list = []
    for filename in sorted(os.listdir(scan_path)):
        if not filename.endswith(".md") or filename.startswith("_"):
            continue

        file_path = os.path.join(scan_path, filename)
        if not os.path.isfile(file_path):
            continue

        try:
            text = _read_file(file_path)
            doc = parse_document(file_path, text)
        except ValueError:
            continue

        if doc.type != "research":
            continue

        documents.append({
            "file": file_path,
            "name": doc.name,
            "draft_marker_present": "<!-- DRAFT -->" in doc.content,
            "word_count": len(doc.content.split()),
            "sources_count": len(doc.sources),
        })

    return {"directory": scan_path, "documents": documents}


def _read_file(path: str) -> str:
    """Read file content as UTF-8 text."""
    with open(path, encoding="utf-8") as f:
        return f.read()


def _classify_sources(sources: List[str]) -> Tuple[List[str], int]:
    """Split sources into URLs and non-URLs.

    Returns:
        Tuple of (url_list, non_url_count).
    """
    urls: List[str] = []
    non_url_count = 0
    for source in sources:
        if source.startswith("http://") or source.startswith("https://"):
            urls.append(source)
        else:
            non_url_count += 1
    return urls, non_url_count


_SECTION_KEYWORDS = frozenset({"claims", "synthesis", "sources", "findings"})


def _detect_sections(content: str) -> Dict[str, bool]:
    """Detect presence of key sections by heading text.

    Looks for markdown headings containing known keywords.
    """
    found = {kw: False for kw in _SECTION_KEYWORDS}
    for line in content.split("\n"):
        stripped = line.strip()
        if not stripped.startswith("#"):
            continue
        heading_text = stripped.lstrip("#").strip().lower()
        for kw in _SECTION_KEYWORDS:
            if kw in heading_text:
                found[kw] = True
    return found
