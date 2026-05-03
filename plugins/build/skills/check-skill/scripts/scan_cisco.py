#!/usr/bin/env python3
"""scan_cisco.py — Tier-1 wrapper around cisco-ai-skill-scanner.

Maps each input path to its parent skill directory and runs the
scanner once per dir. Static analyzers only by default. Pass --llm
(or set SCAN_USE_LLM=1) to add the LLM analyzer; that path requires
ANTHROPIC_API_KEY in the environment.

Severity mapping (canonical):
  CRITICAL / HIGH -> FAIL  (excludes the skill from Tier-2)
  MEDIUM          -> WARN
  LOW / INFO      -> INFO

Soft-fail when scanner missing: emits one INFO line and exits 0, so
/build:check-skill remains runnable on a fresh clone without the
~5GB scanner dependency tree.

Usage:
  scan_cisco.py <SKILL.md | skills/dir | file-under-skill> [...]
  scan_cisco.py --llm plugins/wiki/skills/lint/SKILL.md

Exit codes:
  0   no FAIL findings (or scanner not installed)
  1   one or more CRITICAL/HIGH findings
  64  bad arguments or --llm without API key
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

INSTALL_HINT = (
    "pip install cisco-ai-skill-scanner==2.0.9 "
    "(or: pip install --require-hashes -r .github/scripts/requirements.lock)"
)

SEVERITY_TO_TIER1 = {
    "CRITICAL": "FAIL",
    "HIGH": "FAIL",
    "MEDIUM": "WARN",
    "LOW": "INFO",
    "INFO": "INFO",
}


def emit(severity: str, path: str, check: str, detail: str, rec: str) -> None:
    print(f"{severity}  {path} — {check}: {detail}")
    print(f"  Recommendation: {rec}")


def discover_skill_dirs(paths: list[str]) -> list[Path]:
    """Resolve each input to its parent skill directory.

    Accepts a SKILL.md path, a directory containing skills, or any
    file living under a skill directory. Skips _shared/ trees.
    """
    dirs: set[Path] = set()
    for raw in paths:
        p = Path(raw)
        if not p.exists():
            print(f"scan_cisco.py: path not found: {raw}", file=sys.stderr)
            sys.exit(64)
        if "_shared" in p.parts:
            continue
        if p.is_file() and p.name == "SKILL.md":
            dirs.add(p.parent)
        elif p.is_dir():
            for skill_md in p.rglob("SKILL.md"):
                if "_shared" in skill_md.parts:
                    continue
                dirs.add(skill_md.parent)
        elif p.is_file():
            for parent in p.parents:
                if (parent / "SKILL.md").exists():
                    dirs.add(parent)
                    break
    return sorted(dirs)


def run_scanner(skill_dir: Path, use_llm: bool) -> dict:
    cmd = ["skill-scanner", "scan", str(skill_dir), "--format", "json"]
    if use_llm:
        cmd.append("--use-llm")
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if not proc.stdout.strip():
        return {}
    return json.loads(proc.stdout)


def map_finding(
    finding: dict, skill_dir: Path
) -> tuple[str, str, str, str, str] | None:
    sev = finding.get("severity", "").upper()
    tier1 = SEVERITY_TO_TIER1.get(sev)
    if tier1 is None:
        return None
    rule = finding.get("rule_id", "scanner")
    title = finding.get("title") or finding.get("description") or "scanner finding"
    file_rel = finding.get("file_path") or ""
    line = finding.get("line_number")
    path = f"{skill_dir}/{file_rel}" if file_rel else str(skill_dir)
    detail = f"[{rule}] {title}"
    if line:
        detail = f"{detail} (line {line})"
    rec = finding.get("remediation") or "See `skill-scanner` rule docs."
    return tier1, path, "Skill scanner", detail, rec


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="scan_cisco.py",
        description="Tier-1 wrapper around cisco-ai-skill-scanner.",
    )
    parser.add_argument(
        "paths",
        nargs="+",
        help="SKILL.md paths, skills/ directories, or files under a skill dir.",
    )
    parser.add_argument(
        "--llm",
        action="store_true",
        default=os.environ.get("SCAN_USE_LLM") == "1",
        help="Include the LLM analyzer (requires ANTHROPIC_API_KEY in env).",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    try:
        return _main(argv)
    except KeyboardInterrupt:
        return 130


def _main(argv: list[str] | None) -> int:
    args = parse_args(argv)

    if shutil.which("skill-scanner") is None:
        emit(
            "INFO",
            "(scanner)",
            "Skill scanner",
            "skill-scanner not installed; Tier-1 scanner audit skipped",
            f"Install with: {INSTALL_HINT}",
        )
        return 0

    if args.llm and not (
        os.environ.get("ANTHROPIC_API_KEY")
        or os.environ.get("SKILL_SCANNER_LLM_API_KEY")
    ):
        print(
            "scan_cisco.py: --llm requested but ANTHROPIC_API_KEY is not set",
            file=sys.stderr,
        )
        return 64

    skill_dirs = discover_skill_dirs(args.paths)
    if not skill_dirs:
        return 0

    any_fail = False
    for skill_dir in skill_dirs:
        try:
            data = run_scanner(skill_dir, args.llm)
        except (OSError, json.JSONDecodeError) as exc:
            emit(
                "WARN",
                str(skill_dir),
                "Skill scanner",
                f"scanner invocation failed: {exc}",
                "Re-run skill-scanner manually and inspect output.",
            )
            continue
        for finding in data.get("findings", []):
            mapped = map_finding(finding, skill_dir)
            if mapped is None:
                continue
            sev, *rest = mapped
            emit(sev, *rest)
            if sev == "FAIL":
                any_fail = True
    return 1 if any_fail else 0


if __name__ == "__main__":
    sys.exit(main())
