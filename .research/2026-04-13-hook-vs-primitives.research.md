---
name: "Hook vs. Other Claude Code Primitives"
description: "Decision criteria for when to use a Claude Code hook vs. skill, CLAUDE.md, subagent, or MCP server — what each primitive is optimized for and documented failure modes from wrong choices"
type: research
sources:
  - https://code.claude.com/docs/en/hooks
  - https://code.claude.com/docs/en/hooks-guide
  - https://code.claude.com/docs/en/skills
  - https://code.claude.com/docs/en/sub-agents
  - https://claude.com/blog/subagents-in-claude-code
  - https://alexop.dev/posts/understanding-claude-code-full-stack/
  - https://www.youngleaders.tech/p/claude-skills-commands-subagents-plugins
  - https://www.shareuhack.com/en/posts/claude-code-claude-md-setup-guide-2026
  - https://okhlopkov.com/claude-code-setup-mcp-hooks-skills-2026/
  - https://paddo.dev/blog/claude-code-hooks-guardrails/
related:
  - docs/context/hooks-deterministic-enforcement-vs-advisory.context.md
  - docs/context/hook-quality-criteria.context.md
  - docs/context/hook-event-payload-schemas.context.md
  - docs/context/claude-code-primitive-routing-and-reliability.context.md
  - docs/context/claude-md-to-hook-conversion-signals.context.md
  - docs/context/claude-code-wrong-primitive-failure-modes.context.md
  - docs/research/2026-04-07-hooks-ecosystem.research.md
  - docs/research/2026-04-13-hook-quality-and-evaluation.research.md
---

I investigated when a Claude Code hook is the right primitive vs. a skill, CLAUDE.md instruction, subagent, or MCP server — and what happens when the wrong primitive is chosen. Domain: Claude Code as of 2026. Focus: decision criteria and routing logic, not feature descriptions. Preferred sources: T1 (official Anthropic docs and blog), T3 (practitioners with documented experience).

## Research Question

When should a Claude Code hook be used rather than another available primitive, and what criteria determine which primitive is appropriate for a given enforcement or automation goal?

## Sub-Questions

1. What is each Claude Code primitive optimized for — what job does it do that others can't?
2. What are the decision criteria distinguishing hook-appropriate work from skill/command-appropriate work?
3. What are the decision criteria distinguishing hook-appropriate work from CLAUDE.md-appropriate work?
4. What are the documented failure modes when the wrong primitive is chosen?

## Sources

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|-----------|------|------|--------|
| 1 | https://code.claude.com/docs/en/hooks | Hooks reference | Anthropic | 2026 | T1 | verified |
| 2 | https://code.claude.com/docs/en/hooks-guide | Automate workflows with hooks | Anthropic | 2026 | T1 | verified |
| 3 | https://code.claude.com/docs/en/skills | Extend Claude with skills | Anthropic | 2026 | T1 | verified |
| 4 | https://code.claude.com/docs/en/sub-agents | Create custom subagents | Anthropic | 2026 | T1 | verified |
| 5 | https://claude.com/blog/subagents-in-claude-code | How and when to use subagents | Anthropic | 2026 | T1 | verified |
| 6 | https://alexop.dev/posts/understanding-claude-code-full-stack/ | Understanding Claude Code's Full Stack | alexop.dev | 2026 | T3 | verified |
| 7 | https://www.youngleaders.tech/p/claude-skills-commands-subagents-plugins | Skills vs Commands vs Subagents vs Plugins | Young Leaders Tech | 2026 | T3 | verified |
| 8 | https://www.shareuhack.com/en/posts/claude-code-claude-md-setup-guide-2026 | Claude Code Ignores Your CLAUDE.md? | shareuhack | 2026 | T3 | verified |
| 9 | https://okhlopkov.com/claude-code-setup-mcp-hooks-skills-2026/ | My Claude Code Setup After 4 Months | okhlopkov | 2026 | T3 | verified |
| 10 | https://paddo.dev/blog/claude-code-hooks-guardrails/ | Claude Code Hooks: Guardrails That Actually Work | paddo.dev | 2026 | T3 | verified |

