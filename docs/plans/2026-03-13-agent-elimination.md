---
name: Agent Elimination
description: Remove static agent definitions and compose subagent prompts dynamically from enriched reference files and MANIFEST.md
type: plan
status: completed
related:
  - docs/designs/2026-03-13-agent-elimination-design.md
  - docs/designs/2026-03-13-composable-pipeline-design.md
  - skills/_shared/references/MANIFEST.md
  - skills/research/SKILL.md
  - skills/distill/SKILL.md
---

# Agent Elimination

**Goal:** Remove all 9 static agent definitions (`agents/`) and compose
equivalent subagent prompts dynamically from enriched reference files +
MANIFEST.md. Zero information loss, single source of truth for all stage
knowledge.

**Scope:**

Must have:
- All 11 primary reference files enriched with `tools:` frontmatter, expanded
  Input/Output sections, and Constraints sections
- Stage-specific behavioral guidance migrated from agents to reference files
- Context Model section added to self-verify-claims.md (verifier isolation note)
- MANIFEST.md updated with Tools, Entry Gate, and Role columns
- Research SKILL.md updated with prompt composition dispatch instructions
- Distill SKILL.md updated with prompt composition dispatch instructions
- All 9 agent files deleted
- All tests passing, audit clean
- Zero information loss from agent files

Won't have:
- Automated prompt composition script (orchestrator composes manually from
  instructions in SKILL.md)
- Changes to gate check logic (assess_research.py unchanged)
- Changes to inline execution path (already reads reference files directly)
- Changes to test fixtures (gate assertions unchanged)

**Approach:** Work in three phases: first enrich all reference files with
agent-unique content (agents still exist as safety net), then update
MANIFEST.md and SKILL.md dispatch logic, then delete agents/ and clean up.
Each phase is independently verifiable and rolls back cleanly.

**File Changes:**
- Modify: `skills/_shared/references/research/frame.md`
- Modify: `skills/_shared/references/research/gather-and-extract.md`
- Modify: `skills/_shared/references/research/evaluate-sources-sift.md`
- Modify: `skills/_shared/references/research/challenge.md`
- Modify: `skills/_shared/references/research/synthesize.md`
- Modify: `skills/_shared/references/research/self-verify-claims.md`
- Modify: `skills/_shared/references/research/finalize.md`
- Modify: `skills/_shared/references/distill/mapping-guide.md`
- Modify: `skills/_shared/references/distill/distillation-guidelines.md`
- Modify: `skills/_shared/references/MANIFEST.md`
- Modify: `skills/research/SKILL.md`
- Modify: `skills/distill/SKILL.md`
- Delete: `agents/research-framer.md`
- Delete: `agents/research-gatherer.md`
- Delete: `agents/research-evaluator.md`
- Delete: `agents/research-challenger.md`
- Delete: `agents/research-synthesizer.md`
- Delete: `agents/research-verifier.md`
- Delete: `agents/research-finalizer.md`
- Delete: `agents/distill-mapper.md`
- Delete: `agents/distill-worker.md`

**Branch:** `feat/agent-elimination`
**PR:** TBD

---

## Chunk 1: Enrich Research Reference Files

### Task 1: Enrich frame.md (framer)

**Files:**
- Modify: `skills/_shared/references/research/frame.md`
- Source: `agents/research-framer.md`

Migrate unique framer agent content into frame.md:

- [x] Add `tools:` frontmatter field: `[Read, Glob, Grep]`
- [x] Expand Input section with structured dispatch format (research
      question, stated constraints, project root path)
- [x] Add Step 7 to methodology: suggest output path
      (`docs/research/YYYY-MM-DD-<slug>.md`)
- [x] Expand Output section with 7 structured items from agent output
      contract (restated question, mode, sub-questions, search strategy,
      constraints, brief, output path)
- [x] Add `## Constraints` section: read-only (no Write/Edit), no web
      searches, no user prompts
