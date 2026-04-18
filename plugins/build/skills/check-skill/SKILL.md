---
name: check-skill
description: >
  Audit an existing SKILL.md for quality issues. Use when the user wants
  to "audit a skill", "review a skill", "check skill quality", "find
  problems in a skill", or "improve a skill".
argument-hint: "[path/to/SKILL.md — omit to audit all skills]"
user-invocable: true
---

# Check Skill

Audit one skill or all skills against twenty-two research-backed quality criteria,
then offer an opt-in repair loop.

## Workflow

### 1. Determine Scope

- **Argument provided** — audit that single SKILL.md
- **No argument** — walk `skills/` and audit all non-`_shared` subdirectories

### 2. Run Static Checks

```bash
# Prerequisite: pip install -e plugins/build
python3 <plugin-scripts-dir>/../../src/check/lint.py --root <project-root> --no-urls
```

Extract findings for the target skill(s). Static checks run deterministically
and always precede LLM checks. They cover:

- **Body length** — warn at >500 non-blank lines (criterion #1)
- **ALL-CAPS directive density** — warn at ≥3 MUST/NEVER/ALWAYS/REQUIRED/FORBIDDEN (criterion #2)
- **`allowed-tools` shape** — fail on comma-separated-as-string (canonical: space-separated or YAML list)
- **Description cap** — fail at >1024 chars; when `when_to_use` is present, fail at >1536 combined
- **Description quality** — warn on second-person ("you can", "I will"), vague phrasings ("helps with", "processes data"), or XML tags
- **Reserved words in name** — fail on `anthropic` or `claude` (platform-owned namespaces)
- **Windows-style paths** — fail on backslash path separators in fenced blocks or inline code (drive-letter prefixes, relative `.\` / `..\` prefixes, or multi-component paths with file extensions)
- **Substitution usage** — warn when `argument-hint` is set but the body has no `$ARGUMENTS`, `$ARGUMENTS[N]`, or `$N` substitution; without one, the user-supplied argument lands at the end as `ARGUMENTS: <value>`
- **Gerund/vague naming** — warn on vague tokens (`helper`, `utils`, `tools`, `thing`, etc.) anywhere in the name; warn on names that aren't in gerund (`-ing`) or agent-noun (`-er`) form (style suggestion only)

### 3. Run LLM Checks

For each skill, read the SKILL.md body and assess the remaining twenty criteria:

**Category key:** **canonical** = enforces a documented Anthropic requirement. **best-practice** = recommended by Anthropic best-practices, not binding. **toolkit-opinion** = house style with no spec backing; flagged only when a trigger condition elevates the finding.

**Structural checks:**

| # | Check | Category | Pass condition |
|---|-------|----------|---------------|
| 3 | Handoff completeness | toolkit-opinion | `## Handoff` section present; all three fields populated (Receives / Produces / Chainable-to); Receives and Produces use concrete, specific descriptors — not generic placeholders like "document", "output", or "data" that leave scope ambiguous |
| 4 | Anti-pattern guards | toolkit-opinion | `## Anti-Pattern Guards` section present with at least one guard |
| 5 | Gate checks | best-practice | At least one explicit gate (user approval, lint verification, precondition) before a consequential step |
| 6 | Examples | best-practice | At least one concrete example — illustrative invocation, sample output, or table row with a real case |
| 7 | Description routing quality | canonical | First sentence front-loads the primary trigger phrase; no second-person ("you can", "you should") or passive voice; description contains a distinct WHAT element (what the skill accomplishes or produces) and a WHEN element (trigger conditions or scenarios), both identifiable without inference. If routing behavior is uncertain after static assessment, flag as "recommend trigger evaluation": generate 8–10 should-trigger queries and 8–10 should-NOT-trigger queries (near-miss cases), test each against the skill's description — pass when both hit rates exceed 80%. |
| 11 | Won't-do scope | toolkit-opinion | `## Key Instructions` contains at least one explicit scope exclusion ("Won't…", "Does not…", "Excluded:", or equivalent negative boundary statement). Acceptable pass if the skill's entire Workflow is read-only and the Handoff Receives/Produces fields unambiguously constrain scope with no plausible overreach. |
| 13 | Routing guidance placement | canonical | The skill body contains no sections titled or framed as "When to Use This Skill", "When to invoke", or equivalent routing-condition guidance. All trigger conditions must appear in the `description` frontmatter — the body is loaded after triggering and routing guidance inside it is never evaluated at routing time. |
| 14 | Workflow step ordering | best-practice | If the skill describes a multi-step workflow with ≥3 sequential steps, each step is numbered, explicitly ordered, and any data-flow or dependency between steps is stated — not implied. |
| 15 | Critical instructions placement | toolkit-opinion | The most consequential rules (irreversible actions, hard constraints, scope limits) appear at the top of `## Key Instructions`, not buried mid-section. |
| 17 | Frontmatter completeness | canonical | `name` and `description` are present and non-empty; if `paths` is set, all glob patterns are syntactically valid (no unmatched brackets, valid wildcard usage). |
| 18 | Fork isolation boundary | canonical | If `context: fork` appears in frontmatter, `## Key Instructions` explicitly states the subagent's operational scope (read-only, write-gated, requires approval, etc.) and that scope is consistent with the `allowed-tools` field if present. |
| 20 | Argument-hint present | best-practice | If the skill accepts arguments (evidenced by Workflow steps, Handoff Receives field, or invoke examples referencing user-provided input), `argument-hint` is set in frontmatter with a concrete placeholder (e.g., `[path/to/file]`, `[issue-number]`). |
| 22 | Iteration termination | toolkit-opinion | If the Workflow includes looping or retry logic ("repeat until", "try again", "re-run"), `## Key Instructions` or the Workflow step states an explicit termination condition (exit criterion, maximum attempt count, or convergence signal). |
| 23 | Disable-model-invocation | canonical | If the skill's Workflow or Key Instructions describe operations that are destructive, irreversible, or carry significant unintended-invocation risk (deploy, rm -rf, DROP TABLE, force-push, external write API), `disable-model-invocation: true` is set in frontmatter to prevent auto-triggering. |

**Content-quality checks (from HIGH-evidence research anti-patterns):**

| # | Check | Category | Pass condition |
|---|-------|----------|---------------|
| 8 | Vagueness | best-practice | Each rule produces a consistent decision; two developers reading it would make the same choice in the same situation |
| 9 | Removal test | best-practice | Each significant rule would cause a mistake if removed; rules that restate model defaults or code-visible conventions are noise |
| 10 | Persona framing | best-practice | No "act as X" or "you are a senior X expert" constructions; OpenSSF 2025 found persona framing reduces performance on the intended tasks |
| 12 | Contradiction-free | best-practice | No two rules in the skill body produce explicitly opposite directives for the same scenario. Flag as fail only when Rule A says "always X" and Rule B says "never X" in the same or overlapping trigger context within `## Key Instructions` or `## Anti-Pattern Guards`. Semantic tension and trade-off language ("prefer X unless Y") is not a contradiction. |
| 16 | Edge case handling | best-practice | The skill explicitly addresses at least one failure mode: missing or ambiguous input, a precondition that isn't met, or a mid-workflow failure. A gate check (#5) that blocks on missing input counts; a Workflow step that says "if X is unavailable, do Y" counts. Silence on all failure modes is a fail. |
| 21 | Reversibility | best-practice | If the skill performs irreversible or high-impact operations (file deletion, git reset, commit, deploy, external API write), `## Key Instructions` or `## Handoff` documents how to revert or recover from an unintended execution (e.g., "use `git reflog` to recover", "review with `/diff` before confirming"). |

**Note on directive density (check #2):** newer frontier models respond better
to rationale-based instructions than directives. When flagging ALL-CAPS density
≥3: (a) if `tested_with` is present and lists only sub-frontier models (e.g.,
haiku), downgrade to informational — stronger directives are calibrated
differently for lower-tier targets; (b) for all other cases, suggest the
transformation pattern: convert "ALWAYS X" to "X — because [reason why X
matters in this skill's context]." This produces smarter adaptation than
compliance enforcement.

### 4. Report Findings

Output a findings table:

```
| File | Issue | Severity |
|------|-------|----------|
| skills/foo/SKILL.md | Missing ## Handoff section | warn |
```

Summary line at top and bottom: `N fail, N warn` across N skills.
Sort: fail before warn; structural (checks 3–7, 11, 13–15, 17, 18, 20, 22, 23) before content-quality (8–10, 12, 16, 21).

### 5. Opt-In Repair Loop

After presenting findings, ask:

> "Apply fixes? Enter y (all), n (skip), or comma-separated numbers."

For each selected finding:
1. Read the relevant section of the SKILL.md
2. Propose a minimal specific edit — fix the finding without restructuring surrounding content
3. Show the diff
4. Write the change only on user confirmation
5. Re-run `scripts/lint.py` after each applied fix

## Anti-Pattern Guards

1. **Running LLM checks before `scripts/lint.py`** — static checks are deterministic and fast; always run them first
2. **Applying all fixes at once** — per-change confirmation is required; bulk application removes the user's ability to review individual changes
3. **Auditing `skills/_shared/`** — this directory holds shared references, not invocable skills; exclude it from all-skill audits

## Handoff

**Receives:** Path to a SKILL.md (or no argument for all-skills audit)
**Produces:** Structured findings table in `scripts/lint.py` format (file, issue, severity); optionally, targeted edits applied to the audited skill(s)
**Chainable to:** build-skill (to create a replacement), start-work (for bulk repair across skills)

## Key Instructions

- Exclude `skills/_shared/` from all-skill audits
- Do not modify `wos/skill_audit.py` — the static checks are authoritative; this skill adds LLM-level judgment on top
- When proposing edits, keep changes minimal — fix the finding without restructuring surrounding content
- Checks 8 and 9 (vagueness, removal test) are the highest-value content-quality checks; prioritize surfacing them clearly
