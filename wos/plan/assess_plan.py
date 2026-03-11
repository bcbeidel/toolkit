"""Plan document structural assessment.

Reports observable facts about plan documents — status, task completion,
section presence, file-boundary analysis. The model infers execution
state and next actions from these facts.
"""

from __future__ import annotations

import os
import re
from typing import Dict, List, Optional

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
            if "task" in heading:
                in_tasks = True
                continue
            elif "validation" in heading:
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


_FILE_CHANGE_RE = re.compile(
    r"^-\s*(?:Create|Modify|Delete|Test):\s*`?([^`\s]+?)(?::\d[\d\-]*)?`?\s*$",
    re.IGNORECASE,
)


def _extract_file_changes(content: str) -> List[str]:
    """Extract file paths from the File Changes section.

    Parses lines like ``- Create: `path/to/file.py` `` between
    the File Changes heading and the next heading.

    Returns:
        List of file path strings.
    """
    files: List[str] = []
    in_section = False
    for line in content.split("\n"):
        stripped = line.strip()
        if stripped.startswith("#"):
            heading = stripped.lstrip("#").strip().lower()
            if "file changes" in heading:
                in_section = True
                continue
            elif in_section:
                break  # hit next section
        if not in_section:
            continue
        match = _FILE_CHANGE_RE.match(stripped)
        if match:
            files.append(match.group(1))
    return files


_TASK_HEADING_RE = re.compile(r"^#{2,4}\s+Task\s+(\d+)", re.IGNORECASE)


def _map_task_files(
    tasks: List[dict], file_changes: List[str], content: str,
) -> Dict[str, List[str]]:
    """Map tasks to files they modify.

    If the plan has per-task headings with file listings, uses those.
    Otherwise falls back to assigning all file_changes to all tasks
    (conservative — forces sequential execution).

    Returns:
        Dict mapping task index (str) to list of file paths.
    """
    if not tasks:
        return {}

    # Try to find per-task file listings under task headings
    task_files: Dict[str, List[str]] = {}
    current_task: Optional[str] = None
    for line in content.split("\n"):
        stripped = line.strip()
        heading_match = _TASK_HEADING_RE.match(stripped)
        if heading_match:
            current_task = heading_match.group(1)
            task_files[current_task] = []
            continue
        if current_task is not None:
            file_match = _FILE_CHANGE_RE.match(stripped)
            if file_match:
                task_files[current_task].append(file_match.group(1))

    # If we found per-task mappings, use them
    if task_files and any(task_files.values()):
        return task_files

    # Fallback: assign all files to all tasks
    return {str(t["index"]): list(file_changes) for t in tasks}


def _find_overlaps(task_file_map: Dict[str, List[str]]) -> List[dict]:
    """Find task pairs that modify the same files.

    Returns:
        List of dicts with keys: tasks (pair of indices), shared_files.
    """
    overlaps: List[dict] = []
    keys = sorted(task_file_map.keys())
    for i, k1 in enumerate(keys):
        for k2 in keys[i + 1:]:
            shared = sorted(set(task_file_map[k1]) & set(task_file_map[k2]))
            if shared:
                overlaps.append({"tasks": [k1, k2], "shared_files": shared})
    return overlaps


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
        file_changes, readiness. If file doesn't exist, all values
        except file and exists are None.
    """
    if not os.path.isfile(path):
        return {
            "file": path,
            "exists": False,
            "frontmatter": None,
            "sections": None,
            "tasks": None,
            "file_changes": None,
            "readiness": None,
        }

    text = _read_file(path)
    doc = parse_document(path, text)

    sections = _detect_sections(doc.content)
    tasks = _parse_tasks(doc.content)
    file_changes = _extract_file_changes(doc.content)
    task_file_map = _map_task_files(tasks, file_changes, doc.content)
    overlaps = _find_overlaps(task_file_map)

    completed = sum(1 for t in tasks if t["completed"])
    pending = len(tasks) - completed

    # Readiness assessment
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

    parallel_eligible = (
        pending >= 3
        and len(overlaps) == 0
        and status_ok
    )

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
        "file_changes": {
            "files": file_changes,
            "task_file_map": task_file_map,
            "overlapping_tasks": overlaps,
        },
        "readiness": {
            "status_ok": status_ok,
            "sections_complete": sections["all_present"],
            "has_pending_tasks": pending > 0,
            "parallel_eligible": parallel_eligible,
            "issues": issues,
        },
    }


def scan_plans(root: str, subdir: str = "docs/plans") -> dict:
    """Find plans with status: executing in a directory.

    Args:
        root: Project root directory.
        subdir: Subdirectory to scan (default: docs/plans).

    Returns:
        Dict with keys: directory, plans. Each plan has: file, name,
        status, total_tasks, completed_tasks, pending_tasks.
    """
    scan_path = os.path.join(root, subdir)

    if not os.path.isdir(scan_path):
        return {"directory": scan_path, "plans": []}

    plans: list = []
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

        if doc.type != "plan" or doc.status != "executing":
            continue

        tasks = _parse_tasks(doc.content)
        completed = sum(1 for t in tasks if t["completed"])

        plans.append({
            "file": file_path,
            "name": doc.name,
            "status": doc.status,
            "total_tasks": len(tasks),
            "completed_tasks": completed,
            "pending_tasks": len(tasks) - completed,
        })

    return {"directory": scan_path, "plans": plans}
