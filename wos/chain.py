"""Chain manifest parsing and structural validation.

Provides ChainDocument — a Document subclass for *.chain.md manifests —
and validate_chain() which parses and validates a manifest in one call.

Each issue dict has keys: file, issue, severity.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

from wos.document import Document, parse_document

# ── Step table helpers ─────────────────────────────────────────────


def _is_separator_row(cells: List[str]) -> bool:
    """Return True if this is a markdown table separator row (e.g. |---|---|)."""
    return bool(cells) and all(
        bool(c) and all(ch in "-: " for ch in c) for c in cells
    )


_HEADER_KEYWORDS = {"step", "skill", "input contract", "output contract", "gate"}


def _is_header_row(cells: List[str]) -> bool:
    """Return True if this row looks like a table header."""
    lower = {c.lower() for c in cells}
    return sum(1 for kw in _HEADER_KEYWORDS if kw in lower) >= 3


def _norm_cell(value: str) -> str:
    """Normalize em-dash / en-dash placeholder cells to empty string."""
    return "" if value.strip() in ("—", "–", "-") else value.strip()


def _parse_steps_table(body: str, manifest_path: Path) -> List[dict]:
    """Parse the ## Steps pipe table from the chain manifest body.

    Args:
        body: Markdown body content after frontmatter.
        manifest_path: Path used in error messages.

    Returns:
        List of step dicts with keys: step, skill, input_contract,
        output_contract, gate.

    Raises:
        ValueError: If no ## Steps section is found.
    """
    lines = body.splitlines()

    steps_start: Optional[int] = None
    for i, line in enumerate(lines):
        if line.strip().lower().startswith("## steps"):
            steps_start = i
            break

    if steps_start is None:
        raise ValueError(f"No '## Steps' section found in {manifest_path}")

    steps: List[dict] = []
    in_table = False

    for line in lines[steps_start + 1:]:
        stripped = line.strip()

        if not stripped:
            if in_table:
                break
            continue

        if not stripped.startswith("|"):
            if in_table:
                break
            continue

        cells = [c.strip() for c in stripped.split("|") if c.strip()]

        if not cells:
            continue
        if _is_separator_row(cells):
            in_table = True
            continue
        if not in_table and _is_header_row(cells):
            in_table = True
            continue
        if not in_table:
            continue

        while len(cells) < 5:
            cells.append("")

        steps.append({
            "step": _norm_cell(cells[0]),
            "skill": _norm_cell(cells[1]),
            "input_contract": _norm_cell(cells[2]),
            "output_contract": _norm_cell(cells[3]),
            "gate": _norm_cell(cells[4]),
        })

    return steps


# ── ChainDocument ──────────────────────────────────────────────────


@Document.register("chain")
@dataclass
class ChainDocument(Document):
    """A chain manifest document with parsed step list and structural validation.

    Adds a ``steps`` field (parsed from the ## Steps table in content)
    and overrides ``issues()`` to check skill existence, termination
    condition, and step-sequence cycles.
    """

    steps: List[dict] = field(default_factory=list, init=False)

    def __post_init__(self) -> None:
        self._steps_error: Optional[str] = None
        try:
            self.steps = _parse_steps_table(self.content, Path(self.path))
        except ValueError as exc:
            self._steps_error = str(exc)

    @property
    def goal(self) -> str:
        """The chain's termination condition (from frontmatter ``goal`` field)."""
        return self.meta.get("goal") or ""

    @property
    def negative_scope(self) -> str:
        """What the chain explicitly does not handle."""
        return self.meta.get("negative-scope") or ""

    def issues(
        self,
        root: Path,
        skills_dirs: Optional[List[Path]] = None,
        **_: object,
    ) -> List[dict]:
        """Return base issues plus chain-specific structural checks.

        Adds: steps-table parse error, skill existence, termination
        condition, and cycle detection.

        Args:
            root: Project root directory (used by base class for related paths).
            skills_dirs: Directories to search for skill subdirectories.
                Defaults to ``[root / "skills"]`` if not provided.

        Returns:
            List of issue dicts with keys: file, issue, severity.
        """
        result = super().issues(root)

        if self._steps_error:
            result.append({
                "file": self.path,
                "issue": self._steps_error,
                "severity": "fail",
            })
            return result  # can't meaningfully check skills or cycles

        if skills_dirs is None:
            skills_dirs = [root / "skills"]

        # Skill existence
        known_skills: set = set()
        for skills_dir in skills_dirs:
            p = Path(skills_dir)
            if p.is_dir():
                for entry in sorted(p.iterdir()):
                    if entry.is_dir() and not entry.name.startswith("_"):
                        known_skills.add(entry.name)

        for step in self.steps:
            skill = step.get("skill", "")
            if skill and skill not in known_skills:
                result.append({
                    "file": self.path,
                    "issue": (
                        f"Chain step {step.get('step', '?')} declares skill"
                        f" '{skill}' which does not exist in skills directories"
                    ),
                    "severity": "fail",
                })

        # Termination condition
        if not self.goal:
            result.append({
                "file": self.path,
                "issue": (
                    "Chain manifest has no termination condition"
                    " (goal is missing or empty)"
                ),
                "severity": "fail",
            })

        # Cycle detection
        prev_step_num: Optional[int] = None
        prev_skill = ""
        for step in self.steps:
            step_id = step.get("step", "")
            skill = step.get("skill", "")
            try:
                step_num = int(step_id)
                if prev_step_num is not None and step_num <= prev_step_num:
                    result.append({
                        "file": self.path,
                        "issue": (
                            f"Chain step numbers are not strictly increasing:"
                            f" step {step_id} follows step {prev_step_num}"
                        ),
                        "severity": "fail",
                    })
                prev_step_num = step_num
            except (ValueError, TypeError):
                pass
            if skill and skill == prev_skill:
                result.append({
                    "file": self.path,
                    "issue": (
                        f"Chain step {step_id} repeats skill '{skill}'"
                        f" from the immediately preceding step (direct loop)"
                    ),
                    "severity": "fail",
                })
            prev_skill = skill

        return result


# ── Convenience wrappers ───────────────────────────────────────────


def parse_chain(manifest_path: Path) -> ChainDocument:
    """Read and parse a *.chain.md manifest into a ChainDocument.

    Args:
        manifest_path: Path to a *.chain.md file.

    Returns:
        A ChainDocument with steps, goal, and negative_scope populated.

    Raises:
        ValueError: If the file cannot be read or frontmatter is missing.
    """
    try:
        text = manifest_path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ValueError(f"Cannot read {manifest_path}: {exc}") from exc

    doc = parse_document(str(manifest_path), text)
    if not isinstance(doc, ChainDocument):
        raise ValueError(
            f"{manifest_path}: expected type 'chain', got '{doc.type}'"
        )
    return doc


def validate_chain(
    manifest_path: Path,
    skills_dirs: List[Path],
    root: Optional[Path] = None,
) -> List[dict]:
    """Validate a chain manifest against all structural checks.

    Parses the manifest and runs ChainDocument.issues(). If parsing
    fails, returns a single warn and exits early.

    Args:
        manifest_path: Path to a *.chain.md file.
        skills_dirs: Directories to search for declared skills.
        root: Project root for resolving related paths. Defaults to
            manifest_path.parent.

    Returns:
        List of issue dicts. Empty on a clean manifest.
    """
    if root is None:
        root = manifest_path.parent

    try:
        text = manifest_path.read_text(encoding="utf-8")
        doc = parse_document(str(manifest_path), text)
    except (OSError, ValueError) as exc:
        return [{
            "file": str(manifest_path),
            "issue": f"Invalid chain manifest: {exc}",
            "severity": "warn",
        }]

    if not isinstance(doc, ChainDocument):
        return [{
            "file": str(manifest_path),
            "issue": f"Not a chain document (type: {doc.type!r})",
            "severity": "warn",
        }]

    return doc.issues(root, skills_dirs=skills_dirs)