- [x] Verify: frame.md contains all unique content from research-framer.md
      (diff agent against reference, confirm no content loss)
- [x] Commit

### Task 2: Enrich gather-and-extract.md (gatherer)

**Files:**
- Modify: `skills/_shared/references/research/gather-and-extract.md`
- Source: `agents/research-gatherer.md`

Migrate unique gatherer agent content. This is the primary file for the
gather stage — Output covers the combined gather+verify result.

- [x] Add `tools:` frontmatter field: `[Read, Write, Edit, Glob, Grep,
      Bash, WebSearch, WebFetch]`
- [x] Expand Input section with structured dispatch format (DRAFT path,
      research brief fields, search strategy, mode, output path)
- [x] Add deferred sources comment format to methodology
      (`<!-- deferred: URL — reason -->`)
- [x] Expand Output section to cover combined gather+verify result
      (4 requirements: DRAFT with `type: research` + `<!-- DRAFT -->`,
      sources table with # | URL | Title | Author/Org | Date | Status,
      structured extracts for every sub-question, search protocol comment)
- [x] Add `## Constraints` section: do not evaluate or tier sources,
      do not synthesize, do not prompt the user
- [x] Verify: gather-and-extract.md contains all unique gatherer content
- [x] Commit

### Task 3: Enrich evaluate-sources-sift.md (evaluator)

**Files:**
- Modify: `skills/_shared/references/research/evaluate-sources-sift.md`
- Source: `agents/research-evaluator.md`

- [x] Add `tools:` frontmatter field: `[Read, Write, Edit, Glob, Grep, Bash]`
- [x] Expand Input section: path to DRAFT with gathered sources and
      verified URLs
- [x] Expand Output section with 3 requirements: Tier column with T1-T5,
      Status column updated, no untiered sources remaining
- [x] Add `## Constraints` section: do not search for new sources,
      do not synthesize findings, do not prompt the user
- [x] Verify: evaluate-sources-sift.md contains all unique evaluator content
- [x] Commit

### Task 4: Enrich challenge.md (challenger)

**Files:**
- Modify: `skills/_shared/references/research/challenge.md`
- Source: `agents/research-challenger.md`

- [x] Add `tools:` frontmatter field: `[Read, Write, Edit, Glob, Grep,
      Bash, WebSearch, WebFetch]`
- [x] Expand Input section: path to DRAFT with evaluated (tiered) sources
- [x] Add anti-anchoring prompt inline in ACH procedure: "Ask 'What would
      someone who disagrees propose?' and add it"
- [x] Add WebSearch/WebFetch authorization at end of Methodology: "You may
      use WebSearch and WebFetch to find counter-evidence"
- [x] Expand Output section with absence-as-valid-finding note: "If no
      counter-evidence is found, document that explicitly"
- [x] Add `## Constraints` section: do not modify findings or sources
      (challenge only), do not prompt the user
- [x] Verify: challenge.md contains all unique challenger content
- [x] Commit

### Task 5: Enrich synthesize.md (synthesizer)

**Files:**
- Modify: `skills/_shared/references/research/synthesize.md`
- Source: `agents/research-synthesizer.md`

- [x] Add `tools:` frontmatter field: `[Read, Write, Edit, Glob, Grep, Bash]`
- [x] Expand Input section: path to DRAFT with challenge section completed
- [x] Expand Output section with 3 requirements: findings by sub-question,
      confidence levels on every finding, source attribution for all claims
- [x] Add `## Constraints` section: do not search for new sources,
      do not modify prior sections, do not prompt the user
- [x] Verify: synthesize.md contains all unique synthesizer content
- [x] Commit

### Task 6: Enrich self-verify-claims.md (verifier)

**Files:**
- Modify: `skills/_shared/references/research/self-verify-claims.md`
- Source: `agents/research-verifier.md`

Most complex migration — verifier has context isolation note and spans
2 reference files. This is the primary file; Output covers combined
Phase 7+8 result.

