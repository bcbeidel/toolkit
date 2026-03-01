---
name: report-issue
description: >
  Use when the user wants to "report a bug", "submit feedback",
  "request a feature", "file an issue", or when you discover
  a problem, limitation, or missing capability in WOS during
  normal work. Proactively suggest filing when you encounter
  WOS issues the maintainer should know about.
argument-hint: "[describe the issue or feedback]"
user-invocable: true
references:
  - references/issue-templates.md
  - references/report-issue-submit.md
---

# Report-Issue Skill

Submit bug reports, feature requests, and feedback to the wos
source repository via GitHub Issues.

## Workflow

This is a linear workflow — no routing needed. All requests follow
the same gather → dedupe → draft → submit pipeline.

Follow the steps in `references/report-issue-submit.md`.

## Key Rules

- **Always preview before submitting.** Show the formatted issue draft
  and get explicit approval before running `gh issue create`.
- **Check `gh` first.** Verify the CLI is installed and authenticated
  before gathering details. If missing, show setup instructions.
- **Target repo is hardcoded:** `bcbeidel/wos`
- **Include context automatically:** wos version from plugin.json,
  Python version, platform info.
- **Never submit without approval.** The user must explicitly confirm.
