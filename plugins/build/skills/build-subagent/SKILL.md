---
name: build-subagent
description: >
  Scaffolds a Claude Code custom subagent definition — a `.md` file
  under `.claude/agents/` with a routing-oriented description, an
  explicit `tools` allowlist sized to the workflow, a bounded system
  prompt in the markdown body, and explicit failure behavior. Use when
  the user wants to "create a subagent", "add a subagent", "build an
  agent", "scaffold an agent", or "make a custom agent". Not for
  skills (route to `/build:build-skill`), hooks (route to
  `/build:build-hook`), or rules (route to `/build:build-rule`).
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebFetch, WebSearch
argument-hint: "[name or intent]"
user-invocable: true
references:
  - ../../_shared/references/subagent-best-practices.md
  - ../../_shared/references/primitive-routing.md
license: MIT
---

# Build Subagent

Scaffold a Claude Code custom subagent definition: a single `.md` file
in `.claude/agents/` (project) or `~/.claude/agents/` (user) that the
routing agent can delegate to with confidence. The authoring rubric —
what a good subagent does, the file anatomy, the patterns that work —
lives in
[subagent-best-practices.md](../../_shared/references/subagent-best-practices.md).
This skill is the workflow; the principles doc is the rubric.

A subagent is a **full context fork** — high-cost compared to a skill
(same-context execution) or an inline tool call. The first question
every intake answers is whether a subagent is even the right primitive.

**Workflow sequence:** 1. Route → 2. Scope Gate → 3. Elicit →
4. Draft → 5. Safety Check → 6. Review Gate → 7. Save → 8. Test

## 1. Route

Confirm a subagent is the right primitive before asking scaffold
questions.

**Wrong primitive:**

- **Reusable recipe the parent agent runs inline** → `/build:build-skill`.
  Skills execute in the parent context; no fork cost.
- **Event-triggered quality gate** (PreToolUse, SessionStart, Stop, etc.)
  → `/build:build-hook`. Hooks have a `settings.json` registration and
  a lifecycle a subagent does not express.
- **Semantic judgment captured as an LLM-evaluated rule** →
  `/build:build-rule`.
- **Standalone CLI tool** → `/build:build-bash-script` or
  `/build:build-python-script`.

The full primitive-selection decision lives in
[primitive-routing.md](../../_shared/references/primitive-routing.md).

**Right primitive** — proceed to Scope Gate only when at least one
subagent-specific justification holds:

- **Parallelism or scope** — the task is genuinely isolated and the
  context-fork cost is justified by workstream size, or multiple
  instances will run concurrently.
- **Permission isolation** — the task needs tool access or a
  `permissionMode` the parent should not hold.
- **Context pressure** — intermediate work (large file reads, search
  output) would degrade the parent's reasoning quality.

If none hold, recommend a skill instead and stop:

> "A skill fits this better — same-context execution, no fork cost.
> Use `/build:build-skill` instead?"

## 2. Scope Gate

Refuse to scaffold — and recommend an alternative — when the request
signals subagent is the wrong choice. Probe for:

1. **Recreating an existing skill's behavior** with no parallelism,
   isolation, or permission-scope benefit. Subagents that duplicate
   skills are cost multipliers without upside.
2. **Workflow wants shell execution the parent already allows** — no
   isolation benefit; use a skill.
3. **Running as main thread via `claude --agent <name>`** — a
   different authoring surface than subagent delegation. The
   `tools` / `Agent(<type>)` semantics differ; flag and confirm the
   user wants the subagent (delegated) path, not the main-thread path.

If a signal fires, state it, name the alternative, and stop.

## 3. Elicit

If `$ARGUMENTS` is non-empty, seed the intake: first token is the
proposed name, remainder is the capability description. Confirm both
before moving on.

Gather inputs one at a time:

**1. Name** — kebab-case, lowercase, hyphen-separated, descriptive of
the primary role (`typescript-linter`, `migration-reviewer`). Not
generic (`agent`, `helper`). The filename stem must equal the `name`.

**2. Description** — the routing contract. Write it for the routing
agent, not a human reader. Structure:

