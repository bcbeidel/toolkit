#!/usr/bin/env python3
"""Evaluate skill-scanner findings and produce risk-summary.json.

Step 1 of the split evaluator/comment-writer architecture. Reads scanner
findings (rule_id, severity, analyzer, description per finding) and asks
Claude for a 2-3 sentence narrative plus the top findings. Raw skill
content is never passed to this step — only structured scanner metadata —
so prompt injection from skill text cannot reach the LLM call.

The output schema (risk-summary.json) must not contain skill_text,
excerpt, snippet, or any raw skill content. The downstream comment-writer
trusts that contract.

Example:
    FINDINGS_FILE=findings.json SUMMARY_FILE=risk-summary.json \\
      ./evaluate-findings.py findings.json risk-summary.json

Dependencies: anthropic (declared in .github/scripts/requirements.lock).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path

import anthropic

EXIT_USAGE = 2
EXIT_INTERRUPTED = 130

SEVERITY_ORDER = {"CRITICAL": 4, "HIGH": 3, "MEDIUM": 2, "LOW": 1, "UNKNOWN": 0}
DEFAULT_MODEL = "claude-opus-4-6"
DEFAULT_POLICY_PATH = "policy/skill-scan-policy.yml"


def policy_fingerprint(policy_file: Path) -> str:
    try:
        return "sha256:" + hashlib.sha256(policy_file.read_bytes()).hexdigest()
    except FileNotFoundError:
        return "sha256:missing"


def parse_simple_yaml_list(policy_file: Path, key: str) -> list[str]:
    """Extract a flat list of `- value` items under a top-level YAML key.

    Avoids requiring PyYAML in CI (keeps the install small/fast).
    """
    out: list[str] = []
    in_block = False
    try:
        with policy_file.open(encoding="utf-8") as f:
            for raw in f:
                line = raw.rstrip()
                if line.startswith(f"{key}:"):
                    in_block = True
                    continue
                if in_block:
                    if line and not line.startswith((" ", "\t", "-", "#")):
                        break
                    stripped = line.strip()
                    if stripped.startswith("- "):
                        out.append(stripped[2:].strip())
    except FileNotFoundError:
        return []
    return out


def load_findings(findings_file: Path) -> tuple[list[dict], bool]:
    """Load scanner findings and extract only structured metadata.

    Returns (findings, scan_failed). Raw skill content (skill_text,
    excerpt, snippet, etc.) is discarded — never forwarded.
    """
    if not findings_file.exists():
        print(
            f"findings file not found: {findings_file} — treating as scan failure",
            file=sys.stderr,
        )
        return [], True

    try:
        data = json.loads(findings_file.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"failed to parse findings JSON: {e}", file=sys.stderr)
        return [], True

    scan_failed = bool(data.get("scan_failed", False))

    if "results" in data:
        raw_findings = [f for r in data["results"] for f in r.get("findings", [])]
    else:
        raw_findings = data.get("findings", [])

    structured = [
        {
            "rule_id": str(f.get("rule_id", "UNKNOWN"))[:100],
            "severity": str(f.get("severity", "UNKNOWN")).upper(),
            "analyzer": str(f.get("analyzer", "unknown"))[:100],
            "description": str(f.get("description", "No description"))[:500],
        }
        for f in raw_findings
    ]
    return structured, scan_failed


def apply_escalation(
    findings: list[dict],
    escalation_signals: list[str],
    critical_signals: list[str],
) -> list[dict]:
    """Bump severity by one level when a finding matches an escalation signal.

    Match against `critical_signals` first → CRITICAL outright.
    Case-insensitive substring match across description + rule_id.
    """
    bump = {
        "LOW": "MEDIUM",
        "MEDIUM": "HIGH",
        "HIGH": "HIGH",
        "CRITICAL": "CRITICAL",
        "UNKNOWN": "UNKNOWN",
    }
    for f in findings:
        haystack = (f["description"] + " " + f["rule_id"]).lower()
        if any(sig.lower() in haystack for sig in critical_signals):
            f["severity"] = "CRITICAL"
            continue
        if any(sig.lower() in haystack for sig in escalation_signals):
            f["severity"] = bump.get(f["severity"], f["severity"])
    return findings


def compute_overall_severity(findings: list[dict]) -> str:
    severities = {f["severity"] for f in findings}
    if "CRITICAL" in severities or "HIGH" in severities:
        return "high"
    if "MEDIUM" in severities:
        return "medium"
    if "LOW" in severities:
        return "low"
    return "none"


def call_evaluator(
    client: anthropic.Anthropic,
    model: str,
    plugin_name: str,
    findings: list[dict],
) -> dict:
    """Ask Claude for a narrative + recommendation only.

    The findings table is rendered deterministically by write-comment.py;
    the LLM contributes only the human-readable framing.
    """
    severity_counts = {
        sev: sum(1 for f in findings if f["severity"] == sev)
        for sev in ("CRITICAL", "HIGH", "MEDIUM", "LOW")
    }

    sample = findings[:20]

    prompt = (
        f"Plugin: {plugin_name}\n"
        f"Total findings: {len(findings)}\n"
        f"Severity breakdown: "
        f"CRITICAL={severity_counts['CRITICAL']}, "
        f"HIGH={severity_counts['HIGH']}, "
        f"MEDIUM={severity_counts['MEDIUM']}, "
        f"LOW={severity_counts['LOW']}\n\n"
        f"Highest-severity findings (structured metadata only, up to 20):\n"
        f"{json.dumps(sample, indent=2)}\n\n"
        "Produce a JSON object with exactly these fields:\n"
        '- "narrative": 2–3 sentence summary of the security posture\n'
        '- "recommendation": one sentence on what the reviewer should do\n\n'
        "Return only valid JSON. No markdown fences, no explanation."
    )

    response = client.messages.create(
        model=model,
        max_tokens=1024,
        system=[
            {
                "type": "text",
                "text": (
                    "You are a security analyst reviewing Claude Code skill scan results. "
                    "You receive only structured scan metadata (rule IDs, severities, "
                    "analyzer names, short descriptions) — never raw skill content. "
                    "Produce concise, accurate risk summaries. Output only valid JSON."
                ),
                "cache_control": {"type": "ephemeral"},
            }
        ],
        messages=[{"role": "user", "content": prompt}],
    )

    try:
        return json.loads(response.content[0].text)
    except (json.JSONDecodeError, IndexError) as e:
        print(f"warning: could not parse Claude response as JSON: {e}", file=sys.stderr)
        return {}


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Evaluate skill-scanner findings and write risk-summary.json.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "findings_file", type=Path, help="Path to scanner findings JSON."
    )
    parser.add_argument(
        "summary_file", type=Path, help="Path to write risk-summary.json."
    )
    return parser


def run(args: argparse.Namespace) -> int:
    plugin_name = os.environ.get("PLUGIN_NAME", "unknown-plugin")
    policy_file = Path(os.environ.get("POLICY_FILE", DEFAULT_POLICY_PATH))
    scanner_version = os.environ.get("SCANNER_VERSION", "unknown")
    model = os.environ.get("EVALUATOR_MODEL", DEFAULT_MODEL)
    commit_sha = os.environ.get("GIT_COMMIT_SHA", "")

    findings, scan_failed = load_findings(args.findings_file)

    escalation_signals = parse_simple_yaml_list(policy_file, "escalation_signals")
    critical_signals = parse_simple_yaml_list(policy_file, "critical_signals")
    findings = apply_escalation(findings, escalation_signals, critical_signals)

    # Sort by severity desc once; this ordering is what the comment renders.
    findings.sort(
        key=lambda f: SEVERITY_ORDER.get(f["severity"], 0),
        reverse=True,
    )

    overall_severity = compute_overall_severity(findings)
    if scan_failed:
        overall_severity = "high"

    summary: dict = {}
    if findings and not scan_failed:
        client = anthropic.Anthropic()
        summary = call_evaluator(client, model, plugin_name, findings)

    # Authoritative fields the LLM cannot override.
    summary["overall_severity"] = overall_severity
    summary["finding_count"] = len(findings)
    summary["findings"] = findings
    summary["scan_failed"] = scan_failed
    summary["policy_fingerprint"] = policy_fingerprint(policy_file)
    summary["scanner_version"] = scanner_version
    summary["model_used"] = model
    if commit_sha:
        summary["commit_sha"] = commit_sha

    summary.setdefault(
        "narrative",
        "Scan failed — no findings could be produced."
        if scan_failed
        else f"Scan completed for {plugin_name}. {len(findings)} finding(s) detected.",
    )
    summary.setdefault(
        "recommendation",
        "Scan failed; do not merge until the workflow runs successfully."
        if scan_failed
        else "Review the findings above before merging.",
    )

    args.summary_file.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"risk summary written to: {args.summary_file}")
    print(
        f"overall severity: {overall_severity} "
        f"({len(findings)} finding(s), scan_failed={scan_failed})"
    )
    return 0


def main(argv: list[str] | None = None) -> int:
    args = get_parser().parse_args(argv)
    try:
        return run(args)
    except KeyboardInterrupt:
        return EXIT_INTERRUPTED


if __name__ == "__main__":
    sys.exit(main())
