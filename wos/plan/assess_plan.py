"""Plan document structural assessment.

Reports observable facts about plan documents — status, task completion,
section presence. The model infers execution state and next actions from
these facts.
"""

from __future__ import annotations

import os
import re
from typing import Dict, List

from wos.document import parse_document

_TASK_RE = re.compile(
    r"^- \[([ xX])\] "          # checkbox at line start (not indented)
    r"(?:Task \d+:\s*)?"        # optional "Task N: " prefix
    r"(.+?)"                    # title (non-greedy)
    r"(?:\s*<!--\s*sha:(\w+)\s*-->)?"  # optional SHA annotation
    r"\s*$",
)


def _parse_tasks(content: str) -> List[dict]:
    """Extract top-level checkbox items from plan task sections.

    Parses ``- [ ] Task N: title`` and ``- [x] Task N: title <!-- sha:abc -->``
    patterns. Indented checkboxes (sub-steps) are ignored. Only parses
    checkboxes that appear after a Tasks/Task heading and before a
    Validation heading (to exclude validation checkboxes).

    Returns:
        List of dicts with keys: index, title, completed, sha.
    """
    # Check if content has a Tasks heading — if so, restrict parsing
    has_tasks_heading = any(
        "task" in line.lstrip("#").strip().lower()
        for line in content.split("\n")
        if line.strip().startswith("#")
    )

    tasks: List[dict] = []
    index = 0
    in_tasks = not has_tasks_heading  # if no heading, parse everything
    for line in content.split("\n"):
        stripped = line.strip()
        if stripped.startswith("#") and has_tasks_heading:
            heading = stripped.lstrip("#").strip().lower()
            if "task" in heading or "chunk" in heading:
                in_tasks = True
            else:
                in_tasks = False
            continue
        if not in_tasks:
            continue
        match = _TASK_RE.match(line)
        if not match:
            continue
        index += 1
        check, title, sha = match.groups()
        tasks.append({
            "index": index,
            "title": title.strip(),
            "completed": check.lower() == "x",
            "sha": sha,
        })
    return tasks


_PLAN_SECTIONS = {
    "goal": "goal",
    "scope": "scope",
    "approach": "approach",
    "file_changes": "file changes",
    "tasks": "tasks",
    "validation": "validation",
}


def _detect_sections(content: str) -> Dict[str, bool]:
    """Check for presence of 6 required plan sections by heading text.

    Returns:
        Dict mapping section keys to bool, plus 'all_present' summary.
    """
    found: Dict[str, bool] = {key: False for key in _PLAN_SECTIONS}
    for line in content.split("\n"):
        stripped = line.strip()
        if not stripped.startswith("#"):
            continue
        heading_text = stripped.lstrip("#").strip().lower()
        for key, keyword in _PLAN_SECTIONS.items():
            if keyword in heading_text:
                found[key] = True
    found["all_present"] = all(
        v for k, v in found.items() if k != "all_present"
    )
    return found


def _read_file(path: str) -> str:
    """Read file content as UTF-8 text."""
    with open(path, encoding="utf-8") as f:
        return f.read()


def assess_file(path: str) -> dict:
    """Assess structural facts of a single plan document.

    Args:
        path: Absolute or relative path to a plan markdown file.

    Returns:
        Dict with keys: file, exists, frontmatter, sections, tasks,
        readiness. If file doesn't exist, all values except file and
        exists are None.
    """
    if not os.path.isfile(path):
        return {
            "file": path,
            "exists": False,
            "frontmatter": None,
            "sections": None,
            "tasks": None,
            "readiness": None,
        }

    text = _read_file(path)
    doc = parse_document(path, text)

    sections = _detect_sections(doc.content)
    tasks = _parse_tasks(doc.content)

    completed = sum(1 for t in tasks if t["completed"])
    pending = len(tasks) - completed

    executable_statuses = {"approved", "executing"}
    status_ok = doc.status in executable_statuses
    issues: List[str] = []
    if doc.status and doc.status not in executable_statuses:
        issues.append(f"Status is '{doc.status}' — not executable")
    if doc.status is None:
        issues.append("No status field — legacy plan")
        status_ok = True  # allow with warning
    if not sections["all_present"]:
        missing = [
            k for k, v in sections.items()
            if k != "all_present" and not v
        ]
        issues.append(f"Missing sections: {', '.join(missing)}")

    return {
        "file": path,
        "exists": True,
        "frontmatter": {
            "name": doc.name,
            "status": doc.status,
            "type": doc.type,
        },
        "sections": sections,
        "tasks": {
            "total": len(tasks),
            "completed": completed,
            "pending": pending,
            "items": tasks,
        },
        "readiness": {
            "status_ok": status_ok,
            "sections_complete": sections["all_present"],
            "has_pending_tasks": pending > 0,
            "issues": issues,
        },
    }


def scan_plans(root: str, subdir: str = "") -> dict:
    """Find plans with status: executing in the project.

    Uses the discovery module to find all type: plan documents with
    status: executing. If subdir is provided, restricts to that
    subdirectory.

    Args:
        root: Project root directory.
        subdir: Optional subdirectory to restrict scan (default: full tree).

    Returns:
        Dict with keys: directory, plans. Each plan has: file, name,
        status, total_tasks, completed_tasks, pending_tasks.
    """
    from pathlib import Path

    from wos.discovery import discover_documents

    root_path = Path(root)
    docs = discover_documents(root_path)

    plan_docs = [
        d for d in docs
        if d.type == "plan" and d.status == "executing"
    ]

    if subdir:
        plan_docs = [
            d for d in plan_docs
            if d.path.startswith(subdir + "/") or d.path.startswith(subdir)
        ]

    scan_label = os.path.join(root, subdir) if subdir else root

    plans: list = []
    for doc in plan_docs:
        tasks = _parse_tasks(doc.content)
        completed = sum(1 for t in tasks if t["completed"])

        plans.append({
            "file": os.path.join(root, doc.path),
            "name": doc.name,
            "status": doc.status,
            "total_tasks": len(tasks),
            "completed_tasks": completed,
            "pending_tasks": len(tasks) - completed,
        })

    return {"directory": scan_label, "plans": plans}
