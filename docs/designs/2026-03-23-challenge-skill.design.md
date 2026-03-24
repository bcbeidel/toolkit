---
name: Challenge Skill
description: Design for /wos:challenge — a skill that enumerates assumptions behind an output, sanity-checks them against project context and research, and proposes corrections for gaps
type: design
status: draft
related:
  - docs/context/validation-architecture.md
  - docs/context/reads-writes-separation.md
  - docs/context/human-in-the-loop-design.md
  - docs/context/preview-before-execute.md
  - docs/context/show-your-work-patterns.md
  - docs/research/source-evaluation-claim-verification.md
---

## Purpose

Create `/wos:challenge`, a skill that surfaces implicit assumptions and
reasoning behind a specific output or recent conversation, then checks those
assumptions against the project's context and research documents. Where
assumptions conflict with evidence or lack coverage, it proposes specific
corrections for user approval.

The skill sits in the feedback layer — independent of the delivery pipeline but
recommended at key checkpoints (post-design, post-plan).

## Trigger

**Skill name:** `challenge`
**Prefix:** `/wos:challenge`
**User-invocable:** yes

**Trigger phrases:** "check your assumptions", "challenge this", "what are you
assuming", "sanity check", "ground check", "challenge reasoning", "what
assumptions", "verify reasoning"

## Input Modes

**Conversation mode:** No argument. The skill introspects on the most recent
substantive output in the current session and extracts assumptions from it.

**Artifact mode:** User provides a file path or quotes specific output. The
skill operates on that artifact.

## Lifecycle Position

Independent (feedback layer). Not gated by upstream status. Recommended at:

- After `/wos:brainstorm` produces a design, before `/wos:write-plan`
- After `/wos:write-plan` produces a plan, before `/wos:execute-plan`
- Any time the user wants to pressure-test reasoning

Other skills may suggest running `/wos:challenge` at these points but never
invoke it automatically. Always user-triggered.

## Workflow

Four sequential phases with user gates between Phase 1→2 and Phase 3→4.

### Phase 1 — Extract Assumptions

The LLM enumerates assumptions and reasoning from the input. Each assumption
is stated as a testable claim — specific, non-trivial, and falsifiable.

Output: numbered markdown list shared with the user.

**User gate:** "Here are the assumptions I identified. Want to add, remove, or
rephrase any before I check them?"

The user may modify the list. Numbering stabilizes after this gate and persists
through all subsequent phases.

### Phase 2 — Layered Search

For each assumption, find relevant context and research documents using two
layers:

1. **Explicit layer:** If the input is an artifact with `related` frontmatter,
   parse those paths and read the linked documents first.
2. **Broad layer:** Run `scripts/discover_context.py` to scan all `.md` files
   under `docs/context/` and `docs/research/`, matching each assumption
   against frontmatter `name` and `description` fields via keyword overlap
   scoring. Returns ranked candidate documents per assumption.

The LLM then reads matched documents and evaluates which assumptions each
document supports, contradicts, or is silent on.

No user-facing output in this phase — discovery happens behind the scenes.

The skill logs its search activity using the `SearchProtocol` pattern from
`wos/research_protocol.py`: which assumptions were searched, which documents
matched, which were read, and which produced evidence. This log is appended
as a collapsed details block below the gap analysis table in Phase 3, giving
the user an auditable record of the search process.

### Phase 3 — Gap Analysis

Present a summary table:

| # | Assumption | Status | Confidence | Evidence | Source |
|---|-----------|--------|------------|----------|--------|
| 1 | Users authenticate via OAuth | Aligned | High | Context confirms OAuth pattern | `docs/context/auth.md` |
| 2 | Rate limits are 1000 req/min | Gap | High | Research shows 500 req/min | `docs/research/api-limits.md` |
| 3 | Cache invalidation is eventual | No coverage | — | No docs address this | — |

**Statuses:**

- **Aligned** — A context or research document supports the assumption.
- **Gap** — A document contradicts or conflicts with the assumption.
- **No coverage** — No documents address the assumption.

**Confidence levels** (for Aligned and Gap statuses):

- **High** — Direct, specific evidence addressing the assumption. The source
  document explicitly discusses the same concept with a clear position.
- **Moderate** — Related evidence that bears on the assumption but doesn't
  address it directly. Requires inference to connect source to claim.
- **Low** — Tangential evidence. The connection is plausible but weak. The
  user should weigh carefully before acting on this classification.

No Coverage items have no confidence level (evidence is absent, not weak).

Below the table, a brief narrative: "X assumptions aligned, Y gaps found, Z
with no coverage."

Below the narrative, a collapsed `<details>` block containing the search
protocol log: which documents were searched, which matched each assumption,
and which were read in full. This supports auditability — users can verify
that the search was thorough and that classifications are grounded in actual
document reads, not hallucinated evidence.

### Phase 4 — Propose Corrections

For each Gap item, draft a specific correction:

- **Proposed correction:** Revised assumption text or concrete change to the
  artifact
- **Rationale:** Why, citing the source document
- **Action:** `accept` / `adjust` / `skip`

For each No Coverage item, recommend whether:

- Research is needed (suggest `/wos:research`)
- The assumption is safe to hold given current evidence

