---
name: "Onboarding Progressive Disclosure"
description: "A three-layer model for managing CLI tool complexity — zero-config first run, configuration-driven customization, and expert-level control — grounded in progressive disclosure principles and developer adoption research"
metadata:
  type: reference
  sources:
    - https://www.nngroup.com/articles/progressive-disclosure/
    - https://clig.dev/
    - https://lawsofux.com/hicks-law/
    - https://newsletter.pragmaticengineer.com/p/frictionless-why-great-developer
    - https://www.doc-e.ai/post/measuring-and-analyzing-developer-adoption-metrics-the-roadmap-to-devtool-success
    - https://www.nngroup.com/articles/empty-state-interface-design/
    - https://developer.hashicorp.com/terraform/cli/commands/init
  related:
    - docs/research/onboarding-progressive-disclosure.md
    - docs/context/convention-driven-design.md
    - docs/context/idempotency-convergent-operations.md
    - docs/context/feedback-loop-design.md
---

Progressive disclosure — deferring advanced features until needed — is the
foundational UX technique for managing complexity in onboarding. For CLI
developer tools, it translates into a three-layer model, context-aware
defaults, and deliberate optimization of the path to first value.

## Three Layers of Onboarding Complexity

The research converges on three distinct layers for graduating complexity:

**Layer 1: Zero-config first run.** The tool works immediately with sensible
defaults. No configuration file required. The user's first interaction produces
visible value. This maps directly to the "Time to First Hello World" metric
from adoption research and Nielsen's principle of showing essential options
first.

**Layer 2: Configuration-driven customization.** As needs grow, the user
creates a configuration file to customize behavior. The tool detects this file
and adapts. This is the CLI equivalent of Nielsen's "secondary screen" — where
advanced options live without cluttering the primary experience.

**Layer 3: Expert-level control.** Explicit flags, environment variables, and
advanced subcommands provide full control. Documented but never required for
basic operation. Power users discover them through `--help` and reference docs.

This layering reflects Hick's Law: decision time increases logarithmically
with the number of choices presented. Each layer limits visible options to what
matters at the user's current level of engagement.

## Context Detection Over Branching

The strongest pattern across successful tools (terraform, cargo, npm) is
idempotent context detection rather than explicit "new vs. existing" branching.
The same command works for both new and mature projects — behavior adapts based
on what the tool finds on disk, no user input needed. This makes init commands
safe to run repeatedly without side effects, doing more or less work depending
on what already exists.

This connects directly to convention-driven design: file system presence
(config files, state directories, lock files) becomes the implicit signal for
project maturity. No interrogation required.

## Guiding First Actions

Four mechanisms guide users without overwhelming them:

1. **Next-step suggestions** after each operation ("Created config. Run `audit`
   to check it."). This is progressive disclosure's CLI equivalent — revealing
   the next capability at the moment it becomes relevant.
2. **Example-first help** showing the most common command before listing flags.
   Users reach for examples over other documentation forms.
3. **Contextual error recovery** that suggests fixes, not just failures. Rust's
   compiler pioneered this: errors become learning opportunities.
4. **Dual-path entry** (quick-start defaults vs. guided setup) accommodating
   both novices who need guidance and experts who want control.

## Optimizing Time to First Value

Time to First Value (TTFV) is the critical adoption metric. The "aha moment"
for a developer tool occurs when it does something the user could not easily
do themselves. For a linter, that is the first real bug caught. For a context
tool, it is surfacing structure the user did not have before.

Three elements reduce friction on the path to that moment: fast feedback loops
enabling rapid iteration, flow state protection minimizing interruptions, and
reduced cognitive load simplifying workflows.

## Key Constraint

Progressive disclosure fails when the primary/secondary split is wrong. If
frequently-needed features are hidden behind extra steps, usability degrades
worse than if everything were visible. The pattern is most valuable when
genuine complexity would overwhelm new users if presented at once. For tools
with a small surface area, it may add unnecessary indirection.
