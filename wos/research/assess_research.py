"""Research document structural assessment.

Reports observable facts about research documents — word count, draft
markers, section presence, source listing. The model infers phase and
next actions from these facts.

Gate checks validate phase handoff conditions with deterministic
structural checks (no LLM judgment). Each gate corresponds to an
agent's exit condition in the research pipeline.
"""

from __future__ import annotations

import os
from typing import Dict, List, Optional, Tuple

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


def scan_directory(root: str, subdir: str = "") -> dict:
    """Scan for research documents and return summaries.

    Uses the discovery module to find all type: research documents.
    If subdir is provided, restricts to that subdirectory.

    Args:
        root: Project root directory.
        subdir: Optional subdirectory to restrict scan (default: full tree).

    Returns:
        Dict with keys: directory, documents. Each document has:
        file, name, draft_marker_present, word_count, sources_count.
    """
    from pathlib import Path

    from wos.discovery import discover_documents

    root_path = Path(root)
    docs = discover_documents(root_path)

    # Filter to research type
    research_docs = [d for d in docs if d.type == "research"]

    # Optionally restrict to subdir
    if subdir:
        research_docs = [
            d for d in research_docs
            if d.path.startswith(subdir + "/") or d.path.startswith(subdir)
        ]

    scan_label = os.path.join(root, subdir) if subdir else root

    documents: list = []
    for doc in research_docs:
        documents.append({
            "file": os.path.join(root, doc.path),
            "name": doc.name,
            "draft_marker_present": "<!-- DRAFT -->" in doc.content,
            "word_count": len(doc.content.split()),
            "sources_count": len(doc.sources),
        })

    return {"directory": scan_label, "documents": documents}


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


_SECTION_KEYWORDS = frozenset({
    "claims", "synthesis", "sources", "findings", "challenge",
})


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


# ---------------------------------------------------------------------------
# Gate checks — deterministic phase handoff validation
# ---------------------------------------------------------------------------

# Ordered list of gate names for current_phase derivation.
_GATE_ORDER = [
    "gatherer_exit",
    "evaluator_exit",
    "challenger_exit",
    "synthesizer_exit",
    "verifier_exit",
    "finalizer_exit",
]

# Phase name that follows each gate (used for current_phase).
_PHASE_AFTER_GATE = {
    "gatherer_exit": "evaluator",
    "evaluator_exit": "challenger",
    "challenger_exit": "synthesizer",
    "synthesizer_exit": "verifier",
    "verifier_exit": "finalizer",
    "finalizer_exit": "done",
}


def check_gates(path: str) -> dict:
    """Check all research phase gates for a document.

    Returns a dict with ``file``, ``gates`` (per-gate results), and
    ``current_phase`` (the phase after the highest passing gate, or
    ``"gatherer"`` if none pass).
    """
    if not os.path.isfile(path):
        empty_checks: Dict[str, dict] = {}
        for gate in _GATE_ORDER:
            empty_checks[gate] = {"pass": False, "checks": {}}
        return {
            "file": path,
            "gates": empty_checks,
            "current_phase": "gatherer",
        }

    text = _read_file(path)
    doc = parse_document(path, text)
    content = doc.content
    sections = _detect_sections(content)

    gates: Dict[str, dict] = {
        "gatherer_exit": _check_gatherer_exit(content, doc, sections),
        "evaluator_exit": _check_evaluator_exit(content),
        "challenger_exit": _check_challenger_exit(sections),
        "synthesizer_exit": _check_synthesizer_exit(sections),
        "verifier_exit": _check_verifier_exit(content, sections),
        "finalizer_exit": _check_finalizer_exit(content, doc),
    }

    # Derive current_phase: phase after highest passing gate.
    current_phase = "gatherer"
    for gate_name in _GATE_ORDER:
        if gates[gate_name]["pass"]:
            current_phase = _PHASE_AFTER_GATE[gate_name]
        else:
            break

    return {
        "file": path,
        "gates": gates,
        "current_phase": current_phase,
    }


def check_single_gate(path: str, gate_name: str) -> dict:
    """Check a single named gate and return its result."""
    result = check_gates(path)
    if gate_name == "all":
        return result
    if gate_name not in result["gates"]:
        return {"error": f"Unknown gate: {gate_name}",
                "valid_gates": _GATE_ORDER + ["all"]}
    return {
        "file": path,
        "gate": gate_name,
        **result["gates"][gate_name],
        "current_phase": result["current_phase"],
    }


# --- Individual gate checks -----------------------------------------------

def _check_gatherer_exit(content: str, doc: object, sections: Dict[str, bool]) -> dict:
    """Gatherer exit: DRAFT exists, sources table present, URLs present."""
    sources_table = _find_table_under_heading(content, "sources")
    has_urls = False
    if sources_table is not None:
        columns = _table_columns(sources_table)
        has_urls = any("url" in c.lower() for c in columns)

    checks = {
        "draft_exists": True,  # file exists (checked before calling)
        "sources_table_present": sources_table is not None,
        "sources_have_urls": has_urls,
        "extracts_present": _has_extracts(content),
    }
    return {"pass": all(checks.values()), "checks": checks}


