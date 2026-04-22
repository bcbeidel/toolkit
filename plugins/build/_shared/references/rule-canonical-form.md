---
name: Rule Canonical Form
description: Canonical Anthropic-spec for Claude Code rule files under `.claude/rules/` — file location, naming, optional `paths:` frontmatter with glob syntax, and documented body conventions. Spec-only; no toolkit opinion.
---

# Rule Canonical Form

Rules are markdown files Claude Code reads automatically:
- **Project rules:** `.claude/rules/*.md` (and recursive subdirectories)
- **User-level rules:** `~/.claude/rules/*.md`

Rules without `paths:` frontmatter load at session start with the same
priority as `.claude/CLAUDE.md`. Rules with `paths:` load on demand when
Claude reads files matching one of the globs.

Source: [Anthropic — Organize rules with `.claude/rules/`](https://code.claude.com/docs/en/memory#organize-rules-with-claude/rules/).

This document is pure Anthropic-spec — location, naming, frontmatter, and
body conventions only. Toolkit opinion (the structured-Intent body shape
for enforcement rules) lives in
[rule-structured-intent.md](rule-structured-intent.md).

## Table of Contents

- [File Location and Naming](#file-location-and-naming)
- [Frontmatter](#frontmatter)
- [Body Conventions](#body-conventions)
- [Glob Reference](#glob-reference)

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

Files at other paths (e.g., `docs/rules/`, project root) are not loaded
by Claude Code as rules.

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

Multiple patterns are listed under the single `paths:` key. Brace
expansion (`{ts,tsx}`) is supported within a pattern.

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

## Glob Reference

| Pattern | Matches |
|---------|---------|
| `**/*.ts` | All TypeScript files in any directory |
| `src/**/*` | All files under `src/` |
| `*.md` | Markdown files in the project root |
| `src/components/*.tsx` | React components in a specific directory |
