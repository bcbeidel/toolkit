---
name: Audit Dimensions — README
description: The complete check inventory for check-readme — Tier-1 deterministic check table (~28 checks across 7 scripts) and Tier-2 judgment dimension specifications (7 dimensions, each citing its source principle). Referenced by the check-readme workflow.
---

# Audit Dimensions

The check-readme audit runs in three tiers. This document is the
inventory: every deterministic check Tier-1 emits, every judgment
dimension Tier-2 evaluates. Every dimension cites the source principle
it audits from
[readme-best-practices.md](../../../_shared/references/readme-best-practices.md).

## Tier-1 — Deterministic Checks

Seven scripts, ~28 atomic checks. Each script emits findings in the
fixed lint format. Exit codes: `0` clean / WARN / INFO / HINT-only;
`1` on FAIL; `64` arg error; `69` missing required dependency
(`markdownlint`, `lychee`, `gitleaks` are optional and degrade
gracefully).

| Script | Check ID | What | Severity | Source principle |
|---|---|---|---|---|
| `check_secrets.py` | `secret` | API keys, tokens, private URLs, credentials via regex pattern list; optional `gitleaks`/`detect-secrets` wrapper | FAIL | Hard safety rules |
| `check_structure.py` | `h1-present` | Exactly one H1 heading, on the first non-frontmatter content line | FAIL | Single H1, first content line |
| `check_structure.py` | `heading-hierarchy` | Heading levels increment by at most 1; no H2→H4 skips (MD001) | WARN | Sequential heading hierarchy |
| `check_structure.py` | `section-coverage` | Minimum sections present: Installation, Usage (or Quickstart), License | WARN | Predictable H2 sequence in reader-intent order |
| `check_structure.py` | `section-order` | Canonical section sequence respected when sections are present (Prerequisites → Installation → Usage → Configuration → Troubleshooting → Contributing → License) | WARN | Predictable H2 sequence in reader-intent order |
| `check_structure.py` | `toc-threshold` | Table of Contents heading present when rendered document exceeds 400 lines | WARN | Hand-maintain a TOC once the document earns one |
| `check_structure.py` | `size` | Document length ≤ 500 lines (above which detailed docs belong elsewhere) | WARN | Link to detailed docs rather than duplicating |
| `check_structure.py` | `prose-line-length` | Source lines ≤ 120 characters (excluding fenced code blocks, tables, bare-URL lines) | WARN | Prose lines under 120 characters |
| `check_codeblocks.py` | `fence-language` | Every fenced code block has a non-empty language info-string (MD040) | WARN | Copy-pasteable install and run commands |
| `check_codeblocks.py` | `shell-prompt` | No `$`, `>`, or `#` prompt prefix at the start of lines in `bash`/`sh`/`console` blocks | WARN | No `$` prompt prefixes unless showing output inline |
| `check_codeblocks.py` | `smart-quotes` | No smart quotes / em-dash / en-dash / ellipsis inside fenced code blocks | WARN | Code-block lines ASCII-safe |
| `check_codeblocks.py` | `code-line-length` | Fenced code block lines ≤ 80 characters | WARN | Code-block lines under 80 |
| `check_links.py` | `broken-relative` | Every relative link resolves to an existing file on disk | FAIL | Ensure every link resolves |
| `check_links.py` | `broken-anchor` | Every fragment link (`#section`) matches an existing heading slug | WARN | Ensure every link resolves |
| `check_links.py` | `broken-external` | External URLs return 2xx/3xx (when `lychee`/`markdown-link-check` available) | WARN | Ensure every link resolves |
| `check_images.py` | `alt-text` | Every image and badge has non-empty, non-placeholder alt text (MD045) | WARN | Descriptive alt text on every image and badge |
| `check_images.py` | `image-size` | Embedded images ≤ 500 KB each; total README assets ≤ 2 MB | WARN | Oversized images |
| `check_images.py` | `badge-overload` | ≤ 5 badge-like image nodes in the prelude (between H1 and first prose block) | WARN | Badge overload |
| `check_safety.py` | `destructive` | Destructive commands (`rm -rf`, `dd if=`, `mkfs`, `DROP DATABASE`, `--force`) in fenced blocks flagged unless an adjacent warning callout (blockquote or bold) is present | FAIL | Destructive commands without warning |
| `check_safety.py` | `pipe-to-shell` | `curl ... \| sh`, `wget ... \| bash`, `iex (iwr ...)` flagged unless a manual alternative is documented within the same section | FAIL | Piped-to-shell installers without a manual alternative |
| `check_safety.py` | `tls-disable` | Instructions to disable TLS verification, SELinux, or firewalls flagged | FAIL | Instructions to disable TLS verification / SELinux / firewalls |
| `check_safety.py` | `non-reserved-hosts` | Hostnames outside reserved TLDs / IPs outside RFC 5737 ranges in examples | FAIL | Use reserved example domains |
| `check_safety.py` | `emoji-headings` | Emoji code points in heading text (Unicode `Emoji_Presentation` property) | WARN | Emoji in headings |
| `check_completeness.py` | `license-file` | A `LICENSE` (or `LICENSE.md`/`LICENSE.txt`) file exists in the repository root | FAIL | Named license + link to LICENSE file |
| `check_completeness.py` | `license-link` | README contains a heading matching `/license/i` and a link to the LICENSE file | WARN | Named license + link to LICENSE file |
| `check_completeness.py` | `contributing-link` | README contains a Contributing heading or a link to `CONTRIBUTING.md` | WARN | Contributing pointer |
| `check_completeness.py` | `todo-markers` | No `TODO`, `FIXME`, or `XXX` markers in the published README | WARN | `TODO`, `FIXME`, `XXX` markers in the published README |
| `check_completeness.py` | `readme-gitignored` | `README.md` is not listed in `.gitignore` | WARN | README should be version-controlled |

