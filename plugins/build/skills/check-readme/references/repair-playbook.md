---
name: Repair Playbook — README
description: One repair recipe per Tier-1 finding type plus one per Tier-2 dimension plus one per Tier-3 collision. Each recipe is Signal → CHANGE → FROM → TO → REASON. Applied during the check-readme opt-in repair loop with per-finding confirmation.
---

# Repair Playbook

Per-finding repair recipes for check-readme. Every Tier-1 finding
type and every Tier-2 dimension has a recipe here. Apply one at a
time, with explicit user confirmation, re-running the producing
check after each fix.

**HINT-severity findings are feed-forward context, not repair
targets.** They inform the Tier-2 prompt; they do not enter the
repair queue.

## Format

- **Signal** — the finding string or dimension name
- **CHANGE** — what to modify, in one sentence
- **FROM** — concrete non-compliant example
- **TO** — compliant replacement
- **REASON** — why, tied to source principle

---

## Tier-1 — `check_secrets.py`

### Signal: `secret — API key / token / credential detected`

**CHANGE** Remove the secret; replace with a clearly-marked placeholder
and reference an env var in prose.

**FROM**
```bash
export API_KEY="sk-proj-abc123def456"
```
**TO**
```bash
export API_KEY="<YOUR_OPENAI_API_KEY>"   # set to your OpenAI key
```
**REASON** Real credentials in committed source leak via git history,
archives, and forks. Placeholder + env-var convention is the minimum
safe pattern.

---

## Tier-1 — `check_structure.py`

### Signal: `h1-present — no H1, or multiple H1s, or H1 not on first content line`

**CHANGE** Ensure exactly one `# Title` line as the first non-frontmatter
content of the file; demote or remove any other H1.

**FROM**
```markdown
## Project
This is a thing.

# My Project
```
**TO**
```markdown
# My Project
This is a thing.
```
**REASON** The single H1 anchors the document for readers, GitHub's
preview, and TOC tooling.

### Signal: `heading-hierarchy — heading level skipped (MD001)`

**CHANGE** Promote the skipped heading to match the sequence, or insert
the missing level.

**FROM** an `H2` followed directly by an `H4` (e.g., `## Installation`
then `#### Linux`).
**TO** an `H2` followed by an `H3` (e.g., `## Installation` then
`### Linux`), or insert an intermediate `H3` before the `H4`.

**REASON** Accessibility tools and auto-TOCs rely on sequential levels.

### Signal: `section-coverage — required section missing`

**CHANGE** Add the missing section (Installation, Usage, or License) in
reader-intent order.

**FROM** No `## License` heading anywhere in the file.
**TO**
```markdown
## License
MIT — see [LICENSE](LICENSE).
```
**REASON** Installation, Usage, and License are the minimum sections a
project README owes its readers.

### Signal: `section-order — canonical H2 sequence violated`

**CHANGE** Reorder H2 sections to: Prerequisites → Installation → Usage
→ Configuration → Troubleshooting → Contributing → License.

**FROM** `## License` before `## Installation`.
**TO** License last.
**REASON** The order matches the path readers actually take through the
document.

### Signal: `toc-threshold — no TOC in document over 400 lines`

**CHANGE** Add a hand-maintained Table of Contents under the opening
paragraph.

**TO**
```markdown
## Table of Contents
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
```
**REASON** Long READMEs on npm / PyPI / fork views have no auto-TOC
sidebar; a hand TOC is the only navigation.

### Signal: `size — README exceeds 500 lines`

**CHANGE** Move detailed sections into `/docs/` and link in. Keep the
README as an orientation layer.

**FROM** 800-line README with full API reference inline.
**TO** README links to `docs/api.md`; the deep content moves.
**REASON** The README orients a stranger; docs explain the domain. Two
roles, two files.

### Signal: `prose-line-length — source line over 120 characters`

**CHANGE** Hard-wrap prose to 120 columns; do not touch fenced code
blocks, tables, or bare-URL lines.

**REASON** Reviewers read diffs, not rendered HTML; long lines
produce bad diffs.

---

## Tier-1 — `check_codeblocks.py`

### Signal: `fence-language — fenced code block has no language tag (MD040)`

**CHANGE** Add the appropriate language identifier after the opening
fence.

**FROM**
````markdown
```
npm install
```
````
**TO**
````markdown
```bash
npm install
```
````
**REASON** Syntax highlighting, copy buttons, and tool extraction all
key off the language tag.

### Signal: `shell-prompt — shell block contains prompt prefix`

**CHANGE** Strip `$`, `>`, or `#` prefixes from command lines. If output
needs showing, split into an input block and a separate output block.

**FROM**
```bash
$ npm install
$ npm start
```
**TO**
```bash
npm install
npm start
```
**REASON** Prompt characters break copy-paste.

### Signal: `smart-quotes — smart quote or em-dash inside code block`

**CHANGE** Replace curly quotes, em-dashes, en-dashes, and ellipsis with
ASCII equivalents inside the code block.

