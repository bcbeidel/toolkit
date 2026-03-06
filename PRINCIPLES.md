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
