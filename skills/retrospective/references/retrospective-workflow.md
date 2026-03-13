# Retrospective Workflow

Reflect on the session, gather observations, and submit feedback.

## Phase 1: Check Prerequisites

Verify `gh` is available:

```bash
gh auth status 2>&1
```

If `gh` is not installed or not authenticated, respond with:

> To submit retrospective feedback, you need the GitHub CLI installed and authenticated:
>
> 1. Install: `brew install gh` (macOS) or see https://cli.github.com
> 2. Authenticate: `gh auth login`
> 3. Try again after setup is complete.

Do NOT proceed until `gh auth status` succeeds.

## Phase 2: Reflect

Summarize what happened in this session, then ask the user three questions
(one at a time, not all at once):

1. **What worked?** — "Think about a specific moment in this session
   where WOS helped you. What were you doing, and what happened?"
2. **What was frustrating?** — "Was there a point where you got stuck
   or had to work around WOS? Walk me through what happened."
3. **What was missing?** — "Was there something you wished WOS could
   do but it couldn't? What were you trying to accomplish?"

**Adaptive follow-up:** If the user's response is vague or incomplete,
ask one targeted follow-up before moving on:

- Vague ("it was fine") → "Can you point to the specific moment?"
- Abstract ("the workflow was slow") → "What exactly did that look
  like? Which step took longest?"
- Missing why ("I had to copy-paste") → "Why do you think that
  happened? What would have helped?"

Cap at 1 follow-up probe per question. If the response is already
specific and grounded, move on.

If the user provided a focus area in the invocation, tailor the questions
to that area instead of using the generic three.

## Phase 3: Gather Context

Auto-gather (do not ask the user for these):

```bash
# wos version
python <plugin-scripts-dir>/get_version.py

# Python version
python3 --version

# Platform
uname -s -r -m
```

## Phase 4: Check for Duplicates

Before drafting, search for related existing issues:

```bash
gh issue list --repo bcbeidel/wos --state all --search "KEYWORDS_HERE" --limit 5
```

Use 2-3 keywords extracted from the user's observations. Vary terms
(e.g., "research" vs. "workflow") to catch near-duplicates.

If related issues are found, show them to the user. For closed issues,
note the resolution (fixed, won't-fix, duplicate) so the user has
context. Then offer:

1. **Comment on existing** — add new context to the existing issue
2. **File new with cross-reference** — proceed, mentioning related
   issues in the body
3. **Abandon** — the issue is already tracked

If no related issues are found, proceed to synthesis.

## Phase 5: Synthesize Action Items

Review all observations from Phase 2 and extract 1-3 discrete action
items. For each, use the **Observation-Impact-Request** structure:

- **Observation:** What specifically happened (grounded in the session)
- **Impact:** Why it matters (time lost, quality affected, workflow blocked)
- **Request:** A concrete change or investigation

Present the action items to the user and ask them to assign a severity
to each:

- `blocking` — prevents effective use, no workaround
- `friction` — slows down workflow, workaround exists
- `nit` — minor polish, low urgency

If the user edits or removes items, apply their changes. If no
actionable observations emerged, skip this phase and note "No action
items" in the draft.

## Phase 6: Draft & Preview

Compose a GitHub issue using this template:

```markdown
## Session Retrospective

**Focus:** [focus area if provided, otherwise "General session review"]

### What Worked

[Bullet points from user's response to question 1]

### What Was Frustrating

[Bullet points from user's response to question 2]

### What Was Missing

[Bullet points from user's response to question 3]

### Action Items

[For each action item from Phase 5, format as:]

- **`[severity]`** *Observation:* [what happened] → *Impact:* [why it
  matters] → *Request:* [what to change]

[If no action items, write "No actionable items identified."]

### Session Context

[Brief, anonymized summary of what the session involved — e.g.,
"Research workflow on a new topic" or "Auditing and fixing a project".
Do NOT include repo names, file contents, or sensitive details.]

### Environment

- **wos version:** [version from plugin.json]
- **Python:** [python3 --version output]
- **Platform:** [uname output]
```

**Framing rule:** Write from the WOS tool author's perspective. Use
"a WOS user" instead of "I". Replace vault-specific details with
generic descriptions. Strip any repo names, file paths, or personal
information.

Show the draft to the user: "Here's the retrospective feedback I'd
submit. Want to change anything before I file it?"

Wait for explicit approval.

## Phase 7: Submit

Only after explicit approval:

```bash
gh issue create \
  --repo bcbeidel/wos \
  --title "Retrospective: [BRIEF_SUMMARY]" \
  --body "BODY_HERE" \
  --label "feedback"
```

On success, show the issue URL. On failure, show the error and suggest
checking `gh auth status`.
