---
name: audit
description: >
  Full project health check — orchestrates lint, audit-skill, audit-rule,
  audit-chain, and wiki validation into a single prioritized report. Use
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
| **High** | `scripts/lint.py` `warn` findings; `fail` findings from audit-skill and audit-rule |
| **Medium** | `warn` findings from audit-skill, audit-rule, and audit-chain; `fail` findings from wiki validation |
| **Low** | `warn` findings from audit-chain and wiki validation |

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

Invoke `/wos:audit-skill` with no argument to audit all skills. Collect
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

If any rules exist: invoke `/wos:audit-rule` with no argument. Collect
all findings. Tag rule `fail` → High, rule `warn` → Medium.

If no rules found: note "No rules found — skipping rule audit."

### Step 4 — Chain Health (conditional)

Check for `*.chain.md` files anywhere in the project. If any exist:
invoke `/wos:audit-chain` on each, in manifest mode. Collect all findings.
Tag chain `fail` → High, chain `warn` → Medium.

If no chain files found: note "No chain manifests found — skipping chain audit."

### Step 5 — Wiki Health (conditional)

Check for `wiki/SCHEMA.md`. If it exists, wiki validation runs automatically
as part of Step 1's `scripts/lint.py` output — parse out any wiki-tagged
findings and re-tag them: wiki `fail` → Medium, wiki `warn` → Low.

If `wiki/SCHEMA.md` does not exist: note "No wiki schema found — skipping wiki audit."

### Step 6 — Consolidated Report

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

### Step 7 — Repair Offer

After the report, ask:

> "Would you like to address these findings now? I'll work through them in priority order."

If yes: start at Critical findings, invoke the relevant sub-audit skill's
repair loop for each tier in order (Critical → High → Medium → Low).

- Critical findings: walk through each `scripts/lint.py` finding with the
  user; offer targeted fixes via the lint skill's cleanup actions
- High/Medium findings from skill audit: invoke `/wos:audit-skill` repair loop
- High/Medium findings from rule audit: invoke `/wos:audit-rule` repair loop
- Medium/Low findings from chain audit: invoke `/wos:audit-chain` repair loop

Do not apply any fix without per-finding user confirmation.

## Anti-Pattern Guards

1. **Running LLM checks before `scripts/lint.py`** — structural checks are
   deterministic and fast; always run them first. Structural failures can
   produce misleading LLM findings.
2. **Auto-applying fixes** — the repair offer is opt-in and per-finding.
   Never modify files without explicit user confirmation.
3. **Running chain or wiki checks unconditionally** — these steps are
   conditional on file existence. Running them on projects without those
   artifacts produces noise and wastes context.
4. **Omitting sub-check attribution** — every finding in the consolidated
   report must identify which sub-check produced it. "Missing ## Handoff"
   without "source: audit-skill" is not actionable.
5. **Treating a clean lint as a clean audit** — structural validity does not
   imply quality. Steps 2–5 add LLM-judgment on top of deterministic checks.

## Handoff

**Receives:** Project root path (defaults to CWD)
**Produces:** Prioritized health report with Critical/High/Medium/Low tiers,
sub-check attribution on each finding, and summary line; optionally triggers
sub-skill repair loops on user confirmation
**Chainable to:** lint (structural repair), audit-skill (skill repair loop),
audit-rule (rule repair loop), audit-chain (chain repair loop)
