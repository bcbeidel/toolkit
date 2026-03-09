# Extraction Heuristics

How to identify implicit principles in project artifacts and classify
them as principles, rules, or preferences.

## Scan Sources (in order)

1. **CLAUDE.md** — sections labeled "principles", "philosophy", "values",
   or numbered guideline lists
2. **AGENTS.md** — convention statements beyond operational instructions
3. **ADRs / docs/plans/** — recurring rationale patterns ("we chose X
   because Y" repeated across documents)
4. **Recent commits (~50)** — patterns like "prefer X over Y",
   "always/never do Z" in commit messages
5. **Code patterns** — repeated structural conventions in key files
   (e.g., every module uses composition, all errors use stdlib exceptions)

## Signal Patterns

| Signal | Likely Classification | Example |
|--------|----------------------|---------|
| "Prefer X over Y" | Principle | "Prefer composition over inheritance" |
| "Always/never do X" | Rule | "Never use default exports" |
| "We use X" / "Use X" | Rule or preference | "Use ruff for linting" |
| Repeated rationale across commits/PRs | Principle candidate | 5 PRs cite "keeping it simple" |
| Numbered philosophy/values list | Principles | CLAUDE.md "Design Principles" section |
| Glob/file-specific instruction | Rule | "*.test.ts files use vitest" |
| Style/formatting guidance | Preference | "Use single quotes" |

## Classification

For each candidate, apply the five-criteria filter from the principle
structure reference. Show reasoning for each classification:

- **Principle** (3+ criteria met) — outcome-focused, guides judgment
  under ambiguity, stable across tech changes
- **Rule** (0-2 criteria met, procedural) — prescribes a specific action,
  may be tech-specific
- **Preference** (0-2 criteria met, stylistic) — not architectural,
  affects presentation not behavior

## Confidence Levels

Convergence across multiple sources is a confidence signal:

| Sources | Confidence |
|---------|-----------|
| CLAUDE.md + commits + code patterns | HIGH |
| Two sources converge (e.g., CLAUDE.md + commits) | MODERATE |
| Single source only (e.g., one commit message) | LOW |

## Presentation Format

Present extraction results as a table for user review:

```
| # | Candidate | Source | Classification | Confidence |
|---|-----------|--------|----------------|------------|
| 1 | Convention over configuration | CLAUDE.md:L32 | principle | HIGH |
| 2 | Use ValueError + stdlib only | CLAUDE.md:L78 | rule | HIGH |
| 3 | Prefer composition over inheritance | 12 commits | principle | MODERATE |
```

User approves, rejects, or reclassifies each row. Only approved
principles proceed to articulation.

Rules and preferences are noted but stay where they are — do not move
them to PRINCIPLES.md.
