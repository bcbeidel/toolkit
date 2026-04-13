---
name: audit
description: >
  Full project health check — orchestrates lint, check-skill, check-rule,
  check-skill-chain, and wiki validation into a single prioritized report. Use
  when the user wants to "audit the project", "run a health check", "check
  project quality", "find all issues", "what's wrong with this project", or
  "get a full quality report".
argument-hint: "[project root — defaults to CWD]"
user-invocable: true
---

# /wos:audit

Orchestrate a full project health check. Run deterministic structural checks
first, then LLM-judgment checks from the audit family, then consolidate all
findings into a single prioritized report.

**Announce at start:** "I'm using the `/wos:audit` skill to run a full project health check."

## Severity Tiers

| Tier | What goes here |
|------|---------------|
| **Critical** | `scripts/lint.py` `fail` findings — broken structure, missing required fields, unreachable URLs |
| **High** | `scripts/lint.py` `warn` findings; `fail` findings from check-skill, check-rule, and check-hook |
| **Medium** | `warn` findings from check-skill, check-rule, check-hook, and check-skill-chain; `fail` findings from wiki validation |
| **Low** | `warn` findings from check-skill-chain and wiki validation |

## Workflow

### Step 1 — Structural Check (always runs)

```bash
python <plugin-scripts-dir>/lint.py --root . --no-urls
```

Collect all findings. Tag `fail` → Critical, `warn` → High.

Do not skip this step or run LLM checks before it. Structural failures
indicate the project is in a broken state that LLM checks cannot reason
about reliably.

### Step 2 — Skill Quality (always runs)

Invoke `/wos:check-skill` with no argument to check all skills. Collect
all findings from the findings table it produces.

Tag skill `fail` → High, skill `warn` → Medium.

If `skills/` does not exist or contains no non-`_shared` subdirectories,
note: "No skills found — skipping skill audit."

### Step 3 — Rule Quality (conditional)

Discover rules:

| Format | Location |
|--------|----------|
| WOS | `docs/rules/*.rule.md` |
| Cursor | `.cursor/rules/*.mdc` |
| Claude Code | `## Rule:` sections in `CLAUDE.md` |

If any rules exist: invoke `/wos:check-rule` with no argument. Collect
all findings. Tag rule `fail` → High, rule `warn` → Medium.

If no rules found: note "No rules found — skipping rule audit."

### Step 4 — Chain Health (conditional)

Check for `*.chain.md` files anywhere in the project. If any exist:
invoke `/wos:check-skill-chain` on each, in manifest mode. Collect all findings.
Tag skill-chain `fail` → High, skill-chain `warn` → Medium.

If no chain files found: note "No skill-chain manifests found — skipping skill-chain audit."

### Step 5 — Hook Quality (conditional)

Check for a `hooks:` key in `.claude/settings.json` or `.claude/settings.local.json`.
If hooks are configured: invoke `/wos:check-hook` with no argument. Collect all findings.
Tag hook `fail` → High, hook `warn` → Medium.

If no hooks configured: note "No hooks configured — skipping hook audit."

### Step 6 — Wiki Health (conditional)

Check for `wiki/SCHEMA.md`. If it exists, wiki validation runs automatically
as part of Step 1's `scripts/lint.py` output — parse out any wiki-tagged
findings and re-tag them: wiki `fail` → Medium, wiki `warn` → Low.

If `wiki/SCHEMA.md` does not exist: note "No wiki schema found — skipping wiki audit."

### Step 7 — Consolidated Report

Emit the health report. Print each tier only when it has findings. Print
sources (the sub-check and file) alongside each finding.

```
## Project Health Report

### Critical (fix before shipping)
[structural failures from lint — file, issue]

### High (degrade self-improvement loop)
[lint warns, skill fails, rule fails]

### Medium (degrade over time)
[skill warns, rule warns, chain fails, wiki fails]

### Low (advisory)
[chain warns, wiki warns]
```

When the Critical tier is empty: add a line at the top: "No critical issues found."

When all four tiers are empty: print only: "All checks passed."

Print a summary line at the bottom:
`N findings: X critical, X high, X medium, X low | across N sub-checks`

### Step 8 — Repair Offer

After the report, ask:

> "Would you like to address these findings now? I'll work through them in priority order."

If yes: start at Critical findings, invoke the relevant sub-audit skill's
repair loop for each tier in order (Critical → High → Medium → Low).

- Critical findings: walk through each `scripts/lint.py` finding with the
  user; offer targeted fixes via the lint skill's cleanup actions
- High/Medium findings from skill audit: invoke `/wos:check-skill` repair loop
- High/Medium findings from rule audit: invoke `/wos:check-rule` repair loop
- High/Medium findings from hook audit: invoke `/wos:check-hook` repair loop
- Medium/Low findings from skill-chain audit: invoke `/wos:check-skill-chain` repair loop

Do not apply any fix without per-finding user confirmation.

## Anti-Pattern Guards

1. **Running LLM checks before `scripts/lint.py`** — structural checks are
   deterministic and fast; always run them first. Structural failures can
   produce misleading LLM findings.
2. **Auto-applying fixes** — the repair offer is opt-in and per-finding.
   Never modify files without explicit user confirmation.
3. **Running conditional checks unconditionally** — chain, hook, and wiki steps are
   conditional on file/config existence. Running them on projects without those
   artifacts produces noise and wastes context.
4. **Omitting sub-check attribution** — every finding in the consolidated
   report must identify which sub-check produced it. "Missing ## Handoff"
   without "source: check-skill" is not actionable.
5. **Treating a clean lint as a clean audit** — structural validity does not
   imply quality. Steps 2–5 add LLM-judgment on top of deterministic checks.

## Handoff

**Receives:** Project root path (defaults to CWD)
**Produces:** Prioritized health report with Critical/High/Medium/Low tiers,
sub-check attribution on each finding, and summary line; optionally triggers
sub-skill repair loops on user confirmation
**Chainable to:** lint (structural repair), check-skill (skill repair loop),
check-rule (rule repair loop), check-hook (hook repair loop), check-skill-chain (skill-chain repair loop)
