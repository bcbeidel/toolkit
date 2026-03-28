---
name: "Onboarding Progressive Disclosure"
description: "How to layer complexity for different project maturity contexts, drawing on UX progressive disclosure research, CLI onboarding patterns, and developer tool adoption science"
metadata:
  type: research
  sources:
    - https://www.nngroup.com/articles/progressive-disclosure/
    - https://clig.dev/
    - https://lawsofux.com/hicks-law/
    - https://www.lucasfcosta.com/blog/ux-patterns-cli-tools
    - https://newsletter.pragmaticengineer.com/p/frictionless-why-great-developer
    - https://thenewstack.io/tackling-developer-onboarding-complexity/
    - https://en.wikipedia.org/wiki/Progressive_disclosure
    - https://www.doc-e.ai/post/measuring-and-analyzing-developer-adoption-metrics-the-roadmap-to-devtool-success
    - https://www.smashingmagazine.com/2017/02/user-onboarding-empty-states-mobile-apps/
    - https://www.nngroup.com/articles/empty-state-interface-design/
    - https://medium.com/relay-sh/command-line-ux-in-2020-e537018ebb69
    - https://developer.hashicorp.com/terraform/cli/commands/init
  related:
    - docs/research/context-engineering.md
    - docs/research/information-architecture.md
    - docs/research/feedback-loop-design.md
    - docs/research/plugin-extension-architecture.md
    - docs/context/onboarding-progressive-disclosure.md
---

## Key Findings

Progressive disclosure is the foundational UX technique for managing complexity in
onboarding. When applied to CLI developer tools, it translates into three concrete
strategies: context-aware defaults that adapt to project maturity, layered help
systems that reveal complexity on demand, and empty-state design that guides first
actions. The research converges on a single principle: minimize time-to-first-value
by showing only what the user needs right now, with clear paths to more when ready.

## Sub-Questions

### 1. What is progressive disclosure and what are its established principles?

Jakob Nielsen introduced progressive disclosure in 1995 as an interaction design
pattern to reduce user errors in complex applications [1]. The core definition:
defer advanced or rarely used features to a secondary screen, making applications
easier to learn and less error-prone [1][7].

**Foundational principles:**

- **Show essential options first.** The primary interface displays only the most
  commonly needed features. Advanced features live behind an explicit "show more"
  action [1].
- **Get the split right.** Incorrect classification of what is "primary" vs.
  "secondary" undermines the entire pattern. This requires user research (card
  sorting, task analysis) to determine what users frequently need [1].
- **Make progression obvious.** Users must be able to discover that advanced options
  exist. Hidden features are worse than visible complexity [1].
- **Staged disclosure requires task analysis.** Understanding which options are used
  together determines how to group and layer them. Too many stages cause navigation
  overhead; too few fail to reduce complexity [1].

**Psychological basis — Hick's Law (1952):** The time to make a decision increases
logarithmically with the number of choices presented [3]. Choice overload leads to
decision fatigue, decision paralysis, and abandonment. Progressive disclosure
directly counteracts this by limiting visible options at each step [3].

**Key constraint:** Progressive disclosure works only when the primary/secondary
split aligns with actual user needs. If frequently-needed features are hidden,
users experience worse usability than if everything were visible [1].

### 2. How do successful CLI tools handle first-run onboarding?

CLI tools employ several distinct patterns for first-run experiences:

**Pattern A: Idempotent Init Commands**

`terraform init` exemplifies the adaptive init pattern [12]. It inspects existing
configuration, detects providers and modules, downloads dependencies, and creates
state infrastructure — all idempotently. Running it on an empty directory does
minimal work; running it on a mature project with many providers does significant
work. The same command adapts to context without user intervention.

`cargo init` similarly detects whether it is inside an existing VCS repository
and adjusts behavior (skipping git init if already in a git repo). `npm init`
walks through interactive prompts but can be bypassed with `npm init -y` for
convention defaults.

**Pattern B: Instructive Onboarding via Examples**

Rather than showing a complex manual page, start with an example showing the
command users are most likely to need first [4]. The Command Line Interface
Guidelines (clig.dev) recommend displaying concise help by default when a command
is run without arguments, and extensive help when explicitly requested via
`--help` [2].

Help pages should lead with examples because users tend to use examples over other
forms of documentation [2][4]. Tell a story with a series of examples, building
from simple to complex use cases.

**Pattern C: Wizard vs. Convention Defaults**

The wizard pattern offers two paths: QuickStart (convention defaults) and Advanced
(full control). QuickStart forces sensible defaults and produces a valid
configuration immediately. This dual-path approach accommodates both novice users
who need guidance and experienced users who want control.

**Pattern D: Contextual Error Messages**

