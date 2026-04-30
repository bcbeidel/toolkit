---
name: build-readme
description: >
  Scaffolds a project's top-level README.md — the `README.md` at a
  repository root that orients a first-time reader in the top 30
  seconds. Produces a conditionalized template with a single H1,
  one-sentence description, problem statement, badges block, H2
  section sequence (Prerequisites → Installation → Usage →
  Configuration → Troubleshooting → Contributing → License), fenced
  code blocks with language tags, and placeholder discipline. Use
  when the user wants to "create a README", "scaffold a README",
  "write the project README", "new README for this repo", or
  "bootstrap README.md". Not for sub-package READMEs inside a
  monorepo, docs-site landing pages, or GitHub org-profile READMEs
  — those have different audiences and out of scope.
argument-hint: "[project-name]"
user-invocable: true
references:
  - ../../_shared/references/readme-best-practices.md
  - ../../_shared/references/primitive-routing.md
license: MIT
---

# Build README

Scaffold a project's top-level `README.md`: the first file a stranger
sees after `git clone`, a dependency listing, or a package-registry
page. The authoring rubric — what a good README does, the anatomy
template, the patterns that work — lives in
[readme-best-practices.md](../../_shared/references/readme-best-practices.md).
This skill is the workflow; the principles doc is the rubric.

**Scope is top-level only.** Sub-package READMEs inside a monorepo
directory, documentation-site landing pages, and GitHub organization
profile READMEs are out of scope and refused at the Scope Gate. They
serve different audiences and deserve different rubrics.

**Workflow sequence:** 1. Route → 2. Scope Gate → 3. Elicit →
4. Draft → 5. Safety Check → 6. Review Gate → 7. Save → 8. Test

## 1. Route

Confirm a top-level `README.md` is the right artifact before asking
scaffold-specific questions.

**Wrong artifact:**

- **Package/module docstring, not a README** → author in the language's
  native docstring format; not this skill.
- **A Claude Code skill or rule doc** → `/build:build-skill` or
  `/build:build-rule`.
- **A changelog, contributing guide, or architecture doc** → those are
  sibling markdown files (`CHANGELOG.md`, `CONTRIBUTING.md`,
  `ARCHITECTURE.md`), not the README — the README *links to* them.

**Wrong scope — recommend an alternative:**

- **Sub-package README** (`packages/foo/README.md` in a monorepo) —
  the audience is a reader already in the repo, not a stranger; the
  rubric differs. Hand-write or propose a dedicated
  `/build:build-subpackage-readme` pair when demand justifies it.
- **Docs-site landing page** — styled deliverable; the toolchain
  (Docusaurus, mkdocs, etc.) drives the shape.
- **GitHub org-profile README** (`.github/profile/README.md`) —
  marketing surface, not a project entry point.

**Right artifact and right scope** → proceed to Scope Gate.

## 2. Scope Gate

Refuse to scaffold when any of these signal:

1. **An existing `README.md` is already present at the target path
   and non-trivial** (more than ~20 lines of real content, not a
   stub). Scaffolding over it would discard work. Offer instead to
   run `/build:check-readme <path>` and iterate from findings.
2. **No project context available** — the target directory has no
   discernible project (no `package.json`, `pyproject.toml`,
   `Cargo.toml`, `go.mod`, `Gemfile`, `pom.xml`, or similar). A
   README for an empty directory is a template, not a README; ask
   the user to confirm they want a generic skeleton or to initialize
   the project first.
3. **Target is not a repository root** — the path given is several
   directories deep and is clearly a sub-package. Confirm scope (see
   Route §1); refuse sub-package READMEs.

If any signal fires, state the signal, name the recommended
alternative, and stop. Do not proceed to Elicit.

## 3. Elicit

If `$ARGUMENTS` is non-empty, parse it as `[project-name]` and
pre-fill question 1. Otherwise ask, one question at a time:

