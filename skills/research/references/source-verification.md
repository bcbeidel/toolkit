# Source Verification Reference

Mechanical URL verification to catch dead links and hallucinated sources.
Run this after gathering sources and before SIFT evaluation.

## How to Run

Use the `wos.url_checker` module to verify source URLs are reachable:

```bash
uv run <plugin-scripts-dir>/check_url.py https://example.com/page https://other.com/article
```

Each result has:
- `reachable` — `True` if the URL returned 2xx/3xx, `False` otherwise
- `status` — HTTP status code (0 for connection/DNS failures)
- `reason` — human-readable explanation when `reachable=False`

## What to Do with Results

**Unreachable sources (status 404, 0, DNS failure):** Drop them from your
source list. Do not include them in the research document. Note in your
investigation that N sources were removed during verification.

**Unreachable sources (status 403, 5xx):** The source exists but is
temporarily unavailable or paywalled. Keep the source but note the access
issue.

**All sources unreachable:** If verification removes every source, stop and
inform the user. Do not proceed with empty sources — gather new ones instead.