- Start with a verb phrase naming the capability ("Lints staged
  TypeScript files…", "Reviews database migrations for…").
- State **trigger conditions** explicitly ("use after editing `.ts`
  files", "when the user asks to check migration safety").
- Name at least one **exclusion** ("not for JavaScript files", "not
  for production schema changes").
- Mention what the agent **returns** (format or location).
- If the agent should self-invoke without explicit mention, include
  "use proactively" or equivalent routing language.

Keep the total under **1,024 characters** — descriptions exceeding this
limit are silently truncated by Claude Code without warning.

**3. Primary capability + workflow** — what does the agent do, start
to finish? What artifact does it produce? Every workflow has an
explicit completion condition — "done" must be describable.

**4. Tool requirements** — what does the agent need to do its job? For
each proposed tool, verify the workflow requires it. Apply
least-privilege in step 3 of Draft; surface over-/under-requests now
only to clarify scope.

**5. Advanced fields** — surface each only when the workflow signals
it; do not present as a menu.

- **`permissionMode`** — only when the agent's risk profile differs
  from the parent. Six spec values: `default`, `acceptEdits`, `auto`,
  `dontAsk`, `bypassPermissions`, `plan`.
  - Parent precedence: if parent uses `bypassPermissions`,
    `acceptEdits`, or `auto`, the subagent's `permissionMode` is
    overridden at runtime.
  - **Plugin-scope restriction:** for subagents loaded from a plugin
    directory (`plugins/<plugin>/agents/`), `permissionMode`, `hooks`,
    and `mcpServers` are silently ignored.
- **`maxTurns`** — multi-step or recursive workflows; safety net
  against runaway loops. Add alongside (not instead of) a workflow
  completion condition.
- **`background: true`** — only when parallelism was the Step 1
  justification.
- **`isolation: worktree`** — **required** when `background: true`
  AND effective tools include `Write` or `Edit`. Parallel writes on
  shared files conflict without worktree isolation.
- **`skills`** — parent session skills are **not** inherited. List
  explicitly if the workflow needs project-specific procedures.
- **`memory: user | project | local`** — enables a persistent memory
  directory. **Side effect:** auto-grants Read, Write, Edit regardless
  of the `tools` allowlist. Flag this to the user when `tools` is
  narrow.
- **`mcpServers`** — scope MCP servers to this subagent only (keeps
  server tool descriptions out of the parent's token budget). Ignored
  for plugin-scoped subagents.

## 4. Draft

Produce the subagent definition.

```markdown
---
name: <kebab-case-slug>
description: <routing-rule: verb-phrase capability + trigger conditions + exclusion + returns>
tools:
  - <Tool1>
  - <Tool2>
---

# <Display Name>

<One-line role/goal statement: "You are a ...">

## Scope

In scope: <what the agent handles>.
Out of scope: <what the agent refuses or escalates>.

## Process

1. <First step — reads inputs, validates preconditions>
2. <…>
N. <Completion condition: what "done" looks like and what the
   agent returns to the parent>

## Output

<Mandated format — JSON schema / markdown structure / named artifact
path. Downstream callers parse this; keep it machine-parsable.>

## Failure behavior

<How the agent reports blockers: bad input, missing access, ambiguous
request. Deterministic exits only — no workarounds, no flailing.>
```

**Least-privilege filter** — before locking the `tools` list:

- Every tool must be required by the described workflow. "Just in
  case" is not a justification.
- Read/report agents do not need `Write`, `Edit`, or `Bash`.
- `Bash` is the widest attack surface — grant only when shell
  execution is the core job, and enumerate allowed commands in the
  prompt body.
- `WebFetch` / `WebSearch` — internal-only workflows should not have
  these.
- **`Agent` in subagent scope** — the Agent tool is filtered out at
  the platform level for delegated subagents; listing it has no
  effect and misleads readers. Exception: `Agent(<worker>, ...)` is
  meaningful for definitions intended to run as main thread via
  `claude --agent <name>`. Flag only for subagent-scope use.

Add optional frontmatter fields only when intake surfaced them — no
placeholder or commented-out keys.

## 5. Safety Check

Before presenting for review, run the rubric checks yourself:

**Location & format.** File will save to `.claude/agents/<name>.md`
(or `~/.claude/agents/<name>.md`). Frontmatter is a `---`-delimited
YAML block. `name` and `description` are present and non-empty.

**Naming.** `name` is kebab-case. Filename stem equals `name`. Not
generic.

**Description.** Routing-rule form (verb-phrase + trigger + exclusion
+ returns). Under 1,024 characters. No duplicated trigger vocabulary
with existing siblings in `.claude/agents/` (scan the directory).

**Tools.** Effective set is declared explicitly, no wildcards.
Proportionate to the described workflow. `Agent` not listed (unless
main-thread use). When `background: true` + Write/Edit is set,
`isolation: worktree` is present. When `memory:` is set alongside a
narrow `tools` list, the user has been warned about the implicit
Read/Write/Edit grant.

**Body.** Prompt opens with a role/goal statement. Scope and
out-of-scope are explicit. A completion condition exists in the
workflow. Output format is mandated, not free-form. Failure behavior
is explicit. Voice is imperative; no hedging ("try your best", "if
possible"). Total body bounded — target ≤~1,500 tokens (~6,000
chars), hard cap ≈3,000 tokens (~12,000 chars).

**Safety.** No embedded secrets. No raw interpolation of untrusted
user input.

If any check fails, revise before presenting. The Review Gate is for
user approval, not correctness recovery.

## 6. Review Gate

Present the draft with a short narration — 3–6 bullets naming the
design choices: which tools, why; which advanced fields, why; which
considered patterns were skipped and why. A user unfamiliar with
subagent authoring should be able to disagree with any structural
choice from the narration alone.

Wait for explicit user approval before writing. If the user requests
changes, revise and re-present. Proceed to Save only on explicit
approval.

## 7. Save

Write to `.claude/agents/<name>.md` (or the plugin path when
scaffolding inside a plugin). Confirm the save path and that the file
was written.

## 8. Test

Offer the audit:

> "Run `/build:check-subagent <path>` to audit the scaffolded
> definition against the Tier-1 checks and judgment dimensions?"

The audit is the canonical follow-on — it catches anything the Safety
Check missed and gives a baseline-clean starting point.

## Anti-Pattern Guards

1. **Skipping the Route step** — scaffolding a subagent for work that
   wants a skill pushes the wrong primitive into the codebase.
2. **Over-permissioning "to be safe"** — every tool must be justified
   by a workflow step. Broad `tools` sets are flagged by
   `/build:check-subagent` Tier-2.
3. **`Agent` in a subagent's tools list** — always a no-op for
   delegated subagents; drop it or flag the main-thread alternative.
4. **Capability-summary descriptions** — "handles data tasks" fails
   as a routing contract. Descriptions are router prompts, not
   documentation.
5. **Missing completion condition** — a workflow with no explicit
   "done" step is a runaway risk. Add a terminating step **and**
   consider `maxTurns` for multi-step workflows.
6. **`background: true` with Write/Edit and no `isolation: worktree`**
   — parallel writes on shared files conflict. Scaffold the
   worktree isolation when the combination appears.
7. **Silent `memory:` tool expansion** — when `memory:` is set
   alongside a narrow `tools` list, surface the implicit
   Read/Write/Edit grant to the user before Save.
8. **Writing before Review Gate** — the approval gate is hard; no
   file lands before it passes.

## Key Instructions

- Refuse on Route failure. If a skill / hook / rule / script fits
  better, recommend it and stop.
- Elicit the name, description, workflow, and tools before drafting —
  do not invent any of them from `$ARGUMENTS` alone.
- The description is the routing contract. Verb-phrase + trigger +
  exclusion + returns. Flag one-liners.
- Write files to disk only after the Review Gate passes.
- Surface spec-documented side effects (plugin field no-ops, memory
  auto-grant, parent-precedence override, description truncation) at
  Elicit time — these are silent failures at runtime otherwise.
- Won't scaffold subagents that duplicate existing skills without
  parallelism / isolation / permission justification — recommend the
  skill.
- Won't list `Agent` in a subagent's `tools` — it's filtered at the
  platform level for delegated agents.
- Recovery if a definition is written in error: `rm
  .claude/agents/<name>.md` removes it cleanly. The definition is
  self-contained (no registration, no shared-module dependency).

## Handoff

**Receives:** user intent for a Claude Code subagent (name,
routing-oriented description, primary capability + workflow, tool
requirements, any advanced fields the workflow signals).
**Produces:** an executable subagent definition at
`.claude/agents/<name>.md` with complete frontmatter, bounded prompt
body, mandated output format, and explicit failure behavior.
**Chainable to:** `/build:check-subagent` (audit the scaffolded
definition against the Tier-1 checks and judgment dimensions).
