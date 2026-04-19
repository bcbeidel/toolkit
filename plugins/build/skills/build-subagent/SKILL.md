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
references:
  - ../../_shared/references/primitive-routing.md
---

# Build Subagent

Scaffold a new Claude Code custom subagent definition with correct
structure, least-privilege tool selection, and a complete handoff contract.
The output is a `.claude/agents/<name>.md` file — not code, not a plan.

**Announce at start:** "I'm using the build-subagent skill to scaffold this agent."

## Workflow

### 1. Justify the Subagent

Before any intake, confirm a subagent is the right primitive. Full decision matrix: [primitive-routing.md](../../_shared/references/primitive-routing.md).

A subagent is a full context fork — high cost, separate context window. Ask: "Before we build this, is a subagent the right choice here?"

A subagent is justified only when at least one holds:
- **Parallelism or scope** — task is genuinely isolated; context fork cost is justified by workstream size or parallel execution
- **Permission isolation** — task requires tool access or permissions the parent agent should not hold
- **Context pressure** — intermediate work (search results, large file reads) is large enough to degrade the parent's reasoning quality

If none apply, recommend a skill instead:

> "A skill may be more appropriate here — lower overhead, same-context execution, no fork required. Use `/build:build-skill` instead?"

Do not proceed to intake until the user confirms a subagent is the right primitive.

### 2. Elicit Requirements

If `$ARGUMENTS` is non-empty, seed the intake from it: treat the first token
as the proposed name and the remainder as the capability description, then
confirm with the user before moving on.

Gather four inputs, one at a time:

1. **Name** — slug form: lowercase, hyphen-separated, no spaces
   (e.g., `data-analyst`, `doc-reviewer`)
2. **Description** — one sentence used for routing. Prompt: "What problem
   does this agent solve, and when should Claude invoke it instead of a skill?"
3. **Primary capability** — what workflow does the agent execute, start to
   finish? What does it produce?
4. **Tool requirements** — what does the agent need to do its job?

### 3. Apply Least-Privilege

#### Tool selection — always

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
- `Agent` listed in tools for a **subagent-scoped** definition — subagents
  cannot spawn other subagents; the Agent tool is filtered out at the
  platform level. Listing it has no effect. Exception: the `Agent` and
  `Agent(worker, researcher)` syntax *is* meaningful when the definition
  is intended to run as the *main thread* via `claude --agent <name>` (spec
  documents this path explicitly). Flag only for subagent-scoped use.

**`tools` allowlist vs `disallowedTools` denylist:**
Use `tools` when the agent needs only a small, specific set. Use
`disallowedTools` when the agent should inherit most tools but block
specific ones. If both are set, `disallowedTools` is applied first.

#### Advanced configuration — conditional

Do not present these as a menu. Surface each only when the described
workflow signals it:

**`permissionMode`** — raise only when the agent's risk profile differs from
the parent session (read-only exploration, auto-accepting edits, etc.). Spec
values:
- `default`: standard permission checking with prompts
- `acceptEdits`: auto-accepts file edits and common filesystem commands for
  paths in the working directory or `additionalDirectories`
- `auto`: background classifier reviews commands and protected-directory writes
- `dontAsk`: auto-denies permission prompts (explicitly allowed tools still work)
- `bypassPermissions`: skips permission prompts (use with caution)
- `plan`: plan mode (read-only exploration)

Parent-session precedence rules (spec):
- If the parent uses `bypassPermissions` **or `acceptEdits`**, that takes
  precedence and the subagent's `permissionMode` is ignored.
- If the parent uses `auto` mode, the subagent inherits auto mode and its own
  `permissionMode` is ignored; the parent's classifier evaluates each tool call.
- Plugin subagents have `permissionMode`, `hooks`, and `mcpServers` silently
  ignored regardless of value (spec: security-scoped plugin restriction).

**`maxTurns`** — raise only if the workflow is multi-step or recursive:
> "This workflow has several steps — add `maxTurns: N` as a safety net.
> Agents without a turn limit can loop indefinitely on unexpected input."

**`background`** — raise only if parallelism was cited as the justification
in Step 1:
> "Since parallelism is the reason for this subagent, `background: true`
> lets it run concurrently while the parent continues."

**`isolation: worktree`** — **required** when `background: true` is set AND
the effective tool set includes `Write` or `Edit`. Also recommended when
the agent makes changes to versioned files that require a clean working
copy. This mirrors check-subagent #11: background agents with write access
and no worktree isolation are a flagged warn because parallel writes on
shared files conflict. Surface this to the user:
> "Since this agent modifies files in parallel, `isolation: worktree` gives
> it a clean working copy to prevent write conflicts. Without it,
> check-subagent will flag this combination."

