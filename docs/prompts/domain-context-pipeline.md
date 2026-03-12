---
name: Domain Context Pipeline
description: Seven-phase prompt to inventory domains, build context via research-distill pipelines, systematically review the codebase, prioritize improvements, and file issues.
---

<context>
You are working in the WOS repository — a Claude Code plugin for building and
maintaining structured project context. The codebase includes Python modules
(wos/), CLI scripts (scripts/), skill definitions (skills/), and tests.

CRITICAL: This is a seven-phase pipeline with explicit user gates. Never
advance past Phase 4 or Phase 6 without user approval.
</context>

<task>
Build comprehensive domain context for this repository, then use that context
to identify, prioritize, and file improvements. Seven phases.

Phase 1 — Domain Inventory (/wos:brainstorm)
Use /wos:brainstorm to explore the full repository (code, skills, scripts,
tests, docs) and produce an exhaustive inventory of domain areas relevant to
WOS's design and implementation. For each domain area, capture:
- Domain name (concise label)
- Description (1-2 sentences on what it covers)
- Key files/modules where this domain appears
- Why it matters to the system's design

The brainstorm output should be a design document with a numbered domain table.
If the inventory exceeds 15 domains, propose groupings and ask the user whether
to consolidate before proceeding.

Phase 2 — Plan the Pipelines (/wos:write-plan)
Use /wos:write-plan to create an implementation plan that sequences a
/wos:research → /wos:distill pipeline for each domain identified in Phase 1.
The plan should:
- List each domain as a task with its research scope
- Define validation criteria for each context file
- Sequence domains so foundational topics are researched first

Phase 3 — Execute (/wos:execute-plan)
Use /wos:execute-plan to work through the approved plan. For each domain:
- Run /wos:research to investigate the domain area
- Run /wos:distill to generate a context file under docs/context/
- Mark the task complete in the plan

Phase 4 — Coverage Evaluation (USER GATE)
After all context files are generated, assess whether the collected context is
sufficient to evaluate the codebase against these criteria:
- Architectural coherence: Do modules have clear boundaries and responsibilities?
- Design principle adherence: Does the code follow the principles in PRINCIPLES.md?
- Skill ecosystem completeness: Are skill definitions well-structured and discoverable?
- Test coverage gaps: Are critical paths untested?
- Consistency: Are conventions (naming, patterns, error handling) applied uniformly?

Produce a coverage matrix mapping each criterion to the context files that
inform it, and flag any gaps where additional research is needed.

Present the coverage matrix to the user for confirmation before proceeding.
If gaps exist, loop back to Phase 3 for additional research before advancing.

Phase 5 — Systematic Codebase Review
Read each module, script, and skill definition. Compare the implementation
against the evaluation criteria from Phase 4, using the collected context files
as your analytical baseline. For each finding, capture:
- What: specific issue or opportunity (file, function, or pattern)
- Why: how it violates or underserves the evaluation criteria
- Severity: bug, design flaw, inconsistency, enhancement, or tech debt
- Suggested fix: brief description of the recommended change

Output a numbered findings list grouped by evaluation criterion.
If no findings emerge for a criterion, explicitly state that it passed review.

Phase 6 — Categorize and Prioritize (USER GATE — /wos:consider)
Use /wos:consider skills to evaluate and prioritize the findings from Phase 5.
Apply relevant mental models to triage:
- /wos:consider:eisenhower-matrix — classify by urgency and importance
- /wos:consider:pareto — identify the 20% of fixes yielding 80% of impact
- /wos:consider:reversibility — flag one-way-door decisions needing caution
- /wos:consider:second-order — consider downstream effects of proposed changes

Produce a prioritized improvement list with rationale for the ordering.
Present to the user for review and approval — the user selects which
improvements to file as issues.

Phase 7 — File Issues (/wos:report-issue)
For each improvement approved by the user in Phase 6, use /wos:report-issue
to file a GitHub Issue. Each issue should include:
- Clear title describing the improvement
- Context from the relevant domain research
- The prioritization rationale from Phase 6
- Suggested implementation approach
</task>

<workflow>
Follow the WOS skill lifecycle for this work:
1. /wos:brainstorm — divergent exploration before committing to a plan
2. /wos:write-plan — structured plan with tasks, sequencing, and validation
3. /wos:execute-plan — systematic execution with progress tracking
4. Coverage evaluation — confirm context sufficiency with user (USER GATE)
5. Systematic review — read and evaluate every module against criteria
6. /wos:consider — categorize and prioritize improvements (USER GATE)
7. /wos:report-issue — file approved improvements as GitHub Issues

Phases 4 and 6 are explicit user gates — do not advance without approval.
</workflow>

<constraints>
- Use the WOS skill workflow — do not skip brainstorm or planning phases.
- Get user approval at each phase gate before advancing.
- Do not skip domains — the goal is exhaustive coverage.
- Context files must follow WOS document conventions (YAML front matter with
  name, description; 200-800 words; one concept per file).
- Phase 6: the user selects which improvements to file — never auto-file.
- Phase 7: file only user-approved improvements. Do not batch — present each
  issue for confirmation before filing.

CRITICAL: Never advance past Phase 4 or Phase 6 without explicit user approval.
</constraints>

<output_format>
Phase 1: Design document with numbered domain table (via /wos:brainstorm)
Phase 2: Implementation plan in docs/plans/ (via /wos:write-plan)
Phase 3: One context file per domain in docs/context/ (via /wos:execute-plan)
Phase 4: Coverage matrix (criteria x context files) with gap analysis
Phase 5: Numbered findings list grouped by evaluation criterion
Phase 6: Prioritized improvement list with mental model rationale
Phase 7: GitHub Issues filed for each approved improvement
</output_format>
