---
name: Resolver Repair Playbook (check-resolver)
description: Per-finding repair recipes for check-resolver — canonical fixes for Tier-1 artifact/path findings, Tier-2 semantic dimensions, and Tier-3 reachability/staleness.
---

# Resolver Repair Playbook

Every FAIL and WARN finding maps to a canonical repair. Before applying, state the original intent: **"This resolver routes [filing type] to [location] / [task] to [doc bundle]."** If the repair would change the routing (not just how the row is phrased), flag for human review.

## Table of Contents

- [Tier 1: Deterministic Repairs](#tier-1-deterministic-repairs)
- [Tier 2: Semantic Dimensions](#tier-2-semantic-dimensions)
  - [Dimension 1: Filing Coverage](#dimension-1-filing-coverage)
  - [Dimension 2: Context Actionability](#dimension-2-context-actionability)
  - [Dimension 3: Eval Representativeness](#dimension-3-eval-representativeness)
- [Tier 3: Cross-Artifact](#tier-3-cross-artifact)

---

## Tier-1 — Deterministic Repairs

### Signal: `pointer-present` — AGENTS.md does not reference RESOLVER.md

**CHANGE:** Add a one-line pointer to AGENTS.md
**FROM:** `AGENTS.md` with no `RESOLVER.md` reference
**TO:** Insert after the first major section (commonly "Context Navigation"):
> Before filing new content or loading context beyond a skill's eager `references:`, consult `RESOLVER.md`.
**REASON:** Without the AGENTS.md anchor, the resolver is unreachable from the root of the context — a file no session opens.

### Signal: `pointer-resolves` — AGENTS.md references a non-existent path

**CHANGE:** Correct the path or move RESOLVER.md to the referenced location
**FROM:** pointer names `docs/RESOLVER.md` but file lives at `./RESOLVER.md`
**TO:** Either update the pointer to `./RESOLVER.md` or move the file to `docs/RESOLVER.md`
**REASON:** A dangling pointer gives the worst of both worlds — the surface says the resolver is reachable while it silently isn't.

### Signal: `markers-present` — managed-region markers missing or unbalanced

**CHANGE:** Restore `<!-- resolver:begin -->` and `<!-- resolver:end -->` around the filing/context/out-of-scope section; regenerate via `/build:build-resolver --regenerate`
**REASON:** Without markers, regeneration stomps human prose and the auditor cannot distinguish disk-derived content from hand edits.

### Signal: `filing-paths-resolve` — filing row points at a non-existent directory

**CHANGE:** Remove the row (if the directory was intentionally deleted) or restore the directory (if it should exist)
**FROM:** Filing row `| design | .designs/ | … |` with no `.designs/` on disk
**TO:** Either delete the row or `mkdir .designs/` and seed it with a file matching the row's naming pattern
**REASON:** A filing row that doesn't resolve routes new content into nothing.

### Signal: `context-paths-resolve` — context bundle points at missing path

**CHANGE:** Update the path to its current location (file or directory), or remove the entry from the bundle
**FROM:** Bundle lists `_shared/references/hook-best-practices.md` at path no longer present
**TO:** Correct to `plugins/build/_shared/references/hook-best-practices.md` (or remove). A directory entry like `.research/` is also valid — the agent uses Glob on the directory's naming pattern and reads frontmatter to find the right file.
**REASON:** Broken context loads train Claude to skip the resolver.

### Signal: `filing-rows-unique` — duplicate filing rows

**CHANGE:** Merge the duplicates, keeping the more specific location
**FROM:** Two filing rows both using content-type `research`, one pointing at `.research/` and one at `.docs/research/`
**TO:** One row. If both locations are real, promote to a glob pattern or rename one content-type to disambiguate.
**REASON:** Two rows routing the same content-type produce inconsistent filing decisions.

### Signal: `context-rows-unique` — duplicate context rows

**CHANGE:** Merge the duplicates, keeping the broader or more recent bundle
**FROM:** Two context rows both for task `authoring a hook`, with overlapping but non-identical doc lists
**TO:** One row listing the union (capped at 1–4 entries per Dimension 2)
**REASON:** Two rows for the same task produce inconsistent context loads.

### Signal: `evals-parse` — `.resolver/evals.yml` does not parse

**CHANGE:** Fix the YAML error (most often an unescaped quote or inconsistent indentation); re-run `/build:check-resolver`
**REASON:** An unparseable eval file is equivalent to no evals.

### Signal: `mtime-stale` — RESOLVER.md older than 90 days

**CHANGE:** Run `/build:build-resolver --regenerate` to refresh the managed region against current disk state
**REASON:** Long-stale resolvers drift from the directories they claim to route.

### Signal: `eval-pass-stale` — last eval-pass older than 30 days

**CHANGE:** Run `/build:check-resolver --run-evals`; fix failing cases (resolver or evals, depending on which drifted)
**REASON:** Untested routing is unproven routing; staleness thresholds are conservative and tunable.

---

## Tier-2 — Semantic Dimensions

### Dimension 1: Filing Coverage

**Signal:** Dark capability — directory exists on disk, not in filing table or out-of-scope list.

**CHANGE:** Classify the directory explicitly — add as a filing row or to out-of-scope
**FROM:** `.inbox/` present with 10 files; no classification
**TO:** Either `| inbox note | .inbox/ | <slug>.md |` in filing table, or `- .inbox/ — transient ingress` in out-of-scope
**REASON:** Silence is ambiguous; explicit classification is load-bearing.

**Signal:** Filing row matches only one of several same-purpose directories.

**CHANGE:** Widen the row (glob-style location) or add siblings
**FROM:** `| research | .research/public/ | ... |` when `.research/private/` also holds research
**TO:** `| research | .research/ (including subdirectories) | ... |` or add a second row
**REASON:** Unclassified siblings become dark capabilities.

### Dimension 2: Context Actionability

**Signal:** Context row names prose instead of paths.

**CHANGE:** Replace prose with concrete paths
**FROM:** `| building APIs | read the style guide |`
**TO:** `| building APIs | [docs/api-style.md, docs/api-examples.md] |`
**REASON:** Prose pointers fail silently; concrete paths are auditable.

**Signal:** Bundle is empty or has >6 entries.

**CHANGE:** Narrow to 1–4 load-bearing entries (files or directories)
**REASON:** Empty bundles defeat the purpose; large bundles equal "just look everywhere" and waste context budget. A directory counts as one entry — the agent uses Glob on the naming pattern and reads frontmatter to find the right file.

### Dimension 3: Eval Representativeness

**Signal:** Fewer eval cases than filing rows.

**CHANGE:** Add ≥1 positive case per filing row
**REASON:** Untested rows are unproven rows; coverage is the baseline.

**Signal:** Zero negative cases.

**CHANGE:** Add 1–2 negative cases per overlap-prone row
**FROM:** All 8 cases of shape `"save X" → .research/`
**TO:** Add `"save this raw webhook payload" → .raw/` and `"save this stripe config" → NOT .research/`
**REASON:** Negative cases catch the false-positive failure mode; pure positive-case evals can't detect overlap drift.

**Signal:** All cases filing, no context (or vice versa).

**CHANGE:** Add cases from the missing side in proportion to the table sizes
**REASON:** Coverage gaps hide routing defects in the uncovered table.

---

## Tier-3 — Cross-Artifact

### Signal: dark capabilities — directory on disk not classified

**CHANGE:** Classify the directory explicitly — add it as a filing row, a context-load target, or an out-of-scope entry
**FROM:** `.inbox/` present at repo root with 10 files; no entry in filing, context, or out-of-scope
**TO:** Either `| inbox note | .inbox/ | <slug>.md |` in filing table, or `- .inbox/ — transient ingress` in out-of-scope
**REASON:** Unclassified directories are capabilities Claude can't reach. Silence is ambiguous; explicit classification is load-bearing. Cross-references Dimension 1 (Filing Coverage) — the Tier-3 scan is what raises the dark-capability finding; the repair recipe is shared.

### Signal: drift between managed region and fresh regeneration

**CHANGE:** Run `/build:build-resolver --regenerate` and commit the resulting diff
**REASON:** The managed region is a build artifact; drift indicates either a new directory the resolver doesn't know about or a hand-edit that survived until the next build.

### Signal: eval execution failure

**Filing case failed:** the chosen location does not match `expected_filing`.

**CHANGE:** One of two diagnoses —
- If the resolver is correct and the eval is wrong → update the eval's `expected_filing`
- If the eval is correct and the resolver drifted → correct the filing row or add a missing row
**REASON:** An eval failure is a drift signal, not always a bug in the resolver; diagnose before repairing.

**Context case failed:** expected doc paths did not surface.

**CHANGE:** Same diagnosis shape — update the eval's `expected_context`, or correct the context-row bundle.
