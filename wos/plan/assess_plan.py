"""Plan document structural assessment.

Reports observable facts about plan documents — status, task completion,
section presence, file-boundary analysis. The model infers execution
state and next actions from these facts.
"""

from __future__ import annotations

import re
from typing import List

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
