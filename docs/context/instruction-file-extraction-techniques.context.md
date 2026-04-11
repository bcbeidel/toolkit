---
name: "Instruction File Extraction Techniques"
description: "Three techniques for extracting instruction file rules from existing codebases, ranked by evidence strength: iterative correction loop, meta-prompt from code samples, and full-codebase scan — all require a human filtering pass before deployment"
type: context
sources:
  - https://cursor.com/blog/agent-best-practices
  - https://code.claude.com/docs/en/best-practices
  - https://virtuslab.com/blog/ai/how-to-write-rules-for-ai
  - https://github.com/nedcodes-ok/rule-gen
  - https://arxiv.org/abs/2602.11988
  - https://arize.com/blog/optimizing-coding-agent-rules-claude-md-agents-md-clinerules-cursor-rules-for-improved-accuracy/
related:
  - docs/research/2026-04-10-rules-creation-and-curation.research.md
  - docs/context/instruction-file-lifecycle-and-pruning.context.md
  - docs/context/agents-md-empirical-effectiveness-findings.context.md
  - docs/context/instruction-file-authoring-anti-patterns.context.md
---

# Instruction File Extraction Techniques

Three techniques extract rules from existing source material. All three produce candidate rules that require a human filtering pass before deployment — the ETH Zurich finding (arXiv 2602.11988) shows that unfiltered generated rules reduce task success −0.5% to −2%.

## T1: Iterative Correction Loop (Highest Evidence)

Add a rule every time the agent makes the same mistake twice. Both Claude Code and Cursor official docs recommend this explicitly.

The loop: observe failure → identify pattern → write a specific rule addressing the failure case → verify behavior shifts. Rules produced this way have demonstrated failure-case coverage — they map directly to observed failure modes rather than hypothesized ones.

Arize's automated variant of this pattern (Prompt Learning) applies iterative optimization with unit test feedback, improving GPT-4.1 performance 10–15%. The key mechanism is "rich English feedback" from LLM evaluation, not just pass/fail signals. This suggests the loop works because it grounds each rule in a concrete failure instance.

Practical threshold: optimized rule sets contain 20–50 rules. Below this range, coverage is thin; above it, attention degradation sets in.

## T2: Meta-Prompt Extraction from Code Samples

Provide 2–3 existing code files and ask an LLM to extract conventions. VirtusLab describes this as their preferred approach: "LLMs are extremely good at pattern recognition, even patterns you don't realize you follow."

A meta-prompt (publicly available via VirtusLab's blog) instructs the model to identify recurring patterns across the sample files and express them as actionable rules. The output is codebase-specific rather than generic — rules like "import Prisma from `../db` — never instantiate PrismaClient directly" rather than "use dependency injection."

This technique captures conventions that developers follow unconsciously, making it useful for bootstrapping a rules file for an existing codebase where the iterative loop hasn't had time to accumulate rules.

## T3: Full-Codebase Scan via Large-Context Model

Tools like rule-gen (nedcodes-ok/rule-gen on GitHub) automate rules extraction by scanning the full project tree using a 1M-token context model (e.g., Gemini 1.5 Pro). The pipeline:

1. Scan project tree, respecting `.gitignore`, skipping binaries
2. Prioritize config files, entry points, routes, and pattern-rich source files
3. Detect tech stack from `package.json`, `requirements.txt`, etc.
4. Send unified context in a single API call
5. Output to the target format: `.cursor/rules/`, `CLAUDE.md`, `AGENTS.md`, or `.github/copilot-instructions.md`

This produces highly specific rules tied to the actual codebase structure, but requires a large-context model and per-use API cost. The ETH Zurich caveat applies: generated output must be filtered before deployment. Classify each rule as Essential, Helpful, Redundant, or Move-to-tooling before committing.

## Filtering Pass (Required for All Techniques)

All three techniques produce candidate rules, not deployment-ready files. Before deploying any extracted rules:

- **Essential**: architecture decisions, non-inferable constraints → keep
- **Helpful**: measurably improves output → keep
- **Redundant**: model already does this, visible in code → delete
- **Move-to-tooling**: style/format enforcement → move to linter or formatter

See `docs/context/instruction-file-lifecycle-and-pruning.context.md` for the full lifecycle pattern.
