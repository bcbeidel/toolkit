---
name: build-rule + audit-rule skills
description: Add /wos:build-rule and /wos:audit-rule as the build-X/audit-X pair for Claude Code rules, replacing deprecated check-rules and extract-rules
type: plan
status: executing
related:
  - docs/context/llm-rule-structural-characteristics.context.md
  - docs/context/linter-patterns-transferable-to-llm-rules.context.md
  - docs/context/rule-system-failure-modes-fatigue-and-instability.context.md
  - docs/context/rule-library-operational-practices.context.md
  - docs/context/rubric-specificity-and-deterministic-first-evaluation.context.md
---

# build-rule + audit-rule skills

**Goal:** Add `/wos:build-rule` and `/wos:audit-rule` to the `build-X`/`audit-X` skill family, replacing `extract-rules` and `check-rules` respectively. `build-rule` creates correctly-structured rules across project formats (WOS `.rule.md`, Cursor `.mdc`, Claude Code CLAUDE.md) with conflict detection and structural validation. `audit-rule` evaluates rule libraries for six quality dimensions (conflicts, coverage gaps, specificity, research grounding, staleness, format compliance) and reports findings in `scripts/lint.py` output format. Both predecessors emit deprecation notices before proceeding.

**Scope:**

Must have:
- `skills/build-rule/SKILL.md` — full 7-step creation workflow with conflict detection and structure validation
- `skills/build-rule/references/rule-format-guide.md` — extended format guide covering WOS, Cursor, and CLAUDE.md formats
- `skills/audit-rule/SKILL.md` — 5-step audit workflow covering all 6 quality dimensions
- `skills/audit-rule/references/audit-dimensions.md` — evaluation criteria for each audit dimension
- Deprecation notice prepended to `skills/check-rules/SKILL.md`
- Deprecation notice prepended to `skills/extract-rules/SKILL.md`

Won't have:
- Changes to `scripts/lint.py` or any Python validators (audit-rule is skill-only)
- Auto-remediation of rule issues (findings are informational)
- Persistent rule conflict database (all checks are in-context per invocation)
- Removal of `check-rules` or `extract-rules` directories (deprecated, not deleted)

**Approach:** `build-rule` extends `extract-rules` with four new capabilities: format detection (WOS `.rule.md`, Cursor `.mdc`, or CLAUDE.md section); conflict checking before write; structural validation against the four LLM rule requirements (specificity, scale matching, scope isolation, behavioral anchoring) and five linter patterns (meta/create separation, start-narrow, default-closed, fix-safety classification, concern-prefix); and fix-safety classification — each rule must declare whether its findings are auto-remediable or require human judgment.

`audit-rule` uses the three-tier grading hierarchy from `rubric-specificity-and-deterministic-first-evaluation.context.md`: (1) deterministic format compliance first (parse required frontmatter fields and body sections — no LLM needed); (2) one LLM call per rule with all five semantic dimensions as a locked rubric in a single pass — complete rubric evaluation outperforms per-dimension calls by 11.5 points on average (per Hong et al. 2026); (3) cross-rule conflict detection as a second LLM pass over rule pairs. Deprecation blocks in the old skills present a prompt before continuing.

**File Changes:**
- Create: `skills/build-rule/SKILL.md`
- Create: `skills/build-rule/references/rule-format-guide.md`
- Create: `skills/audit-rule/SKILL.md`
- Create: `skills/audit-rule/references/audit-dimensions.md`
- Modify: `skills/check-rules/SKILL.md` (prepend deprecation block)
- Modify: `skills/extract-rules/SKILL.md` (prepend deprecation block)

**Branch:** `feat/build-audit-rule`
**PR:** TBD

---

### Task 1: Create `skills/build-rule/` — SKILL.md and rule-format-guide reference

**Files:**
- Create: `skills/build-rule/SKILL.md`
- Create: `skills/build-rule/references/rule-format-guide.md`

- [x] **Step 1:** Write `skills/build-rule/references/rule-format-guide.md`. Start from `skills/extract-rules/references/rule-format-guide.md` (which covers `docs/rules/*.rule.md`). Extend with two additional format sections:

  **Cursor format (`.mdc`):**
  ```
  .cursor/rules/<slug>.mdc
  ---
  description: <one-sentence trigger description>
  globs: <glob pattern>
  alwaysApply: false
  ---
  <rule body in markdown>
  ```

  **Claude Code format (CLAUDE.md section):**
  Rules embedded directly in `CLAUDE.md` as named sections with a `## Rule: <name>` heading, intent, and compliant/non-compliant examples.

  Also add a **Format Detection** section: if `.cursor/` exists → Cursor; if `CLAUDE.md` exists and no `docs/rules/` → CLAUDE.md; otherwise → WOS `.rule.md`. User can override.

