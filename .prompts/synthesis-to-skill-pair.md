---
name: Synthesis to Skill Pair
description: Turn an ensemble-rules synthesis (best-practices guidance + shared deterministic checks) into a build-<X> / check-<X> skill pair with supporting Tier-1 scripts. Produces the principles doc, both SKILL.md files, audit rubric, repair playbook, and executable scripts.
---

# Synthesis to Skill Pair

## Goal

Take a single synthesis output from `ensemble-rules` — a markdown document with six sections (consensus rules, strong minority, divergences, omissions, **shared deterministic checks**, final rules file) — and produce a working skill pair that operationalizes it inside this toolkit:

- A shared **principles doc** that build-* and check-* both cite
- A **build-<X>** skill that authors new artifacts following the principles
- A **check-<X>** skill that audits existing artifacts against the principles using a three-tier architecture (deterministic scripts → LLM judgment → cross-entity conflict)
- A set of **Tier-1 scripts** derived directly from the synthesis' deterministic-checks section
- A **repair playbook** with one recipe per finding type

The synthesis' Section 5 (*Shared Deterministic Checks*) is the direct source for the Tier-1 script catalog. Every shared check becomes either an off-the-shelf tool invocation or a bash script; singleton checks are evaluated case-by-case.

## Inputs

1. **Path to a synthesis markdown file** — produced by `ensemble-rules`; expected sections: Consensus Rules, Strong Minority Rules, Divergences, Notable Omissions, Shared Deterministic Checks (+ singleton checks), Final Rules File.
2. **Topic name** — the singular noun the skill pair operates on (e.g., `rule`, `skill`, `hook`, `agent`, `prompt`, `eval`). Used to generate `build-<topic>` and `check-<topic>` skill names.
3. **Target plugin directory** — default `plugins/build/`. Skills land under `plugins/<plugin>/skills/`; the shared principles doc lands under `plugins/<plugin>/_shared/references/`.

## What's already decided (constraints — do not reopen)

- **Principles doc is positively framed from word one.** Do not draft with "Don't X" / "Never Y" as the primary mode. Reserve negative framing for cases where no clean positive counterpart exists.
- **No rule-type taxonomy.** Categories like directive/enforcement/procedural/style dissolve on contact. Focus on judgment-vs-deterministic-vs-structural as the real distinction.
- **Three tiers, fixed.** Tier-1 = deterministic scripts. Tier-2 = one locked-rubric LLM call per artifact evaluating all dimensions simultaneously. Tier-3 = cross-entity conflict detection. No trigger gates on Tier-2 — all dimensions run always; dimensions that don't apply return PASS silently.
- **Principle → audit dimension is 1:1.** Every principle is either a Tier-2 dimension or explicitly author-time-only. No orphans. Collapse overlapping principles into one dimension rather than multiplying dimensions.
- **Scripts target bash-3.2-portable by default.** macOS compatibility. Use `/build:build-shell` in full human-mode for every script — not `--as-tool`. POSIX utilities only (no GNU-specific `\<\>` word boundaries, no `mapfile`, no associative arrays).
- **Scripts live at `plugins/<plugin>/skills/check-<X>/scripts/*.sh`.** Claude resolves absolute paths at invocation time; do not rely on `$CLAUDE_PLUGIN_ROOT` (documented for hooks, not skills). Use a `${SKILL_DIR}` placeholder in SKILL.md and document the resolution convention.
- **Output lint format is fixed:** `SEVERITY  <path> — <check>: <detail>` on one line, followed by `  Recommendation: <specific change>` on the next. Severities: `FAIL`, `WARN`, `INFO`, `HINT`. Exit 0 on clean / WARN / INFO / HINT-only; exit 1 on FAIL; exit 64 on arg error; exit 69 on missing dependency.
- **Commit in vertical slices, one PR.** Each phase below that produces artifacts lands as its own commit. Self-review then human review before merge.

## What to produce (outputs)

