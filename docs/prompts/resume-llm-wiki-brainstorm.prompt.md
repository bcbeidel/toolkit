---
name: Resume LLM Wiki Brainstorm
description: Resumes the mid-session brainstorm on extending WOS to implement the LLM wiki pattern, starting from the unanswered A/B clarifying question
related:
  - docs/research/2026-04-09-llm-wiki-knowledge-base-pattern.research.md
---

<context>
This is a resumed Claude Code session. The following work has been completed in this repo (/Users/bbeidel/Documents/git/wos):

1. Research completed — `docs/research/2026-04-09-llm-wiki-knowledge-base-pattern.research.md` contains a full landscape research of how developers implement the "LLM wiki" pattern (Karpathy's gist: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f). Key findings: ingest/query/lint operations are universal; the schema document is the decisive artifact; index.md navigation scales to an uncertain threshold (100-500 pages depending on source); MCP and AGENTS.md portability are complementary strategies.

2. Brainstorm started — A `/wos:brainstorm` session on "How should WOS be extended to implement the LLM wiki pattern?" reached Step 1 (Understand Intent) and paused at an unanswered clarifying question:

> Is the goal:
> - **A)** WOS becomes a wiki tool — users point WOS at any project and get ingest/query/lint skills for managing a knowledge base of context documents. WOS is the tool, users bring their own wikis.
> - **B)** WOS improves its own internal context management — adopt wiki patterns (confidence scoring, staleness detection, typed page relationships) to make the existing `docs/context/` layer more robust. WOS's own docs are the wiki.

The user has not yet answered this question.
</context>

<task>
Resume the `/wos:brainstorm` session exactly where it paused:

1. Present the A/B question above to the user and wait for their answer before proceeding.
2. Read `docs/research/2026-04-09-llm-wiki-knowledge-base-pattern.research.md` for full research context before diverging into approaches.
3. Once the user answers, continue the brainstorm workflow: diverge into 2-3 approaches with tradeoffs → converge on a recommendation → produce a design spec → get user approval → hand off to `/wos:write-plan`.
</task>

<constraints>
- Do not re-run the research — it is already complete at the path above.
- Do not invoke `/wos:write-plan` until the brainstorm design is explicitly approved by the user.
- Follow the `/wos:brainstorm` workflow exactly: understand → diverge → converge → spec → review → hand off.
- Do not start writing a plan or implementation — this is a design session only.
</constraints>