## Raw Extracts

### Sub-question 1: What each primitive is optimized for

**CLAUDE.md (T1, skills docs; T3, shareuhack):**

CLAUDE.md is session-persistent behavioral context. It loads automatically at session start and stays in context throughout. It is advisory — Claude interprets it as context, exercises judgment about relevance, and may deprioritize it under context pressure.

From the official skills docs:
> "For injecting context on every session start, consider using CLAUDE.md instead."

From the shareuhack article on why CLAUDE.md fails:
> "Claude actively judges whether the CLAUDE.md content is relevant to the current task, and may skip it if it judges otherwise."
> "Every low-value rule added dilutes the compliance probability of every high-value rule equally."

Degradation accelerates past roughly 150–200 lines (after the system prompt consumes ~50). No hard cutoff, but community evidence points to uniform compliance degradation beyond this.

Best for: architectural context, implicit knowledge Claude can't derive from code, non-obvious project conventions, behavioral preferences with counterexamples. *Not* for mechanical enforcement.

**Skills (T1, skills docs; T3, alexop, youngleaders):**

Skills are demand-loaded instruction sets. The description is always in context; the full content loads only when invoked. From the official docs:
> "Skills extend what Claude can do. Create a SKILL.md file with instructions, and Claude adds it to its toolkit. Claude uses skills when relevant, or you can invoke one directly with /skill-name."
> "Create a skill when you keep pasting the same playbook, checklist, or multi-step procedure into chat, or when a section of CLAUDE.md has grown into a procedure rather than a fact."

The T3 alexop source frames this precisely: *"Skills are modular chunks of a CLAUDE.md file"* — same content type, but demand-loaded. This eliminates the context bloat problem of always-on CLAUDE.md content.

Invocation is either user-driven (`/skill-name`) or model-driven (Claude matches description to task). `disable-model-invocation: true` restricts to user-only. `user-invocable: false` restricts to model-only (background knowledge).

Skills can also spawn subagents via `context: fork` — making them a composition primitive, not just an instruction primitive.

Best for: repeatable multi-step procedures, domain-specific workflows with more detail than fits CLAUDE.md, processes you want demand-loaded rather than always-on, named commands with side effects that should only run when explicitly invoked.

**Hooks (T1, hooks-guide; T1, hooks reference; T3, alexop):**

Hooks are lifecycle-triggered deterministic handlers. From the official guide:
> "Hooks provide deterministic control over Claude Code's behavior, ensuring certain actions always happen rather than relying on the LLM to choose to run them."

From T3 alexop, the cleanest single-line distinction:
> "Hooks run without Claude's decision-making; they're deterministic handlers. Skills require Claude to recognize when they apply."

And:
> "Skills extend what Claude can do. Hooks constrain how Claude does it."

Best for: enforcement that must happen regardless of LLM judgment, lifecycle automation (pre-tool, post-tool, session events), security gates, format enforcement, anything that must fire at a specific lifecycle event without asking Claude to decide.

**Subagents (T1, subagents docs; T1, subagents blog):**

Subagents are isolated context windows with custom system prompts, tool permissions, and independent execution. From the official docs:
> "Use one when a side task would flood your main conversation with search results, logs, or file contents you won't reference again: the subagent does that work in its own context and returns only the summary."

From the blog:
> "Subagents prevent 'context poisoning' — when detailed implementation work clutters your main conversation."

