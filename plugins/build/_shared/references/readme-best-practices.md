---
name: README Best Practices
description: Authoring guide for a project's top-level README.md — what a good README does, the canonical anatomy, the patterns that work, and the safety posture. Referenced by build-readme and check-readme.
---

# README Best Practices

## What a Good README Does

A project's `README.md` is the file GitHub, npm, PyPI, and `ls` all
show first. Its reader is a stranger: somebody who arrived from a
search result, a dependency list, or a colleague's recommendation and
has roughly thirty seconds to decide whether this project is the one
they want. A good README answers, in that order: what the project is,
why it exists, and how to run it on a clean machine without asking
anybody for help.

The scope here is **the top-level `README.md` at a repository root** —
the one `git clone` lands a reader on. Sub-package READMEs inside a
monorepo directory serve a different audience (readers already in the
repo), docs-site landing pages are styled deliverables, and
organization profiles are marketing surfaces. All three earn their own
rubrics; this one does not cover them.

## Anatomy

````markdown
# project-name                                  ← single H1, first content line

One-sentence description of what this project is.

Two or three sentences stating the problem it solves and who it's for.

[![build](badge)](link)  [![license](badge)](link)   ← ~3-5 badges max, under title

## Prerequisites                                ← versioned, before install
- Node.js 18+
- PostgreSQL 14+

## Installation                                 ← copy-pasteable, clean-machine
```bash
git clone https://github.com/org/project
cd project
npm install
```

## Usage                                        ← minimal runnable example
```bash
npm start
```
Expected output:
```
Server listening on :3000
```

## Configuration                                ← env vars in a table or block
| Variable        | Default | Required | Description       |
|-----------------|---------|----------|-------------------|
| `DATABASE_URL`  | —       | yes      | Postgres DSN      |
| `LOG_LEVEL`     | `info`  | no       | `debug`/`info`/…  |

## Troubleshooting                              ← symptom → cause → fix

## Contributing                                 ← link to CONTRIBUTING.md
See [CONTRIBUTING.md](CONTRIBUTING.md).

## License
MIT — see [LICENSE](LICENSE).
````

Load-bearing pieces: a single H1 as the first content line, a one-sentence
description below it, an H2 section sequence in reader-intent order
(Prerequisites → Installation → Usage → Configuration → Troubleshooting
→ Contributing → License), fenced code blocks with language tags, a
named license with a link to the `LICENSE` file, and a contributing
pointer.

## Patterns That Work

**Single H1, first content line.** The title anchors the document for
readers, rendered TOCs, and tooling (GitHub's header slug generator,
SEO, screen readers). Frontmatter is allowed above it.

**One-sentence "what is this" on line 2.** It is the most-read line in
the document — GitHub's preview, npm's summary, and Google's snippet
all pull from the top. Save the problem statement for the next 2-3
sentences.

**Predictable H2 sequence in reader-intent order.** Prerequisites →
Installation → Usage → Configuration → Troubleshooting → Contributing
→ License matches the order readers need answers. Ordering is contested
for Quickstart-vs-Why (see Divergences below); the rest is not.

**Sequential heading hierarchy.** H1 → H2 → H3 with no skipped levels.
Accessibility tools and renderers rely on it; auto-generated TOCs
break when a file jumps H2 to H4.

**Versioned prerequisites before install commands.** "Node 18+",
"PostgreSQL 14+". Unmet prerequisites are the single largest cause of
failed first-runs — naming them before the install command saves the
reader a `command not found` round-trip.

**Copy-pasteable install and run commands.** Every command sits in a
fenced block tagged with the language (`bash`, `sh`, `console`,
`pwsh`). No `$` prompt prefixes unless showing output inline — prompts
break copy-paste. User-supplied values are marked placeholders
(`<YOUR_API_KEY>`) and defined once.

**Minimal runnable example in Quickstart.** Speed to first success
drives adoption. Show the command, show the expected output. Silence
after a command breeds doubt.

**Table or block for environment variables.** Name, type, default,
required. Variables described only in prose get missed.

**Named license + link to `LICENSE` file.** "MIT — see LICENSE." Legal
clarity needs both the human-readable name and a link to the canonical
text. An SPDX identifier in the README body is a nice-to-have.

**Contributing pointer.** A one-liner linking to `CONTRIBUTING.md`
beats silence. Even "PRs welcome — see CONTRIBUTING.md" clears the
bar.

**Relative links for repo-local files, absolute for consumer
surfaces.** Relative links survive forks and mirrors on GitHub;
absolute links survive package-mirror rendering on npm / PyPI.
Projects with package distribution should use absolute URLs for
references the package consumer will see (or configure their package
tooling to rewrite relative links).

**Descriptive alt text on every image and badge.** `![build status:
passing](badge.svg)` — not `![image]` or the filename. Screen readers
and failing-image fallbacks depend on it.

**Prose lines under 120 characters, code-block lines under 80.** 120
for prose keeps diffs readable; 80 for code prevents horizontal scroll
in terminals and soft-wrap breakage on copy-paste.

**Link to detailed docs rather than duplicating.** `/docs/`, a wiki, a
docs site — wherever the deep material lives. The README orients; the
docs explain.

**Keep the README in sync with the code.** Update the README in the
*same commit* as any behavior change it documents. Separate commits
mean the README loses the race.

