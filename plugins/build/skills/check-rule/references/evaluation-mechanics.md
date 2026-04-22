---
name: Check-Rule Evaluation Mechanics
description: Per-skill evaluation process for check-rule — Tier-1 deterministic format checks, the locked-rubric prompt skeleton that calls into rule-audit-rubric.md, Tier-3 cross-rule conflict procedure, and finding output format. Dimension definitions live in the shared rubric.
---

# Check-Rule Evaluation Mechanics

Rule auditing uses a three-tier hierarchy:

1. **Tier 1** — deterministic format checks, no LLM.
2. **Tier 2** — semantic dimensions, one locked-rubric LLM call per rule.
   Dimensions are defined in
   [rule-audit-rubric.md](../../../_shared/references/rule-audit-rubric.md);
   this file supplies the prompt skeleton only.
3. **Tier 3** — cross-rule conflict detection, one LLM pass per
   co-firing rule pair.

Handle deterministic checks (file location, glob syntax, file size)
with code-style grep/read — faster, cheaper, and more reliable than
asking the LLM to parse them.

## Table of Contents

- [Tier 1: Deterministic Format Checks](#tier-1-deterministic-format-checks)
- [Tier 2: Evaluation Prompt Skeleton](#tier-2-evaluation-prompt-skeleton)
- [Tier 3: Cross-Rule Conflict Detection](#tier-3-cross-rule-conflict-detection)
- [Output Format](#output-format)

---

## Tier 1: Deterministic Format Checks

Run for every rule file before any LLM evaluation. Emit findings
immediately. Rules with FAIL findings are excluded from Tier 2.

| Check | Category | Condition | Severity |
|-------|----------|-----------|----------|
| Location | canonical | File is not under `.claude/rules/` or `~/.claude/rules/` (Claude Code does not load rules from other paths) | fail |
| Extension | canonical | File extension is not `.md` (e.g., `.rule.md`, `.mdx`, `.markdown`) | fail |
| `paths:` glob validity | canonical-mirror | `paths:` is present but a glob has unmatched brackets, invalid wildcards, or empty pattern. Mirrors check-skill's `paths` validity check. | fail |
| File size | research-grounded | File exceeds 200 non-blank lines (Anthropic's CLAUDE.md guidance applies analogously — larger rules consume context and reduce adherence) | warn |
| Frontmatter shape | toolkit-opinion | Frontmatter contains top-level keys other than `paths:` — Anthropic documents only `paths:`; unknown keys are inert at best | info |

### Notes

- **Location check:** the project's `.claude/rules/` and the user's
  `~/.claude/rules/` are the only canonical locations. Files at
  `docs/rules/`, project root, or other paths are not picked up by
  Claude Code.
- **Glob validity:** parse each glob in `paths:` with the same logic
  check-skill uses for `paths:` on skills — both fields share the same
  Anthropic semantics.
- **Size warning:** the 200-line threshold mirrors Anthropic's CLAUDE.md
  guidance. Rules above this should be split into topic files.

---

## Tier 2: Evaluation Prompt Skeleton

Present every applicable dimension as a locked rubric in a single call
per rule. Include the full rule file verbatim — never summarize.

**Per-dimension calls are an anti-pattern.** Per-criterion separate
calls score 11.5 points lower on average (Hong et al., 2026, RULERS).
Present all applicable dimensions simultaneously; score each
independently within the same call.

For each dimension, produce: **verdict** (WARN or PASS), **evidence**
(specific text from the rule that triggered the verdict), and
**recommendation** (what to change). Default-closed: when evidence is
borderline, surface as WARN, not PASS.

Dimension criterion statements, fail/pass signals, and canonical repairs
come from
[rule-audit-rubric.md](../../../_shared/references/rule-audit-rubric.md)
— do not regenerate them per-audit.

```
You are auditing a Claude Code rule file. Evaluate every applicable
dimension below in a single response.

Dimensions 1–3 (Specificity, Single Concern, Staleness) always apply.

Dimensions 4–6 (Intent Completeness, Example Pair Quality,
Default-Closed Declaration) apply only when the rule opts into the
toolkit-opinion structured-Intent shape — body contains
`## Compliant` AND `## Non-compliant` sections, OR a `## Why` (or
`## Intent`) section. If the rule does not opt in, output
"N/A — rule does not opt into structured-Intent shape" for
Dimensions 4–6.

For each applicable dimension (defined in rule-audit-rubric.md):
1. Quote the specific text from the rule that is most relevant (evidence)
2. Explain your reasoning
3. State your verdict: WARN or PASS
4. Give a specific Recommendation if WARN (name the exact change)

When evidence is borderline, surface as WARN, not PASS.

---

<rule file verbatim>

---

Output format (one block per applicable dimension):
## Dimension N: [Name]
Evidence: "[quoted text from rule]"
Reasoning: [your reasoning]
Verdict: WARN | PASS | N/A
Recommendation: [specific change if WARN, else "None"]
```

---

## Tier 3: Cross-Rule Conflict Detection

Run after per-rule semantic evaluation. Compare rule pairs that could
co-fire.

**Anthropic's basis:**

> "if two rules contradict each other, Claude may pick one arbitrarily"

**A pair can co-fire when:**
- Both rules are always-on (no `paths:`), OR
- Their `paths:` globs share at least one matching file

**A conflict exists when:** following one rule's directives as written
would cause a developer to violate the other rule. Look for:
- Overlapping `paths:` globs (or both global) covering the same convention
- Always-on rules that contradict each other's directives
- Subtle tension (e.g., one says "prefer composition", another says "use inheritance for X")

**Evaluation prompt for each rule pair:**
1. Present Rule A verbatim
2. Present Rule B verbatim
3. Ask: "If a developer follows Rule A's directives exactly, does Rule
   B's guidance contradict?"
4. Ask the reverse
5. If either answer is yes → FAIL finding for both rules

**Canonical Repair options (to surface in the Recommendation):** narrow
the scope of one rule, merge them, add an explicit boundary
(`Exception: in files covered by [other-rule], …`), or deprecate one.

**Output format for conflicts:**
```
FAIL  .claude/rules/rule-a.md — Conflicts with rule-b.md
  "Rule A says X; Rule B says not-X"
FAIL  .claude/rules/rule-b.md — Conflicts with rule-a.md
  "Rule B says not-X; Rule A says X"
```

---

## Output Format

All findings use the `scripts/lint.py` format:

```
FAIL  .claude/rules/api-handlers.md — Malformed paths glob: unclosed brace
WARN  .claude/rules/code-style.md — Specificity: "format code properly" is anchor-free
WARN  .claude/rules/testing.md — File length 287 lines exceeds 200-line guidance
```

Sort order: FAIL findings first, WARN findings second; within each
severity, Tier-1 deterministic findings first, then Tier-2 dimensions
in numerical order (Specificity → Single Concern → Staleness → Intent
Completeness → Example Pair Quality → Default-Closed Declaration), then
Tier-3 conflicts; ties break alphabetically by file path.

Final summary line: `N rules audited, M findings (X fail, Y warn)` or
`N rules audited — no findings`.
