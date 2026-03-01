# Issue Templates

Templates for composing GitHub issues. Fill in the bracketed placeholders
with gathered context.

## Bug Report

```markdown
## Description

[What happened — clear, concise description of the bug]

## Steps to Reproduce

[The smallest possible setup that triggers the bug. Include:
- A minimal document fixture (inline or as a file description)
- The exact command or skill invocation
- The exact error output]

## Expected Behavior

[What should have happened]

## Actual Behavior

[What actually happened, including full error messages]

## Workaround / Proposed Fix

[Optional: any workaround you found, or ideas for a fix]

## Environment

- **wos version:** [version from plugin.json]
- **Python:** [python3 --version output]
- **Platform:** [uname output]
```

## Feature Request

```markdown
## Problem

[Describe the problem generically — any WOS user should recognize it.
Avoid references to specific vaults, file counts, or personal workflows.]

## Proposed Solution

[What the feature does and how it works. Include before/after examples
where behavior changes.

- **Scope:** What's included in this proposal
- **Non-goals:** What's explicitly excluded to prevent scope creep]

## Acceptance Criteria

This issue is resolved when:

- [specific observable condition]

## Environment

- **wos version:** [version from plugin.json]
```

## General Feedback

```markdown
## Context

[What were you doing when this observation came up?]

## Observation

[What did you notice? What could be better?]

## Suggestion

[Any ideas for improvement]

## Environment

- **wos version:** [version from plugin.json]
```
