---
name: build-skill
description: >
  Create new skills and iteratively improve existing ones. Use when the
  user wants to "create a skill", "add a skill", "build a skill",
  "scaffold a skill", "new skill for [X]", or "write a skill that does X".
  Also use when the user wants to capture or automate a workflow, or turn
  a conversation into a reusable skill.
argument-hint: "[skill name and description]"
user-invocable: true
tested_with: [sonnet]
references:
  - references/platform-notes.md
  - references/skill-writing-guide.md
  - ../../_shared/references/primitive-routing.md
---

# Skill Creator

A skill for creating new skills and iteratively improving them.

At a high level, the process looks like this:

- Decide what you want the skill to do and roughly how it should do it
- Write a draft of the skill
- Try it on a realistic prompt, review the output with the user, and revise
- Repeat until it's working well

Your job when using this skill is to figure out where the user is in this process and then jump in and help them progress. So for instance, maybe they're like "I want to make a skill for X". You can help narrow down what they mean, write a draft, try it on a realistic prompt, and iterate. Or maybe they already have a draft — then you can go straight to the iteration part of the loop.

Always be flexible. If the user says "just vibe with me", you can do that instead.

## Communicating with the user

The skill creator is liable to be used by people across a wide range of familiarity with coding jargon. There's a trend where the power of Claude is inspiring plumbers to open up their terminals, parents and grandparents to google "how to install npm". On the other hand, the bulk of users are probably fairly computer-literate.

Pay attention to context cues to understand how to phrase your communication. It's OK to briefly explain terms if you're in doubt, and feel free to clarify terms with a short definition if you're unsure if the user will get it.

---

## Creating a skill

### Confirm Primitive

Before eliciting, confirm a skill is the right artifact. Full decision matrix: [primitive-routing.md](../../_shared/references/primitive-routing.md).

Ask: "Building this as a **skill** (triggered instruction set) — right primitive?" Redirect if:
- Must fire at a lifecycle event regardless of LLM judgment → `/build:build-hook`
- Evaluates static file content for semantic compliance → `/build:build-rule`
- Needs context isolation or different tool permissions → `/build:build-subagent`
- Is advisory always-on context (not a procedure) → CLAUDE.md section

Proceed without a gate if intent is unambiguous; ask one clarifying question if uncertain.

### Capture Intent

Start by understanding the user's intent. If `$ARGUMENTS` is non-empty, use it as the initial skill name and description signal — for example, `/build-skill processing-pdfs` → propose `processing-pdfs` as the name and ask for the description. The current conversation might already contain a workflow the user wants to capture (e.g., they say "turn this into a skill"). If so, extract answers from the conversation history first — the tools used, the sequence of steps, corrections the user made, input/output formats observed. The user may need to fill the gaps, and should confirm before proceeding to the next step.

1. What should this skill enable Claude to do?
2. When should this skill trigger? (what user phrases/contexts)
3. What's the expected output format?

### Interview and Research

Proactively ask questions about edge cases, input/output formats, example files, success criteria, and dependencies.

Also probe for structural decisions that shape how the skill is built — derive these from the conversation where possible; only ask if the answer isn't clear:

- **Dangerous or irreversible operations?** Deploys, destructive commands, external API writes, anything hard to undo. Affects gate placement, `disable-model-invocation`, and the won't-do scope in Key Instructions. For any irreversible action, document recovery steps in `## Key Instructions` or `## Handoff`. *(check-skill #21, #23)*
- **Scoped to specific files or directories?** A backend skill that shouldn't fire when working on frontend code benefits from `paths` frontmatter. Relevant especially in monorepos. *(check-skill #17)*
- **User-facing command or agent background knowledge?** If the user wants this as domain context injected into an agent rather than a callable command, `user-invocable: false` is the right pattern.
- **Needs persistent configuration?** API keys, project IDs, user preferences that vary per-person. If yes, plan for the `config.json` setup pattern.
- **Depends on other skills?** If the skill calls out to another skill by name, it needs a won't-work-without dependency note in Key Instructions.
- **Single file or multiple files?** If the body will exceed ~400 lines, or the domain has heterogeneous sub-topics (e.g. AWS / GCP / Azure, or one pattern per language), plan for reference files under `references/`. Reference files keep the main SKILL.md lean and load on demand. See `references/skill-writing-guide.md` → Progressive Disclosure. *(check-skill: reference-depth, reference-TOC WARNs)*
- **Risk and freedom level?** Classify the workflow and pick a matching instruction style (see `references/skill-writing-guide.md` → Degrees of Freedom):
  - **Reversible, low-stakes** (file transforms, doc generation, reads) → **high-freedom prose** — describe the intent; let Claude pick tools and order.
  - **External effects or specific tool order matters** → **medium-freedom** — parameterized steps with specific tool calls.
  - **Destructive or irreversible** (deploy, rm -rf, DROP TABLE, force-push) → **low-freedom** — scripts, explicit gates, no variation.

  Calibrate specificity to task fragility. Fragile tasks get low-freedom; routine tasks get high-freedom. Over-specifying a routine task produces brittle skills that break on edge cases Claude could have handled.
