---
name: "Planning Skill Workflow Prompt"
description: "Prompt for working through issues #157-#164 (WOS planning skills) sequentially"
---

# Planning Skill Workflow Prompt

Use this prompt to work through issues #157–#164 (WOS planning skills) sequentially.

## Prompt

```text
<context>
We are building WOS planning skills. Issues #157–#164 form a dependency chain:
#157 (plan document format) → #158 (brainstorm) → #159 (write-plan) →
#160 (execute-plan) → #161 (validate-plan) → #162 (finish-work) →
#163 (brainstorm↔write-plan feedback) → #164 (deprecation docs).

Start with the next unstarted issue in that sequence. My personal notes repo
at ~/Documents/git/notes may contain prior research, design thinking, or
related references.
</context>

<task>
Complete the selected issue end-to-end using this workflow:

1. **Discover** — Read the GitHub issue. Search ~/Documents/git/notes for
   files mentioning planning workflows, skill design, document formats, or
   the specific issue topic. Summarize the issue and any relevant notes found.

2. **Gap analysis** — List what we know vs. what we still need to answer
   before implementation. Be specific about unknowns.

3. **Research** (/wos:research) — Investigate the identified gaps. Focus on
   how existing WOS skills and conventions inform the design.

4. **Brainstorm** (/wos:brainstorm) — Explore design options for the issue,
   informed by research findings and notes.

5. **Plan** (/wos:write-plan) — Write an implementation plan. Store it in
   docs/plans/ per CLAUDE.md conventions.

6. **Execute** (/wos:execute-plan) — Implement the plan on a feature branch.

7. **Validate** (/wos:validate-plan)

8. **PR** — Create a pull request. Wait for CI to pass and human feedback
   before merging.
</task>

<constraints>
- Do NOT skip workflow phases — each informs the next.
- Pause for my input after gap analysis (step 2) and after the plan (step 5).
- If no relevant notes are found in ~/Documents/git/notes, state that and
  proceed to gap analysis.
- Follow WOS conventions: feature branch, plan in docs/plans/, checkboxes
  for progress, PR with CI verification.
</constraints>
```
