---
name: Frame the Question
description: Phase 1 — restate the question, identify mode, break into sub-questions, write research brief
stage: frame
pipeline: research
tools:
  - Read
  - Glob
  - Grep
---

## Purpose

Analyze the research question, detect the appropriate mode, and produce a structured brief with sub-questions and search strategy.

## Input

- **Research question/topic** from the user
- **Stated constraints** (time period, domain, technology stack, etc.)
- **Project root path** for context exploration

# Phase 1: Frame the Question

1. Restate the user's question in a precise, answerable form
2. Identify the research mode (see research-modes.md)
3. Break into 2-4 sub-questions
4. Confirm with user: "I'll investigate [question] by looking at [sub-questions]. Sound right?"
5. Note constraints (time period, domain, technology stack)
6. Declare search protocol — state which sources you'll search and initial terms. Initialize:

```json
{"entries": [], "not_searched": []}
```

> **Source diversity:** `WebSearch` routes through a single engine. Vary
> query terms to surface different source types. Fetch known database URLs
> directly when relevant. Log `"google"` as the source honestly. The
> `not_searched` field lists sources you chose not to search, not sources
> the tool can't access.

7. **Write a research brief.** After confirming sub-questions, write a
   1-paragraph first-person brief that becomes the opening of the DRAFT
   document:
   - State the question from the user's perspective
   - List all stated constraints (time period, domain, stack, etc.)
   - Mark unstated dimensions as explicitly open-ended
   - Specify preferred source types: official docs for technical questions,
     peer-reviewed for scientific, primary sources for historical

8. **Suggest output path.** Suggest `docs/research/YYYY-MM-DD-<slug>.md` based on the topic.

## Output

Structured brief containing:
- **Restated question** (precise, answerable)
- **Research mode** (from the mode table)
- **SIFT rigor level** (High, Medium, or Low)
- **Sub-questions** (2-4)
- **Search strategy** (initial terms, source types)
- **Constraints** (stated + open dimensions)
- **Research brief** (1 paragraph)
- **Suggested output path**

## Constraints

- **Read-only.** Do not write files. Do not use Write or Edit.
- **No web searches.** Do not use WebSearch or WebFetch.
- **No user prompts.** Do not ask the user anything. Return the brief
  to the dispatcher; the dispatcher handles user interaction.
- **Return the brief.** Your output is the structured brief, not a
  research document.

### Phase Gate: Phase 1 → Phase 2

User confirmed sub-questions, research brief written.
