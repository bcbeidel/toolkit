"""Skill dataclass and skill quality auditing.

Provides the Skill dataclass for reading and validating SKILL.md files,
along with module-level functions for skill size and metadata checks.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Tuple

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
_RIGID_DIRECTIVE_RE = re.compile(r"\b(?:MUST|NEVER|ALWAYS|REQUIRED|FORBIDDEN)\b")
_RIGID_DIRECTIVE_THRESHOLD = 3


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



def _check_name(name: str, file_str: str) -> List[dict]:
    issues: List[dict] = []
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
    return issues


def _check_description(desc: str, file_str: str) -> List[dict]:
    issues: List[dict] = []
    if len(desc) > 1024:
        issues.append({
            "file": file_str,
            "issue": f"skill description exceeds 1024 characters ({len(desc)})",
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
    return issues


def _check_directives(body: str, file_str: str) -> List[dict]:
    directive_matches = _RIGID_DIRECTIVE_RE.findall(body)
    if len(directive_matches) >= _RIGID_DIRECTIVE_THRESHOLD:
        return [{
            "file": file_str,
            "issue": (
                f"SKILL.md body has {len(directive_matches)} ALL-CAPS "
                f"directives (MUST/NEVER/ALWAYS/etc.) — consider "
                f"explaining rationale instead of rigid commands"
            ),
            "severity": "warn",
        }]
    return []


def _check_body_lines(body: str, file_str: str) -> List[dict]:
    raw_lines = sum(1 for line in body.splitlines() if line.strip())
    if raw_lines > 500:
        return [{
            "file": file_str,
            "issue": f"SKILL.md body exceeds 500 non-blank lines ({raw_lines})",
            "severity": "warn",
        }]
    return []


# ── Skill dataclass ────────────────────────────────────────────────


@dataclass
class Skill:
    """Represents a parsed SKILL.md skill definition.

    Fields:
        path:        Path to the SKILL.md file (as string).
        name:        Skill name from frontmatter (None if absent).
        description: Skill description from frontmatter (None if absent).
        body:        Body text with frontmatter stripped.
    """

    path: str
    name: Optional[str]
    description: Optional[str]
    body: str

    @classmethod
    def parse(cls, skill_dir: Path) -> Optional[Skill]:
        """Read SKILL.md from skill_dir and return a Skill instance.

        Returns None if no SKILL.md exists in the directory.
        """
        from wos.frontmatter import parse_frontmatter

        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            return None
        raw = skill_md.read_text(encoding="utf-8")
        try:
            fm, body = parse_frontmatter(raw)
            name = str(fm["name"]) if fm.get("name") is not None else None
            description = (
                str(fm["description"]) if fm.get("description") is not None else None
            )
        except ValueError:
            body = strip_frontmatter(raw)
            name = None
            description = None
        return cls(
            path=str(skill_md),
            name=name,
            description=description,
            body=body,
        )

    def size(self, skill_dir: Optional[Path] = None) -> dict:
        """Return size metrics for this skill.

        Reads the SKILL.md body (already parsed) and optionally reads
        reference files from ``skill_dir/references/*.md``.

        Args:
            skill_dir: Directory containing this skill. When provided,
                reference files are also measured.

        Returns:
            Dict with keys: name, skill_lines, ref_lines, total_lines,
            words, files.
        """
        skill_lines = count_instruction_lines(self.body)
        skill_words = len(self.body.split())
        files = [self.path]

        ref_lines = 0
        ref_words = 0
        if skill_dir is not None:
            for ref_path in sorted(skill_dir.rglob("references/*.md")):
                raw_ref = ref_path.read_text(encoding="utf-8")
                body_ref = strip_frontmatter(raw_ref)
                ref_lines += count_instruction_lines(body_ref)
                ref_words += len(body_ref.split())
                files.append(str(ref_path))

        total_lines = skill_lines + ref_lines
        total_words = skill_words + ref_words

        # Derive a name for the summary from the path if name is absent
        summary_name = self.name
        if summary_name is None:
            summary_name = Path(self.path).parent.name

        return {
            "name": summary_name,
            "skill_lines": skill_lines,
            "ref_lines": ref_lines,
            "total_lines": total_lines,
            "words": total_words,
            "files": files,
        }

    def issues(self, **_: object) -> List[dict]:
        """Return validation issues for this skill's metadata and body.

        Checks name format, description quality, ALL-CAPS directive density,
        and raw body line count.

        Returns:
            List of issue dicts with keys: file, issue, severity.
        """
        result: List[dict] = []
        if self.name:
            result.extend(_check_name(self.name, self.path))
        if self.description:
            result.extend(_check_description(self.description, self.path))
        result.extend(_check_directives(self.body, self.path))
        result.extend(_check_body_lines(self.body, self.path))
        return result


# ── Module-level orchestration functions ──────────────────────────


def check_skill_sizes(
    skills_dir: Path, max_lines: int = 500
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

        skill = Skill.parse(entry)
        if skill is None:
            continue

        summary = skill.size(skill_dir=entry)
        # check_skill_sizes uses directory name as the summary name
        summary["name"] = entry.name
        summaries.append(summary)

        if max_lines > 0 and summary["total_lines"] > max_lines:
            issues.append({
                "file": skill.path,
                "issue": (
                    f"skill '{entry.name}' has {summary['total_lines']} instruction "
                    f"lines (threshold: {max_lines})"
                ),
                "severity": "warn",
            })

    return summaries, issues


def check_skill_meta(skill_dir: Path) -> List[dict]:
    """Validate SKILL.md frontmatter and structure conventions.

    Returns a list of issues in standard validator format.
    """
    skill = Skill.parse(skill_dir)
    if skill is None:
        return []
    return skill.issues()
