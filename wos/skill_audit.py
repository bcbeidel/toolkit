"""Skill size auditing — measure instruction density of skill files.

Provides functions to strip frontmatter, count instruction lines, and
check skill directories for size thresholds.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import List, Tuple

_NAME_RE = re.compile(r"^[a-z0-9-]+$")
_XML_TAG_RE = re.compile(r"<[a-zA-Z]")
_RESERVED_WORDS = ("anthropic", "claude")
_SECOND_PERSON_PATTERNS = (
    "you can",
    "you should",
    "you will",
    "your ",
    "i can",
    "i will",
    "this skill should be used when",
)


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


def parse_skill_meta(text: str) -> dict:
    """Extract name and description from SKILL.md frontmatter.

    Handles YAML ``>`` block scalars for multi-line descriptions.
    Returns dict with ``name`` and ``description`` keys (None if absent).
    """
    if not text.startswith("---"):
        return {"name": None, "description": None}

    close = text.find("\n---", 3)
    if close == -1:
        return {"name": None, "description": None}

    yaml_text = text[4:close]

    name = None
    description = None

    name_match = re.search(r"^name:\s*(.+)$", yaml_text, re.MULTILINE)
    if name_match:
        name = name_match.group(1).strip().strip('"').strip("'")

    desc_match = re.search(r"^description:\s*(.*)$", yaml_text, re.MULTILINE)
    if desc_match:
        value = desc_match.group(1).strip()
        if value in (">", "|", ">-", "|-"):
            lines = yaml_text.split("\n")
            desc_parts: List[str] = []
            capture = False
            for line in lines:
                if line.strip().startswith("description:"):
                    capture = True
                    continue
                if capture:
                    if line.startswith("  ") or line.startswith("\t"):
                        desc_parts.append(line.strip())
                    else:
                        break
            description = " ".join(desc_parts)
        else:
            description = value.strip('"').strip("'")

    return {"name": name, "description": description}


def check_skill_meta(skill_dir: Path) -> List[dict]:
    """Validate SKILL.md frontmatter and structure conventions.

    Returns a list of issues in standard validator format.
    """
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return []

    raw = skill_md.read_text(encoding="utf-8")
    meta = parse_skill_meta(raw)
    file_str = str(skill_md)
    issues: List[dict] = []

    # Name checks
    name = meta.get("name")
    if name:
        if not _NAME_RE.match(name):
            issues.append({
                "file": file_str,
                "issue": (
                    f"skill name '{name}' must be lowercase letters, "
                    f"numbers, and hyphens only"
                ),
                "severity": "fail",
            })
        if len(name) > 64:
            issues.append({
                "file": file_str,
                "issue": f"skill name exceeds 64 characters ({len(name)})",
                "severity": "fail",
            })
        for word in _RESERVED_WORDS:
            if word in name:
                issues.append({
                    "file": file_str,
                    "issue": f"skill name contains reserved word '{word}'",
                    "severity": "fail",
                })

    # Description checks
    desc = meta.get("description")
    if desc:
        if len(desc) > 1024:
            issues.append({
                "file": file_str,
                "issue": (
                    f"skill description exceeds 1024 characters ({len(desc)})"
                ),
                "severity": "warn",
            })
        if _XML_TAG_RE.search(desc):
            issues.append({
                "file": file_str,
                "issue": "skill description contains XML tags",
                "severity": "warn",
            })
        desc_lower = desc.lower()
        for pattern in _SECOND_PERSON_PATTERNS:
            if pattern in desc_lower:
                issues.append({
                    "file": file_str,
                    "issue": (
                        f"skill description may not use third person "
                        f"(found '{pattern}')"
                    ),
                    "severity": "warn",
                })
                break

    # Raw line count
    body = strip_frontmatter(raw)
    raw_lines = sum(1 for line in body.splitlines() if line.strip())
    if raw_lines > 500:
        issues.append({
            "file": file_str,
            "issue": (
                f"SKILL.md body exceeds 500 non-blank lines ({raw_lines})"
            ),
            "severity": "warn",
        })

    return issues
