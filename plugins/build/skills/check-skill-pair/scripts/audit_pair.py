#!/usr/bin/env python3
"""Audit a skill-pair deterministically. Example: ./audit_pair.py bash-script"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

# Script lives at plugins/build/skills/check-skill-pair/scripts/audit_pair.py.
# parents[0]=scripts, [1]=check-skill-pair, [2]=skills, [3]=build, [4]=plugins,
# [5]=repo root. This script reads paths beyond its plugin, so plugin-relative
# resolution (Path(__file__).parents[1]) would be wrong.
DEFAULT_REPO_ROOT = Path(__file__).resolve().parents[5]


@dataclass(frozen=True)
class Finding:
    tier: int
    check: str
    artifact: str
    issue: str
    severity: str  # "fail" | "warn" | "info"


SEVERITY_ORDER = {"fail": 0, "warn": 1, "info": 2}


def read_text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return None


def extract_h2(text: str) -> list[str]:
    return [m.strip() for m in re.findall(r"^##\s+(.+)$", text, flags=re.M)]


def extract_h3(text: str) -> list[str]:
    return [m.strip() for m in re.findall(r"^###\s+(.+)$", text, flags=re.M)]


def normalize_dimension_id(raw: str) -> str:
    r"""Reduce a verbose H3 heading or table-cell ID to a canonical identifier.

    Handles forms seen across pairs:
      - ``### secret``                                          -> ``secret``
      - ``### Signal: `secret -- API key ...` ``                -> ``secret``
      - ``### Signal: `SC2086 -- unquoted ...` *(FAIL)*``       -> ``sc2086``
      - ``### D1 Output Discipline``                            -> ``d1``
      - ``### `SC2013` / `SC2162` ``                            -> ``sc2013 / sc2162``
    Steps: strip *(FAIL)*, strip "Signal: " prefix, take everything before
    " -- " (em-dash space) or " - ", remove ALL backticks (handles
    ``A` / `B`` form), collapse whitespace, lowercase. For ``Dn ...`` Tier-2
    dimensions, keep just ``dn``.
    """
    s = raw.strip()
    s = re.sub(r"\s*\*\(FAIL\)\*\s*$", "", s)
    s = re.sub(r"^Signal:\s*", "", s)
    s = s.strip()
    for sep in (" — ", " – ", " - "):
        if sep in s:
            s = s.split(sep, 1)[0]
            break
    s = s.replace("`", "").strip()
    s = re.sub(r"\s+", " ", s)
    if re.match(r"^[Dd]\d+\b", s):
        s = re.match(r"^[Dd]\d+", s).group(0).lower()
    return s.lower()


def extract_tier1_table_ids(text: str) -> list[str]:
    """Extract Check IDs from rows in the Tier-1 markdown table.

    Pre-existing pairs document Tier-1 deterministic checks as a table under
    `## Tier-1 — Deterministic Checks` (compact for ~26 mechanical signals)
    rather than per-signal H3s. The table column shape is:

        | Script | Check ID | What | Severity | Source principle |

    We pull the second column from data rows. Skips header / separator /
    rows with fewer than five pipe-delimited fields.
    """
    out: list[str] = []
    in_section = False
    for line in text.splitlines():
        if line.startswith("## Tier-1"):
            in_section = True
            continue
        if in_section and line.startswith("## "):
            break
        if not in_section or not line.startswith("|"):
            continue
        parts = [p.strip() for p in line.strip("|").split("|")]
        if len(parts) < 5:
            continue
        first = parts[0]
        if first in ("Script", "") or first.startswith("---"):
            continue
        if all(set(p) <= set("- ") for p in parts):
            continue
        check_id = parts[1].strip("`").strip()
        if check_id:
            out.append(check_id)
    return out


def parse_references_field(frontmatter_text: str) -> list[str]:
    """Extract the list items under a `references:` key in YAML frontmatter.

    Stdlib-only — we don't need pyyaml for a single known-shape field.
    """
    lines = frontmatter_text.splitlines()
    refs: list[str] = []
    in_refs = False
    for line in lines:
        stripped = line.strip()
        if not in_refs:
            if stripped == "references:":
                in_refs = True
            continue
        # Still inside references: block as long as line is indented list item.
        if line.startswith((" ", "\t")) and stripped.startswith("- "):
            refs.append(stripped[2:].strip())
        elif stripped == "":
            continue
        else:
            break
    return refs


def extract_frontmatter(text: str) -> str | None:
    """Return the YAML block between the first two `---` fences, or None."""
    match = re.match(r"^---\n(.*?)\n---", text, flags=re.S)
    return match.group(1) if match else None


def resolve_reference(skill_dir: Path, ref: str) -> Path:
    return (skill_dir / ref).resolve()


def tier1_existence(
    primitive: str, root: Path
) -> tuple[list[Finding], dict[str, Path]]:
    """Return findings plus a dict of resolved artifact paths (even if missing)."""
    paths = {
        "principles_doc": root
        / "plugins/build/_shared/references"
        / f"{primitive}-best-practices.md",
        "build_skill": root
        / "plugins/build/skills"
        / f"build-{primitive}"
        / "SKILL.md",
        "check_skill": root
        / "plugins/build/skills"
        / f"check-{primitive}"
        / "SKILL.md",
        "audit_dims": root
        / "plugins/build/skills"
        / f"check-{primitive}"
        / "references"
        / "audit-dimensions.md",
        "repair_playbook": root
        / "plugins/build/skills"
        / f"check-{primitive}"
        / "references"
        / "repair-playbook.md",
        "routing_doc": root / "plugins/build/_shared/references/primitive-routing.md",
    }
    findings: list[Finding] = []

    def rel(p: Path) -> str:
        try:
            return str(p.relative_to(root))
        except ValueError:
            return str(p)

    if not (
        paths["principles_doc"].is_file() and paths["principles_doc"].stat().st_size > 0
    ):
        findings.append(
            Finding(
                1,
                "principles-doc-presence",
                rel(paths["principles_doc"]),
                "missing or empty",
                "fail",
            )
        )
    if not paths["build_skill"].is_file():
        findings.append(
            Finding(
                1, "build-skill-presence", rel(paths["build_skill"]), "missing", "fail"
            )
        )
    if not paths["check_skill"].is_file():
        findings.append(
            Finding(
                1, "check-skill-presence", rel(paths["check_skill"]), "missing", "fail"
            )
        )
    if not paths["audit_dims"].is_file():
        findings.append(
            Finding(
                1,
                "audit-dimensions-presence",
                rel(paths["audit_dims"]),
                "missing",
                "fail",
            )
        )
    if not paths["repair_playbook"].is_file():
        findings.append(
            Finding(
                1,
                "repair-playbook-presence",
                rel(paths["repair_playbook"]),
                "missing",
                "fail",
            )
        )

    routing_text = read_text(paths["routing_doc"]) or ""
    build_route = f"/build:build-{primitive}"
    check_route = f"/build:check-{primitive}"
    has_build_route = build_route in routing_text
    has_check_route = check_route in routing_text
    if not has_build_route and not has_check_route:
        findings.append(
            Finding(
                1,
                "routing-registration-presence",
                rel(paths["routing_doc"]),
                f"both {build_route} and {check_route} route lines missing",
                "fail",
            )
        )
    elif not has_build_route:
        findings.append(
            Finding(
                1,
                "routing-registration-presence",
                rel(paths["routing_doc"]),
                f"{build_route} route line missing",
                "warn",
            )
        )
    elif not has_check_route:
        findings.append(
            Finding(
                1,
                "routing-registration-presence",
                rel(paths["routing_doc"]),
                f"{check_route} route line missing",
                "warn",
            )
        )

    return findings, paths


REQUIRED_H2_PREFIXES = [
    "What a Good",
    "Anatomy",
    "Patterns That Work",
    "Safety",
]


def tier2_content(paths: dict[str, Path], root: Path) -> list[Finding]:
    findings: list[Finding] = []

    def rel(p: Path) -> str:
        try:
            return str(p.relative_to(root))
        except ValueError:
            return str(p)

    principles_text = read_text(paths["principles_doc"])
    if principles_text:
        h2s = extract_h2(principles_text)
        for required in REQUIRED_H2_PREFIXES:
            if not any(h.startswith(required) for h in h2s):
                findings.append(
                    Finding(
                        2,
                        "principles-doc-structure",
                        rel(paths["principles_doc"]),
                        f"missing required H2 section: {required}",
                        "warn",
                    )
                )

    audit_text = read_text(paths["audit_dims"])
    playbook_text = read_text(paths["repair_playbook"])
    if audit_text and playbook_text:
        # Audit dimensions = H3 headings + Tier-1 table-row IDs (pre-existing
        # pairs document deterministic checks compactly as a table, not H3s).
        audit_raw = extract_h3(audit_text) + extract_tier1_table_ids(audit_text)
        playbook_raw = extract_h3(playbook_text)
        audit_dims = {normalize_dimension_id(d) for d in audit_raw if d}
        playbook_dims = {normalize_dimension_id(d) for d in playbook_raw if d}
        audit_orphans = sorted(audit_dims - playbook_dims)
        playbook_orphans = sorted(playbook_dims - audit_dims)
        for dim in audit_orphans:
            findings.append(
                Finding(
                    2,
                    "dimension-coverage-alignment",
                    "audit-dimensions.md vs repair-playbook.md",
                    f"audit dimension '{dim}' has no repair entry",
                    "fail",
                )
            )
        for dim in playbook_orphans:
            findings.append(
                Finding(
                    2,
                    "dimension-coverage-alignment",
                    "audit-dimensions.md vs repair-playbook.md",
                    f"playbook dimension '{dim}' has no audit entry",
                    "warn",
                )
            )

    return findings


def tier3_cross_reference(
    primitive: str, paths: dict[str, Path], root: Path
) -> list[Finding]:
    findings: list[Finding] = []

    def rel(p: Path) -> str:
        try:
            return str(p.relative_to(root))
        except ValueError:
            return str(p)

    build_text = read_text(paths["build_skill"])
    check_text = read_text(paths["check_skill"])

    def extract_principles_ref(skill_text: str, skill_path: Path) -> Path | None:
        fm = extract_frontmatter(skill_text or "")
        if not fm:
            return None
        for ref in parse_references_field(fm):
            if ref.endswith(f"{primitive}-best-practices.md"):
                return resolve_reference(skill_path.parent, ref)
        return None

    build_principles = (
        extract_principles_ref(build_text or "", paths["build_skill"])
        if build_text
        else None
    )
    check_principles = (
        extract_principles_ref(check_text or "", paths["check_skill"])
        if check_text
        else None
    )

    if build_text and build_principles is None:
        findings.append(
            Finding(
                3,
                "shared-principles-path",
                rel(paths["build_skill"]),
                "frontmatter references: does not cite the principles doc",
                "fail",
            )
        )
    if check_text and check_principles is None:
        findings.append(
            Finding(
                3,
                "shared-principles-path",
                rel(paths["check_skill"]),
                "frontmatter references: does not cite the principles doc",
                "fail",
            )
        )
    if build_principles and check_principles and build_principles != check_principles:
        findings.append(
            Finding(
                3,
                "shared-principles-path",
                "build/check SKILL.md references",
                f"halves reference different principles docs "
                f"({rel(build_principles)} vs {rel(check_principles)})",
                "fail",
            )
        )

    if check_text:
        fm = extract_frontmatter(check_text) or ""
        refs = parse_references_field(fm)
        has_audit = any(ref.endswith("audit-dimensions.md") for ref in refs)
        has_playbook = any(ref.endswith("repair-playbook.md") for ref in refs)
        if not has_audit:
            findings.append(
                Finding(
                    3,
                    "check-frontmatter-references",
                    rel(paths["check_skill"]),
                    "frontmatter references: missing audit-dimensions.md",
                    "warn",
                )
            )
        if not has_playbook:
            findings.append(
                Finding(
                    3,
                    "check-frontmatter-references",
                    rel(paths["check_skill"]),
                    "frontmatter references: missing repair-playbook.md",
                    "warn",
                )
            )

    if build_text:
        check_route = f"/build:check-{primitive}"
        if check_route not in build_text:
            findings.append(
                Finding(
                    3,
                    "build-to-check-handoff",
                    rel(paths["build_skill"]),
                    f"body does not mention {check_route}",
                    "warn",
                )
            )

    scripts_dir = root / "plugins/build/skills" / f"check-{primitive}" / "scripts"
    if scripts_dir.is_dir():
        py_scripts = list(scripts_dir.glob("*.py"))
        sh_scripts = list(scripts_dir.glob("*.sh")) + list(scripts_dir.glob("*.bash"))
        if py_scripts:
            findings.append(
                Finding(
                    3,
                    "dogfood-script-audit",
                    rel(scripts_dir),
                    f"{len(py_scripts)} Python script(s) — "
                    "run /build:check-python-script",
                    "info",
                )
            )
        if sh_scripts:
            findings.append(
                Finding(
                    3,
                    "dogfood-script-audit",
                    rel(scripts_dir),
                    f"{len(sh_scripts)} shell script(s) — run /build:check-bash-script",
                    "info",
                )
            )

    return findings


def format_table(findings: list[Finding]) -> str:
    findings_sorted = sorted(
        findings, key=lambda f: (SEVERITY_ORDER[f.severity], f.tier, f.check)
    )
    lines = [
        "| Tier | Check | Artifact | Issue | Severity |",
        "|------|-------|----------|-------|----------|",
    ]
    for f in findings_sorted:
        lines.append(
            f"| T{f.tier} | {f.check} | {f.artifact} | {f.issue} | {f.severity} |"
        )
    return "\n".join(lines)


def summary_counts(findings: list[Finding]) -> tuple[int, int, int]:
    fails = sum(1 for f in findings if f.severity == "fail")
    warns = sum(1 for f in findings if f.severity == "warn")
    infos = sum(1 for f in findings if f.severity == "info")
    return fails, warns, infos


def audit(primitive: str, root: Path) -> tuple[list[Finding], bool]:
    """Return (findings, no_pair_found)."""
    t1, paths = tier1_existence(primitive, root)
    # "No pair found": principles doc + both SKILLs all absent → nothing to audit.
    critical_missing = sum(
        1
        for key in ("principles_doc", "build_skill", "check_skill")
        if not paths[key].is_file()
    )
    if critical_missing == 3:
        return [], True
    t2 = tier2_content(paths, root)
    t3 = tier3_cross_reference(primitive, paths, root)
    return t1 + t2 + t3, False


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Audit a skill-pair for structural and cross-artifact integrity.",
    )
    parser.add_argument(
        "primitive", help="Primitive name (kebab-case, no path prefix)."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=DEFAULT_REPO_ROOT,
        help="Repo root (default: resolved from script location).",
    )
    args = parser.parse_args(argv)

    try:
        findings, no_pair = audit(args.primitive, args.root.resolve())
    except KeyboardInterrupt:
        return 130

    if no_pair:
        print(
            f"No pair found for {args.primitive} — "
            f"recommend /build:build-skill-pair {args.primitive}"
        )
        return 0

    if not findings:
        print(f"All checks passed for skill-pair: {args.primitive}")
        return 0

    fails, warns, infos = summary_counts(findings)
    header = f"{fails} fail, {warns} warn, {infos} info across 6 artifact slots"
    print(header)
    print()
    print(format_table(findings))
    print()
    print(header)

    return 1 if fails > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