- **Where should this skill live?** Pick a scope before drafting:
  - **project** — `.claude/skills/<name>/SKILL.md` (default when working in a repo with a `.claude/` directory; ships with the codebase)
  - **personal** — `~/.claude/skills/<name>/SKILL.md` (single-user, all projects)
  - **plugin** — `<plugin-root>/skills/<name>/SKILL.md` (when contributing to a plugin marketplace)
  - **enterprise** — managed deployment path defined by the deploying org

  This decision is load-bearing: the write step needs the full path, not the relative `skills/<name>/SKILL.md`.

Check available MCPs — if useful for research (searching docs, finding similar skills, looking up best practices), research in parallel via subagents if available, otherwise inline. Come prepared with context to reduce burden on the user.

### Write the SKILL.md

Before drafting the body, read `references/skill-writing-guide.md` → **Lifecycle & Compaction**. Skills are standing instructions that persist throughout a conversation, not one-time steps. First 5K tokens are the only part guaranteed to survive compaction, so lead with load-bearing content.

Based on the user interview, fill in these components. Most skills need only `name` + `description` — reach for the others when the use case calls for it:

- **name**: Skill identifier (lowercase, hyphens, ≤64 chars). Reserved words (`anthropic`, `claude`) are rejected — they collide with platform-owned namespaces. Prefer **gerund form** (`processing-pdfs`, `analyzing-spreadsheets`) or **agent-noun form** (`checker`, `parser`) — these read as actions and improve trigger matching. Reject vague tokens (`helper`, `utils`, `tools`, `thing`, `stuff`) — they provide no triggering signal. *(check-skill: gerund-naming WARN)*
- **description**: When to trigger, what it does. Primary triggering mechanism — write it in **third person** ("Processes X", not "You can use this to…") and front-load the trigger phrase. Cap is **1024 characters**; if the draft passes ~800 chars, actively offer to split trigger phrases into optional `when_to_use` (combined cap 1536) rather than truncating. Avoid vague phrasings ("helps with", "processes data") — name a specific capability. Claude undertriggers, so cover adjacent phrasings and contexts even when the user doesn't name the skill explicitly. *(check-skill #7, #13)*
- **when_to_use** _(Claude Code only)_: Optional split for trigger phrases when the `description` alone would exceed 1024 chars. The two fields are concatenated at routing time under a combined 1536-char cap. When the description is at risk of overflow, prefer this split over compression — the trigger surface is what determines whether the skill fires at all.
- **argument-hint**: One-line hint shown in the CLI (e.g., `"[skill name and description]"`). When set, the body must consume the argument via a substitution: `$ARGUMENTS` (full string), `$ARGUMENTS[N]` or `$N` (Nth token). Without one, Claude Code appends `ARGUMENTS: <value>` at the end of the rendered skill — wrong position relative to the workflow. Insert `$ARGUMENTS` into the workflow step that consumes the input (e.g., "Read $ARGUMENTS"). See `references/skill-writing-guide.md` → Substitutions. *(check-skill #20, substitution-usage WARN)*
- **user-invocable**: Default `true` — **omit** unless you need `false` (reduces frontmatter noise and the post-compaction token budget). Set `false` for background-knowledge skills that should be preloaded into an agent rather than called directly; this also hides them from the `/` menu. *(check-skill #17)*
- **disable-model-invocation** _(optional)_: Set `true` for dangerous or consequential skills (deploy, destructive ops) that should only fire on explicit user invocation — never auto-triggered. *(check-skill #23)*
- **model** _(optional)_: Override the session model for this skill. Use `haiku` for fast lookups, `opus` for complex multi-step work.
- **effort** _(optional)_: Override reasoning depth (`low`/`medium`/`high`/`max`). Use `low` for templating, `high` for code review or analysis.
- **context: fork** _(optional)_: Run the skill in an isolated subagent — the parent context only sees the final result, not intermediate tool calls. Pair with `agent:` to set the subagent type. When using `context: fork`, declare the subagent's operational scope in `## Key Instructions` (read-only, write-gated, requires approval, etc.). *(check-skill #18)*
- **hooks** _(optional)_: Lifecycle hooks scoped to this skill's session. Use for on-demand safety guardrails — see On-Demand Hooks in the writing guide.
- **paths** _(optional)_: Glob patterns that limit when the skill auto-activates. Useful in monorepos to prevent a backend skill firing in frontend code: `paths: "packages/backend/**"`. *(check-skill #17)*
- **allowed-tools** _(optional)_: Tools that run without per-use confirmation when this skill is active. Canonical forms: **space-separated string** (`Grep Read`) or **YAML list** (`[Grep, Read]` or block form). **Never comma-separated as a string** (`Grep, Read`) — YAML parses it as one literal value and the field silently does nothing.
- **tested_with** _(optional)_: Model tiers verified against (e.g., `[sonnet, haiku]`); omit if untested. *(check-skill #2)*
- **references** _(optional)_: Reference files or assets in the skill directory for progressive disclosure.

**Optional toolkit sections.** Add these when trigger conditions apply — they're house-style scaffolding, not canonical requirements. See [check-skill criteria](../../check-skill/SKILL.md) for the exact triggers.

- `## Handoff` (Receives / Produces / Chainable-to) — include when this skill chains to another skill, writes files, or runs under `context: fork`. *(check-skill #3)*
- `## Anti-Pattern Guards` — include when the Workflow performs destructive, irreversible, or external-effect operations. *(check-skill #4)*
- `## Key Instructions` with an explicit won't-have — include when the skill performs destructive ops or overlaps with other skills in the same plugin. *(check-skill #11)*

Read-only single-step skills generally don't need any of these sections. Add them only when the trigger conditions apply.

### Skill Writing Guide

Read `references/skill-writing-guide.md` before drafting. It covers anatomy,
progressive disclosure patterns, on-demand hooks, config.json setup, skill
composition, persistent state, writing style, writing patterns, and the full
quality requirements checklist.

**Canonical correctness.** In code blocks and inline code, use forward slashes
(`path/to/file`) — Windows-style backslashes (`path\to\file`) are rejected by
`check-skill` as they don't round-trip across platforms.

### Narrate the Draft

Before running lint or asking for approval, walk the user through the key design choices in the draft. Keep it to 3–6 bullets. Cover:

- **Frontmatter choices** — explain any non-default field settings and why. Name the field *and* explain the reasoning: "I set `disable-model-invocation: true` because this deploys to production — it should never fire unless you explicitly invoke it."
- **Structure choices** — why the workflow is ordered the way it is, where gate checks are placed and what they guard, how prescriptive vs. flexible each section is and why.
- **Patterns applied** — call out explicitly if you used progressive disclosure, on-demand hooks, agent skill pattern, config.json setup, or skill composition. New users won't recognize these patterns unless named.
- **What you didn't use and why** — briefly note any patterns you considered but skipped. This is often more educational than listing what you did use: "I didn't add `context: fork` — you'll want to see the intermediate steps while we iterate; we can add it later if the skill gets noisy."

The goal is that a user who doesn't know skill authoring can read the narration and understand — and disagree with — any structural choice. If you can't explain a choice clearly, revisit it before presenting.

**Example narration:**
> - `disable-model-invocation: true` — this pushes to production; shouldn't ever fire on its own
> - Gate before the push step — CI must be green first; I made that an explicit check rather than a comment
> - No reference files yet — the workflow fits in the body at ~80 lines; would split if it grows
> - Didn't use `context: fork` — you'll want to see tool calls while we're still iterating on the skill

### WOS Quality Check

Before writing to disk, run lint and reindex:

```bash
python3 plugins/wiki/scripts/lint.py --root <project-root> --no-urls   # fix any skill quality findings
python3 plugins/wiki/scripts/reindex.py --root <project-root>           # update _index.md navigation
```

Write to the full path determined by the scope decision in the Interview step (e.g. `.claude/skills/<name>/SKILL.md` for a project skill). Write only after the user approves the draft. After writing, invoke `/check-skill` on the new skill — surface any findings and offer the repair loop before moving on.

---

## Iterating

After the user tries the skill on a realistic prompt and gives feedback, make it better. A few principles:

1. **Generalize from the feedback.** The big picture is that we're trying to create skills that can be used many times across many different prompts. The user knows their own example inside-out, but if the skill only works for that example, it's useless. Rather than putting in fiddly overfitty changes, or oppressively constrictive MUSTs, if there's a stubborn issue try branching out — different metaphors, different patterns of working. It's relatively cheap to try and maybe you'll land on something great.

2. **Keep the prompt lean.** Remove things that aren't pulling their weight. Read transcripts when you can — if the skill is making the model waste time on unproductive things, try removing the parts that drive that and see what happens.

3. **Explain the why.** Try hard to explain the **why** behind everything you're asking the model to do. Today's LLMs are smart — they have good theory of mind and can go beyond rote instructions when given a good harness. Even if user feedback is terse or frustrated, try to understand the task and why the user is writing what they wrote, and transmit that understanding into the instructions. Writing 'always' or 'never' in all caps, or using super rigid structures, is a yellow flag — if possible, reframe and explain the reasoning so the model understands why the thing you're asking for matters.

4. **Look for repeated work.** If a skill keeps making the model independently write the same helper script or take the same multi-step approach, that's a strong signal the skill should bundle that script. Write it once, put it in `scripts/`, and tell the skill to use it.

Take your time. Write a draft revision, then read it fresh before finalizing. Get into the head of the user: understand what they actually want and why they're asking.

---

## Platform-Specific Instructions

If you're on **Claude.ai**, **Copilot**, or **Cowork**, some mechanics differ from the standard Claude Code workflow. Read `references/platform-notes.md` for the details on what to skip, adapt, or substitute for your environment.

---

## Package and Present (only if `present_files` tool is available)

Check whether you have access to the `present_files` tool. If you don't, skip this step. If you do, package the skill and present the .skill file to the user:

```bash
python -m scripts.package_skill <path/to/skill-folder>
```

After packaging, direct the user to the resulting `.skill` file path so they can install it.

---

## Anti-Pattern Guards

1. **Writing to disk before user approval** — always show the draft first; the user must explicitly approve before SKILL.md is written
2. **Overfitting to one example** — narrow, example-specific rules make skills that fail outside that example; generalize from feedback rather than patching individual failures
3. **Skipping the Confirm Primitive gate** — if artifact type is ambiguous, building a skill when a hook, script, or context doc would serve better wastes the user's time

## Handoff

**Receives:** Skill name and intent (or path to existing SKILL.md for improvement); or no argument if the user wants to capture the current conversation as a skill
**Produces:** SKILL.md written to `skills/<name>/SKILL.md`
**Chainable to:** check-skill (to audit quality after writing)

## Key Instructions

- Won't write any file — including SKILL.md — without explicit user approval of the draft
- Won't skip the Confirm Primitive gate when the artifact type is uncertain
- Won't overfit: generalizes improvements from feedback rather than patching individual failures
- Use theory of mind: explain the *why* behind instructions rather than issuing rigid commands or ALL-CAPS directives
- Keep SKILL.md under 500 non-blank lines; move detail to `references/` when approaching the limit
- After writing or modifying a skill, run `check-skill` against it — build-skill must produce skills that pass all 22 criteria it enforces
