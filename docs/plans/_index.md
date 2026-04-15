# Plans


Implementation plans for WOS features.

| File | Description |
| --- | --- |
| [2026-04-13-rebuild-rule-skills.plan.md](2026-04-13-rebuild-rule-skills.plan.md) | Rebuild the build-rule and check-rule skills to incorporate new research on rule taxonomy, Intent section quality, example construction, validation methodology, and repair strategies. |
| [2026-04-14-restructure-toolkit-marketplace.plan.md](2026-04-14-restructure-toolkit-marketplace.plan.md) | Split the wos monorepo into a Claude Code plugin marketplace with 5 self-contained plugins — build, check, wiki, work, consider |
| [2026-04-15-document-inheritance-refactor.plan.md](2026-04-15-document-inheritance-refactor.plan.md) | Replace the flat Document dataclass with a base class + typed subclasses (ResearchDocument, PlanDocument, ChainDocument, WikiDocument), each owning its own validation via issues() and is_valid(). |
| [2026-04-15-simplify-validation-architecture.plan.md](2026-04-15-simplify-validation-architecture.plan.md) | Replace grep-equivalent Python validation with self-contained shell scripts; strip parallel dispatch and table parsing from Python assessment modules; delete /distill and related artifacts; create a clean baseline for the toolkit restructure. |
