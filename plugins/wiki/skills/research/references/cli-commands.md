---
name: Python Utilities Reference
description: CLI commands for lint and URL checking during research sessions
stage: shared
pipeline: research
---

## Purpose
Reference for CLI commands used across multiple research stages — lint validation and URL reachability checking.

# Python Utilities Reference

CLI commands for research sessions. `<plugin-scripts-dir>` refers to
the `scripts/` directory at the root of the `wiki` plugin (`plugins/wiki/scripts/`).

## Validate a Document

```bash
python <plugin-scripts-dir>/lint.py <file> --root . [--urls]
```

## Check URL Reachability

```bash
python <plugin-scripts-dir>/check_url.py URL1 URL2 ...
```
