---
name: build-rule
description: Create a Claude Code rule under `.claude/rules/` — a markdown instruction file with optional `paths:` frontmatter for path-scoping. Use when the user wants to "create a rule", "build a rule", "add a rule", "capture this convention", or "enforce this pattern".
argument-hint: A topic name or description of the convention to capture
user-invocable: true
references:
  - ../../_shared/references/rules-best-practices.md
  - ../../_shared/references/primitive-routing.md
---

# /build:build-rule

Create a Claude Code rule. Rules are markdown files in `.claude/rules/`
that Claude reads automatically — globally at session start (no frontmatter)
or on demand when a matching file is opened (with `paths:` frontmatter).
See [Anthropic's `.claude/rules/` reference](https://code.claude.com/docs/en/memory#organize-rules-with-claude/rules/).

Authoring principles — what makes a rule load-bearing, the anatomy
template, patterns that work — live in
[rules-best-practices.md](../../_shared/references/rules-best-practices.md).
This skill is the workflow; the principles doc is the rubric.

## Workflow

### 0. Verify Primitive

Before proceeding, confirm a rule is the right mechanism. Full decision matrix: [primitive-routing.md](../../_shared/references/primitive-routing.md).

A rule is right when:
- The instruction should always (or path-conditionally) shape Claude's
  behavior in a project — not fire as a one-off workflow
- It belongs in version control, shared with the team
- It's small enough to live as one topic file (~under 200 lines)

Redirect when:
- Procedural multi-step workflow Claude should execute on demand → `/build:build-skill`
- Lifecycle-event enforcement (pre-commit, pre-tool-use) → `/build:build-hook`
- A check is shell-expressible (grep, file existence, regex) → recommend a hook or linter
- Always-loaded global standards → consider `.claude/CLAUDE.md` instead — rules
  are right when the topic justifies its own file

### 1. Intake — One Rule or Many

Read `$ARGUMENTS` and decide: does the input describe one convention or
several?

**Signals that the input is multi-concern:**
- Multiple "and" clauses naming distinct conventions ("API endpoints
  need validation **and** tests must mirror source paths")
- Comma-separated list of unrelated rules
- Bullet list with topics that wouldn't naturally co-evolve (e.g.,
  API conventions + test naming + deploy process)

**If single-concern:** proceed to Step 2 with one rule in scope.

**If multi-concern:** propose a split. Present the candidate rule list
(one line per rule, with a proposed filename) and ask the user to
confirm, merge, or re-split. On approval, subsequent steps iterate
per rule.

Example fork:
> "I see three conventions here. Proposed split:
> 1. `api-validation.md` — API endpoints must validate input
> 2. `test-path-mirroring.md` — test files mirror source paths with `.test.ts` suffix
> 3. `commit-messages.md` — commit messages follow Conventional Commits
>
> Accept, merge any, or re-split?"

This enforces *one claim per file* (from rules-best-practices.md)
at intake rather than after drafting.

### 2. Pick a Topic Name (per rule)

Each rule becomes `<topic>.md` under `.claude/rules/`. Use a descriptive,
single-word or hyphenated name like `testing.md`, `api-design.md`,
`security.md`, `code-style.md`. Subdirectories are allowed (e.g.,
`.claude/rules/frontend/components.md`).

If the intake didn't settle filenames, propose 2–3 candidates per rule
and let the user pick.

### 3. Decide Scope (per rule)

Two choices:

| Scope | Frontmatter | When to use |
|-------|-------------|-------------|
| **Always-on** | none | Project-wide standards (e.g., naming conventions, commit message format) |
| **Path-scoped** | `paths:` glob list | Rules that only apply when Claude works with specific files (e.g., backend rules in a monorepo) |

Path-scope example:
```yaml
---
paths:
  - "src/api/**/*.ts"
---
```

Globs follow standard syntax; brace expansion works
(`"src/**/*.{ts,tsx}"`). Multiple patterns live under one `paths:` key.

Prefer narrow, directory-rooted patterns. An unscoped rule is a context
tax on every unrelated task — justify `paths:` omission explicitly.

### 4. Check for Conflicts (per rule)

Read existing rules in `.claude/rules/` (and `~/.claude/rules/` if the
user maintains personal rules). Anthropic warns explicitly:

> "if two rules contradict each other, Claude may pick one arbitrarily"

Check for:
- Rules with overlapping `paths:` globs (or both global) covering the
  same convention
- Instructions that pull in opposite directions for the same scenario
- When drafting multiple sibling rules in one invocation, check the
  siblings against each other too

If overlap found, ask: "This overlaps with `[existing rule]`. Merge,
replace, or keep both with explicit boundaries?"

### 5. Draft (per rule)

Follow the anatomy template from
[rules-best-practices.md](../../_shared/references/rules-best-practices.md):

```markdown
---
paths:
  - "path/glob/**/*.ext"
---

<One-line imperative rule statement, framed as an action to take.>

**Why:** <the reason — incident, constraint, strong preference>
**How to apply:** <when/where this kicks in, including edge cases>

<Optional: one concrete example. When the rule requires judgment and
the boundary is non-obvious, show a contrasting non-compliant example.>
```

Apply the principles without restating them here — the rubric is the
principles doc. Key things to get right:

- **Frame in the positive** — state what to do, not what to avoid
- **Direct, definite voice** — "Use X." not "We prefer X."
- **Specific enough to be falsifiable** — a reviewer can cite a violation
- **Include the *why*** — for judgment-based rules, name failure cost + exception
- **Domain-specific examples** — real code from the codebase, not `foo`/`bar`

For judgment-heavy rules (Claude evaluates a file against the rule),
the why becomes longer and an example pair makes the boundary visible.
For simple directive rules ("use snake_case"), a one-line rule +
inline Why is enough.

### 6. Present for Approval (per rule)

Before writing, narrate the design choices in 2–4 bullets per rule:

- **Filename + location** — `.claude/rules/<name>.md`
- **Scope** — always-on or path-scoped (and which globs)
- **Length and structure** — rough line count, whether it uses an example
- **What was skipped and why** — patterns considered but rejected

Show the complete file. Iterate on feedback. Hold the write until the
user approves.

When multiple rules are in flight, present each rule's draft and gate
separately. Do not batch approvals.

### 7. Write

- Create `.claude/rules/` (and any subdirectory) if it doesn't exist
- Write each approved rule to `.claude/rules/<name>.md`
- Report each file path

Claude Code picks up the new rules on the next session (always-on rules)
or the next time it reads a file matching `paths:` (scoped rules).

## Example

<example>
User: "I want a rule that staging dbt models only do casts, renames, and deduplication"

Single-concern intake — one rule. Filename `staging-model-purity.md`.
Path-scoped to `models/staging/**/*.sql`. Judgment-based — boundary
between "pure" and "has business logic" benefits from a contrasting
example pair.

Drafts:

```markdown
---
paths:
  - "models/staging/**/*.sql"
---

Keep staging models to casts, renames, and deduplication only.

**Why:** Business logic in staging (revenue calculations, tier
classifications) couples source schema changes to business definitions.
When either changes, both layers need coordinated updates, which
produces silent divergence between the staging contract and downstream
assumptions.

**Exception:** pure data-type normalization (parsing a date string to
a date type) is permitted.

## Compliant

```sql
-- models/staging/stg_orders.sql
select
  id as order_id,
  cast(order_date as date) as order_date,
  cast(quantity as integer) as quantity
from {{ source('raw', 'orders') }}
qualify row_number() over (partition by id order by _loaded_at desc) = 1
```

## Non-compliant

```sql
-- models/staging/stg_orders.sql
-- revenue calculation and tier classification are business logic
select id, quantity * unit_price as revenue,
  case when lifetime_value > 1000 then 'high' else 'standard' end as tier
from {{ source('raw', 'orders') }}
```
```

Narrates design (path-scoped, ~30 lines, example pair because the
boundary is subtle). On approval, writes to
`.claude/rules/staging-model-purity.md`.
</example>

## Key Instructions

- Run the Step 0 primitive check before drafting — if the ask fits a hook or linter better, redirect and stop
- At Step 1, detect multi-concern input and propose a split before any drafting — one claim per file is a principle; enforce it at intake
- Run the Step 4 conflict check before drafting — Anthropic warns that contradicting rules cause Claude to pick one arbitrarily
- Draft against the anatomy template and principles from [rules-best-practices.md](../../_shared/references/rules-best-practices.md); don't invent new frontmatter fields or required sections
- Hold each write until the user approves that rule's draft (Step 6 gate) — gate per rule, not per batch
- Keep rules short; split when they approach the audit's 200-line warn threshold (check-rule fails at 500)

## Anti-Pattern Guards

1. **Rule outside `.claude/rules/`** — Claude Code only auto-loads rules from `.claude/rules/` (and `~/.claude/rules/`); files elsewhere are inert. Refuse to write to `docs/rules/` or other invented paths.
2. **Multi-concern rule written as one file** — if Step 1 missed a split opportunity and the draft covers multiple topics, fork back to Step 1 and re-split before writing.
3. **Vague directive** ("be clean", "format properly") — restate in concrete, verifiable terms before accepting. Principle: Specific enough to be falsifiable.
4. **Convention enforceable by a traditional linter** (syntax, formatting, import ordering) — redirect to the linter and stop. Principle: Reserve rules for judgment.
5. **Conflict check skipped** — run Step 4 before drafting; contradicting rules produce arbitrary behavior.
6. **Always-on rule that should be path-scoped** — flag rules whose content names a specific directory or file type but that omit `paths:`; the unscoped rule consumes context every session for content that only applies sometimes.
7. **Negative-only framing** — rule states only what to avoid without naming the positive action. Negations are fragile in English; a dropped `not` inverts the rule. Principle: Frame in the positive.

## Handoff

**Receives:** Topic name or description of one or more conventions to capture
**Produces:** One or more rule files under `.claude/rules/` (or subdirectories)
**Chainable to:** check-rule (verify new rules fit the existing library without conflicts)