**1. Project name** — the single H1. Typically the package name or
repo name. Avoid marketing phrases; the H1 is for humans and tools.

**2. One-sentence description** — what the project *is* (not what it
does). "A Python library for X", "A CLI tool that X", "A service
that X". This is the most-read line in the document.

**3. Problem statement** — 2-3 sentences: what problem does this
solve, who is it for. Features answer *how*; the problem statement
answers *why I should care*.

**4. Language / runtime + minimum version** — Node 18+, Python 3.10+,
Go 1.22+, etc. Populates Prerequisites.

**5. Install command(s)** — the command a reader would run on a
clean machine. Include language identifier for the fenced block
(`bash`, `sh`, `pwsh`). Multi-platform? List each with a labeled
block.

**6. Quickstart command + expected output** — the minimal runnable
example. If the project is a library, show the smallest import + call
that produces visible output.

**7. Configuration surface** — environment variables, config files,
or CLI flags the user must set before running. Omit if none (the
scaffold drops the Configuration H2).

**8. License** — SPDX identifier (MIT, Apache-2.0, GPL-3.0, etc.).
Required; the scaffold refuses to omit the License section.

**9. Distribution channel** — GitHub-only, or does this also ship to
npm / PyPI / crates.io / similar? Determines relative-vs-absolute
link default (relative for GitHub-only; absolute for package
mirrors).

**10. Badges to include** — CI status, package version, license,
coverage. Cap at 5; more is scan-noise. Ask for URLs or accept
"standard set for this stack" and propose defaults.

**11. Save path** — default is `README.md` at the current working
directory. Confirm.

## 4. Draft

Produce a single conditionalized template. Sections marked *(if X)*
are omitted when intake rules them out.

````markdown
# <project-name>                                        ← Intake #1

<one-sentence description>                              ← Intake #2

<2-3 sentence problem statement>                        ← Intake #3

<badges block — under title, ~3-5 max>                  ← Intake #10 (if any)

## Prerequisites

- <language/runtime> <min-version>                      ← Intake #4
- <other prerequisites if named>

## Installation

```<lang>
<install command>                                        ← Intake #5
```

<repeat block per platform if multi-platform>

## Usage

```<lang>
<quickstart command>                                     ← Intake #6
```

Expected output:
```
<expected output>
```

## Configuration                                         ← (if Intake #7 non-empty)

| Variable | Default | Required | Description |
|----------|---------|----------|-------------|
| `<VAR>`  | <def>   | yes/no   | <desc>      |

## Troubleshooting                                       ← placeholder; one FAQ entry

**Problem:** <common symptom>
**Cause:** <root cause>
**Fix:** <concrete remediation>

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

<SPDX-id> — see [LICENSE](LICENSE).                      ← Intake #8
````

**Link style default:**

- *(if Intake #9 = GitHub-only)* Use relative links (`CONTRIBUTING.md`,
  `LICENSE`).
