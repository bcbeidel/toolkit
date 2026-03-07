# Python Utilities Reference

CLI commands available during research sessions. All commands use
`<plugin-scripts-dir>` to resolve script paths — this refers to the `scripts/`
directory at the root of the WOS plugin.

## Validate a Single Document

Runs all checks: frontmatter, content length, source URLs, related paths.

```bash
uv run <plugin-scripts-dir>/audit.py <file> [--root DIR] [--no-urls]
```

Example:
```bash
uv run <plugin-scripts-dir>/audit.py docs/research/2026-02-25-my-research.md --root . --no-urls
```

Output on success:
```
All checks passed.
```

Output on failure:
```
1 fail, 0 warn across 1 files

file                                     | sev  | issue
docs/research/my-research.md             | fail | Research document has no sources
```

## Regenerate Index Files

Regenerate all `_index.md` files under `docs/` subdirectories.

```bash
uv run <plugin-scripts-dir>/reindex.py [--root DIR]
```

## Document Model

The `Document` dataclass fields relevant to research:

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `name` | string | Yes | Concise title |
| `description` | string | Yes | One-sentence summary |
| `type` | string | No | Set to `research` for research docs |
| `sources` | list of strings | For research | URLs of verified sources |
| `related` | list of strings | No | Relative paths to related documents |