**FROM** `curl "https://api.example.com"` (curly quotes)
**TO** `curl "https://api.example.com"` (ASCII quotes)
**REASON** Shells interpret ASCII quotes; smart quotes fail
unpredictably at runtime.

### Signal: `code-line-length — fenced code line over 80 characters`

**CHANGE** Break the command with line continuations (`\`) or pull flag
values into env vars set earlier.

**FROM** One 180-char `curl` invocation.
**TO** `curl ... \` continuation or a two-step `API=... ; curl "$API/..."`.
**REASON** Terminal soft-wrap inside code blocks breaks copy-paste.

---

## Tier-1 — `check_links.py`

### Signal: `broken-relative — relative link points to a missing file`

**CHANGE** Create the target file, correct the path, or remove the link.

**FROM** `[contributing](CONTRIBUTING.md)` with no `CONTRIBUTING.md`.
**TO** Either add the file or drop the link.
**REASON** Broken links erode trust and signal neglect.

### Signal: `broken-anchor — fragment link does not match any heading slug`

**CHANGE** Update the fragment to match the target heading's rendered
slug.

**FROM** `[see below](#setup-steps)` when the heading is `## Setup`.
**TO** `[see below](#setup)`.
**REASON** Anchor slugs are derived from heading text; drift between
them silently.

### Signal: `broken-external — external URL returns 4xx / 5xx`

**CHANGE** Update the URL, swap to a canonical source, or remove if the
resource is gone.

**REASON** External URL rot is common; stale links point readers at
error pages.

---

## Tier-1 — `check_images.py`

### Signal: `alt-text — image or badge has empty or placeholder alt text`

**CHANGE** Replace empty / placeholder alt with descriptive text naming
what the image conveys.

**FROM** `![image](screenshot.png)`
**TO** `![dashboard screenshot showing three active workers](screenshot.png)`
**REASON** Screen readers and failing-image fallbacks depend on alt
text; `image` and the filename are worse than nothing.

### Signal: `image-size — embedded image over 500 KB or total over 2 MB`

**CHANGE** Convert to SVG or asciicast, recompress as WebP, or move the
demo to an external host.

**REASON** Repo page load matters on mobile and low-bandwidth
connections.

### Signal: `badge-overload — more than 5 badges in the prelude`

**CHANGE** Trim to the badges a reader would actually check: CI,
version, license, coverage. Move the rest to a dedicated section or
drop.

**REASON** More than ~5 badges is scan-noise; readers stop reading
them.

---

## Tier-1 — `check_safety.py`

### Signal: `destructive — rm -rf / dd / DROP / --force in a block without a warning`

**CHANGE** Add a blockquote or bold warning immediately before the
block; name the consequence.

**FROM**
````markdown
```bash
rm -rf /var/lib/project
```
````
**TO**
````markdown
> ⚠ **Warning:** this deletes all local project data.
```bash
rm -rf /var/lib/project
```
````
**REASON** Accidental destruction is unrecoverable; warnings must be
visually prominent.

### Signal: `pipe-to-shell — curl | sh pattern without a manual alternative`

**CHANGE** Add a manual alternative in the same section (download +
inspect + run) and an explicit warning on the piped form.

**FROM**
```bash
curl https://install.example.com | sh
```
**TO**
```bash
# Recommended: inspect before running
curl -O https://install.example.com/install.sh
less install.sh
bash install.sh

# Or, if you trust the source:
curl https://install.example.com | sh
```
**REASON** Pipe-to-shell is a security posture the reader should opt
into, not be pushed into.

### Signal: `tls-disable — instructions to disable TLS / SELinux / firewalls`

**CHANGE** Remove the workaround; document the real fix or file an
issue. If unavoidable for now, add a blockquote explaining the scope
and the tracking issue.

**REASON** Security-weakening guidance outlives the problem that
prompted it; it spreads.

### Signal: `non-reserved-hosts — real hostname or public IP in example`

**CHANGE** Swap for RFC-reserved: `example.com`, `*.test`, `*.local`,
`127.0.0.1`, `192.0.2.0/24` (RFC 5737).

**FROM** `curl https://api.acme.com/v1`
**TO** `curl https://api.example.com/v1`
**REASON** Real hostnames and IPs invite accidental traffic to
production systems the reader does not own.

### Signal: `emoji-headings — emoji code point in heading text`

**CHANGE** Remove the emoji from the heading; if you want visual
marker, use it in body prose, not heading text.

**FROM** `## 🚀 Getting Started`
**TO** `## Getting Started`
**REASON** Emoji break grep, anchor slug generation, and screen
readers.

---

## Tier-1 — `check_completeness.py`

### Signal: `license-file — no LICENSE file at repository root`

**CHANGE** Add a `LICENSE` file with the full license text (use the
chooser at [choosealicense.com](https://choosealicense.com) if
unsure).

**REASON** Without a license file, the project is "all rights
reserved" by default — unusable by anyone who reads the README.

### Signal: `license-link — README has no License section or no link to LICENSE`

**CHANGE** Add a `## License` H2 section with the SPDX identifier and
a link to the LICENSE file.

**TO**
```markdown
## License
MIT — see [LICENSE](LICENSE).
```
**REASON** Readers need both the human-readable name and the
canonical text; the section is the pointer.

### Signal: `contributing-link — no Contributing section or link to CONTRIBUTING.md`

**CHANGE** Add a one-line Contributing section linking to
`CONTRIBUTING.md` (create the file separately if absent).

**TO**
```markdown
## Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md).
```
**REASON** Silence signals "not accepting contributions"; even a
one-liner beats silence.

### Signal: `todo-markers — TODO / FIXME / XXX in published README`

**CHANGE** Convert to a tracked issue; remove from the README.

**FROM** `TODO: add Windows instructions`
**TO** Open issue `#N`, remove line from README. Optionally link the
issue in a Roadmap section.
**REASON** Markers signal incompleteness to every reader; issues are
where work tracks.

### Signal: `readme-gitignored — README.md listed in .gitignore`

**CHANGE** Remove the `README.md` entry from `.gitignore`; commit the
README.

**REASON** A README not in version control is not a README; it is a
local note.

---

## Tier-2 — Judgment Dimension Recipes

### D1 Opening Clarity

**Signal** Stranger cannot answer "what is this and should I care" in
the top 30 seconds.

**CHANGE** Rewrite the first three content lines: H1 (project name),
one-sentence "what is this", 2-3 sentences stating the problem.

**FROM**
```markdown
# Lightning Fast Framework
🚀 Features:
- Fast
- Modular
- Cloud-native
```
**TO**
```markdown
# LFF
A Python web framework focused on low-latency request handling.

Built for teams running latency-sensitive APIs where request p99 matters more
than developer ergonomics. LFF trades framework richness for predictable
performance under load.
```
**REASON** The top 30 seconds are the only bytes most readers see.

### D2 Installation Correctness

**Signal** Install commands would fail on a clean machine.

**CHANGE** Add missing prerequisites with versions; list hidden setup
steps; test on a fresh VM or container.

**REASON** First-run failure is the largest source of abandoned
adoption.

### D3 Quickstart Effectiveness

**Signal** Quickstart is missing expected output or is not minimal.

**CHANGE** Trim the example to one command or call that demonstrates
the core value; add an expected-output block beneath.

**TO**
````markdown
## Quickstart
```bash
lff serve --port 3000
```
Expected output:
```
LFF listening on :3000 (pid 1234)
```
````
**REASON** Silence after a command breeds doubt; visible output
confirms success.

### D4 Placeholder Discipline

**Signal** Placeholders undefined, inconsistent, or mixed with real
values.

**CHANGE** Define each placeholder once, typically in Configuration;
use the same token everywhere; swap any real-looking example values
for `<...>`.

**REASON** Reader copies. Reader pastes. Reader hits prod.

### D5 Warning Prominence

**Signal** Warnings on destructive / security-sensitive ops are prose,
not callouts.

**CHANGE** Promote inline warnings to blockquotes or bold callouts
immediately adjacent to the block.

**FROM** "Note: this will delete everything."
**TO** `> ⚠ **Warning:** this deletes everything in /var/project.`
**REASON** Readers scan; warnings must catch a scanning eye, not a
careful read.

### D6 Maintenance Posture

**Signal** Staleness indicators (old version numbers, dead roadmap,
pasted `--help`).

**CHANGE** Update version references, replace pasted `--help` with a
link to `tool --help` or a generated docs page, prune roadmap items
completed or abandoned.

**REASON** Stale docs cost reader trust; one stale line taints nearby
correct ones.

### D7 Style & Voice

**Signal** Instructions in indicative / passive voice; jargon
undefined; emoji in headings.

**CHANGE** Convert to imperative ("Run X", not "You should run X");
define jargon on first use; remove heading emoji.

**FROM** "You might want to consider running `npm install` to get started."
**TO** "Run `npm install`."
**REASON** Imperative + second person is the clearest instruction
form; hedging reads as uncertainty.

---

## Tier-3 — Cross-Entity Collision

### Signal: `collision — near-identical boilerplate across READMEs in a scope`

**CHANGE** Hoist the shared content to a common location — an org-level
`.github/profile/README.md`, a shared docs site, or a snippet file —
and link from the per-project READMEs.

**REASON** Duplication silently diverges; a single source of truth is
the only durable fix.

## Notes

- **Per-finding confirmation.** Apply one fix, re-run the producing
  script, confirm green, then move to the next. Bulk application
  overwrites mid-refactor intent.
- **Tier-2 fixes are structural.** D1 / D3 / D5 / D7 rewrites often
  cascade into surrounding sections; show the diff broadly and let
  the user confirm before writing.
- **Tier-1 FAIL exclusions.** If a file was excluded from Tier-2 by a
  Tier-1 FAIL (secrets, missing H1, unguarded destructive command,
  pipe-to-shell without alternative, TLS-disable, non-reserved
  hosts/IPs, missing LICENSE), re-run `/build:check-readme` after the
  Tier-1 fix to unlock the judgment dimensions.
