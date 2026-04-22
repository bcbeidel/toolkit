---
name: Rule Repair Playbook (check-rule)
description: Per-failure-mode repair strategies for check-rule findings against `.claude/rules/` files — canonical fixes for Tier-1 deterministic findings, Tier-2 semantic dimensions, and Tier-3 conflicts.
---

# Rule Repair Playbook

Every check-rule finding maps to a canonical repair. Before applying
any repair, state the original intent explicitly: **"This rule
guides Claude to [original directive]."** Verify the proposed repair
preserves that guidance. If the repair would change what Claude is
told to do (not just how the directive is phrased), flag it as
requiring human review before applying.

## Table of Contents

- [Tier 1: Deterministic Format Repairs](#tier-1-deterministic-format-repairs)
- [Tier 2: Semantic Dimensions](#tier-2-semantic-dimensions)
  - [Dimension 1: Framing](#dimension-1-framing)
  - [Dimension 2: Specificity](#dimension-2-specificity)
  - [Dimension 3: Single Concern](#dimension-3-single-concern)
  - [Dimension 4: Why Adequacy](#dimension-4-why-adequacy)
  - [Dimension 5: Scope Tightness](#dimension-5-scope-tightness)
  - [Dimension 6: Staleness](#dimension-6-staleness)
  - [Dimension 7: Judgment-Not-Linter](#dimension-7-judgment-not-linter)
  - [Dimension 8: Example Realism](#dimension-8-example-realism)
- [Tier 3: Conflicts](#tier-3-conflicts)

---

## Tier 1: Deterministic Format Repairs

### Wrong Location

**Signal:** Rule file lives outside `.claude/rules/` (e.g., `docs/rules/`, project root, `rules/` without `.claude/` prefix)

**CHANGE:** Move the file under `.claude/rules/`
**FROM:** `docs/rules/api-handlers.md`
**TO:** `.claude/rules/api-handlers.md`
**REASON:** Claude Code only auto-loads rules from `.claude/rules/` (and `~/.claude/rules/` for user rules). Files at other paths are inert — Claude never reads them as rules.

### Wrong Extension

**Signal:** Rule file uses `.rule.md`, `.mdx`, `.markdown`, or another non-`.md` extension

**CHANGE:** Rename to `.md`
**FROM:** `.claude/rules/api-handlers.rule.md`
**TO:** `.claude/rules/api-handlers.md`
**REASON:** Claude Code's rule discovery scans for `.md` files only. Other extensions are skipped.

### Malformed `paths:` Glob

**Signal:** `paths:` is present but a glob has unmatched brackets, invalid wildcards, or empty pattern

**CHANGE:** Repair the glob syntax
**FROM:** `paths: "src/api/**/*.{ts"` (unclosed brace)
**TO:** `paths: "src/api/**/*.{ts,tsx}"`
**REASON:** Malformed globs silently fail to match — the rule is in the file but Claude never loads it for any real file path.

### File Too Large (WARN at 200)

**Signal:** File exceeds 200 non-blank lines but is under 500

**CHANGE:** Split into topic-specific files
**FROM:** `.claude/rules/conventions.md` (350 lines covering API + tests + deploy)
**TO:** `.claude/rules/api-conventions.md` + `.claude/rules/test-conventions.md` + `.claude/rules/deploy-conventions.md`
**REASON:** Larger rules consume context and reduce adherence. Splitting also improves the on-demand load path for path-scoped rules.

### File Too Large (FAIL at 500)

**Signal:** File exceeds 500 non-blank lines

**CHANGE:** Split into rules + move long-form explanation elsewhere
**FROM:** `.claude/rules/architecture.md` (650 lines — mixes rule text with extended rationale and design history)
**TO:** `.claude/rules/architecture-layering.md` + `.claude/rules/service-boundaries.md` (rules); move the long-form rationale to `.context/architecture-rationale.md` or a CLAUDE.md section
**REASON:** At 500+ lines the file is a document, not a rule. Rules should be scannable at the point of application; documents belong in `.context/` or CLAUDE.md where they carry different expectations.

### Unknown Frontmatter Key

**Signal:** Frontmatter contains top-level keys other than `paths:`

**CHANGE:** Remove the unknown key, or move its content into the body
**FROM:**
```yaml
---
paths:
  - "src/api/**/*.ts"
severity: warn
description: API conventions
---
```
**TO:**
```yaml
---
paths:
  - "src/api/**/*.ts"
---

# API Conventions
```
**REASON:** Claude Code documents only `paths:` in rule frontmatter. Other keys (`severity:`, `description:`, `name:`, `type:`) are not consumed and add maintenance noise without behavioral effect.

---

## Tier 2: Semantic Dimensions

### Dimension 1: Framing

#### Prohibition-Only Directive

**Signal:** Rule statement is only a prohibition ("Don't X", "Never Y", "Avoid Z") with no positive counterpart

**CHANGE:** Restate as a positive action, or pair the prohibition with its positive alternative
**FROM:** "Don't use global state."
**TO:** "Thread dependencies through constructors." (positive)
*or* "Thread dependencies through constructors; never reach for module-level globals." (pair)
**REASON:** Negations are fragile in English — a dropped or misattributed `not`/`don't`/`never` inverts the rule. Positive framings also name the target action; pure prohibitions leave the target implicit.

#### Stacked Negations

**Signal:** Rule contains multiple negations in a single sentence ("Don't not return …", "Never avoid doing X unless Y")

**CHANGE:** Rewrite with at most one negation, or reframe positively
**FROM:** "Don't forget to not return null from these handlers."
**TO:** "Return an empty result object, not null, from these handlers."
**REASON:** Double negatives compound the fragility — each negation is another token that can be lost or misattributed.

#### Hedged Prohibition

**Signal:** Prohibition uses hedging language ("Try not to …", "Avoid when possible", "Generally don't …")

**CHANGE:** Commit to the rule (positive framing) or remove it
**FROM:** "Try not to use `any` type annotations."
**TO:** "Annotate function parameters and return types with specific types. Exception: third-party APIs without type definitions may use `any` at the boundary."
**REASON:** A hedged prohibition doesn't tell Claude what to do and doesn't commit to what to avoid — it produces inconsistent adherence in both directions.

---

### Dimension 2: Specificity

#### Anchor-Free Directive

**Signal:** Directive uses anchor-free terms ("good", "clean", "clear", "appropriate", "well-structured", "properly", "nice", "consistent") without a verifiable definition

**CHANGE:** Replace each anchor-free term with a verifiable directive
**FROM:** "Format code properly and keep files organized."
**TO:** "Use 2-space indentation; run `prettier --check` before committing. API handlers live in `src/api/handlers/`."
**REASON:** Anchor-free directives produce uneven adherence — two readers (or two Claude sessions) interpret them differently.

#### Reader-Defers Directive

**Signal:** Directive defers the decision back to the reader without a fallback rule ("use your judgment", "as appropriate", "where it makes sense")

**CHANGE:** Either remove the deferred directive (it carries no information) or add the fallback rule
**FROM:** "Use TypeScript strict mode where it makes sense."
**TO:** "Use TypeScript strict mode in all files under `src/`. Exception: generated code in `src/codegen/`."
**REASON:** A directive that doesn't tell Claude what to do isn't a rule. Either commit or remove.

#### Hedged Phrasing

**Signal:** Rule uses "prefer", "generally", "usually", "consider" as its primary directive

**CHANGE:** Commit to the directive; move the hedge into a named exception if one exists
**FROM:** "Generally prefer composition over inheritance."
**TO:** "Use composition over inheritance. Exception: when extending a framework base class that requires inheritance (e.g., `React.Component` in legacy code)."
**REASON:** Hedged rules push judgment back onto Claude at every invocation, defeating the point of writing the rule down.

---

### Dimension 3: Single Concern

#### Multiple Topics in One File

**Signal:** Multiple top-level `##` sections cover distinct topics that wouldn't naturally co-evolve

**CHANGE:** Split into separate topic files
**FROM:** `.claude/rules/conventions.md` with sections "API design", "Test naming", "Deployment process"
**TO:** `.claude/rules/api-design.md` + `.claude/rules/test-naming.md` + `.claude/rules/deployment.md`
**REASON:** One claim per file. Each rule should answer one question — "how do we do X?" Mixing topics makes path-scoping impossible (each topic might apply to different files) and grows the file beyond the size guidance.

#### Body Doesn't Match Filename

**Signal:** Filename describes one topic but body covers another in addition

**CHANGE:** Move the off-topic content to a file matching its actual topic
**FROM:** `api-design.md` containing API conventions AND a section on commit message format
**TO:** `api-design.md` (API only) + `commit-messages.md` (or move into `.claude/CLAUDE.md` if it's a project-wide standard)
**REASON:** Filename is the discovery handle. Future maintainers grep for `commit-messages.md` when looking for commit conventions; they don't expect to find them inside `api-design.md`.

#### `paths:` Union Covers Distinct Topics

**Signal:** `paths:` is a union of unrelated patterns where each `##` section applies to only one of them

**CHANGE:** Split the rule so each file's `paths:` covers only the directives in that file
**FROM:**
```yaml
---
paths:
  - "src/api/**/*.ts"
  - "tests/**/*.test.ts"
---
```
with separate API-section and test-section bodies
**TO:** Two files, one with `paths: "src/api/**/*.ts"` and one with `paths: "tests/**/*.test.ts"`
**REASON:** Path-scoping wastes effort if Claude loads the API section when reading test files (and vice versa). Splitting halves the loaded context and tightens the rule's relevance.

---

### Dimension 4: Why Adequacy

#### Missing Why Entirely

**Signal:** Rule has no reasoning — no `**Why:**` line, no `## Why` section, no rationale in prose

**CHANGE:** Add a brief why. For simple directives a single inline line suffices; for judgment-based rules, include failure cost and an exception.
**FROM:** "Use snake_case for Postgres table names."
**TO:** "Use snake_case for Postgres table names. **Why:** case-sensitive identifiers in Postgres require quoting; snake_case avoids the quoting trap across ORMs."
**REASON:** Reasoning lets Claude extend the rule to edge cases and lets maintainers decide whether the rule is still load-bearing.

#### Missing Failure Cost (judgment-based rule)

**Signal:** Judgment-based rule's why names the violation only ("Avoid `console.log`") with no description of what breaks or who bears the cost

**CHANGE:** Add a sentence naming the specific consequence and who bears it
**FROM:** "Avoid using `console.log` in production code. It creates noise."
**TO:** "`console.log` in production builds exposes internal state to end users via browser developer tools and adds measurable latency in high-frequency call paths."
**REASON:** Without failure cost, developers weigh the rule as bureaucratic overhead rather than a real risk. Rules without failure cost have higher disable rates.

#### Missing Exception Policy (judgment-based rule)

**Signal:** Judgment-based rule's why has no `Exception:` line naming a legitimate bypass case

**CHANGE:** Append an `Exception:` line naming at least one legitimate case
**FROM:** Why section ends without exception language
**TO:** Append: `"Exception: <name at least one legitimate case — e.g., 'test files', 'scripts in tools/ that are never bundled for production'>."`
**REASON:** Rules with no named exception appear to admit no flexibility, causing developers to disable them entirely rather than follow them in the 95% case.

---

### Dimension 5: Scope Tightness

#### Unscoped Rule Names a Specific Directory

**Signal:** Rule has no `paths:` but its body begins "For React components…", "In API handlers…", or otherwise names a specific directory/file-type

**CHANGE:** Add `paths:` matching the content's actual reach
**FROM:**
```markdown
<no frontmatter>

# React Component Conventions

Use named exports for components...
```
**TO:**
```markdown
---
paths:
  - "src/components/**/*.tsx"
---

# React Component Conventions

Use named exports for components...
```
**REASON:** An unscoped rule is a context tax on every unrelated task. When the content names a specific scope, encoding that scope in `paths:` makes the rule load only where it applies.

#### `paths:` Glob Too Wide

**Signal:** `paths:` is broader than the content warrants (e.g., `paths: "**/*"` for a rule that only applies to `.ts` files)

**CHANGE:** Narrow the glob to match the content
**FROM:** `paths: "**/*"` for a TypeScript-only rule
**TO:** `paths: "**/*.{ts,tsx}"`
**REASON:** A too-wide glob makes the rule fire when it shouldn't, consuming context for irrelevant work.

---

### Dimension 6: Staleness

#### Reference to a Path That No Longer Exists

**Signal:** `paths:` glob, file-path comment in an example, or prose names a directory or file that is not in the current codebase

**CHANGE:** Update the reference to the current path, or delete the rule
**FROM:** `paths: "app/legacy/**/*.rb"` (directory removed in v3 refactor)
**TO:** `paths: "app/services/**/*.rb"` (replacement layer)
**REASON:** A rule that scopes itself to a non-existent directory never fires. Either the convention still applies under the new layout (update) or the convention is retired with the layer (delete).

#### Stale Command or Import in Examples

**Signal:** Example code uses an import path or command that has been replaced

**CHANGE:** Rewrite the example using current imports / commands
**FROM:** `import { Logger } from '@old-org/logging'` (package replaced 6 months ago)
**TO:** `import { Logger } from '@new-org/observability'`
**REASON:** Stale examples mislead Claude — they teach the wrong pattern. If no current pattern exists, the rule itself is likely stale and should be deleted.

---

### Dimension 7: Judgment-Not-Linter

#### Rule Restates a Formatter's Job

**Signal:** Rule enforces whitespace, indentation, quote style, or other formatting concerns handled by Prettier, Black, gofmt, etc.

**CHANGE:** Remove the rule; add the formatter to the project's tooling if not already present
**FROM:** "Use 2-space indentation. Use single quotes for strings. Trailing commas in multi-line lists."
**TO:** Delete the rule. Ensure `.prettierrc` (or equivalent) encodes these settings and runs in CI / pre-commit.
**REASON:** Formatters enforce mechanical rules deterministically. A rule file restating them dilutes the authority of rules that need judgment, and formatter violations get caught deterministically anyway.

#### Rule Restates a Linter's Job

**Signal:** Rule enforces import ordering, unused-import removal, or other concerns handled by ESLint, Ruff, etc.

**CHANGE:** Remove the rule; configure the linter
**FROM:** "Sort imports: stdlib, third-party, local. Remove unused imports before committing."
**TO:** Delete the rule. Configure `ruff` / `eslint` to enforce import ordering and unused-import detection.
**REASON:** Deterministic checks belong in tooling. Tooling catches violations at edit-time and CI-time; a rule only catches them when Claude happens to re-read the file.

#### Rule Restates a Type-Checker's Job

**Signal:** Rule enforces type annotations that `mypy`, `tsc`, or equivalent would catch

**CHANGE:** Remove the rule; tighten type-checker config
**FROM:** "All function parameters must have type annotations."
**TO:** Delete the rule. Enable `--strict` (TypeScript) or `--disallow-untyped-defs` (mypy) in the project's type-checker config.
**REASON:** Type-checker violations produce build failures. A rule cannot compete with that enforcement strength.

---

### Dimension 8: Example Realism

#### Synthetic Examples

**Signal:** Example code uses generic placeholders (`foo`, `bar`, `baz`, `myFunction`, `Thing`, `Widget`) as primary identifiers

**CHANGE:** Replace with real code from the codebase — actual table names, function names, module paths
**FROM:**
```typescript
function foo(x) { return bar(x); }
```
**TO:**
```typescript
// src/api/handlers/users.ts
async function getUser(userId: string) {
  return db.users.findById(userId);
}
```
**REASON:** Domain-specific identifiers anchor the rule more strongly than synthetic placeholders. The evaluator (human or Claude) recognizes the context and applies the rule the way they would to new code in the same codebase. File path comments (optional) strengthen provenance.

---

## Tier 3: Conflicts

**Signal:** Following one rule's directives as written would cause a developer to violate another rule

Resolution strategies in preference order:

1. **Narrow scope** — if one rule was over-broad (always-on when it should be path-scoped, or paths-glob too wide), narrow it so the two rules no longer co-fire on the same files. Verify the narrowed scope still covers the cases the rule was added for.

2. **Merge** — if two rules enforce complementary aspects of the same convention, merge into one rule with both directives stated together. Verify the merged file still passes the size and single-concern checks.

3. **Explicit boundary** — add an exception to one rule acknowledging the other: "Exception: in files covered by `[other-rule.md]`, [behavior] is acceptable." This preserves both rules without contradiction.

4. **Deprecate one** — if one rule supersedes the other: delete the older file. Claude Code doesn't define an `archived:` status for rules; deletion is the canonical retirement.

**Intent-preservation check for conflict resolution:** Confirm the resolution preserves the behavioral intent of both rules, not just one. A resolution that silently retires one rule's directive must be flagged for human review.
