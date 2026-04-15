# Retrospective Format

Format for the optional `## Retrospective` section appended to plan files
after work is integrated.

## When to Offer

Offer a retrospective only when a plan file was found during the
finish-work workflow. Do not offer for ad-hoc branches without plans.

## Where to Insert

Append the `## Retrospective` section at the end of the plan file, after
the **Validation** section. It is the final section in the document.

## Section Structure

The retrospective has 3 subsections:

### Completed

What was actually delivered. Reference task checkboxes and commit SHAs
from the plan. Keep it factual — this is a record, not a narrative.

### Deviations

Where the implementation diverged from the original plan. Include:
- Tasks added or removed during execution
- Scope changes and why they happened
- Approach changes from the original design

If there were no deviations, state: "None — plan executed as written."

### Lessons

What would be done differently next time. Focus on actionable insights:
- What assumptions were wrong
- What was harder or easier than expected
- What tooling or process changes would help

## Example

```markdown
## Retrospective

### Completed

5/5 tasks completed. Added URL validation for research documents,
content length checks for context files, and index sync verification.

### Deviations

- Added Task 3b (content length upper bound) after discovering context
  files exceeding 1000 words during testing. Not in original plan.
- Dropped configurable thresholds from Task 4 — YAGNI, hardcoded
  defaults were sufficient.

### Lessons

- Testing validators against real project files caught edge cases that
  synthetic test fixtures missed. Use real files in future validator work.
- The index sync check was simpler than expected — `generate_index()`
  already returned enough state to diff against disk.
```
