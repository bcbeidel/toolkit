# Changelog

All notable changes to wos will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.23.0] - 2026-03-12

### Removed

- **Removed all completed/outdated docs.** Deleted all 33 plan/design files,
  all 6 research files, and 1 saved prompt. Removed empty `docs/plans/`,
  `docs/research/`, and `docs/prompts/` directories.

### Fixed

- **Fixed broken references.** Removed stale links in CLAUDE.md and AGENTS.md
  pointing to deleted or non-existent files (`architecture-reference`,
  `simplification-design`, `docs/designs/`, `docs/research/`).

## [0.22.0] - 2026-03-12

### Changed

- **PRINCIPLES.md drift detection update.** Updated 5 principles (P2, P3, P4,
  P6, P8) to reflect current practice: P2 clarifies assessment modules, P3
  covers artifact lifecycle state, P4 replaces line-count limit with
  single-purpose criterion, P6 reflects 500-line threshold, P8 adds explicit
  skill-to-skill handoff pattern.

## [0.21.0] - 2026-03-12

### Added

- **Ad-hoc validation mode in `/wos:validate-work`.** Users can now call
  validate-work without a plan. The skill builds a validation hypothesis from
  git diff (branch + working tree), project config files (pyproject.toml,
  package.json, Cargo.toml, etc.), and project docs (CLAUDE.md, AGENTS.md,
  README). User confirms or edits proposed checks before execution.
  ([#187](https://github.com/bcbeidel/wos/pull/187))

### Changed

- **Skill instruction density threshold raised to 500.** Default warn
  threshold increased from 200 to 500 instruction lines, reflecting that
  complex skills legitimately need more instruction surface. No fail tier.
  ([#187](https://github.com/bcbeidel/wos/pull/187))

- **Research phases 2+3 merged into per-sub-question loop.** Research skill
  now processes source discovery and evaluation together per sub-question,
  reducing context window pressure and improving source-to-question traceability.
  ([#150](https://github.com/bcbeidel/wos/issues/150),
  [#186](https://github.com/bcbeidel/wos/pull/186))

- **Skill workflow explicit handoffs.** Execute-plan now uses explicit
  confirmation prompts before invoking validate-work and finish-work.
  Research-to-distill pipeline added with structured handoff.
  ([#184](https://github.com/bcbeidel/wos/pull/184))

### Fixed

- **Worktree storage location.** Default worktree storage changed from
  `.claude/worktrees/` to `.worktrees/`, making it model-agnostic.
  ([#175](https://github.com/bcbeidel/wos/issues/175),
  [#185](https://github.com/bcbeidel/wos/pull/185))

## [0.20.0] - 2026-03-12

### Added

- **Empty-repo onboarding in `/wos:init`.** When initializing an empty repo,
  init now offers three optional steps: `.gitignore` with Python defaults,
  `README.md` stub from a project-intent question, and guided first-action
  suggesting WOS skill sequences. All steps are skippable; non-empty repos
  are unaffected.
  ([#172](https://github.com/bcbeidel/wos/issues/172),
  [#182](https://github.com/bcbeidel/wos/pull/182))

## [0.19.0] - 2026-03-12

### Changed

- **Renamed `/wos:validate-plan` to `/wos:validate-work`.** The skill validates
  completed work against plan criteria, not the plan document itself. The new
  name accurately reflects this purpose. All cross-references updated across
  skills, shared references, OVERVIEW.md, and examples.
  ([#177](https://github.com/bcbeidel/wos/issues/177),
  [#180](https://github.com/bcbeidel/wos/pull/180))

### Added

- **`docs/designs/` directory for design specs.** `/wos:brainstorm` now saves
  design documents to `docs/designs/` instead of `docs/plans/`, separating
  exploratory artifacts from committed implementation plans. `/wos:init` creates
  the directory, and AGENTS.md navigation includes it.
  ([#173](https://github.com/bcbeidel/wos/issues/173),
  [#180](https://github.com/bcbeidel/wos/pull/180))

## [0.18.1] - 2026-03-11

### Fixed

- **Worktree cleanup in parallel dispatch.** Merge protocol now includes
  worktree and branch cleanup steps immediately after merging, preventing
  orphaned worktrees from accumulating.
  ([#178](https://github.com/bcbeidel/wos/issues/178),
  [#179](https://github.com/bcbeidel/wos/pull/179))
- **Distill skill enforces `docs/context/` output location.** Target area must
  be under `docs/context/`. If the user requests a different location, the skill
  writes to `docs/context/` first, then offers to copy files elsewhere.
  ([#176](https://github.com/bcbeidel/wos/issues/176),
  [#179](https://github.com/bcbeidel/wos/pull/179))

## [0.18.0] - 2026-03-11

### Added

- **Plan lifecycle skills.** Five new skills forming a complete plan lifecycle:
  `/wos:brainstorm` (divergent-then-convergent design exploration),
  `/wos:write-plan` (structured implementation plans with checkboxes and
  verification criteria), `/wos:execute-plan` (sequential execution with
  parallel subagent dispatch), `/wos:validate-plan` (automated + human
  validation of completed work), and `/wos:finish-work` (merge, PR, keep,
  or discard options with safety verification).
  ([#157](https://github.com/bcbeidel/wos/issues/157)–[#163](https://github.com/bcbeidel/wos/issues/163))
- **Plan document format specification.** Plans use a standardized markdown
  format with metadata header, task checkboxes, verification criteria, and
  explicit lifecycle states (draft → approved → in-progress → completed/abandoned).
  ([#157](https://github.com/bcbeidel/wos/issues/157),
  [#165](https://github.com/bcbeidel/wos/pull/165))
- **OVERVIEW.md ecosystem documentation.** Documents the full skill ecosystem
  with Mermaid lifecycle diagram, layer descriptions, and skill table. Cleaned
  up superpowers references.
  ([#164](https://github.com/bcbeidel/wos/pull/164))
- **Research skill improvements.** Added research brief output, reflection
  checkpoints, and extraction phase for pulling actionable items from research.
  ([#152](https://github.com/bcbeidel/wos/pull/152))
- **Per-skill entry scripts.** Research assessment prototype using per-skill
  script pattern (`skills/<name>/scripts/`).
  ([#151](https://github.com/bcbeidel/wos/pull/151))
- **Feedback path from `/wos:write-plan` to `/wos:brainstorm`.** Plans can
  loop back to brainstorming when requirements need further exploration.
  ([#163](https://github.com/bcbeidel/wos/issues/163),
  [#171](https://github.com/bcbeidel/wos/pull/171))

## [0.17.0] - 2026-03-10

### Added

- **`/wos:principles` skill.** Capture and maintain project principles in
  PRINCIPLES.md. Includes extraction heuristics, principle structure guide,
  and drift detection references. Supports defining, reviewing, and checking
  principle drift.
  ([#145](https://github.com/bcbeidel/wos/pull/145))
- **Worked examples for all 16 `/wos:consider` models.** Each mental model
  now includes a concrete worked example demonstrating application.
  ([#126](https://github.com/bcbeidel/wos/issues/126))
- **Skill quality criteria from Anthropic skill-creator analysis.** New
  quality benchmarks derived from Anthropic's own skill authoring patterns.
  ([#142](https://github.com/bcbeidel/wos/pull/142))

### Changed

- **Research skill instruction density reduced.** Split `research-workflow.md`
  into gather (phases 1–3) and synthesis (phases 4–6) references. Aligned
  research skill with authoring guide conventions.
  ([#124](https://github.com/bcbeidel/wos/issues/124))
- **Skill quality polish across 5 skills.** Aligned research, distill, init,
  report-issue, and consider skills with the skill authoring guide.
  ([#143](https://github.com/bcbeidel/wos/pull/143))
- **PRINCIPLES.md expanded.** Added rationale, boundary conditions, and
  verification guidance for each design principle.

## [0.16.1] - 2026-03-09

### Added

- **Skill workflows documentation.** README now documents four recommended
  skill composition patterns: research pipeline, project setup, feedback loop,
  and standalone prompt improvement. Closes #127.

## [0.16.0] - 2026-03-07

### Changed

- **Research skill: 9-phase workflow.** Restructured from 6 phases (with
  5.5a/5.5b sub-phases) to a clean 9-phase sequence. Split old Phase 3
  (Verify & Evaluate) into Phase 3 (Verify Sources — mechanical URL
  checking) and Phase 4 (Evaluate Sources — SIFT judgment and tier
  classification). Promoted 5.5a/5.5b to Phase 7 (Self-Verify Claims)
  and Phase 8 (Citation Re-Verify). Finalize becomes Phase 9.
- **Research skill: consolidated references.** Reduced from 8 reference
  files (592 instruction lines) to 7 self-contained files (285 lines,
  51% reduction). Each reference maps to specific phases for selective
  loading during resume-after-context-reset. Merged `sift-framework.md` +
  `source-evaluation.md` + `source-verification.md` → `source-quality.md`.
  Rewrote `challenge-phase.md` → `challenge.md`. Extracted
  `synthesis-guide.md` from workflow. Trimmed `claim-verification.md`.
- **Research skill: description fixed.** Replaced "This skill should be
  used when" (voice violation) with "Conducts structured investigations
  using the SIFT framework" — leading with what the skill does.
- **Init skill: broader description triggers.** Added "setting up context
  structure" and "configuring project documentation" trigger phrases.
- **Distill skill: added examples.** Two `<example>` blocks demonstrating
  a distillation proposal table and a distilled context file with proper
  frontmatter.

## [0.15.0] - 2026-03-06

### Added

- **Skill metadata validation (`check_skill_meta`).** 7 deterministic quality
  checks for SKILL.md frontmatter: name format (lowercase+hyphens, ≤64 chars,
  no reserved words), description quality (≤1024 chars, no XML tags,
  third-person voice heuristic), and body length (≤500 non-blank lines).
  New `parse_skill_meta(text)` extracts name/description from SKILL.md raw
  text, handling YAML block scalars (`>` and `|`). Wired into `scripts/audit.py`
  — runs automatically when a `skills/` directory exists.
  ([#128](https://github.com/bcbeidel/wos/issues/128),
  [#140](https://github.com/bcbeidel/wos/pull/140))
- **Skill authoring guide.** New reference file at
  `skills/audit/references/skill-authoring-guide.md` with conventions for
  writing high-quality skills. Linked from `/wos:audit` skill evaluation
  section.
- **PRINCIPLES.md.** Extracted design principles from CLAUDE.md into a
  standalone file with full descriptions and tension examples.
- **Research: skill authoring rubric.** New research document at
  `docs/research/2026-03-06-skill-authoring-rubric.md` synthesizing skill
  quality conventions from 12 verified sources.

### Fixed

- **Distill skill description updated to third-person voice** for consistency
  with skill naming conventions.
- **Init skill name normalized.** Renamed from `wos:init` to `init` in
  SKILL.md frontmatter for consistency with other skills.

## [0.14.0] - 2026-03-06

### Added

- **Minimum word count warning for context files.** `check_content()` now warns
  when context files fall below a configurable minimum (default 100 words).
  CLI flag: `--context-min-words N`. Same exclusions as the max check
  (`_index.md` files and non-context files skipped).
  ([#132](https://github.com/bcbeidel/wos/issues/132))
- **Skill instruction density reporting.** New `wos/skill_audit.py` module with
  `strip_frontmatter()`, `count_instruction_lines()`, and `check_skill_sizes()`.
  The audit prints a skill density summary table to stderr and warns when skills
  exceed a configurable instruction line threshold (default 200). CLI flag:
  `--skill-max-lines N` (0 to disable warnings while preserving the summary).
  ([#133](https://github.com/bcbeidel/wos/issues/133))
- **Research: skill density threshold.** New research document at
  `docs/research/2026-03-05-skill-density-threshold.md` establishing the
  200-line default, anchored on Claude Code's documented guidance and supported
  by IFScale and Du et al. findings.

### Fixed

- **CLI flags `--context-min-words` and `--context-max-words` now wired
  through.** Both flags are passed from `scripts/audit.py` through
  `validate_file()` and `validate_project()` to `check_content()`.
  Previously `--context-max-words` was silently ignored (pre-existing on main).
- **`strip_frontmatter()` no longer matches `---` inside YAML values.**
  Changed delimiter search from `text.find("---", 3)` to
  `text.find("\n---", 3)` to match `frontmatter.py` behavior.

## [0.13.0] - 2026-03-05

### Changed

- **Refine-prompt: replace aggressive instruction language.** Rewrote
  `CRITICAL: You are a prompt ANALYST, not a prompt EXECUTOR` to clear, direct
  language without ALL-CAPS or aggressive markers. The analyst-not-executor
  guardrail is preserved — only the tone changed.
  ([#130](https://github.com/bcbeidel/wos/issues/130))
- **Refine-prompt: add target-model awareness.** The skill now asks which model
  or platform the refined prompt targets before proceeding. Format selection in
  technique #2 uses the answer to choose XML, Markdown, or hybrid structuring.
  Default changed from XML (Claude-optimized) to Markdown headers (broadest
  compatibility). Technique renamed from "XML Structuring" to "Structured
  Sectioning". Claude-specific over-prompting reference removed.
  ([#117](https://github.com/bcbeidel/wos/issues/117))

## [0.12.4] - 2026-03-05

### Added

- **Format-selection mapping table for refine-prompt skill.** Technique #2
  (XML Structuring) now includes a vendor-specific format recommendation table
  based on official documentation and independent benchmarks. Claude defaults
  to XML; GPT to Markdown; Gemini to either; Llama to Markdown+XML; multi-model
  to Markdown headers. Format choice and rationale are logged in the change log.
  ([#125](https://github.com/bcbeidel/wos/issues/125))
- **Fenced code output rule for refine-prompt.** Refined prompts are always
  wrapped in ` ```text ` blocks so XML tags and other markup render correctly
  in Claude Code.
- **Research: LLM format preferences by vendor.** New research document at
  `docs/research/2026-03-05-llm-format-preferences.md` with benchmark data
  from ImprovingAgents and He et al. (arXiv:2411.10541).

## [0.12.3] - 2026-03-05

### Removed

- **Excluded Techniques section removed from technique-registry.md.** Removed
  ~155 words describing techniques that were intentionally excluded from the
  registry. Mentioning excluded techniques by name may prime models to consider
  them, and every token competes for attention budget.
  ([#120](https://github.com/bcbeidel/wos/issues/120))

## [0.12.2] - 2026-03-05

### Changed

- **`/wos:consider` models moved from skills to commands.** Consider models are
  now registered as commands rather than sub-skills, enabling terminal
  autocompletion for `/wos:consider:{model-name}`.

## [0.12.1] - 2026-03-05

### Changed

- **`/wos:consider` models restructured as nested sub-skills.** Intermediate
  step in restructuring consider models for better autocompletion support.

## [0.12.0] - 2026-03-05

### Changed

- **`/wos:consider` models flattened for autocompletion.** Consider models
  restructured so terminal autocompletion surfaces individual model names.

## [0.11.0] - 2026-03-05

### Added

- **`/wos:init` skill replaces `/wos:create`.** New unified initialization skill
  that sets up or updates WOS project context. Idempotent — safe to run multiple
  times. Includes Document Standards subsection in AGENTS.md render.
  ([#123](https://github.com/bcbeidel/wos/pull/123))
- **Communication preferences merged into `/wos:init`.** Preferences capture
  (previously a separate `/wos:preferences` skill) is now an integrated step in
  the init workflow. Preferences are written to AGENTS.md instead of CLAUDE.md,
  with a pointer added to CLAUDE.md.
- **`extract_preferences()` in `agents_md.py`.** New function to read existing
  preferences from AGENTS.md.

### Changed

- **`render_preferences()` returns `List[str]`.** Removed direct CLAUDE.md
  writer; preferences are now rendered as lines for AGENTS.md integration.
- **`update_preferences.py` writes to AGENTS.md.** Script updated to use
  `--root` flag and write preferences via AGENTS.md markers.

### Fixed

- **Preferences preserved during reindex.** `reindex.py` no longer clobbers
  communication preferences when updating AGENTS.md.
- **Stray `/wos:create` and `/wos:preferences` references removed.** Updated
  all skill docs and cross-references to point to `/wos:init`.

### Removed

- **`/wos:create` skill** — replaced by `/wos:init`.
- **`/wos:preferences` skill** — merged into `/wos:init`.

## [0.10.0] - 2026-03-05

### Removed

- **`/wos:experiment` skill deleted.** Removed the experiment skill, state
  machine module (`wos/experiment_state.py`), CLI script
  (`scripts/experiment_state.py`), tests, and plan documents. The feature was
  fully implemented in v0.7.0 but never used in practice. To revisit, see the
  v0.7.0 changelog entry and `git log --all -- skills/experiment wos/experiment_state.py`
  for the original implementation.

## [0.9.0] - 2026-03-03

### Added

- **Claim verification for `/wos:research` skill.** New claim-level fact-checking
  workflow that catches fabricated quotes, inflated statistics, misattributions,
  and incorrect superlatives before research documents are finalized. Includes:
  - 4 claim types (quote, statistic, attribution, superlative) with a Claims Table
    format for registering and tracking verification status
  - Phase 5.5a (CoVe self-verification): extracts claims and verifies them
    independently to prevent confirmation bias
  - Phase 5.5b (citation re-verification): re-fetches sources and cross-checks
    claims against actual source content
  - 5 resolution statuses (verified, corrected, removed, unverifiable, human-review)
    with uniform contradiction resolution procedure
  - Writing constraints in Phase 5, gate checks in Phase 6, updated Quality Checklist
  - Context-reset resumption logic for the new phases
  - New reference file: `skills/research/references/claim-verification.md`
  ([#118](https://github.com/bcbeidel/wos/issues/118),
  [#121](https://github.com/bcbeidel/wos/pull/121))

## [0.8.1] - 2026-03-01

### Fixed

- **`/wos:report-issue` skill improvements.** Added adaptive follow-up probing
  for vague bug reports (capped at 2 probes), duplicate search phase before
  drafting via `gh issue list --search`, title quality check enforcing
  component + behavior + context, "Workaround / Proposed Fix" section in bug
  template, and "Acceptance Criteria" section in feature template.
  ([#112](https://github.com/bcbeidel/wos/issues/112),
  [#113](https://github.com/bcbeidel/wos/pull/113))
- **`/wos:retrospective` skill improvements.** Replaced abstract questions with
  incident-anchored prompts that ask for specific moments. Added adaptive
  follow-up with 3 probe types (vague, abstract, missing-why) capped at 1 per
  question, duplicate search phase before drafting, and a new "Synthesize Action
  Items" phase using Observation-Impact-Request structure with severity labels
  (`blocking`/`friction`/`nit`). Workflow expanded from 5 to 7 phases.
  ([#111](https://github.com/bcbeidel/wos/issues/111),
  [#114](https://github.com/bcbeidel/wos/pull/114))

## [0.8.0] - 2026-02-28

### Added

- **`/wos:retrospective` skill.** Session review and feedback workflow with
  five phases: prerequisites, reflect, gather context, draft, and submit via
  GitHub Issues.
  ([#90](https://github.com/bcbeidel/wos/issues/90),
  [#101](https://github.com/bcbeidel/wos/pull/101))
- **Auto-derive AGENTS.md areas table.** New `discover_areas()` function in
  `agents_md.py` scans `docs/context/` subdirectories and extracts area names
  from `_index.md` preambles. `reindex.py` now auto-updates the AGENTS.md
  areas table on every run, enforcing Principle 3 (single source of truth).
  ([#97](https://github.com/bcbeidel/wos/issues/97),
  [#107](https://github.com/bcbeidel/wos/pull/107))
- **Interactive URL cleanup flow.** `/wos:audit` skill now offers multi-modal
  verification options for 403/429 URL warnings: browser check, screenshot,
  PDF, pasted content, or mark as dead.
  ([#92](https://github.com/bcbeidel/wos/issues/92),
  [#103](https://github.com/bcbeidel/wos/pull/103))
- **Pipeline quality improvements.** Three new validation checks: DRAFT marker
  detection in research docs (`warn`), AGENTS.md/CLAUDE.md initialization
  checks (`warn`), and 403/429 URL responses downgraded from `fail` to `warn`.
  Distill skill now encourages explicit sibling cross-references in `related:`
  fields.
  ([#91](https://github.com/bcbeidel/wos/issues/91),
  [#102](https://github.com/bcbeidel/wos/pull/102))

### Fixed

- **Refine-prompt skill no longer auto-executes input.** Added explicit guards
  preventing Claude from treating input prompts as instructions to execute.
  ([#89](https://github.com/bcbeidel/wos/issues/89),
  [#100](https://github.com/bcbeidel/wos/pull/100))
- **CI workflow aligned with documented patterns.** Replaced `pip` with `uv`
  in GitHub Actions, added `astral-sh/setup-uv@v4`, and fixed `--extra dev`
  for optional dependencies.
  ([#93](https://github.com/bcbeidel/wos/issues/93),
  [#104](https://github.com/bcbeidel/wos/pull/104))
- **Description unified across config files.** Standardized project description
  in `plugin.json` and `pyproject.toml` to match `marketplace.json`.
  ([#94](https://github.com/bcbeidel/wos/issues/94),
  [#105](https://github.com/bcbeidel/wos/pull/105))
- **All scripts use argparse.** Converted `check_url.py`, `update_preferences.py`,
  and `get_version.py` from manual `sys.argv` to `argparse` for consistent CLI
  patterns.
  ([#95](https://github.com/bcbeidel/wos/issues/95),
  [#106](https://github.com/bcbeidel/wos/pull/106))
- **Code hygiene cleanup.** Simplified no-op type assignment in `document.py`
  and promoted `_protocol_from_json()` to public `protocol_from_json()`.
  ([#98](https://github.com/bcbeidel/wos/issues/98),
  [#108](https://github.com/bcbeidel/wos/pull/108))
- **Skill frontmatter normalized.** Added missing `argument-hint` to create
  skill and `references:` preflight declarations to all 4 skills that use it.
  ([#99](https://github.com/bcbeidel/wos/issues/99),
  [#109](https://github.com/bcbeidel/wos/pull/109))
- **`_extract_preamble()` handles empty directories.** Fixed preamble extraction
  to treat end-of-content as a valid boundary when no table line exists.
  ([#97](https://github.com/bcbeidel/wos/issues/97))

## [0.7.0] - 2026-02-28

### Added

- **`/wos:experiment` skill.** Complete 6-phase experiment framework for
  empirical validation of research claims. Guides users through Design, Audit,
  Evaluation, Execution, Analysis, and Publication with tier-appropriate depth
  (Pilot / Exploratory / Confirmatory).
  ([#67](https://github.com/bcbeidel/wos/issues/67))
  - `wos/experiment_state.py` — state machine with `ExperimentState` and
    `PhaseState` dataclasses, artifact-existence gates, phase progression,
    and backtracking with `.prev` file preservation
  - `scripts/experiment_state.py` — CLI with 6 subcommands: `init`, `status`,
    `advance`, `check-gates`, `generate-manifest`, `backtrack`
  - Blinding support: `generate_manifest()` assigns NATO phonetic opaque IDs
    (ALPHA–HOTEL) to conditions with randomized mapping
  - Backtracking: `backtrack_to_phase()` resets downstream phases and
    `preserve_artifacts()` renames existing files with `.prev` suffix
  - SKILL.md guidance for all 6 phases with conversation flows, quality checks,
    gate verification, and tier-gated interpretation
  - Supplementary sections: LLM-as-judge debiasing (5 biases + calibration
    protocol), reproducibility (tier-scaled requirements + caching strategy),
    error recovery (analyze.py failures, gate failures, abandonment), and
    edge cases (single-condition, 3+ conditions, mixed evaluation methods)
  - 8 Common Deviations entries
  - ([#74](https://github.com/bcbeidel/wos/pull/75),
    [#76](https://github.com/bcbeidel/wos/pull/81),
    [#77](https://github.com/bcbeidel/wos/pull/82),
    [#80](https://github.com/bcbeidel/wos/pull/83),
    [#78](https://github.com/bcbeidel/wos/pull/85),
    [#79](https://github.com/bcbeidel/wos/pull/86))

### Changed

- **Directory layout unified under `docs/`.** `context/` and `artifacts/`
  consolidated into `docs/context/`, `docs/plans/`, and `docs/research/`.
  Aligns with ecosystem conventions (`docs/` is the dominant standard) and
  the superpowers plugin's `docs/plans/` convention. Updated: `validators.py`,
  `reindex.py`, `agents_md.py`, all tests, 6 skill files, CLAUDE.md, README.md,
  and 20 frontmatter `related:` fields.
  ([#84](https://github.com/bcbeidel/wos/issues/84),
  [#87](https://github.com/bcbeidel/wos/pull/87))

## [0.6.0] - 2026-02-28

### Added

- **`/wos:refine-prompt` skill.** Assess and refine prompts using
  evidence-backed techniques. Three-stage pipeline (Assess → Refine →
  Present) with a 7-technique registry in Pareto priority order.
  ([#71](https://github.com/bcbeidel/wos/issues/71),
  [#73](https://github.com/bcbeidel/wos/pull/73))
- `references:` frontmatter convention — all skills with reference files
  now declare them in SKILL.md frontmatter for auto-loading. Updated:
  distill, preferences, report-issue, research.

## [0.5.0] - 2026-02-27

### Changed

- **Universal `uv run` script invocation.** All WOS scripts now use PEP 723
  inline metadata and are invoked via `uv run`. `uv` is now required to run
  WOS scripts.
  ([#70](https://github.com/bcbeidel/wos/issues/70),
  [#72](https://github.com/bcbeidel/wos/pull/72))

### Added

- `scripts/check_runtime.py` — canary script to validate `uv run` + PEP 723
  pipeline.
- `scripts/check_url.py` — URL reachability checking via `wos.url_checker`.
- `scripts/update_preferences.py` — communication preferences updates.
- `scripts/get_version.py` — print plugin version from `plugin.json`.
- `skills/_shared/references/preflight.md` — reusable 3-step preflight check
  (uv availability → canary → actual script) for skills needing `uv run`.

### Removed

- References to non-existent `CLAUDE_PLUGIN_ROOT` environment variable.

## [0.4.0] - 2026-02-26

### Changed

- **Zero runtime dependencies.** Replaced `pyyaml` with a custom restricted
  YAML subset parser (`wos/frontmatter.py`) — scalars are always strings (no
  type coercion), lists via `- item` syntax, no nested dicts. Replaced
  `requests` with `urllib.request` in `url_checker.py`. Removed unused
  `pydantic`. `pyproject.toml` now declares `dependencies = []`.
  ([#68](https://github.com/bcbeidel/wos/issues/68),
  [#69](https://github.com/bcbeidel/wos/pull/69))
- **Warn/fail severity in validators.** `check_frontmatter()` now merges the
  old `check_research_sources()` and adds two new warnings: dict-format source
  items (`warn`) and context files missing `related` fields (`warn`). All
  validators return issues with explicit `severity: "fail"` or `"warn"`.
- **LLM-friendly audit output.** `scripts/audit.py` now prints a summary line
  (`N fail, M warn across K files`) followed by a table with severity column.
  Exit code: 1 on any `fail`, 0 on `warn` only. New `--strict` flag exits 1
  on any issue.
- **Single-file audit mode.** `audit.py` accepts an optional positional file
  argument for validating a single document. `scripts/validate.py` removed
  (functionality merged into `audit.py`).
- **Preamble-preserving indexes.** `generate_index()` accepts an optional
  `preamble` parameter. `check_index_sync()` and `reindex.py` extract and
  preserve existing preambles during regeneration. `check_all_indexes()` warns
  when an `_index.md` has no area description preamble.
- **`Document.extra` field removed.** Unknown frontmatter keys are ignored
  rather than stored.
- **Research protocol CLI removed.** `main()` and `if __name__` block stripped
  from `research_protocol.py`. Search protocols are now formatted as inline
  markdown tables in the research document.

### Added

- `wos/frontmatter.py` — custom YAML subset parser (stdlib-only, 94 lines).
- `wos/validators.check_content()` — warns when context files exceed 800 words
  (configurable via `--context-max-words`). Artifacts and `_index.md` excluded.
- `/wos:distill` skill — converts research artifacts into focused context files
  with confidence mapping, word count guidance, splitting heuristics, and
  bidirectional linking. Includes `references/distillation-guidelines.md`.
- `/wos:create` skill now prompts for area description preambles, checks word
  count, and suggests `related:` candidates with bidirectional linking.
- 14 new tests across `test_frontmatter.py` (22 tests), `test_index.py`
  (6 preamble tests), `test_validators.py` (8 new check tests), and
  `test_audit.py` (11 tests rewritten for new output format).

### Removed

- `scripts/validate.py` and `tests/test_validate.py` — merged into `audit.py`.
- `research_protocol.py` CLI entry point (`main()`, argparse, `--summary`).
- Runtime dependencies: `pyyaml`, `requests`, `pydantic`.

## [0.3.6] - 2026-02-25

### Fixed

- Research skill restructured for workflow compliance — declared tool
  dependencies in `compatibility` field, added phase gates and common
  deviations to SKILL.md, inlined `url_checker` command at point of use in
  Phase 3, and search protocol is now persisted on disk in DRAFT document
  during research sessions.
  ([#65](https://github.com/bcbeidel/wos/issues/65),
  [#66](https://github.com/bcbeidel/wos/issues/66))

### Added

- Experiment framework design document for empirical claim validation
  (`artifacts/plans/2026-02-25-experiment-framework-design.md`).

## [0.3.5] - 2026-02-25

### Fixed

- Audit URL reachability check no longer crashes on dict-format sources
  (`{url: ..., title: ...}`) — sources are normalized to URL strings before
  passing to `check_urls()`.
  ([#61](https://github.com/bcbeidel/wos/issues/61))

## [0.3.4] - 2026-02-25

### Fixed

- Research workflow no longer references unreachable `/wos:create` skill —
  replaced with direct document creation instructions.
  ([#56](https://github.com/bcbeidel/wos/issues/56))
- Python utility paths in skill references now use `${CLAUDE_PLUGIN_ROOT}`
  instead of bare relative paths that failed in installed plugin mode.
  Scripts also include `sys.path` self-insertion for plugin cache
  compatibility.
  ([#59](https://github.com/bcbeidel/wos/issues/59))
- Research workflow restructured for progressive document building — the
  document is created in Phase 2 and updated at each phase boundary, so
  intermediate work survives context window resets. Includes a resumption
  heuristic for detecting which phases are complete.
  ([#60](https://github.com/bcbeidel/wos/issues/60))

## [0.3.3] - 2026-02-25

### Fixed

- All skills now explicitly set `user-invocable: true` in SKILL.md frontmatter
  so they appear as `/wos:*` slash commands when the plugin is installed.
  Previously, `create` had `user-invocable: false`, and `consider`, `research`,
  `report-issue`, and `preferences` omitted the field entirely (relying on
  default behavior).

## [0.3.2] - 2026-02-25

### Fixed

- `not_searched` format mismatch between docs and code — clarified format as
  `List[str]` in research workflow and added input validation in
  `_protocol_from_json()` that raises `ValueError` for non-string entries.
  ([#52](https://github.com/bcbeidel/wos/issues/52))
- Research quality gate updated to use `python3 scripts/validate.py` (runs all
  4 checks) instead of `parse_document()` which only validated generic fields.
  ([#54](https://github.com/bcbeidel/wos/issues/54))

### Added

- `scripts/validate.py` — CLI for single-file validation (`python3
  scripts/validate.py <file> [--root DIR] [--no-urls]`). Runs frontmatter,
  research sources, source URLs, and related paths checks.
  ([#53](https://github.com/bcbeidel/wos/issues/53))
- `skills/research/references/python-utilities.md` — reference doc for all CLI
  commands used during research sessions (validate, audit, research protocol
  format), including full JSON schema and Document model fields.
  ([#53](https://github.com/bcbeidel/wos/issues/53))
- Fetch failure guidance in research workflow Phase 2 — documents parallel
  `WebFetch` cascading failures and 403/301/timeout handling.
  ([#55](https://github.com/bcbeidel/wos/issues/55))
- Source diversity guidance in research workflow Phase 1 — acknowledges
  `WebSearch` single-engine limitation with workarounds.
  ([#55](https://github.com/bcbeidel/wos/issues/55))
- `tests/test_validate.py` — 5 tests for the new validate CLI.
- 2 new tests in `tests/test_research_protocol.py` for `not_searched`
  validation.

## [0.3.1] - 2026-02-24

### Fixed

- Audit script now displays file paths relative to `--root` instead of absolute
  paths, making output readable in narrow terminals and Claude Code.
- Python warnings (e.g. urllib3 NotOpenSSLWarning) suppressed from audit output.
- Summary footer added to audit failure output (e.g. "3 issues found.").
  ([#50](https://github.com/bcbeidel/wos/issues/50))

### Added

- `tests/test_audit.py` — 9 tests covering audit CLI output formatting.

## [0.3.0] - 2026-02-24

### Added

- `wos/research_protocol.py` — search protocol logging for research
  auditability. `SearchEntry` and `SearchProtocol` dataclasses, markdown table
  renderer (`format_protocol`), one-line summary (`format_protocol_summary`),
  JSON parser, and CLI entry point (`python3 -m wos.research_protocol format
  [--summary]`).
- `skills/research/references/challenge-phase.md` — Challenge phase quality
  gate with three sub-steps: Assumptions Check (all modes), Analysis of
  Competing Hypotheses (deep-dive, options, competitive, feasibility), and
  Premortem (all modes).
- `skills/research/references/research-workflow.md` — 6-phase research workflow
  integrating search protocol logging, Challenge phase, and confidence levels.
- Challenge column and sub-step matrix added to
  `skills/research/references/research-modes.md`.
- Three new key rules in `/wos:research` SKILL.md: challenge before synthesis,
  log search protocol, confidence levels on every finding.
- 19 new tests in `tests/test_research_protocol.py`.

### Changed

- `/wos:research` workflow restructured from 7 phases to 6 phases. Phase 4
  (Challenge) inserted between Verify & Evaluate and Synthesize. Phase 5
  (Synthesize) now requires confidence level annotations (HIGH/MODERATE/LOW)
  on every finding. Phase 6 (Produce Research Document) includes search
  protocol table insertion.
  ([#39](https://github.com/bcbeidel/wos/issues/39),
  [#49](https://github.com/bcbeidel/wos/pull/49))

### Removed

- `skills/research/references/research-investigate.md` — replaced by
  `research-workflow.md`.

## [0.2.1] - 2026-02-23

### Removed

- `wos/source_verification.py` and `tests/test_source_verification.py` — 1,021
  lines of dead code. Module was unused by any production import and duplicated
  `url_checker.py`. Research skill references updated to use `url_checker`.

### Added

- `wos/markers.py` — shared `replace_marker_section()` utility extracted from
  duplicated logic in `agents_md.py` and `preferences.py`.
- `tests/test_version.py` — version consistency test asserting `pyproject.toml`,
  `plugin.json`, and `marketplace.json` all have matching versions.

### Changed

- `wos/index.py` now uses `document.parse_document()` for frontmatter extraction
  instead of its own independent YAML parsing.
- Renamed `check_urls` parameter to `verify_urls` in `validators.py` to avoid
  shadowing the imported `check_urls` function from `url_checker.py`.
- `/wos:report-issue` skill simplified from 6 phases to 4. Merged Classify into
  Gather Context, merged Preview into Draft. Trimmed feature request template
  (removed Evaluation, Alternatives Considered, Why This Matters sections).

## [0.2.0] - 2026-02-22

### Changed

- **Architecture simplification.** Replaced 23-class DDD hierarchy with a
  single `Document` dataclass. Reduced 18 validators to 5 essential checks.
  Merged 11 skills into 6. Replaced hand-curated `_overview.md` with
  auto-generated `_index.md`. Net: +2,239 / -14,000 lines.
  ([#38](https://github.com/bcbeidel/wos/pull/38))

### Removed

- `wos/models/` directory (23 classes, DDD hierarchy)
- `wos/cross_validators.py`, `wos/templates.py`, `wos/auto_fix.py`,
  `wos/token_budget.py`, `wos/discovery.py`, `wos/scaffold.py`,
  `wos/document_types.py`, `wos/formatting.py`
- Skills: `create-context`, `create-document`, `discover`, `fix`,
  `update-context`, `update-document`, `health`, `observe`
- Document type subclasses, section ordering validation, size bounds,
  staleness tracking, auto-fix engine, token budget estimation
- Old `scripts/check_health.py`, `scripts/scan_context.py`,
  `scripts/create_document.py`, `scripts/update_discovery.py`,
  `scripts/create_context.py`

### Added

- `wos/document.py` — single `Document` dataclass + `parse_document()`
- `wos/index.py` — `_index.md` generation + sync checking
- `wos/validators.py` — 5 validation checks (frontmatter, research sources,
  URLs, related paths, index sync)
- `wos/url_checker.py` — HTTP HEAD/GET URL reachability
- `wos/agents_md.py` — marker-based AGENTS.md section management
- `scripts/audit.py` — CLI for validation with `--fix` for index regeneration
- `scripts/reindex.py` — CLI for `_index.md` regeneration
- `/wos:create` — unified skill (replaces create-context + create-document)
- `/wos:audit` — rewritten to use 5-check system

## [0.1.9] - 2026-02-20

### Added

- **Communication preferences** (`wos/preferences.py`): Capture user
  communication preferences via five evidence-based dimensions (directness,
  verbosity, depth, expertise, tone) and write them as structured LLM
  instructions in CLAUDE.md using `<!-- wos:communication:begin/end -->`
  markers. New `/wos:preferences` skill with freeform capture workflow.
  Optional preferences step added to `/wos:create-context` initialization.
  ([#22](https://github.com/bcbeidel/wos/issues/22))
- **Progressive context scanner** (`scripts/scan_context.py`): Token-efficient
  context discovery with three progressive subcommands: `index` (list all
  documents, filterable by area/type), `outline` (section headings with word
  counts), and `extract` (raw section content). Reduces typical context lookup
  from ~8,500 tokens (4 Read calls) to ~700-1,000 tokens (2 Bash calls).
  ([#12](https://github.com/bcbeidel/wos/issues/12))
- **Discover skill** (`/wos:discover`): Routes agents through the progressive
  index → outline → extract pattern for finding and accessing context.

### Changed

- **AGENTS.md is now the primary config file.** The context manifest (area
  table between `<!-- wos:context:begin/end -->` markers) is written to
  AGENTS.md instead of CLAUDE.md. CLAUDE.md becomes a thin pointer with an
  `@AGENTS.md` reference so Claude Code loads it. Existing CLAUDE.md files
  with old-style markers are automatically migrated on the next discovery run.
  `check_manifest_sync` now validates AGENTS.md instead of CLAUDE.md.
  ([#23](https://github.com/bcbeidel/wos/issues/23))
- **Human-readable health output** is now the default. `scripts/check_health.py`
  outputs formatted text with issues sorted by severity, one line per issue in
  summary mode, or grouped by severity with suggestions in `--detailed` mode.
  JSON output preserved via `--json` flag. Basic ANSI color auto-detected on
  TTY, disabled with `--no-color`.
  ([#15](https://github.com/bcbeidel/wos/issues/15))
- Audit skill workflows simplified to show text output directly instead of
  instructing the LLM to parse and format JSON.

## [0.1.8] - 2026-02-19

### Added

- **Note document type** (`document_type: note`): A generic document type with
  minimal frontmatter requirements (`document_type` + `description` only). Notes
  can live anywhere in the repo without failing health checks, have no required
  sections, no directory constraints, and are excluded from the CLAUDE.md
  manifest. Useful for work products that don't fit the topic/overview/research/
  plan schema — decision records, reading notes, templates, personal docs, etc.
  ([#5](https://github.com/bcbeidel/wos/issues/5))

## [0.1.7] - 2026-02-18

### Improved

- **Report-issue skill: quality gates, framing guidance, and LLM invocability.**
  The `/wos:report-issue` skill now produces higher-quality issues with three
  changes: (1) the agent can invoke the skill proactively when it discovers WOS
  issues during normal work (`disable-model-invocation` removed), (2) templates
  include evaluation criteria, MRE sections, scope/non-goals, and before/after
  examples matching the quality standard of issue #12, (3) a framing rule in the
  drafting phase prevents consumer-specific language, and an advisory quality
  checklist is shown alongside the preview before submission.
  ([#14](https://github.com/bcbeidel/wos/issues/14))

## [0.1.6] - 2026-02-18

### Improved

- **Health check error messages now include expected section lists** for both
  `check_section_presence` and `check_section_ordering` validators. When a
  section is missing or misordered, the `suggestion` field lists all required
  sections in canonical order for that document type, eliminating the
  "whack-a-mole" pattern of fixing one section, re-running health, and
  discovering the next. ([#9](https://github.com/bcbeidel/wos/issues/9))

## [0.1.5] - 2026-02-18

### Added

- **Source URL reachability checking** (`wos/source_verification.py`): Lightweight
  HEAD-request reachability check for source URLs, wired into `/wos:health` behind
  `--tier2` flag. Cross-validator deduplicates URLs across documents and reports
  unreachable (404, DNS, timeout) as `warn` and access-restricted (403) as `info`.

## [0.1.4] - 2026-02-18

### Added

- **Token budget estimation** (`wos/token_budget.py`): Estimates aggregate token
  cost of context files using a `words × 1.3` heuristic, grouped by area. Always
  included in `/wos:health` output as a `token_budget` key with per-area breakdown,
  total estimate, and configurable warning threshold (default 40K tokens). Emits
  `severity: warn` issue when total context exceeds threshold.
  ([#7](https://github.com/bcbeidel/wos/issues/7))

### Fixed

- Pre-existing lint issues in `tests/test_source_verification.py` (unused import,
  line length, import sorting)

## [0.1.3] - 2026-02-18

### Added

- **Source URL verification** (`wos/source_verification.py`): Mechanical
  verification pass that checks cited source URLs resolve and page titles match
  cited titles. Catches hallucinated sources, dead links, and title mismatches
  before they propagate into context files. ([#6](https://github.com/bcbeidel/wos/issues/6))
  - `verify_sources()` for batch URL checking with structured `VerificationResult` output
  - HTTP status handling: 404/DNS/timeout → removed; 403/5xx/cross-domain redirect → flagged
  - Title comparison via normalized substring matching (lowercase, strip punctuation, collapse whitespace)
  - HTML `<title>` extraction with `<h1>` fallback using stdlib `html.parser`
  - CLI entry point: `python3 -m wos.source_verification` (JSON stdin/stdout, human summary on stderr)
- **Research skill workflow integration**: New Phase 3 (Verify Sources) inserted
  between source gathering and SIFT evaluation in `research-investigate.md`,
  with `source-verification.md` reference for agent instructions

### Fixed

- `titles_match()` no longer vacuously matches when either title normalizes to
  an empty string
- `verify_source()` now catches all `requests.RequestException` subclasses
  (e.g., `TooManyRedirects`, `SSLError`) instead of only `ConnectionError` and
  `Timeout`

### Changed

- Added `requests>=2.28` to project dependencies

## [0.1.2] - 2026-02-18

### Changed

- **Rename work-os → wos** across entire project for consistency with plugin
  prefix (`/wos:`). GitHub repo renamed `bcbeidel/work-os` → `bcbeidel/wos`.
- Context markers: `<!-- wos:context:begin -->` / `<!-- wos:context:end -->`
- Rules file: `.claude/rules/wos-context.md`
- Data directory: `.wos/` (was `.work-os/`)
- Package name in pyproject.toml: `wos`
- Marketplace and plugin config: name and repo updated

## [0.1.0] - 2026-02-18

First complete release of wos — a Claude Code plugin for building and
maintaining structured project context. All 10 v0.1-foundation phases
implemented with 229 tests passing.

### Added

#### Foundation (Phases 1.1–1.2)

- **Document type models** (`wos/document_types.py`): Pydantic v2 models for
  four document types (topic, overview, research, plan) with discriminated
  union `parse_document()`, dispatch tables for sections, size bounds, and
  directory patterns
- **Discovery layer** (`wos/discovery.py`): Auto-generates CLAUDE.md manifest
  with marker-delimited `## Context` section, `.claude/rules/work-os-context.md`
  rules file, and AGENTS.md mirroring — all derived from files on disk (note: rules file renamed to `.claude/rules/wos-context.md` in v0.1.2)

#### Core Skills (Phases 2.1–3.2)

- **Setup skill** (`/wos:setup`): Project scaffolding with `context/` directory
  structure, area creation with `_overview.md` files, discovery artifact
  generation
- **Health skill** (`/wos:health`): Type-dispatched Tier 1 validators (section
  presence/ordering, size bounds, directory placement, staleness, source
  diversity), Tier 2 LLM triggers, cross-validators (link graph, overview-topic
  sync, manifest drift, naming conventions), CLI entry point with JSON output
- **Curate skill** (`/wos:curate`): Document creation and update workflows for
  all four types, template rendering with `parse_document()` round-trip
  validation, manifest regeneration after context-type changes
- **Maintain skill** (`/wos:maintain`): Auto-fix engine with dispatch table
  (section reordering, missing sections, last_updated), lifecycle state machine
  for plan status transitions, manifest regeneration, cleanup for unparseable
  files

#### Standalone Skills (Phases 4.1–4.2)

- **Report-issue skill** (`/wos:report-issue`): GitHub issue submission workflow
  via `gh` CLI with context gathering, issue classification, draft preview,
  and explicit approval before submission
- **Consider skill** (`/wos:consider`): 16 mental model files (first-principles,
  inversion, pareto, 5-whys, SWOT, etc.) with uniform structure for structured
  reasoning

#### Capability Skills (Phase 5.1)

- **Research skill** (`/wos:research`): SIFT-based investigation framework with
  8 modes (deep dive, landscape, technical, feasibility, competitive, options,
  historical, open source), T1–T6 source hierarchy, and structured output as
  research documents

#### Extended Skills (Phase 6.1)

- **Observe skill** (`/wos:observe`): PostToolUse hook for auto-logging Read
  access to context files, utilization data layer (JSONL append-only log with
  record/aggregate/purge), recommendations engine with 6 categories
  (stale_high_use, never_referenced, low_utilization, hot_area, cold_area,
  expand_depth) gated by minimum data thresholds, dashboard/recommendations/
  trends workflows

#### Infrastructure

- Plugin manifest (`.claude-plugin/plugin.json`) with `/wos:` skill prefix
- GitHub Actions CI with pytest + ruff on push
- Design documents and research artifacts in `artifacts/research/v0.1-foundation/`
- Build roadmap with session protocol and dependency graph
- 18 design principles across four layers

[0.19.0]: https://github.com/bcbeidel/wos/releases/tag/v0.19.0
[0.18.1]: https://github.com/bcbeidel/wos/releases/tag/v0.18.1
[0.18.0]: https://github.com/bcbeidel/wos/releases/tag/v0.18.0
[0.17.0]: https://github.com/bcbeidel/wos/releases/tag/v0.17.0
[0.16.1]: https://github.com/bcbeidel/wos/releases/tag/v0.16.1
[0.15.0]: https://github.com/bcbeidel/wos/releases/tag/v0.15.0
[0.14.0]: https://github.com/bcbeidel/wos/releases/tag/v0.14.0
[0.13.0]: https://github.com/bcbeidel/wos/releases/tag/v0.13.0
[0.12.4]: https://github.com/bcbeidel/wos/releases/tag/v0.12.4
[0.12.3]: https://github.com/bcbeidel/wos/releases/tag/v0.12.3
[0.12.2]: https://github.com/bcbeidel/wos/releases/tag/v0.12.2
[0.12.1]: https://github.com/bcbeidel/wos/releases/tag/v0.12.1
[0.12.0]: https://github.com/bcbeidel/wos/releases/tag/v0.12.0
[0.11.0]: https://github.com/bcbeidel/wos/releases/tag/v0.11.0
[0.10.0]: https://github.com/bcbeidel/wos/releases/tag/v0.10.0
[0.9.0]: https://github.com/bcbeidel/wos/releases/tag/v0.9.0
[0.8.1]: https://github.com/bcbeidel/wos/releases/tag/v0.8.1
[0.8.0]: https://github.com/bcbeidel/wos/releases/tag/v0.8.0
[0.7.0]: https://github.com/bcbeidel/wos/releases/tag/v0.7.0
[0.6.0]: https://github.com/bcbeidel/wos/releases/tag/v0.6.0
[0.5.0]: https://github.com/bcbeidel/wos/releases/tag/v0.5.0
[0.4.0]: https://github.com/bcbeidel/wos/releases/tag/v0.4.0
[0.3.6]: https://github.com/bcbeidel/wos/releases/tag/v0.3.6
[0.3.5]: https://github.com/bcbeidel/wos/releases/tag/v0.3.5
[0.3.4]: https://github.com/bcbeidel/wos/releases/tag/v0.3.4
[0.3.3]: https://github.com/bcbeidel/wos/releases/tag/v0.3.3
[0.3.2]: https://github.com/bcbeidel/wos/releases/tag/v0.3.2
[0.3.1]: https://github.com/bcbeidel/wos/releases/tag/v0.3.1
[0.3.0]: https://github.com/bcbeidel/wos/releases/tag/v0.3.0
[0.2.1]: https://github.com/bcbeidel/wos/releases/tag/v0.2.1
[0.2.0]: https://github.com/bcbeidel/wos/releases/tag/v0.2.0
[0.1.9]: https://github.com/bcbeidel/wos/releases/tag/v0.1.9
[0.1.8]: https://github.com/bcbeidel/wos/releases/tag/v0.1.8
[0.1.7]: https://github.com/bcbeidel/wos/releases/tag/v0.1.7
[0.1.6]: https://github.com/bcbeidel/wos/releases/tag/v0.1.6
[0.1.5]: https://github.com/bcbeidel/wos/releases/tag/v0.1.5
[0.1.4]: https://github.com/bcbeidel/wos/releases/tag/v0.1.4
[0.1.3]: https://github.com/bcbeidel/wos/releases/tag/v0.1.3
[0.1.2]: https://github.com/bcbeidel/wos/releases/tag/v0.1.2
[0.1.0]: https://github.com/bcbeidel/wos/releases/tag/v0.1.0
