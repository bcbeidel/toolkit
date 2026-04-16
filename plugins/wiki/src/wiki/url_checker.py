"""URL reachability checker — HTTP HEAD with GET fallback.

Lightweight module for checking whether URLs are reachable.
Uses HEAD requests with a GET fallback when HEAD returns 405.
Used by validators to verify source URL reachability.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen


@dataclass
class UrlCheckResult:
    """Result of checking a single URL's reachability."""

    url: str
    status: int
    reachable: bool
    reason: Optional[str] = None


_HEADERS = {"User-Agent": "wos-url-checker/1.0"}
_TIMEOUT = 10


def check_url(url: str) -> UrlCheckResult:
    """Check whether a URL is reachable via HTTP HEAD (GET fallback on 405).

    - Non-HTTP URLs (ftp://, etc.) return reachable=False immediately.
    - HTTP HEAD request with 10s timeout.
    - If HEAD returns 405, falls back to GET.
    - 2xx/3xx = reachable, 4xx/5xx = unreachable.
    - Connection errors / timeouts return status=0, reachable=False.
    """
    # Reject non-HTTP schemes
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        return UrlCheckResult(
            url=url,
            status=0,
            reachable=False,
            reason=f"Unsupported scheme {parsed.scheme!r}: only http/https supported",
        )

    # Try HEAD first
    try:
        req = Request(url, method="HEAD", headers=_HEADERS)
        resp = urlopen(req, timeout=_TIMEOUT)
        status = resp.status
    except HTTPError as exc:
        if exc.code == 405:
            # HEAD not allowed — fall back to GET
            return _try_get(url)
        return UrlCheckResult(
            url=url,
            status=exc.code,
            reachable=False,
            reason=f"HTTP {exc.code}",
        )
    except URLError as exc:
        return UrlCheckResult(
            url=url, status=0, reachable=False, reason=str(exc.reason)
        )
    except Exception as exc:
        return UrlCheckResult(
            url=url, status=0, reachable=False, reason=str(exc)
        )

    # 2xx and 3xx are reachable (urllib follows redirects, so we mostly see 2xx)
    if 200 <= status < 400:
        return UrlCheckResult(url=url, status=status, reachable=True)

    return UrlCheckResult(
        url=url,
        status=status,
        reachable=False,
        reason=f"HTTP {status}",
    )


def _try_get(url: str) -> UrlCheckResult:
    """Fallback GET request when HEAD returns 405."""
    try:
        req = Request(url, headers=_HEADERS)
        resp = urlopen(req, timeout=_TIMEOUT)
        status = resp.status
    except HTTPError as exc:
        return UrlCheckResult(
            url=url,
            status=exc.code,
            reachable=False,
            reason=f"HTTP {exc.code}",
        )
    except (URLError, Exception) as exc:
        reason = str(exc.reason) if hasattr(exc, "reason") else str(exc)
        return UrlCheckResult(
            url=url, status=0, reachable=False, reason=reason
        )

    if 200 <= status < 400:
        return UrlCheckResult(url=url, status=status, reachable=True)

    return UrlCheckResult(
        url=url, status=status, reachable=False, reason=f"HTTP {status}",
    )


def check_urls(urls: list) -> list:
    """Check multiple URLs for reachability, deduplicating.

    Each unique URL is checked only once. Returns one UrlCheckResult
    per unique URL. Empty input returns an empty list.
    """
    if not urls:
        return []

    seen: set = set()
    results: list = []
    for url in urls:
        if url in seen:
            continue
        seen.add(url)
        results.append(check_url(url))
    return results
