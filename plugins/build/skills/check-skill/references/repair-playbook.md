---
name: Skill Repair Playbook (check-skill)
description: Per-failure-mode repair strategies for check-skill findings against SKILL.md files — canonical fixes for Tier-1 deterministic findings, Tier-2 semantic dimensions, and Tier-3 description collisions.
---

# Skill Repair Playbook

Every FAIL and WARN finding maps to a canonical repair. Before applying
any repair, state the original intent explicitly: **"This skill guides
Claude to [original workflow]."** Verify the proposed repair preserves
that workflow. If the repair would change what the skill *does* (not
just how it's phrased or structured), flag it as requiring human review
before applying.

## Table of Contents

- [Tier 1: Deterministic Format Repairs](#tier-1-deterministic-format-repairs)
  - [Wrong Filename](#wrong-filename)
  - [Directory Basename Mismatch](#directory-basename-mismatch)
  - [Name Slug Invalid](#name-slug-invalid)
  - [Reserved Name Token](#reserved-name-token)
  - [Missing Required Frontmatter Key](#missing-required-frontmatter-key)
  - [Malformed Version](#malformed-version)
  - [Description Cap Exceeded](#description-cap-exceeded)
  - [Missing Required Section](#missing-required-section)
  - [Steps Not an Ordered List](#steps-not-an-ordered-list)
  - [Steps Numbering Non-Sequential](#steps-numbering-non-sequential)
  - [Examples Lacks Fenced Block](#examples-lacks-fenced-block)
  - [Body Length Over Threshold](#body-length-over-threshold)
  - [Line Length Over 120](#line-length-over-120)
  - [Secret Detected in Body](#secret-detected-in-body)
  - [Remote-Exec or Destructive Command](#remote-exec-or-destructive-command)
  - [Prose Hedges or Absolute Paths](#prose-hedges-or-absolute-paths)
- [Tier 2: Semantic Dimensions](#tier-2-semantic-dimensions)
  - [Dimension 1: Description Retrieval Signal](#dimension-1-description-retrieval-signal)
  - [Dimension 2: Trigger Conditions](#dimension-2-trigger-conditions)
  - [Dimension 3: Step Discipline](#dimension-3-step-discipline)
  - [Dimension 4: Clarity and Consistency](#dimension-4-clarity-and-consistency)
  - [Dimension 5: Prerequisites and Contract](#dimension-5-prerequisites-and-contract)
  - [Dimension 6: Failure Handling](#dimension-6-failure-handling)
  - [Dimension 7: Safety Gating](#dimension-7-safety-gating)
  - [Dimension 8: Example Realism](#dimension-8-example-realism)
- [Tier 3: Description Collisions](#tier-3-description-collisions)

---

## Tier 1: Deterministic Format Repairs

### Wrong Filename

**Signal:** File is not named `SKILL.md` (case-sensitive).

**CHANGE:** Rename the file to `SKILL.md`.
**FROM:** `plugins/build/skills/foo/skill.md`
**TO:** `plugins/build/skills/foo/SKILL.md`
**REASON:** Claude Code's skill loader matches on `SKILL.md` exactly. Lowercase or extension variants are invisible to the loader.

### Directory Basename Mismatch

**Signal:** Parent directory basename does not equal the frontmatter `name` field.

**CHANGE:** Either rename the directory to match `name`, or update `name` to match the directory. Prefer renaming the directory unless the skill is already published and consumers reference `name`.
**FROM:** `skills/csv-to-parquet/SKILL.md` with `name: csv_to_parquet`
**TO:** `skills/csv-to-parquet/SKILL.md` with `name: csv-to-parquet`
**REASON:** The skill collection keys on `name` for routing. Drift between directory and identifier breaks discovery and produces inconsistent citations.

### Name Slug Invalid

Covers three subtypes:

#### Non-kebab-case

**Signal:** `name` contains uppercase letters, underscores, or punctuation other than hyphens.

**CHANGE:** Rewrite as lowercase kebab-case.
**FROM:** `name: CSV_to_Parquet`
**TO:** `name: csv-to-parquet`
**REASON:** Canonical slug format is `^[a-z0-9]+(-[a-z0-9]+)*$`. Other forms break tooling that parses skill names as identifiers.

#### Over 64 characters

**Signal:** `name` length exceeds 64 chars.

**CHANGE:** Shorten while preserving meaning.
**FROM:** `name: convert-csv-to-apache-parquet-with-compression-options-and-schema-inference`
**TO:** `name: convert-csv-to-parquet`
**REASON:** Long names degrade routing match quality and clutter the CLI. Move detail into `description`.

#### Uniqueness collision

**Signal:** Another skill in the collection already claims the same `name`.

**CHANGE:** Rename the newer skill to a distinct, more specific name.
**FROM:** two skills both named `deploy`
**TO:** `deploy-staging` and `deploy-production`, or merge the two workflows into one skill
**REASON:** Name collisions force arbitrary selection. Routing becomes nondeterministic.

### Reserved Name Token

**Signal:** `name` contains `anthropic` or `claude`.

**CHANGE:** Rename without the reserved token.
**FROM:** `name: claude-helper`
**TO:** `name: workflow-helper`
**REASON:** `anthropic` and `claude` collide with platform-owned namespaces and are rejected at skill-load time.

### Missing Required Frontmatter Key

**Signal:** One or more of `name` / `description` / `version` / `owner` is missing or empty.

**CHANGE:** Add the missing key with a valid value.
**FROM:** frontmatter without `owner`
**TO:** `owner: data-platform` (or a resolvable person/team)
**REASON:** These four fields anchor identity, routing, cache-busting, and ownership. Missing any of them degrades discoverability, release semantics, or maintenance — a skill with no owner rots unclaimed.

### Malformed Version

**Signal:** `version` does not match `^\d+\.\d+\.\d+$`.

**CHANGE:** Rewrite as semver `MAJOR.MINOR.PATCH`.
**FROM:** `version: 1.0` or `version: v1.0.0` or `version: 0.1-beta`
**TO:** `version: 1.0.0`
**REASON:** Semver is the cache-busting signal consumers rely on. Non-semver strings confuse release tooling and invalidate comparison semantics.

### Description Cap Exceeded

**Signal:** `description` > 1024 chars, or `description` + `when_to_use` > 1536 chars combined.

**CHANGE:** Split trigger phrases into `when_to_use` (combined cap 1536) rather than compressing the description.
**FROM:** 1100-char description cramming capability + every trigger phrase into one field
**TO:** description stays ≤1024 (the trigger opener and one-sentence purpose); trigger enumeration moves to `when_to_use`
**REASON:** Description is the primary retrieval signal; compressing it erodes the routing surface. The `when_to_use` split preserves the full trigger set without truncating the routing-critical opener.

### Missing Required Section

**Signal:** Body lacks one of `## When to use`, `## Prerequisites`, `## Steps`, `## Failure modes`, `## Examples`.

**CHANGE:** Add the missing section with real content (not a placeholder).
**FROM:** skill with no `## Failure modes` heading
**TO:** skill with a `## Failure modes` section naming at least three likely failures and their recovery actions
**REASON:** Silence on any of the five canonical sections is the structural anti-pattern the principles doc targets. Agents invent behavior where the skill is silent.

### Steps Not an Ordered List

**Signal:** `## Steps` is prose, bullet list, or otherwise not a Markdown ordered list.

**CHANGE:** Convert to an ordered list starting at 1, one atomic action per item.
**FROM:** "First, read the file. Then, validate its shape. Finally, write the output."
**TO:**
```markdown
1. Read `$ARGUMENTS`.
2. Validate the input matches `^.+\.csv$`.
3. Write the converted output to `./output.parquet`.
```
**REASON:** Numbered ordered lists are followed more reliably than prose or bullets. The structure itself is instruction.

### Steps Numbering Non-Sequential

**Signal:** Ordered list increments skip values or restart mid-sequence.

**CHANGE:** Renumber 1..N sequentially.
**FROM:** `1. … 2. … 4. … 5. …`
**TO:** `1. … 2. … 3. … 4. …`
**REASON:** Gaps in numbering break the sequence contract and confuse readers about whether a step was removed or missed.

### Examples Lacks Fenced Block

**Signal:** `## Examples` section exists but contains no fenced code block.

**CHANGE:** Add at least one fenced block showing input, output, and any side effects.
**FROM:** prose description of what a call might look like
**TO:** fenced block with the exact invocation and its result
**REASON:** Concrete examples anchor the model better than abstract rules. Models copy-paste better than they translate prose.

### Body Length Over Threshold

**Signal:** Non-blank line count exceeds 300 (WARN) or 400 (FAIL).

**CHANGE:** Move reference material, long examples, or complex scripts into sibling files under `references/` and `scripts/`.
**FROM:** 450-line SKILL.md that includes a 200-line embedded shell script
**TO:** <400-line SKILL.md that references `./scripts/convert.sh`
**REASON:** Every line is paid for in context tokens at invocation time. Long skills degrade both model focus and review quality.

### Line Length Over 120

**Signal:** Any line outside fenced blocks and URLs exceeds 120 chars.

**CHANGE:** Wrap the line. In prose, break at a natural clause boundary.
**REASON:** Improves diff readability and matches toolkit-wide conventions.

### Secret Detected in Body

**Signal:** Body matches an AWS/GitHub/OpenAI/Anthropic/Stripe key pattern or a credential-shaped variable assignment.

**CHANGE:** Replace the literal with an env-var reference or vault path. Rotate the exposed credential.
**FROM:** `AWS_ACCESS_KEY=AKIAIOSFODNN7EXAMPLE`
**TO:** `AWS_ACCESS_KEY=${AWS_ACCESS_KEY}`
**REASON:** Skill files are committed config; a committed credential is a breach. Rotation is mandatory regardless of whether the finding surfaces here or later — history retains the exposed value.

### Remote-Exec or Destructive Command

**Signal:** Shell code blocks contain `curl | bash`, `eval $(curl …)`, `source <(curl …)`, or destructive commands (`rm -rf`, `dd if=`, `DROP TABLE`, `TRUNCATE`, force-push, `mv` without `-i`) without safety flags or a preceding approval gate.

**CHANGE for remote-exec:** pin a version and verify a hash, or install via the package manager.
**FROM:** `curl -fsSL https://example.com/install.sh | bash`
**TO:** `curl -fsSL https://example.com/install.sh -o install.sh && echo "<sha256> install.sh" | sha256sum --check && bash install.sh`

**CHANGE for destructive cmd:** precede with an approval step or convert to a dry-run default.
**FROM:** `rm -rf ./build/`
**TO:**
```markdown
1. Ask the user to confirm the build directory should be deleted.
2. On confirmation, run `rm -rf ./build/`.
```
**REASON:** Remote-exec is a supply-chain vector; destructive commands are often legitimate when gated but dangerous when ungated. D7 Safety Gating judges whether the gate exists.

### Prose Hedges or Absolute Paths

**Signal:** Body contains hedging words from the banned list, or absolute-path references that break portability.

**CHANGE for hedges:** replace with direct phrasing or delete the hedge.
**FROM:** "Generally, you should probably run this before the build step, etc."
**TO:** "Run this before the build step."

**CHANGE for absolute paths:** convert to relative paths or environment variables.
**FROM:** `bash /home/alice/project/scripts/convert.sh`
**TO:** `bash ./scripts/convert.sh`
**REASON:** Hedges propagate ambiguity into model behavior. Absolute paths break the skill on relocation.

---

## Tier 2: Semantic Dimensions

### Dimension 1: Description Retrieval Signal

**Signal:** Description reads as capability ("Handles X") rather than trigger ("Use when the user asks to X").

**CHANGE:** Rewrite the first clause as a trigger. Name at least one concrete user phrase, file extension, error string, or event type.
**FROM:** `description: Handles tabular conversion and data transformation workflows.`
**TO:** `description: Use when the user asks to convert .csv to .parquet, transform tabular data, or mentions "read_csv" / "to_parquet". Produces Parquet output with inferred schema.`
**REASON:** Descriptions are the router's retrieval signal. Capability phrasing ("handles") names what the skill contains; trigger phrasing ("use when") names the situation that invokes it.

### Dimension 2: Trigger Conditions

**Signal:** `## When to use` bullets restate the description or are too abstract.

**CHANGE:** Rewrite bullets to name concrete triggers not already in the description.
**FROM:**
```markdown
## When to use
- When you need data transformation
- When working with tabular data
```
**TO:**
```markdown
## When to use
- The user pastes a `.csv` path and asks for Parquet output
- A data pipeline step requires columnar storage for downstream queries
- A notebook loads a CSV and hits memory pressure — Parquet reduces it
```
**REASON:** The description retrieves; this section confirms. Restating the description wastes budget and adds no routing signal.

### Dimension 3: Step Discipline

**Signal:** Steps in passive voice, commentary embedded in step body, conditional nesting ≥3 levels, or multi-action fused steps.

**CHANGE:** Rewrite each step as a single imperative action. Move rationale to surrounding prose. Split fused steps. Extract deep branches into a separate skill.
**FROM:**
```markdown
1. The input file should be read, and then — because we want to avoid double-processing — it should be validated against the schema registry; if the schema is new, we'd want to cache it, and if the cache exists but is stale, refresh it; either way, proceed to writing.
```
**TO:**
```markdown
1. Read `$ARGUMENTS`.
2. Validate the input's schema against the registry.
3. If the schema is not cached, cache it. If the cache is stale, refresh it.
4. Write the Parquet output to `./output.parquet`.
```
**REASON:** Atomic imperative steps are followed reliably. Commentary and fused actions degrade instruction-following.

### Dimension 4: Clarity and Consistency

**Signal:** Undefined jargon, inconsistent terminology, or non-obvious hedging.

**CHANGE:** Define domain terms on first use. Pick one name per concept and use it throughout. Replace "where applicable" / "if possible" with direct phrasing or concrete conditions.
**FROM:** "The DAG's upstream CDC source feeds into the staging ELT, where `service_id` (later renamed `svc`) indexes into …"
**TO:** "The pipeline's upstream change-data-capture source feeds into the staging ELT, where `service_id` indexes into …"
**REASON:** Undefined jargon excludes readers; inconsistent naming forces re-derivation at every reference.

### Dimension 5: Prerequisites and Contract

**Signal:** Prerequisites section is generic, missing dependencies referenced in Steps, or omits privilege/I-O shape when the skill needs them.

**CHANGE:** Enumerate tools, versions, env vars, privilege tier (for elevated skills), and input/output shapes. Cross-check against Steps.
**FROM:**
```markdown
## Prerequisites
- Terminal access
- git
```
**TO:**
```markdown
## Prerequisites
- `pandas >= 2.0`, `pyarrow >= 14.0`
- Env var `AWS_PROFILE` set to a profile with `s3:PutObject` on the target bucket
- Input: path to a `.csv` file (first row is header)
- Output: a `.parquet` file at `<input>.parquet` with inferred schema
```
**REASON:** Implicit contracts force guessing. Explicit ones make the skill callable without reading the body.

### Dimension 6: Failure Handling

**Signal:** Failure modes are placeholders; polling/retry/wait without timeout + backoff; external calls with no corresponding failure mode.

**CHANGE:** Name specific failures and their recoveries. Add explicit timeout + backoff to any polling/retry step.
**FROM:**
```markdown
## Failure modes
- If something goes wrong, handle it.
```
**TO:**
```markdown
## Failure modes
- `pandas.read_csv` raises `ParserError` → surface the line number and stop; do not write partial output.
- `s3:PutObject` returns 403 → surface the missing permission; do not retry.
- Schema-registry request times out → retry once with exponential backoff starting at 2s, up to 30s total; then surface `registry-unavailable`.
```
**REASON:** Generic recovery text is functionally silence. Specific failures with specific recoveries give the agent something to execute.

### Dimension 7: Safety Gating

**Signal:** Destructive step runs without an approval gate or dry-run default; vague approval language; `disable-model-invocation` missing on a destructive skill.

**CHANGE:** Add an explicit approval step before destructive operations. Make dry-run the default. Set `disable-model-invocation: true` on skills whose auto-invocation would be dangerous.
**FROM:**
```markdown
## Steps
1. Drop the staging schema and recreate it.
```
**TO:**
```markdown
---
...
disable-model-invocation: true
---

## Steps
1. Show a dry-run of the drop plan (tables, row counts, dependent views).
2. Ask the user to confirm. Require the exact string `drop staging`.
3. On confirmation, drop the staging schema and recreate it.
```
**REASON:** Agents execute what they read. Destructive operations need an explicit human gate.

### Dimension 8: Example Realism

**Signal:** Examples use `foo`/`bar`/`Widget` placeholders, generic inputs, or omit side effects.

**CHANGE:** Replace placeholders with realistic domain identifiers. Show inputs, outputs, and side effects.
**FROM:**
```markdown
## Examples
```
bash
./foo --input bar.csv --output baz.parquet
```
```
**TO:**
```markdown
## Examples
```
bash
./scripts/convert.sh \
  --input data/raw/orders-2026-04-22.csv \
  --output data/staging/orders-2026-04-22.parquet
# Writes ~2.3MB parquet (1.8M rows); prints "schema inferred: order_id INT64, order_date DATE, ..."
```
```
**REASON:** Domain-specific identifiers let the evaluator (human or Claude) recognize the context and apply the skill the way they would to new cases. Synthetic placeholders defeat the point of the example.

---

## Tier 3: Description Collisions

### Overlapping Triggers

**Signal:** Two skills' descriptions plausibly route the same request.

**CHANGE:** Narrow each description to name a distinguishing axis. If the axes cannot be cleanly separated, merge the skills.
**FROM:** two skills both described as "Use when the user asks to deploy"
**TO:**
- Skill A: "Use when the user asks to deploy to **staging**. Runs `terraform apply` against the staging workspace."
- Skill B: "Use when the user asks to deploy to **production**. Requires on-call approval; sets `disable-model-invocation: true`."
**REASON:** Ambiguous routing means Claude picks one arbitrarily. Narrowing the trigger surface makes routing deterministic. When the workflows are genuinely identical, one skill parameterized by environment is better than two.
