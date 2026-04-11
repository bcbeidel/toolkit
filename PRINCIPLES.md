# WOS Design Principles

## What WOS cares about

### 1. Convention over configuration
Document patterns, don't enforce them.

**Rationale:** Projects that enforce conventions via tooling create coupling and
rigidity. Documentation lets teams adopt patterns voluntarily and evolve them
without breaking automation.
**Boundary:** When safety-critical behavior requires enforcement (e.g.,
preventing accidental data loss), use code checks or hooks instead of
documentation alone.
**Verification:** No WOS code rejects valid documents based on content quality.
Validators check structure (frontmatter exists, links resolve), not content.

### 2. Structure in code, quality in skills
Deterministic checks in Python, judgment in LLMs. Neither does the other's job.

**Rationale:** Code excels at deterministic checks (does this file exist? does
this URL resolve?). LLMs excel at judgment (is this research thorough?). Mixing
responsibilities creates brittle, unreliable systems.
**Boundary:** When a quality check can be made deterministic (e.g., instruction
line count thresholds), it belongs in code. The test: can you write a unit test
for it?
**Verification:** `wos/validators.py` contains no content quality assessments.
Assessment modules (`research/`, `plan/`) report observable structural facts
(checkbox state, word count, section presence); models interpret those facts.
Skills contain no deterministic validation logic.

### 3. Single source of truth
Navigation, indexes, and artifact lifecycle state are derived from disk, never
curated by hand.

**Rationale:** Hand-maintained indexes drift from actual content. Auto-generation
from disk state makes navigation correct by construction.
**Boundary:** Preambles in `_index.md` files are hand-written and preserved
across regeneration — human curation is appropriate for context that isn't
derivable from file metadata.
**Verification:** `scripts/reindex.py` regenerates all `_index.md` from disk
state. `check_index_sync()` fails when indexes don't match directory contents.
Plan and design documents track lifecycle via frontmatter `status` fields —
execution gates check status from the document, not from external state.

## How WOS is built

### 4. Keep it simple
No class hierarchies, no frameworks, no indirection. Choose the straightforward
implementation.

**Rationale:** Simplicity reduces bug surface area, lowers onboarding cost, and
makes the codebase navigable without specialized knowledge.
**Boundary:** Skill workflows may involve multi-phase complexity (e.g., research
skill's phased structure). Simplicity applies within each phase, not to overall
workflow design.
**Verification:** `wos/` uses no class inheritance. Modules are single-purpose —
larger modules (validators, assessors) remain cohesive tools without abstraction
indirection. No abstractions exist that serve only one caller.

### 5. When in doubt, leave it out
Every field, abstraction, and feature must justify its presence.

**Rationale:** Each addition increases maintenance burden, documentation surface,
and cognitive load for agents. Removal is harder than non-addition.
**Boundary:** Does not apply to structural requirements. If omitting a field
causes silent downstream failures (validators expect it, navigation breaks), the
field is load-bearing, not optional.
**Verification:** Frontmatter requires only `name` and `description`. Optional
fields (`type`, `sources`, `related`) are validated only when present.

### 6. Omit needless words
Every word in agent-facing output must earn its place.

**Rationale:** Agents consume navigation and context on every conversation turn.
Verbose output wastes attention budget and can push important information out of
context windows.
**Boundary:** When cutting text degrades output quality, the words aren't
needless. Measure by outcome (does the skill still produce good results?), not
by word count.
**Verification:** Skill audit warns when instruction lines exceed 500 or
SKILL.md body exceeds 500 lines. `_index.md` entries are single-line
descriptions.

### 7. Depend on nothing
The core package depends only on the standard library. External dependencies are
isolated to scripts that declare their own.

**Rationale:** Eliminates version conflicts and supply-chain risk. Users install
one tool, not a dependency tree.
**Boundary:** Dev dependencies (pytest, ruff) are acceptable. Scripts may use
PEP 723 inline metadata for their own isolated deps.
**Verification:** `wos/` imports nothing outside stdlib. `scripts/` use only
PEP 723 `[tool.uv]` dependencies.

### 8. One obvious way to run
Every script, every skill, same entry point. Skill-to-skill transitions name
the target and wait for user consent. Consistency eliminates a class of failures.

**Rationale:** When every script runs the same way and every skill transition
follows the same pattern, skills don't need special-case instructions and users
don't need to remember invocation variants. Explicit handoffs preserve user
awareness of workflow structure.
**Boundary:** Test invocation (`python -m pytest`) differs from script
invocation (`python scripts/foo.py`) — acceptable because they're different
tools, not different patterns for the same tool. Within a single skill's
internal phases, transitions don't require handoff confirmation — this applies
to cross-skill boundaries only.
**Verification:** All scripts in `scripts/` have PEP 723 inline metadata and
run via `python`. No skill documentation requires external runtime dependencies.
Delivery pipeline skills (scope-work → plan-work → start-work →
check-work → finish-work) end with explicit handoff naming the next skill
before invocation.

## How WOS operates

### 9. Separate reads from writes
Audit observes and reports. Fixes require explicit user action. No tool modifies
files as a side effect of reading them.

**Rationale:** Side-effect-free reads let users safely explore project state
without worrying about unintended modifications. This builds trust in the
tooling.
**Boundary:** The `--fix` flag on audit explicitly opts into writes — this is
the user choosing to modify, not a side effect of reading.
**Verification:** `scripts/lint.py` without `--fix` modifies no files.
`scripts/reindex.py` is a separate explicit command.

### 10. Bottom line up front
Key insights go at the top and bottom. Detail in the middle.

**Rationale:** LLMs lose attention in the middle of long documents (the "lost in
the middle" phenomenon). Front-loading conclusions maximizes comprehension.
**Boundary:** Short documents (under ~50 lines) don't benefit from BLUF
formatting — the overhead exceeds the value.
**Verification:** Skill output formats place summaries and key findings before
supporting detail. `_index.md` preambles provide area context before file
listings.

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
