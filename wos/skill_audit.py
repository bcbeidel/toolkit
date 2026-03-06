"""Skill size auditing — measure instruction density of skill files.

Provides functions to strip frontmatter, count instruction lines, and
check skill directories for size thresholds.
"""

from __future__ import annotations

from pathlib import Path
from typing import List, Tuple


def strip_frontmatter(text: str) -> str:
    """Remove YAML frontmatter (--- delimited) from text.

    If text starts with ``---``, finds the next ``---`` after position 3
    and returns everything after it.  If no closing delimiter is found,
    returns the text unchanged.
    """
    if not text.startswith("---"):
        return text
    close = text.find("\n---", 3)
    if close == -1:
        return text
    # Skip past the \n--- and the newline that follows it
    after = close + 4
    if after < len(text) and text[after] == "\n":
        after += 1
    return text[after:]


def count_instruction_lines(text: str) -> int:
    """Count non-empty, non-structural lines in markdown text.

    Excludes blank lines, headers, code fences, table separators,
    and horizontal rules.  Everything else counts (bullets, prose,
    table data rows, numbered steps, code inside fences).
    """
    count = 0
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("#"):
            continue
        if stripped.startswith("```"):
            continue
        if stripped.startswith("|") and set(stripped) <= set("|-: "):
            continue
        if set(stripped) <= set("-* _"):
            continue
        count += 1
    return count


def check_skill_sizes(
    skills_dir: Path, max_lines: int = 200
) -> Tuple[List[dict], List[dict]]:
    """Measure instruction density of each skill directory.

    Walks *skills_dir* looking for subdirectories that contain a
    ``SKILL.md`` file.  Directories whose name starts with ``_`` are
    skipped.

    Returns a tuple of ``(summaries, issues)`` where each summary is a
    dict with keys ``name``, ``skill_lines``, ``ref_lines``,
    ``total_lines``, ``words``, ``files`` and each issue follows the
    standard validator dict shape (``file``, ``issue``, ``severity``).
    """
    summaries: List[dict] = []
    issues: List[dict] = []

    if not skills_dir.is_dir():
        return summaries, issues

    for entry in sorted(skills_dir.iterdir()):
        if not entry.is_dir():
            continue
        if entry.name.startswith("_"):
            continue

        skill_md = entry / "SKILL.md"
        if not skill_md.exists():
            continue

        # Measure SKILL.md
        raw_skill = skill_md.read_text(encoding="utf-8")
        body_skill = strip_frontmatter(raw_skill)
        skill_lines = count_instruction_lines(body_skill)
        skill_words = len(body_skill.split())
        files = [str(skill_md)]

        # Measure references/*.md
        ref_lines = 0
        ref_words = 0
        for ref_path in sorted(entry.rglob("references/*.md")):
            raw_ref = ref_path.read_text(encoding="utf-8")
            body_ref = strip_frontmatter(raw_ref)
            ref_lines += count_instruction_lines(body_ref)
            ref_words += len(body_ref.split())
            files.append(str(ref_path))

        total_lines = skill_lines + ref_lines
        total_words = skill_words + ref_words

        summary = {
            "name": entry.name,
            "skill_lines": skill_lines,
            "ref_lines": ref_lines,
            "total_lines": total_lines,
            "words": total_words,
            "files": files,
        }
        summaries.append(summary)

        if max_lines > 0 and total_lines > max_lines:
            issues.append({
                "file": str(skill_md),
                "issue": (
                    f"skill '{entry.name}' has {total_lines} instruction "
                    f"lines (threshold: {max_lines})"
                ),
                "severity": "warn",
            })

    return summaries, issues
