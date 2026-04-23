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

1. **Path to a synthesis run directory** — produced by `ensemble-rules`; expects at minimum:
   - `synthesis.md` — six sections (Consensus Rules, Strong Minority Rules, Divergences, Notable Omissions, Shared Deterministic Checks, Final Rules File)
   - `coverage-llm.md` — LLM-clustered coverage matrix: rule × model with ✓ marks; **primary attribution source** for the tier filter
   - `coverage.md` — rapidfuzz-deterministic coverage matrix; **cross-check source** at borderlines where LLM clustering and rapidfuzz disagree
   - `meta.json` — includes the panel model list used for the run
2. **Topic name** — the singular noun the skill pair operates on (e.g., `rule`, `skill`, `hook`, `agent`, `prompt`, `eval`). Used to generate `build-<topic>` and `check-<topic>` skill names.
3. **Target plugin directory** — default `plugins/build/`. Skills land under `plugins/<plugin>/skills/`; the shared principles doc lands under `plugins/<plugin>/_shared/references/`.

## What's already decided (constraints — do not reopen)

- **Principles doc is positively framed from word one.** Do not draft with "Don't X" / "Never Y" as the primary mode. Reserve negative framing for cases where no clean positive counterpart exists.
- **No rule-type taxonomy.** Categories like directive/enforcement/procedural/style dissolve on contact. Focus on judgment-vs-deterministic-vs-structural as the real distinction.
- **Three tiers, fixed.** Tier-1 = deterministic scripts. Tier-2 = one locked-rubric LLM call per artifact evaluating all dimensions simultaneously. Tier-3 = cross-entity conflict detection. No trigger gates on Tier-2 — all dimensions run always; dimensions that don't apply return PASS silently.
- **Principle → audit dimension is 1:1.** Every principle is either a Tier-2 dimension or explicitly author-time-only. No orphans. Collapse overlapping principles into one dimension rather than multiplying dimensions.
- **Inclusion bar (cross-family corroboration AND deployment guarantee).** A candidate rule, dimension, or check enters the Core principles doc *only if*:
  1. **Cross-family support** — raised by at least 2 different model families (OpenAI / Anthropic / Google / xAI) per `coverage-llm.md`, AND
  2. **Deployment guarantee** — either Haiku (or the panel's affordable-tier Anthropic model) raised it, *or* the check is mechanically deterministic (enforceable by a Tier-1 script or off-the-shelf tool without model judgment).

  Rules that meet (1) but fail (2) are **dropped**, not preserved in an Advanced section. The goal is a tight core that affordable-tier models (Sonnet-class and below) can execute. Rules failing (1) are also dropped. Discrepancies between `coverage-llm.md` and `coverage.md` at the borderline are noted in the principles doc's provenance footnote.
- **Scripts target bash-3.2-portable by default.** macOS compatibility. Use `/build:build-shell` in full human-mode for every script — not `--as-tool`. POSIX utilities only (no GNU-specific `\<\>` word boundaries, no `mapfile`, no associative arrays).
- **Scripts live at `plugins/<plugin>/skills/check-<X>/scripts/*.sh`.** Claude resolves absolute paths at invocation time; do not rely on `$CLAUDE_PLUGIN_ROOT` (documented for hooks, not skills). Use a `${SKILL_DIR}` placeholder in SKILL.md and document the resolution convention.
- **Output lint format is fixed:** `SEVERITY  <path> — <check>: <detail>` on one line, followed by `  Recommendation: <specific change>` on the next. Severities: `FAIL`, `WARN`, `INFO`, `HINT`. Exit 0 on clean / WARN / INFO / HINT-only; exit 1 on FAIL; exit 64 on arg error; exit 69 on missing dependency.
- **Commit in vertical slices, one PR.** Each phase below that produces artifacts lands as its own commit. Self-review then human review before merge.
- **Skill-chain relationships are declared, not inferred.** Every `build-<X>` and `check-<X>` SKILL.md ends with a `## Handoff` section carrying `Receives:` / `Produces:` / `Chainable to:` fields. The default chain is bidirectional: `build-<X>` is chainable to `check-<X>` (audit the just-built artifact); `check-<X>` is chainable to `build-<X>` (rebuild after flagged repairs). Preserve any chain relationships the legacy skills declared — if the old `build-<X>` chained into another skill (e.g., `verify-work`, `finish-work`), that linkage carries over unless the ensemble or project docs explicitly deprecate it. Chain relationships are part of the project-fact content extracted in Phase 1.

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

### Phase 0a: Panel classification

Read `meta.json` and tag each model by `{family, tier}`. Families: OpenAI, Anthropic, Google, xAI. Tiers: frontier, affordable.

Produce a table:

| Model | Family | Tier |
|---|---|---|
| openai/gpt-5 | OpenAI | frontier |
| openai/gpt-4o-mini | OpenAI | affordable |
| anthropic/claude-opus-4-7 | Anthropic | frontier |
| anthropic/claude-haiku-4-5 | Anthropic | affordable |
| … | … | … |

If an unknown model appears, halt and ask for classification rather than guessing. Flag families that have only frontier representation or only affordable representation — the inclusion bar can still apply, but note the gap in the principles doc provenance footnote ("Google is represented by Gemini Pro only; affordable-tier Google coverage was not verifiable").

The affordable-tier Anthropic model ("Haiku in the default panel) is the **deployment-guarantee proxy** — if it raised a rule, Sonnet-class and above can apply the rule.

### Phase 0b: Rule classification (Core / Drop)

For every candidate rule, dimension, or check from synthesis Sections 1, 2, and 5:

1. Read the attribution from `coverage-llm.md` — which models raised this rule?
2. Count distinct **families** that raised it (≥2 required for Core).
3. Check if the affordable-tier Anthropic model (Haiku) is among them.
4. If Haiku is not among them, determine whether the check is **mechanically deterministic**: enforceable by regex, AST traversal, a file-format parse, or an off-the-shelf tool (`shellcheck`, `gitleaks`, `markdownlint`) without model judgment.
5. Cross-check against `coverage.md`: if rapidfuzz attributes fewer families than LLM clustering, treat the rule as lower-confidence (still Core if both criteria hold, but note the discrepancy).

Classify:

| | Haiku raised | Haiku silent |
|---|---|---|
| **Cross-family (≥2) AND deterministic** | **Core** | **Core** |
| **Cross-family (≥2) AND judgment-only** | **Core** | **Drop** |
| **Single-family (1)** | **Drop** | **Drop** |

Produce a classification table and flag any clustering discrepancies between the two coverage sources.

**Approval gate** — the classification determines what lands in the principles doc. Do not proceed without sign-off. Expect roughly half of candidates to drop; that is the filter working.

### Phase 0c: Foundation — principles doc

Consuming **only Core-classified** items from Phase 0b, produce `<topic>s-best-practices.md` with these sections in order:

1. **What a Good <X> Does** — one-paragraph scope statement
2. **Anatomy** — the file/structure template the skills will both reference
3. **Authoring Principles** — Core principles from Phase 0b, each one paragraph. Include the *why* alongside each.
4. **Patterns That Work** — the same principles reframed as positive shapes ("X over Y"). Each corresponds to a failure mode Tier-2 audits.
5. **Safety** — Core safety rules. Name what's auditable deterministically vs. what relies on author judgment.
6. **Review and Decay** — retirement triggers, cadence
7. A closing diagnostic paragraph
8. **Provenance footnote** — one short paragraph naming the ensemble run, the panel, the inclusion bar (cross-family + Haiku-or-deterministic), and any clustering discrepancies flagged in Phase 0b.

Constraints:
- 400–800 words total. Over 800, trim.
- Positive framing throughout. Negative framing only where no clean positive counterpart exists.
- No concrete numeric thresholds (those live in check-<X>'s Tier-1, not principles).
- No rule-type taxonomy.
- Do **not** include an "Advanced" section. Rules that failed the inclusion bar are dropped. If you believe a dropped rule is load-bearing, raise it in the approval conversation — do not silently include it.

**Approval gate.** Present the draft. Iterate on feedback. Do not proceed to Phase 1 without explicit approval.

### Phase 1: Legacy extraction (skip if greenfield)

If the plugin already has an existing `build-<X>` / `check-<X>` pair, **the ensemble is the source of truth for principles; legacy content is discarded without per-opinion review.** The inclusion bar in Phase 0b is the filter — legacy principles, patterns, dimensions, or repair recipes that aren't reaffirmed by the ensemble are dropped.

The **only** thing to preserve from the legacy skill is **project-fact content** — things the ensemble cannot know because they're specific to this toolkit's local ecosystem. Extract these in a brief one-pass scan:

| Category | Examples |
|---|---|
| Tool mechanics | "Claude Code loads rules from `.claude/rules/*.md`"; "hook scripts receive `${CLAUDE_PLUGIN_ROOT}`" |
| Path conventions | "Plugins live at `plugins/<name>/`"; "skills at `plugins/<plugin>/skills/<name>/SKILL.md`"; "shared references at `plugins/<plugin>/_shared/references/`" |
| Output conventions | Lint format `SEVERITY  <path> — <check>: <detail>`; exit-code contract; severity naming |
| Test conventions | `tmp_path` fixtures; stdlib-only; inline markdown strings |
| Version/release conventions | `pyproject.toml` + `.claude-plugin/plugin.json` bump pattern |
| **Skill-chain relationships** | "`build-<X>` chained to `check-<X>`"; any third-party chain targets (e.g., "`build-rule` → `check-rule` → `verify-work`"); custom `Receives:` / `Produces:` contracts beyond the default |

Produce a short artifact at `plans/<date>-legacy-facts-<topic>.md` — bulleted list, one fact per line, citing the legacy file and line where each was found. Commit this as the first vertical slice of the PR. It serves as the audit trail: a reviewer can see exactly what was preserved from the legacy skill and why.

**Everything else in the legacy skill — principles, patterns, audit dimensions, repair recipes, anti-pattern guards, narrative prose — is discarded.** It either survives the ensemble inclusion bar in Phase 0b or it doesn't matter. No walkthrough, no per-opinion accept/modify/drop ceremony.

**Approval gate** — present the extracted facts list. A short list is the expected outcome; if the list gets long, you're probably preserving too much. Target ≤20 bullets.

### Phase 2: Principle → audit dimension mapping

Produce a table mapping each principle to exactly one Tier-2 audit dimension, one Tier-1 check, or explicit author-time-only.

| Principle | Dimension | Tier | Notes |
|---|---|---|---|
| … | … | 1/2/3/author-time | … |

Collapse overlapping principles (e.g., "positive framing" + "direct voice" → single "Framing" dimension). No orphans — every principle must be accounted for.

**Approval gate.**

### Phase 3: Script breakdown from Section 5

Read synthesis Section 5 (*Shared Deterministic Checks*) cross-referenced with `coverage-llm.md`. Apply the same inclusion bar as Phase 0b:

1. **Shared checks (≥2 families raised it).** Implement as Tier-1 script (deterministic-enforcement automatically satisfies the deployment-guarantee criterion). Group related checks into one script where the signal sources overlap (e.g., a single script for location + extension + frontmatter shape, since all read the file header).

2. **Singleton checks (one family only).** **Default: drop.** These fail the cross-family bar. Include only with an explicit justification ("this one-model check plugs a known gap other models missed"); the default is to skip.

3. **Off-the-shelf tools.** If the synthesis names a tool (`shellcheck`, `gitleaks`, `markdownlint`, etc.) and it covers the check adequately, wrap the tool (don't re-implement). A bash wrapper that invokes the tool and reformats output into the fixed lint format is the right move.

Produce a script breakdown table:

| Script | Source check(s) | Family count (LLM / rapidfuzz) | Tier-1 severity | Tool candidate |
|---|---|---|---|---|

Pre-filter scripts for Tier-2 dimensions (hedges / prohibitions / synthetic placeholders) are **optional** and only add them when the target Tier-2 dimension is a Core principle AND a cheap deterministic "obvious case" catcher exists. Pre-filters emit WARN only; they do not replace Tier-2, they accelerate it.

**Approval gate** — the breakdown is the design; scripts are mechanical after this. Do not write scripts without approval.

### Phase 4: Skill rescaffold (one commit)

Write all four skill artifacts:

- `build-<X>/SKILL.md` — workflow (primitive check → intake → scope → conflict check → draft → approval gate → write), plus anti-pattern guards each citing a principle by name. Reference frontmatter points at the shared principles doc and `primitive-routing.md`. End with a `## Handoff` section: `Receives:` / `Produces:` / `Chainable to:` (minimally `check-<X>`; plus any chain relationships preserved from Phase 1's legacy-facts extraction).
- `check-<X>/SKILL.md` — three-tier workflow. Tier-1 section lists scripts (placeholder — scripts not yet written). Tier-2 lists all dimensions, always-on. Tier-3 describes cross-entity conflict detection. End with a `## Handoff` section: `Receives:` / `Produces:` / `Chainable to:` (minimally `build-<X>` to rebuild after repairs; plus any preserved chain relationships).
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

- Every Core principle meets the inclusion bar: cross-family support (≥2 families per `coverage-llm.md`) AND (Haiku raised it OR the check is mechanically deterministic). Advanced/strong-minority rules are not preserved — they are dropped.
- Every SKILL.md in the pair ends with a `## Handoff` section declaring `Receives:` / `Produces:` / `Chainable to:`. `build-<X>` minimally chains to `check-<X>`; `check-<X>` minimally chains to `build-<X>`. Any additional chain relationships extracted from legacy skills in Phase 1 are preserved unless explicitly deprecated.
- Every principle in the shared doc maps to exactly one audit dimension OR explicit author-time-only.
- Every Tier-2 dimension cites its source principle by name.
- Every Tier-1 script finding (including each subtype a script emits) has a repair-playbook recipe.
- Every script executes cleanly (`./script.sh -h` prints usage; `./script.sh some.md` produces correctly-formatted output).
- The principles doc carries a provenance footnote naming the ensemble run, the panel, and the inclusion bar. Clustering discrepancies between `coverage-llm.md` and `coverage.md` at the Core boundary are documented.
- End-to-end validation on the fixture produces expected output.
- The shared principles doc is 400-800 words, positively framed, no rule-type taxonomy, no "Advanced" section.
- All cross-reference paths resolve (`python3 plugins/wiki/scripts/lint.py` passes).
- Commits are vertical slices; each is reviewable independently; the sequence tells the story.

## Anti-patterns to avoid

1. **Writing principles with negative framing.** Positive from word one; rewriting is expensive.
2. **Preserving legacy principles that the ensemble didn't reaffirm.** Legacy content outside the project-facts extraction is discarded. Do not run a per-opinion keep/loosen/drop walkthrough as a way to smuggle legacy principles past the ensemble inclusion bar.
3. **Preserving rules that failed the inclusion bar in an "Advanced" section.** Dropped means dropped. If a dropped rule is genuinely load-bearing, raise it in conversation so the inclusion bar can be debated — do not smuggle it back in via a side section.
4. **Including a rule-type taxonomy.** Dissolves on contact; don't include.
5. **Using `$CLAUDE_PLUGIN_ROOT` in skill-invoked bash.** Documented for hooks only. Use `${SKILL_DIR}` placeholder.
6. **Trigger-gating Tier-2 dimensions.** All dimensions always run; those that don't apply return PASS.
7. **Writing scripts before the breakdown is approved.** The breakdown is the design; scripts are mechanical.
8. **Skipping `/build:build-shell`'s safety check.** It catches real issues in 3+ scripts.
9. **Dimension names drifting across files.** Settle naming in Phase 2; don't renegotiate later.
10. **Scripts that exit 1 on WARN.** Exit 0 on anything short of FAIL.
11. **Skipping end-to-end validation.** First real invocation after merge is the worst place to find integration bugs.
12. **Relying on `coverage.md` alone or `coverage-llm.md` alone.** LLM clustering catches semantic equivalence rapidfuzz misses; rapidfuzz is synthesizer-bias-free. Consume the LLM version as primary but cross-check at borderlines.

## Estimated effort

First time through: ~half a day of interactive pairing (≈ 4 hours). Subsequent skill pairs following this playbook: ~2–3 hours — most of the original complexity was in *discovering* the process, not executing it.

## Related

- `plugins/build/skills/build-shell/SKILL.md` — the skill used to scaffold each Tier-1 script
- `plugins/build/skills/check-shell/SKILL.md` — audits scaffolded scripts against 15 lints
- `plugins/build/_shared/references/primitive-routing.md` — decision framework for rule vs. hook vs. skill vs. CLAUDE.md
- `plugins/build/_shared/references/rules-best-practices.md` — worked example of the principles-doc shape this prompt produces
