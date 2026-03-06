# Principle Tensions Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Create `PRINCIPLES.md` at repo root with full design principle descriptions and tension resolution examples, then fix the broken link in CLAUDE.md.

**Architecture:** Restore deleted content from git history, add a new "When Principles Conflict" section with 4 tension examples, update CLAUDE.md to point to the new file.

**Tech Stack:** Markdown only. No code changes.

---

### Task 1: Create PRINCIPLES.md with restored content

**Files:**
- Create: `PRINCIPLES.md`

**Step 1: Create PRINCIPLES.md with the original design principles content plus the new tensions section**

The content comes from the deleted file at `git show b5c7a1b~1:docs/research/2026-02-22-design-principles.md`, with these changes:
- Remove YAML frontmatter (this is a root-level living doc, not a WOS-managed document)
- Add "When Principles Conflict" section with 4 tension examples

```markdown
# WOS Design Principles

## What WOS cares about

1. **Convention over configuration.** Good patterns — document structure, naming
   conventions, source hierarchies — are documented for humans and LLMs to
   follow voluntarily, not enforced in code.

2. **Structure in code, quality in skills.** The code layer checks what's
   deterministic — links resolve, frontmatter exists, indexes sync. The skill
   layer guides content quality through research rigor, source verification,
   and structured workflows. Neither does the other's job.

3. **Single source of truth.** Navigation and indexes are derived from disk
   state, never curated by hand. Anything maintained manually will drift.

## How WOS is built

4. **Keep it simple.** No class hierarchies, no frameworks, no indirection.
   When choosing between a flexible abstraction and a straightforward
   implementation, choose the straightforward one.

5. **When in doubt, leave it out.** Every required field, every abstraction,
   every feature must justify its presence. When choosing between adding
   complexity and removing a case, remove it.

6. **Omit needless words.** Every word in agent-facing output must earn its
   place. Agents consume navigation and context on every conversation —
   brevity is a feature.

7. **Depend on nothing.** The core package depends only on the standard
   library. External dependencies are isolated to scripts that declare their
   own.

8. **One obvious way to run.** Every script, every skill, same entry point.
   Consistency eliminates a class of failures.

## How WOS operates

9. **Separate reads from writes.** Audit observes and reports. Fixes require
   explicit user action. No tool modifies files as a side effect of reading
   them.

10. **Bottom line up front.** LLMs lose attention in the middle of long
    documents. Key insights go at the top and bottom. This is convention
    (principle 1), not enforcement.

## What these principles reject

- No content quality validation in the code layer
- No class hierarchies or framework patterns
- No mandatory curation (navigation is always derived)
- No runtime dependencies in the core package
- No special-case invocation patterns

## When Principles Conflict

Principles occasionally pull in opposite directions. These worked examples
document how to resolve the most common tensions.

### P5 "leave it out" vs P10 "bottom line up front"

**Scenario:** Adding a summary section to a document increases word count but
front-loads key insights for the reader.

**Resolution:** P10 wins. The added words aren't needless — they serve
comprehension by putting conclusions where attention is highest. P5 targets
optional complexity, not communication clarity.

### P4 "keep it simple" vs P2 "quality in skills"

**Scenario:** A skill needs complex multi-phase workflow logic (e.g., the
research skill's 8-phase gate structure).

**Resolution:** P2 wins for skill internals — skills are where judgment-heavy
complexity belongs. But each phase within a skill should be as simple as P4
demands. Complexity is permitted at the workflow level, not within individual
steps.

### P5 "leave it out" vs structural requirements

**Scenario:** A frontmatter field exists but has no clear value for a specific
document. Should it be omitted?

**Resolution:** P5 applies to optional additions, not structural requirements.
If omitting a field causes silent downstream failures (e.g., a validator
expects it, or navigation breaks), add it — the field isn't optional, it's
load-bearing. P5 governs discretionary choices, not system contracts.

### P6 "omit needless words" vs P2 "quality in skills"

**Scenario:** A skill's instruction volume is high, but cutting text risks
degrading output quality.

**Resolution:** Reduce volume without reducing capability. If cutting
instruction text degrades output quality, the words weren't needless — they
were earning their place. Measure by outcome (does the skill still produce
good results?), not by word count. This is the rubric for skill density
reduction: cut what's redundant or implicit, preserve what's load-bearing.
```

**Step 2: Verify the file was created correctly**

Run: `wc -w PRINCIPLES.md`
Expected: ~450-500 words

**Step 3: Commit**

```bash
git add PRINCIPLES.md
git commit -m "docs: create PRINCIPLES.md with design principles and tension examples

Restores full design principle descriptions from deleted
docs/research/2026-02-22-design-principles.md and adds a new
'When Principles Conflict' section with 4 worked tension examples:
- P5 vs P10 (leave it out vs bottom line up front)
- P4 vs P2 (keep it simple vs quality in skills)
- P5 vs structural requirements
- P6 vs P2 (omit needless words vs quality in skills)

Closes #129"
```

---

### Task 2: Update CLAUDE.md link

**Files:**
- Modify: `CLAUDE.md:43`

**Step 1: Update the broken link on line 43**

Change:
```
Full descriptions: [Design Principles](docs/research/2026-02-22-design-principles.md)
```
To:
```
Full descriptions: [Design Principles](PRINCIPLES.md)
```

**Step 2: Also update the Reference section link (line ~108)**

Change:
```
- Design principles: [WOS Design Principles](docs/research/2026-02-22-design-principles.md)
```
To:
```
- Design principles: [WOS Design Principles](PRINCIPLES.md)
```

**Step 3: Commit**

```bash
git add CLAUDE.md
git commit -m "fix: update CLAUDE.md design principles links to PRINCIPLES.md"
```

---

### Task 3: Verify

**Step 1: Check for any remaining broken references to the old path**

Run: `grep -r "2026-02-22-design-principles" .`
Expected: no results (or only git history references)

**Step 2: Check for any other files linking to the old path**

Run: `grep -r "design-principles.md" . --include="*.md"`
Expected: only PRINCIPLES.md itself or irrelevant matches
