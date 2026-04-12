---
name: "Single-Entry-Point Creation Routing"
description: "One command, interactive type prompt — how scaffold tools structurally prevent starting-point errors by forcing type selection before scaffolding begins"
type: context
sources:
  - https://vscode-docs.readthedocs.io/en/stable/tools/yocode/
  - https://github.com/microsoft/vscode-generator-code
  - https://nx.dev/docs/reference/create-nx-workspace
  - https://nextjs.org/docs/app/api-reference/cli/create-next-app
  - https://turborepo.dev/docs/reference/create-turbo
  - https://plugins.jetbrains.com/docs/intellij/plugin-types.html
related:
  - docs/research/2026-04-11-primitive-selection-routing.research.md
  - docs/context/creation-time-intake-routing.context.md
---

Single-entry-point creation routing is the dominant scaffolding pattern for developer tools: one command, one interactive prompt asking for type, then type-specific scaffolding. The structural effect is that users cannot accidentally begin on the wrong scaffolding path — they must actively select the wrong type from a presented list.

VS Code's `yo code` is the clearest example within a plugin ecosystem for an existing tool. Running `yo code` presents an interactive menu: "What type of extension do you want?" — routing to extension, color theme, language support, snippets, keymap, or extension pack. Type selection is the first question; subsequent prompts are type-specific. There is no separate `yo code-theme` or `yo code-command`. The generator's README confirms type selection triggers distinct question sequences (selecting "theme" prompts for a TextMate file path; selecting "command extension" prompts for command name and display name).

At broader scale, Nx's `create-nx-workspace` is structurally equivalent and covers cross-framework selection: "Which stack do you want to use?" routes to Angular, React, Next.js, Nest, Express, or empty workspace configurations before any framework-specific questions appear. `create-next-app` and `create-turbo` follow the same pattern within their ecosystems — single entry, interactive prompts, type-specific scaffolding.

**The counterexample: JetBrains**

JetBrains takes the opposite approach. The Plugin Types page lists five categories (Custom Language Support, Framework Integration, Tool Integration, UI Add-Ons, Themes) with brief descriptions and links to examples. Developers self-select based on whether a description matches their use case. There is no routing wizard, no interactive intake, no cross-referencing. The only pre-selection gate is a link to "alternative solutions" — a passive redirect, not an interactive prompt.

**What this pattern cannot do**

Single-entry-point routing prevents starting-point errors only for users who can correctly identify their intent from a type list. It routes on declared type, not on underlying intent. A user who doesn't know the difference between a "skill" and a "hook" will still select incorrectly from a presented list — the structural protection applies to accidental omission (forgetting to choose type), not to semantic misidentification. No controlled study was found measuring the actual error-rate difference between single-entry-point and separate-path creation flows. The structural advantage is logical, not empirically measured. (MODERATE confidence — multiple T1 examples confirm the pattern as common practice; effectiveness claim is structural only.)

**Takeaway:** Single-entry-point routing is the established scaffold pattern for preventing accidental wrong-path creation. Its limit is that it routes on declared type, not intent — users who don't know their type will mis-declare it.
