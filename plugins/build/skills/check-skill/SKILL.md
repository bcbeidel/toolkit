---
name: check-skill
description: >
  Audit an existing SKILL.md for quality issues. Use when the user wants
  to "audit a skill", "review a skill", "check skill quality", "find
  problems in a skill", or "improve a skill".
argument-hint: "[path/to/SKILL.md — omit to audit all skills]"
user-invocable: true
references:
  - ../../_shared/references/as-tool-contract.md
---

# Check Skill

Audit one skill or all skills against thirty-one research-backed quality criteria,
then offer an opt-in repair loop.

## Workflow

### 1. Determine Scope

- **Argument provided** — audit that single SKILL.md
- **No argument** — walk `skills/` and audit all non-`_shared` subdirectories

### 2. Run Static Checks

```bash
# Prerequisites: pip install -e plugins/build -e plugins/wiki
python3 plugins/wiki/scripts/lint.py --root <project-root> --no-urls
```

The linter lives in the wiki plugin and imports the `check` package from the
build plugin — both must be installed.

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
- **Reference depth** — warn on files nested more than one level under `references/`; flat structure keeps on-demand loading predictable
- **Reference TOC** — warn on reference files over 100 non-blank lines without a `## Table of Contents`, `## Contents`, or `## TOC` heading in the first 20 lines
- **MCP reference format** — warn on raw `mcp__<server>__<tool>` names in prose; prefer the shorter `Server:tool_name` form per Anthropic best-practices (raw form in code is fine — it's the actual invocation string)
- **Time-sensitive content** — warn on year references (`in 2025`, `as of 2024`) and version references (`v3.2`) outside `<details>` blocks; evergreen bodies should wrap historical content in `<details>` "old patterns" blocks
- **Embedded-script exits** — warn on bare `sys.exit(N)` or `exit N` in `python` / `bash` / `sh` / `zsh` fenced blocks without an explanatory comment on the same or immediately prior line ("solve don't punt")

### 3. Run LLM Checks

For each skill, read the SKILL.md body and assess the remaining twenty criteria:

**Category key:** **canonical** = enforces a documented Anthropic requirement. **best-practice** = recommended by Anthropic best-practices, not binding. **toolkit-opinion** = house style with no spec backing; flagged only when a trigger condition elevates the finding.

**Structural checks:**

| # | Check | Category | Pass condition |
|---|-------|----------|---------------|
| 3 | Handoff completeness | toolkit-opinion | **Trigger:** skill chains to another skill (references another skill by name in Workflow or Handoff), OR Workflow writes files, OR `context: fork` is set. **When triggered:** `## Handoff` section present; all three fields populated (Receives / Produces / Chainable-to); Receives and Produces use concrete, specific descriptors — not generic placeholders like "document", "output", or "data" that leave scope ambiguous. **Otherwise:** not flagged. |
| 4 | Anti-pattern guards | toolkit-opinion | **Trigger:** Workflow performs destructive or irreversible operations (deploy, rm -rf, DROP TABLE, force-push, external write API), OR external-effect operations (network writes, outbound messages). **When triggered:** `## Anti-Pattern Guards` section present with at least one guard that names a specific failure mode. **Otherwise:** not flagged. |
| 5 | Gate checks | best-practice | At least one explicit gate (user approval, lint verification, precondition) before a consequential step |
| 6 | Examples | best-practice | At least one concrete example — illustrative invocation, sample output, or table row with a real case |
| 7 | Description routing quality | canonical | First sentence front-loads the primary trigger phrase; no second-person ("you can", "you should") or passive voice; description contains a distinct WHAT element (what the skill accomplishes or produces) and a WHEN element (trigger conditions or scenarios), both identifiable without inference. If routing behavior is uncertain after static assessment, flag as "recommend trigger evaluation": generate 8–10 should-trigger queries and 8–10 should-NOT-trigger queries (near-miss cases), test each against the skill's description — pass when both hit rates exceed 80%. |
| 11 | Won't-do scope | toolkit-opinion | **Trigger:** Workflow performs destructive ops, OR skill's description overlaps with other skills in the same plugin/directory (overlap risk: same verb, similar trigger phrase). **When triggered:** `## Key Instructions` contains at least one explicit scope exclusion ("Won't…", "Does not…", "Excluded:", or equivalent negative boundary statement). **Otherwise:** not flagged. |
| 13 | Routing guidance placement | canonical | The skill body contains no sections titled or framed as "When to Use This Skill", "When to invoke", or equivalent routing-condition guidance. All trigger conditions must appear in the `description` frontmatter — the body is loaded after triggering and routing guidance inside it is never evaluated at routing time. |
| 14 | Workflow step ordering | best-practice | If the skill describes a multi-step workflow with ≥3 sequential steps, each step is numbered, explicitly ordered, and any data-flow or dependency between steps is stated — not implied. |
| 15 | Critical instructions placement | toolkit-opinion | **Trigger:** `## Key Instructions` has ≥5 entries (placement matters at scale). **When triggered:** the most consequential rules (irreversible actions, hard constraints, scope limits) appear at the top of `## Key Instructions`, not buried mid-section. **Otherwise:** not flagged — short Key Instructions sections don't benefit from strict ordering. |
| 17 | Frontmatter completeness | canonical | `name` and `description` are present and non-empty; if `paths` is set, all glob patterns are syntactically valid (no unmatched brackets, valid wildcard usage). |
| 18 | Fork isolation boundary | canonical | If `context: fork` appears in frontmatter, `## Key Instructions` explicitly states the subagent's operational scope (read-only, write-gated, requires approval, etc.) and that scope is consistent with the `allowed-tools` field if present. |
| 20 | Argument-hint present | best-practice | If the skill accepts arguments (evidenced by Workflow steps, Handoff Receives field, or invoke examples referencing user-provided input), `argument-hint` is set in frontmatter with a concrete placeholder (e.g., `[path/to/file]`, `[issue-number]`). |
| 22 | Iteration termination | toolkit-opinion | **Trigger:** Workflow includes looping or retry logic ("repeat until", "try again", "re-run"). **When triggered:** `## Key Instructions` or the Workflow step states an explicit termination condition (exit criterion, maximum attempt count, or convergence signal). **Otherwise:** not flagged. |
| 23 | Disable-model-invocation | canonical | If the skill's Workflow or Key Instructions describe operations that are destructive, irreversible, or carry significant unintended-invocation risk (deploy, rm -rf, DROP TABLE, force-push, external write API), `disable-model-invocation: true` is set in frontmatter to prevent auto-triggering. |

**Content-quality checks (from HIGH-evidence research anti-patterns):**

| # | Check | Category | Pass condition |
|---|-------|----------|---------------|
| 8 | Vagueness | best-practice | Each rule produces a consistent decision; two developers reading it would make the same choice in the same situation |
| 9 | Removal test | best-practice | Each significant rule would cause a mistake if removed; rules that restate model defaults or code-visible conventions are noise |
| 10 | Affirmative rule phrasing | best-practice | Each rule states what *to* do, not what to avoid. "Don't X" must be rewritten as "Do Y instead" or paired with the affirmative alternative in the same rule. Negative phrasings are easier for the model to invert or miss than positive directives. Exceptions: explicit scope boundaries flagged by #11 ("this skill won't X") and failure-recovery steps flagged by #21 — those are identity/recovery statements, not instructional rules. |
| 12 | Contradiction-free | best-practice | No two rules in the skill body produce explicitly opposite directives for the same scenario. Flag as fail only when Rule A says "always X" and Rule B says "never X" in the same or overlapping trigger context within `## Key Instructions` or `## Anti-Pattern Guards`. Semantic tension and trade-off language ("prefer X unless Y") is not a contradiction. |
| 16 | Edge case handling | best-practice | The skill explicitly addresses at least one failure mode: missing or ambiguous input, a precondition that isn't met, or a mid-workflow failure. A gate check (#5) that blocks on missing input counts; a Workflow step that says "if X is unavailable, do Y" counts. Silence on all failure modes is a fail. |
| 21 | Reversibility | best-practice | If the skill performs irreversible or high-impact operations (file deletion, git reset, commit, deploy, external API write), `## Key Instructions` or `## Handoff` documents how to revert or recover from an unintended execution (e.g., "use `git reflog` to recover", "review with `/diff` before confirming"). |

**`--as-tool` contract checks (23–31):** dual-invocation support. These checks
only fire when a skill declares `skill-invocable: true` in frontmatter
(default is off). Skills without the field are unaffected — no migration
burden on the existing 41 skills. The shared mechanism spec lives at
[`../../_shared/references/as-tool-contract.md`](../../_shared/references/as-tool-contract.md).

| # | Check | Category | Severity | Pass condition |
|---|-------|----------|----------|---------------|
| 23 | `skill-invocable` frontmatter shape | canonical | warn | When `skill-invocable` is present, its value is boolean (`true`/`false` — YAML true/false literals or quoted strings). Non-boolean values warn. |
| 24 | `## --as-tool contract` section present | canonical | **fail** | When `skill-invocable: true`, the body contains a `## --as-tool contract` (or `## \`--as-tool\` contract`) H2 section, and that section is not empty. A declared-but-missing contract is runtime-breaking — callers cannot know the invocation shape. |
| 25 | Return shape declared | canonical | **fail** | Inside the contract section, a `**Return shape:**` line declares either `DATA` or `ARTIFACT`. |
| 26 | All three envelope cases documented | canonical | **fail** | The contract section mentions all three cases by name: `Success`, `NeedsMoreInfo`, `Refusal`. Missing any case fails — the envelope is a closed-set union and every case must be declared. |
| 27 | ARTIFACT declares `Artifact types:` | canonical | **fail** | When `**Return shape:** ARTIFACT`, the section contains a `**Artifact types:**` line with at least one MIME type (e.g., `text/x-shellscript`, `application/json`). Without it, callers can't know which language tag to expect per fenced block. |
| 28 | Required fields documented | toolkit-opinion | warn | Contract section has a `**Required fields:**` subsection (list or `none`). |
| 29 | Side effects documented | toolkit-opinion | warn | Contract section has a `**Side effects:**` subsection (list or `none`). |
| 30 | Parallel-safe documented | toolkit-opinion | warn | Contract section has a `**Parallel-safe:**` subsection (default `yes`; non-default values must explain why). |
| 31 | Non-invocable pathology | toolkit-opinion | warn | Skills declaring `user-invocable: false` without also declaring `skill-invocable: true` are not invocable by humans or other skills — likely misplaced in `skills/`. Either move to a non-skill location or set `skill-invocable: true` to make them callable programmatically. |

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
Sort: fail before warn; structural (checks 3–7, 11, 13–15, 17, 18, 20, 22, 23–27, 31) before content-quality (8–10, 12, 16, 21, 28–30).

### 5. Opt-In Repair Loop

After presenting findings, ask:

> "Apply fixes? Enter y (all), n (skip), or comma-separated numbers."

For each selected finding:
1. Read the relevant section of the SKILL.md
2. Propose a minimal specific edit — fix the finding without restructuring surrounding content
3. Show the diff
4. Write the change only on user confirmation
5. Re-run `lint.py` after each applied fix

## Anti-Pattern Guards

1. **Running LLM checks before `lint.py`** — static checks are deterministic and fast; always run them first
2. **Applying all fixes at once** — per-change confirmation is required; bulk application removes the user's ability to review individual changes
3. **Auditing `skills/_shared/`** — this directory holds shared references, not invocable skills; exclude it from all-skill audits

## Handoff

**Receives:** Path to a SKILL.md (or no argument for all-skills audit)
**Produces:** Structured findings table in `lint.py` format (file, issue, severity); optionally, targeted edits applied to the audited skill(s)
**Chainable to:** build-skill (to create a replacement), start-work (for bulk repair across skills)

## Key Instructions

- Exclude `skills/_shared/` from all-skill audits
- Treat `plugins/build/src/check/skill.py` as read-only — the static checks are authoritative; this skill adds LLM-level judgment on top
- When proposing edits, keep changes minimal — fix the finding without restructuring surrounding content
- Checks 8 and 9 (vagueness, removal test) are the highest-value content-quality checks; prioritize surfacing them clearly
