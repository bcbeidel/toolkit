#!/usr/bin/env python3
"""Render a risk-summary.json as a GitHub PR audit comment.

Step 2 of the split evaluator/comment-writer architecture. Receives only
the structured risk summary produced by evaluate-findings.py — never raw
skill content — and renders it deterministically as Markdown. No LLM call:
the narrative + recommendation already live in the summary; the table and
provenance are pure templating. This makes the comment reproducible and
removes truncation risk for plugins with many findings.

The output always begins with the stable marker `<!-- skill-audit:report -->`
so post-audit-comment.sh can upsert by HTML comment match.

Example:
    ./write-comment.py risk-summary.json audit-comment.md
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

EXIT_INTERRUPTED = 130

COMMENT_MARKER = "<!-- skill-audit:report -->"

SEVERITY_BADGE = {
    "none": "![none](https://img.shields.io/badge/severity-none-brightgreen)",
    "low": "![low](https://img.shields.io/badge/severity-low-yellow)",
    "medium": "![medium](https://img.shields.io/badge/severity-medium-orange)",
    "high": "![high](https://img.shields.io/badge/severity-HIGH-red)",
}

MERGE_BLOCKED_NOTICE = (
    "⛔ **MERGE BLOCKED** — the security scan failed and could not "
    "produce findings. Resolve the workflow error before merging."
)


def _md_escape_cell(text: str) -> str:
    """Make a string safe to drop into a Markdown table cell on one line."""
    return str(text).replace("|", "\\|").replace("\r", " ").replace("\n", " ").strip()


def render_findings_table(findings: list[dict]) -> str:
    if not findings:
        return "_No findings._"
    header = "| # | Severity | Analyzer | Rule | Description |\n|---|---|---|---|---|\n"
    rows = [
        "| {idx} | {sev} | {analyzer} | {rule} | {desc} |".format(
            idx=i,
            sev=_md_escape_cell(f.get("severity", "UNKNOWN")),
            analyzer=_md_escape_cell(f.get("analyzer", "unknown")),
            rule=_md_escape_cell(f.get("rule_id", "UNKNOWN")),
            desc=_md_escape_cell(f.get("description", "")),
        )
        for i, f in enumerate(findings, start=1)
    ]
    return header + "\n".join(rows) + "\n"


def render_comment(plugin_name: str, summary: dict) -> str:
    severity = summary.get("overall_severity", "none")
    badge = SEVERITY_BADGE.get(severity, SEVERITY_BADGE["none"])
    findings = summary.get("findings", [])
    finding_count = summary.get("finding_count", len(findings))
    scan_failed = bool(summary.get("scan_failed", False))

    parts: list[str] = [
        COMMENT_MARKER,
        "",
        f"## Security Audit: {plugin_name}",
        "",
        badge,
        "",
    ]

    if scan_failed:
        parts.extend([MERGE_BLOCKED_NOTICE, ""])
    else:
        narrative = summary.get(
            "narrative",
            f"Scan completed for {plugin_name}. {finding_count} finding(s) detected.",
        )
        parts.extend([narrative, ""])

    parts.extend(
        [
            f"### Findings ({finding_count})",
            "",
            render_findings_table(findings),
            "",
        ]
    )

    recommendation = summary.get(
        "recommendation",
        "Review the findings above before merging.",
    )
    parts.extend([f"**Recommendation:** {recommendation}", ""])

    parts.extend(
        [
            "---",
            "",
            "**Provenance:**",
            f"- Scanner: `{summary.get('scanner_version', 'unknown')}`",
            f"- Evaluator model: `{summary.get('model_used', 'unknown')}`",
            f"- Policy fingerprint: `{summary.get('policy_fingerprint', 'unknown')}`",
        ]
    )
    if summary.get("commit_sha"):
        parts.append(f"- Commit: `{summary['commit_sha']}`")
    parts.extend(
        [
            "",
            "*Assessed by [skill-scanner](https://github.com/cisco-ai-defense/skill-scanner) "
            "+ Claude evaluator.*",
            "",
        ]
    )

    return "\n".join(parts)


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Render risk-summary.json as a GitHub PR audit comment.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("summary_file", type=Path, help="Path to risk-summary.json.")
    parser.add_argument(
        "comment_file", type=Path, help="Path to write the Markdown comment."
    )
    return parser


def run(args: argparse.Namespace) -> int:
    plugin_name = os.environ.get("PLUGIN_NAME", "unknown-plugin")
    try:
        summary = json.loads(args.summary_file.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"error loading summary file: {e}", file=sys.stderr)
        return 1

    body = render_comment(plugin_name, summary)
    args.comment_file.write_text(body, encoding="utf-8")
    print(f"PR comment written to: {args.comment_file}")
    return 0


def main(argv: list[str] | None = None) -> int:
    args = get_parser().parse_args(argv)
    try:
        return run(args)
    except KeyboardInterrupt:
        return EXIT_INTERRUPTED


if __name__ == "__main__":
    sys.exit(main())