- *(if Intake #9 = package mirror)* Use absolute URLs
  (`https://github.com/<owner>/<repo>/blob/main/CONTRIBUTING.md`)
  and prompt for the repo URL.

*(if Intake #7 = none)* Omit the entire Configuration H2.

Present the draft plus a suggested `git add README.md` invocation
line to the user before any safety checks.

## 5. Safety Check

Review the draft against the rubric in
[readme-best-practices.md](../../_shared/references/readme-best-practices.md)
before presenting. Group the checks:

**Structure.** Single H1 on first content line. One-sentence
description on the next line. 2-3 sentence problem statement
follows. H2 sequence in reader-intent order. Heading levels
sequential (no H2 → H4 skips).

**Commands & code blocks.** Every command block carries a language
tag. No shell-prompt prefixes (`$`, `>`, `#`). Placeholders marked
with `<...>`. Code-block lines ≤80 characters.

**Safety.** No real secrets, tokens, credentials, or hostnames in
the draft. No `curl … | sh` installers without a documented manual
alternative. No destructive commands without a warning callout.
Example domains/IPs are RFC-reserved only (`example.com`, `*.test`,
`127.0.0.1`, RFC 5737 ranges).

**Completeness.** License section present with SPDX identifier and
link. Contributing section links to `CONTRIBUTING.md`. No `TODO` /
`FIXME` / `XXX` markers in the draft.

**Style.** Imperative mood for instructions ("Run `npm install`",
not "You should run…"). No emoji in headings. Prose lines ≤120
characters.

If any check fails, revise the draft before presenting. The Review
Gate is for user approval, not correctness recovery.

## 6. Review Gate

Present the draft (full README content + suggested `git add`
invocation) and wait for explicit user approval before writing any
file to disk. Write only after this gate passes.

If the user requests changes, revise and re-present. Continue until
the user explicitly approves or cancels. Proceed to Save only on
explicit approval.

## 7. Save

Write the approved README to the path elicited in Step 3.11 (default
`README.md` at the current working directory).

Do **not** `chmod +x` — markdown is data, not executable. Do not
create sibling files (`LICENSE`, `CONTRIBUTING.md`); the README
references them, but creating them is out of scope. Prompt the user
to add those files separately if they are not yet present.

## 8. Test

Offer the audit:

> "Run `/build:check-readme <path>` to audit the scaffolded README
> against structure, safety, completeness, and judgment dimensions?"

The audit is the canonical follow-on; running it once after scaffold
catches anything the Safety Check missed.

## Anti-Pattern Guards

1. **Skipping the Scope Gate** — always probe the three signals
   before Elicit. Scaffolding over an existing non-trivial README
   destroys work.
2. **Omitting the License section** — even if the user does not yet
   have a LICENSE file, the section is required. The scaffold links
   to a LICENSE file that may not exist yet; that is the prompt to
   create it, not an excuse to skip the section.
3. **Scaffolding marketing language** — the H1 is the project name,
   not a tagline. The one-sentence description is what it *is*, not
   what it *promises*. Salesy language belongs on a landing page.
4. **Forgetting expected output in Quickstart** — the command alone
   is half the contract. Silence after a command breeds doubt.
5. **Shell prompts in code blocks** — `$ npm install` cannot be
   copy-pasted. Drop the prompt.
6. **Real secrets in examples** — even in a draft. Readers copy-paste
   before reviewers read.
7. **Skipping the Review Gate** — write to disk only after explicit
   user approval. Present the whole draft first.

## Key Instructions

- Refuse cleanly on Scope Gate signals. Sub-package READMEs and
  existing non-trivial READMEs are hard refuses with alternatives
  named.
- Write files to disk only after the Review Gate passes.
- The License section is always scaffolded — it is not intake-gated.
  An SPDX identifier is elicited explicitly.
- The Configuration H2 *is* intake-gated — omit when no config
  surface exists. Empty sections are scan-noise.
- Code-block language tags are mandatory on every fenced block.
  Default to the target shell / language; never empty info-strings.
- Use relative links by default; switch to absolute URLs only when
  Intake #9 flags package-mirror distribution.
- Won't scaffold sub-package READMEs — out of scope; different
  audience, different rubric.
- Won't scaffold over a non-trivial existing README — offer
  `/build:check-readme` instead.
- Won't inline real secrets, hostnames, or credentials in examples
  — use reserved ranges.
- Recovery if a README is scaffolded in error: `rm <path>` removes
  it cleanly. The scaffold is self-contained (no sibling file
  writes, no registration), so removal leaves no dangling state.

## Handoff

**Receives:** user intent for a top-level `README.md` (project name,
one-sentence description, problem statement, language/runtime,
install / quickstart commands, configuration surface, license,
distribution channel, badges, save path).

**Produces:** a single `README.md` at the user-supplied path (default
repo root) plus a suggested `git add` invocation line.

**Chainable to:** `/build:check-readme` (audit the scaffolded README
against structure, safety, completeness, and the seven judgment
dimensions).
