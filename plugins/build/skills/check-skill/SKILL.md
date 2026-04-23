---
name: check-skill
description: Audit a Claude Code SKILL.md for format compliance, content quality, and description collisions. Use when the user wants to "audit a skill", "review a skill", "check skill quality", "find problems in a skill", or "improve a skill".
argument-hint: "[path/to/SKILL.md or skills/ directory — scans the plugin's skills when omitted]"
user-invocable: true
version: 1.0.0
owner: build-plugin
references:
  - ../../_shared/references/skills-best-practices.md
  - references/audit-dimensions.md
  - references/repair-playbook.md
---

# /build:check-skill

Evaluate the quality of an existing Claude Code skill. Three tiers, in
order: deterministic format checks (no LLM), per-skill semantic checks
(eight always-on dimensions in a single locked-rubric call), then
cross-skill description collision detection.

This skill evaluates the skills themselves — not files against skills.

The audit rubric mirrors the authoring principles in
[skills-best-practices.md](../../_shared/references/skills-best-practices.md).
Each Tier-2 dimension cites its source principle. When the principles doc
changes, the dimensions should follow.

## Workflow

### 1. Discover Skills

Skill files live at `<plugin>/skills/<name>/SKILL.md`. When `$ARGUMENTS`
resolves to a `SKILL.md` path, scope discovery to that single file. When
`$ARGUMENTS` resolves to a directory, audit every `SKILL.md` under it.
When `$ARGUMENTS` is empty, scan the current plugin's `skills/`
directory (excluding `_shared/`).

Report: "Found N skills. Auditing..."

### 2. Tier 1 — Deterministic Format Checks

Tier 1 is implemented as seven shell scripts under `scripts/`. Each
script is deterministic, POSIX-portable (bash 3.2+), and emits findings
in the standard `FAIL|WARN|INFO|HINT  <path> — <check>: <detail>`
format followed by a `  Recommendation: <specific change>` line. See
[audit-dimensions.md](references/audit-dimensions.md) for the rubric
behind each check.