| Artifact | Location |
|---|---|
| Principles doc | `plugins/<plugin>/_shared/references/<topic>s-best-practices.md` |
| Authoring skill | `plugins/<plugin>/skills/build-<X>/SKILL.md` |
| Audit skill | `plugins/<plugin>/skills/check-<X>/SKILL.md` |
| Audit rubric | `plugins/<plugin>/skills/check-<X>/references/audit-dimensions.md` |
| Repair playbook | `plugins/<plugin>/skills/check-<X>/references/repair-playbook.md` |
| Tier-1 scripts | `plugins/<plugin>/skills/check-<X>/scripts/*.sh` |
| Plugin version bump | `plugins/<plugin>/pyproject.toml` + `plugins/<plugin>/.claude-plugin/plugin.json` |

## Workflow

Each phase ends with an approval gate unless marked otherwise. Do not proceed without approval.

### Phase 0: Foundation — principles doc

Read synthesis Section 6 (*Final Rules File*) and Section 1 (*Consensus Rules*).

Produce `<topic>s-best-practices.md` with these sections in order:
1. **What a Good <X> Does** — one-paragraph scope statement
2. **Anatomy** — the file/structure template the skills will both reference
3. **Authoring Principles** — ~8-12 principles from Section 1, each one paragraph. Include the *why* alongside each.
4. **Patterns That Work** — the same principles reframed as positive shapes ("X over Y"). Each corresponds to a failure mode Tier-2 audits.
5. **Safety** — from Section 1's safety subsection. Name what's auditable deterministically vs. what relies on author judgment.
6. **Review and Decay** — retirement triggers, cadence
7. A closing diagnostic paragraph

