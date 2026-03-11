---
name: Brainstorm Skill Implementation
description: Create wos:brainstorm skill with SKILL.md and two reference files — issue #158
type: plan
status: completed
related:
  - skills/_shared/references/plan-format.md
---

# Brainstorm Skill Implementation

**Goal:** Ship the `wos:brainstorm` skill (#158) — a WOS-native skill that
scaffolds divergent-then-convergent thinking before plan creation, producing
design documents with WOS-compatible frontmatter.

**Scope:**

Must have:
- `skills/brainstorm/SKILL.md` under 500 lines, following WOS skill conventions
- `skills/brainstorm/references/spec-format-guide.md` — how to write effective specs
- `skills/brainstorm/references/exploration-patterns.md` — divergent/convergent scaffolds
- Skill triggers on "brainstorm", "explore", "design", "what should we build"
- Hard gate: produces design docs, never plans or code
- Scaffolds 2-3 approaches before convergence
- Feedback instruction text for future write-plan integration (#159/#163)
- Design doc output with `type: design` frontmatter and `related` linkage

Won't have:
- Visual companion (CLI-focused, no browser dependency)
- Spec-document-reviewer subagent dispatch (WOS doesn't use TodoWrite/subagent review loops)
- Scripts or Python code (pure markdown skill)
- New validators or document model changes

**Approach:** Create three markdown files. SKILL.md adapts the issue #158
spec with enhancements from superpowers experience (scope decomposition,
incremental section validation, isolation/clarity principles). Reference
files distill research from brainstorming patterns and pre-implementation
design patterns into concise, agent-facing playbooks. Validate with the
existing skill audit.

**Branch:** `feat/158-brainstorm-skill`
**PR:** TBD

---

### Task 1: Create skill directory and SKILL.md

**Files:**
- Create: `skills/brainstorm/SKILL.md`
- Create: `skills/brainstorm/references/` (directory)

- [x] **Step 1: Create the directory structure**

```bash
mkdir -p skills/brainstorm/references
```

- [x] **Step 2: Write SKILL.md**

Create `skills/brainstorm/SKILL.md` with the following content:

```markdown
---
name: brainstorm
description: >
  Use before creating implementation plans. Explores user intent,
  requirements, and design through structured divergent-then-convergent
  thinking. Produces a design document, not code. Use when the user
  wants to "brainstorm", "explore", "design", "figure out what to build",
  or needs to think through a problem before planning.
user-invocable: true
references:
  - references/spec-format-guide.md
  - references/exploration-patterns.md
---

# Brainstorm

Explore ideas and turn them into design specifications through structured
dialogue. The output is a design document — not a plan, not code.

<HARD-GATE>
Do NOT invoke any planning or implementation skill, write any code, or take
any implementation action until you have presented a design and the user has
approved it. This applies to EVERY task regardless of perceived simplicity.
</HARD-GATE>

## Workflow

### 1. Understand Intent

- Explore project context — read relevant files, docs, recent commits.
- Assess scope: if the request describes multiple independent subsystems,
  flag this immediately. Don't refine details of a project that needs
  decomposition first. Each sub-project gets its own brainstorm → plan cycle.
- Ask clarifying questions one at a time, multiple-choice preferred.
  Establish what and why before how.

### 2. Diverge

- Propose 2-3 approaches with tradeoffs.
- Lead with your recommendation and reasoning.
- Do not converge prematurely — if only one approach is proposed,
  divergence was skipped.

See [Exploration Patterns](references/exploration-patterns.md) for question
templates and approach comparison format.

### 3. Converge

- Narrow to a recommended approach based on user input and constraints.
- Confirm scope boundaries (must have / won't have).

### 4. Write the Spec

- Present design section by section. Ask after each whether it looks right.
  Cover: purpose, behavior, components, constraints, acceptance criteria.
- Calibrate depth to task complexity — a paragraph for simple tasks, full
  structured spec for multi-system changes.
- Save to `docs/plans/YYYY-MM-DD-<name>-design.md` with WOS frontmatter.

See [Spec Format Guide](references/spec-format-guide.md) for format
conventions and examples.

### 5. Review with User

- Present a summary of the complete design.
- Hard gate: do not proceed until the user approves.

### 6. Hand Off

- Offer to invoke `wos:write-plan` with the approved spec.
- The plan should reference this design doc via its `related` field,
  establishing traceability between design and plan.

## Key Instructions

- **Specs define WHAT and WHY, not HOW.** Architecture decisions belong
  in the plan, not the spec. If the spec reads like pseudo-code, it has
  crossed into implementation.
- **Calibrate depth to complexity.** A paragraph for simple tasks, full
  structured spec for multi-system changes.
- **One question at a time.** Prefer multiple-choice over open-ended.
- **Design for isolation and clarity.** Break systems into units with one
  clear purpose, well-defined interfaces, testable independently.
- **Follow existing patterns.** Explore the current codebase structure
  before proposing changes. Work with conventions, not against them.
- **YAGNI.** Remove unnecessary features from all designs. Every element
  must justify its presence.

## Receiving Feedback from Write-Plan

If receiving structured feedback from `wos:write-plan` indicating design
infeasibility, consume the feedback artifact and revise affected design
sections. For major revisions, follow the "supersede, don't edit" pattern:
create a new design doc that references the original via `related`, rather
than modifying the approved original.

> Note: The structured feedback format and delivery mechanism are defined
> in the write-plan skill (#159) and the feedback loop (#163).

## Anti-Pattern Guards

1. **Premature convergence** — jumping to solutions before exploring the
   problem space. If only one approach is proposed, divergence was skipped.
2. **Over-specification** — if the spec reads like pseudo-code, it has
   crossed into implementation. Specs should be verifiable from the outside.
3. **Skipping exploration** — even "simple" tasks benefit from clarification.
   The calibration instruction handles truly trivial changes, not anything
   involving design decisions.
4. **Scope blindness** — not flagging projects that need decomposition
   before deep-diving into details.

## Output Format

Design docs use WOS frontmatter:

    ---
    name: Feature Name
    description: One-sentence summary
    type: design
    status: draft
    related:
      - docs/context/relevant-file.md
    ---

Save to `docs/plans/YYYY-MM-DD-<name>-design.md`. The `related` field
links to context files, research docs, or other design docs.
```

- [x] **Step 3: Verify line count is under 500**

Run: `wc -l skills/brainstorm/SKILL.md`
Expected: under 500 lines (target ~130 lines)

- [x] **Step 4: Commit**

```bash
git add skills/brainstorm/SKILL.md
git commit -m "feat: add wos:brainstorm SKILL.md — issue #158"
```

---

### Task 2: Create spec-format-guide.md reference

**Files:**
- Create: `skills/brainstorm/references/spec-format-guide.md`

- [x] **Step 1: Write spec-format-guide.md**

Create `skills/brainstorm/references/spec-format-guide.md` with the following
content:

```markdown
---
name: Spec Format Guide
description: How to write effective design specifications — behavior-focused, observable, bounded
---

# Spec Format Guide

Design specifications define WHAT the system does externally, not HOW it
works internally. Architecture decisions belong in the plan.

## Required Frontmatter

    ---
    name: Feature Name
    description: One-sentence summary
    type: design
    status: draft
    related:
      - docs/context/relevant-file.md
    ---

Use unquoted values. The WOS frontmatter parser does not strip quotes.

## Spec Sections

Scale each section to the complexity of the task. A simple task may need
only Purpose and Acceptance Criteria. A multi-system change needs all
sections.

| Section | Purpose | When to Include |
|---------|---------|-----------------|
| **Purpose** | What this achieves and why. State the user-visible outcome. | Always |
| **User Journeys** | Who uses this and how. Scenarios, not implementation. | Multi-user or workflow changes |
| **Behavior** | Observable input/output mappings, preconditions, postconditions. | API or data model changes |
| **Scope** | Must have / Won't have. Explicit exclusions prevent scope creep. | Always |
| **Constraints** | Technical, organizational, or timeline constraints. | When constraints affect design |
| **Acceptance Criteria** | Observable behaviors that prove success. Verifiable from outside. | Always |

## Writing Principles

1. **Behavior over implementation** — describe what the user sees, not what
   the code does. "Users can filter by date range" not "Add a SQL WHERE
   clause on created_at."
2. **Observable outcomes** — every requirement should be verifiable without
   reading source code. If you can't test it from the outside, it's an
   implementation detail.
3. **Explicit boundaries** — state what's excluded alongside what's included.
   "Won't have" is as important as "Must have."
4. **Structured over freeform** — use tables, lists, and Given/When/Then
   where they add clarity. Avoid long prose paragraphs.
5. **Minimum viable specification** — match effort to stakes. A config
   change needs a sentence. A new subsystem needs structured sections.

## Depth Calibration

| Task Complexity | Spec Depth | Example |
|----------------|------------|---------|
| Trivial (config, typo) | 1-2 sentences — purpose and acceptance criteria | "Change timeout from 30s to 60s. Verify with integration test." |
| Simple (single component) | Short paragraph per section, 2-3 sections | New validation rule, API endpoint |
| Moderate (multi-component) | Full sections, acceptance criteria per component | Feature spanning frontend + backend |
| Complex (multi-system) | Decompose into sub-projects first, then full spec per sub-project | Platform-level changes |
```

- [x] **Step 2: Verify line count**

Run: `wc -l skills/brainstorm/references/spec-format-guide.md`
Expected: under 80 lines (target ~65 lines)

- [x] **Step 3: Commit**

```bash
git add skills/brainstorm/references/spec-format-guide.md
git commit -m "docs: add spec-format-guide reference for brainstorm skill"
```

---

### Task 3: Create exploration-patterns.md reference

**Files:**
- Create: `skills/brainstorm/references/exploration-patterns.md`

- [x] **Step 1: Write exploration-patterns.md**

Create `skills/brainstorm/references/exploration-patterns.md` with the
following content:

```markdown
---
name: Exploration Patterns
description: Divergent/convergent thinking scaffolds, question templates, and approach comparison format
---

# Exploration Patterns

Scaffolds for structured exploration. Use these patterns during the
Understand, Diverge, and Converge phases.

## Asking Questions

One question at a time. Prefer multiple-choice.

**Multiple-choice format:**
> How should [component] handle [scenario]?
> - **A)** [option] — [1-sentence tradeoff]
> - **B)** [option] — [1-sentence tradeoff]
> - **C)** Something else (describe)

**When open-ended is appropriate:**
- When the answer space is too large to enumerate
- When you need the user's domain expertise, not a design choice
- Keep it focused: "What does [term] mean in your context?" not
  "Tell me about your requirements"

## Exploring Approaches

Present 2-3 approaches with tradeoffs. Lead with your recommendation.

**Approach comparison format:**

| | Approach A: [Name] | Approach B: [Name] | Approach C: [Name] |
|---|---|---|---|
| **Summary** | 1-2 sentences | 1-2 sentences | 1-2 sentences |
| **Strengths** | Bullet list | Bullet list | Bullet list |
| **Weaknesses** | Bullet list | Bullet list | Bullet list |
| **Best when** | Condition | Condition | Condition |

> **Recommendation:** Approach [X] because [reason tied to user's
> stated constraints].

If you can only think of one approach, you haven't explored enough.
Push for at least two — even if one is "do nothing" or "simpler
alternative."

## Scope Decomposition

Flag oversized projects before deep-diving into details.

**Signals a project needs decomposition:**
- Request mentions 3+ independent subsystems
- Components have no runtime dependencies on each other
- Different teams or skills would own different pieces
- The spec would exceed ~2 pages if written as one document

**Decomposition response:**
> This looks like it has [N] independent pieces: [list]. I'd suggest
> brainstorming each one separately — they can be built in any order.
> Which should we start with?

## Convergence Checklist

Before moving from Converge to Write the Spec, confirm:

- [ ] User selected an approach (or a hybrid)
- [ ] Scope boundaries confirmed (must have / won't have)
- [ ] No open ambiguities about user intent
- [ ] Acceptance criteria are articulable (even if not yet written)
```

- [x] **Step 2: Verify line count**

Run: `wc -l skills/brainstorm/references/exploration-patterns.md`
Expected: under 80 lines (target ~65 lines)

- [x] **Step 3: Commit**

```bash
git add skills/brainstorm/references/exploration-patterns.md
git commit -m "docs: add exploration-patterns reference for brainstorm skill"
```

---

### Task 4: Run validation

**Files:**
- None modified (validation only)

Depends on: Tasks 1-3

- [x] **Step 1: Run existing test suite**

Run: `uv run python -m pytest tests/ -v`
Expected: ALL PASS (no regressions)

- [x] **Step 2: Run skill audit**

Run: `uv run scripts/audit.py --root .`
Expected: No new failures. Check that the brainstorm skill passes:
- Name format (lowercase, no reserved words)
- Description length (under 1024 chars, no XML tags)
- Instruction line count (SKILL.md + references under 200 lines)
- SKILL.md body under 500 lines

- [x] **Step 3: Fix any audit findings**

If the audit reports warnings or failures for the brainstorm skill, fix them
and re-run until clean.

- [x] **Step 4: Commit any fixes**

```bash
git add skills/brainstorm/
git commit -m "fix: address audit findings for brainstorm skill"
```

(Skip if no fixes needed.)

---

## Validation

- [x] `uv run python -m pytest tests/ -v` — all tests pass
- [x] `uv run scripts/audit.py --root .` — no failures for brainstorm skill
- [x] `skills/brainstorm/SKILL.md` exists and is under 500 body lines
- [x] `skills/brainstorm/references/spec-format-guide.md` exists
- [x] `skills/brainstorm/references/exploration-patterns.md` exists
- [x] SKILL.md frontmatter has name, description, user-invocable, references
- [x] Skill triggers on "brainstorm", "explore", "design" (verify via description text)
- [x] Hard gate present: no plan/code creation until spec approved
- [x] Design doc output format includes `type: design` frontmatter
- [x] Feedback instruction references issues #159 and #163
