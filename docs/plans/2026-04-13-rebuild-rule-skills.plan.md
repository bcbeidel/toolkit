---
name: Rebuild build-rule and check-rule Skills
description: Rebuild the build-rule and check-rule skills to incorporate new research on rule taxonomy, Intent section quality, example construction, validation methodology, and repair strategies.
type: plan
status: executing
branch: feat/rebuild-rule-skills
related:
  - docs/research/2026-04-13-rule-taxonomy-intent-quality.research.md
  - docs/research/2026-04-13-rule-example-construction.research.md
  - docs/research/2026-04-13-rule-testing-validation.research.md
  - docs/research/2026-04-13-rule-repair-eval-prompts.research.md
  - skills/build-rule/SKILL.md
  - skills/check-rule/SKILL.md
---

# Rebuild build-rule and check-rule Skills

**Goal:** The build-rule and check-rule skills are updated to reflect a complete research corpus on LLM semantic enforcement rules. Users building rules receive taxonomy-aware guidance that sets the right structural properties by rule type, an Intent section model that prevents enforcement-without-education, example construction guidance that produces strong anchors, and a co-located test file for validation before deployment. Users auditing rules receive per-finding repair recommendations with canonical fix strategies, and the evaluation prompt structure is explicitly specified so check-rule produces consistent, auditable results.

**Scope:**

Must have:
- 6 new context docs distilling the 4 research documents into actionable reference material
- build-rule SKILL.md updated: taxonomy classification step, 5-component Intent model, example quality checks, co-located test file output
- build-rule references updated: rule category table with structural properties, Intent section template, testing guide
- check-rule SKILL.md updated: LLM prompt anatomy for semantic audit, repair recommendation per finding
- check-rule references updated: canonical repair per audit dimension, evaluation prompt template