Constraints:
- 400–800 words total. Over 800, trim.
- Positive framing throughout. Negative framing only where no clean positive counterpart exists.
- No concrete numeric thresholds (those live in check-<X>'s Tier-1, not principles).
- No rule-type taxonomy.

**Approval gate.** Present the draft. Iterate on feedback. Do not proceed to Phase 1 without explicit approval.

### Phase 1: Legacy-opinion walkthrough (skip if greenfield)

If the plugin already has an existing build-<X> / check-<X> pair:

List every format or convention the old docs carry. Walk one at a time. For each opinion, answer:
- What does **check-<X>** get from enforcing it?
- What does **build-<X>** get from teaching it?
- Does the evidence justify the ceremony?

Classify each as **keep / loosen / drop**. Expect to drop more than half. Document the disposition inline (table or numbered list).

**Approval gate** — get a sign-off on the walkthrough outcomes before merging them into the new principles doc.

### Phase 2: Principle → audit dimension mapping

Produce a table mapping each principle to exactly one Tier-2 audit dimension, one Tier-1 check, or explicit author-time-only.

| Principle | Dimension | Tier | Notes |
|---|---|---|---|
| … | … | 1/2/3/author-time | … |

Collapse overlapping principles (e.g., "positive framing" + "direct voice" → single "Framing" dimension). No orphans — every principle must be accounted for.

**Approval gate.**

### Phase 3: Script breakdown from Section 5

Read synthesis Section 5 (*Shared Deterministic Checks*). For each check:

1. **Shared checks (raised by multiple models).** Default: implement. Group related checks into one script where the signal sources overlap (e.g., a single script for location + extension + frontmatter shape, since all read the file header).

2. **Singleton checks.** Judgment call. Implement if the check is generally useful beyond the single model that raised it; skip if it's narrow.

3. **Off-the-shelf tools.** If the synthesis names a tool (`shellcheck`, `gitleaks`, `markdownlint`, etc.) and it covers the check adequately, document the tool invocation in the skill rather than re-implementing. A bash wrapper that calls the tool and reformats output in our lint format is often the right move.

Produce a script breakdown table:

| Script | Source check(s) | Tier-1 severity | Tool candidate |
|---|---|---|---|

Include optional **pre-filter** scripts for Tier-2 dimensions with cheap deterministic "obvious case" catchers (hedges, prohibitions, synthetic placeholders in examples). Pre-filters emit WARN only, do not replace Tier-2, accelerate it.

**Approval gate** — the breakdown is the design; scripts are mechanical after this. Do not write scripts without approval.

### Phase 4: Skill rescaffold (one commit)

Write all four skill artifacts:

- `build-<X>/SKILL.md` — workflow (primitive check → intake → scope → conflict check → draft → approval gate → write), plus anti-pattern guards each citing a principle by name. Reference frontmatter points at the shared principles doc and `primitive-routing.md`.
- `check-<X>/SKILL.md` — three-tier workflow. Tier-1 section lists scripts (placeholder — scripts not yet written). Tier-2 lists all dimensions, always-on. Tier-3 describes cross-entity conflict detection.
- `audit-dimensions.md` — Tier-1 check table + Tier-2 dimension descriptions. Each dimension cites its source principle by name from the shared doc.
- `repair-playbook.md` — one recipe per Tier-1 finding type (including each subtype a script might emit) + one recipe per Tier-2 dimension failure + one per Tier-3 conflict. Each recipe: Signal → CHANGE → FROM → TO → REASON. Note at top that HINT output is feed-forward context, not a finding requiring repair.

Delete any legacy reference files whose content was absorbed.

Bump the plugin version (minor for substantive rework).

**Commit and push.**

### Phase 5: First self-consistency audit

Before writing any scripts, cross-check the four artifacts:

- Does every principle in the shared doc appear as a dimension in audit-dimensions.md (or is explicitly author-time-only)?
- Do dimension names match across SKILL.md, audit-dimensions.md, and repair-playbook.md?
- Do cross-reference paths (`../../_shared/references/...`) resolve?
- Does the build-<X> example produce a file that would pass all Tier-2 dimensions?
- Does the check-<X> example output use the correct severity names?

Fix findings. **Do not skip this.** Fresh-eye audit finds things author bias misses.

**Commit fixes.**

### Phase 6: Write scripts via `/build-shell`

For each script in the approved breakdown (Phase 3), invoke `/build:build-shell` in full human-mode:

1. Route → Scope Gate → Elicit → Draft → Safety Check → Review Gate → Save

Elicit fields (pre-fill from the breakdown):
- target-shell: `bash-3.2-portable`
- purpose: one sentence
- invocation-style: `cli`
- setuid: `no`
- deps: comma-separated (prefer POSIX standards: `awk`, `find`, `basename`, `grep`, `tr`, `sed`, `head`)
- save-path: under `scripts/` in the check-<X> directory

Each script:
- Emits in the fixed lint format
- Exits per the fixed contract (0/1/64/69)
- Includes a top-of-file header with purpose, usage, exit codes, dependencies
- Has a `preflight` function that names missing deps + install hint
- Uses POSIX-only awk (no `\<\>` word boundaries — use `[^A-Za-z_]` groups)
- Follows the same shape as the other scripts in the directory (copy a sibling's skeleton)

Smoke-test each script against a real `.md` file after writing.

**Commit scripts as one unit** (or a small number of vertical slices if the set is large).

### Phase 7: Wire scripts into check-<X>/SKILL.md

Replace the placeholder Tier-1 section with concrete invocation:

```bash
SCRIPTS="${SKILL_DIR}/scripts"  # Claude resolves ${SKILL_DIR} from the skill's base directory
TARGETS="$ARGUMENTS"

bash "$SCRIPTS/<script-1>.sh"     $TARGETS
bash "$SCRIPTS/<script-2>.sh"     $TARGETS
...
```

Add a script-to-check map (table: script | checks | severity levels).

Add explicit orchestration rules:
- Which FAIL findings exclude from Tier-2 (usually: location, extension, secrets, glob syntax, oversize)
- Which findings do NOT exclude (WARN, INFO, HINT)
- How HINT lines feed the Tier-2 prompt as context

**Commit.**

### Phase 8: Second self-consistency audit

After scripts exist, re-audit:

- Every finding a script emits has a repair-playbook recipe (including each subtype — e.g., check_paths_glob emits four subtypes; playbook should cover all four).
- Script severity column matches audit-dimensions.md severity column.
- Script exit-code contract matches SKILL.md orchestration rules.
- The `${SKILL_DIR}` pattern is documented; `$CLAUDE_PLUGIN_ROOT` is not used.
- Smoke-test each script against a real `.md` file; verify output parses cleanly.

Fix findings. **Commit fixes.**

### Phase 9: Pre-filter scripts (optional)

If Phase 3 identified pre-filter candidates (obvious hedges for Specificity, prohibition openers for Framing, synthetic placeholders for Example Realism):

- Write one consolidated `check_prose.sh` via `/build-shell`
- All findings WARN severity
- Exit 0 always (heuristics, not failures)
- Wire into Tier-1 invocation
- Update audit-dimensions.md table

Skip this phase if Tier-2 is already cheap or if no obvious-case patterns emerged.

**Commit if used.**

### Phase 10: End-to-end validation (do not skip)

Create a small fixture — 3–5 `.md` files covering:
- One clean file that should pass all checks
- One with a deterministic FAIL (secret, bad glob, wrong location)
- One with a Tier-2-detectable problem (hedged language, prohibition-only)
- One with both

Run check-<X> against the fixture. Verify:
- Scripts execute without shell errors
- Output parses in the expected format
- FAIL findings exclude the file from Tier-2 (no Tier-2 output for malformed files)
- Dimension names used in Tier-2 output match audit-dimensions.md

Fix integration issues. **Commit the fixture and any fixes.**

### Phase 11: PR review

Self-review the entire PR commit-by-commit. Then hand off to a human reviewer.

## Acceptance criteria

- Every principle in the shared doc maps to exactly one audit dimension OR explicit author-time-only.
- Every Tier-2 dimension cites its source principle by name.
- Every Tier-1 script finding (including each subtype a script emits) has a repair-playbook recipe.
- Every script executes cleanly (`./script.sh -h` prints usage; `./script.sh some.md` produces correctly-formatted output).
- End-to-end validation on the fixture produces expected output.
- The shared principles doc is 400-800 words, positively framed, no rule-type taxonomy.
- All cross-reference paths resolve (`python3 plugins/wiki/scripts/lint.py` passes).
- Commits are vertical slices; each is reviewable independently; the sequence tells the story.

## Anti-patterns to avoid

1. **Writing principles with negative framing.** Positive from word one; rewriting is expensive.
2. **Absorbing legacy opinions without triage.** Each opinion must earn its keep. Drop more than half.
3. **Including a rule-type taxonomy.** Dissolves on contact; don't include.
4. **Using `$CLAUDE_PLUGIN_ROOT` in skill-invoked bash.** Documented for hooks only. Use `${SKILL_DIR}` placeholder.
5. **Trigger-gating Tier-2 dimensions.** All dimensions always run; those that don't apply return PASS.
6. **Writing scripts before the breakdown is approved.** The breakdown is the design; scripts are mechanical.
7. **Skipping `/build:build-shell`'s safety check.** It catches real issues in 3+ scripts.
8. **Dimension names drifting across files.** Settle naming in Phase 2; don't renegotiate later.
9. **Scripts that exit 1 on WARN.** Exit 0 on anything short of FAIL.
10. **Skipping end-to-end validation.** First real invocation after merge is the worst place to find integration bugs.

## Estimated effort

First time through: ~half a day of interactive pairing (≈ 4 hours). Subsequent skill pairs following this playbook: ~2–3 hours — most of the original complexity was in *discovering* the process, not executing it.

## Related

- `plugins/build/skills/build-shell/SKILL.md` — the skill used to scaffold each Tier-1 script
- `plugins/build/skills/check-shell/SKILL.md` — audits scaffolded scripts against 15 lints
- `plugins/build/_shared/references/primitive-routing.md` — decision framework for rule vs. hook vs. skill vs. CLAUDE.md
- `plugins/build/_shared/references/rules-best-practices.md` — worked example of the principles-doc shape this prompt produces
