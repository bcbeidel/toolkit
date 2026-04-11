"""Chain manifest parsing and structural validation.

Provides parse_chain() for reading *.chain.md manifests and five
structural check functions for validating chain correctness.

Each check returns a list of issue dicts with keys: file, issue, severity.
"""

from __future__ import annotations

from pathlib import Path
from typing import List, Optional

from wos.frontmatter import parse_frontmatter

# ── Parsing ────────────────────────────────────────────────────────


def parse_chain(manifest_path: Path) -> dict:
    """Read and parse a *.chain.md manifest. Returns structured dict.

    Parses frontmatter (name, description, type, goal, negative-scope)
    and the ## Steps markdown pipe table into a list of step dicts.

    Args:
        manifest_path: Path to a *.chain.md file.

    Returns:
        Dict with keys: path, name, description, type, goal,
        negative_scope, steps. ``steps`` is a list of dicts with
        keys: step, skill, input_contract, output_contract, gate.

    Raises:
        ValueError: If the file cannot be read, frontmatter is missing,
            or the ## Steps section is absent.
    """
    try:
        text = manifest_path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ValueError(f"Cannot read {manifest_path}: {exc}") from exc

    fm, body = parse_frontmatter(text)

    return {
        "path": str(manifest_path),
        "name": fm.get("name") or "",
        "description": fm.get("description") or "",
        "type": fm.get("type") or "",
        "goal": fm.get("goal") or "",
        "negative_scope": fm.get("negative-scope") or "",
        "steps": _parse_steps_table(body, manifest_path),
    }


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

    # Find the ## Steps heading
    steps_start: Optional[int] = None
    for i, line in enumerate(lines):
        if line.strip().lower().startswith("## steps"):
            steps_start = i
            break

    if steps_start is None:
        raise ValueError(
            f"No '## Steps' section found in {manifest_path}"
        )

    steps: List[dict] = []
    in_table = False

    for line in lines[steps_start + 1:]:
        stripped = line.strip()

        if not stripped:
            if in_table:
                break  # Blank line ends the table
            continue

        if not stripped.startswith("|"):
            if in_table:
                break
            continue

        # Split on | and strip whitespace; drop empty tokens from leading/trailing |
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

        # Pad to 5 columns
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


# ── Structural checks ──────────────────────────────────────────────


def check_chain_skills_exist(
    manifest: dict, skills_dirs: List[Path]
) -> List[dict]:
    """Fail issues for each declared skill that doesn't exist.

    For each step, checks whether the skill name matches a subdirectory
    in any of the provided skills_dirs.

    Args:
        manifest: Parsed chain manifest dict from parse_chain().
        skills_dirs: List of directories to search for skill subdirectories.

    Returns:
        List of issue dicts with severity 'fail'.
    """
    file_path = manifest.get("path", "")

    known_skills: set = set()
    for skills_dir in skills_dirs:
        p = Path(skills_dir)
        if p.is_dir():
            for entry in sorted(p.iterdir()):
                if entry.is_dir() and not entry.name.startswith("_"):
                    known_skills.add(entry.name)

    issues: List[dict] = []
    for step in manifest.get("steps", []):
        skill = step.get("skill", "")
        if skill and skill not in known_skills:
            issues.append({
                "file": file_path,
                "issue": (
                    f"Chain step {step.get('step', '?')} declares skill"
                    f" '{skill}' which does not exist in skills directories"
                ),
                "severity": "fail",
            })

    return issues


