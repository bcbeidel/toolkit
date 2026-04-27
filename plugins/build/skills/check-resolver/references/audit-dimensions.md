---
name: Audit Resolver Dimensions
description: Evaluation criteria for auditing a root-level resolver — Tier-1 deterministic artifact/path/parse checks, Tier-2 three-dimension semantic rubric mirroring the authoring principles, and Tier-3 cross-artifact reachability + staleness against disk.
---

# Audit Resolver Dimensions

Resolver auditing uses a three-tier hierarchy: deterministic checks first (no LLM), then semantic evaluation (one LLM call with a locked rubric), then cross-artifact reachability against the live filesystem.

Handle deterministic checks (pointer presence, path resolution, YAML parse, mtime) with code. The Tier-2 rubric mirrors the authoring principles in [resolver-best-practices.md](../../../_shared/references/resolver-best-practices.md).

## Table of Contents

- [Category Tiers](#category-tiers)
- [Tier 1: Deterministic Checks](#tier-1-deterministic-checks)
- [Tier 2: Semantic Dimensions (One LLM Call)](#tier-2-semantic-dimensions-one-llm-call)
  - [Dimension 1: Filing Coverage](#dimension-1-filing-coverage)
  - [Dimension 2: Context Actionability](#dimension-2-context-actionability)
  - [Dimension 3: Eval Representativeness](#dimension-3-eval-representativeness)
- [Tier 3: Cross-Artifact Checks](#tier-3-cross-artifact-checks)
- [Evaluation Prompt Template](#evaluation-prompt-template)
- [Output Format](#output-format)

---

## Category Tiers

| Tier | Meaning |
|------|---------|
| **canonical** | Enforces an artifact contract (pointer present, markers intact, paths resolve) |
| **principle** | Mirrors a principle from `resolver-best-practices.md` |
| **research-grounded** | Toolkit-opinion check whose design is supported by published evidence |

---

## Tier-1 — Deterministic Checks

| Script | Check ID | What | Severity | Source principle |
|---|---|---|---|---|
| `check_pointer.py` | `pointer-present` | `AGENTS.md` contains a reference to `RESOLVER.md` | FAIL | AGENTS.md pointer, not skill mandates |
| `check_pointer.py` | `pointer-resolves` | The path named in the pointer exists on disk | FAIL | AGENTS.md pointer, not skill mandates |
| `check_resolver.py` | `markers-present` | `<!-- resolver:begin -->` and `<!-- resolver:end -->` each appear exactly once | FAIL | Machine-managed region |
| `check_resolver.py` | `filing-paths-resolve` | Every directory in the filing table exists | FAIL | Disk-derived, not hand-curated |
| `check_resolver.py` | `context-paths-resolve` | Every doc path in the context table resolves to a file or directory | FAIL | Cross-link, don't restate |
| `check_resolver.py` | `filing-rows-unique` | No two filing rows share a content-type | FAIL | Two tables, one file |
| `check_resolver.py` | `context-rows-unique` | No two context rows share a task | FAIL | Two tables, one file |
| `check_evals.py` | `evals-parse` | `.resolver/evals.yml` is valid YAML with the expected schema | FAIL | Trigger evals prove routing |
| `check_resolver.py` | `dark-capability` | Every depth 1–2 directory is in filing, context, out-of-scope, ambient set, or contains a nested `RESOLVER.md` (delegation) | WARN | Reachability + staleness |
| `check_resolver.py` | `mtime-stale` | `RESOLVER.md` mtime older than 90 days | WARN | Reachability + staleness |
| `check_evals.py` | `eval-pass-stale` | Last recorded eval-pass timestamp older than 30 days | WARN | Reachability + staleness |

**Exclusion rule:** Any of the first five FAIL findings excludes the resolver from Tier 2 — a malformed or unreachable resolver shouldn't burn LLM budget.

---

## Tier-2 — Semantic Dimensions

Present all three dimensions as a locked rubric in a single call. Include `RESOLVER.md` verbatim, the directory scan output, and `.resolver/evals.yml`.

**Per-dimension calls are an anti-pattern** — per-criterion splits score 11.5 points lower (Hong et al., 2026, RULERS).

For each dimension: **verdict** (WARN, PASS, or N/A), **evidence**, **recommendation**. Default-closed on borderline.

---

### Dimension 1: Filing Coverage

*(principle — [Disk-derived, not hand-curated](../../../_shared/references/resolver-best-practices.md))*

**What it checks:** Does the filing table reflect the directories that actually exist? Dark capabilities — directories on disk not listed in the filing table and not in the out-of-scope list — are the "surgeon the hospital can't find" failure mode.

**Fail signals (→ WARN):**
- A tracked directory (one with frontmatter-tagged contents or a consistent naming pattern) exists but no filing row names it
- A filing row points at a directory type (e.g., "research") but multiple such directories exist and the row names only one
- Out-of-scope list is empty despite `.git/`, `node_modules/`, or similar ambient directories present

**Pass signals:**
- Every depth-1 directory classified (in filing, in context, in out-of-scope, or in the ambient default list)
- Filing rows match the directory's frontmatter `type:` or naming-pattern purpose

**Canonical Repair:** See `repair-playbook.md` → Dimension 1.

---

### Dimension 2: Context Actionability

*(principle — [Cross-link, don't restate](../../../_shared/references/resolver-best-practices.md))*

**What it checks:** Does each context-table row name concrete paths (files or directories), not vague prose? Is the bundle size appropriate — enough to compress useful context, not so many that the bundle defeats the purpose?

**Fail signals (→ WARN):**
- A context row's column contains prose ("the style guide") without a resolvable path
- A bundle lists zero entries (empty right-hand column)
- A bundle lists >6 entries (approaching a "just look everywhere" pattern)

**Pass signals:**
- Each bundle lists 1–4 concrete entries (files or directories)
- Each entry resolves to a real path; directories follow the convention of being explored via Glob on the directory's naming pattern + frontmatter Read
- Bundle scope matches the task named (authoring a hook points at hook + routing, not the whole style guide)

**Canonical Repair:** See `repair-playbook.md` → Dimension 2.

---

### Dimension 3: Eval Representativeness

*(principle — [Trigger evals prove routing](../../../_shared/references/resolver-best-practices.md); research-grounded — OpenAI skill-eval guidance on positive + negative trigger coverage)*

**What it checks:** Do the evals exercise both filing and context routing? Is there at least one case per filing row? Are there negative cases catching overlap?

**Fail signals (→ WARN):**
- Fewer than 1 eval case per filing row
- Zero negative cases (every case is "X routes to Y"; none are "X does NOT route to Z")
- All cases are filing; none are context (or vice versa)
- Cases duplicate (same prompt tested twice with the same expected outcome)

**Pass signals:**
- ≥1 positive case per filing row
- ≥15% negative cases
- Mix of filing and context cases proportional to the respective table sizes

**Canonical Repair:** See `repair-playbook.md` → Dimension 3.

---

## Tier-3 — Cross-Artifact Checks

*(principle — [Reachability + staleness](../../../_shared/references/resolver-best-practices.md))*

### Signal: drift between managed region and fresh regeneration

**What it checks:** Simulate a fresh regeneration of the managed region (same disk scan `build-resolver` would run) and diff against the current managed region.

**Fail signals (→ WARN):** Non-empty diff — "filing table drifted from disk; regenerate".

**Pass signals:** Fresh regeneration produces no diff against the stored managed region.

**Canonical Repair:** See `repair-playbook.md` → Signal: drift between managed region and fresh regeneration.

### Signal: dark capabilities — directory on disk not classified

**What it checks:** For every depth 1–2 directory, classify as: in-filing, in-context, in-out-of-scope, ambient (baked-in list: `.git/`, `node_modules/`, `dist/`, `build/`, `.cache/`, `.venv/`, `target/`, `__pycache__/`, `.resolver/`), or *delegated* (the directory contains a nested `RESOLVER.md`). Unclassified directories are "dark capabilities" — reachable on disk but invisible to Claude's filing decisions. Subdirectories of a filing dir are *not* auto-classified — the filing rule names files directly inside.

**Mechanized.** This signal is implemented deterministically by `check_resolver.py` (Tier 1, `dark-capability`) and surfaces here as a Tier-3 cross-reference; the LLM rubric does not re-evaluate it.

**Fail signals (→ WARN):** Depth 1–2 directory exists with no row in filing, context, or out-of-scope; not in the ambient default list; no nested `RESOLVER.md` inside.

**Pass signals:** Every depth 1–2 directory is classified.

**Canonical Repair:** See `repair-playbook.md` → Dimension 1: Filing Coverage.

### Signal: eval execution failure

**What it checks:** (Opt-in via `--run-evals`.) For each case in `.resolver/evals.yml`:
- **Filing case:** pose the prompt to a Claude call with `RESOLVER.md` in context; compare the chosen location against `expected_filing`.
- **Context case:** check whether the resolver's context table surfaces the expected doc paths for the named task.

**Fail signals (→ WARN):** Chosen location does not match `expected_filing`; expected doc paths do not surface.

**Pass signals:** All eval cases pass. Pass timestamp stored in `.resolver/.eval-pass` for the `eval-pass-stale` Tier-1 check.

**Canonical Repair:** See `repair-playbook.md` → Signal: eval execution failure.

---

## Evaluation Prompt Template

```
You are auditing a resolver (RESOLVER.md, AGENTS.md pointer, .resolver/evals.yml) against three dimensions. Evaluate all three in a single response.

Directory scan results for this repo:
<bulleted list of depth 1-2 directories, each tagged with naming-pattern / frontmatter-type presence and file count>

For each dimension:
1. Quote the specific text from RESOLVER.md or evals.yml that is most relevant (evidence)
2. Explain your reasoning
3. State your verdict: WARN, PASS, or N/A
4. Give a specific Recommendation if WARN

When evidence is borderline, surface as WARN, not PASS.

---

## Dimension 1: Filing Coverage
Criterion: Does the filing table (plus out-of-scope list) classify every directory that exists on disk, modulo ambient directories?

PASS anchor: every .research/, .plans/, .designs/ has a filing row; .git/ and node_modules/ are ambient (not flagged)
FAIL anchor: .inbox/ exists on disk with 10 files; no filing row names it; no out-of-scope entry

## Dimension 2: Context Actionability
Criterion: Does each context row list 1-4 concrete entries (files or directories) that resolve?

PASS anchor: "authoring a hook" → [_shared/references/primitive-routing.md, _shared/references/hook-best-practices.md]
PASS anchor: "planning research" → [.research/]   (directory entry; agent uses Glob + frontmatter Read)
FAIL anchor: "building features" → "read the style guide"

## Dimension 3: Eval Representativeness
Criterion: >=1 case per filing row; >=15% negative cases; mix of filing and context.

PASS anchor: 12 cases covering all 5 filing rows plus 3 context rows, with 2 negative cases
FAIL anchor: 5 cases all positive filing, no context cases, no negative cases

---

<RESOLVER.md verbatim>
<.resolver/evals.yml verbatim>
<directory scan output>

---

Output format (one block per dimension):
## Dimension N: [Name]
Evidence: "[quoted text]"
Reasoning: [your reasoning]
Verdict: WARN | PASS | N/A
Recommendation: [specific change if WARN, else "None"]
```

---

## Output Format

All findings use the standard lint format:

```
FAIL  RESOLVER.md — filing path .designs/ does not resolve
WARN  RESOLVER.md — dark capability: .inbox/ not classified
WARN  .resolver/evals.yml — no negative cases in 8 rows
```

Sort order: Tier-1 FAIL → Tier-2 FAIL → Tier-3 FAIL → Tier-1 WARN → Tier-2 WARN → Tier-3 WARN; ties break alphabetically by artifact path.

Final summary: `Resolver audited, N findings (X fail, Y warn)` or `Resolver audited — no findings`.