def _check_evaluator_exit(content: str) -> dict:
    """Evaluator exit: sources table has Tier column with values."""
    sources_table = _find_table_under_heading(content, "sources")
    has_tier = False
    has_status = False
    if sources_table is not None:
        columns = _table_columns(sources_table)
        has_tier = any("tier" in c.lower() for c in columns)
        has_status = any("status" in c.lower() for c in columns)

    checks = {
        "sources_have_tier": has_tier,
        "sources_have_status": has_status,
    }
    return {"pass": all(checks.values()), "checks": checks}


def _check_challenger_exit(sections: Dict[str, bool]) -> dict:
    """Challenger exit: ## Challenge section exists."""
    checks = {"challenge_section_exists": sections.get("challenge", False)}
    return {"pass": all(checks.values()), "checks": checks}


def _check_synthesizer_exit(sections: Dict[str, bool]) -> dict:
    """Synthesizer exit: ## Findings section exists."""
    checks = {"findings_section_exists": sections.get("findings", False)}
    return {"pass": all(checks.values()), "checks": checks}


def _check_verifier_exit(content: str, sections: Dict[str, bool]) -> dict:
    """Verifier exit: Claims section with rows, no 'unverified' in Status column."""
    has_claims = sections.get("claims", False)
    claims_table = _find_table_under_heading(content, "claims")
    has_rows = False
    no_unverified = True
    if claims_table is not None:
        rows = _table_data_rows(claims_table)
        has_rows = len(rows) > 0
        columns = _table_columns(claims_table)
        status_idx = next(
            (i for i, c in enumerate(columns) if "status" in c.lower()), None
        )
        for row in rows:
            # Check only the Status column if found, else fall back to all cells.
            cells_to_check = (
                [row[status_idx]] if status_idx is not None and status_idx < len(row)
                else row
            )
            for cell in cells_to_check:
                if "unverified" in cell.lower():
                    no_unverified = False
                    break

    checks = {
        "claims_section_exists": has_claims,
        "claims_table_has_rows": has_rows,
        "no_unverified_claims": no_unverified,
    }
    return {"pass": all(checks.values()), "checks": checks}


def _check_finalizer_exit(content: str, doc: object) -> dict:
    """Finalizer exit: no DRAFT marker, type is research, sources non-empty."""
    checks = {
        "draft_marker_absent": "<!-- DRAFT -->" not in content,
        "type_is_research": getattr(doc, "type", None) == "research",
        "sources_non_empty": len(getattr(doc, "sources", [])) > 0,
    }
    return {"pass": all(checks.values()), "checks": checks}


# --- Table parsing helpers -------------------------------------------------

def _find_table_under_heading(content: str, keyword: str) -> Optional[str]:
    """Find the first markdown table under a heading containing keyword.

    Returns the full table text (header + separator + data rows), or
    None if not found.
    """
    lines = content.split("\n")
    in_section = False
    section_level = 0
    table_lines: List[str] = []
    collecting = False

    for line in lines:
        stripped = line.strip()

        # Detect headings.
        if stripped.startswith("#"):
            heading_level = len(stripped) - len(stripped.lstrip("#"))
            heading_text = stripped.lstrip("#").strip().lower()
            if keyword in heading_text:
                in_section = True
                section_level = heading_level
                collecting = False
                table_lines = []
                continue
            elif in_section:
                # Sub-headings (deeper level) stay within the section.
                if heading_level > section_level:
                    continue
                # Same or higher level heading ends the section.
                if collecting and table_lines:
                    return "\n".join(table_lines)
                in_section = False
                collecting = False
                table_lines = []
                continue

        if not in_section:
            continue

        # Collect table rows (lines starting with |).
        if stripped.startswith("|"):
            collecting = True
            table_lines.append(stripped)
        elif collecting:
            # Non-table line ends the table.
            if table_lines:
                return "\n".join(table_lines)
            collecting = False

    # End of file while collecting.
    if collecting and table_lines:
        return "\n".join(table_lines)
    return None


def _table_columns(table_text: str) -> List[str]:
    """Extract column names from a markdown table header row."""
    lines = table_text.split("\n")
    if not lines:
        return []
    header = lines[0]
    cells = [c.strip() for c in header.split("|")]
    # Split on | gives empty strings at start/end.
    return [c for c in cells if c]


def _table_data_rows(table_text: str) -> List[List[str]]:
    """Extract data rows from a markdown table (skip header + separator)."""
    lines = table_text.split("\n")
    rows: List[List[str]] = []
    for line in lines[2:]:  # Skip header and separator.
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [c.strip() for c in stripped.split("|")]
        cells = [c for c in cells if c]
        if cells:
            rows.append(cells)
    return rows


def _has_extracts(content: str) -> bool:
    """Check if the document has structured extracts.

    Looks for blockquote lines (common extract format) or multiple
    sub-question headings (### level) which structure Phase 2 output.
    """
    blockquote_count = 0
    subheading_count = 0
    for line in content.split("\n"):
        stripped = line.strip()
        if stripped.startswith(">") and len(stripped) > 2:
            blockquote_count += 1
        if stripped.startswith("###"):
            subheading_count += 1
    # Extracts present if there are multiple blockquotes or sub-headings.
    return blockquote_count >= 2 or subheading_count >= 2
