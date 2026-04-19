---
name: Rule Repair Playbook (check-rule)
description: Per-failure-mode repair strategies for check-rule findings against `.claude/rules/` files — canonical fixes for Tier-1 deterministic findings, Tier-2 specificity / single-concern findings, and Tier-3 conflicts.
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
- [Tier 2 — Always-on Dimensions](#tier-2--always-on-dimensions)
  - [Dimension 1: Specificity](#dimension-1-specificity)
  - [Dimension 2: Single Concern](#dimension-2-single-concern)
  - [Dimension 3: Staleness](#dimension-3-staleness)
- [Tier 2 — Trigger-gated Dimensions (structured-Intent rules)](#tier-2--trigger-gated-dimensions-structured-intent-rules)
  - [Dimension 4: Intent Completeness](#dimension-4-intent-completeness)
  - [Dimension 5: Example Pair Quality](#dimension-5-example-pair-quality)
  - [Dimension 6: Default-Closed Declaration](#dimension-6-default-closed-declaration)
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
**REASON:** Anthropic's discovery scans for `.md` files only. Other extensions are skipped.

### Malformed `paths:` Glob

**Signal:** `paths:` is present but a glob has unmatched brackets, invalid wildcards, or empty pattern

**CHANGE:** Repair the glob syntax
**FROM:** `paths: "src/api/**/*.{ts"` (unclosed brace)
**TO:** `paths: "src/api/**/*.{ts,tsx}"`
**REASON:** Malformed globs silently fail to match — the rule is in the file but Claude never loads it for any real file path.

### File Too Large

**Signal:** File exceeds 200 non-blank lines

**CHANGE:** Split into topic-specific files
**FROM:** `.claude/rules/conventions.md` (350 lines covering API + tests + deploy)
**TO:** `.claude/rules/api-conventions.md` + `.claude/rules/test-conventions.md` + `.claude/rules/deploy-conventions.md`
**REASON:** Anthropic's CLAUDE.md guidance — "longer files consume more context and reduce adherence" — applies to rules. Splitting also improves the on-demand load path for path-scoped rules.

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
**REASON:** Anthropic documents only `paths:` in rule frontmatter. Other keys (`severity:`, `description:`, `name:`, `type:`) are not consumed by Claude Code and add maintenance noise without behavioral effect.

---

## Tier 2 — Always-on Dimensions

### Dimension 1: Specificity

### Anchor-Free Directive

**Signal:** Directive uses anchor-free terms ("good", "clean", "clear", "appropriate", "well-structured", "properly", "nice", "consistent") without a verifiable definition

**CHANGE:** Replace each anchor-free term with a verifiable directive
**FROM:** "Format code properly and keep files organized"
**TO:** "Use 2-space indentation; run `prettier --check` before committing. API handlers live in `src/api/handlers/`."
**REASON:** Anthropic's example: *"'Use 2-space indentation' instead of 'Format code properly'"*. Anchor-free directives produce uneven adherence because two readers (or two Claude sessions) can interpret them differently.

### Reader-Defers Directive

**Signal:** Directive defers the decision back to the reader without a fallback rule ("use your judgment", "as appropriate", "where it makes sense")

**CHANGE:** Either remove the deferred directive (it carries no information) or add the fallback rule
**FROM:** "Use TypeScript strict mode where it makes sense"
**TO:** "Use TypeScript strict mode in all files under `src/`. Exception: generated code in `src/codegen/`."
**REASON:** A directive that doesn't tell Claude what to do isn't a rule. Either commit to the directive or remove it.

---

### Dimension 2: Single Concern

### Multiple Topics in One File

**Signal:** Multiple top-level `##` sections cover distinct topics that wouldn't naturally co-evolve

**CHANGE:** Split into separate topic files
**FROM:** `.claude/rules/conventions.md` with sections "API design", "Test naming", "Deployment process"
**TO:** `.claude/rules/api-design.md` + `.claude/rules/test-naming.md` + `.claude/rules/deployment.md`
**REASON:** One topic per file. Each rule should answer one question — "how do we do X?" Mixing topics makes path-scoping impossible (each topic might apply to different files) and grows the file beyond the size guidance.

### Body Doesn't Match Filename

**Signal:** Filename describes one topic but body covers another in addition

**CHANGE:** Move the off-topic content to a file matching its actual topic
**FROM:** `api-design.md` containing API conventions AND a section on commit message format
**TO:** `api-design.md` (API only) + `commit-messages.md` (or move into `.claude/CLAUDE.md` if it's a project-wide standard)
**REASON:** Filename is the discovery handle. Future maintainers grep for `commit-messages.md` when looking for commit conventions; they don't expect to find them inside `api-design.md`.

### `paths:` Union Covers Distinct Topics

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

### Dimension 3: Staleness

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

## Tier 2 — Trigger-gated Dimensions (structured-Intent rules)

These repairs apply only when the rule opts into the toolkit-opinion
structured-Intent shape (`## Why` and/or `## Compliant` + `## Non-compliant`
sections). Rules that don't opt in skip these dimensions entirely.

### Dimension 4: Intent Completeness

#### Missing Failure Cost (load-bearing)

**Signal:** Why section names the violation only ("Avoid `console.log`") with no description of what breaks or who bears the cost

**CHANGE:** Add a sentence naming the specific consequence and who bears it
**FROM:** "Avoid using `console.log` in production code. It creates noise."
**TO:** "`console.log` in production builds exposes internal state to end users via browser developer tools and adds measurable latency in high-frequency call paths."
**REASON:** Without failure cost, developers weigh the rule as bureaucratic overhead rather than a real risk. Rules without failure cost have higher disable rates.

#### Missing Exception Policy (load-bearing)

**Signal:** Why section has no `Exception:` line naming a legitimate bypass case

**CHANGE:** Append an `Exception:` line naming at least one legitimate case
**FROM:** Why section ends without exception language
**TO:** Append: `"Exception: <name at least one legitimate case — e.g., 'Exception: test files', 'Exception: scripts in tools/ that are never bundled for production'>."`
**REASON:** Rules with no named exception appear to admit no flexibility, causing developers to disable them entirely rather than follow them in the 95% case.

#### Missing Principle

**Signal:** Why section names what the rule catches and what goes wrong, but not the underlying value

**CHANGE:** Add a sentence naming the principle being enforced
**FROM:** Why section without principle
**TO:** Add: `"This enforces the principle that <value — e.g., 'production code does not leak implementation details'>."`
**REASON:** A named principle anchors the rule when its specifics don't quite fit a new situation. The principle survives changes the specifics can't.

### Dimension 5: Example Pair Quality

#### Synthetic Examples

**Signal:** Examples use generic identifiers (`foo`, `bar`, `myFunction`) or have no file path comment

**CHANGE:** Replace synthetic examples with real codebase code
**FROM:** `function foo(x) { return bar(x) }`
**TO:** `// src/api/handlers/users.ts\nasync function getUser(userId: string) { return db.users.findById(userId) }`
**REASON:** Evidence-anchored rubrics produce more consistent evaluations (+0.17 QWK per RULERS) than pure-inference rubrics. Real code with domain context reduces ambiguity.

#### Wrong Example Order

**Signal:** Compliant example appears before non-compliant example

**CHANGE:** Swap the two example sections
**FROM:** `## Compliant` ... `## Non-compliant`
**TO:** `## Non-compliant` ... `## Compliant`
**REASON:** Listing the rejection case first improves LLM classification accuracy. The compliant example anchors the accepted case after the evaluator has seen what failure looks like.

#### Multiple Examples Per Section

**Signal:** Multiple code snippets in a single Non-Compliant or Compliant section

**CHANGE:** Reduce to one canonical example per section
**FROM:** Non-Compliant section with three different snippets showing different violation patterns
**TO:** Keep the single most clear-cut instance and remove the extras.
**REASON:** Multiple examples encode subtly different behavioral patterns. A single canonical example produces a stronger, less ambiguous anchor.

### Dimension 6: Default-Closed Declaration

**Signal:** Why section has no "When evidence is borderline…" line

**CHANGE:** Append the default-closed declaration to the Why section
**FROM:** Why section ends without uncertainty handling
**TO:** Append: `"When evidence is borderline, prefer WARN over PASS."`
**REASON:** Without this declaration, LLM evaluators silently default to PASS on ambiguous cases, hiding real violations.

---

## Tier 3: Conflicts

**Signal:** Following one rule's directives as written would cause a developer to violate another rule

Resolution strategies in preference order:

1. **Narrow scope** — if one rule was over-broad (always-on when it should be path-scoped, or paths-glob too wide), narrow it so the two rules no longer co-fire on the same files. Verify the narrowed scope still covers the cases the rule was added for.

2. **Merge** — if two rules enforce complementary aspects of the same convention, merge into one rule with both directives stated together. Verify the merged file still passes the size and single-concern checks.

3. **Explicit boundary** — add an exception to one rule acknowledging the other: "Exception: in files covered by `[other-rule.md]`, [behavior] is acceptable." This preserves both rules without contradiction.

4. **Deprecate one** — if one rule supersedes the other: delete the older file. (Anthropic doesn't define an `archived:` status for rules; deletion is the canonical retirement.)

**Intent-preservation check for conflict resolution:** Confirm the resolution preserves the behavioral intent of both rules, not just one. A resolution that silently retires one rule's directive must be flagged for human review.