- [x] Add `tools:` frontmatter field: `[Read, Write, Edit, Glob, Grep,
      Bash, WebFetch]`
- [x] Add `## Context Model` section before Methodology: verifier's context
      isolation paragraph ("You are the primary beneficiary of the per-agent
      context model...")
- [x] Expand Input section: path to DRAFT with findings section completed
- [x] Expand Output section to cover combined Phase 7+8 result
      (3 requirements: Claims table populated, no unverified cells,
      all claims resolved)
- [x] Add `## Constraints` section: WebFetch only for re-verification
      (no WebSearch), do not modify findings structure, do not prompt the user
- [x] Verify: self-verify-claims.md + citation-reverify.md together contain
      all unique verifier content. Verify human-review triggers list parity
      between agent and citation-reverify.md
- [x] Commit

### Task 7: Enrich finalize.md (finalizer)

**Files:**
- Modify: `skills/_shared/references/research/finalize.md`
- Source: `agents/research-finalizer.md`

- [x] Add `tools:` frontmatter field: `[Read, Write, Edit, Glob, Grep, Bash]`
- [x] Expand Input section: path to DRAFT with all claims verified
- [x] Add to Final Verification step: "Ensure unverifiable and human-review
      entries are annotated in the body"
- [x] Add to Format Search Protocol step: summary line format
      (`N searches across M sources, X found, Y used`)
- [x] Expand Output section with 4 requirements: DRAFT marker removed,
      `type: research` in frontmatter, non-empty `sources:`, passes audit
- [x] Add `## Constraints` section: do not add new content, do not modify
      claims table, do not prompt the user
- [x] Verify: finalize.md contains all unique finalizer content
- [x] Commit

---

## Chunk 2: Enrich Distill Reference Files

### Task 8: Enrich mapping-guide.md (distill-mapper)

**Files:**
- Modify: `skills/_shared/references/distill/mapping-guide.md`
- Source: `agents/distill-mapper.md`

Primary file for the map stage. Output covers the full mapper contract.

- [x] Add `tools:` frontmatter field: `[Read, Glob, Grep]`
- [x] Expand Input section with structured dispatch format (research
      document paths, target area root, user constraints)
- [x] Expand Output section with 7 items from agent output contract
      (finding summary, source paths, target filename, target area,
      word count, one-concept test result, confidence carry-forward)
- [x] Add `## Constraints` section: do not write files (return proposal
      to dispatcher), do not modify research documents, do not prompt user
- [x] Verify: mapping-guide.md contains all unique mapper content
- [x] Commit

### Task 9: Enrich distillation-guidelines.md (distill-worker)

**Files:**
- Modify: `skills/_shared/references/distill/distillation-guidelines.md`
- Source: `agents/distill-worker.md`

- [x] Add `tools:` frontmatter field: `[Read, Write, Edit, Glob, Grep, Bash]`
- [x] Expand Input section with structured dispatch format (assigned
      findings, source research paths, target file paths + areas,
      estimated word counts)
- [x] Add frontmatter template (YAML example) to methodology
- [x] Add bidirectional linking step to methodology
- [x] Add reindex and validate step to methodology (with bash commands)
- [x] Expand Output section with 4 items: valid frontmatter, 200-800 words
      (advisory), passes audit, bidirectional related links
- [x] Add `## Constraints` section: do not modify source research documents,
      do not drop or dilute verified findings, do not prompt the user
- [x] Verify: distillation-guidelines.md contains all unique worker content
- [x] Commit

---

## Chunk 3: Update MANIFEST.md and SKILL.md

### Task 10: Update MANIFEST.md schema

**Files:**
- Modify: `skills/_shared/references/MANIFEST.md`

Add Tools, Entry Gate, and Role columns to both pipeline tables.

- [x] Replace Research Pipeline References table with expanded 6-column
      version (Stage, Role, Files, Tools, Entry Gate, Purpose)
- [x] Replace Distill Pipeline References table with expanded 6-column
      version
- [x] Verify: every stage has a Role, Tools list, and Entry Gate (or `—`)
- [x] Cross-check: MANIFEST.md Tools column matches `tools:` frontmatter
      in each primary reference file
- [x] Commit

### Task 11: Update research SKILL.md dispatch logic

**Files:**
- Modify: `skills/research/SKILL.md`

Update dispatch instructions to compose prompts from reference files
instead of dispatching named agents.

- [x] Update Step 2 heading to "Compose and Dispatch Framer"
- [x] Update Step 2 body: read framer reference files per MANIFEST.md,
      compose prompt (role + input + methodology + output + constraints),
      dispatch with tools from MANIFEST.md
- [x] Update Step 4 delegate path: replace "Dispatch the named agent
      (e.g., `research-gatherer`)" with compose-from-references instruction
- [x] Update delegate code block to remove named agent references
- [x] Update announcement example to show composed dispatch
- [x] Preserve inline path unchanged
- [x] Verify: no references to `research-framer`, `research-gatherer`,
      `research-evaluator`, `research-challenger`, `research-synthesizer`,
      `research-verifier`, or `research-finalizer` agent names remain
- [x] Verify: SKILL.md body line count stays under 500
- [x] Commit

### Task 12: Update distill SKILL.md dispatch logic

**Files:**
- Modify: `skills/distill/SKILL.md`

- [x] Update Step 2: compose mapper prompt from mapping-guide.md +
      distillation-guidelines.md per MANIFEST.md, dispatch with
      tools from MANIFEST.md
- [x] Update Step 4 delegate path: compose worker prompt from
      distillation-guidelines.md per MANIFEST.md
- [x] Verify: no references to `distill-mapper` or `distill-worker`
      agent names remain
- [x] Commit

---

## Chunk 4: Delete Agents and Clean Up

### Task 13: Delete agents/ directory

**Files:**
- Delete: all 9 files in `agents/`

- [x] Delete `agents/research-framer.md`
- [x] Delete `agents/research-gatherer.md`
- [x] Delete `agents/research-evaluator.md`
- [x] Delete `agents/research-challenger.md`
- [x] Delete `agents/research-synthesizer.md`
- [x] Delete `agents/research-verifier.md`
- [x] Delete `agents/research-finalizer.md`
- [x] Delete `agents/distill-mapper.md`
- [x] Delete `agents/distill-worker.md`
- [x] Verify: `ls agents/` returns no such directory
- [x] Run: `uv run python -m pytest tests/ -v` — all tests pass
- [x] Commit

### Task 14: Update documentation references

**Files:**
- Modify: `docs/designs/2026-03-13-composable-pipeline-design.md` (update
  appendix — "What Does NOT Change" said agent definitions unchanged)

- [x] Update composable pipeline design doc appendix to note agent
      definitions were subsequently eliminated
- [x] Verify: no stale operational references to `agents/` in AGENTS.md,
      CLAUDE.md, or skills/ (docs/research and docs/context references
      are informational and don't need updating)
- [x] Commit

---

## Validation

- [x] `uv run python -m pytest tests/ -v` — all tests pass (no regressions)
- [x] `uv run python -m pytest tests/test_research_gates.py -v` — all gate
      fixture tests pass
- [x] `uv run scripts/audit.py --root .` — no new failures
- [x] `agents/` directory does not exist
- [x] MANIFEST.md has 6 columns (Stage, Role, Files, Tools, Entry Gate, Purpose)
      for both pipeline tables
- [x] All 9 primary reference files have `tools:` frontmatter + Constraints section
- [x] self-verify-claims.md has `## Context Model` section
- [x] Research SKILL.md contains no named agent references (research-framer, etc.)
- [x] Distill SKILL.md contains no named agent references (distill-mapper, etc.)
- [x] Research SKILL.md body under 500 lines
- [x] Every piece of unique agent content has been migrated per the
      information migration table in the design doc
