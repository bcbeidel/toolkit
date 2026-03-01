# Report-Issue Submit Workflow

Gather context, draft a GitHub issue, and submit.

## Phase 1: Check Prerequisites

Before gathering details, verify `gh` is available:

```bash
gh auth status 2>&1
```

If `gh` is not installed or not authenticated, respond with:

> To file issues, you need the GitHub CLI installed and authenticated:
>
> 1. Install: `brew install gh` (macOS) or see https://cli.github.com
> 2. Authenticate: `gh auth login`
> 3. Try again after setup is complete.

Do NOT proceed until `gh auth status` succeeds.

## Phase 2: Gather Context & Classify

Ask the user what happened. Collect:

- **What happened** — the problem or idea
- **What was expected** (for bugs) — what should have happened
- **Steps to reproduce** (for bugs) — how to trigger it
- **Error messages** — any error output

**Adaptive follow-up:** If the user's initial response is vague or
incomplete, ask one targeted follow-up before moving on:

- Vague description ("it broke") → "Can you walk me through what you
  did step by step?"
- Missing expected behavior → "What did you expect to happen instead?"
- No error output mentioned → "Did you see any error messages or
  unexpected output?"

If the user describes multiple distinct problems, ask which one to file
first and note the others for follow-up issues.

Cap at 2 follow-up probes total. If the response is already specific
and complete, proceed to classification.

Auto-gather (do not ask the user for these):

```bash
# wos version
uv run <plugin-scripts-dir>/get_version.py

# Python version
python3 --version

# Platform
uname -s -r -m
```

Based on the user's description, classify as one of:

| Type | Label | Signal words |
|------|-------|-------------|
| Bug report | `bug` | "broken", "error", "crash", "doesn't work", "wrong" |
| Feature request | `enhancement` | "would be nice", "add", "support", "could we" |
| General feedback | `feedback` | "suggestion", "thought", "observation" |

If ambiguous, ask: "Should I file this as a **bug report** or a
**feature request**?"

## Phase 3: Check for Duplicates

Before drafting, search for related existing issues:

```bash
gh issue list --repo bcbeidel/wos --state all --search "KEYWORDS_HERE" --limit 5
```

Use 2-3 keywords extracted from the user's description. Vary terms
(e.g., "crash" vs. "error") to catch near-duplicates.

If related issues are found, show them to the user. For closed issues,
note the resolution (fixed, won't-fix, duplicate) so the user has
context. Then offer:

1. **Comment on existing** — add new context to the existing issue
2. **File new with cross-reference** — proceed, mentioning related
   issues in the body
3. **Abandon** — the issue is already tracked

If no related issues are found, proceed to drafting.

## Phase 4: Draft & Preview

Use the appropriate template from `references/issue-templates.md`.

Fill in:
- **Title**: Concise summary (under 70 characters)
- **Body**: From the template, with gathered context
- **Labels**: From classification above

**Title quality check:** Before showing the preview, verify the title
identifies the component, the behavior, and the context.
"Audit --fix silently skips unreachable URLs" is actionable.
"Audit broken" is not. Rewrite if needed.

**Framing rule:** Write issues from the WOS tool author's perspective.
Use "a WOS user" instead of "I" or "my vault". Replace vault-specific
details with generic examples. Describe solutions in terms of WOS's
internal architecture.

Verify the issue is self-contained and uses generic framing before
showing the preview.

Show the user the complete draft and ask: "Does this look right? I can
edit any part before submitting."

Wait for explicit approval. If the user requests changes, apply them
and preview again.

## Phase 5: Submit

Only after explicit approval:

```bash
gh issue create \
  --repo bcbeidel/wos \
  --title "TITLE_HERE" \
  --body "BODY_HERE" \
  --label "LABEL_HERE"
```

On success, show the issue URL to the user.

On failure, show the error and suggest:
- Check `gh auth status`
- Try again with `gh issue create` manually
