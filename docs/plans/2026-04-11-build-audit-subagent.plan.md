---
name: build-subagent + audit-subagent Skills
description: Add /wos:build-subagent and /wos:audit-subagent skills to scaffold and audit Claude Code custom subagent definitions in .claude/agents/<name>.md
type: plan
status: completed
branch: feat/build-audit-subagent
pr: TBD
related:
  - docs/plans/2026-04-10-roadmap-v036-v039.plan.md
  - docs/context/skill-mcp-tool-subagent-taxonomy.context.md
  - docs/context/tool-description-quality-and-consolidation.context.md
  - docs/context/multi-agent-orchestration-patterns-and-selection-criteria.context.md
  - docs/context/production-reliability-gap-and-multi-agent-failures.context.md
  - docs/context/agentic-fault-taxonomy-and-interface-mismatch-pattern.context.md
---

# build-subagent + audit-subagent Skills

**Goal:** Deliver two new skills — `/wos:build-subagent` and `/wos:audit-subagent` — that apply the same scaffolding and quality-audit discipline to Claude Code custom subagents that the wider build/audit family applies to skills, rules, commands, and hooks. The primary risk this addresses is over-permissioned subagents: agents with broad tool sets that exceed their described capability scope.

**Scope:**

Must have:
- `skills/build-subagent/SKILL.md` — guided intake workflow that produces a valid `.claude/agents/<name>.md`
- `skills/audit-subagent/SKILL.md` — scan-and-check workflow that produces structured findings (file, issue, severity)
- Both skills pass `python scripts/lint.py --root . --no-urls` with no new failures or warnings
- `## Handoff` section in both skills (Receives / Produces / Chainable-to)
- Roadmap Task 13 checkbox updated on PR merge

Won't have:
- `wos/subagent.py` Python validator or `scripts/lint.py` auto-detection (pure skill-layer, no tooling)
- Tests (skill quality is verified by lint checks, not unit tests)
- Changes to existing skills
- References subdirectories — both SKILL.md files stand alone

