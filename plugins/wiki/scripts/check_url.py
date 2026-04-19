#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""Check URL reachability using wiki.url_checker.

Usage:
    python scripts/check_url.py URL [URL ...]
"""
from __future__ import annotations

import argparse
import json

import _bootstrap  # noqa: F401 — side effect: adds plugin root to sys.path


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Check URL reachability via HTTP HEAD/GET.",
    )
    parser.add_argument(
        "urls",
        nargs="+",
        metavar="URL",
        help="One or more URLs to check",
    )
    args = parser.parse_args()

    from wiki.url_checker import check_urls

    results = check_urls(args.urls)
    for r in results:
        print(json.dumps({
            "url": r.url,
            "reachable": r.reachable,
            "status": r.status,
            "reason": r.reason,
        }))


if __name__ == "__main__":
    main()
