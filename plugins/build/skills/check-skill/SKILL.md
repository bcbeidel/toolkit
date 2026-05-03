---
name: check-skill
description: >-
  Use when the user wants to "audit a skill", "review a skill", "check
  skill quality", "find problems in a skill", or "improve a skill".
  Audits a Claude Code SKILL.md for format compliance, content
  quality, and cross-skill description collisions across three tiers
  (deterministic scripts → LLM rubric → cross-skill conflict).
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
argument-hint: "[path/to/SKILL.md or skills/ directory — scans the plugin's skills when omitted]"
user-invocable: true
version: 1.0.0
owner: build-plugin
references:
  - ../../_shared/references/skill-best-practices.md
  - references/audit-dimensions.md
  - references/repair-playbook.md
license: MIT
---

# /build:check-skill

Evaluate the quality of an existing Claude Code skill. Three tiers,
in order: deterministic format checks (no LLM), per-skill semantic
checks (nine always-on dimensions in a single locked-rubric call),
then cross-skill description collision detection.

This skill evaluates the skills themselves — not files against skills.

The audit rubric mirrors the authoring principles in
[skill-best-practices.md](../../_shared/references/skill-best-practices.md).
Each Tier-2 dimension cites its source principle. When the principles
doc changes, the dimensions should follow.

## When to use

- The user asks to "audit / review / check" a skill or skill library
- The user asks "find problems in", "improve", or "is this skill
  well-formed"
- After `/build:build-skill` writes a new skill — chain-call to audit
  the just-written artifact
- Bulk audits across a plugin's `skills/` directory, as part of
  `/work:start-work` repair passes

## Prerequisites

- Seven Tier-1 scripts under `scripts/` relative to this SKILL.md
  (`check_identity.sh`, `check_frontmatter.sh`, `check_structure.sh`,
  `check_size.sh`, `check_prose.sh`, `scan_secrets.sh`,
  `scan_dangerous_patterns.sh`)
- `bash` 3.2+, POSIX utilities (`awk`, `find`, `basename`, `head`,
  `grep`, `dirname`)
- Optional: `gitleaks` on `PATH` for stronger secret scanning
  (`scan_secrets.sh` falls back to a built-in regex set when absent)
- `$ARGUMENTS` may carry a `SKILL.md` path, a `skills/` directory, or
  be empty (scans the current plugin's `skills/` excluding
  `_shared/`)

## Steps

1. **Discover skills.** Resolve `$ARGUMENTS`. A `SKILL.md` path →
   audit that one file. A directory → audit every `SKILL.md` under
   it (excluding `_shared/`). Empty → scan the current plugin's
   `skills/` directory. Report: "Found N skills. Auditing...".

2. **Run Tier-1 deterministic checks.** Invoke all seven scripts
   against the discovered skill set. Scripts live in `scripts/`
   relative to this SKILL.md; Claude resolves the absolute path from
   the skill's base directory at invocation time. (`$CLAUDE_PLUGIN_ROOT`
   is documented for hook scripts, not skill-invoked bash; do not
   rely on it here.)

   ```bash
   SCRIPTS="${SKILL_DIR}/scripts"
   TARGETS="$ARGUMENTS"  # path(s) from user; default: plugin's skills/

   bash "$SCRIPTS/check_identity.sh"          $TARGETS
   bash "$SCRIPTS/check_frontmatter.sh"       $TARGETS
   bash "$SCRIPTS/check_structure.sh"         $TARGETS
   bash "$SCRIPTS/check_size.sh"              $TARGETS
   bash "$SCRIPTS/check_prose.sh"             $TARGETS
   bash "$SCRIPTS/scan_secrets.sh"            $TARGETS
   bash "$SCRIPTS/scan_dangerous_patterns.sh" $TARGETS
   ```

   Emit all Tier-1 output immediately, before any LLM work. Exit
   codes: 0 on clean / WARN-only / INFO-only, 1 on FAIL, 64 on arg
   error, 69 on missing dependency. Treat exit 1 as the "exclude
   from Tier 2" signal. INFO findings are toolkit-opinion advisories
   (no spec backing) — surface them in the report but do not exclude
   from Tier 2.

3. **Apply orchestration rules.** Skills with a FAIL from
   `check_identity.sh`, `check_frontmatter.sh`, `check_structure.sh`
   (missing required section or Steps-not-ordered-list),
   `check_size.sh` (>400 lines), or `scan_secrets.sh` are **excluded
   from Tier 2** — malformed skills don't reach the LLM step.
   `check_structure.sh` WARNs (Examples-without-fenced-block,
   non-sequential Steps), `check_size.sh` WARNs (>300 lines, line
   length), `check_prose.sh` WARNs, and `scan_dangerous_patterns.sh`
   WARNs do **not** exclude — they accompany Tier-2 output and feed
   the Tier-2 prompt as signals (destructive-cmd WARNs inform D7
   Safety Gating; hedge WARNs inform D4 Clarity and Consistency).