## Anti-Patterns

- **No H1, multiple H1s, or H1 below a blockquote/image.** Renderers
  pick unpredictable anchors; the TOC breaks; tools that look for "the
  title" find the wrong node.
- **Wall-of-features before "what is this".** Feature bullets answer
  *how*; the one-sentence description answers *what*. Readers who do
  not know what the project is cannot tell whether the features matter.
- **Install commands that assume preexisting state.** "Run `make
  deploy`" with no prior "install Make", "export AWS creds", "bootstrap
  the cluster". A clean machine is the baseline.
- **Shell-prompt prefixes in code blocks.** `$ npm install` cannot be
  copy-pasted without editing. Prompts belong in prose, not in code
  blocks a reader will run.
- **Real secrets, tokens, hostnames, or IPs in examples.** Readers
  copy-paste. Reviewers miss it. Use reserved ranges (`example.com`,
  `127.0.0.1`, RFC 5737 `192.0.2.0/24`, `*.test`).
- **Piped-to-shell installers with no manual alternative.** `curl … |
  sh` is a posture the reader should opt into — provide a downloadable
  script and a warning alongside.
- **Destructive commands without a warning callout.** `rm -rf`, `dd`,
  `mkfs`, `DROP DATABASE`, `--force` without a bold-or-blockquote
  warning. Accidental destruction is unrecoverable.
- **Instructions to disable TLS verification, SELinux, firewalls.**
  Document the real fix or file the bug. Security-weakening guidance
  outlives the one issue that prompted it.
- **Emoji in headings.** Break grep, anchor slugs, screen readers, and
  some renderers. Put emoji in prose if you must, not in H2s.
- **Hand-maintained duplicates of `--help` output.** They drift from
  reality within one release. Regenerate or link to `tool --help`.
- **`TODO`, `FIXME`, `XXX` markers in the published README.** They
  signal incompleteness to every reader. Use issues for work items.
- **Badge overload.** More than ~5 badges under the title is
  scan-noise. Trim to the ones a reader would actually check.
- **Oversized images.** A 3 MB animated GIF of a CLI demo makes the
  repo page slow on mobile. SVG or asciicast is smaller, scalable, and
  text-selectable.
- **README past ~500 lines with no Table of Contents.** Auto-TOCs on
  GitHub help, but a reader on npm / PyPI or a fork sees no sidebar.
  Hand-maintain a TOC once the document earns one.
- **Duplicated docs inside the README.** When `ARCHITECTURE.md`,
  `CONTRIBUTING.md`, or `CHANGELOG.md` already say it, link and stop.
  Two copies drift.

## Divergences (project-contextual, not failures)

**Relative vs. absolute links for repo-local files.** Relative for
GitHub-first projects; absolute for projects whose READMEs render on
npm / PyPI / other package mirrors. Either is correct — the wrong
choice for the distribution channel is the defect. Audits flag this as
INFO, not WARN.

**Quickstart-first vs. Problem-first.** Some audiences want "how do I
try this in 30 seconds" (Quickstart first); others want "why should I
care" (Problem first). Recommended compromise: one-sentence
description → 2-3 sentences on the problem → Quickstart. Both
orderings are defensible once the top 30 seconds answers "what is this
and should I care."

**`sudo` in examples.** Avoid when a non-privileged alternative exists;
acceptable when the package manager legitimately requires it. Flag as
a soft warning, not a hard violation.

**Line-length limit for prose.** 80 / 100 / 120 all have proponents.
This rubric uses 120 for prose and 80 for code blocks — the split
reconciles the major sources. Projects that prefer tighter are free to
configure.

## Safety & Maintenance

**Hard safety rules** (audit flags as FAIL):

- No real secrets, tokens, credentials, private URLs, or internal
  hostnames in examples or fenced blocks.
- No `curl … | sh` / `iex (iwr …)` / `wget … | bash` installers
  without a documented manual alternative and an explicit warning.
- No destructive commands (`rm -rf`, `dd if=`, `mkfs`, `DROP`,
  `--force`) in examples without an adjacent warning callout.
- No instructions to disable TLS verification, SELinux, firewalls,
  or other security posture as a workaround.

**Maintenance posture:**

- Every command in the README should run successfully on a supported
  platform as of the last commit. Stale commands are the most common
  README defect — they erode reader trust fast and silently.
- Update the README in the same commit as any behavior change it
  documents. Two commits means doc-code drift; one commit makes drift
  structurally impossible for the duration of that change.
- Link to `CONTRIBUTING.md`, `ARCHITECTURE.md`, `CHANGELOG.md`,
  `SECURITY.md` rather than duplicating. Single source of truth.
- Do not hand-maintain duplicates of `--help` output or pinned
  version numbers that live in manifests. Regenerate or link.
- Provide a private security-disclosure channel (`SECURITY.md` or a
  contact email). Responsible disclosure protects users and the
  project's reputation.

---

**Diagnostic when a README underperforms.** First check the top 30
seconds: H1, one-sentence description, problem statement. If a
stranger cannot answer "what is this" after reading those three lines,
the rest of the document is wasted. Then check Prerequisites +
Installation on a clean machine — not your laptop. Then check
copy-paste: every command block, no prompts, no smart quotes, tagged
language. Most README pathologies live in one of those three places.
