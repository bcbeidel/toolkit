---
name: Plan Document Format
description: Canonical reference for plan document structure, lifecycle states, and task decomposition rules
---

# Plan Document Format

Plans are Markdown files stored at `.plans/YYYY-MM-DD-<feature-name>.plan.md`.

## Frontmatter Schema

```yaml
---
name: Feature Name
description: One-sentence summary of what this plan achieves
type: plan
status: draft
related:
  - .designs/YYYY-MM-DD-<topic>.design.md
---
```

**Fields:**

- `name` — plan title (required)
- `description` — one-sentence summary (required)
- `type: plan` — document type (required, literal)
- `status` — lifecycle state (required when `type: plan`, one of: draft,
  approved, executing, completed, abandoned)
- `related` — links to design docs, context files, other plans (optional)

Note: the frontmatter parser does not strip quotes. Use unquoted values.

## Required Sections

These are format conventions for plan authors. Downstream skills (plan-work,
start-work, check-work) enforce these through workflow, not code
validation.

| Section | Purpose | Research Basis |
|---------|---------|----------------|
| **Goal** | What this plan achieves and why. 2-3 sentences. State user-visible outcome. | Codex "Purpose / Big Picture"; observable acceptance criteria |
| **Scope** | Must have / Won't have. Explicit exclusions prevent scope creep. | No tool does this; MoSCoW from PM research |
| **Approach** | High-level technical strategy. How the goal will be achieved. | Codex "Plan of Work"; "middle altitude" specification |
| **File Changes** | Every file created, modified, or deleted. | Prior art from planning tools; Cursor codebase-aware research |
| **Tasks** | Decomposed work items as checkbox list with verification commands. | Checkbox convergence across all tools; 3-level verification |
| **Validation** | How to verify the plan succeeded end-to-end. Observable behavior. At least one concrete criterion required. | Gap in comparative analysis; plan-level verification |

## Lifecycle State Machine

```
draft → approved → executing → completed
                             → abandoned
draft → abandoned
approved → abandoned
```

| Transition | Trigger | Gate |
|------------|---------|------|
| draft → approved | User explicitly approves | Consensus-based: human says "approved" or equivalent |
| approved → executing | Execution begins | Evidence-based: start-work checks `status: approved` |
| approved → abandoned | User decides not to proceed | Consensus-based: human decision |
| executing → completed | All tasks checked, validation passing | Evidence-based: all checkboxes checked + check-work passes |
| executing → abandoned | User decides to stop | Consensus-based: human decision |
| draft → abandoned | User decides not to proceed | Consensus-based: human decision |

## Task Decomposition Rules

1. **Outcome-oriented** — name tasks as deliverables, not activities
2. **"Middle altitude"** — observable outcomes, not implementation prescriptions
3. **Independently verifiable** — every task ends with a verification command
4. **No task exceeds 1000 lines of change** — split further if larger
5. **Dependencies explicit** — if task B requires task A, say so
6. **Chunk boundaries** — use `## Chunk N: <name>` for plans with 10+ tasks

## Design Justification

| Decision | Source | Evidence |
|----------|--------|----------|
| 6-section format | [Codex PLANS.md](https://developers.openai.com/cookbook/articles/codex_exec_plans/) (OpenAI, 2025) | ACH analysis across 6 tools selected this as least-inconsistent format |
| 5-state lifecycle | [IETF RFC 2026](https://www.rfc-editor.org/rfc/rfc2026) (1996); [KEP Process](https://github.com/kubernetes/enhancements/tree/master/keps/sig-architecture/0000-kep-process) (K8s, 2024); [ADR Process](https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/adr-process.html) (AWS, 2024) | 3-7 states is the sweet spot; every state must have a consumer |
| Scope section with Must/Won't | MoSCoW prioritization (PM research) | No AI coding tool captures explicit exclusions |
| Checkbox task format | [Codex PLANS.md](https://developers.openai.com/cookbook/articles/codex_exec_plans/); [Effective Harnesses](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) (Anthropic, 2025) | Checkbox convergence across all 6 tools studied |
| "Middle altitude" tasks | [Codex PLANS.md](https://developers.openai.com/cookbook/articles/codex_exec_plans/) | Observable outcomes, not implementation prescriptions |
| Lifecycle in frontmatter | Comparative analysis across 6 tools | No existing tool tracks plan status as queryable metadata |
| Status validation in document.py | toolkit convention | Same module as existing required-field checks; catches typos early |
