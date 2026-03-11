---
name: "Plan Document Format Design"
description: "Design spec for plan document format, lifecycle, and status field — issue #157"
related:
  - docs/plans/2026-03-06-audit-validation-enhancements-plan.md
---

## Goal

Define a self-contained plan document format with lifecycle metadata so that
WOS skills (write-plan, execute-plan, validate-plan) share a common structure.
No existing AI coding tool tracks plan lifecycle as queryable metadata — this
fills that gap.

## Design

### Frontmatter Schema

Plans are Markdown files stored at `docs/plans/YYYY-MM-DD-<feature-name>.md`
with this frontmatter:

```yaml
---
name: "Feature Name"
description: "One-sentence summary of what this plan achieves"
type: plan
status: draft
related:
  - docs/plans/YYYY-MM-DD-<topic>-design.md
---
```

**Fields:**

- `name` — plan title (required)
- `description` — one-sentence summary (required)
- `type: plan` — document type (required, literal)
- `status` — lifecycle state (required, one of: draft, approved, executing,
  completed, abandoned)
- `related` — links to design docs, context files, other plans (optional)

### Required Sections

| Section | Purpose | Research Basis |
|---------|---------|----------------|
| **Goal** | What this plan achieves and why. 2-3 sentences. State user-visible outcome. | Codex "Purpose / Big Picture"; observable acceptance criteria |
| **Scope** | Must have / Won't have. Explicit exclusions prevent scope creep. | No tool does this; MoSCoW from PM research |
| **Approach** | High-level technical strategy. How the goal will be achieved. | Codex "Plan of Work"; "middle altitude" specification |
| **File Changes** | Every file created, modified, or deleted. | superpowers precedent; Cursor codebase-aware research |
| **Tasks** | Decomposed work items as checkbox list with verification commands. | Checkbox convergence across all tools; 3-level verification |
| **Validation** | How to verify the plan succeeded end-to-end. Observable behavior. At least one concrete criterion required. | Gap in comparative analysis; plan-level verification |

### Lifecycle State Machine

```
draft → approved → executing → completed
                             → abandoned
draft → abandoned
```

| Transition | Trigger | Gate |
|------------|---------|------|
| draft → approved | User explicitly approves | Consensus-based: human says "approved" or equivalent |
| approved → executing | Execution begins | Evidence-based: execute-plan checks `status: approved` |
| executing → completed | All tasks checked, validation passing | Evidence-based: all checkboxes checked + validate-plan passes |
| executing → abandoned | User decides to stop | Consensus-based: human decision |
| draft → abandoned | User decides not to proceed | Consensus-based: human decision |

### Task Decomposition Rules

1. **Outcome-oriented** — name tasks as deliverables, not activities
2. **"Middle altitude"** — observable outcomes, not implementation prescriptions
3. **Independently verifiable** — every task ends with a verification command
4. **No task exceeds 1000 lines of change** — split further if larger
5. **Dependencies explicit** — if task B requires task A, say so
6. **Chunk boundaries** — use `## Chunk N: <name>` for plans with 10+ tasks

### Document Model Change

Add `status: Optional[str]` to the `Document` dataclass in `wos/document.py`.
Default `None`. Parsed from frontmatter like existing optional fields.

### Status Enum Validation

When `status` is present in parsed frontmatter, validate it against the
closed set: `draft`, `approved`, `executing`, `completed`, `abandoned`.
Raise `ValueError` on invalid values. This is parse-time enforcement in
`wos/frontmatter.py`, same pattern as existing required-field checks.

### Existing Plan Retrofit

Add `type: plan` and `status` to all existing plan files in `docs/plans/`.
Infer status from checkbox state:

- All checkboxes checked → `completed`
- Some checked → `executing`
- None checked → `draft`

This validates the lifecycle model against real data.

## Design Justification

| Decision | Source | Evidence |
|----------|--------|----------|
| 6-section format | [Codex PLANS.md](https://developers.openai.com/cookbook/articles/codex_exec_plans/) (OpenAI, 2025) | ACH analysis across 6 tools selected this as least-inconsistent format |
| 5-state lifecycle | [IETF RFC 2026](https://www.rfc-editor.org/rfc/rfc2026) (1996); [KEP Process](https://github.com/kubernetes/enhancements/tree/master/keps/sig-architecture/0000-kep-process) (K8s, 2024); [ADR Process](https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/adr-process.html) (AWS, 2024) | 3-7 states is the sweet spot; every state must have a consumer |
| Scope section with Must/Won't | MoSCoW prioritization (PM research) | No AI coding tool captures explicit exclusions |
| Checkbox task format | [Codex PLANS.md](https://developers.openai.com/cookbook/articles/codex_exec_plans/); [Effective Harnesses](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) (Anthropic, 2025) | Checkbox convergence across all 6 tools studied |
| "Middle altitude" tasks | [Codex PLANS.md](https://developers.openai.com/cookbook/articles/codex_exec_plans/) | Observable outcomes, not implementation prescriptions |
| Lifecycle in frontmatter | Comparative analysis across 6 tools | No existing tool tracks plan status as queryable metadata |
| Parse-time status validation | WOS convention | Same pattern as existing required-field checks; catches typos early |

## Not In Scope

- Plan-specific audit validators in `validators.py` — deferred (see #161 comment)
- Required section validation — deferred
- Task format validation — deferred
