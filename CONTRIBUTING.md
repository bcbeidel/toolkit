# Contributing to WOS

## Versioning (SemVer)

Pre-1.0 — the public API is not yet stable.

Version bump requires updating all three: `pyproject.toml`,
`.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`

| Bump | When | Examples |
|------|------|----------|
| **Patch** (0.x.**Z**) | Bug fixes, internal refactors, doc-only changes | Fix `--fix` stripping preambles, rename private to public API |
| **Minor** (0.**Y**.0) | New features, new/removed skills or commands, behavioral changes to existing skills/scripts | Add `/wos:consider`, new validation check, change CLI flags |
| **Major** (**X**.0.0) | Explicit human decision only. Signals API stability commitment. Never automated, never triggered by a single change. | Declaring 1.0 |

**No version bump needed for:** plans, research docs, changelog updates,
CI config changes — anything that doesn't ship in the plugin.
