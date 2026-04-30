---
name: check-resolver
description: Audit a root-level resolver — verify AGENTS.md pointer, managed-region integrity, filing-table coverage against disk, context-table actionability, and trigger-eval pass rate. Use when the user wants to "audit a resolver", "check RESOLVER.md", "validate routing table", "find dark capabilities", or "are my filing rules current".
argument-hint: "[target directory — defaults to CWD; walks up to the nearest RESOLVER.md and audits that one]"
user-invocable: true
references:
  - ../../_shared/references/resolver-best-practices.md
  - references/audit-dimensions.md
  - references/repair-playbook.md
license: MIT
---

# /build:check-resolver

Evaluate a root-level resolver in three tiers: deterministic artifact and path checks (no LLM), per-dimension semantic evaluation (one locked-rubric LLM call), and cross-artifact reachability + staleness against disk state.

The audit rubric mirrors the authoring principles in [resolver-best-practices.md](../../_shared/references/resolver-best-practices.md). When the principles doc changes, the dimensions follow.

## Workflow

### 1. Discover Resolver Artifacts

Walk up from the target directory looking for `RESOLVER.md`. The first ancestor that has one becomes the **resolver root** for this audit; all checks scope to that resolver and its subtree.

Locate three artifacts at the resolver root:
- `RESOLVER.md`
- `AGENTS.md` (for the pointer check) — at the resolver root
- `.resolver/evals.yml` — sibling to `RESOLVER.md` under the resolver root

Report: "Found resolver at <resolver root>. Auditing N filing rows, M context rows, K eval cases."

If no `RESOLVER.md` is found anywhere up to the filesystem root, emit FAIL and stop — nothing to audit. To audit every resolver in a repo with nested resolvers, run this skill once per resolver root.

### 2. Tier 1 — Deterministic Checks

Tier-1 scripts (to be scaffolded via `/build:build-python-script` per Language Selection) produce findings in the standard `FAIL|WARN|INFO|HINT  <path> — <check>: <detail>` format. Until the scripts exist, Claude performs these checks inline:

| Check | Severity | Detail |
|---|---|---|
| AGENTS.md pointer present | FAIL | `RESOLVER.md` is referenced from `AGENTS.md` (text match) |
| AGENTS.md pointer resolves | FAIL | The path named in the pointer exists |
| Managed-region markers present | FAIL | Both `<!-- resolver:begin -->` and `<!-- resolver:end -->` appear exactly once |
| Filing-table paths resolve | FAIL | Every directory named in the filing table exists on disk |
| Context-table paths resolve | FAIL | Every doc path named in the context table exists |
| No duplicate filing rows | FAIL | Content-type column is unique across filing rows |
| No duplicate context rows | FAIL | Task column is unique across context rows |
| Eval file parses | FAIL | `.resolver/evals.yml` is valid YAML with the expected schema |
| File mtime threshold | WARN | `RESOLVER.md` mtime older than 90 days |
| Last-eval-pass threshold | WARN | Last recorded eval-pass older than 30 days |

Rules with a FAIL finding from the first five rows are **excluded from Tier 2** — a malformed or unreachable resolver shouldn't burn LLM budget.

### 3. Tier 2 — Semantic Dimensions (One LLM Call)

Present the three judgment dimensions from [audit-dimensions.md](references/audit-dimensions.md) as a locked rubric in one call. Include `RESOLVER.md` verbatim, the output of the directory scan, and the `.resolver/evals.yml` contents.

1. **Filing Coverage** — Does the filing table reflect the directories that actually exist on disk? Flag dark capabilities (directories not in table and not in out-of-scope list).
2. **Context Actionability** — Does each context row list at least one concrete doc path (not vague references)? Is the bundle size appropriate (1–4 docs)?
3. **Eval Representativeness** — Do the evals cover both filing and context routing? Are there negative cases? Is coverage ≥1 case per filing row?

Output per dimension: `evidence → reasoning → verdict (WARN or PASS) → recommendation`. Default-closed on borderline evidence.

### 4. Tier 3 — Cross-Artifact Checks

**Dark capabilities scan.** Mechanized in `check_resolver.py` as Tier-1 `dark-capability`. For every directory under the resolver root (depth 1–2 from that root), check whether it appears in the filing table, the context table, the out-of-scope list, the ambient default list (`.git`, `node_modules`, `dist`, `build`, `.cache`, `.venv`, `target`, `__pycache__`, `.resolver`), or contains a nested `RESOLVER.md` (delegation — that subtree belongs to the nested resolver, not this one). Anything unclassified → WARN. Subdirectories of a filing dir are not auto-classified.

