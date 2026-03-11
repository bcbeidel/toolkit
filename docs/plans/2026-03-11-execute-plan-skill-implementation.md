---
name: Execute Plan Skill Implementation
description: Implementation plan for wos:execute-plan skill — entry script, SKILL.md, and 4 reference files
type: plan
status: executing
related:
  - docs/plans/2026-03-11-execute-plan-skill-design.md
---

# Execute Plan Skill Implementation

**Goal:** Create the `wos:execute-plan` skill with a deterministic entry
script (`plan_assess.py`), SKILL.md under 500 lines, and 4 reference files
covering execution, parallel dispatch, recovery, and multi-session resumption.

**Scope:**

Must have:
- `wos/plan/assess_plan.py` with `assess_file()`, `scan_plans()`, and all
  helper functions
- `skills/execute-plan/scripts/plan_assess.py` PEP 723 CLI wrapper
- `tests/test_plan_assess.py` with comprehensive test coverage
- `skills/execute-plan/SKILL.md` under 500 lines
- 4 reference files in `skills/execute-plan/references/`

Won't have:
- `wos:validate-plan` skill (#161)
- `wos:finish-work` skill (#162)
- Code-enforced status transitions (instruction-based, not Python)
- Plan format validation in `wos/validators.py` (separate concern)

**Approach:** TDD — write tests first for the Python module, then implement.
Follow the `wos/research/assess_research.py` pattern exactly for module
structure and CLI wrapper. Write SKILL.md and references last since they
have no code dependencies.

**File Changes:**
- Create: `wos/plan/__init__.py`
- Create: `wos/plan/assess_plan.py`
- Create: `tests/test_plan_assess.py`
- Create: `skills/execute-plan/scripts/plan_assess.py`
- Create: `skills/execute-plan/SKILL.md`
- Create: `skills/execute-plan/references/execution-guide.md`
- Create: `skills/execute-plan/references/parallel-dispatch.md`
- Create: `skills/execute-plan/references/recovery-patterns.md`
- Create: `skills/execute-plan/references/multi-session-resumption.md`

**Branch:** `feat/160-execute-plan-skill`

---

## Chunk 1: Core Python Module (TDD)

### Task 1: Create package and write tests for `_parse_tasks`

**Files:**
- Create: `wos/plan/__init__.py`
- Create: `wos/plan/assess_plan.py` (stub)
- Create: `tests/test_plan_assess.py`

- [ ] Create `wos/plan/__init__.py` with docstring:

```python
"""WOS plan skill support modules."""
```

- [ ] Create `wos/plan/assess_plan.py` with module docstring and empty
  `_parse_tasks` stub that raises `NotImplementedError`

```python
"""Plan document structural assessment.

Reports observable facts about plan documents — status, task completion,
section presence, file-boundary analysis. The model infers execution
state and next actions from these facts.
"""

from __future__ import annotations


def _parse_tasks(content: str) -> list:
    raise NotImplementedError
```

- [ ] Write failing tests in `tests/test_plan_assess.py`:

```python
"""Tests for wos/plan/assess_plan.py."""

from __future__ import annotations


class TestParseTasks:
    """Tests for _parse_tasks() — checkbox extraction."""

    def test_unchecked_tasks(self) -> None:
        """Unchecked tasks parsed with completed=False."""
        from wos.plan.assess_plan import _parse_tasks

        content = (
            "### Tasks\n"
            "\n"
            "- [ ] Task 1: Create package structure\n"
            "- [ ] Task 2: Write tests\n"
        )
        tasks = _parse_tasks(content)
        assert len(tasks) == 2
        assert tasks[0] == {"index": 1, "title": "Create package structure", "completed": False, "sha": None}
        assert tasks[1] == {"index": 2, "title": "Write tests", "completed": False, "sha": None}

    def test_checked_tasks_with_sha(self) -> None:
        """Checked tasks with SHA annotation parsed correctly."""
        from wos.plan.assess_plan import _parse_tasks

        content = (
            "- [x] Task 1: Create package <!-- sha:a1b2c3d -->\n"
            "- [x] Task 2: Write tests <!-- sha:e4f5g6h -->\n"
            "- [ ] Task 3: Implement parser\n"
        )
        tasks = _parse_tasks(content)
        assert len(tasks) == 3
        assert tasks[0]["completed"] is True
        assert tasks[0]["sha"] == "a1b2c3d"
        assert tasks[1]["sha"] == "e4f5g6h"
        assert tasks[2]["completed"] is False
        assert tasks[2]["sha"] is None

    def test_checked_tasks_without_sha(self) -> None:
        """Checked tasks without SHA have sha=None."""
        from wos.plan.assess_plan import _parse_tasks

        content = "- [x] Task 1: Create package\n"
        tasks = _parse_tasks(content)
        assert tasks[0]["completed"] is True
        assert tasks[0]["sha"] is None

    def test_empty_content(self) -> None:
        """No checkboxes returns empty list."""
        from wos.plan.assess_plan import _parse_tasks

        assert _parse_tasks("# Just a heading\n\nSome text.\n") == []

    def test_nested_checkboxes_ignored(self) -> None:
        """Indented sub-checkboxes (step-level) are not treated as tasks."""
        from wos.plan.assess_plan import _parse_tasks

        content = (
            "- [ ] Task 1: Create package\n"
            "  - [ ] Step 1a: Write init file\n"
            "  - [ ] Step 1b: Add docstring\n"
            "- [ ] Task 2: Write tests\n"
        )
        tasks = _parse_tasks(content)
        assert len(tasks) == 2

    def test_title_without_task_prefix(self) -> None:
        """Checkboxes without 'Task N:' prefix use full text as title."""
        from wos.plan.assess_plan import _parse_tasks

        content = "- [ ] Create package structure\n- [ ] Write tests\n"
        tasks = _parse_tasks(content)
        assert tasks[0]["title"] == "Create package structure"
        assert tasks[1]["title"] == "Write tests"
```

- [ ] Run tests — expected: all FAIL with `NotImplementedError`

```bash
uv run python -m pytest tests/test_plan_assess.py -v
```

- [ ] Implement `_parse_tasks` in `wos/plan/assess_plan.py`:

```python
import re
from typing import Dict, List, Optional, Tuple

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
```

- [ ] Run tests — expected: all PASS

```bash
uv run python -m pytest tests/test_plan_assess.py -v
```

- [ ] Commit

### Task 2: Write tests for `_detect_sections` and implement

**Files:**
- Modify: `wos/plan/assess_plan.py`
- Modify: `tests/test_plan_assess.py`

- [ ] Add tests to `tests/test_plan_assess.py`:

```python
class TestDetectSections:
    """Tests for _detect_sections() — required section detection."""

    def test_all_sections_present(self) -> None:
        """All 6 required sections detected."""
        from wos.plan.assess_plan import _detect_sections

        content = (
            "## Goal\n\nBuild the thing.\n\n"
            "## Scope\n\nMust/Won't.\n\n"
            "## Approach\n\nHow.\n\n"
            "## File Changes\n\n- Create: foo.py\n\n"
            "## Tasks\n\n- [ ] Do stuff\n\n"
            "## Validation\n\n- [ ] pytest passes\n"
        )
        result = _detect_sections(content)
        assert result == {
            "goal": True,
            "scope": True,
            "approach": True,
            "file_changes": True,
            "tasks": True,
            "validation": True,
            "all_present": True,
        }

    def test_missing_sections(self) -> None:
        """Missing sections reported as False, all_present is False."""
        from wos.plan.assess_plan import _detect_sections

        content = "## Goal\n\nBuild it.\n\n## Tasks\n\n- [ ] Do it\n"
        result = _detect_sections(content)
        assert result["goal"] is True
        assert result["tasks"] is True
        assert result["scope"] is False
        assert result["approach"] is False
        assert result["file_changes"] is False
        assert result["validation"] is False
        assert result["all_present"] is False

    def test_heading_level_insensitive(self) -> None:
        """Detects sections at any heading level."""
        from wos.plan.assess_plan import _detect_sections

        content = "### Goal\n\n#### Scope\n\n# Approach\n\n"
        result = _detect_sections(content)
        assert result["goal"] is True
        assert result["scope"] is True
        assert result["approach"] is True

    def test_file_changes_with_spaces(self) -> None:
        """'File Changes' heading detected (two words)."""
        from wos.plan.assess_plan import _detect_sections

        content = "## File Changes\n\n- Modify: foo.py\n"
        result = _detect_sections(content)
        assert result["file_changes"] is True

    def test_empty_content(self) -> None:
        """Empty content returns all False."""
        from wos.plan.assess_plan import _detect_sections

        result = _detect_sections("")
        assert result["all_present"] is False
        assert all(v is False for k, v in result.items() if k != "all_present")
```

- [ ] Run tests — expected: FAIL (function doesn't exist)
- [ ] Implement `_detect_sections`:

```python
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
    found = {key: False for key in _PLAN_SECTIONS}
    for line in content.split("\n"):
        stripped = line.strip()
        if not stripped.startswith("#"):
            continue
        heading_text = stripped.lstrip("#").strip().lower()
        for key, keyword in _PLAN_SECTIONS.items():
            if keyword in heading_text:
                found[key] = True
    found["all_present"] = all(found.values())
    return found
```

- [ ] Run tests — expected: all PASS
- [ ] Commit

### Task 3: Write tests for `_extract_file_changes` and implement

**Files:**
- Modify: `wos/plan/assess_plan.py`
- Modify: `tests/test_plan_assess.py`

- [ ] Add tests:

```python
class TestExtractFileChanges:
    """Tests for _extract_file_changes() — file path extraction."""

    def test_extracts_paths_from_file_changes_section(self) -> None:
        """Paths extracted from Create/Modify/Delete/Test lines."""
        from wos.plan.assess_plan import _extract_file_changes

        content = (
            "## File Changes\n"
            "- Create: `wos/plan/__init__.py`\n"
            "- Create: `wos/plan/assess_plan.py`\n"
            "- Modify: `wos/document.py`\n"
            "- Test: `tests/test_plan_assess.py`\n"
            "\n"
            "## Tasks\n"
            "- [ ] Task 1\n"
        )
        files = _extract_file_changes(content)
        assert "wos/plan/__init__.py" in files
        assert "wos/plan/assess_plan.py" in files
        assert "wos/document.py" in files
        assert "tests/test_plan_assess.py" in files

    def test_no_file_changes_section(self) -> None:
        """Returns empty list when no File Changes section exists."""
        from wos.plan.assess_plan import _extract_file_changes

        content = "## Goal\n\nBuild it.\n\n## Tasks\n\n- [ ] Do it\n"
        assert _extract_file_changes(content) == []

    def test_paths_without_backticks(self) -> None:
        """Paths without backticks still extracted."""
        from wos.plan.assess_plan import _extract_file_changes

        content = (
            "## File Changes\n"
            "- Create: wos/plan/__init__.py\n"
            "- Modify: wos/document.py\n"
            "\n"
            "## Tasks\n"
        )
        files = _extract_file_changes(content)
        assert "wos/plan/__init__.py" in files
        assert "wos/document.py" in files

    def test_stops_at_next_section(self) -> None:
        """Only parses files within File Changes section."""
        from wos.plan.assess_plan import _extract_file_changes

        content = (
            "## File Changes\n"
            "- Create: `wos/plan/assess_plan.py`\n"
            "\n"
            "## Tasks\n"
            "- Create: `not/a/file/change.py`\n"
        )
        files = _extract_file_changes(content)
        assert files == ["wos/plan/assess_plan.py"]

    def test_line_with_colon_and_range(self) -> None:
        """Paths with line ranges like 'file.py:123-145' extract just path."""
        from wos.plan.assess_plan import _extract_file_changes

        content = (
            "## File Changes\n"
            "- Modify: `wos/document.py:72-81`\n"
        )
        files = _extract_file_changes(content)
        assert files == ["wos/document.py"]
```

- [ ] Run tests — expected: FAIL
- [ ] Implement `_extract_file_changes`:

```python
_FILE_CHANGE_RE = re.compile(
    r"^- \s*(?:Create|Modify|Delete|Test):\s*`?([^`\s]+?)(?::\d[\d\-]*)?`?\s*$",
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
```

- [ ] Run tests — expected: all PASS
- [ ] Commit

### Task 4: Write tests for `_map_task_files` and `_find_overlaps`, then implement

**Files:**
- Modify: `wos/plan/assess_plan.py`
- Modify: `tests/test_plan_assess.py`

- [ ] Add tests:

```python
class TestMapTaskFiles:
    """Tests for _map_task_files() — task-to-file mapping."""

    def test_maps_files_under_task_headings(self) -> None:
        """Files listed under task headings mapped to those tasks."""
        from wos.plan.assess_plan import _map_task_files

        tasks = [
            {"index": 1, "title": "Create package", "completed": False, "sha": None},
            {"index": 2, "title": "Write tests", "completed": False, "sha": None},
        ]
        file_changes = ["wos/plan/__init__.py", "wos/plan/assess_plan.py", "tests/test_plan_assess.py"]
        content = (
            "### Task 1: Create package\n"
            "\n"
            "**Files:**\n"
            "- Create: `wos/plan/__init__.py`\n"
            "- Create: `wos/plan/assess_plan.py`\n"
            "\n"
            "### Task 2: Write tests\n"
            "\n"
            "**Files:**\n"
            "- Create: `tests/test_plan_assess.py`\n"
        )
        result = _map_task_files(tasks, file_changes, content)
        assert result["1"] == ["wos/plan/__init__.py", "wos/plan/assess_plan.py"]
        assert result["2"] == ["tests/test_plan_assess.py"]

    def test_flat_file_list_assigns_all(self) -> None:
        """Without per-task grouping, all files assigned to all tasks."""
        from wos.plan.assess_plan import _map_task_files

        tasks = [
            {"index": 1, "title": "Task A", "completed": False, "sha": None},
            {"index": 2, "title": "Task B", "completed": False, "sha": None},
        ]
        file_changes = ["foo.py", "bar.py"]
        content = (
            "## File Changes\n"
            "- Create: `foo.py`\n"
            "- Create: `bar.py`\n"
            "\n"
            "## Tasks\n"
            "- [ ] Task A\n"
            "- [ ] Task B\n"
        )
        result = _map_task_files(tasks, file_changes, content)
        assert result["1"] == ["foo.py", "bar.py"]
        assert result["2"] == ["foo.py", "bar.py"]

    def test_empty_tasks(self) -> None:
        """No tasks returns empty map."""
        from wos.plan.assess_plan import _map_task_files

        assert _map_task_files([], ["foo.py"], "content") == {}


class TestFindOverlaps:
    """Tests for _find_overlaps() — file overlap detection."""

    def test_no_overlaps(self) -> None:
        """Tasks with disjoint files return empty overlap list."""
        from wos.plan.assess_plan import _find_overlaps

        task_file_map = {"1": ["foo.py"], "2": ["bar.py"], "3": ["baz.py"]}
        assert _find_overlaps(task_file_map) == []

    def test_overlapping_tasks(self) -> None:
        """Tasks sharing files detected as overlapping pairs."""
        from wos.plan.assess_plan import _find_overlaps

        task_file_map = {"1": ["foo.py", "bar.py"], "2": ["bar.py"], "3": ["baz.py"]}
        overlaps = _find_overlaps(task_file_map)
        assert len(overlaps) == 1
        assert overlaps[0] == {"tasks": ["1", "2"], "shared_files": ["bar.py"]}

    def test_multiple_overlaps(self) -> None:
        """Multiple overlap pairs all reported."""
        from wos.plan.assess_plan import _find_overlaps

        task_file_map = {"1": ["a.py"], "2": ["a.py", "b.py"], "3": ["b.py"]}
        overlaps = _find_overlaps(task_file_map)
        assert len(overlaps) == 2

    def test_empty_map(self) -> None:
        """Empty map returns empty list."""
        from wos.plan.assess_plan import _find_overlaps

        assert _find_overlaps({}) == []
```

- [ ] Run tests — expected: FAIL
- [ ] Implement `_map_task_files` and `_find_overlaps`:

```python
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
```

- [ ] Run tests — expected: all PASS
- [ ] Commit

### Task 5: Write tests for `assess_file` and `scan_plans`, then implement

**Files:**
- Modify: `wos/plan/assess_plan.py`
- Modify: `tests/test_plan_assess.py`

Depends on: Tasks 1-4

- [ ] Add tests:

```python
class TestAssessFile:
    """Tests for assess_file() — full plan assessment."""

    def _write_plan(self, path, status="approved", tasks_content="", file_changes_content=""):
        """Helper to create a plan file."""
        content = (
            "---\n"
            f"name: Test Plan\n"
            f"description: A test plan\n"
            f"type: plan\n"
            f"status: {status}\n"
            "---\n"
            "\n"
            "## Goal\n\nBuild the thing.\n\n"
            "## Scope\n\nMust/Won't.\n\n"
            "## Approach\n\nHow.\n\n"
            f"## File Changes\n{file_changes_content}\n\n"
            f"## Tasks\n{tasks_content}\n\n"
            "## Validation\n\n- [ ] pytest passes\n"
        )
        path.write_text(content)

    def test_approved_plan_ready(self, tmp_path) -> None:
        """Approved plan with all sections reports ready."""
        from wos.plan.assess_plan import assess_file

        plan = tmp_path / "plan.md"
        self._write_plan(
            plan,
            tasks_content="- [ ] Task 1: Do stuff\n- [ ] Task 2: More stuff\n",
            file_changes_content="- Create: `foo.py`\n",
        )
        result = assess_file(str(plan))
        assert result["exists"] is True
        assert result["frontmatter"]["status"] == "approved"
        assert result["sections"]["all_present"] is True
        assert result["tasks"]["total"] == 2
        assert result["tasks"]["completed"] == 0
        assert result["tasks"]["pending"] == 2
        assert result["readiness"]["status_ok"] is True
        assert result["readiness"]["sections_complete"] is True
        assert result["readiness"]["has_pending_tasks"] is True

    def test_executing_plan_with_progress(self, tmp_path) -> None:
        """Executing plan reports correct completed/pending counts."""
        from wos.plan.assess_plan import assess_file

        plan = tmp_path / "plan.md"
        self._write_plan(
            plan,
            status="executing",
            tasks_content=(
                "- [x] Task 1: Done <!-- sha:abc1234 -->\n"
                "- [ ] Task 2: Pending\n"
                "- [ ] Task 3: Also pending\n"
            ),
        )
        result = assess_file(str(plan))
        assert result["frontmatter"]["status"] == "executing"
        assert result["tasks"]["total"] == 3
        assert result["tasks"]["completed"] == 1
        assert result["tasks"]["pending"] == 2
        assert result["tasks"]["items"][0]["sha"] == "abc1234"
        assert result["readiness"]["status_ok"] is True

    def test_draft_plan_not_ready(self, tmp_path) -> None:
        """Draft plan reports status_ok=False."""
        from wos.plan.assess_plan import assess_file

        plan = tmp_path / "plan.md"
        self._write_plan(plan, status="draft")
        result = assess_file(str(plan))
        assert result["readiness"]["status_ok"] is False
        assert any("draft" in i.lower() for i in result["readiness"]["issues"])

    def test_nonexistent_file(self) -> None:
        """Non-existent file returns exists=False."""
        from wos.plan.assess_plan import assess_file

        result = assess_file("/nonexistent/plan.md")
        assert result["exists"] is False
        assert result["frontmatter"] is None

    def test_parallel_eligibility(self, tmp_path) -> None:
        """Plan with 3+ non-overlapping tasks is parallel eligible."""
        from wos.plan.assess_plan import assess_file

        plan = tmp_path / "plan.md"
        content = (
            "---\n"
            "name: Parallel Plan\n"
            "description: A parallel plan\n"
            "type: plan\n"
            "status: approved\n"
            "---\n"
            "\n## Goal\n\nBuild.\n\n## Scope\n\nAll.\n\n"
            "## Approach\n\nParallel.\n\n"
            "## File Changes\n"
            "- Create: `a.py`\n- Create: `b.py`\n- Create: `c.py`\n\n"
            "### Task 1: A\n\n**Files:**\n- Create: `a.py`\n\n"
            "- [ ] Do A\n\n"
            "### Task 2: B\n\n**Files:**\n- Create: `b.py`\n\n"
            "- [ ] Do B\n\n"
            "### Task 3: C\n\n**Files:**\n- Create: `c.py`\n\n"
            "- [ ] Do C\n\n"
            "## Validation\n\n- [ ] Works\n"
        )
        plan.write_text(content)
        result = assess_file(str(plan))
        assert result["readiness"]["parallel_eligible"] is True
        assert result["file_changes"]["overlapping_tasks"] == []

    def test_not_parallel_with_overlaps(self, tmp_path) -> None:
        """Plan with overlapping files is not parallel eligible."""
        from wos.plan.assess_plan import assess_file

        plan = tmp_path / "plan.md"
        content = (
            "---\n"
            "name: Overlap Plan\n"
            "description: Overlapping\n"
            "type: plan\n"
            "status: approved\n"
            "---\n"
            "\n## Goal\n\nBuild.\n\n## Scope\n\nAll.\n\n"
            "## Approach\n\nSequential.\n\n"
            "## File Changes\n"
            "- Modify: `shared.py`\n- Create: `b.py`\n- Create: `c.py`\n\n"
            "### Task 1: A\n\n**Files:**\n- Modify: `shared.py`\n\n"
            "- [ ] Do A\n\n"
            "### Task 2: B\n\n**Files:**\n- Modify: `shared.py`\n- Create: `b.py`\n\n"
            "- [ ] Do B\n\n"
            "### Task 3: C\n\n**Files:**\n- Create: `c.py`\n\n"
            "- [ ] Do C\n\n"
            "## Validation\n\n- [ ] Works\n"
        )
        plan.write_text(content)
        result = assess_file(str(plan))
        assert result["readiness"]["parallel_eligible"] is False
        assert len(result["file_changes"]["overlapping_tasks"]) > 0


class TestScanPlans:
    """Tests for scan_plans() — find executing plans."""

    def _make_plan(self, path, name, status="draft"):
        path.write_text(
            f"---\nname: {name}\ndescription: A plan\n"
            f"type: plan\nstatus: {status}\n---\n"
            f"## Goal\n\nDo it.\n"
        )

    def test_finds_executing_plans(self, tmp_path) -> None:
        """Scan returns only plans with status: executing."""
        from wos.plan.assess_plan import scan_plans

        plans_dir = tmp_path / "docs" / "plans"
        plans_dir.mkdir(parents=True)
        self._make_plan(plans_dir / "a.md", "Plan A", status="executing")
        self._make_plan(plans_dir / "b.md", "Plan B", status="draft")
        self._make_plan(plans_dir / "c.md", "Plan C", status="executing")

        result = scan_plans(str(tmp_path))
        assert len(result["plans"]) == 2
        names = {p["name"] for p in result["plans"]}
        assert names == {"Plan A", "Plan C"}

    def test_empty_directory(self, tmp_path) -> None:
        """Empty plans directory returns empty list."""
        from wos.plan.assess_plan import scan_plans

        plans_dir = tmp_path / "docs" / "plans"
        plans_dir.mkdir(parents=True)
        result = scan_plans(str(tmp_path))
        assert result["plans"] == []

    def test_missing_directory(self, tmp_path) -> None:
        """Missing docs/plans returns empty list."""
        from wos.plan.assess_plan import scan_plans

        result = scan_plans(str(tmp_path))
        assert result["plans"] == []

    def test_skips_non_plan_docs(self, tmp_path) -> None:
        """Non-plan documents are ignored."""
        from wos.plan.assess_plan import scan_plans

        plans_dir = tmp_path / "docs" / "plans"
        plans_dir.mkdir(parents=True)
        (plans_dir / "design.md").write_text(
            "---\nname: Design\ndescription: A design\n"
            "type: design\n---\n# Design\n"
        )
        self._make_plan(plans_dir / "plan.md", "Real Plan", status="executing")

        result = scan_plans(str(tmp_path))
        assert len(result["plans"]) == 1

    def test_skips_index_files(self, tmp_path) -> None:
        """Index files are skipped."""
        from wos.plan.assess_plan import scan_plans

        plans_dir = tmp_path / "docs" / "plans"
        plans_dir.mkdir(parents=True)
        (plans_dir / "_index.md").write_text("# Plans Index\n")
        result = scan_plans(str(tmp_path))
        assert result["plans"] == []
```

- [ ] Run tests — expected: FAIL
- [ ] Implement `assess_file` and `scan_plans`:

```python
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
        missing = [k for k, v in sections.items() if k != "all_present" and not v]
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
```

  Also add the missing imports and `_read_file` helper to the top of the module:

```python
import os
```

```python
def _read_file(path: str) -> str:
    """Read file content as UTF-8 text."""
    with open(path, encoding="utf-8") as f:
        return f.read()
```

- [ ] Run full test suite — expected: all PASS

```bash
uv run python -m pytest tests/test_plan_assess.py -v
```

- [ ] Commit

### Task 6: Create CLI wrapper script

**Files:**
- Create: `skills/execute-plan/scripts/plan_assess.py`

Depends on: Task 5

- [ ] Create directory structure:

```bash
mkdir -p skills/execute-plan/scripts
```

- [ ] Write `skills/execute-plan/scripts/plan_assess.py`:

```python
#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""Assess plan document state for skill execution and resumption.

Usage:
    uv run skills/execute-plan/scripts/plan_assess.py --file PATH
    uv run skills/execute-plan/scripts/plan_assess.py --scan [--root DIR]
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

# Ensure `import wos` works whether pip-installed or run from plugin cache.
# Prefer CLAUDE_PLUGIN_ROOT env var (set by Claude Code for hooks/MCP);
# fall back to navigating from __file__ (required for skill-invoked scripts).
_env_root = os.environ.get("CLAUDE_PLUGIN_ROOT", "")
# skills/execute-plan/scripts/ → skills/execute-plan/ → skills/ → plugin root
_plugin_root = (
    Path(_env_root) if _env_root and os.path.isdir(_env_root)
    else Path(__file__).resolve().parent.parent.parent.parent
)
if str(_plugin_root) not in sys.path:
    sys.path.insert(0, str(_plugin_root))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Assess plan document state.",
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--file",
        help="Assess a single plan document",
    )
    group.add_argument(
        "--scan",
        action="store_true",
        help="Find all executing plans",
    )
    parser.add_argument(
        "--root",
        default=".",
        help="Project root directory (default: current directory)",
    )
    args = parser.parse_args()

    from wos.plan.assess_plan import assess_file, scan_plans

    if args.file:
        result = assess_file(args.file)
    else:
        root = str(Path(args.root).resolve())
        result = scan_plans(root)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
```

- [ ] Test the CLI wrapper:

```bash
uv run skills/execute-plan/scripts/plan_assess.py --file docs/plans/2026-03-11-execute-plan-skill-design.md
```

Expected: JSON output with plan assessment.

- [ ] Test scan mode:

```bash
uv run skills/execute-plan/scripts/plan_assess.py --scan --root .
```

Expected: JSON output (likely empty plans list since no executing plans).

- [ ] Commit

---

## Chunk 2: SKILL.md and Reference Files

### Task 7: Write SKILL.md

**Files:**
- Create: `skills/execute-plan/SKILL.md`

Depends on: Task 6

- [ ] Write `skills/execute-plan/SKILL.md` following the design spec's
  workflow (Steps 1-6), key instructions, and anti-pattern guards. Must
  include:
  - Frontmatter with metadata, argument-hint, user-invocable, references
    (including `../_shared/references/preflight.md`)
  - 6-step workflow: Load Plan, Approval Gate, Choose Execution Mode,
    Execute Tasks, Validate, Finish
  - Approval gate table (6 status values)
  - Task execution loop with three-tier verification reference
  - Key instructions (5 items)
  - Anti-pattern guards (5 items)

- [ ] Verify line count under 500:

```bash
wc -l skills/execute-plan/SKILL.md
```

- [ ] Commit

### Task 8: Write `references/execution-guide.md`

**Files:**
- Create: `skills/execute-plan/references/execution-guide.md`

- [ ] Write execution guide covering:
  - Task execution protocol (implement → verify → checkbox → SHA → commit)
  - Commit discipline (per-task, message format, chunk boundaries)
  - Three-tier verification model table (automated, structural, reasoning)
  - Verification protocol per type
  - Scope discipline
  - When to stop and ask

  Use WOS frontmatter:

```yaml
---
name: Execution Guide
description: Core execution loop guidance — task protocol, commit discipline, three-tier verification model
---
```

- [ ] Verify line count ~100:

```bash
wc -l skills/execute-plan/references/execution-guide.md
```

- [ ] Commit

### Task 9: Write `references/parallel-dispatch.md`

**Files:**
- Create: `skills/execute-plan/references/parallel-dispatch.md`

- [ ] Write parallel dispatch reference covering:
  - Eligibility criteria (3+ tasks, no overlaps, user opt-in)
  - File-boundary analysis interpretation
  - Wave-based execution pattern
  - Abstract dispatch pattern (worktree isolation, full task context)
  - 3-status protocol (DONE, NEEDS_HELP, BLOCKED)
  - Merge and conflict escalation
  - No platform-specific API calls

  Use WOS frontmatter:

```yaml
---
name: Parallel Dispatch
description: Platform-agnostic parallel execution protocol — eligibility, file boundaries, status protocol, merge
---
```

- [ ] Verify line count ~100:

```bash
wc -l skills/execute-plan/references/parallel-dispatch.md
```

- [ ] Commit

### Task 10: Write `references/recovery-patterns.md`

**Files:**
- Create: `skills/execute-plan/references/recovery-patterns.md`

- [ ] Write recovery patterns reference covering:
  - Task splitting on partial completion
  - Retry protocol (2 retries / 3 total attempts)
  - Escalation format (tried, evidence, options, recommendation)
  - Git-based rollback using commit SHAs
  - Task-pass / plan-fail handling (add tasks, don't fail plan)
  - Transient vs. non-transient classification

  Use WOS frontmatter:

```yaml
---
name: Recovery Patterns
description: Failure handling — task splitting, retry protocol, escalation, git rollback, task-pass/plan-fail
---
```

- [ ] Verify line count ~90:

```bash
wc -l skills/execute-plan/references/recovery-patterns.md
```

- [ ] Commit

### Task 11: Write `references/multi-session-resumption.md`

**Files:**
- Create: `skills/execute-plan/references/multi-session-resumption.md`

- [ ] Write multi-session resumption reference covering:
  - Session start protocol (5-step: script → pending task → git log → SHA confirm → resume)
  - Plan file as source of truth, git as secondary
  - No conversation context reliance
  - Orientation sequence
  - Stale executing state detection
  - SHA mismatch handling

  Use WOS frontmatter:

```yaml
---
name: Multi-Session Resumption
description: Session recovery protocol — plan file reading, SHA verification, stale state detection
---
```

- [ ] Verify line count ~80:

```bash
wc -l skills/execute-plan/references/multi-session-resumption.md
```

- [ ] Commit

---

## Chunk 3: Validation and Cleanup

### Task 12: Run full validation

**Files:**
- None (verification only)

Depends on: Tasks 1-11

- [ ] Run full test suite:

```bash
uv run python -m pytest tests/ -v
```

Expected: ALL PASS (including existing tests).

- [ ] Run linter:

```bash
ruff check wos/plan/ tests/test_plan_assess.py skills/execute-plan/scripts/plan_assess.py
```

- [ ] Run WOS audit:

```bash
uv run scripts/audit.py --root .
```

Expected: No new failures from execute-plan files.

- [ ] Verify SKILL.md under 500 lines:

```bash
wc -l skills/execute-plan/SKILL.md
```

- [ ] Verify entry script works end-to-end:

```bash
uv run skills/execute-plan/scripts/plan_assess.py --file docs/plans/2026-03-11-execute-plan-skill-design.md
```

- [ ] Update this plan's status to `executing` (if not already)
- [ ] Commit any fixes

---

## Validation

- [ ] `uv run python -m pytest tests/ -v` — all tests pass (existing + new)
- [ ] `ruff check wos/plan/ tests/test_plan_assess.py` — no lint errors
- [ ] `uv run scripts/audit.py --root .` — no new failures
- [ ] `wc -l skills/execute-plan/SKILL.md` — under 500 lines
- [ ] Entry script `--file` mode returns valid JSON with all expected keys
- [ ] Entry script `--scan` mode returns valid JSON
- [ ] All 13 issue #160 acceptance criteria addressed
- [ ] All 7 design addition criteria addressed