- [x] **Step 2:** Write `skills/build-rule/SKILL.md` with this 7-step workflow:
  1. **Detect format** — check project structure; report detected format; allow override
  2. **Elicit pattern** — three intake modes: conversation (user describes), from-code (user points to exemplary files), from-source (style guide or RFC). Ask one clarifying question at a time.
  3. **Check for conflicts** — read existing rules matching similar scope or description; if overlap found, show it and ask user to merge, replace, or keep both
  4. **Draft rule** — compose rule following the format guide for the detected format. Non-compliant example placed BEFORE compliant example (research: listing exclusions first improves classification accuracy).
  5. **Validate structure** — self-check against four structural requirements (specificity, scale matching, scope isolation, behavioral anchoring) AND five linter patterns (meta/create separation — criterion defined separately from evaluation prompt; start-narrow — starts from a known failure case; default-closed — undefined states surface as WARN not PASS; fix-safety classification — explicitly declares whether findings are auto-remediable or require human judgment; concern-prefix organization — rule name prefixed by domain when library has >5 rules). Fix any gaps before presenting.
  6. **Present for approval** — show complete rule; iterate on user feedback; do not write until approved
  7. **Write the rule** — create parent directory if needed; write file

  Required frontmatter (all formats have an equivalent): name, description, type (or alwaysApply), scope (or globs), severity (or `alwaysApply: false`).

  Include these anti-pattern guards:
  1. Rules without both examples — refuse; examples improve enforcement reliability 4×
  2. Overly broad scope (`**/*` or `**/*.py` without directory prefix) — flag, require narrowing
  3. Multiple conventions in one rule — split
  4. Linter-appropriate checks — recommend the appropriate linter instead
  5. Missing default-closed stance — require declaration of how uncertain cases resolve
  6. Skipping conflict check — always check existing rules before writing

  Handoff block:
  - Receives: code pattern, behavior description, or existing rule draft
  - Produces: rule file written to appropriate location for detected format
  - Chainable to: audit-rule (to verify the new rule doesn't conflict with the library)

- [x] **Step 3:** Verify: `python scripts/lint.py --root /Users/bbeidel/Documents/git/wos-build-rule --no-urls 2>&1 | grep -E "build-rule|ERROR|FAIL"` — no failures on build-rule; `grep -c "Anti-Pattern" skills/build-rule/SKILL.md` → ≥ 1; `grep "Handoff" skills/build-rule/SKILL.md` → match

- [x] **Step 4:** Commit: `git -C /Users/bbeidel/Documents/git/wos-build-rule add skills/build-rule/ && git -C /Users/bbeidel/Documents/git/wos-build-rule commit -m "feat: add /wos:build-rule skill with multi-format support and conflict detection"` <!-- sha:2d58b7e -->

---

### Task 2: Create `skills/audit-rule/` — SKILL.md and audit-dimensions reference

**Files:**
- Create: `skills/audit-rule/SKILL.md`
- Create: `skills/audit-rule/references/audit-dimensions.md`

**Depends on:** Task 1 (sequential; shares same session, no structural dependency)

- [x] **Step 1:** Write `skills/audit-rule/references/audit-dimensions.md`. The file has two sections: **deterministic checks** (run first, no LLM needed) and **semantic dimensions** (evaluated in one LLM call per rule with the full rubric present).

  **Deterministic checks (parse/grep — no LLM):**

  | Check | Fail condition | Severity |
  |-------|---------------|----------|
  | Required frontmatter | Missing `name`, `description`, `type`, `scope`, or `severity` field | fail |
  | Required body sections | Missing `## Intent`, `## Non-Compliant Example`, or `## Compliant Example` | fail for Intent, warn for examples |
  | Severity value | Not `warn` or `fail` | fail |

  **Semantic dimensions (one LLM call per rule, all five presented simultaneously as locked rubric):**

  | Dimension | Verdict trigger | Severity |
  |-----------|----------------|----------|
  | **Specificity** | Scope glob is `**/*` or `**/*.ext` without directory prefix; OR description uses "good", "clean", "appropriate", "clear" without behavioral definition | warn |
  | **Research grounding** | Rule violates guidance in `llm-rule-structural-characteristics.context.md` (e.g., multi-dimension rule, no behavioral anchor) or `linter-patterns-transferable-to-llm-rules.context.md` (e.g., missing default-closed stance) | warn |
  | **Staleness** | Rule references a tool, API, or pattern not present in the current codebase | warn |
  | **Fix-safety classification** | Rule has no declaration of whether findings are auto-remediable or require human judgment | warn |
  | **Rubric instability risk** | Non-compliant/compliant examples are absent or synthetic (not drawn from actual code patterns); phrasing contains hedging ("might", "usually", "generally") | warn |

  **Cross-rule conflict detection (separate LLM pass over rule pairs):**
  Two rules conflict when following one rule's compliant example would cause the other rule to produce a FAIL verdict. Present both rule files verbatim; ask: "Would complying with Rule A cause Rule B to fail?" → FAIL if yes.

  Default-closed on all semantic dimensions: borderline evidence surfaces as WARN, never silently PASS.

- [x] **Step 2:** Write `skills/audit-rule/SKILL.md` with this 5-step workflow applying the three-tier grading hierarchy (deterministic first, then LLM):

  1. **Discover rules** — find all rule files (`.rule.md` in `docs/rules/`, `.mdc` in `.cursor/rules/`, `## Rule:` sections in CLAUDE.md). If path argument provided, scope to that path.
  2. **Deterministic format check** — for each rule, parse frontmatter and body without LLM: check required fields exist, required sections present, severity is `warn` or `fail`. Emit findings immediately; do not pass structurally invalid rules to the LLM step.
  3. **Semantic audit (one LLM call per rule)** — for each structurally valid rule, present the FULL rule file verbatim plus all five semantic dimension rubrics from [audit-dimensions.md](references/audit-dimensions.md) in a single call. Score all five dimensions in one pass. Do not make per-dimension calls — research shows per-criterion separate calls score 11.5 points lower on average due to excessive stringency (Hong et al. 2026, `rubric-specificity-and-deterministic-first-evaluation.context.md`).
  4. **Conflict detection (separate LLM pass)** — compare rule pairs: for each pair, present both rules verbatim and ask whether complying with one would fail the other. This requires pair-level context unavailable in the per-rule step, so it is a second pass.
  5. **Report findings** — output in `scripts/lint.py` format (file, issue, severity). Sort: FAIL first, WARN second. Summary: `N rules audited, M findings (X fail, Y warn)`. On a clean library: "N rules audited — no findings."

  Input: path to a rules file or directory; if none provided, scan project for all rule formats.

  Key instructions:
  - Run deterministic checks before invoking the LLM — do not send malformed rules to LLM evaluation
  - Present all five semantic dimensions as a locked rubric in one call per rule; never split into per-dimension calls
  - Include the full rule file verbatim in every evaluation — never summarize
  - For conflict detection, evaluate rule PAIRS; cite both rule names and the specific contradiction
  - Default-closed: borderline evidence surfaces as WARN, never silently PASS

  Anti-pattern guards:
  1. Per-dimension LLM calls — degrades accuracy by 11.5 points; use complete rubric in one call
  2. LLM-evaluating format compliance — deterministic check is faster, cheaper, and more reliable
  3. Treating ambiguous compliance as PASS — default-closed; surface as WARN
  4. Reporting vague findings — every FAIL/WARN must cite the specific rule file and the failing criterion

  Handoff block:
  - Receives: path to rules file, directory, or no argument (scans project)
  - Produces: structured findings report (file, issue, severity)
  - Chainable to: build-rule (to fix flagged issues)

- [x] **Step 3:** Verify: `python scripts/lint.py --root /Users/bbeidel/Documents/git/wos-build-rule --no-urls 2>&1 | grep -E "audit-rule|ERROR|FAIL"` — no failures on audit-rule; `grep -c "dimension\|Conflict\|Coverage\|Specificity\|Staleness\|Format" skills/audit-rule/references/audit-dimensions.md` → ≥ 6; `grep "Handoff" skills/audit-rule/SKILL.md` → match

- [x] **Step 4:** Commit: `git -C /Users/bbeidel/Documents/git/wos-build-rule add skills/audit-rule/ && git -C /Users/bbeidel/Documents/git/wos-build-rule commit -m "feat: add /wos:audit-rule skill with six-dimension rule quality evaluation"` <!-- sha:2456569 -->

---

### Task 3: Deprecate `check-rules` and `extract-rules` + lint clean

**Files:**
- Modify: `skills/check-rules/SKILL.md`
- Modify: `skills/extract-rules/SKILL.md`

**Depends on:** Tasks 1 and 2 (must exist before directing users to replacements)

- [ ] **Step 1:** Prepend the following deprecation block to `skills/check-rules/SKILL.md`, immediately before `# /wos:check-rules`:

  ```markdown
  > **Deprecated.** This skill is replaced by `/wos:audit-rule`.
  > `/wos:audit-rule` provides all check-rules functionality plus conflict detection,
  > coverage gap analysis, specificity checks, research grounding, and staleness detection.
  >
  > Proceed with check-rules anyway? If not, invoke `/wos:audit-rule` instead.
  ```

  Then ask the user "Proceed anyway? (y/n)" and only continue the existing check-rules workflow if the user confirms.

- [ ] **Step 2:** Prepend the following deprecation block to `skills/extract-rules/SKILL.md`, immediately before `# /wos:extract-rules`:

  ```markdown
  > **Deprecated.** This skill is replaced by `/wos:build-rule`.
  > `/wos:build-rule` provides all extract-rules functionality plus multi-format support
  > (WOS `.rule.md`, Cursor `.mdc`, Claude Code CLAUDE.md), conflict detection, and
  > structural validation against LLM rule research.
  >
  > Proceed with extract-rules anyway? If not, invoke `/wos:build-rule` instead.
  ```

  Then ask the user "Proceed anyway? (y/n)" and only continue the existing extract-rules workflow if the user confirms.

- [ ] **Step 3:** Verify deprecation blocks are in place:
  ```bash
  grep -A2 "Deprecated" skills/check-rules/SKILL.md skills/extract-rules/SKILL.md
  ```
  Expected: both files contain "Deprecated" notice near the top.

- [ ] **Step 4:** Run full lint clean:
  ```bash
  python scripts/lint.py --root /Users/bbeidel/Documents/git/wos-build-rule --no-urls
  ```
  Expected: no new failures; any existing warnings are pre-existing.

- [ ] **Step 5:** Commit:
  ```bash
  git -C /Users/bbeidel/Documents/git/wos-build-rule add skills/check-rules/SKILL.md skills/extract-rules/SKILL.md
  git -C /Users/bbeidel/Documents/git/wos-build-rule commit -m "feat: deprecate check-rules and extract-rules in favor of audit-rule and build-rule"
  ```

---

## Validation

- [ ] `grep -A2 "Deprecated" skills/check-rules/SKILL.md skills/extract-rules/SKILL.md` — both files contain deprecation notices
- [ ] `python scripts/lint.py --root /Users/bbeidel/Documents/git/wos-build-rule --no-urls` — exits clean (no new failures vs. main)
- [ ] `ls skills/build-rule/SKILL.md skills/build-rule/references/rule-format-guide.md skills/audit-rule/SKILL.md skills/audit-rule/references/audit-dimensions.md` — all four files exist
- [ ] `grep "Handoff" skills/build-rule/SKILL.md skills/audit-rule/SKILL.md` — both skills have Handoff sections
- [ ] Manual: invoke `/wos:build-rule` with a code pattern → rule written to correct format location for project; no conflicts reported for a clean library
- [ ] Manual: invoke `/wos:audit-rule` on `docs/rules/` → findings report in file/issue/severity format; "no findings" on a clean library
- [ ] Manual: invoke `/wos:check-rules` → deprecation notice appears before workflow proceeds
- [ ] Manual: invoke `/wos:extract-rules` → deprecation notice appears before workflow proceeds

## Notes

- Roadmap reference: `docs/plans/2026-04-10-roadmap-v036-v039.plan.md` Task 12. Update Task 12 checkbox with merge commit SHA when PR merges.
- Context references used:
  - `llm-rule-structural-characteristics.context.md` — four structural requirements (specificity, scale matching, scope isolation, behavioral anchoring)
  - `linter-patterns-transferable-to-llm-rules.context.md` — five transferable patterns (meta/create separation, start-narrow, default-closed, fix-safety classification, concern-prefix)
  - `rubric-specificity-and-deterministic-first-evaluation.context.md` — three-tier grading hierarchy; complete rubric outperforms per-dimension calls; deterministic checks before LLM
  - `rule-system-failure-modes-fatigue-and-instability.context.md` — alert fatigue, enforcement without rationale, rubric instability as compounding failure modes
  - `rule-library-operational-practices.context.md` — warn-before-enforce, 100 labeled examples, structured output, positive+negative test cases
- Issue: bcbeidel/wos#227