def check_chain_internal_consistency(manifest: dict) -> List[dict]:
    """Warn issues where a step's input contract doesn't match the prior step's output.

    Warns when:
    - Any step has an empty input_contract or output_contract
    - Consecutive steps have non-empty contracts with no shared words
      (heuristic mismatch)

    Args:
        manifest: Parsed chain manifest dict from parse_chain().

    Returns:
        List of issue dicts with severity 'warn'.
    """
    file_path = manifest.get("path", "")
    steps = manifest.get("steps", [])
    issues: List[dict] = []

    for i, step in enumerate(steps):
        step_id = step.get("step", str(i + 1))

        if not step.get("input_contract"):
            issues.append({
                "file": file_path,
                "issue": f"Chain step {step_id} has no input contract declared",
                "severity": "warn",
            })

        if not step.get("output_contract"):
            issues.append({
                "file": file_path,
                "issue": f"Chain step {step_id} has no output contract declared",
                "severity": "warn",
            })

        # Heuristic: compare previous step's output with current step's input
        if i > 0:
            prev_output = steps[i - 1].get("output_contract", "")
            curr_input = step.get("input_contract", "")
            if prev_output and curr_input:
                prev_words = set(prev_output.lower().split())
                curr_words = set(curr_input.lower().split())
                if not prev_words & curr_words:
                    issues.append({
                        "file": file_path,
                        "issue": (
                            f"Chain step {step_id} input contract"
                            f" ({curr_input!r}) shares no terms with"
                            f" prior step output contract ({prev_output!r})"
                        ),
                        "severity": "warn",
                    })

    return issues


_READ_ONLY_SKILL_KEYWORDS = ("research", "assess")


def check_chain_gates(manifest: dict) -> List[dict]:
    """Warn issues for consequential steps without a declared gate.

    A step is considered consequential if its skill name does not
    contain 'research' or 'assess' (heuristic for read-only skills).
    Warns when such a step has an empty gate field.

    Args:
        manifest: Parsed chain manifest dict from parse_chain().

    Returns:
        List of issue dicts with severity 'warn'.
    """
    file_path = manifest.get("path", "")
    issues: List[dict] = []

    for step in manifest.get("steps", []):
        skill = step.get("skill", "").lower()
        gate = step.get("gate", "")
        step_id = step.get("step", "?")

        is_read_only = any(kw in skill for kw in _READ_ONLY_SKILL_KEYWORDS)

        if not is_read_only and not gate:
            issues.append({
                "file": file_path,
                "issue": (
                    f"Chain step {step_id} (skill: '{step.get('skill', '')}')"
                    f" has no gate declared for a consequential step"
                ),
                "severity": "warn",
            })

    return issues


def check_chain_termination(manifest: dict) -> List[dict]:
    """Fail issue if no termination condition declared at chain level.

    Checks that the manifest's 'goal' field is non-empty.

    Args:
        manifest: Parsed chain manifest dict from parse_chain().

    Returns:
        List of issue dicts with severity 'fail'.
    """
    file_path = manifest.get("path", "")

    if not manifest.get("goal"):
        return [{
            "file": file_path,
            "issue": (
                "Chain manifest has no termination condition"
                " (goal is missing or empty)"
            ),
            "severity": "fail",
        }]

    return []


def check_chain_cycles(manifest: dict) -> List[dict]:
    """Fail issue for any circular skill references in the step sequence.

    Detects:
    - Step numbers that are not strictly increasing integers
    - The same skill appearing in two consecutive steps (direct loop)

    Args:
        manifest: Parsed chain manifest dict from parse_chain().

    Returns:
        List of issue dicts with severity 'fail'.
    """
    file_path = manifest.get("path", "")
    steps = manifest.get("steps", [])
    issues: List[dict] = []

    prev_step_num: Optional[int] = None
    prev_skill = ""

    for step in steps:
        step_id = step.get("step", "")
        skill = step.get("skill", "")

        # Check monotonically increasing step numbers
        try:
            step_num = int(step_id)
            if prev_step_num is not None and step_num <= prev_step_num:
                issues.append({
                    "file": file_path,
                    "issue": (
                        f"Chain step numbers are not strictly increasing:"
                        f" step {step_id} follows step {prev_step_num}"
                    ),
                    "severity": "fail",
                })
            prev_step_num = step_num
        except (ValueError, TypeError):
            pass  # Non-integer step IDs are allowed

        # Check consecutive same-skill (direct loop)
        if skill and skill == prev_skill:
            issues.append({
                "file": file_path,
                "issue": (
                    f"Chain step {step_id} repeats skill '{skill}'"
                    f" from the immediately preceding step (direct loop)"
                ),
                "severity": "fail",
            })

        prev_skill = skill

    return issues
