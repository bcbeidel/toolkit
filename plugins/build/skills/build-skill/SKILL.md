---
name: build-skill
description: >
  Create new skills, modify and improve existing skills, and measure skill
  performance. Use when the user wants to "create a skill", "add a skill",
  "build a skill", "scaffold a skill", "new skill for [X]", "write a skill
  that does X", run evals on a skill, benchmark skill performance, or
  optimize a skill's description for better triggering accuracy. Also use
  when the user wants to capture or automate a workflow, turn a conversation
  into a reusable skill, or improve how an existing skill triggers.
argument-hint: "[skill name and description]"
user-invocable: true
tested_with: [sonnet]
references:
  - references/schemas.md
  - references/platform-notes.md
  - references/description-optimization.md
  - references/skill-writing-guide.md
  - references/eval-workflow.md
  - ../../_shared/references/primitive-routing.md
---

# Skill Creator

A skill for creating new skills and iteratively improving them.

At a high level, the process of creating a skill goes like this:

- Decide what you want the skill to do and roughly how it should do it
- Write a draft of the skill
- Create a few test prompts and run claude-with-access-to-the-skill on them
- Help the user evaluate the results both qualitatively and quantitatively
  - While the runs happen in the background, draft some quantitative evals if there aren't any (if there are some, you can either use as is or modify if you feel something needs to change about them). Then explain them to the user (or if they already existed, explain the ones that already exist)
  - Use the `eval-viewer/generate_review.py` script to show the user the results for them to look at, and also let them look at the quantitative metrics
- Rewrite the skill based on feedback from the user's evaluation of the results (and also if there are any glaring flaws that become apparent from the quantitative benchmarks)
- Repeat until you're satisfied
- Expand the test set and try again at larger scale

Your job when using this skill is to figure out where the user is in this process and then jump in and help them progress through these stages. So for instance, maybe they're like "I want to make a skill for X". You can help narrow down what they mean, write a draft, write the test cases, figure out how they want to evaluate, run all the prompts, and repeat.

On the other hand, maybe they already have a draft of the skill. In this case you can go straight to the eval/iterate part of the loop.

Of course, you should always be flexible and if the user is like "I don't need to run a bunch of evaluations, just vibe with me", you can do that instead.

Then after the skill is done (but again, the order is flexible), you can also run the skill description improver, which we have a whole separate script for, to optimize the triggering of the skill.

## Communicating with the user

The skill creator is liable to be used by people across a wide range of familiarity with coding jargon. If you haven't heard (and how could you, it's only very recently that it started), there's a trend now where the power of Claude is inspiring plumbers to open up their terminals, parents and grandparents to google "how to install npm". On the other hand, the bulk of users are probably fairly computer-literate.

So please pay attention to context cues to understand how to phrase your communication! In the default case, just to give you some idea:

- "evaluation" and "benchmark" are borderline, but OK
- for "JSON" and "assertion" you want to see serious cues from the user that they know what those things are before using them without explaining them

It's OK to briefly explain terms if you're in doubt, and feel free to clarify terms with a short definition if you're unsure if the user will get it.

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
4. Should we set up test cases to verify the skill works? Skills with objectively verifiable outputs (file transforms, data extraction, code generation, fixed workflow steps) benefit from test cases. Skills with subjective outputs (writing style, art) often don't need them. Suggest the appropriate default based on the skill type, but let the user decide.

### Interview and Research

Proactively ask questions about edge cases, input/output formats, example files, success criteria, and dependencies. Wait to write test prompts until you've got this part ironed out.

Also probe for structural decisions that shape how the skill is built — derive these from the conversation where possible; only ask if the answer isn't clear:

- **Dangerous or irreversible operations?** Deploys, destructive commands, external API writes, anything hard to undo. Affects gate placement, `disable-model-invocation`, and the won't-do scope in Key Instructions. For any irreversible action, document recovery steps in `## Key Instructions` or `## Handoff`. *(check-skill #21, #23)*
- **Scoped to specific files or directories?** A backend skill that shouldn't fire when working on frontend code benefits from `paths` frontmatter. Relevant especially in monorepos. *(check-skill #17)*
- **User-facing command or agent background knowledge?** If the user wants this as domain context injected into an agent rather than a callable command, `user-invocable: false` is the right pattern.
- **Needs persistent configuration?** API keys, project IDs, user preferences that vary per-person. If yes, plan for the `config.json` setup pattern.
- **Depends on other skills?** If the skill calls out to another skill by name, it needs a won't-work-without dependency note in Key Instructions.
- **Where should this skill live?** Pick a scope before drafting:
  - **project** — `.claude/skills/<name>/SKILL.md` (default when working in a repo with a `.claude/` directory; ships with the codebase)
  - **personal** — `~/.claude/skills/<name>/SKILL.md` (single-user, all projects)
  - **plugin** — `<plugin-root>/skills/<name>/SKILL.md` (when contributing to a plugin marketplace)
  - **enterprise** — managed deployment path defined by the deploying org

  This decision is load-bearing: the write step needs the full path, not the relative `skills/<name>/SKILL.md`.