**Staleness signal.** Compare `RESOLVER.md` mtime against a fresh regeneration output (simulated via the same scan `build-resolver` would run). Differences → WARN ("filing table drifted from disk; regenerate").

**Optional: Run evals.** When invoked with `--run-evals`, execute each case in `.resolver/evals.yml`:
- For filing cases: pose the prompt to a Claude call with RESOLVER.md in context and check whether the chosen location matches `expected_filing`.
- For context cases: check whether the resolver surfaces the expected doc paths.
- Emit one finding per failing case.

### 5. Report Findings

Output all findings in file/issue/severity format. Sort: Tier-1 FAIL → Tier-2 FAIL → Tier-3 FAIL → Tier-1 WARN → Tier-2 WARN → Tier-3 WARN. Each finding carries a `Recommendation:` line drawn from [repair-playbook.md](references/repair-playbook.md).

Close with:
- `Resolver audited — no findings` or
- `Resolver audited, N findings (X fail, Y warn)`

### 6. Opt-In Repair Loop

After presenting findings, ask:
> "Apply fixes? Enter y (all), n (skip), or comma-separated numbers."

For each selected finding, draw the canonical repair from `repair-playbook.md`. Show the diff; apply only on per-change confirmation. Re-run Tier-1 after each applied fix.

## Key Instructions

- Run Tier-1 first; exclude malformed resolvers from Tier 2
- Present the three Tier-2 dimensions in a single locked-rubric call; per-dimension calls degrade agreement (RULERS, Hong et al. 2026)
- Include `RESOLVER.md` verbatim in the Tier-2 prompt — never summarize
- Gate the dark-capabilities scan on depth — depth 1–2 is the sweet spot; deeper scans overwhelm with transient build outputs
- Run evals only when `--run-evals` is passed; eval execution is slow and costs LLM calls, so keep it opt-in
- Surface borderline evidence as WARN (default-closed)

## Anti-Pattern Guards

1. **LLM-evaluating path existence.** Handle with deterministic file checks (Tier 1); paths either resolve or they don't.
2. **Per-dimension Tier-2 calls.** Collapse into one locked-rubric call per resolver.
3. **Hand-managed region edits treated as valid.** Any row in the managed region that doesn't regenerate from disk is drift — FAIL or WARN depending on whether the row still resolves.
4. **Reporting without recommendations.** Every finding names the specific change from the repair playbook.
5. **Silent out-of-scope expansion.** If the user asks to suppress a dark-capability finding, add the directory to the explicit out-of-scope list; don't silently ignore it.

## Example

<example>
User: `/build:check-resolver`

Step 1 — Discovers `RESOLVER.md` at repo root, `AGENTS.md`, `.resolver/evals.yml`.

Step 2 Tier 1:
- AGENTS.md pointer present — PASS
- Managed-region markers present — PASS
- Filing paths resolve — FAIL: `.designs/` not found (filing row points at non-existent directory)
- Eval file parses — PASS
- File mtime 102 days old — WARN

Step 3 Tier 2 (excludes `.designs/` row from filing coverage assessment):
- Filing Coverage — WARN: `.inbox/` directory on disk, not in table or out-of-scope
- Context Actionability — PASS
- Eval Representativeness — WARN: 8 cases all positive, no negative cases

Step 4 Tier 3:
- Dark capability: `.inbox/` — WARN (already flagged in Tier 2)
- Staleness: filing table drift (`.designs/` removed from disk, still in table) — WARN

Output:
```
FAIL  RESOLVER.md — filing path .designs/ does not resolve
  Recommendation: Remove `.designs/` row or restore the directory
WARN  RESOLVER.md — mtime 102 days; staleness threshold 90 days
  Recommendation: Run /build:build-resolver --regenerate
WARN  RESOLVER.md — dark capability: .inbox/ not in filing table or out-of-scope
  Recommendation: Add to filing table or out-of-scope list
WARN  .resolver/evals.yml — no negative cases in 8 eval rows
  Recommendation: Add 1-2 negative cases per filing row (prompt routes AWAY from similar directory)
```
</example>

## Handoff

**Receives:** Target directory (defaults to CWD); walks up to the nearest `RESOLVER.md` and audits that resolver. Optional `--run-evals` flag.
**Produces:** Structured findings report in file/issue/severity format.
**Chainable to:** `/build:build-resolver --regenerate` (rebuild managed region); `/build:build-resolver --add-filing <type>` (add missing row).
