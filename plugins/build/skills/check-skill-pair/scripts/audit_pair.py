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

# Primitive names are kebab-case identifiers (build-skill, check-makefile, etc.).
# Validating at the CLI boundary keeps untrusted input out of path construction
# downstream — the name is interpolated into directory paths, so traversal-style
# inputs like `../foo` would otherwise resolve outside the intended skill root.
_PRIMITIVE_NAME_RE = re.compile(r"^[a-z][a-z0-9-]*$")

# Target prefixes per skill-locations.md. `<SKILL_ROOT>` is where build-/check-
# skills live; `<SHARED_REF_DIR>` holds the principles doc and routing doc.
TARGET_PREFIXES: dict[str, dict[str, str]] = {
    "plugin": {
        "skill_root": "plugins/build/skills",
        "shared_ref_dir": "plugins/build/_shared/references",
    },
    "project": {
        "skill_root": ".claude/skills",
        "shared_ref_dir": ".claude/skills/_shared/references",
    },
    "user": {
        "skill_root": "~/.claude/skills",
        "shared_ref_dir": "~/.claude/skills/_shared/references",
    },
}


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

    Pairs document Tier-1 deterministic checks as a table rather than per-
    signal H3s. Two section-heading dialects exist in the wild:

        ## Tier-1 — Deterministic Checks     (bash-script, python-script)
        ## Tier 1: Deterministic Format Checks   (rule)

    Two column shapes exist:

        | Script | Check ID | What | Severity | Source principle |  (col 1)
        | Check  | Category | Condition | Severity |                  (col 0)

    We locate the first row starting with `|` as the header row, scan it
    for a cell named `Check` or `Check ID`, and pull that column from each
    data row until a new `## ` section begins.
    """
    out: list[str] = []
    in_section = False
    check_col: int | None = None
    for line in text.splitlines():
        if re.match(r"^##\s+Tier[-\s]*1\b", line):
            in_section = True
            check_col = None
            continue
        if in_section and line.startswith("## "):
            break
        if not in_section or not line.startswith("|"):
            continue
        parts = [p.strip() for p in line.strip("|").split("|")]
        if check_col is None:
            for i, cell in enumerate(parts):
                if cell.lower() in ("check", "check id"):
                    check_col = i
                    break
            continue
        if all(set(p) <= set("- :") for p in parts):
            continue
        if check_col >= len(parts):
            continue
        check_id = parts[check_col].strip("`").strip()
        if check_id:
            out.append(check_id)
    return out


NON_DIMENSION_H3_NAMES = frozenset(
    name.lower()
    for name in (
        "Notes",
        "Evaluation Prompt Template",
        "Output Format",
        "Format",
        "Table of Contents",
    )
)


def extract_audit_dimension_h3s(text: str) -> list[str]:
    """Extract H3 headings inside any `## Tier-*` / `## Tier *` H2 section.

    Some pairs document Tier-1 as H3s (skill-pair), others as a table
    (bash-script, python-script, rule). Either way, H3s inside Tier sections
    are dimensions. H3s inside non-Tier H2s (`## Cross-Dimension Notes`,
    `## Output Format`) are excluded.

    Known non-dimension H3 labels — `### Notes`-style prose subsections —
    are filtered out by name so the rule pair's `### Notes` footnote under
    `## Tier 1` is not counted as an orphan dimension.
    """
    out: list[str] = []
    in_tier = False
    for line in text.splitlines():
        h2 = re.match(r"^##\s+(.+)$", line)
        if h2:
            in_tier = bool(re.match(r"^Tier[-\s]*\d+\b", h2.group(1).strip()))
            continue
        if in_tier:
            h3 = re.match(r"^###\s+(.+)$", line)
            if h3:
                name = h3.group(1).strip()
                if name.lower() not in NON_DIMENSION_H3_NAMES:
                    out.append(name)
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


def resolve_target_paths(target: str, root: Path) -> tuple[Path, Path]:
    """Resolve `<SKILL_ROOT>` and `<SHARED_REF_DIR>` for a target.

    `plugin` and `project` prefixes are interpreted relative to ``root``.
    ``user`` prefixes start with ``~`` and are expanded to the user's home
    directory; ``root`` is ignored for that target.
    """
    prefixes = TARGET_PREFIXES[target]
    if target == "user":
        skill_root = Path(prefixes["skill_root"]).expanduser()
        shared_ref_dir = Path(prefixes["shared_ref_dir"]).expanduser()
    else:
        skill_root = root / prefixes["skill_root"]
        shared_ref_dir = root / prefixes["shared_ref_dir"]
    return skill_root, shared_ref_dir


def tier1_existence(
    primitive: str, root: Path, target: str = "plugin"
) -> tuple[list[Finding], dict[str, Path]]:
    """Return findings plus a dict of resolved artifact paths (even if missing)."""
    skill_root, shared_ref_dir = resolve_target_paths(target, root)
    paths = {
        "principles_doc": shared_ref_dir / f"{primitive}-best-practices.md",
        "build_skill": skill_root / f"build-{primitive}" / "SKILL.md",
        "check_skill": skill_root / f"check-{primitive}" / "SKILL.md",
        "audit_dims": skill_root
        / f"check-{primitive}"
        / "references"
        / "audit-dimensions.md",
        "repair_playbook": skill_root
        / f"check-{primitive}"
        / "references"
        / "repair-playbook.md",
        "routing_doc": shared_ref_dir / "primitive-routing.md",
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

    # Routing-doc registration is required for `plugin` target, optional
    # for `project` / `user`. When the routing doc is absent at a non-plugin
    # target, the registration check is skipped silently — projects and
    # users that maintain a routing doc still get the same enforcement.
    routing_text = read_text(paths["routing_doc"])
    if routing_text is None and target != "plugin":
        return findings, paths
    routing_text = routing_text or ""
    severity_both_missing = "fail" if target == "plugin" else "warn"
    severity_one_missing = "warn"
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
                severity_both_missing,
            )
        )
    elif not has_build_route:
        findings.append(
            Finding(
                1,
                "routing-registration-presence",
                rel(paths["routing_doc"]),
                f"{build_route} route line missing",
                severity_one_missing,
            )
        )
    elif not has_check_route:
        findings.append(
            Finding(
                1,
                "routing-registration-presence",
                rel(paths["routing_doc"]),
                f"{check_route} route line missing",
                severity_one_missing,
            )
        )

    return findings, paths


REQUIRED_H2_PREFIXES = [
    "What a Good",
    "Anatomy",
    "Patterns That Work",
    "Safety",
]

REQUIRED_BRIEF_H2_PREFIXES = [
    "User ask",
    "So-what",
    "Scope boundaries",
    "Planned artifacts",
    "Planned handoffs",
]


def tier1_brief_presence(primitive: str, root: Path) -> list[Finding]:
    """Check `.briefs/<primitive>.brief.md` presence and required sections.

    Briefs are throw-away intent artifacts written by multi-artifact
    orchestrators at intake; missing or incomplete briefs are `warn`,
    not `fail` — the pair still functions, but the build that produced
    it lacked the intent-capture step.
    """
    brief_path = root / ".briefs" / f"{primitive}.brief.md"
    rel = str(brief_path.relative_to(root)) if brief_path.is_relative_to(root) else str(
        brief_path
    )
    findings: list[Finding] = []
    text = read_text(brief_path)
    if text is None:
        findings.append(
            Finding(
                1,
                "brief-presence-and-content",
                rel,
                "missing — multi-artifact builds should capture intent in a brief",
                "warn",
            )
        )
        return findings
    h2s = extract_h2(text)
    for required in REQUIRED_BRIEF_H2_PREFIXES:
        if not any(h.startswith(required) for h in h2s):
            findings.append(
                Finding(
                    1,
                    "brief-presence-and-content",
                    rel,
                    f"missing required section: {required}",
                    "warn",
                )
            )
    return findings


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
        # Audit dimensions = Tier-2/Tier-3 H3 headings + Tier-1 table-row IDs.
        # Tier-1 is a table; prose H3s under Tier-1 (e.g., `### Notes`) and
        # supplementary sections like `## Cross-Dimension Notes` are excluded.
        audit_raw = extract_audit_dimension_h3s(audit_text) + extract_tier1_table_ids(
            audit_text
        )
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
    primitive: str, paths: dict[str, Path], root: Path, target: str = "plugin"
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

    skill_root, _ = resolve_target_paths(target, root)
    scripts_dir = skill_root / f"check-{primitive}" / "scripts"
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


def audit(
    primitive: str, root: Path, target: str = "plugin"
) -> tuple[list[Finding], bool]:
    """Return (findings, no_pair_found)."""
    t1, paths = tier1_existence(primitive, root, target)
    # "No pair found": principles doc + both SKILLs all absent → nothing to audit.
    critical_missing = sum(
        1
        for key in ("principles_doc", "build_skill", "check_skill")
        if not paths[key].is_file()
    )
    if critical_missing == 3:
        return [], True
    t2 = tier2_content(paths, root)
    t3 = tier3_cross_reference(primitive, paths, root, target)
    brief = tier1_brief_presence(primitive, root)
    return t1 + brief + t2 + t3, False


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
    parser.add_argument(
        "--target",
        choices=("plugin", "project", "user"),
        default="plugin",
        help=(
            "Placement scope per skill-locations.md: `plugin` (toolkit-style "
            "plugins/build/...), `project` (.claude/skills/...), or `user` "
            "(~/.claude/skills/...). Default: plugin (back-compat)."
        ),
    )
    args = parser.parse_args(argv)

    if not _PRIMITIVE_NAME_RE.match(args.primitive):
        print(
            f"error: primitive name must match {_PRIMITIVE_NAME_RE.pattern} "
            f"(got: {args.primitive!r})",
            file=sys.stderr,
        )
        return 64

    try:
        findings, no_pair = audit(args.primitive, args.root.resolve(), args.target)
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
