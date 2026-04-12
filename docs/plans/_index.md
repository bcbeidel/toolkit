# Plans


Implementation plans for WOS features.

| File | Description |
| --- | --- |
| [2026-04-07-knowledge-base-rebuild.plan.md](2026-04-07-knowledge-base-rebuild.plan.md) | Clean-sweep rebuild of the WOS knowledge base — archive existing docs, research 72 topics with fresh sources, distill into focused context files |
| [2026-04-10-roadmap-v036-v039.plan.md](2026-04-10-roadmap-v036-v039.plan.md) | Execute 15 feature issues across 4 releases — wiki foundation, skill refresh, audit-chain and build/audit family, and orchestrator |
| [2026-04-10-skill-script-renames.plan.md](2026-04-10-skill-script-renames.plan.md) | Rename audit-wos→lint, init-wos→setup, audit.py→lint.py, and update all cross-references |
| [2026-04-10-wiki-schema-infrastructure.plan.md](2026-04-10-wiki-schema-infrastructure.plan.md) | Add wos/wiki.py validators, validate_wiki() in validators.py, wiki auto-detection in scripts/lint.py, and a default SCHEMA.md template — Python foundation for the wiki feature. |
| [2026-04-11-audit-chain.plan.md](2026-04-11-audit-chain.plan.md) | Single skill for designing and auditing skill chains — goal-to-manifest design mode and manifest repair loop mode. |
| [2026-04-11-audit-orchestrator.plan.md](2026-04-11-audit-orchestrator.plan.md) | Create the /wos:audit skill as the top-level project health orchestrator combining lint, audit-skill, audit-rule, audit-chain, and wiki validation into a prioritized report |
| [2026-04-11-build-audit-command-hook.plan.md](2026-04-11-build-audit-command-hook.plan.md) | Add 4 SKILL.md files completing the build/audit family for Claude Code commands and hooks (issue #229) |
| [2026-04-11-build-audit-rule.plan.md](2026-04-11-build-audit-rule.plan.md) | Add /wos:build-rule and /wos:audit-rule as the build-X/audit-X pair for Claude Code rules, replacing deprecated check-rules and extract-rules |
| [2026-04-11-build-audit-skill.plan.md](2026-04-11-build-audit-skill.plan.md) | Two skills for the skill development lifecycle — /wos:build-skill scaffolds new SKILL.md files, /wos:audit-skill quality-audits existing ones |
| [2026-04-11-build-audit-subagent.plan.md](2026-04-11-build-audit-subagent.plan.md) | Add /wos:build-subagent and /wos:audit-subagent skills to scaffold and audit Claude Code custom subagent definitions in .claude/agents/<name>.md |
| [2026-04-11-build-skill-improvements.plan.md](2026-04-11-build-skill-improvements.plan.md) | Apply seven improvements to skills/build-skill/SKILL.md derived from the skill-curation comparative analysis (G1, G2, G4, G5, G9/G11, G10, G12). |
| [2026-04-11-chain-infrastructure.plan.md](2026-04-11-chain-infrastructure.plan.md) | Add wos/chain.py validators, validate_chain() in validators.py, and lint.py auto-detection for *.chain.md manifests. |
| [2026-04-11-context-docs-anti-patterns-update.plan.md](2026-04-11-context-docs-anti-patterns-update.plan.md) | Add anti-patterns #11 and #12 to instruction-file-authoring-anti-patterns.context.md and update corroborating evidence for #2 and #8, closing gaps identified in the skill curation comparative analysis |
| [2026-04-11-context-migration.plan.md](2026-04-11-context-migration.plan.md) | Add confidence, created, updated, and wiki-compatible type fields to all 190 docs/context/*.context.md files — closes bcbeidel/wos#220 |
| [2026-04-11-deprecate-retrospective.plan.md](2026-04-11-deprecate-retrospective.plan.md) | Add deprecation header and notice to the retrospective skill, update OVERVIEW.md and README.md to reflect deprecated status ahead of removal in v0.39.0 |
| [2026-04-11-handoff-contracts.plan.md](2026-04-11-handoff-contracts.plan.md) | Add a standardized ## Handoff section (Receives / Produces / Chainable-to) to every existing SKILL.md — prerequisite for audit-chain |
| [2026-04-11-ingest-skill.plan.md](2026-04-11-ingest-skill.plan.md) | Add skills/ingest/SKILL.md — universal source intake that updates 5–15 wiki pages per invocation with append-only semantics |
| [2026-04-11-skill-authoring-guide-improvements.plan.md](2026-04-11-skill-authoring-guide-improvements.plan.md) | Apply nine progressive-disclosure and cross-platform findings from the skill curation comparative analysis to skill-authoring-guide.md |
| [2026-04-12-build-skill-deep-gap-analysis.plan.md](2026-04-12-build-skill-deep-gap-analysis.plan.md) | Findings from deep structural analysis of build-skill/SKILL.md — L2/L3 collapse (3 sections to extract), body quality fixes, and workflow inconsistencies not covered by prior plans |
| [2026-04-11-skill-refresh.plan.md](2026-04-11-skill-refresh.plan.md) | Review and update all 14 SKILL.md files against the v0.35.0 context base — adding anti-pattern guards, strengthening gate checks, and removing contraindicated approaches |
| [2026-04-11-unified-skill-vocabulary.plan.md](2026-04-11-unified-skill-vocabulary.plan.md) | Rename delivery pipeline and meta audit skills to consistent verb-object pairs, restore retrospective as standalone, and update all cross-references and documentation. |
| [2026-04-11-workflow-doc.plan.md](2026-04-11-workflow-doc.plan.md) | Create WORKFLOW.md at project root documenting the canonical WOS workflows — development lifecycle, knowledge management, self-improvement loop, skill chain design, and primitive taxonomy. |
