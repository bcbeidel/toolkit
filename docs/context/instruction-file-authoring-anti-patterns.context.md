---
name: "Instruction File Authoring Anti-Patterns"
description: "Ten ranked anti-patterns in instruction file authoring, from vagueness and length bloat to persona instructions and redundancy with project docs — the top five have HIGH evidence from practitioner research and empirical studies"
type: context
sources:
  - https://code.claude.com/docs/en/best-practices
  - https://www.humanlayer.dev/blog/writing-a-good-claude-md
  - https://cursor.com/blog/agent-best-practices
  - https://virtuslab.com/blog/ai/how-to-write-rules-for-ai
  - https://www.agentrulegen.com/guides/how-to-write-ai-coding-rules
  - https://www.mindstudio.ai/blog/rules-file-ai-agents-standing-orders-claude-code
  - https://best.openssf.org/Security-Focused-Guide-for-AI-Code-Assistant-Instructions.html
  - https://arxiv.org/abs/2602.11988
  - https://www.trychroma.com/research/context-rot
related:
  - docs/research/2026-04-10-rules-creation-and-curation.research.md
  - docs/context/instruction-file-non-inferable-specificity.context.md
  - docs/context/instruction-file-lifecycle-and-pruning.context.md
  - docs/context/instruction-file-extraction-techniques.context.md
  - docs/context/agents-md-empirical-effectiveness-findings.context.md
---

# Instruction File Authoring Anti-Patterns

Ten anti-patterns appear consistently across practitioner research and empirical studies. The top five have HIGH evidence — multiple independent sources converging on the same failure mode.

## Ranked Anti-Patterns

| # | Anti-Pattern | Evidence | Source |
|---|---|---|---|
| 1 | Vagueness — rules without actionable decision trees | HIGH | VirtusLab, MindStudio, community analysis |
| 2 | Length bloat — files exceeding 200–300 lines | HIGH | Claude Code docs, Chroma context-rot, HumanLayer |
| 3 | Redundancy with model defaults | HIGH | Claude Code docs, ETH Zurich 2602.11988 |
| 4 | Delegating style/format to instruction files instead of linters | HIGH | HumanLayer, Factory.ai, Cursor docs |
| 5 | Stale rules — outdated APIs, deprecated patterns | HIGH | MindStudio, Cursor docs, Trigger.dev |
| 6 | Copying community templates wholesale | MODERATE | Cursor docs, OpenSSF, community analysis |
| 7 | Contradictory rules | MODERATE | MindStudio, GitHub Copilot docs |
| 8 | Missing negative rules | MODERATE | MindStudio, VirtusLab |
| 9 | Persona instructions ("act as a senior security expert") | MODERATE | OpenSSF (Sept 2025) |
| 10 | Redundancy with existing project documentation | MODERATE | ETH Zurich 2602.11988 |

## Top Anti-Patterns Explained

**Vagueness.** Rules must produce consistent decisions. "Use semantic selectors" is vague; "Use getByRole() before getByLabel() before getByPlaceholder()" is not. The specificity test: if two developers reading the rule would make different decisions in the same situation, the rule is too vague to follow. Weak phrasing ("prefer," "try to," "maybe") compounds the problem — use strong directives ("always," "never," "IMPORTANT") for constraints that must hold.

**Length bloat.** Claude Code's docs warn explicitly: "Bloated CLAUDE.md files cause Claude to ignore your actual instructions." Chroma's context-rot research tested 18 frontier models and found performance drops at every length increment — even a single distractor reduces accuracy. Practitioner consensus: 300 lines maximum; HumanLayer maintains under 60. The attention gradient also matters: critical rules near the top and bottom of a file survive length better than rules buried in the middle.

**Redundancy with model defaults.** Stating "use TypeScript" in a TypeScript project, or "write clean code," wastes tokens without changing behavior. Every rule should pass the removal test: would removing this line cause the agent to make a mistake? If not, cut it. ETH Zurich's finding that LLM-generated context files hurt task success −0.5% to −2% is attributable primarily to this anti-pattern — files that redundantly describe what agents can already read from code or existing docs.

**Delegating style to instruction files.** Rules like "use 2-space indentation" or "no semicolons" belong in a linter or formatter, not an instruction file. HumanLayer: "Never send an LLM to do a linter's job." Factory.ai: "AI can choose to ignore documentation, but it cannot ignore linting errors in your CI pipeline." Style rules in instruction files consume rule-following headroom and are less reliably enforced than tool-enforced constraints.

**Stale rules.** Rules that reference outdated APIs, deprecated frameworks, or superseded patterns actively mislead agents. MindStudio: "A stale rules file is worse than no rules file in some cases." Framework upgrades and API changes require immediate instruction file review. Schedule audits; don't wait for observed failures.

**Persona instructions.** OpenSSF's security guide (Sept 2025) found that telling the system it is an expert ("act as a senior security expert") often makes it perform worse on the tasks the persona is meant to improve. Persona framing consumes tokens without grounding the model in concrete, actionable constraints. Prefer specific rules over identity framing.

**Redundancy with project documentation.** ETH Zurich's exception case isolates this: when existing project markdown was stripped, generated context files improved task success by +2.7%. The anti-pattern is duplication of what agents can already read, not the existence of context files. Before adding a rule, check whether the information is already in a README or linked doc.
