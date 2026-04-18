"""SkillDocument dataclass and skill quality auditing.

Provides the SkillDocument dataclass for reading and validating SKILL.md files,
along with module-level functions for skill size and metadata checks.

SkillDocument extends Document and aligns with the agentskills.io specification:
required name and description, optional license, compatibility, and allowed-tools.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Tuple

from check.document import Document

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
_VAGUE_PHRASES = (
    "helps with",
    "processes data",
    "handles stuff",
    "deals with",
    "manages things",
    "works with stuff",
)
_DESCRIPTION_CAP = 1024
_DESCRIPTION_COMBINED_CAP = 1536
_SUBSTITUTION_RE = re.compile(r"\$ARGUMENTS(?:\[\d+\])?|\$[0-9]\b")
_VAGUE_NAME_TOKENS = frozenset({
    "helper", "utils", "util", "tools", "tool",
    "thing", "things", "stuff", "common", "misc",
})


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


def _check_description(
    desc: str,
    file_str: str,
    when_to_use: Optional[str] = None,
) -> List[dict]:
    issues: List[dict] = []

    # Cap enforcement — FAIL.
    # Platform cap: description ≤ 1024 chars.
    # Claude Code: description + when_to_use combined ≤ 1536 chars.
    if when_to_use:
        combined = len(desc) + len(when_to_use)
        if combined > _DESCRIPTION_COMBINED_CAP:
            issues.append({
                "file": file_str,
                "issue": (
                    f"description + when_to_use combined exceeds "
                    f"{_DESCRIPTION_COMBINED_CAP} characters ({combined})"
                ),
                "severity": "fail",
            })
    else:
        if len(desc) > _DESCRIPTION_CAP:
            issues.append({
                "file": file_str,
                "issue": (
                    f"skill description exceeds {_DESCRIPTION_CAP} "
                    f"characters ({len(desc)}); split into when_to_use "
                    f"to use the combined {_DESCRIPTION_COMBINED_CAP} cap"
                ),
                "severity": "fail",
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

    for phrase in _VAGUE_PHRASES:
        if phrase in desc_lower:
            issues.append({
                "file": file_str,
                "issue": (
                    f"skill description uses vague phrasing "
                    f"('{phrase}'); name a specific capability"
                ),
                "severity": "warn",
            })
            break

    return issues


def _check_substitution_usage(
    argument_hint: object,
    body: str,
    file_str: str,
) -> List[dict]:
    """Warn when ``argument-hint`` is set but body uses no substitution.

    When ``argument-hint`` is declared, Claude Code expects the body to
    consume the argument via ``$ARGUMENTS``, ``$ARGUMENTS[N]``, or ``$N``.
    Without a substitution, Claude Code falls back to appending
    ``ARGUMENTS: <value>`` at the end of the rendered skill, putting
    the argument in the wrong position relative to the workflow.
    """
    if not isinstance(argument_hint, str) or not argument_hint.strip():
        return []
    if _SUBSTITUTION_RE.search(body):
        return []
    return [{
        "file": file_str,
        "issue": (
            "argument-hint is set but body uses no $ARGUMENTS / $N "
            "substitution; argument will be appended as "
            "'ARGUMENTS: <value>' at end of skill, putting it in the "
            "wrong position for the workflow"
        ),
        "severity": "warn",
    }]


def _check_gerund_naming(name: str, file_str: str) -> List[dict]:
    """Warn on vague names and recommend gerund/agent-suffix naming.

    Vague names (``helper``, ``utils``, ``tools``, ``thing``, etc.) provide
    no triggering signal. Names that don't end in ``-ing`` or ``-er``
    miss the platform-recommended gerund or agent-noun pattern
    (``processing-pdfs``, ``analyzing-spreadsheets``, ``checker``).
    """
    issues: List[dict] = []
    segments = name.split("-")
    for seg in segments:
        if seg in _VAGUE_NAME_TOKENS:
            issues.append({
                "file": file_str,
                "issue": (
                    f"skill name contains vague token '{seg}'; "
                    f"name a specific capability "
                    f"(e.g. 'processing-pdfs', 'analyzing-spreadsheets')"
                ),
                "severity": "warn",
            })
            return issues
    if not any(seg.endswith("ing") or seg.endswith("er") for seg in segments):
        issues.append({
            "file": file_str,
            "issue": (
                f"skill name '{name}' is not in gerund or agent-noun form "
                f"(e.g. 'processing-pdfs', 'checker'); style suggestion only"
            ),
            "severity": "warn",
        })
    return issues


def _check_allowed_tools(value: object, file_str: str) -> List[dict]:
    """Validate the shape of the ``allowed-tools`` frontmatter field.

    Canonical forms (per Claude Code spec):

    - YAML block list (parsed as a Python list)
    - Space-separated string (``"Grep Read"``)
    - Inline YAML list (``"[Grep, Read]"`` — stored as a string by the
      stdlib parser, but real YAML parses it as a list)

    The silent-breakage case is a comma-separated string like ``"Grep, Read"``
    which YAML parses as one literal value, so the field does nothing.
    """
    if value is None:
        return []
    if isinstance(value, list):
        return []
    if not isinstance(value, str):
        return []

    stripped = value.strip()
    if stripped.startswith("[") and stripped.endswith("]"):
        return []
    if "," in stripped:
        return [{
            "file": file_str,
            "issue": (
                "allowed-tools is comma-separated as a string "
                f"({value!r}); YAML parses this as one literal value. "
                "Use space-separated (Grep Read) or YAML list "
                "([Grep, Read] / block list)."
            ),
            "severity": "fail",
        }]
    return []


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


# Match real Windows paths, not escape sequences inside string literals.
# Requires one of: drive letter prefix, ./ or ../ prefix, or a backslash
# immediately followed by a name with a recognizable file extension.
_WINDOWS_PATH_RE = re.compile(
    r"(?:[A-Za-z]:\\\S+"
    r"|\.{1,2}\\[A-Za-z0-9_./-]+"
    r"|[A-Za-z0-9_-]+(?:\\[A-Za-z0-9_-]+)*\\[A-Za-z0-9_-]+\.[A-Za-z]{1,5}\b)"
)


def _iter_code_segments(body: str):
    """Yield (segment_text, line_no) for fenced blocks and inline code spans.

    Fenced blocks: between ``` markers (``` may include a language hint).
    Inline code: text between single backticks on a line.
    """
    in_fence = False
    fence_buf: List[str] = []
    fence_start_line = 0

    for line_no, line in enumerate(body.splitlines(), start=1):
        stripped = line.strip()
        if stripped.startswith("```"):
            if in_fence:
                yield ("\n".join(fence_buf), fence_start_line)
                fence_buf = []
                in_fence = False
            else:
                in_fence = True
                fence_start_line = line_no
            continue
        if in_fence:
            fence_buf.append(line)
            continue

        # Inline code spans on prose lines.
        idx = 0
        while True:
            tick = line.find("`", idx)
            if tick == -1:
                break
            end = line.find("`", tick + 1)
            if end == -1:
                break
            yield (line[tick + 1:end], line_no)
            idx = end + 1


def _check_body_paths(body: str, file_str: str) -> List[dict]:
    """Flag Windows-style backslash path separators in code segments.

    Skips escape sequences that show up in regex / format strings
    (``\\n``, ``\\t``, ``\\\\``) by requiring the backslash to be preceded
    by an identifier character or a drive letter / dot pattern that matches
    a real filesystem path.
    """
    issues: List[dict] = []
    seen_lines: set[int] = set()

    for segment, line_no in _iter_code_segments(body):
        if line_no in seen_lines:
            continue
        for match in _WINDOWS_PATH_RE.finditer(segment):
            issues.append({
                "file": file_str,
                "issue": (
                    f"line {line_no}: Windows-style path separator in "
                    f"code segment ('{match.group(0)}'); use forward "
                    f"slashes for portability"
                ),
                "severity": "fail",
            })
            seen_lines.add(line_no)
            break

    return issues


def _check_body_lines(body: str, file_str: str) -> List[dict]:
    raw_lines = sum(1 for line in body.splitlines() if line.strip())
    if raw_lines > 500:
        return [{
            "file": file_str,
            "issue": f"SKILL.md body exceeds 500 non-blank lines ({raw_lines})",
            "severity": "warn",
        }]
    return []


_TOC_HEADING_RE = re.compile(
    r"^\s*##+\s*(table of contents|contents|toc)\b",
    re.IGNORECASE | re.MULTILINE,
)


def _check_reference_depth(skill_dir: Path, file_str: str) -> List[dict]:
    """Warn on reference files nested more than one level deep.

    Canonical progressive disclosure loads a single level under
    ``references/``. Deeper nesting makes on-demand loading awkward
    because Claude does partial reads of nested files.
    """
    issues: List[dict] = []
    refs_dir = skill_dir / "references"
    if not refs_dir.is_dir():
        return issues
    for path in sorted(refs_dir.rglob("*.md")):
        relative = path.relative_to(refs_dir)
        # One level means len(parts) == 1 (file directly in references/).
        # Two levels: references/foo/bar.md → parts == ("foo", "bar.md") → len 2.
        if len(relative.parts) > 1:
            issues.append({
                "file": file_str,
                "issue": (
                    f"reference file {relative} is nested more than 1 level "
                    f"under references/; flatten for clean on-demand loading"
                ),
                "severity": "warn",
            })
    return issues


def _check_reference_toc(skill_dir: Path, file_str: str) -> List[dict]:
    """Warn on reference files over 100 non-blank lines without a TOC.

    Long references without a table of contents force Claude to scan
    the whole file to find the relevant section. A TOC (``## Table of
    Contents``, ``## Contents``, or ``## TOC``) near the top indexes
    the sections so partial loads land in the right spot.
    """
    issues: List[dict] = []
    refs_dir = skill_dir / "references"
    if not refs_dir.is_dir():
        return issues
    for path in sorted(refs_dir.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        body = strip_frontmatter(text)
        non_blank = sum(1 for line in body.splitlines() if line.strip())
        if non_blank <= 100:
            continue
        head = "\n".join(body.splitlines()[:20])
        if _TOC_HEADING_RE.search(head):
            continue
        relative = path.relative_to(skill_dir)
        issues.append({
            "file": file_str,
            "issue": (
                f"reference file {relative} has {non_blank} non-blank "
                f"lines but no Table of Contents heading in the first 20 "
                f"lines; add one so partial loads find their section"
            ),
            "severity": "warn",
        })
    return issues


# ── SkillDocument dataclass ─────────────────────────────────────────


@Document.register("skill")
@dataclass
class SkillDocument(Document):
    """A parsed SKILL.md skill definition.

    Extends Document with agentskills.io specification fields:
    optional license, compatibility, and allowed_tools. Content is
    stored in the inherited ``content`` field.
    """

    license: Optional[str] = None
    compatibility: Optional[str] = None
    allowed_tools: Optional[str] = None

    def __post_init__(self) -> None:
        # Extract agentskills spec fields from meta (they land there
        # because they're not in Document._KNOWN_KEYS)
        if self.license is None:
            self.license = self.meta.get("license")
        if self.compatibility is None:
            self.compatibility = self.meta.get("compatibility")
        if self.allowed_tools is None:
            self.allowed_tools = self.meta.get("allowed-tools")

    @classmethod
    def parse(cls, skill_dir: Path) -> Optional[SkillDocument]:
        """Read SKILL.md from skill_dir and return a SkillDocument instance.

        Delegates to Document.parse() for frontmatter extraction and
        routing. Returns None if SKILL.md doesn't exist or is unparseable.
        """
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            return None
        text = skill_md.read_text(encoding="utf-8")
        try:
            doc = Document.parse(str(skill_md), text)
        except ValueError:
            return None
        return doc if isinstance(doc, SkillDocument) else None

    def size(self, skill_dir: Optional[Path] = None) -> dict:
        """Return size metrics for this skill.

        Reads the body (``content``) and optionally reads reference files
        from ``skill_dir/references/*.md``.

        Args:
            skill_dir: Directory containing this skill. When provided,
                reference files are also measured.

        Returns:
            Dict with keys: name, skill_lines, ref_lines, total_lines,
            words, files.
        """
        skill_lines = count_instruction_lines(self.content)
        skill_words = len(self.content.split())
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

        summary_name = self.name if self.name else Path(self.path).parent.name

        return {
            "name": summary_name,
            "skill_lines": skill_lines,
            "ref_lines": ref_lines,
            "total_lines": total_lines,
            "words": total_words,
            "files": files,
        }

    def issues(self, root: Path, **_: object) -> List[dict]:
        """Return base issues plus skill-specific checks.

        Base checks: name and description non-empty.
        Skill checks: name format, gerund/vague-name style, description
        quality (cap, third person, vague phrasing), allowed-tools shape,
        argument-hint substitution usage, Windows-style paths in code
        segments, ALL-CAPS directive density, raw body line count.

        Args:
            root: Project root directory (passed to base issues()).

        Returns:
            List of issue dicts with keys: file, issue, severity.
        """
        result = super().issues(root)
        if self.name:
            result.extend(_check_name(self.name, self.path))
            result.extend(_check_gerund_naming(self.name, self.path))
        if self.description:
            when_to_use = self.meta.get("when_to_use") or self.meta.get("when-to-use")
            when_to_use_str = when_to_use if isinstance(when_to_use, str) else None
            result.extend(_check_description(
                self.description, self.path, when_to_use=when_to_use_str,
            ))
        result.extend(_check_allowed_tools(self.allowed_tools, self.path))
        result.extend(_check_substitution_usage(
            self.meta.get("argument-hint"), self.content, self.path,
        ))
        result.extend(_check_body_paths(self.content, self.path))
        result.extend(_check_directives(self.content, self.path))
        result.extend(_check_body_lines(self.content, self.path))
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

        skill = SkillDocument.parse(entry)
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
    skill = SkillDocument.parse(skill_dir)
    if skill is None:
        return []
    return skill.issues(skill_dir)
