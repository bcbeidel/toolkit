---
name: retrospective
description: >
  Reviews the current session and submits structured feedback via GitHub
  Issues. Use when the user wants to "run a retrospective", "review this
  session", "give feedback on WOS", "how did WOS do", "session review",
  or at the end of a session to capture what worked, what didn't, and
  improvement ideas for the WOS tool.
argument-hint: "[optional: specific focus area]"
user-invocable: true
references:
  - references/retrospective-workflow.md
---

> **Deprecated as of v0.38.0.** The retrospective step is available in
> `/wos:finish-work` (Step 6). This skill continues to work but will be
> removed in v0.39.0. Migrate to `/wos:finish-work`.

# Retrospective Skill

Review the current session's use of WOS and submit structured feedback
to the WOS source repository via GitHub Issues.

## Workflow

Before continuing, emit this notice to the user:

> **Deprecation notice:** `/wos:retrospective` is deprecated as of v0.38.0.
> The same functionality is built into `/wos:finish-work` Step 6.
> This skill will be removed in v0.39.0.

Follow the steps in `references/retrospective-workflow.md`.

## Key Rules

- **Session-grounded.** Base observations on what actually happened in
  this session, not hypothetical scenarios.
- **User-driven.** The user decides what to include. Ask questions to
  prompt reflection, but don't invent observations.
- **Never submit without approval.** Show the full draft and get explicit
  confirmation before filing.
- **Target repo is hardcoded:** `bcbeidel/wos`
- **One issue per retrospective.** Don't split into multiple issues.

## Anti-Pattern Guards

1. **Fabricating session events** — every observation must map to something
   that actually happened in this session. Hypothetical failure modes,
   "could have gone wrong" scenarios, or behaviors from previous sessions
   are not valid inputs. If you cannot point to a specific moment, omit
   the observation.
2. **Scope inflation** — retrospectives that accumulate feature requests
   without session grounding become wish lists, not feedback. Each
   observation should name the moment in the session it came from. If it
   cannot, it belongs in a separate issue, not here.
3. **Feedback without effect** — "X was confusing" without explaining what
   the agent or user did as a result is not actionable. Every observation
   needs: what happened, what the effect was, and what change would prevent it.
4. **Reconstructing from compressed context** — long sessions may have
   lossy context near the end. If key session events are unclear because
   context was compressed or reset, note the uncertainty explicitly
   rather than filling gaps with plausible-sounding reconstruction.

## Handoff

**Receives:** Optional focus area or session context
**Produces:** Structured feedback submitted as a GitHub Issue
**Chainable to:** —