Check available MCPs - if useful for research (searching docs, finding similar skills, looking up best practices), research in parallel via subagents if available, otherwise inline. Come prepared with context to reduce burden on the user.

### Write the SKILL.md

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
- **hooks** _(optional)_: Lifecycle hooks scoped to this skill's session. Use for on-demand safety guardrails — see On-Demand Hooks below.
- **paths** _(optional)_: Glob patterns that limit when the skill auto-activates. Useful in monorepos to prevent a backend skill firing in frontend code: `paths: "packages/backend/**"`. *(check-skill #17)*
- **allowed-tools** _(optional)_: Tools that run without per-use confirmation when this skill is active. Canonical forms: **space-separated string** (`Grep Read`) or **YAML list** (`[Grep, Read]` or block form). **Never comma-separated as a string** (`Grep, Read`) — YAML parses it as one literal value and the field silently does nothing.
- **tested_with** _(optional)_: Model tiers verified against (e.g., `[sonnet, haiku]`); omit if untested. *(check-skill #2)*
- **references** _(optional)_: Reference files or assets in the skill directory for progressive disclosure.

After drafting, also include in `## Key Instructions` at least one explicit won't-have — a negative scope boundary ("Won't…", "Does not…", "Excluded:"). Missing negative rules leave scope undefined. *(check-skill #11)*

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

- **Frontmatter choices** — explain any non-default field settings and why. Don't just name the field; explain the reasoning: "I set `disable-model-invocation: true` because this deploys to production — it should never fire unless you explicitly invoke it."
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
python scripts/lint.py --root <project-root> --no-urls   # fix any skill quality findings
python scripts/reindex.py --root <project-root>           # update _index.md navigation
```

Write to the full path determined by the scope decision in the Interview step (e.g. `.claude/skills/<name>/SKILL.md` for a project skill). Do not write until the user approves the draft. After writing, invoke `/check-skill` on the new skill — surface any findings and offer the repair loop before moving to test cases.

### Test Cases

After writing the skill draft, come up with 2-3 realistic test prompts — the kind of thing a real user would actually say. Share them with the user: [you don't have to use this exact language] "Here are a few test cases I'd like to try. Do these look right, or do you want to add more?" Then run them.

Save test cases to `evals/evals.json`. Don't write assertions yet — just the prompts. You'll draft assertions in the next step while the runs are in progress.

```json
{
  "skill_name": "example-skill",
  "evals": [
    {
      "id": 1,
      "prompt": "User's task prompt",
      "expected_output": "Description of expected result",
      "files": []
    }
  ]
}
```

See `references/schemas.md` for the full schema (including the `assertions` field, which you'll add later).

## Running and evaluating test cases

Read `references/eval-workflow.md` for the full step-by-step process. Summary:
spawn with-skill and baseline runs in the same turn (Step 1), draft assertions
while runs are in progress (Step 2), capture timing on completion (Step 3),
grade + aggregate + launch viewer (Step 4), read feedback.json (Step 5).

---

## Improving the skill

This is the heart of the loop. You've run the test cases, the user has reviewed the results, and now you need to make the skill better based on their feedback.

### How to think about improvements

1. **Generalize from the feedback.** The big picture thing that's happening here is that we're trying to create skills that can be used a million times (maybe literally, maybe even more who knows) across many different prompts. Here you and the user are iterating on only a few examples over and over again because it helps move faster. The user knows these examples in and out and it's quick for them to assess new outputs. But if the skill you and the user are codeveloping works only for those examples, it's useless. Rather than put in fiddly overfitty changes, or oppressively constrictive MUSTs, if there's some stubborn issue, you might try branching out and using different metaphors, or recommending different patterns of working. It's relatively cheap to try and maybe you'll land on something great.

2. **Keep the prompt lean.** Remove things that aren't pulling their weight. Make sure to read the transcripts, not just the final outputs — if it looks like the skill is making the model waste a bunch of time doing things that are unproductive, you can try getting rid of the parts of the skill that are making it do that and seeing what happens.

3. **Explain the why.** Try hard to explain the **why** behind everything you're asking the model to do. Today's LLMs are *smart*. They have good theory of mind and when given a good harness can go beyond rote instructions and really make things happen. Even if the feedback from the user is terse or frustrated, try to actually understand the task and why the user is writing what they wrote, and what they actually wrote, and then transmit this understanding into the instructions. If you find yourself writing 'always' or 'never' in all caps, or using super rigid structures, that's a yellow flag — if possible, reframe and explain the reasoning so that the model understands why the thing you're asking for is important. That's a more humane, powerful, and effective approach.

4. **Look for repeated work across test cases.** Read the transcripts from the test runs and notice if the subagents all independently wrote similar helper scripts or took the same multi-step approach to something. If all 3 test cases resulted in the subagent writing a `create_docx.py` or a `build_chart.py`, that's a strong signal the skill should bundle that script. Write it once, put it in `scripts/`, and tell the skill to use it. This saves every future invocation from reinventing the wheel.

Take your time here — write a draft revision, then read it fresh before finalizing. Get into the head of the user: understand what they actually want and why they're asking.

### The iteration loop

After improving the skill:

1. Apply your improvements to the skill
2. Rerun all test cases into a new `iteration-<N+1>/` directory, including baseline runs. If you're creating a new skill, the baseline is always `without_skill` (no skill) — that stays the same across iterations. If you're improving an existing skill, use your judgment on what makes sense as the baseline: the original version the user came in with, or the previous iteration.
3. Launch the reviewer with `--previous-workspace` pointing at the previous iteration
4. Wait for the user to review and tell you they're done
5. Read the new feedback, improve again, repeat

Keep going until:
- The user says they're happy
- The feedback is all empty (everything looks good)
- You're not making meaningful progress

---

## Advanced: Blind comparison

For situations where you want a more rigorous comparison between two versions of a skill (e.g., the user asks "is the new version actually better?"), there's a blind comparison system. Read `agents/comparator.md` and `agents/analyzer.md` for the details. The basic idea is: give two outputs to an independent agent without telling it which is which, and let it judge quality. Then analyze why the winner won.

This is optional, requires subagents, and most users won't need it. The human review loop is usually sufficient.

---

## Description Optimization

After the skill is stable and the user is happy with the outputs, offer to optimize the description for better triggering accuracy. The description is the primary mechanism Claude uses to decide whether to invoke a skill, and undertriggering is a documented bias worth addressing.

Read `references/description-optimization.md` for the full process: generating eval queries, reviewing them with the user, running the optimization loop, and applying the result.

---

### Package and Present (only if `present_files` tool is available)

Check whether you have access to the `present_files` tool. If you don't, skip this step. If you do, package the skill and present the .skill file to the user:

```bash
python -m scripts.package_skill <path/to/skill-folder>
```

After packaging, direct the user to the resulting `.skill` file path so they can install it.

---

## Platform-Specific Instructions

If you're on **Claude.ai** or **Cowork**, some mechanics differ from the standard Claude Code workflow — subagent availability, browser access, and feedback collection all vary. Read `references/platform-notes.md` for the full details on what to skip, adapt, or substitute for your environment.

---

## Reference files

The agents/ directory contains instructions for specialized subagents. Read them when you need to spawn the relevant subagent.

- `agents/grader.md` — How to evaluate assertions against outputs
- `agents/comparator.md` — How to do blind A/B comparison between two outputs
- `agents/analyzer.md` — How to analyze why one version beat another

The references/ directory has additional documentation:
- `references/schemas.md` — JSON structures for evals.json, grading.json, etc.
- `references/platform-notes.md` — Claude.ai and Cowork mechanics (subagents, browser, feedback)
- `references/description-optimization.md` — Full process for optimizing skill triggering accuracy

## Anti-Pattern Guards

1. **Writing to disk before user approval** — always show the draft first; the user must explicitly approve before SKILL.md is written
2. **Overfitting to test cases** — narrow, example-specific rules make skills that fail outside the test set; generalize from feedback, don't patch individual failures
3. **Skipping baselines** — without a baseline run, improvement is unmeasurable; always spawn with-skill and baseline runs in the same turn
4. **Skipping the Confirm Primitive gate** — if artifact type is ambiguous, building a skill when a hook, script, or context doc would serve better wastes the user's time

## Handoff

**Receives:** Skill name and intent (or path to existing SKILL.md for improvement); or no argument if the user wants to capture the current conversation as a skill
**Produces:** SKILL.md written to `skills/<name>/SKILL.md`; optionally: evals.json, eval workspace with benchmark and grading results, optimized description
**Chainable to:** check-skill (to audit quality after writing)

## Key Instructions

- Won't write any file — including SKILL.md — without explicit user approval of the draft
- Won't skip the Confirm Primitive gate when the artifact type is uncertain
- Won't overfit: generalizes improvements from feedback rather than patching individual test case failures
- Use theory of mind: explain the *why* behind instructions rather than issuing rigid commands or ALL-CAPS directives
- Keep SKILL.md under 500 non-blank lines; move detail to `references/` when approaching the limit
- After writing or modifying a skill, run `check-skill` against it — build-skill must produce skills that pass all 22 criteria it enforces

---

Repeating one more time the core loop here for emphasis:

- Figure out what the skill is about
- Draft or edit the skill
- Run claude-with-access-to-the-skill on test prompts
- With the user, evaluate the outputs:
  - Create benchmark.json and run `eval-viewer/generate_review.py` to help the user review them
  - Run quantitative evals
- Repeat until you and the user are satisfied
- Package the final skill and return it to the user.

Please add steps to your TodoList, if you have such a thing, to make sure you don't forget. If you're in Cowork, please specifically put "Create evals JSON and run `eval-viewer/generate_review.py` so human can review test cases" in your TodoList to make sure it happens.