4. **Run Tier-2 semantic checks.** For each structurally valid
   skill, one locked-rubric LLM call assesses all nine always-on
   dimensions in
   [audit-dimensions.md](references/audit-dimensions.md):
   (1) Description Retrieval Signal, (2) Trigger Conditions,
   (3) Step Discipline, (4) Clarity and Consistency,
   (5) Prerequisites and Contract, (6) Failure Handling,
   (7) Safety Gating, (8) Example Realism, (9) Mechanical-Work
   Partition. Include the full `SKILL.md` body verbatim — never
   summarize. Present all nine dimensions in one call; per-dimension
   calls degrade agreement by ~11.5 points (RULERS, Hong et al.
   2026). Dimensions that don't apply return PASS silently (e.g.,
   Safety Gating on a read-only skill; Mechanical-Work Partition on
   a judgment-only skill). Output per dimension: evidence →
   reasoning → verdict (WARN / PASS / N/A) → recommendation.
   Default-closed: borderline evidence surfaces as WARN, not PASS.

5. **Run Tier-3 description-collision detection.** Compare
   descriptions across the skill collection and flag pairs whose
   triggers overlap enough to force arbitrary routing selection.
   Candidates: all skill pairs within the same plugin, plus
   cross-plugin pairs sharing at least one keyword in the first
   clause of the description. For each candidate: present both
   names + descriptions; ask whether the same user request would
   plausibly route to both; on yes → WARN citing both skill names
   and an example ambiguous request. Skill-name collisions (two
   skills sharing a `name` field) are a Tier-1 FAIL under
   `check_identity.sh`, not a Tier-3 finding.

6. **Report findings.** Output all findings in the standard
   `SEVERITY  <path> — <check>: <detail>` format with a
   `Recommendation:` line drawn from
   [repair-playbook.md](references/repair-playbook.md). Sort within
   each severity: Tier-1 deterministic first, then Tier-2 in
   dimension order, then Tier-3 collisions; ties break
   alphabetically. Severity order: FAIL → WARN → INFO. Close with a
   summary line: `N skills audited, M findings (X fail, Y warn,
   Z info)` or `N skills audited — no findings`.

7. **Offer the opt-in repair loop.** Ask: "Apply fixes? Enter y
   (all), n (skip), or comma-separated numbers." For each selected
   finding, draw the canonical repair from `repair-playbook.md`.
   Read the relevant section; apply the minimal specific edit; show
   the diff; write only on user confirmation; re-run the relevant
   Tier-1 scripts after each applied fix. Per-change confirmation is
   required — bulk application removes the user's ability to review
   individual repairs.

## Failure modes

- **Missing Tier-1 dependency.** Any script exits 69 when a required
  command isn't installed (e.g., `awk` missing). Recovery: surface
  the script's install hint; re-run once the dependency is on PATH.
  `gitleaks` absence specifically triggers the fallback regex path
  in `scan_secrets.sh` — not a hard failure.
- **`$ARGUMENTS` path does not exist.** Any script exits 64.
  Recovery: report the bad path and ask the user to correct it.
- **No structurally valid skills for Tier 2.** Every audited skill
  failed Tier-1. Recovery: report the Tier-1 findings and skip
  Tier 2 / Tier 3 — per-skill semantic audit on malformed skills
  produces noise.
- **LLM call returns an unparseable dimension block.** Surface the
  raw response and mark the skill as "Tier-2 inconclusive — rerun or
  inspect manually". Do not silently drop findings.
- **User declines all repair suggestions.** Expected. Close without
  writing any changes; the findings report is the final artifact.

## Examples

<example>
User: `/build:check-skill plugins/build/skills/`

Step 1 — Discovers 3 skills: `foo/SKILL.md`, `bar/SKILL.md`,
`baz/SKILL.md`.

Step 2 — Runs all seven Tier-1 scripts:
- foo/SKILL.md: 140 lines, clean frontmatter, all sections — passes to Tier 2
- bar/SKILL.md: `version: 1.0` → FAIL (not semver); description 1180 chars → FAIL. Excluded from Tier 2.
- baz/SKILL.md: 347 non-blank lines → WARN; Examples has no fenced block → WARN. Proceeds to Tier 2.

