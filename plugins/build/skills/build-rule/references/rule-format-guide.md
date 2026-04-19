---
name: Rule Format Guide (build-rule)
description: Canonical Claude Code rule format under `.claude/rules/` — file location, optional `paths:` frontmatter, body conventions, and an optional structured-Intent template for semantic-enforcement rules.
---

# Rule Format Guide

Rules are markdown files Claude Code reads automatically:
- **Project rules:** `.claude/rules/*.md` (and recursive subdirectories)
- **User-level rules:** `~/.claude/rules/*.md`

Rules without `paths:` frontmatter load at session start with the same
priority as `.claude/CLAUDE.md`. Rules with `paths:` load on demand
when Claude reads files matching one of the globs.

Source: [Anthropic — Organize rules with `.claude/rules/`](https://code.claude.com/docs/en/memory#organize-rules-with-claude/rules/).

## Table of Contents

- [File Location and Naming](#file-location-and-naming)
- [Frontmatter](#frontmatter)
- [Body Conventions](#body-conventions)
- [Optional: Structured Intent for Semantic-Enforcement Rules](#optional-structured-intent-for-semantic-enforcement-rules)

---

## File Location and Naming

| Location | Scope |
|----------|-------|
| `.claude/rules/<name>.md` | Project rule, shared via version control |
| `.claude/rules/<subdir>/<name>.md` | Project rule, organized by topic group |
| `~/.claude/rules/<name>.md` | Personal rules, all projects on this machine |

Filenames should be descriptive: `testing.md`, `api-design.md`,
`security.md`, `code-style.md`. Subdirectories are discovered
recursively, so `frontend/components.md` and `backend/handlers.md` work
for grouped organization.

---

## Frontmatter

Frontmatter is **optional**. The only documented field is `paths:`.

### No frontmatter — always-on rule

```markdown
# Project Naming Conventions

- Branch names use `feature/`, `fix/`, or `refactor/` prefixes
- Migration files are timestamped: `YYYYMMDD_<slug>.sql`
- Test files mirror the source path with `.test.ts` suffix
```

The rule loads at session start and applies everywhere.

### `paths:` — path-scoped rule

```markdown
---
paths:
  - "src/api/**/*.ts"
---

# API Development Rules

- All API endpoints must include input validation
- Use the standard error response format
- Include OpenAPI documentation comments
```

The rule only loads when Claude reads a file matching one of the globs.

### Multiple patterns and brace expansion

```yaml
---
paths:
  - "src/**/*.{ts,tsx}"
  - "lib/**/*.ts"
  - "tests/**/*.test.ts"
---
```

### Glob reference

| Pattern | Matches |
|---------|---------|
| `**/*.ts` | All TypeScript files in any directory |
| `src/**/*` | All files under `src/` |
| `*.md` | Markdown files in the project root |
| `src/components/*.tsx` | React components in a specific directory |

---

## Body Conventions

There is no required body structure. Anthropic shows simple bullet
lists in their canonical example. Apply the same guidance Anthropic
gives for CLAUDE.md and rules:

- **Specific over vague.** "Use 2-space indentation" beats "Format code
  properly".
- **Concrete commands beat hand-waving.** "Run `npm test` before
  committing" beats "Test your changes".
- **Headers and bullets group related instructions** — Claude scans
  structure the way readers do.
- **Target under 200 lines per rule.** Larger rules consume context
  and reduce adherence; split into multiple topic files instead.
- **One topic per file.** A rule that covers two unrelated
  conventions is two rules — split them.

---

## Toolkit Recommendation: Structured Intent for Enforcement Rules

This section is **toolkit opinion**, layered on top of Anthropic's
canonical spec. It does not add frontmatter fields, change file
location, or require any heading Anthropic doesn't allow. It opts the
rule into a body shape that helps the LLM evaluator stay consistent
when the rule asks Claude to *judge* a file's compliance.

### When to use this pattern

Use the structured Intent shape when the rule is an **enforcement
rule** — Claude reads the file, applies the rule, and produces a
PASS/FAIL verdict. Skip it for:

- Procedural rules ("run X before Y") — bullet list is enough
- Style rules ("use 2-space indentation") — single line is enough
- Reference rules ("API handlers live in `src/api/handlers/`") — Anthropic's
  example pattern handles them cleanly

### Body shape

````markdown
---
paths:
  - "models/staging/**/*.sql"
---

# <Rule Name>

## Why

<VIOLATION — what pattern does this rule catch?>
<FAILURE COST — what specifically goes wrong, and who bears it?>
<PRINCIPLE — what underlying value does this enforce?>
Exception: <name at least one legitimate bypass case>.

When evidence is borderline, prefer WARN over PASS.

## Compliant

```<lang>
// real code from the codebase, with file path comment
```

## Non-compliant

```<lang>
// real code that violates the rule
```
````

### Why each piece earns its place

| Piece | Why it helps |
|-------|--------------|
| **`## Why` lead-in** | Names the rule's purpose so a reader (human or Claude) understands the *why*, not just the *what*. Anthropic's specificity guidance applies — the Why section should be concrete, not "this rule keeps things clean". |
| **Failure cost** (load-bearing) | Without it, developers weigh the rule as bureaucratic overhead. Naming what breaks and who bears the cost drives adherence over disable behavior. |
| **Exception policy** (load-bearing) | Rules that admit no exception get disabled wholesale when the legitimate edge case appears. Naming one case keeps the rule alive. |
| **Principle** | Anchors the rule to a value (type safety, security, maintainability). When the rule's specifics don't quite fit a new situation, the principle still guides. |
| **`## Compliant` and `## Non-compliant` examples** | Anchor the evaluation to concrete cases. Research-grounded: evidence-anchored rubrics deliver +0.17 QWK over inference-only (per `.research/rule-best-practices.md`). |
| **Real code with file path comments** | Synthetic `foo`/`bar` examples produce weaker anchors than domain-specific identifiers from the actual codebase. |
| **Default-closed declaration** | Without it, evaluators silently default to PASS on ambiguous cases. The line keeps borderline cases visible. |

### How check-rule audits the structured shape

When `check-rule` detects a rule that opts into this shape (presence
of `## Compliant` AND `## Non-compliant` sections, OR a `## Why`
section), it audits the additional toolkit-opinion dimensions —
Intent completeness, example pair quality, default-closed declaration.
Rules that don't use the structured shape skip those dimensions
entirely. Trigger-gated, mirroring `check-skill`'s pattern.

---

## Conflict Detection

Anthropic explicitly warns:

> "if two rules contradict each other, Claude may pick one arbitrarily"

Before adding a rule, scan existing `.claude/rules/` files (and
`~/.claude/rules/` for the user) for:
- Overlapping `paths:` globs covering the same convention
- Always-on rules that contradict the new rule's directives
- Subtle tension (e.g., one says "prefer composition", another says
  "use inheritance for X")

Resolve by narrowing scope, merging, adding an explicit boundary
("Exception: in files covered by [other-rule], …"), or deprecating
one rule.
