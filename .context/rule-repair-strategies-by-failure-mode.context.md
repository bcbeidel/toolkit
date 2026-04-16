---
name: Rule Repair Strategies by Failure Mode
description: Canonical repair strategies for each check-rule audit failure mode — specificity, staleness, rubric instability, conflict resolution, and research grounding failures. Every repair must preserve the rule's original behavioral intent; repairs that narrow scope or change examples without preserving intent require human review.
type: concept
confidence: high
created: 2026-04-13
updated: 2026-04-13
sources:
  - https://arxiv.org/abs/2601.08654
  - https://semgrep.dev/blog/2020/writing-semgrep-rules-a-methodology/
  - https://medium.com/agoda-engineering/how-to-make-linting-rules-work-from-enforcement-to-education-be7071d2fcf0
related:
  - docs/research/2026-04-13-rule-repair-eval-prompts.research.md
  - docs/context/rule-system-failure-modes-fatigue-and-instability.context.md
  - docs/context/rule-library-operational-practices.context.md
---

# Rule Repair Strategies by Failure Mode

## Key Insight

A check-rule finding without a repair strategy is diagnosis without prescription. Every audit finding maps to a canonical repair. All repairs share one constraint: **intent preservation** — the repair must leave the rule's original behavioral criterion unchanged. A repair that passes the audit by narrowing scope, swapping examples, or removing hedging language in a way that changes *what* the rule enforces is worse than the original failure.

## Intent Preservation Constraint

Before applying any repair, state the original intent explicitly: "This rule enforces [original criterion from Intent section]." Verify that the proposed repair still enforces the same criterion. If the repair would change what files are in scope, what behavior is required, or what constitutes a violation — flag it as requiring human review before applying.

## Dimension 1: Specificity Failures

**Signal:** Scope glob too broad (`**/*` or `**/*.ext` without directory prefix); criterion uses vague terms ("good", "clean", "clear", "appropriate", "well-structured") without behavioral definitions; scope matches unrelated directory trees.

**Repair — broad scope:**
- Replace `**/*.ext` with `<directory>/**/*.ext` where `<directory>` is the specific architectural layer from the Intent section
- Example: `**/*.py` → `src/api/**/*.py` if the Intent references API handler files
- Start narrow: if uncertain which directory, pick the one where the known failure occurred

**Repair — vague criterion terms:**
- Replace each vague term with an observable behavioral definition
- Example: instead of "well-structured Intent section," write "Intent section contains all five components: violation, failure cost, principle, exception policy, fix-safety signal"
- Test: would two developers independently make the same pass/fail decision after reading the revised criterion?

**Do not repair by removing scope** — if the scope is wrong, narrow it to the correct layer; don't delete it.

## Dimension 2: Staleness Failures

**Signal:** Scope glob references a directory that does not exist; examples reference functions, imports, or modules not found in the codebase; Intent references a dependency or framework not in the project manifest.

**Decision tree (in preference order):**

1. **Update examples** — if the convention still applies but the referenced code has changed: replace examples with current code, update file path comments to current paths, re-verify behavioral equivalence
2. **Archive** — if the convention still conceptually applies but the specific implementation it targets no longer exists: add `status: archived` to frontmatter, note the archival reason; do not delete (historical record)
3. **Delete** — if the convention itself no longer applies (the architectural pattern was retired, the framework was replaced): remove the rule file entirely; add a note to the commit message documenting why

The key distinction: update when the pattern is still being enforced; archive when the specific code is gone but the principle may return; delete when the convention is definitively retired.

## Dimension 3: Rubric Instability Failures

**Signal:** Non-compliant or compliant examples are synthetic (generic identifiers, no file path comment); examples are trivially minimal; Intent section uses hedging language ("might," "usually," "could," "generally"); no "when evidence is borderline" declaration.

**Repair — synthetic examples:**
- Replace with examples from actual codebase code, following the example construction methodology
- Add file path comment (`// path/to/actual-file.ext`)
- Use domain-specific identifiers, not `foo`/`bar`

**Repair — hedging language:**
- Replace hedging with categorical language: "usually should" → "must"; "might cause" → "causes"
- Exception: if "usually" was load-bearing (acknowledging intentional exceptions), do not remove it — instead, move the exception to the exception policy in the Intent section and replace "usually" with categorical language in the criterion

**Repair — missing borderline declaration:**
- Add to the Intent section: "When evidence is borderline, prefer WARN over PASS."
- This is the default-closed stance that prevents silent pass-through on ambiguous cases

## Dimension 4: Fix-Safety Failures

**Signal:** Missing `fix-safety` field in frontmatter; value is not `auto-remediable` or `requires-review`.

**Repair:** This is a mechanical fix with no intent-preservation risk.
- Add `fix-safety: requires-review` to frontmatter (default to requires-review when uncertain)
- Downgrade to `auto-remediable` only when the fix preserves all observable behavior (formatting, import ordering, pure renames with no semantic change)

## Dimension 5: Research Grounding Failures

**Signal:** Non-compliant example appears after the compliant example; no default-closed stance; criterion combines multiple evaluation dimensions; hedging language without exception clarification.

**Repair — wrong example order:**
- Swap the Non-Compliant and Compliant Example sections
- Non-compliant must appear first (sets the rejection case before the acceptance case)

**Repair — missing default-closed stance:**
- Add to the Intent section or at the end of the Non-Compliant Example section: "When evidence is borderline, surface as WARN rather than PASS."

**Repair — multiple dimensions in one criterion:**
- Split the rule: one rule per criterion
- If the description contains "and," it likely encodes two rules
- Determine which criterion is primary; create a second rule for the other

## Conflict Failures

**Signal:** Following one rule's compliant example causes another rule to FAIL on the same file.

**Resolution strategies (in preference order):**

1. **Narrow scope** — if one rule was over-broad, narrow its scope glob so the two rules no longer apply to the same files
2. **Merge** — if two rules enforce complementary aspects of the same convention, merge them into one rule with both criteria
3. **Explicit exception** — add an exception policy to one rule acknowledging the other: "Exception: in files covered by [other-rule], [behavior] is acceptable"
4. **Deprecate one** — if one rule supersedes the other, archive the older rule and note the replacement in its frontmatter

## Takeaway

Every repair has a failure mode — repairs that pass the audit by changing what the rule enforces are worse than the original. State the original intent first, verify the proposed repair preserves it, and flag scope or example changes as requiring human review before applying. The decision tree for staleness (update → archive → delete) applies in priority order; do not delete unless the convention is definitively retired.
