---
name: Audit Rule Dimensions
description: Evaluation criteria for auditing a Claude Code `.claude/rules/` library — Tier-1 deterministic format checks, Tier-2 eight-dimension semantic rubric mirroring the authoring principles, and Tier-3 cross-rule conflict detection.
---

# Audit Rule Dimensions

Rule auditing uses a three-tier hierarchy: deterministic checks first
(no LLM), then semantic evaluation (one LLM call per rule, locked rubric),
then cross-rule conflict detection (separate LLM pass over rule pairs that
could co-fire).

Handle deterministic checks (file location, glob syntax, file size) with
code — faster, cheaper, and more reliable than asking the LLM to parse them.

The Tier-2 rubric mirrors the authoring principles in
[rules-best-practices.md](../../../_shared/references/rules-best-practices.md).
Each dimension cites its source principle. When a principle changes, the
dimension follows.

## Table of Contents

- [Category Tiers](#category-tiers)
- [Tier 1: Deterministic Format Checks](#tier-1-deterministic-format-checks)
- [Tier 2: Semantic Dimensions (One LLM Call per Rule)](#tier-2-semantic-dimensions-one-llm-call-per-rule)
  - [Dimension 1: Framing](#dimension-1-framing)
  - [Dimension 2: Specificity](#dimension-2-specificity)
  - [Dimension 3: Single Concern](#dimension-3-single-concern)
  - [Dimension 4: Why Adequacy](#dimension-4-why-adequacy)
  - [Dimension 5: Scope Tightness](#dimension-5-scope-tightness)
  - [Dimension 6: Staleness](#dimension-6-staleness)
  - [Dimension 7: Judgment-Not-Linter](#dimension-7-judgment-not-linter)
  - [Dimension 8: Example Realism](#dimension-8-example-realism)
- [Evaluation Prompt Template](#evaluation-prompt-template)
- [Tier 3: Cross-Rule Conflict Detection](#tier-3-cross-rule-conflict-detection)
- [Output Format](#output-format)

---

## Category Tiers

Every check carries a category tier so users can distinguish spec-backed
findings from house-style guidance.

| Tier | Meaning |
|------|---------|
| **canonical** | Enforces a documented Anthropic rule for `.claude/rules/` (location, extension, `paths:` field) |
| **principle** | Mirrors a principle from `rules-best-practices.md` |
| **research-grounded** | Toolkit-opinion check whose design is supported by published research |

The tier appears in parentheses after each dimension heading.

---

## Tier 1: Deterministic Format Checks

Run for every rule file before any LLM evaluation. Emit findings
immediately. Rules with FAIL findings are excluded from Tier 2.

| Check | Category | Condition | Severity |
|-------|----------|-----------|----------|
| Location | canonical | File is not under `.claude/rules/` or `~/.claude/rules/` | fail |
| Extension | canonical | File extension is not `.md` (e.g., `.rule.md`, `.mdx`) | fail |
| `paths:` glob validity | canonical | `paths:` is present but a glob has unmatched brackets, invalid wildcards, or empty pattern | fail |
| File size (warn) | principle — *Prefer short* | File exceeds 200 non-blank lines | warn |
| File size (fail) | principle — *Prefer short* | File exceeds 500 non-blank lines | fail |
| Frontmatter shape | canonical | Frontmatter contains top-level keys other than `paths:` | info |
| Shape hints (informational) | — | Scan for keywords (`compliant`, `non-compliant`, `violation`, `exception`, `failure`, fenced code blocks); no finding. The hit set is appended to the Tier-2 prompt as context so the evaluator weighs Why Adequacy and Example Realism more closely when present | none |

### Notes

- **Location check:** `.claude/rules/` and `~/.claude/rules/` are the
  only canonical locations. Files at `docs/rules/`, project root, or
  other paths are not picked up by Claude Code.
- **Glob validity:** parse each glob in `paths:` with the same logic
  check-skill uses for `paths:` — both fields share Anthropic semantics.
- **Size thresholds:** 200 lines follows the "prefer short" principle
  as a WARN; 500 lines is a hard FAIL — at that length the file is a
  document, not a rule, and belongs elsewhere (CLAUDE.md, a context
  doc, or split into multiple rules).
- **Shape hints:** the keyword sniff is *not* a trigger gate. All eight
  Tier-2 dimensions run on every rule. Hints are context for the
  evaluator, not dimension filters.

---

## Tier 2: Semantic Dimensions (One LLM Call per Rule)

Present all eight dimensions as a locked rubric in a single call per
rule. Include the full rule file verbatim — never summarize.

**Per-dimension calls are an anti-pattern.** Per-criterion separate calls
score 11.5 points lower on average (Hong et al., 2026, RULERS). Present
all dimensions simultaneously; score each independently within the same
call.

For each dimension, produce: **verdict** (WARN, PASS, or N/A),
**evidence** (specific text from the rule that triggered the verdict),
and **recommendation** (what to change). Default-closed: when evidence
is borderline, surface as WARN, not PASS. Default-closed is evaluator
policy — the rule itself doesn't declare it.

Dimensions that don't apply to the rule (e.g., Example Realism on a
rule with no examples) return PASS silently with verdict "N/A".

---

### Dimension 1: Framing

*(principle — [Frame in the positive](../../../_shared/references/rules-best-practices.md))*

**What it checks:** Whether the rule states what to do, not only what
to avoid. Negations are linguistically fragile — a dropped or
misattributed `not`/`don't`/`never` inverts the rule. Positive framings
also name a target; pure prohibitions leave the target implicit.

**Fail signals (→ WARN):**
- Rule statement is only a prohibition ("Don't use global state", "Never commit secrets") with no positive counterpart stated
- Multiple negations stacked in a single sentence ("Don't not return …")
- Hedged prohibitions ("Try not to …", "Avoid when possible") — vague *and* negative

**Pass signals:**
- Rule statement names a positive action ("Thread dependencies through constructors")
- Prohibition is paired with the positive alternative ("Use X; never use Y")
- Negation is load-bearing and unavoidable (e.g., "Never log PII") — accepted when no clean positive counterpart exists

**Canonical Repair:** See `repair-playbook.md` → Dimension 1.

---

### Dimension 2: Specificity

*(principle — [Specific enough to be falsifiable](../../../_shared/references/rules-best-practices.md); canonical — Anthropic's "Use 2-space indentation" vs. "Format code properly" example)*

**What it checks:** Whether the rule's directives are concrete enough
that a reviewer (or Claude) can verify compliance unambiguously.

**Fail signals (→ WARN):**
- Anchor-free terms as the directive: "good", "clean", "clear",
  "appropriate", "well-structured", "properly", "nice", "consistent"
  without a behavioral definition
- Directives that defer the decision back to the reader ("use your
  judgment", "as appropriate") without a fallback rule
- Hedged phrasing: "prefer", "generally", "usually", "consider"

**Pass signals:**
- Verifiable directive: numeric threshold, named tool, specific file
  path or command, quoted code pattern
- Anchor-free terms paired with a verifiable definition ("clean code:
  no functions over 50 lines, no nested ternaries")

**Canonical Repair:** See `repair-playbook.md` → Dimension 2.

---

### Dimension 3: Single Concern

*(principle — [One claim per file](../../../_shared/references/rules-best-practices.md))*

**What it checks:** Whether the rule covers a single topic. A file
that mixes unrelated conventions is two rules, not one.

**Fail signals (→ WARN):**
- Multiple top-level `##` sections covering distinct topics that
  wouldn't naturally co-evolve (e.g., "API conventions" and "Test
  conventions" in the same file)
- Filename describes one topic but body covers another in addition
- Two unrelated `paths:` patterns where each `##` section applies to
  only one (split signal)

**Pass signals:**
- All sections relate to the topic named in the filename
- `paths:` globs target files where every directive in the body applies

**Canonical Repair:** See `repair-playbook.md` → Dimension 3.

---

### Dimension 4: Why Adequacy

*(principle — [Include the *why*](../../../_shared/references/rules-best-practices.md) — for judgment-based rules, name failure cost + exception)*

**What it checks:** Whether the rule includes reasoning, and for
judgment-based rules, whether the why names the failure cost (what
breaks, who bears it) and at least one legitimate exception.

Judgment-based signals from Tier-1 shape hints: presence of
compliant/non-compliant examples, `violation`/`exception`/`failure`
vocabulary, or multi-paragraph why prose.

**Fail signals (→ WARN):**
- No why/reasoning at all (no `**Why:**` line or `## Why` section, no
  rationale in prose)
- Judgment-based rule's why names the violation only ("X is bad") with
  no specific failure cost
- Judgment-based rule has no exception policy — rules that admit no
  exception get disabled wholesale when the edge case arrives

**Pass signals:**
- Simple directive rules ("Use snake_case for table names") — a brief
  inline why is enough
- Judgment-based rules name what specifically breaks and who bears it
- At least one named exception case present

**Canonical Repair:** See `repair-playbook.md` → Dimension 4.

---

### Dimension 5: Scope Tightness

*(principle — [Scope tightly with `paths:`](../../../_shared/references/rules-best-practices.md))*

**What it checks:** Whether the rule's `paths:` scope matches the
breadth of its actual content. An unscoped rule is a context tax on
every unrelated task; a rule whose content names a specific directory
or file type but omits `paths:` wastes budget.

**Fail signals (→ WARN):**
- Rule is always-on (no `paths:`) but content names a specific
  directory, file extension, or module (e.g., rule text mentions
  "React components" or "API handlers" without a corresponding `paths:`)
- `paths:` glob is wider than the content warrants (e.g., `paths: "**/*"`
  for a rule that applies only to TypeScript files)

**Pass signals:**
- Content is project-wide and `paths:` is absent (justified always-on)
- `paths:` globs target exactly the files the rule applies to, no broader

**Canonical Repair:** See `repair-playbook.md` → Dimension 5.

---

### Dimension 6: Staleness

*(principle — [Describe the codebase as it is](../../../_shared/references/rules-best-practices.md))*

**What it checks:** Whether the rule references file paths, commands,
or code patterns that no longer exist in the codebase.

**Evidence to read:** Scan `paths:` globs, code-block examples, and
prose for file paths, command names, framework imports, and pattern
names. Then check the codebase: do those paths exist? Do those
commands and imports still appear?

**Fail signals (→ WARN):**
- `paths:` glob references a directory that does not exist
- Code-block examples reference functions, imports, or modules not
  found in the codebase
- Prose references a dependency or framework not in the project's
  manifest
- Rule mentions a deprecated convention that has been replaced

**Pass signals:**
- All referenced paths exist
- Commands referenced are still in use
- Examples match current code patterns

**Canonical Repair:** See `repair-playbook.md` → Dimension 6.

---

### Dimension 7: Judgment-Not-Linter

*(principle — [Reserve rules for judgment](../../../_shared/references/rules-best-practices.md))*

**What it checks:** Whether the rule restates a check that a formatter,
linter, or type-checker already enforces. Deterministic checks dilute
the authority of rules that genuinely need judgment.

**Fail signals (→ WARN):**
- Rule enforces whitespace/indentation/quote-style (formatter's job)
- Rule enforces import sorting or unused-import removal (linter/tooling
  job)
- Rule enforces type annotations that a type-checker would catch
- Rule restates a conventional-commits / commitlint / prettier rule

**Pass signals:**
- Rule encodes a semantic convention no tool can express ("staging
  models only cast, rename, dedupe")
- Rule captures a judgment call a reviewer would make that a linter
  wouldn't ("error messages name the failing operation and the input
  that caused it")

**Canonical Repair:** See `repair-playbook.md` → Dimension 7.

---

### Dimension 8: Example Realism

*(principle — [Domain-specific examples over synthetic placeholders](../../../_shared/references/rules-best-practices.md); research-grounded — evidence-anchored rubrics deliver +0.17 QWK over inference-only)*

**What it checks:** Whether example code (when present) uses real
identifiers from the codebase rather than synthetic placeholders.

**Scope:** Applies only when the rule contains at least one code block.
Rules with no examples return N/A.

**Fail signals (→ WARN):**
- Examples use generic placeholders (`foo`, `bar`, `baz`,
  `myFunction`, `Thing`, `Widget`) as primary identifiers
- Code looks synthesized rather than sourced (no domain context,
  generic variable names, no recognizable module boundaries)

**Pass signals:**
- Identifiers match the domain vocabulary of the codebase (table names,
  function signatures, module paths that a reader would recognize)
- Optional but strong signal: file path comment showing provenance

**Canonical Repair:** See `repair-playbook.md` → Dimension 8.

---

## Evaluation Prompt Template

Use this skeleton for every Tier-2 LLM call. Criterion statements and
anchor examples come from the rubric above — do not generate them
per-audit.

```
You are auditing a Claude Code rule file. Evaluate all eight dimensions
below in a single response.

Tier-1 shape hints for this rule (use as context, not as dimension
gating): <keywords found, e.g., "compliant, non-compliant, exception,
code blocks present">

For each dimension:
1. Quote the specific text from the rule that is most relevant (evidence)
2. Explain your reasoning
3. State your verdict: WARN, PASS, or N/A
4. Give a specific Recommendation if WARN (name the exact change)

When evidence is borderline, surface as WARN, not PASS.

---

## Dimension 1: Framing
Criterion: Does the rule state what to do (positive framing), not only
what to avoid? Negations are fragile — a dropped `not` inverts the rule.
Pure prohibitions without a positive counterpart earn a WARN.

PASS anchor: "Thread dependencies through constructors."
FAIL anchor: "Don't use global state." (no positive counterpart)

## Dimension 2: Specificity
Criterion: Are the rule's directives verifiable? A directive is
verifiable when a reader can check compliance without subjective
judgment.

PASS anchor: "Use 2-space indentation; run `prettier --check` before committing."
FAIL anchor: "Format code properly and keep files organized."

## Dimension 3: Single Concern
Criterion: Does the rule cover one topic? Every `##` section advances
the same convention; every `paths:` glob targets files where every
directive applies.

PASS anchor: filename `api-handlers.md`, all sections about handlers, `paths: "src/api/**/*.ts"`
FAIL anchor: filename `conventions.md`, sections cover API design AND test naming AND deployment

## Dimension 4: Why Adequacy
Criterion: Does the rule include reasoning? For judgment-based rules
(signaled by compliant/non-compliant examples or failure/exception
vocabulary), does the why name failure cost and at least one exception?

PASS anchor: "X causes [specific failure] in [specific context]. Exception: [named case]."
FAIL anchor: "Avoid X. It's not great." — violation only, no failure cost, no exception

## Dimension 5: Scope Tightness
Criterion: Does `paths:` match the breadth of the rule's content? An
unscoped rule that names a specific directory or file type, or a
`paths:` glob wider than the content warrants, earns a WARN.

PASS anchor: always-on rule for project-wide standard; or `paths: "src/api/**/*.ts"` matching a rule about API handlers
FAIL anchor: unscoped rule whose body begins "For React components…"; or `paths: "**/*"` for a TypeScript-only rule

## Dimension 6: Staleness
Criterion: Do `paths:` globs and example code reference paths, commands,
and patterns that exist in the current codebase?

PASS anchor: `paths: "src/api/**/*.ts"` and `src/api/` exists; example uses imports present in package.json
FAIL anchor: `paths: "app/legacy/**"` references a directory that no longer exists

## Dimension 7: Judgment-Not-Linter
Criterion: Does the rule encode a semantic convention a linter or
formatter couldn't catch? Rules that restate tool-enforceable checks
earn a WARN.

PASS anchor: "Staging models only cast, rename, dedupe" (semantic — no tool catches this)
FAIL anchor: "Use 2-space indentation" when prettier is in the repo (formatter catches this)

## Dimension 8: Example Realism
Criterion: When examples are present, do they use domain-specific
identifiers rather than synthetic placeholders? Returns N/A when no
examples are present.

PASS anchor: example with real codebase identifiers (e.g., `getUser`, `order_id`, `src/api/handlers/users.ts`)
FAIL anchor: example uses `foo`/`bar`/`Widget` placeholders

---

<rule file verbatim>

---

Output format (one block per dimension):
## Dimension N: [Name]
Evidence: "[quoted text from rule]"
Reasoning: [your reasoning]
Verdict: WARN | PASS | N/A
Recommendation: [specific change if WARN, else "None"]
```

---

## Tier 3: Cross-Rule Conflict Detection

*(principle — [Deconflicted rules over overlapping ones](../../../_shared/references/rules-best-practices.md))*

Run after per-rule semantic evaluation. Compare rule pairs that could
co-fire.

**A pair can co-fire when:**
- Both rules are always-on (no `paths:`), OR
- Their `paths:` globs share at least one matching file

**A conflict exists when:** following one rule's directives as written
would cause a developer to violate the other rule.

**Evaluation prompt for each rule pair:**
1. Present Rule A verbatim
2. Present Rule B verbatim
3. Ask: "If a developer follows Rule A's directives exactly, does Rule
   B's guidance contradict?"
4. Ask the reverse
5. If either answer is yes → FAIL finding for both rules

**Output format for conflicts:**
```
FAIL  .claude/rules/rule-a.md — Conflicts with rule-b.md
  "Rule A says X; Rule B says not-X"
FAIL  .claude/rules/rule-b.md — Conflicts with rule-a.md
  "Rule B says not-X; Rule A says X"
```

Anthropic's basis: *"if two rules contradict each other, Claude may
pick one arbitrarily."*

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
in numerical order (Framing → Specificity → Single Concern → Why
Adequacy → Scope Tightness → Staleness → Judgment-Not-Linter → Example
Realism), then Tier-3 conflicts; ties break alphabetically by file
path.

Final summary line: `N rules audited, M findings (X fail, Y warn)` or
`N rules audited — no findings`.