**User gate:** "Here are my proposed corrections. Approve, adjust, or skip
each one."

After the user responds, the skill applies accepted corrections to the artifact
(artifact mode) or summarizes the revised assumption set (conversation mode).
No automatic handoff to another skill.

## Architecture

### Approach: Hybrid (Skill + Python Module)

Follows "structure in code, quality in skills." Python handles deterministic
document discovery. The LLM handles judgment: extracting assumptions, evaluating
alignment, and proposing corrections.

### New Python Module: `wos/challenge/`

Builds on the existing `wos/discovery.py` module, which already handles
tree-walking and frontmatter parsing via `discover_documents(root)`. The
challenge module adds keyword-scoring on top — it does not duplicate discovery.

**`wos/challenge/__init__.py`** — Empty.

**`wos/challenge/discover.py`** — Assumption-to-document matching:

- `discover_related(artifact_path: str) -> list[Document]` — Parses the
  artifact's frontmatter, resolves `related` paths, returns parsed documents.
  Uses `parse_document()` from `wos/document.py`.
- `discover_by_relevance(assumptions: list[str], docs_root: str) -> dict[str, list[Document]]`
  — Calls `wos.discovery.discover_documents(docs_root)` to get all managed
  documents, then scores each against each assumption using keyword overlap
  (basic tokenization + set intersection on `name` and `description` fields).
  Returns mapping of assumption text → ranked candidate documents. The scoring
  interface is a callable `(assumption, document) -> float`, making it
  swappable for more sophisticated matching (e.g., TF-IDF, semantic) later
  without changing the module's API.

Reuses `discover_documents()` from `wos/discovery.py` and `parse_document()`
from `wos/document.py`. No new dependencies (stdlib only).

### New Script: `scripts/discover_context.py`

CLI entry point for the discovery module:

```
python scripts/discover_context.py --assumptions "claim 1" "claim 2" --root .
```

Optional `--artifact path/to/file.md` to include the explicit layer.

Output: JSON mapping each assumption to ranked matches:

```json
[
  {
    "assumption": "Users authenticate via OAuth",
    "matches": [
      {"path": "docs/context/auth.md", "name": "Auth Patterns", "description": "...", "score": 0.82}
    ]
  }
]
```

The script narrows the search space. The LLM reads matched docs and applies
judgment — the script does not evaluate alignment.

### Script Invocation from SKILL.md

The SKILL.md instructs the LLM to run the script via Bash during Phase 2:

1. LLM extracts the assumption list from Phase 1 as quoted strings.
2. LLM runs: `python <plugin-scripts-dir>/discover_context.py --assumptions "claim 1" "claim 2" --root <project-root>`
   (with `--artifact <path>` if in artifact mode).
3. LLM parses the JSON output to get ranked document matches per assumption.
4. LLM reads the top-scoring documents using the Read tool.
5. LLM evaluates alignment/gap/no-coverage using judgment.

This follows the same pattern as `/wos:audit-wos`, which runs
`python <plugin-scripts-dir>/audit.py` and interprets the output.

### Skill Directory

```
skills/challenge/
  SKILL.md
  references/
    assumption-quality.md    # What makes a well-stated assumption
    gap-analysis-guide.md    # How to evaluate alignment/gap/no-coverage
```

## Key Rules

1. **Read-only until approved.** No file edits or artifact modifications until
   the user explicitly approves corrections in Phase 4.
2. **Assumptions are numbered and stable.** Once shared in Phase 1, numbering
   persists through all phases. User references corrections by number.
3. **Show your sources.** Every alignment or gap claim cites a specific
   document path. "No coverage" is explicit, not a missing cell.
4. **Don't manufacture evidence.** If no doc addresses an assumption, report
   "No coverage." Don't stretch tangential docs to claim alignment.
5. **Artifact mode inherits context.** When pointed at a file with `related`
   frontmatter, those links are the starting point, not a ceiling.
6. **Conversation mode scopes to the recent exchange.** Focus on the most
   recent substantive output unless the user specifies otherwise.
7. **Corrections are proposals, not commands.** Frame as "Consider revising X
   to Y because Z." The user has final say.

## Edge Cases

- **No context/research docs exist:** Report clearly, skip Phases 2–3. Suggest
  `/wos:research` to build the knowledge base.
- **All assumptions aligned:** Present the table, done. No corrections phase.
- **Artifact has no frontmatter or no `related` field:** Skip the explicit
  layer, go straight to broad discovery. Not an error.
- **Too many assumptions (>15):** Ask the user to prioritize before proceeding.
- **User adds assumptions in Phase 1 gate:** Merge into the numbered list and
  proceed.
- **Zero assumptions extracted:** Report that no testable assumptions were
  identified. Ask the user if they want to supply assumptions manually or
  point to a different output.

## Integration Points

Documented in skill references, not enforced in code. Other skills may suggest
`/wos:challenge` at natural checkpoints:

- `/wos:brainstorm`: "Design approved. Want to `/wos:challenge` the
  assumptions before planning?"
- `/wos:write-plan`: "Plan ready. Want to `/wos:challenge` the reasoning
  before execution?"

Invocation is always user-triggered.
