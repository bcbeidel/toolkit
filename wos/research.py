"""Research document class and structural assessment.

Combines the ResearchDocument subclass with module-level assessment
functions (assess_file, scan_directory, check_gates, check_single_gate).
Reports observable facts about research documents — word count, draft
markers, section presence, source listing. The model infers phase and
next actions from these facts.

Gate checks validate phase handoff conditions with deterministic
structural checks (no LLM judgment). Each gate corresponds to an
agent's exit condition in the research pipeline.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

from wos.document import Document, parse_document
from wos.url_checker import check_urls

# ── Document subclass ──────────────────────────────────────────────


@Document.register("research")
@dataclass
class ResearchDocument(Document):
    """A research document with source URL and draft-marker validation."""

    def issues(self, root: Path, verify_urls: bool = True, **_: object) -> List[dict]:
        """Return base issues plus research-specific checks.

        Adds: sources required, sources-as-dicts warning, draft marker
        warning, and source URL reachability (fail/warn).

        Args:
            root: Project root directory.
            verify_urls: If False, skip HTTP reachability checks.

        Returns:
            List of issue dicts with keys: file, issue, severity.
        """
        result = super().issues(root)

        if not self.sources:
            result.append({
                "file": self.path,
                "issue": "Research document has no sources",
                "severity": "fail",
            })

        for idx, source in enumerate(self.sources):
            if isinstance(source, dict):
                result.append({
                    "file": self.path,
                    "issue": f"sources[{idx}] is a dict, expected a URL string",
                    "severity": "warn",
                })

        if "<!-- DRAFT -->" in self.content:
            result.append({
                "file": self.path,
                "issue": "Research document contains <!-- DRAFT --> marker",
                "severity": "warn",
            })

        if verify_urls and self.sources:
            urls = []
            for s in self.sources:
                if isinstance(s, dict):
                    urls.append(s.get("url", s.get("href", "")))
                else:
                    urls.append(str(s))
            for url_result in check_urls(urls):
                if not url_result.reachable:
                    if url_result.status in (403, 429):
                        result.append({
                            "file": self.path,
                            "issue": (
                                f"URL returned {url_result.status}"
                                f" (site may block automated checks):"
                                f" {url_result.url}"
                            ),
                            "severity": "warn",
                        })
                    else:
                        reason = (
                            f" ({url_result.reason})" if url_result.reason else ""
                        )
                        result.append({
                            "file": self.path,
                            "issue": (
                                f"Source URL unreachable:"
                                f" {url_result.url}{reason}"
                            ),
                            "severity": "fail",
                        })

        return result


# ── Module-level assessment functions ─────────────────────────────


_SECTION_KEYWORDS = frozenset({
    "claims", "synthesis", "sources", "findings", "challenge",
})


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

    text = Path(path).read_text(encoding="utf-8")
    doc = parse_document(path, text)

    urls = [s for s in doc.sources if s.startswith(("http://", "https://"))]
    non_url_count = len(doc.sources) - len(urls)
    sections = {kw: doc.has_section(kw) for kw in _SECTION_KEYWORDS}

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
            "word_count": doc.word_count,
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
    from wos.discovery import filter_documents

    label, research_docs = filter_documents(Path(root), "research", subdir=subdir)
    documents = [
        {
            "file": os.path.join(root, doc.path),
            "name": doc.name,
            "draft_marker_present": "<!-- DRAFT -->" in doc.content,
            "word_count": doc.word_count,
            "sources_count": len(doc.sources),
        }
        for doc in research_docs
    ]
    return {"directory": label, "documents": documents}


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
        return {
            "file": path,
            "gates": {gate: {"pass": False, "checks": {}} for gate in _GATE_ORDER},
            "current_phase": "gatherer",
        }

    text = Path(path).read_text(encoding="utf-8")
    doc = parse_document(path, text)

    gates: Dict[str, dict] = {
        "gatherer_exit": _check_gatherer_exit(doc),
        "evaluator_exit": _check_evaluator_exit(doc),
        "challenger_exit": _check_challenger_exit(doc),
        "synthesizer_exit": _check_synthesizer_exit(doc),
        "verifier_exit": _check_verifier_exit(doc),
        "finalizer_exit": _check_finalizer_exit(doc),
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

def _check_gatherer_exit(doc: Document) -> dict:
    """Gatherer exit: Sources section exists, URLs in file, extracts present."""
    checks = {
        "sources_section_present": doc.has_section("sources"),
        "sources_have_urls": "http" in doc.content,
        "extracts_present": _has_extracts(doc.content),
    }
    return {"pass": all(checks.values()), "checks": checks}


def _check_evaluator_exit(doc: Document) -> dict:
    """Evaluator exit: document contains 'Tier' and 'Status' text."""
    checks = {
        "sources_have_tier": "Tier" in doc.content,
        "sources_have_status": "Status" in doc.content,
    }
    return {"pass": all(checks.values()), "checks": checks}


def _check_challenger_exit(doc: Document) -> dict:
    """Challenger exit: ## Challenge section exists."""
    checks = {"challenge_section_exists": doc.has_section("challenge")}
    return {"pass": all(checks.values()), "checks": checks}


def _check_synthesizer_exit(doc: Document) -> dict:
    """Synthesizer exit: ## Findings section exists."""
    checks = {"findings_section_exists": doc.has_section("findings")}
    return {"pass": all(checks.values()), "checks": checks}


def _check_verifier_exit(doc: Document) -> dict:
    """Verifier exit: Claims section exists, no 'unverified' anywhere in document."""
    checks = {
        "claims_section_exists": doc.has_section("claims"),
        "no_unverified_claims": "unverified" not in doc.content.lower(),
    }
    return {"pass": all(checks.values()), "checks": checks}


def _check_finalizer_exit(doc: Document) -> dict:
    """Finalizer exit: no DRAFT marker, type is research, sources non-empty."""
    checks = {
        "draft_marker_absent": "<!-- DRAFT -->" not in doc.content,
        "type_is_research": doc.type == "research",
        "sources_non_empty": len(doc.sources) > 0,
    }
    return {"pass": all(checks.values()), "checks": checks}


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
