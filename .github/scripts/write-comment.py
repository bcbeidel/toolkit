#!/usr/bin/env python3
"""Format a risk-summary.json as a GitHub PR audit comment.

Step 2 of the split evaluator/comment-writer architecture. Receives only
the structured risk summary produced by evaluate-findings.py — never raw
skill content — and formats it as Markdown via Claude. Skill content never
reaches this step, so a malicious skill cannot inject instructions into
the posted security report.

The output always begins with the stable marker `<!-- skill-audit:report -->`
so post-audit-comment.sh can upsert by HTML comment match.

Example:
    ./write-comment.py risk-summary.json audit-comment.md

Dependencies: anthropic (declared in .github/scripts/requirements.lock).
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

import anthropic

EXIT_INTERRUPTED = 130

DEFAULT_MODEL = "claude-opus-4-6"
COMMENT_MARKER = "<!-- skill-audit:report -->"

SEVERITY_BADGE = {
    "none": "![none](https://img.shields.io/badge/severity-none-brightgreen)",
    "low": "![low](https://img.shields.io/badge/severity-low-yellow)",
    "medium": "![medium](https://img.shields.io/badge/severity-medium-orange)",
    "high": "![high](https://img.shields.io/badge/severity-HIGH-red)",
}


def build_prompt(plugin_name: str, summary: dict) -> str:
    return (
        f"Plugin: `{plugin_name}`\n\n"
        f"Risk Summary (structured data — no raw skill content):\n"
        f"{json.dumps(summary, indent=2)}\n\n"
        "Format this as a GitHub PR comment in Markdown. Structure:\n"
        f"1. Header: `## Security Audit: {plugin_name}`\n"
        "2. Severity badge on its own line\n"
        "3. If `scan_failed` is true, lead with a clear MERGE BLOCKED notice; "
        "otherwise the narrative paragraph\n"
        "4. A Markdown table of top findings: | Severity | Analyzer | Description |\n"
        "   (omit the table if there are no findings)\n"
        "5. **Recommendation:** line\n"
        "6. A compact provenance footer with: scanner_version, model_used, "
        "policy_fingerprint, and "
        "`*Assessed by [skill-scanner](https://github.com/cisco-ai-defense/skill-scanner) + "
        "Claude evaluator*`\n\n"
        "Keep it concise and actionable. Do not reproduce raw skill content. "
        "Output only the Markdown comment body."
    )


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Format risk-summary.json as a GitHub PR audit comment.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("summary_file", type=Path, help="Path to risk-summary.json.")
    parser.add_argument(
        "comment_file", type=Path, help="Path to write the Markdown comment."
    )
    return parser


def run(args: argparse.Namespace) -> int:
    plugin_name = os.environ.get("PLUGIN_NAME", "unknown-plugin")
    model = os.environ.get("EVALUATOR_MODEL", DEFAULT_MODEL)

    try:
        summary = json.loads(args.summary_file.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"error loading summary file: {e}", file=sys.stderr)
        return 1

    severity = summary.get("overall_severity", "none")
    summary["_severity_badge"] = SEVERITY_BADGE.get(severity, SEVERITY_BADGE["none"])

    client = anthropic.Anthropic()
    response = client.messages.create(
        model=model,
        max_tokens=1024,
        system=[
            {
                "type": "text",
                "text": (
                    "You are a security report formatter for GitHub pull requests. "
                    "You receive only structured risk summaries — never raw skill content. "
                    "Format summaries as clear, concise, actionable Markdown PR comments. "
                    "Do not reference or reproduce any skill source content."
                ),
                "cache_control": {"type": "ephemeral"},
            }
        ],
        messages=[{"role": "user", "content": build_prompt(plugin_name, summary)}],
    )

    body = response.content[0].text
    args.comment_file.write_text(f"{COMMENT_MARKER}\n{body}\n", encoding="utf-8")
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