Invoke all seven scripts against the discovered skill set. The scripts
live in `scripts/` relative to this SKILL.md — Claude resolves the
absolute path from the skill's base directory at invocation time
(`$CLAUDE_PLUGIN_ROOT` is documented for hook scripts, not
skill-invoked bash; don't rely on it here):

```bash
# SKILL_DIR = absolute path to this SKILL.md's directory (Claude fills in)
SCRIPTS="${SKILL_DIR}/scripts"
TARGETS="$ARGUMENTS"  # path(s) from user; default current plugin's skills/

bash "$SCRIPTS/check_identity.sh"            $TARGETS   # FAIL filename/dir/name-slug/reserved/uniqueness
bash "$SCRIPTS/check_frontmatter.sh"         $TARGETS   # FAIL required keys/semver/owner/description cap
bash "$SCRIPTS/check_structure.sh"           $TARGETS   # FAIL required sections / Steps list
bash "$SCRIPTS/check_size.sh"                $TARGETS   # WARN >300 lines / FAIL >400 / WARN line length
bash "$SCRIPTS/check_prose.sh"               $TARGETS   # WARN hedges / absolute paths
bash "$SCRIPTS/scan_secrets.sh"              $TARGETS   # FAIL on any credential pattern
bash "$SCRIPTS/scan_dangerous_patterns.sh"   $TARGETS   # WARN remote-exec / destructive cmd
```

**Script-to-check map:**

| Script | Checks | Severity levels |
|---|---|---|
| `check_identity.sh` | Filename == `SKILL.md`, parent-dir basename == `name`, `name` kebab-case + ≤64 chars + uniqueness, reserved name tokens (`anthropic`, `claude`) | FAIL |
| `check_frontmatter.sh` | Required keys (`name` / `description` / `version` / `owner`), semver on `version`, description ≤1024 chars (or ≤1536 combined with `when_to_use`) | FAIL |
| `check_structure.sh` | Required H2 sections (`When to use` / `Prerequisites` / `Steps` / `Failure modes` / `Examples`) present; Steps is ordered list starting at 1; Examples contains ≥1 fenced block | FAIL / WARN |
| `check_size.sh` | Non-blank line count (WARN ≥300, FAIL ≥400); line length ≤120 outside fenced blocks + URLs | WARN / FAIL |
| `check_prose.sh` | Hedging wordlist (`etc.`, `maybe`, `probably`, `somehow`, `generally`, `sometimes`, `TBD`, `???`); absolute-path references in body (`/home/`, `~/`, drive-letter, `.\`/`..\` multi-component) | WARN |
| `scan_secrets.sh` | AWS / GitHub / OpenAI / Anthropic / Stripe key patterns + credential-shaped variable assignments; wraps `gitleaks detect --no-git --source <file>` when available, falls back to built-in regex set | FAIL |
| `scan_dangerous_patterns.sh` | `curl \| bash`, `eval $(curl …)`, `source <(curl …)`; destructive commands (`rm -rf`, `dd if=`, `DROP TABLE`, `TRUNCATE`, force-push, `mv` without safety flags) in fenced code blocks | WARN |

**Orchestration rules:**

- Emit all Tier-1 output immediately, before any LLM work.
- Skills with a FAIL finding from `check_identity.sh`, `check_frontmatter.sh`, `check_structure.sh` (missing required section or Steps-not-ordered-list), `check_size.sh` (>400 lines), or `scan_secrets.sh` are **excluded from Tier 2** — malformed skills don't reach the LLM step.
- `check_structure.sh` WARN findings (Examples-without-fenced-block, non-sequential Steps), `check_size.sh` WARN findings (>300 lines, line length), `check_prose.sh` WARNs, and `scan_dangerous_patterns.sh` WARNs do **not** exclude — they accompany Tier-2 output and feed the Tier-2 prompt as signals.
- Specifically, `scan_dangerous_patterns.sh` WARN lines inform D7 Safety Gating (the evaluator looks for an approval gate near the flagged command); `check_prose.sh` hedge WARNs inform D4 Clarity and Consistency.
- Exit codes: 0 on clean / WARN-only / HINT-only, 1 on FAIL, 64 on arg error, 69 on missing dep. The orchestrator treats exit 1 as the "exclude from Tier 2" signal.

### 3. Tier 2 — Per-Skill Semantic Checks (One LLM Call per Skill)

For each structurally valid skill, one locked-rubric LLM call assesses
the eight always-on dimensions in
[audit-dimensions.md](references/audit-dimensions.md):

1. **Description Retrieval Signal** — description front-loads concrete invocation triggers, not capability
2. **Trigger Conditions** — `## When to use` bullets are scannable and concrete, not a description restatement
3. **Step Discipline** — each step one atomic imperative action; no commentary; shallow conditional nesting
4. **Clarity and Consistency** — domain jargon defined on first use; terminology consistent; no non-obvious hedging
5. **Prerequisites and Contract** — tools, env vars, privilege tier, and I/O shapes are declared
6. **Failure Handling** — failure modes are concrete with recovery actions; polling/retry steps carry timeout + backoff
7. **Safety Gating** — destructive operations preceded by an explicit approval gate or dry-run default
8. **Example Realism** — examples use real domain identifiers, show side effects, avoid synthetic placeholders

Include the full SKILL.md body verbatim — never summarize. Present all
eight dimensions in one call (per-dimension calls degrade agreement by
~11.5 points per RULERS, Hong et al. 2026). Dimensions that don't apply
return PASS silently — e.g., Safety Gating PASSes on a read-only skill
with no destructive steps.

Output format per dimension: `evidence (quoted from skill) → reasoning
→ verdict (WARN or PASS) → recommendation`. Default-closed: borderline
evidence surfaces as WARN, not PASS — this is evaluator policy; skills
themselves don't declare it.

### 4. Tier 3 — Cross-Skill Description Collision

After per-skill evaluation, compare descriptions across the skill
collection and flag pairs whose triggers overlap enough to force
arbitrary selection at routing time.

**Candidates for comparison:** all skill pairs within the same plugin,
plus cross-plugin pairs that share at least one keyword in the first
clause of the description.

For each candidate pair:
1. Present Skill A's `name` + `description`
2. Present Skill B's `name` + `description`
3. Ask: "Given the same user request, would both descriptions plausibly route the request? If so, what request wording would trigger the ambiguity?"
4. If yes → WARN finding citing both skill names and the overlapping trigger surface

Skill-name collisions (two skills sharing a `name` field) are a Tier-1
FAIL under `check_identity.sh`, not a Tier-3 finding.

### 5. Report Findings

Output all findings in the standard format (file, issue, severity, recommendation).
Sort within each severity: Tier-1 deterministic first, then Tier-2 in
dimension order (Description Retrieval → Trigger Conditions → Step
Discipline → Clarity → Prerequisites → Failure Handling → Safety Gating
→ Example Realism), then Tier-3 collisions; ties break alphabetically
by file path. FAIL precedes WARN overall.

Each FAIL and WARN finding carries a `Recommendation:` line drawn from
[repair-playbook.md](references/repair-playbook.md). Generic suggestions
("fix this") are not acceptable — name the exact change.

```
FAIL  plugins/build/skills/foo/SKILL.md — Missing required section `## Failure modes`
  Recommendation: Add a `## Failure modes` section listing at least three likely failures and their recovery actions.
WARN  plugins/build/skills/bar/SKILL.md — Description Retrieval Signal: description reads as capability, not trigger
  Recommendation: Rewrite as "Use when the user asks to <specific phrase>" and name at least one concrete trigger.
WARN  plugins/build/skills/baz/SKILL.md — Body length 347 lines exceeds 300-line guidance
  Recommendation: Move long embedded scripts or reference detail to sibling files under `references/` or `scripts/`.
```

Close with a summary line:
- Findings present: `N skills audited, M findings (X fail, Y warn)`
- No findings: `N skills audited — no findings`

### 6. Opt-In Repair Loop

After presenting findings, ask:

> "Apply fixes? Enter y (all), n (skip), or comma-separated numbers."

For each selected finding, draw the canonical repair from
[repair-playbook.md](references/repair-playbook.md). Then:

1. Read the relevant section of the SKILL.md
2. Apply the canonical repair (if no playbook entry exists, skip and
   flag for manual review — do not improvise)
3. Show the diff
4. Write the change only on user confirmation
5. Re-run Tier-1 deterministic checks after each applied fix

Per-change confirmation is required — bulk application removes the
user's ability to review individual repairs.

## Key Instructions

- Run Tier-1 deterministic checks first; gate LLM evaluation on structural validity so malformed skills surface as findings, not as expensive LLM calls
- Feed Tier-1 WARN signals (destructive-cmd hits, hedge hits) as context into the Tier-2 prompt — they inform the evaluator for D7 Safety Gating and D4 Clarity, not the dimension set (all eight dimensions always run)
- Present all eight Tier-2 dimensions as a single locked-rubric call per skill — per-dimension calls degrade agreement by ~11.5 points (RULERS, Hong et al. 2026)
- Include the full SKILL.md body verbatim in every LLM evaluation so the evaluator sees the same anchors a human reviewer would
- Surface borderline evidence as WARN (default-closed) so ambiguous cases enter the report rather than silently passing — evaluator policy, not a per-skill requirement
- Excluded paths: `_shared/` directories hold references, not invocable skills; never audit a `_shared/` tree

## Anti-Pattern Guards

1. **Per-dimension LLM call** — collapse into one locked-rubric call per skill (per-dimension splits degrade agreement by 11.5 points, RULERS)
2. **LLM-evaluating format compliance** — handle filename, frontmatter, and section presence with deterministic parse (Tier 1); send only structurally valid skills to the LLM
3. **Ambiguous compliance reported as PASS** — surface as WARN (default-closed) so the user sees the borderline case
4. **Vague finding text** — cite the specific SKILL.md and the exact phrasing or field that triggered the finding
5. **Generic repair text** ("fix this", "improve the description") — every Recommendation names the specific change, drawn from `repair-playbook.md`
6. **Trigger-gating Tier-2 dimensions** — don't skip dimensions based on whether the skill "opts into" a shape; run all eight always. Dimensions that don't apply return PASS silently

## Example

<example>
User: `/build:check-skill plugins/build/skills/`

Step 1 — Discovers 3 skills: foo/SKILL.md, bar/SKILL.md, baz/SKILL.md

Step 2 — Tier 1 deterministic checks (7 scripts):
- foo/SKILL.md: 140 lines, clean frontmatter, all sections present — passes to Tier 2
- bar/SKILL.md: `version: 1.0` → FAIL (not semver); description 1180 chars → FAIL (exceeds 1024 cap). Excluded from Tier 2.
- baz/SKILL.md: 347 non-blank lines → WARN (>300 line guidance); Examples section contains no fenced block → WARN. Proceeds to Tier 2.

Step 3 — Tier 2 semantic on foo and baz:
- foo/SKILL.md: description reads "Handles tabular conversion" → WARN (D1). Steps fused into two-sentence paragraphs → WARN (D3). Prerequisites missing `AWS_PROFILE` referenced in Steps → WARN (D5). All other dimensions PASS.
- baz/SKILL.md: Safety Gating returns N/A (no destructive ops). Examples use `foo`/`bar` placeholders → WARN (D8). Other dimensions PASS.

Step 4 — Tier 3 description-collision check:
- foo/SKILL.md and baz/SKILL.md both begin "Use when the user asks to convert tabular data" → WARN collision. Recommendation: narrow each description to distinguish input formats.

Step 5 — Output:
```
FAIL  plugins/build/skills/bar/SKILL.md — Malformed version: "1.0" is not semver
  Recommendation: Rewrite as `version: 1.0.0` (MAJOR.MINOR.PATCH).
FAIL  plugins/build/skills/bar/SKILL.md — Description cap exceeded: 1180 chars > 1024
  Recommendation: Split trigger phrases into `when_to_use` (combined cap 1536) rather than compressing.
WARN  plugins/build/skills/baz/SKILL.md — Body length 347 lines exceeds 300-line guidance
  Recommendation: Move long embedded content to sibling files under `references/` or `scripts/`.
WARN  plugins/build/skills/baz/SKILL.md — Examples section lacks a fenced code block
  Recommendation: Add at least one fenced block showing a real invocation with input, output, and any side effects.
WARN  plugins/build/skills/foo/SKILL.md — Description Retrieval Signal: description reads as capability, not trigger
  Recommendation: Rewrite as "Use when the user asks to convert .csv to .parquet" and name at least one concrete trigger.
WARN  plugins/build/skills/foo/SKILL.md — Step Discipline: steps fused into multi-sentence paragraphs
  Recommendation: Split into atomic imperative steps, one action per line.
WARN  plugins/build/skills/foo/SKILL.md — Prerequisites and Contract: `AWS_PROFILE` referenced in Steps but not declared
  Recommendation: Add AWS_PROFILE to `## Prerequisites` with the required IAM actions.
WARN  plugins/build/skills/baz/SKILL.md — Example Realism: examples use `foo`/`bar` placeholders
  Recommendation: Replace with real file paths and realistic parameters from the skill's domain.
WARN  plugins/build/skills/foo/SKILL.md — Description collides with baz/SKILL.md
  Example ambiguous request: "convert this spreadsheet to Parquet"
  Recommendation: Narrow foo's description to the specific tabular format it handles (CSV); narrow baz's to its format.

3 skills audited, 9 findings (2 fail, 7 warn)
```
</example>

## Handoff

**Receives:** Path to a `SKILL.md` file or a directory containing `skills/<name>/SKILL.md` files, or no argument (scans the current plugin's `skills/`)
**Produces:** Structured findings report in file/issue/severity/recommendation format; optionally, targeted edits applied on user confirmation via the Opt-In Repair Loop
**Chainable to:** build-skill (to rebuild a flagged skill from scratch); start-work (for bulk repair across multiple skills)
