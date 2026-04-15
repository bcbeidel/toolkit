"""Plan document class and structural assessment.

Combines the PlanDocument subclass (with task parsing) with classmethods
for assessment (assess, scan).

Reports observable facts about plan documents — status, task completion,
section presence. The model infers execution state and next actions from
these facts.
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List

from wos.document import Document, parse_document

# ── Plan section constants ─────────────────────────────────────────

_PLAN_SECTIONS = {
    "goal": "goal",
    "scope": "scope",
    "approach": "approach",
    "file_changes": "file changes",
    "tasks": "tasks",
    "validation": "validation",
}

# ── Task parsing ───────────────────────────────────────────────────

_TASK_RE = re.compile(
    r"^- \[([ xX])\] "
    r"(?:Task \d+:\s*)?"
    r"(.+?)"
    r"(?:\s*<!--\s*sha:(\w+)\s*-->)?"
    r"\s*$",
)


def _parse_tasks(content: str) -> List[dict]:
    """Extract top-level checkbox items from plan content.

    Parses ``- [ ] Task N: title`` and ``- [x] Task N: title <!-- sha:abc -->``
    patterns. Indented checkboxes are ignored. Parsing is restricted to
    headings containing "task" or "chunk" and stops at a "validation" heading.

    Returns:
        List of dicts with keys: index, title, completed, sha.
    """
    has_tasks_heading = any(
        "task" in line.lstrip("#").strip().lower()
        or "chunk" in line.lstrip("#").strip().lower()
        for line in content.split("\n")
        if line.strip().startswith("#")
    )

    tasks: List[dict] = []
    index = 0
    in_tasks = not has_tasks_heading
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
        tasks.append({
            "index": index,
            "title": match.group(2).strip(),
            "completed": match.group(1).lower() == "x",
            "sha": match.group(3),
        })

    return tasks


def _detect_sections(doc: "PlanDocument") -> Dict[str, bool]:
    """Check for presence of 6 required plan sections by heading text."""
    found = {key: doc.has_section(keyword) for key, keyword in _PLAN_SECTIONS.items()}
    found["all_present"] = all(found.values())
    return found


# ── Document subclass ──────────────────────────────────────────────


@Document.register("plan")
@dataclass
class PlanDocument(Document):
    """A plan document with parsed task list and completion tracking."""

    tasks: List[dict] = field(default_factory=list, init=False)

    def __post_init__(self) -> None:
        self.tasks = _parse_tasks(self.content)

    def tasks_complete(self) -> bool:
        """Return True if all tasks are marked completed."""
        return bool(self.tasks) and all(t["completed"] for t in self.tasks)

    def completion_stats(self) -> dict:
        """Return task completion counts."""
        total = len(self.tasks)
        done = sum(1 for t in self.tasks if t["completed"])
        return {"total": total, "done": done, "remaining": total - done}

    @classmethod
    def assess(cls, path: str) -> dict:
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

        text = Path(path).read_text(encoding="utf-8")
        doc = parse_document(path, text)

        sections = _detect_sections(doc)
        tasks = doc.tasks if isinstance(doc, PlanDocument) else []

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

    @classmethod
    def scan(cls, root: str, subdir: str = "") -> dict:
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
        from wos.discovery import filter_documents

        label, plan_docs = filter_documents(
            Path(root), "plan", subdir=subdir, status="executing"
        )
        plans = []
        for doc in plan_docs:
            tasks = doc.tasks if isinstance(doc, PlanDocument) else []
            completed = sum(1 for t in tasks if t["completed"])
            plans.append({
                "file": os.path.join(root, doc.path),
                "name": doc.name,
                "status": doc.status,
                "total_tasks": len(tasks),
                "completed_tasks": completed,
                "pending_tasks": len(tasks) - completed,
            })
        return {"directory": label, "plans": plans}
