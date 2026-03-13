# Python Utilities Reference

CLI commands for research sessions. `<plugin-scripts-dir>` refers to
the `scripts/` directory at the root of the WOS plugin.

## Validate a Document

```bash
uv run <plugin-scripts-dir>/audit.py <file> --root . [--no-urls]
```

## Regenerate Index Files

```bash
uv run <plugin-scripts-dir>/reindex.py --root .
```

## Check URL Reachability

```bash
uv run <plugin-scripts-dir>/check_url.py URL1 URL2 ...
```