**`skills`** — raise only if the workflow implies needing project-specific
context or toolkit procedures:
> "Parent session skills aren't inherited. If this agent needs [skill]
> procedures, list it explicitly in the `skills` field."

**`mcpServers`** — raise when the subagent needs MCP access the parent
doesn't have, or when you want to keep an MCP server's tool descriptions
out of the parent conversation's token budget:
> "The `mcpServers` field scopes MCP servers to this subagent. Inline
> definitions connect at start and disconnect at finish; string references
> reuse the parent session's connection. Defining a server here instead of
> in `.mcp.json` keeps its tool descriptions out of the parent context."

**`memory`** — raise only if the user wants the subagent to accumulate
knowledge across sessions (codebase patterns, recurring issues, debugging
insights):
> "Setting `memory: project` (or `user`/`local`) gives this subagent a
> persistent directory. Heads-up: enabling memory auto-grants Read/Write/Edit
> regardless of the `tools` field, so the subagent can manage its memory
> files. If you specified a narrow `tools` allowlist, memory will expand it."

Scope choices: `user` (`~/.claude/agent-memory/<name>/`), `project`
(`.claude/agent-memory/<name>/` — shareable via version control, recommended
default), `local` (`.claude/agent-memory-local/<name>/` — not checked in).

**Portability** — raise only if the user mentions Copilot, Cursor, or
cross-platform use:

| Platform | Compatibility | What transfers |
|---|---|---|
| Cursor | Direct — reads `.claude/agents/` natively | All fields; unknown fields ignored |
| GitHub Copilot | Structural — move to `.github/agents/<name>.md` | `name`, `description`, Markdown body; Claude Code-specific fields stripped |
| Codex CLI | Format conversion required | Rebuild as TOML in `.codex/agents/` |
| Windsurf | Different primitive | Not applicable |

If Copilot compatibility is needed, avoid `permissionMode`, `maxTurns`,
`background`, `isolation`, `memory`, and `hooks`.

### 4. Check for Overlap

Scan for conflicts before drafting:

1. Read `.claude/agents/` — list existing agent definitions
2. Read `skills/` — list existing skills

If the proposed capability duplicates an existing skill or agent, flag it:

> "The `research` skill already covers this workflow. Would a subagent
> add parallelism or isolation that the skill can't provide?"

Present overlap findings and confirm with the user before proceeding.

### 5. Draft the Definition

Produce a `.claude/agents/<name>.md` draft using only the fields confirmed
in Steps 2 and 3. Start from the minimum and add only what applies:

```markdown
---
name: <slug>
description: <routing description — write as a routing rule, not a capability summary>
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
Required: 1–2 example requests that SHOULD route here.
Required: at least one example that should NOT (routes to a skill
instead, or is handled inline). The negative case is what disambiguates
this agent from adjacent routing targets and is checked by
check-subagent #3.>

## Workflow

<Numbered steps describing the agent's execution pattern.
The final step must state an explicit completion condition:
what "done" looks like and what the agent returns to the parent.
See check-subagent #5 — agents without a completion condition AND
without `maxTurns` are flagged as runaway risks.>

## Handoff

**Receives:** <concrete input descriptor — e.g., "list of failing test
names and their error messages", not "test results". Generic category
descriptors are flagged by check-subagent #4.>
**Produces:** <concrete output descriptor — format, file path, or
structure the downstream consumer can parse, e.g., "Markdown report at
`.research/<slug>.research.md` with Claims table, Sources table, and
Findings sections">
**Returns to:** <parent agent or orchestrator name>
```

Add fields only when they were raised and confirmed in Step 3:

| Field | Add when |
|---|---|
| `disallowedTools` | denylist approach was chosen over allowlist |
| `model` | specific model was justified for this workflow |
| `permissionMode` | agent's risk profile differs from the parent session (see Step 3 for the 6 spec values) |
| `maxTurns` | multi-step or recursive workflow |
| `background` | parallelism was the Step 1 justification |
| `isolation: worktree` | **required** when `background: true` AND effective tools include `Write` or `Edit`; also recommended when modifying versioned files that require a clean working copy |
| `skills` | workflow needs project-specific procedures |

Do not include fields that were not discussed. Do not include commented-out
placeholders. The output file contains only what applies.

**Description quality checklist** — before presenting for approval, verify
the description covers:

