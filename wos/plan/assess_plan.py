"""Plan document structural assessment.

Reports observable facts about plan documents — status, task completion,
section presence, file-boundary analysis. The model infers execution
state and next actions from these facts.
"""

from __future__ import annotations

import re
from typing import Dict, List, Optional

_TASK_RE = re.compile(
    r"^- \[([ xX])\] "          # checkbox at line start (not indented)
    r"(?:Task \d+:\s*)?"        # optional "Task N: " prefix
    r"(.+?)"                    # title (non-greedy)
    r"(?:\s*<!--\s*sha:(\w+)\s*-->)?"  # optional SHA annotation
    r"\s*$",
)


def _parse_tasks(content: str) -> List[dict]:
    """Extract top-level checkbox items from plan content.

    Parses ``- [ ] Task N: title`` and ``- [x] Task N: title <!-- sha:abc -->``
    patterns. Indented checkboxes (sub-steps) are ignored.

    Returns:
        List of dicts with keys: index, title, completed, sha.
    """
    tasks: List[dict] = []
    index = 0
    for line in content.split("\n"):
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