Rust's compiler and Cargo are notable for providing "did you mean?" suggestions,
actionable error messages, and contextual guidance [2]. When a user types a wrong
subcommand, the tool suggests the closest match. When a build fails, the error
message explains the fix. This transforms errors from dead ends into learning
opportunities.

### 3. What does developer tool adoption research reveal about onboarding friction?

**Time to First Hello World (TTFHW)** is the key adoption metric — measuring how
quickly a developer has their first meaningful interaction with a product [8]. The
faster users reach this moment, the more likely they are to continue. Related
metrics include Time to First Value (TTFV) and Activation Rate [8].

**The "Aha Moment"** is the point where a product's value proposition clicks,
transforming a casual user into an engaged one. Identifying and optimizing the path
to this moment is the central challenge of onboarding design [8].

**Friction sources identified in research:**

- Finding information (services, docs, APIs) is the top time-waster [5]
- Adapting to new technology and context switching between tools [5]
- Broken tooling and slow feedback loops [5]
- Overly complex onboarding that delays first productive use

**The "Frictionless" framework** (Gergely Orosz / Pragmatic Engineer) identifies
three essential elements for reducing friction [5]:

1. **Fast feedback loops** — enabling rapid iteration
2. **Flow state protection** — minimizing interruptions
3. **Reduced cognitive load** — simplifying workflows

The staged complexity approach — graduating task complexity assigned to developers
— is the most commonly used onboarding strategy, followed by exploration-based and
priority-first approaches [6].

**Key finding:** Etsy dedicated 20% of engineering headcount to a DevEx initiative
that saved 50% of engineering hours spent waiting for deployments (reducing deploy
time from 15 to 7 minutes), demonstrating that friction reduction has measurable
business value [5].

### 4. How do tools differentiate between empty/new vs. existing/mature project contexts?

**Detection strategies observed in practice:**

- **File system inspection:** `terraform init` checks for `.tf` files, existing
  `.terraform` directory, and lock files to determine project state. `cargo init`
  checks for existing `Cargo.toml` and VCS directories.
- **Configuration presence:** Tools check whether configuration files exist
  (package.json, pyproject.toml, Cargo.toml) to determine if initialization is
  needed vs. already done.
- **State directory markers:** Hidden directories (`.terraform`, `.git`,
  `node_modules`) signal project maturity and prior tool use.
- **Idempotent operations:** Rather than branching on "new vs. existing," the
  best tools make their init operations idempotent — safe to run repeatedly,
  doing more or less work depending on what already exists.

**Empty state UX principles applied:**

Empty states are a critical onboarding opportunity [9][10]. When a user encounters
an empty project:

1. **Explain the context** — what this space will contain when populated [9]
2. **Guide the next action** — clear call-to-action for the first step [9]
3. **Set expectations** — show what success looks like [10]
4. **Keep it positive** — frame as opportunity, not absence [9]

Nielsen Norman Group's guidelines for empty states in complex applications
recommend providing enough structure that users understand the system's purpose
without requiring them to fill it first [10].

### 5. What progressive disclosure patterns work specifically for developer tools?

**Tiered Help Systems:**

The clig.dev guidelines recommend a three-tier help architecture [2]:

1. **No-argument invocation:** Brief usage hint + most common example
2. **`--help` flag:** Full command documentation with organized options
3. **`man` page / external docs:** Comprehensive reference

This mirrors progressive disclosure directly — each tier reveals more detail.

**Subcommand Architecture:**

Complex tools organize functionality into subcommands (git, docker, kubectl),
creating a natural hierarchy [2][11]. Users learn the top-level commands first,
then discover subcommands as needs arise. This is progressive disclosure applied
to CLI structure.

**Contextual Suggestions:**