Best for: research-heavy side tasks, parallel independent work, fresh-perspective code review, tasks requiring different tool permissions than the main session. *Not* for sequential dependent work (results can't feed step N+1 without round-trip) or small quick fixes where overhead outweighs benefit.

**MCP Servers:**

MCP servers expose external tools (GitHub, databases, APIs). From T3 alexop:
> "MCP connects external systems; skills orchestrate internal workflows."
> "MCP servers expose their own tools. They don't inherit Claude's Read, Write, or Bash unless you provide them."

Best for: connectivity to external systems. Does not replace skills for methodology or hooks for enforcement.

**settings.json permissions.deny (T3, shareuhack):**

Distinct from hooks — this is a static firewall, not event-driven logic:
> "settings.json (technical firewall): Security controls (permissions.deny), environment variable injection, sandbox configuration."

For hard security blocks that need zero runtime logic, `permissions.deny` is the correct primitive, not a hook. Hooks add conditional logic; permissions.deny is unconditional.

---

### Sub-question 2: Hook vs. skill/command decision criteria

**The core distinction (T1, hooks-guide; T3, alexop; T3, youngleaders):**

| Dimension | Hook | Skill |
|-----------|------|-------|
| Invocation | Lifecycle event fires automatically | Claude matches description OR user types /name |
| Decision-maker | None — deterministic | Claude (auto) or user (manual) |
| Can block | Yes (PreToolUse + exit 2) | No |
| Runs | At specific lifecycle moment | When invoked, for rest of session |
| Best when | Action must happen regardless of LLM | Action should happen when Claude judges relevant |

From official skills docs:
> "If the skill seems to stop influencing behavior after the first response, use hooks to enforce behavior deterministically."

This is the clearest routing signal: if a skill-defined procedure keeps getting skipped, the correct fix is not a better description — it's a hook.

**The "side-effects at timing" test:**
Skills with side effects (deploy, commit, send-slack-message) should use `disable-model-invocation: true` — user explicitly triggers them. But the timing itself isn't enforced; if timing enforcement is needed (e.g., "lint *must* run before commit, not just when Claude thinks it should"), that's a hook.

**Hooks inside skills (T1, skills docs):**
Skills can define scoped hooks in frontmatter — hooks that only fire while the skill is active. This is the composition pattern: a skill provides the instruction set, scoped hooks enforce the skill's invariants during execution.

---

### Sub-question 3: Hook vs. CLAUDE.md decision criteria

**The three-layer model (T3 multiple; T1 hooks-guide):**

> "Keep policy in CLAUDE.md, execution routines in Skills, and automatic enforcement in Hooks." (consensus across T3 sources)

> "Use CLAUDE.md and imported memory files for always-on guidance: architecture rules, naming conventions, test expectations. Use a skill when you want Claude to load richer instructions only when relevant. Use a hook when the system should enforce or inject something at a specific lifecycle event." (search result consensus)

**The conversion signal (T3, paddo.dev; T3, existing research):**

> "If a CLAUDE.md rule is one Claude 'keeps violating,' convert it to a hook. If it can be expressed as a shell one-liner, it belongs in a hook, not CLAUDE.md."

This is the operational decision criterion: repeated violation under normal conditions is a signal that CLAUDE.md is the wrong primitive for that rule.

**CLAUDE.md failure modes as routing signals (T3, shareuhack):**

Three failure modes that indicate CLAUDE.md is wrong for the job:

1. **Context dilution** — instructions buried in long CLAUDE.md are deprioritized in long sessions. If the rule matters late in a session, CLAUDE.md may not deliver it.
2. **Relevance judgment** — Claude may judge a rule as not applicable to the current task and skip it. Hooks bypass this judgment entirely.
3. **Instruction density degradation** — each added rule dilutes all others' compliance probability. Rules beyond ~150–200 lines face degraded compliance regardless of quality.

Diagnostic from shareuhack:
> "Paste the ignored rule directly into your first session message (outside CLAUDE.md). If Claude follows it then, the issue is delivery — use a hook. If ignored again, the rule needs rewriting — it's a quality problem, not a primitive problem."

**The settings.json boundary (T3, shareuhack):**

A fourth primitive often conflated with hooks: `permissions.deny` in `settings.json`. Use this for unconditional blocking (never allow tool X, ever). Use hooks when the block is conditional (block tool X when condition Y). The distinction: permissions.deny has no logic; hooks can.

---

### Sub-question 4: Failure modes when the wrong primitive is chosen

**CLAUDE.md used for enforcement (HIGH — multiple T1+T3):**

The most common mismatch. The failure mode: the rule is advisory and probabilistically overridden. Documented incidents (from existing research, paddo.dev): "NEVER edit .env files" → Claude loaded .env and replicated credentials; `rm -rf` with home path → executed after user intended limited removal.

Recovery: convert to a PreToolUse hook.

**Skills used for always-on context (MODERATE — T1, skills docs):**

Skills load only when invoked. Using a skill for always-present behavioral context (e.g., "always follow these conventions") fails when Claude doesn't recognize the description or the skill drops from context after compaction.

From the official docs:
> "Skill content lifecycle: When you or Claude invoke a skill, the rendered SKILL.md content enters the conversation as a single message and stays there for the rest of the session. Claude Code does not re-read the skill file on later turns... Auto-compaction carries invoked skills forward within a token budget."

After compaction, skills share a 25,000-token combined budget. Skills invoked early can be dropped if newer skills were invoked after them. Always-on context belongs in CLAUDE.md; demand-loaded procedures belong in skills.

**Hooks used for advisory guidance (MODERATE — T3, paddo.dev; T3, blakecrosley existing research):**

Over-aggressive hooks — blocking things that are sometimes legitimate — create bypass pressure. From paddo.dev: one false positive per session is enough to generate `--no-verify` culture. Hooks used for "suggestions" waste the blocking mechanism on advisory guidance. The correct primitive for "I'd prefer you do X" is CLAUDE.md or a skill, not a hook that exits 2.

**Subagents used for sequential dependent work (MODERATE — T1, subagents docs):**

> "Avoid subagents for sequential dependent work (step two needs full output of step one)."

Delegating sequential steps to subagents requires a round-trip per step, each spinning up a new context. The overhead cost is paid without the isolation benefit. Sequential multi-step work belongs in the main conversation or in a skill.

**CLAUDE.md for mechanical/objectively-testable rules (HIGH — T3, shareuhack; T1 implied by hooks docs):**

> "Objectively determinable rules (format checking, test coverage, shell-executable constraints) belong in hooks, not CLAUDE.md."

Rules that can be expressed as a shell one-liner are always better as hooks: deterministic, unambiguous, zero compliance probability. CLAUDE.md compliance for "always run prettier before committing" is probabilistic; a PostToolUse hook running prettier is guaranteed.

**Hooks for tasks needing Claude's judgment (MODERATE — T3, multiple):**

Using a hook when the decision requires LLM reasoning is also wrong. A hook that runs a full Claude analysis on every file write is high-cost, high-latency, and often produces nondeterministic results. The correct primitive is a `prompt` or `agent` handler type — but even then, only for high-value gates. For tasks that need Claude's judgment, skills or the main conversation are more appropriate than a hook.

## Challenge

### Assumptions Check

**Assumption:** The layer model (CLAUDE.md → Skills → Hooks) is strictly ordered.

**Challenge:** The official skills documentation shows skills can *contain* hooks (via the `hooks` frontmatter field), and skills can spawn subagents (`context: fork`). The separation is architectural guidance, not a hard boundary. A well-designed skill may legitimately include hooks for its own enforcement. The practical implication: the routing question is not "which layer?" but "does this need to happen deterministically at a lifecycle event?" If yes, use a hook regardless of whether it's standalone or embedded in a skill.

### ACH (Analysis of Competing Hypotheses)

**H1:** The right primitive selection is primarily a capability question (what can each primitive do?).
**H2:** The right primitive selection is primarily a reliability question (which primitive guarantees the behavior?).

Evidence favoring H2: The dominant routing signal in all sources is reliability — "hooks for things that must happen," "CLAUDE.md for guidance that should be followed." The failure modes are almost entirely about reliability (CLAUDE.md violations, skill non-triggers) rather than capability mismatches. The primitives are largely capability-equivalent for many tasks; hooks and CLAUDE.md both express the same constraints, but one is advisory and the other isn't. H2 better explains the observed failure modes.

### Premortem

**Scenario:** A team applies the framework correctly at authoring time but the system degrades over months.

Likely degradation paths:
- CLAUDE.md grows past 200 lines as rules accumulate; compliance probability degrades uniformly
- Hooks proliferate without audit; slow hooks accumulate latency; bypass culture sets in
- Skills drift as code changes but skill descriptions don't update; auto-invocation becomes unreliable
- MCP server tools multiply without governance; Claude invokes expensive operations on routine queries

The framework requires periodic revalidation, not just initial correct selection.

## Findings

### SQ1: Primitive capabilities and optimization targets

**Each primitive occupies a distinct reliability and lifecycle position (HIGH — T1 + T3 convergence):**

| Primitive | Invocation | Decision-maker | Reliability | Best fit |
|-----------|-----------|----------------|-------------|----------|
| CLAUDE.md | Always-on, session-persistent | Claude (probabilistic) | Advisory | Architectural context, implicit knowledge |
| Skill | On-demand, description-matched | Claude or user | Advisory (model-driven) / Deterministic (user-driven) | Repeatable procedures, demand-loaded reference |
| Hook | Lifecycle event, automatic | None | Deterministic | Enforcement, automation at lifecycle boundaries |
| Subagent | Task-delegated, description-matched | Claude | Isolated context | Side tasks that would pollute main context |
| MCP server | Tool call | Claude | Deterministic (external API) | External system connectivity |
| permissions.deny | Always | None (firewall) | Unconditional | Permanent unconditional blocks |

The key differentiator is reliability tier: CLAUDE.md and model-invoked skills are probabilistic; hooks, user-invoked skills, and permissions.deny are deterministic. The right primitive for enforcement is always in the deterministic tier.

---

### SQ2: Hook vs. skill routing

**Use a hook when the action must fire at a lifecycle boundary regardless of LLM judgment; use a skill when Claude should decide when to apply the procedure (HIGH — T1 + T3).**

The cleanest routing signal is the "keep violating" test: if a skill-defined procedure is being skipped when it should run, and the correct behavior is "always run at event X," that's a hook. Skills are the wrong primitive for anything with mandatory timing.

The two-question routing test:
1. **Must this happen at a specific lifecycle event (before/after a tool call, session start, stop)?** → Hook
2. **Should Claude decide whether this applies to the current task?** → Skill (auto-invoke) or CLAUDE.md

Skills can contain hooks (`hooks:` frontmatter field) for their own enforcement. This is the correct pattern for a skill that defines a procedure *and* needs to enforce some invariant during that procedure — the skill provides instructions, the scoped hook enforces the invariant.

---

### SQ3: Hook vs. CLAUDE.md routing

**Use CLAUDE.md for context and judgment-requiring guidance; convert to a hook any rule that (a) can be expressed as a shell one-liner, (b) must fire at a lifecycle event, or (c) Claude keeps violating under normal conditions (HIGH — T1 + T3 convergence).**

The three conversion signals:
1. Claude keeps violating the rule → hook (reliability problem)
2. The rule is shell-expressible → hook (determinism advantage)
3. The rule needs to fire at a specific lifecycle moment → hook (timing guarantee)

For unconditional permanent blocks, `permissions.deny` is a simpler and more reliable primitive than a hook. Hooks add conditional logic; permissions.deny removes the decision entirely.

CLAUDE.md degradation past ~150–200 lines is a documented failure mode. The practical implication: every rule added to CLAUDE.md should pass the hook test (is this actually advisory?) before being added. Rules that fail the hook test belong in hooks, reducing CLAUDE.md size and improving compliance for the rules that remain.

---

### SQ4: Failure modes from wrong primitive choice

**Wrong-primitive failures are almost always reliability failures, not capability failures (HIGH — T1 + T3).**

The primitives are largely capability-equivalent for many tasks. The failure that matters is reliability: will this happen when it needs to?

Priority failure modes:
1. **CLAUDE.md for enforcement** → probabilistic override, context dilution, instruction degradation (HIGH risk, documented incidents)
2. **Skills for always-on context** → skill dropped after compaction; post-compaction behavior changes unpredictably (MODERATE risk)
3. **Hooks for advisory guidance** → over-blocking creates bypass culture; one false positive per session is sufficient (MODERATE risk)
4. **Subagents for sequential work** → context overhead without isolation benefit; each step requires round-trip (MODERATE risk)
5. **CLAUDE.md past 200 lines** → uniform compliance degradation; highest-priority rules affected equally with low-priority ones (HIGH risk, documented)

The diagnostic pattern from shareuhack is general: isolate primitive from rule quality by testing the rule in isolation. If behavior changes in isolation, the primitive is wrong. If behavior doesn't change, the rule needs rewriting.

## Claims

| # | Claim | Type | Source | Status |
|---|-------|------|--------|--------|
| 1 | CLAUDE.md compliance degrades past ~150–200 lines | threshold | [8] shareuhack | human-review — T3 practitioner, no T1 corroboration; community research cited but not primary |
| 2 | Skills extend capabilities; hooks constrain behavior | framing | [3] skills docs | verified — official docs state "Skills extend what Claude can do" |
| 3 | Hooks run without Claude's decision-making; skills require Claude to recognize when they apply | distinction | [6] alexop | verified — consistent with T1 hook docs ("deterministic control") |
| 4 | Skills dropped after compaction share 25,000 token budget, filled from most recent first | behavior | [3] skills docs | verified — explicitly documented in skill content lifecycle section |
| 5 | One false positive per session is sufficient to generate bypass culture | threshold | [10] paddo.dev | human-review — T3 practitioner judgment, plausible but not empirically measured |
| 6 | settings.json permissions.deny is the correct primitive for unconditional blocks; hooks are for conditional logic | architecture | [8] shareuhack | verified — consistent with T1 hook docs (hooks add logic, permissions deny unconditionally) |
| 7 | "If a CLAUDE.md rule is one Claude keeps violating, convert it to a hook" | heuristic | [10] paddo.dev | verified — explicitly stated; consistent with T1 docs on deterministic enforcement |
| 8 | Skills can contain scoped hooks via `hooks:` frontmatter field | feature | [3] skills docs | verified — documented in skills frontmatter reference |

## Search Protocol

<!-- search-protocol
{"entries": [
  {"query": "Claude Code hooks vs skills vs commands when to use which primitive 2026", "source": "google", "date_range": "2024-2026", "results_found": 10, "results_used": 4},
  {"query": "Claude Code CLAUDE.md vs hooks vs skills decision criteria routing 2026", "source": "google", "date_range": "2024-2026", "results_found": 10, "results_used": 3},
  {"query": "Claude Code primitives comparison hooks skills subagents MCP servers slash commands 2026", "source": "google", "date_range": "2024-2026", "results_found": 10, "results_used": 3},
  {"query": "Claude Code hooks vs agents subagents automation when to use 2026", "source": "google", "date_range": "2024-2026", "results_found": 10, "results_used": 3},
  {"query": "\"wrong primitive\" OR \"use hook instead\" OR \"CLAUDE.md insufficient\" Claude Code when not to use 2026", "source": "google", "date_range": "2024-2026", "results_found": 10, "results_used": 1}
], "not_searched": [
  "MCP protocol spec (anthropic.com/mcp) — MCP internals not needed; decision criteria, not implementation",
  "plugins reference — plugins are a distribution primitive, not a runtime decision surface"
]}
-->