Won't have:
- Coverage gap analysis (identifying rules that should exist but don't — scope decision: check-rule audits quality not completeness)
- Automated test file execution (rule tests are authored for human/agent review, not run by check-rule)
- Changes to the Python linting infrastructure (`scripts/lint.py`, `wos/validators.py`)
- New rule formats beyond the existing WOS/Cursor/Claude Code three

**Approach:** Work in four chunks: (1) distill the 4 research documents into 6 standalone context documents that the skills can reference; (2) rebuild build-rule to incorporate taxonomy-aware elicitation, Intent quality enforcement, example construction checks, and test file generation; (3) rebuild check-rule to specify the LLM evaluation prompt structure and add repair recommendations to findings output; (4) run reindex and full lint to confirm the system is clean. Context docs are written first because both skills will reference them via the references/ pattern — they're the shared knowledge base, not inline skill content.

**File Changes:**
- Create: `docs/context/rule-type-taxonomy-and-structural-properties.context.md`
- Create: `docs/context/rule-intent-section-quality.context.md`
- Create: `docs/context/rule-example-construction-methodology.context.md`
- Create: `docs/context/rule-testing-and-validation-methodology.context.md`
- Create: `docs/context/rule-repair-strategies-by-failure-mode.context.md`
- Create: `docs/context/llm-audit-prompt-anatomy.context.md`
- Create: `skills/build-rule/references/rule-testing-guide.md`
- Create: `skills/check-rule/references/repair-playbook.md`
- Modify: `skills/build-rule/SKILL.md` (taxonomy step, Intent 5-component requirement, example quality checks, test file output)
- Modify: `skills/build-rule/references/rule-format-guide.md` (category table, Intent template, fix-safety by type)
- Modify: `skills/check-rule/SKILL.md` (prompt anatomy specification in Step 3, repair recommendation in Step 5 output format)
- Modify: `skills/check-rule/references/audit-dimensions.md` (canonical repair per dimension, evaluation prompt template)

**Branch:** `feat/rebuild-rule-skills`
**PR:** TBD

---

## Chunk 1: Context Documents

### Task 1: Rule type taxonomy context doc

**Files:**
- Create: `docs/context/rule-type-taxonomy-and-structural-properties.context.md`

- [x] Create context doc distilling Part A of `docs/research/2026-04-13-rule-taxonomy-intent-quality.research.md` into a standalone context document. Cover: the 8-category taxonomy (correctness, suspicious, security, complexity, performance, convention/style, accessibility, LLM directive); structural properties per category (binary vs. ordinal framing, fix-safety default, scope strategy); the finding that categorization benefit for LLMs is unvalidated assumption — value is authoring clarity. Target 300–500 words.
- [x] Verify: `python scripts/lint.py --root docs/context/rule-type-taxonomy-and-structural-properties.context.md --no-urls` — no failures
- [x] Commit: `chore: add rule-type-taxonomy context doc` <!-- sha:c8f97a2 -->

---

### Task 2: Intent section quality context doc

**Files:**
- Create: `docs/context/rule-intent-section-quality.context.md`

- [x] Create context doc distilling Part B of `docs/research/2026-04-13-rule-taxonomy-intent-quality.research.md`. Cover: the 5-component model (violation, failure cost, principle, exception policy, fix-safety); weak Intent signals (violation-only, hedging language, no exception policy, prohibition without consequence); the enforcement-without-education failure mode and its four preventions; the worked strong/weak example. Target 300–500 words.
- [x] Verify: lint passes, file is 200–800 words (`wc -w docs/context/rule-intent-section-quality.context.md`)
- [x] Commit: `chore: add rule-intent-section-quality context doc` <!-- sha:c8f97a2 -->

---

### Task 3: Rule example construction methodology context doc

**Files:**
- Create: `docs/context/rule-example-construction-methodology.context.md`

- [x] Create context doc from `docs/research/2026-04-13-rule-example-construction.research.md`. Cover: single canonical example outperforms multiple for LLM anchoring (introducing conflicting signals risk); real code outperforms synthetic (evidence-anchored rubrics +0.17 QWK over pure-inference); what makes an example "real enough" (file path comment, non-generic identifiers, surrounding context); non-compliant before compliant and why; what to do when no real violating code exists yet (craft to realistic density, add file path comment). Target 300–500 words.
- [x] Verify: lint passes
- [x] Commit: `chore: add rule-example-construction-methodology context doc` <!-- sha:c8f97a2 -->

---

### Task 4: Rule testing and validation methodology context doc

**Files:**
- Create: `docs/context/rule-testing-and-validation-methodology.context.md`

- [x] Create context doc from `docs/research/2026-04-13-rule-testing-validation.research.md`. Cover: two-polarity test structure (PASS / FAIL cases, rationale note per case); project-scale sample size (10–20 initial, 20–35 pre-deployment); temperature=0 + 3-run majority vote, pass^k vs pass@k; two-gate criteria (Gate 1 warn: ≥90% TP, ≥85% TN, ≥80% consistency; Gate 2 fail: ≥95% TP, ≥90% TN, ≥90% + CoT spot-check); evaluator-first failure triage. Target 400–600 words.
- [x] Verify: lint passes
- [x] Commit: `chore: add rule-testing-and-validation-methodology context doc` <!-- sha:c8f97a2 -->

---

### Task 5: Rule repair strategies context doc

**Files:**
- Create: `docs/context/rule-repair-strategies-by-failure-mode.context.md`

- [x] Create context doc from `docs/research/2026-04-13-rule-repair-eval-prompts.research.md`. Cover canonical repair per failure mode: specificity (narrow scope or add behavioral definitions); staleness (update examples, archive, or delete based on whether the convention itself still applies); rubric instability (replace hedging language with categorical directives, swap synthetic examples for real); conflict (merge, narrow scope, deprecate one, or add explicit caveats); research grounding (fix example ordering, add default-closed stance declaration). Include intent-preservation constraint: repair must preserve the rule's original criterion. Target 400–600 words.
- [x] Verify: lint passes
- [x] Commit: `chore: add rule-repair-strategies context doc` <!-- sha:c8f97a2 -->

---

### Task 6: LLM audit prompt anatomy context doc

**Files:**
- Create: `docs/context/llm-audit-prompt-anatomy.context.md`

- [x] Create context doc from `docs/research/2026-04-13-rule-repair-eval-prompts.research.md`. Cover: the 6-element prompt anatomy (criterion statement, scale declaration, anchor examples, CoT requirement, output format schema, default-closed instruction); evidence-before-verdict ordering and why it prevents confirmation bias; locked rubric (evaluation call) vs. open generation (repair call) — these must be separate calls; criterion statement as highest-leverage element (removing it drops human correlation from 0.666 to 0.487). Target 350–500 words.
- [x] Verify: lint passes
- [x] Commit: `chore: add llm-audit-prompt-anatomy context doc` <!-- sha:c8f97a2 -->

---

## Chunk 2: Rebuild build-rule

### Task 7: build-rule SKILL.md — taxonomy, Intent model, example checks, test file output

**Files:**
- Modify: `skills/build-rule/SKILL.md`

Read the current `skills/build-rule/SKILL.md` before making any changes.

- [x] **Step 2 (Elicit Pattern):** After determining scope and severity, add a category classification step. Present the 8 categories (reference `rule-type-taxonomy-and-structural-properties.context.md`); ask which best describes the rule. Use the answer to set: fix-safety default (auto-remediable for correctness/style; requires-review for security/suspicious/complexity/LLM directive), binary vs. ordinal framing, and severity recommendation.
- [x] **Step 4 (Draft Rule):** Add explicit Intent section requirements. The Intent must contain all 5 components: what the rule catches (violation), what goes wrong if violated (failure cost), what underlying value this protects (principle), when disabling is legitimate (exception policy), and whether the fix is always safe (fix-safety signal). Flag and require any missing component before proceeding.
- [x] **Step 5 (Validate Structure):** Extend the 9 validation criteria checklist with: (10) Intent has all 5 components — no weak signals present (hedging language, prohibition-without-consequence, no exception policy); (11) Primary example is single and canonical — flag if multiple examples risk conflicting signals; (12) Examples have file path comments or realistic identifiers — flag if synthetic.
- [x] **Step 7 (Write the Rule):** After writing the rule file, also write a co-located test file at `<same-dir>/<slug>.tests.md` with a minimum of 3 PASS cases and 3 FAIL cases, each with rationale. Reference `skills/build-rule/references/rule-testing-guide.md` for format.
- [x] **Key Instructions + Anti-Pattern Guards:** Add: missing Intent components must be resolved before writing; missing test file is a delivery failure; single canonical example preferred over multiple.
- [x] Verify: `python scripts/lint.py --root skills/build-rule --no-urls` — no failures; `wc -l skills/build-rule/SKILL.md` outputs ≤500
- [x] Commit: `feat: rebuild build-rule — taxonomy, Intent model, example checks, test file output` <!-- sha:b465454 -->

---

### Task 8: build-rule rule-format-guide.md — category table, Intent template, fix-safety by type

**Files:**
- Modify: `skills/build-rule/references/rule-format-guide.md`

Read the current file before making any changes.

- [x] Add a "Rule Categories" section before the Format Detection section. Include the 8-category table with: category name, ESLint/Biome analog, fix-safety default, binary-or-ordinal framing. Keep it compact — this is a lookup reference, not prose explanation.
- [x] Add an "Intent Section Template" to the Writing Effective Rules section. Show the 5-component structure with inline labels and a worked example demonstrating strong vs. weak Intent for the same rule.
- [x] Update the Fix-Safety Classification table to note category-level defaults (currently the table only has the two values and when-to-use; add a column or note mapping categories to defaults).
- [x] Verify: `python scripts/lint.py --root skills/build-rule --no-urls` — no failures
- [x] Commit: `feat: update rule-format-guide — category table, Intent template, fix-safety defaults by type` <!-- sha:b465454 -->

---

### Task 9: build-rule rule-testing-guide.md — test file format and acceptance criteria

**Files:**
- Create: `skills/build-rule/references/rule-testing-guide.md`

- [x] Create reference doc covering: test file naming convention (`<slug>.tests.md` co-located with rule file); PASS / FAIL section structure with rationale-note field per case; minimum viable set (3 PASS + 3 FAIL for Gate 1 warn deployment; 8–10 cases for Gate 2 fail promotion); what makes a good test case (one from obvious pattern, one borderline, one known FP/FN candidate); do not use the same code as the rule's own compliant/non-compliant examples (those anchor the rule; tests must be independent). Include a short worked example.
- [x] Add a `references:` entry for this file in `skills/build-rule/SKILL.md` frontmatter.
- [x] Verify: `python scripts/lint.py --root skills/build-rule --no-urls` — no failures
- [x] Commit: `feat: add rule-testing-guide reference to build-rule` <!-- sha:b465454 -->

---

## Chunk 3: Rebuild check-rule

### Task 10: check-rule SKILL.md — prompt anatomy, repair recommendations in output

**Files:**
- Modify: `skills/check-rule/SKILL.md`

Read the current `skills/check-rule/SKILL.md` before making any changes.

- [x] **Step 3 (Semantic Audit):** Specify the 6-element prompt anatomy that the LLM evaluation call must include. The call must contain: (1) criterion statement (the specific dimension being evaluated), (2) PASS/FAIL scale declaration with behavioral definitions, (3) one PASS anchor example and one FAIL anchor example, (4) explicit CoT requirement ("explain your reasoning before stating your verdict"), (5) structured output format (dimension, verdict, evidence, recommendation), (6) default-closed instruction ("when evidence is borderline, surface as WARN"). Reference `skills/check-rule/references/audit-dimensions.md` for the locked rubric text.
- [x] **Step 5 (Report Findings):** Each FAIL or WARN finding must now include a `Recommendation:` line with the canonical repair strategy from `skills/check-rule/references/repair-playbook.md`. Example output format: `WARN  docs/rules/foo.rule.md — Specificity: scope glob too broad\n  Recommendation: Add directory prefix to scope (e.g., src/api/**/*.py instead of **/*.py)`
- [x] **Anti-Pattern Guards:** Add: (6) generic repair suggestions ("fix this") with no actionable instruction — every recommendation must name the specific change; (7) omitting the criterion statement from the evaluation prompt — removing it drops human correlation by 26%.
- [x] Verify: `python scripts/lint.py --root skills/check-rule --no-urls` — no failures; `wc -l skills/check-rule/SKILL.md` outputs ≤500
- [x] Commit: `feat: rebuild check-rule — prompt anatomy, repair recommendations in output` <!-- sha:1963299 -->

---

### Task 11: check-rule audit-dimensions.md — canonical repair per dimension, prompt template

**Files:**
- Modify: `skills/check-rule/references/audit-dimensions.md`

Read the current file before making any changes.

- [x] For each of the 5 Tier 2 dimensions, add a **Canonical Repair** subsection after the Pass/Fail signals. Each repair section names the specific change for the most common failure pattern in that dimension (drawn from `docs/context/rule-repair-strategies-by-failure-mode.context.md`).
- [x] Add a new **Evaluation Prompt Template** section at the end of the Tier 2 block. Provide a skeleton prompt showing all 6 required elements (criterion statement placeholder, scale, anchor examples, CoT instruction, output format schema, default-closed instruction). This is the template the executor uses to construct each per-rule LLM call.
- [x] Verify: file still passes lint; all 5 dimensions have a Canonical Repair section
- [x] Commit: `feat: update audit-dimensions — canonical repair per dimension, evaluation prompt template` <!-- sha:5b2bbfe -->

---

### Task 12: check-rule repair-playbook.md — per-failure-mode repair reference

**Files:**
- Create: `skills/check-rule/references/repair-playbook.md`

- [x] Create reference doc with a repair entry for each of the 5 audit dimensions plus conflicts. Each entry: (a) failure signal that triggers this repair, (b) canonical fix with specific language (not just "make it more specific" but "replace vague terms with behavioral definitions: instead of 'good' write 'contains all four required sections'"), (c) intent-preservation constraint (repair must leave the original criterion unchanged — do not silently expand or contract scope), (d) when to archive instead of repair (if the convention itself no longer applies, archiving is correct). Include the staleness decision tree (update examples → archive → delete, in that preference order).
- [x] Add a `references:` entry for this file in `skills/check-rule/SKILL.md` frontmatter.
- [x] Verify: `python scripts/lint.py --root skills/check-rule --no-urls` — no failures
- [x] Commit: `feat: add repair-playbook reference to check-rule` <!-- sha:5a1123d -->

---

## Chunk 4: Integration

### Task 13: Reindex and full lint clean

**Files:**
- Modify: all `_index.md` files (auto-generated)

- [x] Run `python scripts/reindex.py --all-dirs` — verify output: "Wrote N _index.md files, no errors"
- [x] Run `python scripts/lint.py --no-urls` — verify: 0 FAIL findings; any WARN findings reviewed and addressed or documented as acceptable
- [x] Commit: `chore: reindex after rule skill rebuild` <!-- sha:212e042 -->

---

## Validation

- [ ] `python scripts/lint.py --root skills/build-rule --no-urls` — 0 failures
- [ ] `python scripts/lint.py --root skills/check-rule --no-urls` — 0 failures
- [ ] `python scripts/lint.py --root docs/context --no-urls` — 0 failures on any of the 6 new context docs
- [ ] `wc -l skills/build-rule/SKILL.md` — output ≤500
- [ ] `wc -l skills/check-rule/SKILL.md` — output ≤500
- [ ] Confirm `skills/build-rule/SKILL.md` contains: taxonomy classification step, 5-component Intent requirement, test file output in Step 7
- [ ] Confirm `skills/check-rule/SKILL.md` contains: 6-element prompt anatomy in Step 3, `Recommendation:` field in Step 5 output format
- [ ] Confirm `skills/check-rule/references/audit-dimensions.md` contains a Canonical Repair section for all 5 Tier 2 dimensions