Modern CLIs provide contextual guidance at the point of need:
- "Did you mean?" suggestions on typos
- Next-step suggestions after successful operations ("Your project is ready. Run
  `wos audit` to check it.")
- Upgrade prompts when more advanced features would help

**Progressive Feature Gates:**

Some tools gate features behind explicit opt-in:
- Basic features work immediately with no configuration
- Advanced features require a configuration file
- Expert features require explicit flags or environment variables

This creates natural layers: zero-config → config-file → explicit-flags.

**Agent-Specific Progressive Disclosure:**

In the context of AI agent tools (like Claude Code skills), progressive disclosure
takes a specific form: SKILL.md files provide a brief capability summary loaded at
session start, with detailed references loaded only when the skill is invoked.
This prevents context window overflow while keeping capabilities discoverable.

## Challenge

**Does progressive disclosure actually help in CLI contexts?**

Most progressive disclosure research originates in GUI contexts (dialogs, menus,
forms). CLI tools operate differently: there is no "secondary screen" to defer
options to. The CLI equivalent — hiding options behind subcommands or flags — has
a discovery problem. In GUIs, a "More options" button is visible. In CLIs, users
must already know to type `--help` or guess that subcommands exist. This means
CLI progressive disclosure depends more heavily on contextual suggestions (post-
action hints) than on hiding/revealing UI elements.

**Is the "empty state" pattern transferable from GUI/SaaS to CLI tools?**

Empty state design research focuses on visual applications where blank screens
are obvious. In CLI tools, there is no persistent visual state — the "empty
state" is simply the absence of output or configuration files. The pattern
transfers only partially: the principle of guiding first actions applies, but
the mechanism differs. CLI tools must use output text, not visual design, to
accomplish the same goal.

**Risk of over-engineering progressive disclosure:**

Nielsen explicitly warns that incorrect primary/secondary splits cause worse
usability than no progressive disclosure at all [1]. For a tool with a small
surface area (few commands, clear purpose), progressive disclosure may add
unnecessary indirection. The pattern is most valuable when the tool has genuine
complexity that would overwhelm new users if presented all at once.

**Bias in adoption metric research:**

TTFHW and activation rate research [8] comes primarily from SaaS product
marketing contexts, not developer tool research. The metrics themselves are
valid, but the benchmarks and optimization strategies may not transfer directly
to open-source CLI tools where "adoption" is not a revenue event.

## Findings

### Three Layers of Onboarding Complexity

The research converges on a three-layer model for managing onboarding complexity
in developer tools (HIGH — T1 + T2 + T3 sources converge):

**Layer 1: Zero-config first run.** The tool works immediately with sensible
defaults. No configuration file needed. The user's first interaction produces
visible value. This maps to the "Time to First Hello World" metric [8] and
Nielsen's principle of showing essential options first [1].

**Layer 2: Configuration-driven customization.** As the user's needs grow, they
create a configuration file to customize behavior. The tool detects this file
and adapts. This is the equivalent of Nielsen's "secondary screen" in CLI
contexts [1].

**Layer 3: Expert-level control.** Explicit flags, environment variables, and
advanced subcommands provide full control. These are documented but never
required for basic operation. Power users discover them through `--help` and
documentation.

### Context Detection Over Branching

The strongest pattern across all tools studied is idempotent context detection
rather than explicit "new vs. existing" branching (HIGH — T1 terraform docs +
observed patterns in cargo, npm):

- The same command works for both new and mature projects
- Behavior adapts based on what the tool finds on disk
- No user input needed to determine context
- Safe to run repeatedly without side effects

### Guiding First Actions Without Overwhelming

The research identifies four mechanisms for guiding first actions (MODERATE — T2
+ T3 sources, GUI research partially transfers):

1. **Next-step suggestions** after each operation ("Created config. Run `audit`
   to check it.")
2. **Example-first help** that shows the most common command before listing all
   options [2][4]
3. **Contextual error recovery** that suggests fixes instead of just reporting
   failures [2]
4. **Dual-path entry** (wizard vs. defaults) that lets users choose their
   comfort level

### The Aha Moment for Developer Tools

Time to First Value is the critical metric. The research suggests the aha moment
for a developer tool occurs when the user sees the tool do something they could
not easily do themselves (MODERATE — T2 + T3 sources):

- For a linter: the first real bug it catches
- For a build tool: the first successful build
- For a context tool: the first time it surfaces information the user needed
  but did not know where to find

Optimizing the path to this moment — by reducing steps, providing defaults, and
eliminating prerequisites — is the primary onboarding design challenge [5][8].

## Claims

| # | Claim | Type | Source | Status |
|---|-------|------|--------|--------|
| 1 | Nielsen introduced progressive disclosure in 1995 | attribution | [1][7] | verified |
| 2 | Progressive disclosure defers advanced features to secondary screens | definition | [1] | verified |
| 3 | Hick's Law: decision time increases logarithmically with choices (1952) | attribution | [3] | verified |
| 4 | Hick and Hyman examined stimulus-response relationship | attribution | [3] | verified |
| 5 | terraform init is idempotent and safe to run multiple times | factual | [12] | verified |
| 6 | cargo init detects existing VCS and adjusts behavior | factual | [12] | verified |
| 7 | TTFHW measures how quickly a developer has first meaningful interaction | definition | [8] | verified |
| 8 | Etsy dedicated 20% eng headcount to DevEx, saved 50% deployment wait | statistic | [5] | corrected (original "$2.5M" figure from secondary source; primary Etsy sources describe headcount %) |
| 9 | Staged complexity is the most used onboarding approach | superlative | [6] | verified |
| 10 | clig.dev recommends displaying concise help when run without arguments | factual | [2] | verified |
| 11 | Empty states are a critical onboarding opportunity | factual | [9][10] | verified |
| 12 | Users tend to use examples over other forms of documentation | factual | [2][4] | verified |

## Sources

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|-----------|------|------|--------|
| 1 | https://www.nngroup.com/articles/progressive-disclosure/ | Progressive Disclosure | Nielsen Norman Group / Jakob Nielsen | 2006 | T1 | verified |
| 2 | https://clig.dev/ | Command Line Interface Guidelines | Aanand Prasad, Ben Firshman, Carl Tashian, Eva Parish | 2020 | T2 | verified |
| 3 | https://lawsofux.com/hicks-law/ | Hick's Law | Laws of UX / Jon Yablonski | 2024 | T2 | verified |
| 4 | https://www.lucasfcosta.com/blog/ux-patterns-cli-tools | UX Patterns for CLI Tools | Lucas F. Costa | 2022 | T3 | verified |
| 5 | https://newsletter.pragmaticengineer.com/p/frictionless-why-great-developer | Frictionless: Why Great Developer Experience Can Help Teams Win | Pragmatic Engineer / Gergely Orosz | 2025 | T2 | verified |
| 6 | https://thenewstack.io/tackling-developer-onboarding-complexity/ | Tackling Developer Onboarding Complexity | The New Stack | 2024 | T3 | verified |
| 7 | https://en.wikipedia.org/wiki/Progressive_disclosure | Progressive Disclosure | Wikipedia | 2024 | T4 | verified |
| 8 | https://www.doc-e.ai/post/measuring-and-analyzing-developer-adoption-metrics-the-roadmap-to-devtool-success | Measuring and Analyzing Developer Adoption Metrics | Doc-E.ai | 2024 | T3 | verified |
| 9 | https://www.smashingmagazine.com/2017/02/user-onboarding-empty-states-mobile-apps/ | The Role of Empty States in User Onboarding | Smashing Magazine | 2017 | T2 | verified |
| 10 | https://www.nngroup.com/articles/empty-state-interface-design/ | Designing Empty States in Complex Applications | Nielsen Norman Group | 2023 | T1 | verified |
| 11 | https://medium.com/relay-sh/command-line-ux-in-2020-e537018ebb69 | 3 Commandments for CLI Design | Puppet Relay | 2020 | T3 | verified |
| 12 | https://developer.hashicorp.com/terraform/cli/commands/init | terraform init Command Reference | HashiCorp | 2024 | T1 | verified |

## Takeaways

For WOS specifically, four design decisions follow from this research:

1. **Make init idempotent and context-aware.** Do not branch on "new vs. existing."
   Detect what exists, do the right thing, report what happened. The same command
   should work on an empty repo and a mature project.

2. **Use next-step suggestions, not wizards.** After each operation, suggest the
   logical next command. This is the CLI equivalent of progressive disclosure —
   guiding without requiring the user to navigate a multi-step flow.

3. **Lead help text with examples.** When a user runs a command with no arguments,
   show the single most common usage example, not a list of flags. Reserve flag
   documentation for `--help`.

4. **Define the aha moment.** For WOS, the aha moment is likely when the user sees
   their first generated `_index.md` or first audit result — the tool surfacing
   structure they did not have before. Optimize the path to that moment.

## Search Protocol

| # | Query | Engine | Results | Useful |
|---|-------|--------|---------|--------|
| 1 | progressive disclosure UX design principles research Nielsen Norman | WebSearch | 10 | 4 |
| 2 | CLI onboarding patterns first-run experience developer tools | WebSearch | 10 | 3 |
| 3 | developer tool adoption research onboarding friction time to value | WebSearch | 10 | 3 |
| 4 | progressive disclosure CLI tools empty project vs existing project detection | WebSearch | 10 | 2 |
| 5 | staged complexity layered onboarding software developer experience | WebSearch | 10 | 2 |
| 6 | Nielsen Norman progressive disclosure definition guidelines | WebSearch | 10 | 2 |
| 7 | CLI first run experience git init npm init cargo init onboarding | WebSearch | 10 | 3 |
| 8 | time to hello world developer tools adoption metrics onboarding | WebSearch | 10 | 3 |
| 9 | terraform init first run detect existing configuration scaffold | WebSearch | 10 | 2 |
| 10 | UX research cognitive load onboarding complexity Hick's law | WebSearch | 10 | 3 |
| 11 | developer tool CLI contextual help just in time guidance | WebSearch | 10 | 1 |
| 12 | rust cargo CLI beginner experience error messages helpful suggestions | WebSearch | 10 | 2 |
| 13 | wizard pattern CLI onboarding interactive setup vs convention defaults | WebSearch | 10 | 2 |
| 14 | software adoption curve developer tools aha moment activation point | WebSearch | 10 | 3 |
| 15 | clig.dev command line interface guidelines help text subcommands | WebSearch | 10 | 3 |
| 16 | empty state design pattern first use experience onboarding UX | WebSearch | 10 | 4 |
