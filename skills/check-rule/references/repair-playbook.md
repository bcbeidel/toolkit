---
name: Rule Repair Playbook (check-rule)
description: Per-failure-mode repair strategies for check-rule findings — canonical fixes for each audit dimension with intent-preservation constraint and staleness decision tree. Every repair must leave the rule's original behavioral criterion unchanged.
---

# Rule Repair Playbook

Every check-rule finding maps to a canonical repair. Before applying any repair,
state the original intent explicitly: **"This rule enforces [criterion from Intent section]."**
Verify the proposed repair still enforces the same criterion. If the repair would change
what files are in scope, what behavior is required, or what constitutes a violation —
flag it as requiring human review before applying.

---

## Dimension 1: Specificity

### Broad Scope Glob

**Signal:** Scope is `**/*.ext` or `**/*` with no directory prefix

**CHANGE:** Replace broad pattern with directory-prefixed pattern
**FROM:** `scope: "**/*.py"`
**TO:** `scope: "src/api/**/*.py"`
**REASON:** Scope must target the specific architectural layer named in the Intent section. Use the directory where the known failure occurred.

If the convention applies across multiple distinct directories, use a list:
```yaml
scope:
  - "src/api/**/*.py"
  - "src/handlers/**/*.py"
```

### Vague Criterion Terms

**Signal:** Description or Intent uses anchor-free terms ("good", "clean", "clear", "appropriate", "well-structured", "properly formatted") without behavioral definitions

**CHANGE:** Replace each vague term with an observable behavioral definition
**FROM:** `"handlers should be well-structured and clear"`
**TO:** `"handlers must not exceed 50 lines and must declare a return type annotation"`
**REASON:** Two developers must independently make the same pass/fail decision after reading the criterion. Vague terms produce divergent verdicts.

---

## Dimension 2: Research Grounding

### Wrong Example Order

**Signal:** Compliant example appears before non-compliant example

**CHANGE:** Swap the two example sections
**FROM:** `## Compliant Example` ... `## Non-Compliant Example`
**TO:** `## Non-Compliant Example` ... `## Compliant Example`
**REASON:** Listing the rejection case first improves LLM classification accuracy. The compliant example anchors the accepted case after the evaluator has seen what failure looks like.

### Missing Default-Closed Stance

**Signal:** No declaration of how borderline/uncertain cases should resolve

**CHANGE:** Add default-closed declaration to Intent section
**FROM:** Intent section with no uncertainty handling
**TO:** Append to Intent section: "When evidence is borderline, prefer WARN over PASS."
**REASON:** Without this, LLMs default to PASS on ambiguous cases, hiding real violations.

### Multiple Criteria in One Rule

**Signal:** Description contains "and"; rule combines two evaluation dimensions

**CHANGE:** Split into two separate rules, one criterion each
**FROM:** `description: "API handlers must validate input and sanitize output"`
**TO:** Rule A: `"API handlers must validate all input parameters"` + Rule B: `"API handlers must sanitize all output before returning"`
**REASON:** One criterion per rule. Multiple criteria produce conflicting signals and make the rule harder to enforce consistently.

---

## Dimension 3: Staleness

Staleness requires a triage decision before repair. Apply the decision tree in preference order:

### Decision Tree

1. **Update examples** — convention still applies; referenced code has changed
   - Replace examples with current codebase code
   - Update file path comments to current paths
   - Verify the updated example still demonstrates the same behavioral pattern

2. **Archive** — convention still applies conceptually; the specific implementation it targets no longer exists
   - Add `status: archived` to frontmatter
   - Add a note in the frontmatter or Intent section: "Archived: [reason]. Original scope was [X]."
   - Do not delete — the historical record has value if the pattern returns

3. **Delete** — the convention itself is definitively retired (architectural pattern retired, framework replaced)
   - Remove the rule file entirely
   - Document the reason in the commit message: "Remove [rule]: [convention] retired as of [event]"
   - Do not archive — an archived rule implies possible future relevance

**Key distinction:** Update when the pattern is still enforced. Archive when the code is gone but the principle may return. Delete when the convention is definitively retired.

---

## Dimension 4: Fix-Safety Classification

**Signal:** Missing `fix-safety` field; value not `auto-remediable` or `requires-review`

This is a mechanical repair with no intent-preservation risk.

**CHANGE:** Add or correct `fix-safety` field
**FROM:** frontmatter with no `fix-safety` field
**TO:** `fix-safety: requires-review`
**REASON:** Default to `requires-review` when uncertain. Most rule violations involve architectural or design decisions that require human judgment.

**Downgrade to `auto-remediable` only when:**
- The fix preserves all observable behavior
- Examples: formatting rules, import ordering, pure renames with no semantic change
- Do not use `auto-remediable` for correctness violations, security issues, or architectural boundary crossings

For Cursor `.mdc` files (no frontmatter field): add `**Fix-safety:** requires-review` under the Intent heading.
For CLAUDE.md sections: add `**Fix-safety:** requires-review` as a line under the Severity line.

---

## Dimension 5: Rubric Instability

### Synthetic Examples

**Signal:** Examples use generic identifiers (`foo`, `bar`, `myFunction`) or have no file path comment

**CHANGE:** Replace synthetic examples with real codebase examples
**FROM:** `function foo(x) { return bar(x) }`
**TO:** `// src/api/handlers/users.js\nasync function getUser(userId) { return db.users.findById(userId) }`
**REASON:** Evidence-anchored rubrics produce more consistent evaluations (+0.17 QWK) than pure-inference rubrics. Real code with domain context reduces ambiguity.

If no real violating code exists yet, craft a realistic example using actual file paths and domain-specific identifiers from the codebase.

### Hedging Language

**Signal:** Intent uses "might", "usually", "could", "generally", "often"

**CHANGE:** Replace hedging with categorical language
**FROM:** "usually should avoid logging sensitive data"
**TO:** "must not log fields listed in the sensitive-fields registry (`config/sensitive-fields.json`)"
**REASON:** Hedging creates a moving threshold — evaluators disagree on what "usually" means. Categorical language produces consistent verdicts.

**Exception:** If "usually" was load-bearing (acknowledging intentional exceptions), move the exception to the Intent section's exception policy and replace the hedging term with categorical language in the criterion. Example: "Exception: `console.error` for critical runtime errors where structured logging is unavailable."

### Missing Borderline Declaration

**CHANGE:** Add to Intent section
**FROM:** Intent section with no uncertainty handling
**TO:** Append: "When evidence is borderline, prefer WARN over PASS."

---

## Conflicts

**Signal:** Following one rule's compliant example causes another rule to FAIL on the same file

Resolution strategies in preference order:

1. **Narrow scope** — if one rule was over-broad, narrow its glob so the two rules no longer apply to the same files. Verify the narrowed scope still covers the known failure case.

2. **Merge** — if two rules enforce complementary aspects of the same convention, merge into one rule with both criteria stated explicitly. Verify the merged rule passes the 12-criteria validation checklist.

3. **Explicit exception** — add an exception policy to one rule acknowledging the other: "Exception: in files covered by [other-rule-name], [behavior] is acceptable." This preserves both rules without creating contradiction.

4. **Deprecate one** — if one rule supersedes the other: add `status: archived` to the older rule, add a `superseded-by:` field pointing to the newer rule.

**Intent-preservation check for conflict resolution:** Confirm that the resolution preserves the behavioral intent of both rules, not just one. A resolution that silently retires one rule's criterion must be flagged for human review.
