#!/usr/bin/env python3
"""Run Tier-1 deterministic checks against a help-skill SKILL.md.

Walks the help-skill against the audit-dimensions.md Tier-1 inventory
and emits lint-format findings: SEVERITY  <path> — <check-id>: <message>.

Exit codes:
    0 — clean / WARN-only / INFO-only
    1 — at least one FAIL finding
    2 — usage error

Examples:
    ./check_help_skill.py work
    ./check_help_skill.py plugins/work/skills/help/SKILL.md
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

EXIT_USAGE = 2
EXIT_INTERRUPTED = 130

PLUGIN_ROOT = Path(__file__).resolve().parents[3]
PLUGINS_DIR = PLUGIN_ROOT.parent
RENDER_SCRIPT = (
    PLUGIN_ROOT / "skills" / "build-help-skill" / "scripts" / "render_skill_table.py"
)

REQUIRED_FRONTMATTER_KEYS = (
    "name",
    "description",
    "version",
    "owner",
    "license",
    "references",
)
SANCTIONED_FRONTMATTER_KEYS = frozenset(
    {
        "name",
        "description",
        "version",
        "owner",
        "license",
        "references",
        "argument-hint",
        "user-invocable",
        "disable-model-invocation",
        "when_to_use",
        "paths",
        "allowed-tools",
        "context",
        "agent",
        "model",
        "effort",
        "hooks",
        "tested_with",
    }
)

SECRET_PATTERNS = [
    r"sk-[a-zA-Z0-9]{20,}",
    r"AKIA[0-9A-Z]{16}",
    r"ghp_[A-Za-z0-9]{20,}",
    r"-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----",
    r"(?i)password\s*[:=]\s*[\"']?[^\s\"']{8,}",
]
TLS_DISABLE_PATTERNS = [
    r"(?i)(?:disable|turn\s+off|skip)\s+(?:tls|ssl|certificate|cert)\s+(?:verif|validation|check)",
    r"--insecure\b",
    r"--no-check-certificate\b",
    r"verify\s*=\s*False",
]
PIPE_TO_SHELL_PATTERNS = [
    r"curl\s+[^|\n]*\|\s*(?:sh|bash|zsh)\b",
    r"wget\s+[^|\n]*\|\s*(?:sh|bash|zsh)\b",
    r"iex\s*\(\s*iwr",
]
TRIGGER_PHRASE_PATTERNS = [
    r"what['’]s in",
    r"list\s+\S+\s+skills",
    r"list\s+skills",
    r"how do i use",
    r"which\s+\S+\s+skill",
]
LOAD_BEARING_POINTERS = ("AGENTS.md", "RESOLVER.md", "README.md")

BODY_LINE_TARGET = 150
BODY_LINE_HARD = 200
WORD_LIMIT = 12
DRIFT_PREFIX_WORDS = 6

Finding = tuple[str, str, str]


def get_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Run Tier-1 deterministic checks against a help-skill SKILL.md.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    p.add_argument("target", help="Plugin name or path to a help-skill SKILL.md.")
    return p


def resolve_target(arg: str) -> Path:
    candidate = Path(arg)
    if candidate.suffix == ".md" or candidate.name == "SKILL.md":
        return candidate.resolve()
    return (PLUGINS_DIR / arg / "skills" / "help" / "SKILL.md").resolve()


def split_frontmatter_body(text: str) -> tuple[str, str]:
    if not text.startswith("---\n"):
        return "", text
    lines = text.splitlines(keepends=True)
    for i in range(1, len(lines)):
        if lines[i].rstrip("\n") == "---":
            return "".join(lines[1:i]), "".join(lines[i + 1 :])
    return "", text


def parse_frontmatter(yaml_text: str) -> dict[str, str]:
    out: dict[str, str] = {}
    lines = yaml_text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        m = re.match(r"^([A-Za-z][A-Za-z0-9_-]*):\s*(.*)$", line)
        if not m:
            i += 1
            continue
        key, val = m.group(1), m.group(2).strip()
        if val in (">-", ">", "|", "|-"):
            chunks: list[str] = []
            i += 1
            while i < len(lines) and (
                lines[i].startswith("  ") or not lines[i].strip()
            ):
                if lines[i].strip():
                    chunks.append(lines[i].strip())
                i += 1
            out[key] = " ".join(chunks)
            continue
        out[key] = val.strip("\"'")
        i += 1
    return out


def first_n_words(s: str, n: int) -> str:
    words = s.split()
    return " ".join(words[:n]) if words else ""


def get_siblings(plugin: str) -> list[dict[str, str]]:
    if not RENDER_SCRIPT.is_file():
        return []
    result = subprocess.run(
        [sys.executable, str(RENDER_SCRIPT), plugin, "--format", "json"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return []


def check_slug(path: Path, fm: dict[str, str]) -> list[Finding]:
    out: list[Finding] = []
    if fm.get("name") != "help":
        out.append(
            (
                "FAIL",
                "slug-mismatch",
                f"frontmatter name is {fm.get('name')!r}, expected 'help'",
            )
        )
    if path.parent.name != "help":
        out.append(
            (
                "FAIL",
                "slug-mismatch",
                f"directory basename is {path.parent.name!r}, expected 'help'",
            )
        )
    return out


def check_frontmatter_shape(fm: dict[str, str]) -> list[Finding]:
    missing = [k for k in REQUIRED_FRONTMATTER_KEYS if k not in fm]
    return (
        [("WARN", "frontmatter-shape", f"missing required keys: {', '.join(missing)}")]
        if missing
        else []
    )


def check_frontmatter_invented_key(fm: dict[str, str]) -> list[Finding]:
    invented = sorted(set(fm.keys()) - SANCTIONED_FRONTMATTER_KEYS)
    return (
        [
            (
                "WARN",
                "frontmatter-invented-key",
                f"unsanctioned keys: {', '.join(invented)}",
            )
        ]
        if invented
        else []
    )


def check_body_line_count(body: str) -> list[Finding]:
    n = len(body.splitlines())
    if n > BODY_LINE_HARD:
        return [
            (
                "WARN",
                "body-line-count",
                f"body length {n} exceeds {BODY_LINE_HARD}-line hard ceiling",
            )
        ]
    if n > BODY_LINE_TARGET:
        return [
            (
                "WARN",
                "body-line-count",
                f"body length {n} exceeds {BODY_LINE_TARGET}-line target",
            )
        ]
    return []


def check_patterns(
    text: str, patterns: list[str], severity: str, check_id: str, label: str
) -> list[Finding]:
    return [
        (severity, check_id, f"{label}: pattern {pat!r}")
        for pat in patterns
        if re.search(pat, text)
    ]


def check_synopsis_present(body: str) -> list[Finding]:
    lines = body.splitlines()
    h1, h2 = None, None
    for i, line in enumerate(lines):
        if h1 is None and line.startswith("# "):
            h1 = i
        elif h1 is not None and line.startswith("## "):
            h2 = i
            break
    if h1 is None:
        return [("WARN", "synopsis-present", "no H1 found in body")]
    if h2 is None:
        return [("WARN", "synopsis-present", "no H2 found after H1")]
    if not "\n".join(lines[h1 + 1 : h2]).strip():
        return [("WARN", "synopsis-present", "no synopsis between H1 and first H2")]
    return []


def check_managed_region(body: str) -> tuple[list[Finding], str | None]:
    o = re.search(r"<!--\s*generated[^>]*-->", body)
    c = re.search(r"<!--\s*/generated\s*-->", body)
    if not o or not c or o.start() >= c.start():
        return (
            [
                (
                    "FAIL",
                    "managed-region-present",
                    "missing or out-of-order <!-- generated --> markers",
                )
            ],
            None,
        )
    region = body[o.end() : c.start()].strip()
    if "|" not in region:
        return (
            [
                (
                    "FAIL",
                    "managed-region-present",
                    "managed region contains no markdown table",
                )
            ],
            None,
        )
    return ([], region)


def parse_table_rows(region: str) -> list[tuple[str, str]]:
    rows: list[tuple[str, str]] = []
    for line in region.splitlines():
        if not line.startswith("|"):
            continue
        parts = [p.strip() for p in line.strip("|").split("|")]
        if len(parts) < 2 or all(set(p) <= set("- :") for p in parts):
            continue
        if parts[0].lower() in ("skill", "skill name"):
            continue
        name = parts[0].strip("`").strip()
        if name:
            rows.append((name, parts[1]))
    return rows


def check_skill_index_coverage(
    rows: list[tuple[str, str]], siblings: list[dict[str, str]]
) -> list[Finding]:
    out: list[Finding] = []
    sib = {s["name"] for s in siblings}
    tab = {n for n, _ in rows}
    missing = sib - tab
    extra = tab - sib - {"help"}
    if missing:
        out.append(
            (
                "FAIL",
                "skill-index-coverage",
                f"siblings missing from table: {', '.join(sorted(missing))}",
            )
        )
    if extra:
        out.append(
            (
                "FAIL",
                "skill-index-coverage",
                f"table rows for non-existent skills: {', '.join(sorted(extra))}",
            )
        )
    return out


def check_skill_index_no_self(rows: list[tuple[str, str]]) -> list[Finding]:
    return (
        [("WARN", "skill-index-no-self", "table contains a row for 'help'")]
        if any(name == "help" for name, _ in rows)
        else []
    )


def check_description_fidelity(
    rows: list[tuple[str, str]], siblings: list[dict[str, str]]
) -> list[Finding]:
    out: list[Finding] = []
    by_name = {s["name"]: s for s in siblings}
    for name, triggers in rows:
        sib = by_name.get(name)
        if not sib:
            continue
        expected = first_n_words(sib["description"], DRIFT_PREFIX_WORDS).lower()
        observed = first_n_words(
            triggers.replace("…", "").replace("\\|", "|"), DRIFT_PREFIX_WORDS
        ).lower()
        if expected and expected != observed:
            out.append(
                (
                    "WARN",
                    "description-fidelity",
                    f"row '{name}' triggers do not match sibling description prefix",
                )
            )
    return out


def find_section(body: str, heading: str) -> str | None:
    m = re.search(
        rf"^##\s+{re.escape(heading)}\s*$(.*?)(?=^##\s+|\Z)", body, re.M | re.S
    )
    return m.group(1) if m else None


def check_workflow_section_present(text: str | None) -> list[Finding]:
    if text is None:
        return [
            (
                "WARN",
                "workflow-section-present",
                "no '## Common workflows' section found",
            )
        ]
    if not re.search(r"`[^`]+`\s*(?:→|->)\s*`", text):
        return [
            (
                "WARN",
                "workflow-section-present",
                "workflows section has no composed chain (skill -> skill)",
            )
        ]
    return []


def check_workflow_freshness(
    text: str | None, plugin_skills_dir: Path
) -> list[Finding]:
    if text is None:
        return []
    on_disk = (
        {p.name for p in plugin_skills_dir.iterdir() if p.is_dir()}
        if plugin_skills_dir.is_dir()
        else set()
    )
    referenced = set(re.findall(r"`([a-z][a-z0-9-]*)`", text))
    out: list[Finding] = []
    for name in sorted(referenced - on_disk):
        if "." in name or "/" in name:
            continue
        out.append(
            (
                "WARN",
                "workflow-freshness",
                f"workflow references skill '{name}' that does not exist in plugin",
            )
        )
    return out


def check_pointer_resolution(body: str, skill_md: Path) -> list[Finding]:
    text = find_section(body, "Where to look next")
    if text is None:
        return [
            ("WARN", "pointer-resolution", "no '## Where to look next' section found")
        ]
    out: list[Finding] = []
    for m in re.finditer(r"\[([^\]]+)\]\(([^)]+)\)", text):
        label, link = m.group(1), m.group(2)
        if link.startswith(("http://", "https://", "#", "mailto:")):
            continue
        target = (skill_md.parent / link).resolve()
        if not target.exists():
            is_load_bearing = any(
                p in link or p in label for p in LOAD_BEARING_POINTERS
            )
            sev = "FAIL" if is_load_bearing else "WARN"
            cid = "pointer-broken-fail" if is_load_bearing else "pointer-resolution"
            out.append((sev, cid, f"broken link [{label}]({link})"))
    return out


def check_description_trigger_shape(fm: dict[str, str]) -> list[Finding]:
    desc = fm.get("description", "").lower()
    if not desc:
        return []
    out: list[Finding] = []
    if not desc.lstrip().startswith("use when"):
        out.append(
            (
                "WARN",
                "description-trigger-shape",
                "description does not lead with 'Use when'",
            )
        )
    if not any(re.search(p, desc) for p in TRIGGER_PHRASE_PATTERNS):
        out.append(
            (
                "WARN",
                "description-trigger-shape",
                "description has no help-skill trigger phrase "
                "(what's in / list skills / how do I use / which skill)",
            )
        )
    return out


def render_findings(path: Path, findings: list[Finding]) -> str:
    order = {"FAIL": 0, "WARN": 1, "INFO": 2}
    findings.sort(key=lambda f: (order.get(f[0], 99), f[1], f[2]))
    counts = {"FAIL": 0, "WARN": 0, "INFO": 0}
    for sev, _, _ in findings:
        counts[sev] = counts.get(sev, 0) + 1
    lines = [f"{sev}  {path} — {cid}: {msg}" for sev, cid, msg in findings]
    if findings:
        lines.append("")
    lines.append(f"{counts['FAIL']} fail, {counts['WARN']} warn, {counts['INFO']} info")
    return "\n".join(lines) + "\n"


def run(args: argparse.Namespace) -> int:
    skill_md = resolve_target(args.target)
    if not skill_md.is_file():
        raise FileNotFoundError(f"help-skill not found: {skill_md}")
    text = skill_md.read_text(encoding="utf-8")
    yaml_text, body = split_frontmatter_body(text)
    fm = parse_frontmatter(yaml_text)
    plugin = skill_md.parents[2].name
    plugin_skills_dir = skill_md.parents[1]

    findings: list[Finding] = []
    findings += check_slug(skill_md, fm)
    findings += check_frontmatter_shape(fm)
    findings += check_frontmatter_invented_key(fm)
    findings += check_body_line_count(body)
    findings += check_patterns(
        text, SECRET_PATTERNS, "FAIL", "secret", "secret-like pattern"
    )
    findings += check_patterns(
        text, TLS_DISABLE_PATTERNS, "FAIL", "tls-disable", "TLS-disable pattern"
    )
    findings += check_patterns(
        text, PIPE_TO_SHELL_PATTERNS, "FAIL", "pipe-to-shell", "pipe-to-shell installer"
    )
    findings += check_synopsis_present(body)
    region_findings, region = check_managed_region(body)
    findings += region_findings

    siblings = get_siblings(plugin)
    if region is not None:
        rows = parse_table_rows(region)
        findings += check_skill_index_coverage(rows, siblings)
        findings += check_skill_index_no_self(rows)
        findings += check_description_fidelity(rows, siblings)

    workflow_text = find_section(body, "Common workflows")
    findings += check_workflow_section_present(workflow_text)
    findings += check_workflow_freshness(workflow_text, plugin_skills_dir)
    findings += check_pointer_resolution(body, skill_md)
    findings += check_description_trigger_shape(fm)

    sys.stdout.write(render_findings(skill_md, findings))
    return 1 if any(f[0] == "FAIL" for f in findings) else 0


def main(argv: list[str] | None = None) -> int:
    args = get_parser().parse_args(argv)
    try:
        return run(args)
    except KeyboardInterrupt:
        return EXIT_INTERRUPTED
    except (FileNotFoundError, ValueError) as err:
        print(f"error: {err}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
