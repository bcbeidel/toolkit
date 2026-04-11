---
name: build-subagent
description: >
  Scaffolds a new Claude Code custom subagent definition in the
  .claude/agents/ directory. Guides intake, applies least-privilege to
  tool selection, checks for overlap with existing skills and agents,
  and writes the definition file. Use when the user wants to "create
  a subagent", "add a subagent", "build an agent", "scaffold an agent",
  or "make a custom agent".
argument-hint: "[subagent name or description]"
user-invocable: true
---

# Build Subagent

Scaffold a new Claude Code custom subagent definition with correct
structure, least-privilege tool selection, and a complete handoff contract.
The output is a `.claude/agents/<name>.md` file — not code, not a plan.

**Announce at start:** "I'm using the build-subagent skill to scaffold this agent."

## Workflow

### 1. Justify the Subagent

Before any intake, assess whether a subagent is the right primitive.
A subagent is a full context fork — high cost, separate context window.
Ask the user: "Before we build this, let me check — is a subagent the right
choice here?"

A subagent is justified only when at least one of these conditions holds:

- **Parallelism or scope** — the task is genuinely isolated and the context
  window cost of a full fork is justified by parallel workstreams or large scope
- **Permission isolation** — the task requires tool access or permissions the
  parent agent should not hold
- **Context pressure** — the task is large enough that running it in-context
  would degrade the parent's reasoning quality

If none apply, recommend a skill instead:

> "A skill may be more appropriate here — it has lower overhead and handles
> procedural workflows without a context fork. Would you like to use
> `/wos:build-skill` instead?"

Do not proceed to intake until the user confirms a subagent is the right
primitive.

### 2. Elicit Requirements

Gather four inputs, one at a time:

1. **Name** — slug form: lowercase, hyphen-separated, no spaces
   (e.g., `data-analyst`, `doc-reviewer`)
2. **Description** — one sentence used for routing. Prompt: "What problem
   does this agent solve, and when should Claude invoke it instead of a skill?"
3. **Primary capability** — what workflow does the agent execute, start to
   finish? What does it produce?
4. **Tool requirements** — what does the agent need to do its job?

### 3. Apply Least-Privilege

For each tool the user requests, verify: does the workflow *require* this
tool, or is it "nice to have"?

Propose the minimal justified set. For each exclusion, explain why:

> "`Write` isn't needed — this agent reads and reports, it doesn't modify files."

For tools not requested but clearly needed, suggest them and explain why:

> "You'll need `Read` to inspect files, but I don't see it in your list."

**Common over-permissioning traps:**

- `Bash` when only file reads are needed
- `Write`/`Edit` when the agent only produces reports
- `WebFetch`/`WebSearch` for internal-only workflows
- `Agent` when the agent doesn't orchestrate sub-agents

### 4. Check for Overlap

Scan for conflicts before drafting:

1. Read `.claude/agents/` — list existing agent definitions
2. Read `skills/` — list existing skills

If the proposed capability duplicates an existing skill or agent, flag it:

> "The `research` skill already covers this workflow. Would a subagent
> add parallelism or isolation that the skill can't provide?"

Present overlap findings and confirm with the user before proceeding.

### 5. Draft the Definition

Produce a `.claude/agents/<name>.md` draft:

```markdown
---
name: <slug>
description: <one-sentence routing description>
tools:
  - <Tool1>
  - <Tool2>
---

# <Display Name>

<2–3 sentence capability description: what this agent does, what it
produces, when to use it.>

## When to invoke

<Specific trigger conditions — name the problem, not just the action.
What makes this the right agent over a skill or inline execution?
Include 1-2 example requests that SHOULD route here.
Include at least one example that should NOT (routes to a skill instead).>

## Workflow

<Numbered steps describing the agent's execution pattern.
The final step must state an explicit completion condition:
what "done" looks like and what the agent returns to the parent.>

## Handoff

**Receives:** <specific inputs from parent — name the data, not the category>
**Produces:** <specific outputs returned to parent — format, location, or structure>
**Returns to:** <parent agent or orchestrator>
```

**Description quality checklist** — before presenting for approval, verify
the description covers:

- What the agent does (primary function)
- When to invoke it (specific trigger conditions)
- When NOT to invoke it (at least one exclusion)
- What it returns (output format or location)

A one-liner with no exclusions and no output format is insufficient.

### 6. Present for Approval

Show the complete draft. Wait for explicit user confirmation before writing
any file. If the user requests changes, revise and re-present.

Do not write the file until approved.

### 7. Write the File

Write to `.claude/agents/<name>.md`. Confirm the path and that the file
was written.

## Anti-Pattern Guards

- **Over-permissioning** — requesting tools "to be safe" without per-tool
  justification. Every tool must be required by the workflow description.
- **Under-permissioning** — missing tools the workflow actually requires
  (e.g., no `Read` for a file-analysis agent, no `Bash` for a code executor).
- **Vague description** — a description that doesn't specify when to invoke
  prevents correct routing. Route ambiguity causes missed invocations and
  incorrect handoffs.
- **Skill duplication** — a subagent that replicates an existing skill with
  no parallelism, isolation, or permission benefit. Use a skill instead.
- **Missing completion condition** — a workflow with no explicit final step
  describing what "done" looks like. Agents without stopping conditions fail
  in production.
- **Missing handoff contract** — no `## Handoff` section means the agent
  cannot participate in chain design or `audit-chain` verification.

## Handoff

**Receives:** Subagent name, description, primary capability, and initial
tool requirements from user
**Produces:** `.claude/agents/<name>.md` definition file with validated
frontmatter, capability description, when-to-invoke guidance, workflow with
completion condition, and handoff contract
**Chainable to:** audit-subagent