- What the agent does (primary function)
- When to invoke it (specific trigger conditions, written as routing rules)
- When NOT to invoke it (at least one exclusion)
- What it returns (output format or location)
- "use proactively" — include this phrase if the agent should be invoked automatically without being asked

A one-liner with no exclusions and no output format is insufficient. A description that reads as a capability summary rather than a routing rule will produce unreliable auto-delegation. Keep the total description under 1,024 characters — descriptions exceeding this limit are silently truncated without warning.

**Skills are not inherited.** The parent session's active skills do not carry over to subagents. If the workflow requires project-specific procedures, list them explicitly in the `skills` field. If omitted, the subagent starts with no skill context beyond its own system prompt.

### 6. Narrate the Draft

Before asking for approval, walk the user through the key design choices in
3–6 bullets. Cover:

- **Frontmatter choices** — explain any non-default field settings and why.
  Name the field *and* the reasoning: "I set `permissionMode: acceptEdits`
  because this agent auto-applies linter fixes — interactive prompts would
  defeat the point."
- **Structure choices** — why the workflow is ordered the way it is, where
  gate checks are placed and what they guard, and how prescriptive vs.
  flexible each step is.
- **Patterns applied** — call out `isolation: worktree`, `background: true`,
  `memory: project`, `mcpServers` scoping, or other patterns you used.
- **What you didn't use and why** — briefly note patterns you considered
  but skipped (e.g., "I didn't set `maxTurns` because the workflow has one
  step; if we add retry logic, we should add it then"). This is often the
  most educational part of the narration.

The goal is that a user unfamiliar with subagent authoring can read the
narration and disagree with any structural choice. If you can't explain a
choice clearly, revisit it before presenting.

### 7. WOS Quality Check

Before writing to disk, run lint and reindex on the worktree root:

```bash
python3 plugins/wiki/scripts/lint.py --root <project-root> --no-urls
python3 plugins/wiki/scripts/reindex.py --root <project-root>
```

Fix any findings surfaced by lint before writing. `reindex.py` updates
`_index.md` navigation so the new agent is discoverable.

### 8. Present for Approval

Show the complete draft and the narration together. Wait for explicit user
confirmation before writing any file. If the user requests changes, revise
and re-present.

Do not write the file until approved.

### 9. Write the File and Audit

Write to `.claude/agents/<name>.md`. Confirm the path and that the file
was written.

After writing, invoke `check-subagent` on the new file — surface any findings
and offer the repair loop before moving on. build-subagent must produce
definitions that pass the checks it enforces downstream.

## Key Instructions

- **Won't write the definition file until the user explicitly approves the draft** — Step 8 is a hard gate; no file is written before it passes
- **Won't proceed to intake if a skill would suffice** — Step 1 justification check is mandatory; redirect to `/build:build-skill` if none of the three justification conditions hold

## Anti-Pattern Guards

- **Over-permissioning** — requesting tools "to be safe" without per-tool
  justification. Every tool must be required by the workflow description.
- **Under-permissioning** — missing tools the workflow actually requires
  (e.g., no `Read` for a file-analysis agent, no `Bash` for a code executor).
- **`Agent` tool listed in subagent tools** — subagents cannot spawn other
  subagents; the Agent tool is filtered out at the platform level. Listing it
  has no effect and misleads readers.
- **Vague description** — a description that reads as a capability summary
  rather than a routing rule will produce unreliable auto-delegation. Route
  ambiguity causes missed invocations and incorrect handoffs.
- **Relying on auto-delegation** — auto-delegation by description matching is
  documented but frequently unreliable in practice. Design workflows around
  explicit invocation (@-mention). Do not tell users their agent "will
  automatically run" — it may not.
- **Missing `maxTurns` on complex workflows** — agents with multi-step or
  recursive patterns and no turn limit can loop indefinitely on unexpected
  input. Add `maxTurns` as a safety net for any non-trivial workflow.
- **Skill duplication** — a subagent that replicates an existing skill with
  no parallelism, isolation, or permission benefit. Use a skill instead.
- **Missing completion condition** — a workflow with no explicit final step
  describing what "done" looks like. Agents without stopping conditions fail
  in production.
- **Missing handoff contract** — no `## Handoff` section means the agent
  cannot participate in skill-chain design or `check-skill-chain` verification.

## Handoff

**Receives:** Subagent name, description, primary capability, and initial
tool requirements from user
**Produces:** `.claude/agents/<name>.md` definition file with validated
frontmatter, capability description, when-to-invoke guidance, workflow with
completion condition, and handoff contract
**Chainable to:** check-subagent
