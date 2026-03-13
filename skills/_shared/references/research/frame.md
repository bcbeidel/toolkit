---
name: Frame the Question
description: Phase 1 — restate the question, identify mode, break into sub-questions, write research brief
stage: frame
pipeline: research
---

## Purpose

Analyze the research question, detect the appropriate mode, and produce a structured brief with sub-questions and search strategy.

## Input

Research question from user, project root path, any stated constraints.

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

## Output

Structured brief with restated question, research mode, SIFT rigor level, 2-4 sub-questions, search strategy, and suggested output path.

### Phase Gate: Phase 1 → Phase 2

User confirmed sub-questions, research brief written.