**Approach:** Both skills are pure LLM instruction documents (no scripts, no Python code). `build-subagent` follows the same guided-intake pattern used by `build-rule` and `build-skill` (issues #226, #227), but adds an upfront justification gate: the skill must verify a single agent with tools does not suffice before scaffolding (grounded in `skill-mcp-tool-subagent-taxonomy` — subagents are high-cost context forks, not a default primitive). Workflow: justify → elicit → least-privilege → overlap check → draft → approval → write. `audit-subagent` follows the same scan-and-report pattern: discover → run seven named checks → emit findings sorted by severity. Audit checks are grounded in three context files: tool-description-quality (description quality criteria), production-reliability-gap (41–86% multi-agent failure rates, context loss at handoffs), and agentic-fault-taxonomy (termination failure as a top cognitive fault). The agent definition output format (`.claude/agents/<name>.md`) mirrors the WOS document model: YAML frontmatter + structured markdown body.

**File Changes:**
- Create: `skills/build-subagent/SKILL.md`
- Create: `skills/audit-subagent/SKILL.md`
- Modify: `docs/plans/2026-04-10-roadmap-v036-v039.plan.md` (Task 13 checkbox on merge)

**Branch:** `feat/build-audit-subagent`
**PR:** TBD

---

## Task 1: Create `skills/build-subagent/SKILL.md`

**Files:**
- Create: `skills/build-subagent/SKILL.md`

- [x] **Step 1:** Create the file `skills/build-subagent/SKILL.md` with the following frontmatter and content. <!-- sha:6125f82 -->

  **Frontmatter:**
  ```yaml
  name: build-subagent
  description: >
    Scaffolds a new Claude Code custom subagent definition in
    .claude/agents/<name>.md. Guides intake, applies least-privilege to
    tool selection, checks for overlap with existing skills and agents,
    and writes the definition file. Use when the user wants to "create
    a subagent", "add a subagent", "build an agent", "scaffold an agent",
    or "make a custom agent".
  argument-hint: "[subagent name or description]"
  user-invocable: true
  ```

  **Workflow the SKILL.md must describe (7 steps):**

  1. **Justify the subagent** — before any intake, ask: does this need to be a subagent, or would a skill or a single agent with tools suffice? A subagent is justified only when at least one of these conditions holds:
     - The task is genuinely isolated and the context window cost of a full fork is justified by parallelism or scope
     - The task requires tool access or permissions the parent agent should not hold
     - The task is large enough that running it in-context would degrade the parent's reasoning

     If none of these apply, recommend a skill instead and explain why. Do not proceed to intake until the user confirms a subagent is the right primitive. (Grounding: subagents are high-cost context forks; single agents with tools frequently match or outperform multi-agent architectures — `skill-mcp-tool-subagent-taxonomy.context.md`, `production-reliability-gap-and-multi-agent-failures.context.md`.)

  2. **Elicit** — gather the four required inputs one at a time:
     - Name (slug-form, lowercase-hyphenated, no spaces)
     - Description (one sentence used for routing — what problem does this agent solve, and when should Claude invoke it over a skill?)
     - Primary capability (what workflow does this agent execute?)
     - Tool requirements (what does the agent need to do its job?)

  3. **Apply least-privilege** — for each tool the user requests, ask: does the agent's described workflow *require* this tool, or is it "nice to have"? Propose the minimal set. For tools not requested but likely needed, suggest them and explain why. For any tool not justified by the workflow description, explicitly exclude it with a note.
     Common over-permissioning traps to check: adding `Bash` when only file reads are needed; adding `Write`/`Edit` when the agent only produces reports; adding `WebFetch`/`WebSearch` for internal-only workflows.

  4. **Check for overlap** — scan `.claude/agents/` for existing agent definitions and `skills/` for existing skills. If the proposed subagent duplicates an existing skill's capability, flag it: "A skill already does this — would a subagent add value here?" Present overlap findings before drafting.

  5. **Draft definition** — produce a `.claude/agents/<name>.md` draft using this format:

     ```markdown
     ---
     name: <slug>
     description: <one-sentence routing description>
     tools:
       - <Tool1>
       - <Tool2>
     ---

     # <Display Name>

     <2–3 sentence capability description. What this agent does, what it produces, when to use it.>

     ## When to invoke

     <Specific trigger conditions — name the problem, not just the action. What makes this the right agent over a skill? Include 1-2 example requests that should route here. Include at least one example of what should NOT route here.>

     ## Workflow

     <Numbered steps describing the agent's execution pattern. Last step must be an explicit completion condition: what does "done" look like and what does the agent return to the parent?>

     ## Handoff

     **Receives:** <specific inputs from parent — name the data, not just the category>
     **Produces:** <specific outputs returned to parent — format, location, or structure>
     **Returns to:** <parent agent or orchestrator>
     ```

  6. **Present for approval** — show the draft and wait for explicit user confirmation before writing any file. Do not write until approved.

  7. **Write the file** — write to `.claude/agents/<name>.md`. Confirm file written and provide the path.

  **Anti-pattern guards to include in the SKILL.md:**
  - Over-permissioning: requesting all tools "to be safe" without per-tool justification
  - Under-permissioning: missing tools the workflow description requires (e.g., no `Read` for a file-analysis agent)
  - Vague descriptions: descriptions that do not specify *when* to invoke (prevents correct routing)
  - Skill duplication: a subagent that replicates an existing skill with no added parallelism or isolation benefit
  - Missing handoff contract: no `## Handoff` section means the agent cannot participate in chain design or audit-chain verification

  **Handoff section to include:**
  ```
  ## Handoff

  **Receives:** Subagent name, description, primary capability, and initial tool requirements from user
  **Produces:** .claude/agents/<name>.md definition file with validated frontmatter, capability description, and handoff contract
  **Chainable to:** audit-subagent
  ```

- [x] **Step 2:** Verify file created: `test -f skills/build-subagent/SKILL.md && echo "ok"` <!-- sha:6125f82 -->
- [x] **Step 3:** Verify no lint failures: `python scripts/lint.py --root . --no-urls 2>&1 | grep -A2 "build-subagent"` — no `[fail]` entries <!-- sha:6125f82 -->
- [x] **Step 4:** Commit: `git commit -m "feat: add /wos:build-subagent skill"` <!-- sha:6125f82 -->

---

## Task 2: Create `skills/audit-subagent/SKILL.md`

**Files:**
- Create: `skills/audit-subagent/SKILL.md`

- [x] **Step 1:** Create the file `skills/audit-subagent/SKILL.md` with the following frontmatter and content. <!-- sha:2bad11a -->

  **Frontmatter:**
  ```yaml
  name: audit-subagent
  description: >
    Audits Claude Code custom subagent definitions in .claude/agents/.
    Detects over-permissioned tool sets, unclear routing descriptions,
    incomplete handoff contracts, and overlap with existing skills. Use
    when the user wants to "audit subagents", "check my agents", "review
    agent permissions", "validate my agents directory", or "are my agents
    well-formed".
  argument-hint: "[path to agent file (optional; defaults to scanning .claude/agents/)]"
  user-invocable: true
  ```

  **Workflow the SKILL.md must describe (4 steps):**

  1. **Discover** — if an argument is provided, audit only that file. Otherwise scan `.claude/agents/` recursively for `.md` files. If the directory does not exist or is empty, report "No subagent definitions found at `.claude/agents/`" and exit.

  2. **Run seven checks on each definition:**

     | Check | What to look for | Severity | Grounding |
     |-------|-----------------|----------|-----------|
     | **Tool over-permissioning** | Tool set includes capabilities not supported by the description (e.g., `Bash` on a read-only analysis agent; `Write`+`Edit` on a reporting agent) | warn | skill-mcp-tool-subagent-taxonomy |
     | **Tool under-permissioning** | Description implies capabilities not covered by the tool set (e.g., "writes files" but no `Write` tool) | warn | skill-mcp-tool-subagent-taxonomy |
     | **Description quality** | Description fails to cover: what it does, when to invoke it, when NOT to invoke it, what it returns. A one-liner with no exclusions and no output format is always insufficient. | warn | tool-description-quality-and-consolidation |
     | **Handoff contract completeness** | Missing `## Handoff` section (warn); or section present but `**Receives:**`/`**Produces:**`/`**Returns to:**` contain placeholder text or are empty (fail). Context loss at handoffs is the #2 production failure mode. | warn/fail | production-reliability-gap |
     | **Termination conditions** | Workflow section has no explicit completion condition — no step that describes what "done" looks like or what the agent returns to the parent. Agents without stopping conditions are a top cognitive fault. | warn | agentic-fault-taxonomy |
     | **Context cost justified** | Subagent's described scope is narrow enough that a skill or inline execution would suffice — no evidence of parallelism, isolation, or context-window pressure that justifies a full context fork | warn | skill-mcp-tool-subagent-taxonomy |
     | **Skill overlap** | Agent's described capability matches an existing skill in `skills/` with no added parallelism, isolation, or tool access the skill cannot provide | warn | skill-mcp-tool-subagent-taxonomy |

     **Over-permissioning heuristics to include:**
     - More than 6 tools for a narrowly-scoped agent (description covers one workflow step) → flag
     - `Agent` tool present without evidence the agent orchestrates other agents → flag
     - `Bash` without a description that involves command execution → flag
     - `WebFetch`/`WebSearch` without a description involving external information retrieval → flag

  3. **Emit findings** — output in the same format as `scripts/lint.py`:
     ```
     [severity] path/to/file.md — description of issue
     ```
     Group by file; sort fail before warn within each file. If no issues found for an agent, output: `[ok] path/to/file.md — well-formed`.

  4. **Summarize** — after all findings, print a summary: total agents audited, total issues (N fail, N warn), and one-sentence recommendation if issues found.

  **Handoff section to include:**
  ```
  ## Handoff

  **Receives:** Path to a specific agent definition, or defaults to scanning .claude/agents/
  **Produces:** Structured audit findings (file, issue, severity) sorted by severity; summary with issue counts
  **Chainable to:** build-subagent (to scaffold replacements), audit (wos:audit orchestrator in v0.39.0)
  ```

- [x] **Step 2:** Verify file created: `test -f skills/audit-subagent/SKILL.md && echo "ok"` <!-- sha:2bad11a -->
- [x] **Step 3:** Verify no lint failures: `python scripts/lint.py --root . --no-urls 2>&1 | grep -A2 "audit-subagent"` — no `[fail]` entries <!-- sha:2bad11a -->
- [x] **Step 4:** Commit: `git commit -m "feat: add /wos:audit-subagent skill"` <!-- sha:2bad11a -->

---

## Task 3: Full quality check and index sync

**Files:**
- None (verification only)

- [x] **Step 1:** Run full lint: `python scripts/lint.py --root . --no-urls` → zero `[fail]` entries; any new `[warn]` entries are reviewed and understood (not silently accepted) <!-- sha:8a33a32 -->
- [x] **Step 2:** Verify Handoff sections present in both new skills:
  `grep -c "## Handoff" skills/build-subagent/SKILL.md skills/audit-subagent/SKILL.md` → both > 0 <!-- sha:8a33a32 -->
- [x] **Step 3:** Verify SKILL.md bodies are within the 500-line threshold:
  `wc -l skills/build-subagent/SKILL.md skills/audit-subagent/SKILL.md` → 179 and 180 lines, both under 500 <!-- sha:8a33a32 -->
- [x] **Step 4:** Reindex if needed: `python scripts/reindex.py --root .` → 5 files written <!-- sha:8a33a32 -->
- [x] **Step 5:** Run tests: `python -m pytest tests/ -v` → 415 passed, zero failures <!-- sha:8a33a32 -->
- [x] **Step 6:** Commit any reindex changes: `git commit -m "chore: reindex after build/audit-subagent addition"` <!-- sha:8a33a32 -->

---

## Task 4: Update roadmap on merge

**Files:**
- Modify: `docs/plans/2026-04-10-roadmap-v036-v039.plan.md`

- [ ] **Step 1:** After the PR for `feat/build-audit-subagent` is merged, note the merge commit SHA.
- [ ] **Step 2:** In `docs/plans/2026-04-10-roadmap-v036-v039.plan.md`, update Task 13 from:
  `- [ ] Task 13: Implement #228 — ...`
  to:
  `- [x] Task 13: Implement #228 — skills/build-subagent/SKILL.md, skills/audit-subagent/SKILL.md <!-- sha:<merge-sha> -->`
- [ ] **Step 3:** Commit on main: `git commit -m "chore: mark roadmap Task 13 complete (sha:<merge-sha>)"`

---

## Validation

- [ ] `test -f skills/build-subagent/SKILL.md && test -f skills/audit-subagent/SKILL.md && echo "both exist"` — prints `both exist`
- [ ] `grep -L "## Handoff" skills/build-subagent/SKILL.md skills/audit-subagent/SKILL.md` — empty output (both have Handoff sections)
- [ ] `python scripts/lint.py --root . --no-urls` — no `[fail]` entries for new or existing files
- [ ] `python -m pytest tests/ -v` — zero failures
- [ ] `wc -l skills/build-subagent/SKILL.md skills/audit-subagent/SKILL.md` — both files under 500 lines

## Notes

- No Python code changes are needed. This is a skill-layer-only implementation — pure LLM instruction documents.
- The `.claude/agents/<name>.md` format described in build-subagent is the canonical Claude Code subagent definition format. It must include YAML frontmatter with `name`, `description`, and `tools` fields.
- Both skills are isolated to their own directories with no file overlap with other open tasks (Tasks 9, 10, 12, 14, 15 in the roadmap). This worktree can run in parallel with all of them.
- Task 4 (roadmap update) happens after PR merge, not during branch execution. It is a main-branch commit, not part of the feature branch.