**FAIL exclusions from Tier-2.** Any `secret`, `h1-present`,
`destructive`, `pipe-to-shell`, `tls-disable`, `non-reserved-hosts`,
or `license-file` finding excludes the file from Tier-2. Broken
relative links (`broken-relative` FAIL) leave a parseable document
that judgment can still evaluate productively and are not
exclusion-triggers.

**Missing-tool degradation.** When `markdownlint`, `lychee`,
`markdown-link-check`, `gitleaks`, or `detect-secrets` is absent, the
wrapping script emits an INFO finding (`tool-missing`) and exits 0.
Other scripts continue running. The Missing Tools INFO is the user's
signal that Tier-1 coverage is reduced — surfacing it is the contract.

## Tier-2 — Judgment Dimensions

One LLM call per file. All seven dimensions run every time; a
dimension that doesn't apply returns PASS silently. Findings carry
WARN severity unless a dimension explicitly marks otherwise —
judgment-level drift is coaching, not blocking.

### D1 Opening Clarity

**Source principles:** *One-sentence "what is this" on line 2*;
*Wall-of-features before "what is this"* (anti-pattern).

**Judges:** Does the H1 name the project? Does the next line or
paragraph answer "what is this" in one sentence? Do the following 2-3
sentences state the problem it solves and who it is for? Could a
stranger — somebody arriving from a dependency list or a search
result — answer "what is this and should I care" after reading only
the top 30 seconds of the document?

**PASS conditions:** H1 is the project name, not marketing copy. A
one-sentence "what it is" statement sits immediately below. Problem
statement follows within 2-3 sentences. The top of the document does
not open with a feature list or a screenshot wall.

**Common fail signal:** H1 is a tagline ("Ship faster than light");
description leads with "Features:"; first content block is a
screenshot; opening paragraph explains how the code works without
saying what it is.

### D2 Installation Correctness

**Source principles:** *Versioned prerequisites before install
commands*; *Copy-pasteable install and run commands*; *Install
commands that assume preexisting state* (anti-pattern).

**Judges:** Does the Prerequisites list name every runtime / tool /
external service the reader needs, with minimum versions? Would the
install commands actually succeed on a clean machine that has only
the prerequisites? If the project supports multiple platforms, are
all of them covered with labeled command blocks? Are destructive
install steps (database migrations, filesystem modifications) noted?

**PASS conditions:** Prerequisites explicitly versioned. Install
commands run top-to-bottom on a freshly provisioned machine.
Multi-platform claims are matched by per-platform blocks. Preexisting
state is never assumed silently.

**Common fail signal:** "Just run `make install`" with no Make
prerequisite listed; Node install command with no Node version;
macOS-only `brew` install in a project that claims Linux support.

### D3 Quickstart Effectiveness

**Source principles:** *Minimal runnable example in Quickstart*;
*Forgetting expected output in Quickstart* (anti-pattern).

**Judges:** Is the Quickstart example genuinely minimal (one command
or one function call)? Does it produce visible output a reader can
compare against? Is the expected output shown? Does "minimal" here
mean "smallest thing that demonstrates value", not "smallest thing
that runs without erroring"?

**PASS conditions:** Quickstart has one primary command or call.
Expected output block follows and matches what a reader would see.
The example demonstrates the project's core value, not a tangent.

**Common fail signal:** Quickstart is a feature tour covering three
use cases; no expected output shown; the "minimal" example requires
fifteen lines of setup code; the example's output is mocked or
aspirational.

### D4 Placeholder Discipline

