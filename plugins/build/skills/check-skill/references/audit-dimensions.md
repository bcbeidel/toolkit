---
name: Audit Skill Dimensions
description: Evaluation criteria for auditing a Claude Code SKILL.md — Tier-1 deterministic format checks, Tier-2 eight-dimension semantic rubric mirroring the authoring principles, and Tier-3 cross-skill conflict detection.
---

# Audit Skill Dimensions

Skill auditing uses a three-tier hierarchy: deterministic checks first
(no LLM), then semantic evaluation (one LLM call per skill, locked rubric),
then cross-skill conflict detection (separate LLM pass over skill pairs
whose descriptions could collide at routing time).

Handle deterministic checks (filename, section presence, line count,
frontmatter shape) with code — faster, cheaper, and more reliable than
asking the LLM to parse them.

The Tier-2 rubric mirrors the authoring principles in
[skills-best-practices.md](../../../_shared/references/skills-best-practices.md).
Each dimension cites its source principle. When a principle changes, the
dimension follows.

## Table of Contents

- [Category Tiers](#category-tiers)
- [Tier 1: Deterministic Format Checks](#tier-1-deterministic-format-checks)
- [Tier 2: Semantic Dimensions (One LLM Call per Skill)](#tier-2-semantic-dimensions-one-llm-call-per-skill)
  - [Dimension 1: Description Retrieval Signal](#dimension-1-description-retrieval-signal)
  - [Dimension 2: Trigger Conditions](#dimension-2-trigger-conditions)
  - [Dimension 3: Step Discipline](#dimension-3-step-discipline)
  - [Dimension 4: Clarity and Consistency](#dimension-4-clarity-and-consistency)
  - [Dimension 5: Prerequisites and Contract](#dimension-5-prerequisites-and-contract)
  - [Dimension 6: Failure Handling](#dimension-6-failure-handling)
  - [Dimension 7: Safety Gating](#dimension-7-safety-gating)
  - [Dimension 8: Example Realism](#dimension-8-example-realism)
- [Evaluation Prompt Template](#evaluation-prompt-template)
- [Tier 3: Cross-Skill Description Collision](#tier-3-cross-skill-description-collision)
- [Output Format](#output-format)

---

## Category Tiers

Every check carries a category tier so users can distinguish spec-backed
findings from house-style guidance.

| Tier | Meaning |
|------|---------|
| **canonical** | Enforces a documented Claude Code skill rule (filename, frontmatter field semantics, description cap) |
| **principle** | Mirrors a principle from `skills-best-practices.md` |
| **toolkit-opinion** | House-style guidance with no spec backing; flagged only when a trigger condition elevates the finding |

The tier appears in parentheses after each dimension heading.

---

## Tier 1: Deterministic Format Checks

Run for every skill file before any LLM evaluation. Emit findings
immediately. Skills with FAIL findings from structural scripts are
excluded from Tier 2.

| Check | Category | Condition | Severity |
|-------|----------|-----------|----------|
| Filename | canonical | File is not named `SKILL.md` (case-sensitive) | fail |
| Directory basename | principle — *Name for discovery* | Parent directory basename ≠ frontmatter `name` field | fail |
| Name slug | principle — *Name for discovery* | `name` does not match `^[a-z0-9]+(-[a-z0-9]+)*$`, exceeds 64 chars, or collides with another skill in the collection | fail |
| Reserved names | canonical | `name` contains `anthropic` or `claude` (platform-owned tokens) | fail |
| Required frontmatter | canonical | Any of `name` / `description` / `version` / `owner` is missing or empty | fail |
| Version shape | principle — *Declare identity* | `version` does not match `^\d+\.\d+\.\d+$` | fail |
| Description cap | canonical | `description` exceeds 1024 chars, or combined with `when_to_use` exceeds 1536 | fail |
| Required sections | principle — *Declare triggers / preconditions / failure contract / example* | Missing any of `## When to use`, `## Prerequisites`, `## Steps`, `## Failure modes`, `## Examples` | fail |
| Steps shape | principle — *Steps as numbered sequence* | Steps section is not an ordered list starting at 1 with sequential increments | fail (not ordered list) / warn (non-sequential) |
| Examples content | principle — *Anchor with a concrete example* | Examples section lacks at least one fenced code block | warn |
| Body length (warn) | principle — *Keep the body short* | Non-blank line count exceeds 300 | warn |
| Body length (fail) | principle — *Keep the body short* | Non-blank line count exceeds 400 | fail |
| Line length | principle — *Keep the body short* | Any line (outside fenced blocks + URLs) exceeds 120 chars | warn |
| Secrets | principle — *No embedded secrets* / canonical | Body matches a committed-secret pattern (gitleaks, fallback regex) | fail |
| Remote-exec / destructive cmd | principle — *No unverified remote execution* / *Destructive operations gate on confirmation* | Shell code blocks contain `curl \| bash`, `eval $(curl …)`, or destructive commands without safety flags | warn |
| Prose hedges | principle — *Speak in plain, direct English* | Body contains hedging language (`etc.`, `maybe`, `probably`, `somehow`, `generally`, `sometimes`, `TBD`, `???`) or absolute-path references (`/home/`, `~/`, drive-letter paths) | warn |

### Notes

- **Filename check:** only `SKILL.md` is recognized by Claude Code's skill loader. `Skill.md`, `skill.md`, or extension variants are invisible.
- **Reserved name tokens:** `anthropic` and `claude` collide with platform-owned namespaces and are rejected at load time.
- **Description cap:** hard limit 1024 chars for `description`; when `when_to_use` is present the fields are concatenated at routing time under a combined 1536-char cap. Overflow truncates silently.
- **Required sections:** the toolkit's canonical body shape. Projects may widen this set later without changing the principles doc; tightening it requires a new principle.
- **Secrets scan:** the script prefers `gitleaks detect --no-git --source <file>`. When `gitleaks` is absent, it falls back to a built-in regex set (AWS keys `AKIA[0-9A-Z]{16}`, GitHub PATs `ghp_[A-Za-z0-9]{36}` / `github_pat_[A-Za-z0-9_]{82}`, OpenAI keys `sk-[A-Za-z0-9]{48}`, Anthropic keys `sk-ant-[A-Za-z0-9\-_]{80,}`, Stripe live keys `sk_live_[A-Za-z0-9]{24}`, and generic `password|secret|token|api_key|access_key|private_key` assignments). Any match is FAIL.
- **Remote-exec / destructive-cmd:** emitted as WARN rather than FAIL — destructive commands are often legitimate when gated, and D7 Safety Gating judges whether the gate exists. The WARN text feeds Tier-2 as context.
- **Prose pre-check:** wordlist and absolute-path matches emit WARN only. D4 Clarity and Consistency catches the non-obvious tail.

---

## Tier 2: Semantic Dimensions (One LLM Call per Skill)

Present all eight dimensions as a locked rubric in a single call per
skill. Include the full SKILL.md body verbatim — never summarize.

**Per-dimension calls are an anti-pattern.** Per-criterion separate calls
score 11.5 points lower on average (Hong et al., 2026, RULERS). Present
all dimensions simultaneously; score each independently within the same
call.

For each dimension, produce: **verdict** (WARN, PASS, or N/A),
**evidence** (specific text from the skill that triggered the verdict),
and **recommendation** (what to change). Default-closed: when evidence
is borderline, surface as WARN, not PASS. Default-closed is evaluator
policy — the skill itself doesn't declare it.

Dimensions that don't apply to the skill (e.g., Safety Gating on a
read-only skill with no destructive steps) return PASS silently with
verdict "N/A".

---

### Dimension 1: Description Retrieval Signal

*(principle — [Write the description as a retrieval signal](../../../_shared/references/skills-best-practices.md))*

**What it checks:** Whether the `description` front-loads concrete invocation triggers a router can match on, rather than describing the skill's internal mechanics.

**Fail signals (→ WARN):**
- Description reads as capability ("Handles tabular conversion", "Processes data") rather than trigger ("Use when the user asks to convert .csv to .parquet")
- Starts in second person ("You can use this to…") or passive voice
- Generic tokens (`helper`, `utility`, `tools`, `thing`, `stuff`) used as the primary descriptor with no specific trigger
- No user-visible phrases a router would actually match against — no quoted user phrases, no file extensions, no error strings

**Pass signals:**
- Leads with "Use when…" or equivalent trigger framing
- Names at least one specific invocation phrase, file extension, error string, or event type
- Third-person, active voice

**Canonical Repair:** See `repair-playbook.md` → Dimension 1.

---

### Dimension 2: Trigger Conditions

*(principle — [Declare triggers as scannable conditions](../../../_shared/references/skills-best-practices.md))*

**What it checks:** Whether the `## When to use` section contains concrete, scannable conditions that confirm the skill applies — not a restatement of the description.

**Scope:** Tier-1 already enforces section presence. This dimension judges content quality.

**Fail signals (→ WARN):**
- Bullets restate the description in different words without adding specificity
- Bullets are abstract ("when the user needs data transformation") with no concrete trigger phrase, file type, or condition
- Section contains only one bullet and it's generic

**Pass signals:**
- Multiple scannable bullets, each naming a specific trigger (user phrase, file pattern, error string, lifecycle event)
- Conditions are concrete enough that a reader can decide "does this apply?" without inference

**Canonical Repair:** See `repair-playbook.md` → Dimension 2.

---

### Dimension 3: Step Discipline

*(principle — [Write Steps as a numbered sequence of atomic actions](../../../_shared/references/skills-best-practices.md))*

**What it checks:** Whether each step is one atomic imperative action, free of rationale/commentary, with shallow conditional nesting.

**Fail signals (→ WARN):**
- Steps in passive voice or describing what "should happen" rather than telling the agent what to do
- Reasoning or rationale embedded inside a step body ("We do this because …") — reasoning belongs in surrounding prose
- Conditional logic nested more than two levels deep ("if A: if B: if C: …")
- Multiple distinct actions fused into one step with "and" or bullet sub-lists
- Step paragraphs longer than two sentences

**Pass signals:**
- Each step starts with an imperative verb addressed to the agent ("Run `foo`", "Read `$ARGUMENTS`")
- One action per step; sub-tasks split into separate steps
- Conditional branches at most two levels deep; deeper branching split into a separate skill

**Canonical Repair:** See `repair-playbook.md` → Dimension 3.

---

### Dimension 4: Clarity and Consistency

*(principle — [Speak in plain, direct English](../../../_shared/references/skills-best-practices.md))*

**What it checks:** Whether the skill uses undefined jargon, inconsistent terminology, or hedging that Tier-1's wordlist didn't catch.

**Fail signals (→ WARN):**
- Domain jargon or abbreviations used without definition on first use
- The same concept named differently in different sections (`service_name` → `svc` → `service_id`)
- Non-obvious hedging beyond the Tier-1 wordlist ("where applicable", "if possible", "as needed")

**Pass signals:**
- Domain terms defined on first use or linked to a glossary
- Consistent terminology throughout
- Direct, definite phrasing

**Canonical Repair:** See `repair-playbook.md` → Dimension 4.

---

### Dimension 5: Prerequisites and Contract

*(principle — [State preconditions once / Declare inputs, outputs, and their shapes](../../../_shared/references/skills-best-practices.md))*

**What it checks:** Whether `## Prerequisites` names the actual dependencies (tools, env vars, language versions, privilege tier, input/output shapes) or is a placeholder heading.

**Scope:** Tier-1 enforces section presence. This dimension judges whether the section carries real content.

**Fail signals (→ WARN):**
- Section exists but lists only generic items ("requires a terminal", "requires git")
- Skill references env vars or tools in Steps that are not declared in Prerequisites
- Skill mutates persistent state or affects elevated systems but does not declare the privilege tier or IAM/RBAC roles
- Input/output shapes are implicit — the skill reads a file or produces an artifact without naming its format

**Pass signals:**
- Every tool, env var, and dependency named in Steps is declared in Prerequisites
- When operating on elevated systems, privilege tier is called out
- Inputs and outputs are named with their shapes (types, formats, locations)

**Canonical Repair:** See `repair-playbook.md` → Dimension 5.

---

### Dimension 6: Failure Handling

*(principle — [Write a failure contract](../../../_shared/references/skills-best-practices.md))*

**What it checks:** Whether `## Failure modes` names real failure modes with recovery actions, and whether polling/retry/wait steps name timeouts and backoff.

**Scope:** Tier-1 enforces section presence. This dimension judges content.

**Fail signals (→ WARN):**
- Section exists but lists placeholder failures ("if something goes wrong") with no recovery
- Steps describe polling, waiting, or retrying without naming a timeout and a backoff parameter ("poll until ready" with no upper bound)
- External calls (network, filesystem, subprocess) in Steps with no corresponding failure mode listed
- Recovery actions are generic ("handle the error") rather than specific ("retry once with exponential backoff, then surface `status=timeout`")

**Pass signals:**
- Named failure modes tied to specific steps or external calls
- Each failure has a concrete recovery action
- Polling/retry/wait language carries explicit timeout + backoff parameters

**Canonical Repair:** See `repair-playbook.md` → Dimension 6.

---

### Dimension 7: Safety Gating

*(principle — [Destructive operations gate on confirmation](../../../_shared/references/skills-best-practices.md))*

**What it checks:** When the skill contains destructive operations, whether an explicit approval gate precedes them.

**Scope:** Tier-1 flags destructive-command patterns as WARN and feeds the hit list to this dimension. If no destructive operations are present, this dimension returns N/A.

**Fail signals (→ WARN):**
- Destructive step (`rm -rf`, `DROP TABLE`, force-push, production deploy, secret rotation) with no preceding approval step, dry-run, or confirmation prompt
- Approval language is vague ("confirm with the user") rather than an explicit gate
- Dry-run option mentioned but not made the default, or the destructive variant runs unconditionally
- `disable-model-invocation: true` missing on a skill whose Workflow is destructive by design

**Pass signals:**
- Destructive step is preceded by an explicit approval step the agent must pause on
- Dry-run is the default; destructive variant requires explicit opt-in
- `disable-model-invocation: true` is set for skills whose auto-invocation would be dangerous

**Canonical Repair:** See `repair-playbook.md` → Dimension 7.

---

### Dimension 8: Example Realism

*(principle — [Anchor with a concrete example](../../../_shared/references/skills-best-practices.md))*

**What it checks:** Whether `## Examples` uses real inputs, outputs, and side effects — not synthetic `foo`/`bar` placeholders.

**Scope:** Tier-1 enforces that Examples contains at least one fenced block. This dimension judges whether the example is realistic.

**Fail signals (→ WARN):**
- Examples use generic placeholders (`foo`, `bar`, `baz`, `myFunction`, `Widget`, `Thing`) as primary identifiers
- Example inputs are `"example"` / `"test"` / `"placeholder"` strings rather than realistic values
- Side effects are not shown — a skill that writes a file provides no sample output
- Example is a command template with `<>` placeholders and no concrete invocation

**Pass signals:**
- Identifiers match the domain the skill operates on (real file paths, real parameter values, realistic error messages)
- Inputs, outputs, and side effects are all visible in at least one example
- Optional but strong signal: a file path comment showing provenance

**Canonical Repair:** See `repair-playbook.md` → Dimension 8.

---

## Evaluation Prompt Template

Use this skeleton for every Tier-2 LLM call. Criterion statements and
anchor examples come from the rubric above — do not generate them
per-audit.

```
You are auditing a Claude Code SKILL.md file. Evaluate all eight
dimensions below in a single response.

Tier-1 signals for this skill (use as context, not as dimension gating):
<destructive-cmd lines found, absolute paths found, hedge words found, section presence summary>

For each dimension:
1. Quote the specific text from the skill that is most relevant (evidence)
2. Explain your reasoning
3. State your verdict: WARN, PASS, or N/A
4. Give a specific Recommendation if WARN (name the exact change)

When evidence is borderline, surface as WARN, not PASS.

---

## Dimension 1: Description Retrieval Signal
Criterion: Does the description front-load concrete invocation triggers
(user phrases, file extensions, error strings, event types) instead of
describing the skill's internal mechanics?

PASS anchor: "Use when the user asks to convert .csv to .parquet or tabular data transformation comes up."
FAIL anchor: "Handles tabular conversion and data transformation workflows."

## Dimension 2: Trigger Conditions
Criterion: Does `## When to use` carry concrete scannable bullets
beyond a restatement of the description?

PASS anchor: bullets naming specific user phrases, file patterns, or event types
FAIL anchor: bullets restating the description in other words; single vague bullet

## Dimension 3: Step Discipline
Criterion: Is each step one atomic imperative action, free of
rationale/commentary, with shallow conditional nesting?

PASS anchor: "1. Read `$ARGUMENTS`. 2. Validate the input matches `^.+\.csv$`. 3. Convert with `pandas.read_csv(…).to_parquet(…)`."
FAIL anchor: steps in passive voice, reasoning embedded in step body, conditionals nested 3+ levels, multi-action fused steps

## Dimension 4: Clarity and Consistency
Criterion: Is domain jargon defined on first use, terminology
consistent across sections, and non-obvious hedging absent?

PASS anchor: "backfill (reprocessing historical rows)" defined on first use; `service_name` used consistently
FAIL anchor: "DAG", "CDC", or similar used without definition; `service_name` → `svc` → `service_id`

## Dimension 5: Prerequisites and Contract
Criterion: Does Prerequisites name the actual tools, env vars,
privilege tier, and I/O shapes the skill depends on?

PASS anchor: lists tools + versions + env vars + input/output shapes + privilege tier for elevated skills
FAIL anchor: section contains only generic items; env vars referenced in Steps not in Prerequisites; implicit I/O

## Dimension 6: Failure Handling
Criterion: Does Failure modes name real failures with concrete
recoveries, and do polling/retry/wait steps carry timeout + backoff?

PASS anchor: "If `aws s3 cp` returns 403 → stop; surface the role's missing permission." + "Poll every 10s for up to 5 minutes."
FAIL anchor: "if something goes wrong, handle it" + "poll until ready"

## Dimension 7: Safety Gating
Criterion: Are destructive steps preceded by an explicit approval
gate or dry-run default? (Returns N/A when no destructive operations
are present.)

PASS anchor: explicit approval step before `DROP TABLE`; dry-run default with explicit opt-in for destructive variant
FAIL anchor: destructive step runs unconditionally; approval language is vague; `disable-model-invocation` missing on a destructive skill

## Dimension 8: Example Realism
Criterion: When examples are present, do they use real domain
identifiers, show side effects, and avoid synthetic placeholders?

PASS anchor: example with real file paths, realistic parameters, and visible outputs/side effects
FAIL anchor: `foo`/`bar`/`Widget` placeholders, `"example"` strings, no side effect shown

---

<skill file verbatim>

---

Output format (one block per dimension):
## Dimension N: [Name]
Evidence: "[quoted text from skill]"
Reasoning: [your reasoning]
Verdict: WARN | PASS | N/A
Recommendation: [specific change if WARN, else "None"]
```

---

## Tier 3: Cross-Skill Description Collision

*(principle — [Write the description as a retrieval signal](../../../_shared/references/skills-best-practices.md))*

Run after per-skill semantic evaluation. Compare descriptions across
the skill collection and flag pairs whose triggers overlap enough to
force arbitrary selection at routing time.

**Candidates for comparison:** all skill pairs within the same plugin,
plus cross-plugin pairs that share at least one keyword in the first
clause of the description.

**Evaluation prompt for each candidate pair:**
1. Present Skill A's `name` + `description`
2. Present Skill B's `name` + `description`
3. Ask: "Given the same user request, would both skills' descriptions plausibly route the request? If so, what request wording would trigger the ambiguity?"
4. If the answer is yes → WARN finding citing both skill names and the overlapping trigger surface

**Output format for collisions:**
```
WARN  plugins/build/skills/foo/SKILL.md — Description collides with bar/SKILL.md
  Example ambiguous request: "<user phrase that would route to either>"
  Recommendation: Narrow foo's description to name the <specific axis> it covers; narrow bar's to name <other axis>.
WARN  plugins/build/skills/bar/SKILL.md — Description collides with foo/SKILL.md
  (same)
```

Skill-name collisions (two skills sharing a `name` field) are a Tier-1
FAIL under the uniqueness check, not a Tier-3 finding.

---

## Output Format

All findings use the standard `SEVERITY  <path> — <check>: <detail>`
format with a `Recommendation:` line:

```
FAIL  plugins/build/skills/foo/SKILL.md — Missing required section `## Failure modes`
  Recommendation: Add a `## Failure modes` section listing at least three likely failures and their recovery actions.
WARN  plugins/build/skills/bar/SKILL.md — Description Retrieval Signal: description reads as capability, not trigger
  Recommendation: Rewrite as "Use when the user asks to <specific phrase>" and name at least one concrete trigger.
```

Sort order: FAIL findings first, WARN findings second, HINT last; within
each severity, Tier-1 deterministic findings first, then Tier-2
dimensions in numerical order (Description Retrieval → Trigger
Conditions → Step Discipline → Clarity → Prerequisites → Failure
Handling → Safety Gating → Example Realism), then Tier-3 collisions;
ties break alphabetically by file path.

Final summary line: `N skills audited, M findings (X fail, Y warn)` or
`N skills audited — no findings`.
