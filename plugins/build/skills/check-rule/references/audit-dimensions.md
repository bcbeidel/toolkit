---
name: Audit Rule Dimensions
description: Evaluation criteria for auditing a Claude Code `.claude/rules/` library — Tier-1 deterministic format checks, Tier-2 two-dimension semantic rubric, and Tier-3 cross-rule conflict detection.
---

# Audit Rule Dimensions

Rule auditing uses a three-tier hierarchy: deterministic checks first
(no LLM), then semantic evaluation (one LLM call per rule, locked rubric),
then cross-rule conflict detection (separate LLM pass over rule pairs that
could co-fire).

Handle deterministic checks (file location, glob syntax, file size) with
code-style grep/read — faster, cheaper, and more reliable than asking the
LLM to parse them.

## Table of Contents

- [Category Tiers](#category-tiers)
- [Tier 1: Deterministic Format Checks](#tier-1-deterministic-format-checks)
- [Tier 2: Semantic Dimensions (One LLM Call per Rule)](#tier-2-semantic-dimensions-one-llm-call-per-rule)
  - [Always-on dimensions (every rule)](#always-on-dimensions-every-rule)
    - [Dimension 1: Specificity](#dimension-1-specificity)
    - [Dimension 2: Single Concern](#dimension-2-single-concern)
    - [Dimension 3: Staleness](#dimension-3-staleness)
  - [Trigger-gated dimensions (structured-Intent rules only)](#trigger-gated-dimensions-structured-intent-rules-only)
    - [Dimension 4: Intent Completeness](#dimension-4-intent-completeness)
    - [Dimension 5: Example Pair Quality](#dimension-5-example-pair-quality)
    - [Dimension 6: Default-Closed Declaration](#dimension-6-default-closed-declaration)
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
| **research-grounded** | Toolkit-opinion check whose design is supported by published research (cited in `.research/rule-best-practices.md`) |
| **toolkit-opinion** | Recommended by this toolkit; no upstream spec |

The tier appears in parentheses after each dimension heading.

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
  `~/.claude/rules/` are the only canonical locations. Files at `docs/rules/`,
  project root, or other paths are not picked up by Claude Code.
- **Glob validity:** parse each glob in `paths:` with the same logic
  check-skill uses for `paths:` on skills — both fields share the
  same Anthropic semantics.
- **Size warning:** the 200-line threshold mirrors Anthropic's CLAUDE.md
  guidance. Rules above this should be split into topic files.

---

## Tier 2: Semantic Dimensions (One LLM Call per Rule)

Present every applicable dimension as a locked rubric in a single call
per rule. Include the full rule file verbatim — never summarize.

**Per-dimension calls are an anti-pattern.** Per-criterion separate calls
score 11.5 points lower on average (Hong et al., 2026, RULERS). Present
all applicable dimensions simultaneously; score each independently
within the same call.

For each dimension, produce: **verdict** (WARN or PASS), **evidence**
(specific text from the rule that triggered the verdict), and
**recommendation** (what to change). Default-closed: when evidence is
borderline, surface as WARN, not PASS.

### Always-on dimensions (every rule)

Apply Dimensions 1–3 to every rule. Anthropic-spec compliance plus
single-topic discipline plus drift detection apply regardless of body
shape.

#### Dimension 1: Specificity

*(canonical — Anthropic's "Write effective instructions" guidance: "Use 2-space indentation" passes; "Format code properly" fails)*

**What it checks:** Whether the rule's directives are concrete enough
that a developer (or Claude) can verify compliance unambiguously.

**Fail signals (→ WARN):**
- Anchor-free terms used as the directive: "good", "clean", "clear",
  "appropriate", "well-structured", "properly", "nice", "consistent"
  without a behavioral definition
- Directives that defer the decision back to the reader ("use your
  judgment", "as appropriate") without a fallback rule

**Pass signals:**
- Directives are verifiable: a numeric threshold, a named tool to run,
  a specific file path or command, a quoted code pattern
- Anchor-free terms appear only when paired with a verifiable
  definition ("clean code: no functions over 50 lines, no nested
  ternaries")

**Canonical Repair:** Replace each anchor-free term with a verifiable
directive. Examples:
- "Format code properly" → "Use 2-space indentation; run `prettier --check`"
- "Test your changes" → "Run `npm test` before committing"
- "Keep files organized" → "API handlers live in `src/api/handlers/`"

#### Dimension 2: Single Concern

*(toolkit-opinion — one topic per file; mirrors Anthropic's "split larger CLAUDE.md into topic-specific rules")*

**What it checks:** Whether the rule covers a single topic. A file
that mixes unrelated conventions is two rules, not one.

**Fail signals (→ WARN):**
- Multiple top-level `##` sections covering distinct topics that
  wouldn't naturally co-evolve (e.g., "API conventions" and
  "Test conventions" in the same file)
- Filename describes one topic but body covers another in addition
- Two unrelated `paths:` patterns where each `##` section applies to
  only one (split signal)

**Pass signals:**
- All `##` sections relate to the topic named in the filename
- `paths:` globs all target files where every directive in the body
  applies

**Canonical Repair:** Split into separate topic files. Move each
unrelated section to its own `<topic>.md` under `.claude/rules/`.
Update `paths:` if the original was a union covering multiple file
types — each split file gets the subset that actually applies.

#### Dimension 3: Staleness

*(toolkit-opinion — drift detection; mirrors check-skill's time-sensitive-content guidance)*

**What it checks:** Whether the rule references file paths, commands,
or code patterns that no longer exist in the codebase.

**Evidence to read:** Scan `paths:` globs, code-block examples, and
prose for file paths, command names, framework imports, and pattern
names. Then check the codebase: do those paths exist? Do those
commands and imports still appear?

**Fail signals (→ WARN):**
- `paths:` glob references a directory that does not exist in the project
- Code-block examples reference functions, imports, or modules not found in the codebase
- Prose references a dependency or framework not in the project's manifest
- Rule mentions a deprecated convention that has since been replaced

**Pass signals:**
- All referenced paths exist
- Commands referenced are still in use (e.g., `npm test` is in `package.json`)
- Examples match current code patterns

**Canonical Repair (decision tree, in preference order):**
1. **Update** — convention still applies; the referenced code has changed. Replace examples with current code, update file paths.
2. **Delete** — the convention is retired (architectural pattern abandoned, framework replaced). Remove the rule file and document the reason in the commit message.

Anthropic doesn't define an `archived:` status for rules; deletion is the canonical retirement.

---

### Trigger-gated dimensions (structured-Intent rules only)

Apply Dimensions 4–6 only when the rule opts into the toolkit-opinion
structured-Intent shape (see `references/rule-format-guide.md` →
*Toolkit Recommendation*). The trigger:

- Body contains `## Compliant` AND `## Non-compliant` (or
  `## Non-Compliant`) sections, OR
- Body contains `## Why` (or `## Intent`) section

Rules that don't opt in (directive-pattern rules — bullet lists,
single-line style rules) skip these dimensions entirely. Flagging a
plain Anthropic-shape rule on Intent completeness or example-pair
quality would penalize it for not adopting toolkit opinion, which is
not the rubric's intent.

#### Dimension 4: Intent Completeness

*(toolkit-opinion — four-component Why prevents enforcement-without-education failure mode)*

**What it checks:** Whether the `## Why` (or `## Intent`) section
contains the four toolkit-opinion components.

**The four components:**
1. **Violation** — what pattern does this rule catch?
2. **Failure cost** *(load-bearing)* — what specifically goes wrong, and who bears it?
3. **Principle** — what underlying value does this enforce?
4. **Exception policy** *(load-bearing)* — when is disabling this rule legitimate? Name at least one case.

**Fail signals (→ WARN):**
- Why section names the violation only ("Avoid X") with no failure cost
- Why section uses hedging language ("might", "could") where failure cost should be categorical
- No exception policy ("Exception: …") present
- Why section is fewer than 2 sentences — insufficient to carry all four components

**Pass signals:**
- Why explicitly states what goes wrong and who bears the cost
- At least one named exception case ("Exception: …")
- Principle named (type safety, security, maintainability, etc.)

**Canonical Repair:** See `repair-playbook.md` → Dimension 4.

#### Dimension 5: Example Pair Quality

*(research-grounded — evidence-anchored rubrics deliver +0.17 QWK over inference-only)*

**What it checks:** Whether the rule's example pair anchors evaluation
to concrete, real cases.

**Fail signals (→ WARN):**
- Examples use synthetic identifiers (`foo`, `bar`, `myFunction`) without file path comments
- Compliant example appears before non-compliant (listing exclusions first improves accuracy)
- Multiple code snippets in a single section (encodes conflicting behavioral signals)
- One section is missing entirely (compliant present without non-compliant or vice versa)

**Pass signals:**
- Both sections present; non-compliant first
- Each example uses real codebase code with `// path/to/file.ext` comment
- Each section has exactly one canonical example

**Canonical Repair:** See `repair-playbook.md` → Dimension 5.

#### Dimension 6: Default-Closed Declaration

*(toolkit-opinion — keeps borderline cases visible)*

**What it checks:** Whether the Why section declares how borderline /
uncertain cases should resolve.

**Fail signals (→ WARN):**
- No "When evidence is borderline…" line (or equivalent default-closed declaration)
- Declaration is reversed ("when borderline, prefer PASS over WARN")

**Pass signals:**
- Why contains: "When evidence is borderline, prefer WARN over PASS" (or close paraphrase)

**Canonical Repair:** Append to Why section: `"When evidence is borderline, prefer WARN over PASS."`

---

## Evaluation Prompt Template

Use this skeleton for every Tier-2 LLM call. Criterion statements and
anchor examples come from the rubric above — do not generate them
per-audit.

```
You are auditing a Claude Code rule file. Evaluate every applicable
dimension below in a single response.

Dimensions 1–3 always apply. Dimensions 4–6 apply only when the rule
opts into the toolkit-opinion structured-Intent shape — body contains
`## Compliant` AND `## Non-compliant` sections, OR a `## Why` (or
`## Intent`) section. If the rule does not opt in, output "N/A — rule
does not opt into structured-Intent shape" for Dimensions 4–6.

For each applicable dimension:
1. Quote the specific text from the rule that is most relevant (evidence)
2. Explain your reasoning
3. State your verdict: WARN or PASS
4. Give a specific Recommendation if WARN (name the exact change)

When evidence is borderline, surface as WARN, not PASS.

---

## Dimension 1: Specificity (always-on)
Criterion: Are the rule's directives verifiable? A directive is
verifiable when a reader can check compliance without subjective
judgment — a numeric threshold, a named command, a quoted code
pattern, or a specific file path.

PASS anchor: "Use 2-space indentation; run `prettier --check` before committing"
FAIL anchor: "Format code properly and keep files organized"

## Dimension 2: Single Concern (always-on)
Criterion: Does the rule cover one topic? A rule covers one topic
when every `##` section in the body advances the same convention,
and (if `paths:` is present) every glob targets files where every
directive applies.

PASS anchor: filename `api-handlers.md`, all sections about API handler conventions, `paths: "src/api/**/*.ts"`
FAIL anchor: filename `conventions.md`, sections cover API design AND test naming AND deployment process

## Dimension 3: Staleness (always-on)
Criterion: Do `paths:` globs and example code reference paths,
commands, and patterns that exist in the current codebase?

PASS anchor: `paths: "src/api/**/*.ts"` and `src/api/` exists; example code uses imports present in package.json
FAIL anchor: `paths: "app/legacy/**"` references a directory that no longer exists; example uses a deprecated import

## Dimension 4: Intent Completeness (gated)
Criterion: Does the `## Why` (or `## Intent`) section contain all four
toolkit-opinion components: violation, failure cost, principle,
exception policy?

PASS anchor: "X causes [specific failure] in [specific context] (failure cost). This enforces [principle]. Exception: [named case]."
FAIL anchor: "Avoid X. It's not great." — names violation only

## Dimension 5: Example Pair Quality (gated)
Criterion: Does the rule include both `## Compliant` and `## Non-compliant`
sections (non-compliant first), each with one canonical real-code
example with a file path comment?

PASS anchor: `## Non-compliant` first, single example with `// src/api/handlers/users.ts` comment, real domain identifiers
FAIL anchor: examples use `foo`/`bar`, no file path comment; three snippets in one section; compliant before non-compliant

## Dimension 6: Default-Closed Declaration (gated)
Criterion: Does the Why section contain "When evidence is borderline,
prefer WARN over PASS" (or a close paraphrase)?

PASS anchor: "When evidence is borderline, prefer WARN over PASS."
FAIL anchor: no borderline-handling line; or "when borderline, prefer PASS"

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
in numerical order (Specificity → Single Concern → Staleness → Intent
Completeness → Example Pair Quality → Default-Closed Declaration), then
Tier-3 conflicts; ties break alphabetically by file path.

Final summary line: `N rules audited, M findings (X fail, Y warn)` or
`N rules audited — no findings`.