**Source principles:** *User-supplied values are marked placeholders*;
*Real secrets, tokens, hostnames, or IPs in examples* (anti-pattern).

**Judges:** Are user-supplied values marked as placeholders
(`<YOUR_API_KEY>`, `<PROJECT_ID>`)? Is each placeholder defined
exactly once — in a Configuration section or adjacent prose — and
used consistently? Are placeholder tokens visually distinct from
real values? Conversely: any real values that look like placeholders
but are actually production constants?

**PASS conditions:** Every user-supplied value is bracketed. Each
placeholder is defined once and used consistently. No production
hostnames, tokens, or IPs appear in example blocks.

**Common fail signal:** `export API_KEY=sk-proj-abc123` (real-looking
secret); `<YOUR_API_KEY>` used in three blocks with no definition;
`<project>` used in some blocks and `my-project` in others; a URL
like `https://api.acme-internal.corp.example` that looks internal
but is passed off as documentation.

### D5 Warning Prominence

**Source principles:** *Destructive commands without a warning
callout* (anti-pattern); *Piped-to-shell installers with no manual
alternative* (anti-pattern); *Hard safety rules*.

**Judges:** When destructive or security-sensitive operations appear
(destructive commands, pipe-to-shell installers, privilege-requiring
steps), are warnings visually prominent — callouts, blockquotes,
bold, or a dedicated "⚠ Warning" prefix — rather than buried in prose
the reader's eye skims? Is the prominence proportional to the risk?

**PASS conditions:** Destructive or security-sensitive steps carry
warnings that a reader scanning the document would see. Pipe-to-shell
installers list a manual alternative within the same section.

**Common fail signal:** "Note: this will delete all your data" in a
normal sentence after the `rm -rf` block; pipe-to-shell installer with
no manual alternative; a sudo-requiring step with no explanation of why.

### D6 Maintenance Posture

**Source principles:** *Keep the README in sync with the code*;
*Hand-maintained duplicates of `--help` output* (anti-pattern);
*Duplicated docs inside the README* (anti-pattern).

**Judges:** Staleness indicators visible in the text: commands that
likely no longer work (refer to renamed flags, removed subcommands),
pinned version numbers that look out of date, hand-maintained `--help`
output, "coming soon" links, duplicated content from
`CONTRIBUTING.md` / `ARCHITECTURE.md`, references to features the
project has moved past.

**PASS conditions:** No drift indicators visible. The README is a
pointer to detailed docs, not a duplicate.

**Common fail signal:** A "Roadmap" section with items marked "Q3
2023"; a pasted `--help` block three years old; "See CONTRIBUTING
below" followed by 200 lines of contributing guidelines that also
live in `CONTRIBUTING.md`.

### D7 Style & Voice

**Source principles:** *Imperative mood for instructions*; *No emoji
in headings* (anti-pattern); *Prose lines under 120 characters*.

**Judges:** Are instructions in imperative mood and second person
("Run `npm install`", not "You should run..." or "Running `npm
install` installs..."). Is jargon defined on first use? Are headings
ASCII-clean (no emoji)? Is prose direct — no hedging adverbs
("simply", "just"), no implicit assumption of expertise?

**PASS conditions:** Instructions read as commands. Jargon explained
on first appearance. Headings are plain text. Language is direct.

**Common fail signal:** "You might want to consider running `npm
install`"; "## 🚀 Getting Started"; "Just run the bootstrap"; prose
that assumes the reader already understands the domain.

## Tier-3 — Cross-Entity Collision

### collision

**What it checks:** When the audit scope holds multiple READMEs in
related projects (monorepo scan), look for near-identical install /
contributing / license boilerplate a maintainer could hoist to a
shared docs page or org-level default.

**Severity:** INFO.

**Source principle:** *Link to detailed docs rather than duplicating*
— cross-repo duplication is a slower-moving form of the same anti-
pattern.

## Cross-Dimension Notes

**All dimensions run always.** A dimension that doesn't apply (D5
Warning Prominence on a README with no destructive ops; D2
Installation Correctness on a README that is intentionally minimal —
e.g., a hello-world example in a blog post repo) returns PASS
silently.

**One finding per dimension maximum.** If D6 Maintenance Posture
identifies four staleness indicators, surface the highest-signal one
with concrete detail (line number, what to update). Bulk findings
train the user to disregard the audit.

**Severity defaults to WARN.** Tier-2 findings are judgment-level
coaching, not blocking. A dimension that surfaces a safety concern
the Tier-1 scripts missed (e.g., a prose description of how to
bypass authentication the safety script did not match) can be
escalated to FAIL by the judge, but the default is WARN — Tier-1
is where blocking lives.
