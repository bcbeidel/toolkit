# Human Validation Patterns

Patterns for presenting non-automated validation criteria and collecting
user confirmation.

## Presentation Format

Show the full numbered list with automated results already filled in.
Each item gets a status before the user starts confirming:

```
Validation Results:
1. [PASS] `pytest tests/ -v` — 42 passed, 0 failed
2. [FAIL] `ruff check src/` — 3 errors found
3. [PENDING] All sub-questions answered with cited sources
4. [PENDING] Documentation covers new validation workflow
```

This gives the user full context — they can see which automated checks
passed or failed before judging qualitative criteria.

## Confirmation Modes

**Default: full list** — present all pending criteria at once. Ask the
user to confirm or reject each:

> "Please review the pending criteria above. For each, confirm whether
> it passes or fails. You can respond with the numbers that pass
> (e.g., '3 passes, 4 fails because...')."

**One-by-one mode** — if the user requests, present each criterion
individually with context from the plan's Goal section:

> "Criterion 3: 'All sub-questions answered with cited sources'
> (supports Goal: [goal summary]). Does this pass?"

Wait for confirmation before presenting the next criterion.

## Confirmation vs. Judgment

**Confirmation criteria** have binary, observable answers:
- "ADR includes Alternatives section with 2+ options" — look and count
- "README has installation instructions" — present or absent
- "API returns 200 on health endpoint" — check and report

**Judgment criteria** require qualitative assessment:
- "Documentation is clear and complete"
- "Error messages are user-friendly"
- "Code is well-organized"

For judgment criteria, ask the user to explain their assessment briefly.
This explanation becomes evidence in the structured output:

> "You confirmed criterion 4 passes. Brief reason? (This goes in the
> validation record.)"

## Mixed Validation

When a single criterion has both automated and human components:

1. Run the automated part first
2. If automated fails, mark the whole criterion as failed — skip the
   human part (no point judging coverage if tests don't pass)
3. If automated passes, present the human part for confirmation

Example: "`pytest` passes AND error messages are user-friendly"
- Run `pytest` first → if it fails, criterion fails
- If `pytest` passes → ask user about error message quality

## Escalation

If the user is unsure about a criterion, do not force pass/fail. Mark
it as **uncertain**:

```
3. [UNCERTAIN] All sub-questions answered with cited sources
   User note: "Most are answered but Q4 coverage is thin"
```

Uncertain items are flagged in the structured output for follow-up.
They do not block the validation from completing, but they prevent
the plan from being marked `completed`. Treat uncertain items as
soft failures — suggest tasks to address them.