Step 4 — Tier 2 on foo and baz:
- foo/SKILL.md: description reads "Handles tabular conversion" →
  WARN (D1). Steps fused into multi-sentence paragraphs → WARN (D3).
  `AWS_PROFILE` referenced in Steps but not declared in
  Prerequisites → WARN (D5). Other dimensions PASS.
- baz/SKILL.md: D7 N/A (no destructive ops). Examples use
  `foo`/`bar` placeholders → WARN (D8). Others PASS.

Step 5 — Tier 3: foo and baz both open "Use when the user asks to convert tabular data" → WARN collision.

Step 6 — Output:
```
FAIL  plugins/build/skills/bar/SKILL.md — Malformed version: "1.0" is not semver
  Recommendation: Rewrite as `version: 1.0.0` (MAJOR.MINOR.PATCH).
FAIL  plugins/build/skills/bar/SKILL.md — Description cap exceeded: 1180 chars > 1024
  Recommendation: Split trigger phrases into `when_to_use` (combined cap 1536) rather than compressing.
WARN  plugins/build/skills/baz/SKILL.md — Body length 347 lines exceeds 300-line guidance
  Recommendation: Move long embedded content to sibling files under `references/` or `scripts/`.
WARN  plugins/build/skills/foo/SKILL.md — Description Retrieval Signal: capability, not trigger
  Recommendation: Rewrite as "Use when the user asks to <specific phrase>" and name at least one concrete trigger.
WARN  plugins/build/skills/foo/SKILL.md — Step Discipline: steps fused into multi-sentence paragraphs
  Recommendation: Split into atomic imperative steps, one action per line.
WARN  plugins/build/skills/foo/SKILL.md — Prerequisites and Contract: `AWS_PROFILE` referenced but not declared
  Recommendation: Add AWS_PROFILE to `## Prerequisites` with the required IAM actions.
WARN  plugins/build/skills/baz/SKILL.md — Example Realism: `foo`/`bar` placeholders
  Recommendation: Replace with real file paths and realistic parameters from the skill's domain.
WARN  plugins/build/skills/foo/SKILL.md — Description collides with baz/SKILL.md
  Recommendation: Narrow foo's description to the specific tabular format it handles (CSV); narrow baz's to its format.

3 skills audited, 8 findings (2 fail, 6 warn)
```
</example>

## Key Instructions

- Run Tier-1 deterministic checks first; gate LLM evaluation on
  structural validity so malformed skills surface as findings, not
  as expensive LLM calls
- Feed Tier-1 WARN signals (destructive-cmd hits, hedge hits) as
  context into the Tier-2 prompt — they inform the evaluator for
  D7 Safety Gating and D4 Clarity, not the dimension set (all nine
  dimensions always run)
- Present all nine Tier-2 dimensions as a single locked-rubric
  call per skill — per-dimension calls degrade agreement by ~11.5
  points (RULERS, Hong et al. 2026)
- Include the full SKILL.md body verbatim in every LLM evaluation
- Surface borderline evidence as WARN (default-closed) so ambiguous
  cases enter the report rather than silently passing
- Excluded paths: `_shared/` holds references, not invocable skills;
  never audit a `_shared/` tree

## Anti-Pattern Guards

1. **Per-dimension LLM call** — collapse into one locked-rubric
   call per skill (per-dimension splits degrade agreement by 11.5
   points, RULERS).
2. **LLM-evaluating format compliance** — handle filename,
   frontmatter, and section presence with deterministic parse
   (Tier 1); send only structurally valid skills to the LLM.
3. **Ambiguous compliance reported as PASS** — surface as WARN
   (default-closed) so the user sees the borderline case.
4. **Vague finding text** — cite the specific SKILL.md and the
   exact phrasing or field that triggered the finding.
5. **Generic repair text** ("fix this", "improve the description")
   — every Recommendation names the specific change, drawn from
   `repair-playbook.md`.
6. **Trigger-gating Tier-2 dimensions** — don't skip dimensions
   based on whether the skill "opts into" a shape; run all nine
   always. Dimensions that don't apply return PASS silently.

## Handoff

**Receives:** Path to a `SKILL.md` file or a directory containing
`skills/<name>/SKILL.md` files, or no argument (scans the current
plugin's `skills/`).

**Produces:** Structured findings report in file/issue/severity/
recommendation format; optionally, targeted edits applied on user
confirmation via the opt-in repair loop.

**Chainable to:** `/build:build-skill` (to rebuild a flagged skill
from scratch); `/work:start-work` (for bulk repair across multiple
skills).

