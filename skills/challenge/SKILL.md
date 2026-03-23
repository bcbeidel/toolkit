---
name: challenge
description: >
  Surfaces and sanity-checks assumptions behind an output or recent
  conversation against project context and research documents. Use when
  the user asks to "check your assumptions", "challenge this", "what are
  you assuming", "sanity check", "ground check", "challenge reasoning",
  "what assumptions", or "verify reasoning".
argument-hint: "[file path or quoted output]"
user-invocable: true
references:
  - references/assumption-quality.md
  - references/gap-analysis-guide.md
---

# /wos:challenge

Surface implicit assumptions, check them against project knowledge, and
propose corrections where evidence conflicts or is absent.

## Input

Two modes based on arguments:

- **No argument (conversation mode):** Extract assumptions from the most
  recent substantive output in the current session.
- **File path or quoted text (artifact mode):** Extract assumptions from
  the specified artifact. If the file has `related` frontmatter, those
  linked documents are searched first.

## Workflow

Four phases. Do not skip phases or combine them.

### Phase 1 — Extract Assumptions

Read the input (conversation output or artifact) and enumerate every
implicit assumption and piece of reasoning as a numbered list. Each
assumption must be a testable, specific, non-trivial claim. See
@assumption-quality.md for quality criteria.

Present the numbered list to the user:

> "Here are the assumptions I identified. Want to add, remove, or
> rephrase any before I check them?"

**Wait for the user.** Do not proceed to Phase 2 until the user confirms
or modifies the list. Numbering stabilizes after this gate.

If zero assumptions are extracted, report this and ask the user if they
want to supply assumptions manually or point to a different output. Do
not proceed.

If more than 15 assumptions are extracted, ask the user to prioritize
before proceeding.

### Phase 2 — Layered Search

Run the discovery script to find relevant documents:

```bash
python <plugin-scripts-dir>/discover_context.py \
  --assumptions "assumption 1" "assumption 2" ... \
  --root <project-root>
```

If in artifact mode with a file path, add `--artifact <path>`.

Parse the JSON output. For each assumption, read the top-scoring
documents (up to 5 per assumption) using the Read tool. Evaluate which
assumptions each document supports, contradicts, or is silent on.

Log each search step for the search protocol:
- Which assumptions were searched
- Which documents matched (with scores)
- Which documents were read in full
- What evidence was extracted

No user-facing output in this phase.

### Phase 3 — Gap Analysis

Present a summary table:

| # | Assumption | Status | Confidence | Evidence | Source |
|---|-----------|--------|------------|----------|--------|
| 1 | ... | Aligned | High | ... | `path` |
| 2 | ... | Gap | Moderate | ... | `path` |
| 3 | ... | No coverage | — | ... | — |

See @gap-analysis-guide.md for classification rules and confidence
level definitions.

Below the table, write a one-line narrative:
"X assumptions aligned, Y gaps found, Z with no coverage."

Below the narrative, add a collapsed search protocol log:

```markdown
<details>
<summary>Search protocol</summary>

[Table of searches performed, documents matched, documents read]

</details>
```

If all assumptions are aligned, present the table and stop. Do not
proceed to Phase 4.

### Phase 4 — Propose Corrections

For each **Gap** item, draft:
- **Proposed correction:** Revised assumption or artifact change
- **Rationale:** Why, citing the source document
- **Action:** `accept` / `adjust` / `skip`

For each **No Coverage** item, recommend:
- Whether research is needed (suggest `/wos:research`)
- Whether the assumption is safe to hold

Present all proposals:

> "Here are my proposed corrections. Approve, adjust, or skip each one."

**Wait for the user.** Do not edit any files until the user responds.

After user approval:
- **Artifact mode:** Apply accepted corrections to the artifact file.
- **Conversation mode:** Summarize the revised assumption set.

## Key Rules

1. **Read-only until Phase 4 approval.** No file edits until the user
   explicitly approves corrections.
2. **Numbering is stable.** Once shared in Phase 1, assumption numbers
   persist through all phases.
3. **Show your sources.** Every classification cites a document path.
   "No coverage" is explicit, not a missing cell.
4. **Don't manufacture evidence.** If no doc addresses an assumption,
   report No Coverage. Don't stretch tangential docs.
5. **Conversation mode scopes to the recent exchange.** Don't reach back
   through the entire session unless the user asks.
6. **Corrections are proposals.** Frame as "Consider revising X to Y
   because Z." The user has final say.
