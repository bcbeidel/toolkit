"""Tests for wiki.url_checker — HTTP HEAD/GET URL reachability checks.

All HTTP calls are mocked. No network traffic in tests.
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch
from urllib.error import HTTPError, URLError

from wiki.url_checker import UrlCheckResult, check_url, check_urls

# ── UrlCheckResult dataclass ─────────────────────────────────────


def test_url_check_result_reachable() -> None:
    """UrlCheckResult stores reachable=True with status and no reason."""
    result = UrlCheckResult(url="https://example.com", status=200, reachable=True)
    assert result.url == "https://example.com"
    assert result.status == 200
    assert result.reachable is True
    assert result.reason is None


def test_url_check_result_unreachable_with_reason() -> None:
    """UrlCheckResult stores reachable=False with reason string."""
    result = UrlCheckResult(
        url="https://example.com/missing",
        status=404,
        reachable=False,
        reason="HTTP 404: not found",
    )
    assert result.url == "https://example.com/missing"
    assert result.status == 404
    assert result.reachable is False
    assert result.reason == "HTTP 404: not found"


# ── check_url ────────────────────────────────────────────────────


def _mock_response(status: int = 200) -> MagicMock:
    """Create a mock urllib response with the given status."""
    resp = MagicMock()
    resp.status = status
    resp.__enter__ = MagicMock(return_value=resp)
    resp.__exit__ = MagicMock(return_value=False)
    return resp


@patch("wiki.url_checker.urlopen")
def test_check_url_200_reachable(mock_urlopen: MagicMock) -> None:
    """HTTP 200 response marks URL as reachable."""
    mock_urlopen.return_value = _mock_response(200)
    result = check_url("https://example.com/page")
    assert result.reachable is True
    assert result.status == 200
    assert result.reason is None
    mock_urlopen.assert_called_once()


@patch("wiki.url_checker.urlopen")
def test_check_url_404_unreachable(mock_urlopen: MagicMock) -> None:
    """HTTP 404 response marks URL as unreachable."""
    mock_urlopen.side_effect = HTTPError(
        "https://example.com/missing", 404, "Not Found", {}, None
    )
    result = check_url("https://example.com/missing")
    assert result.reachable is False
    assert result.status == 404
    assert result.reason is not None


@patch("wiki.url_checker.urlopen")
def test_check_url_head_405_falls_back_to_get(mock_urlopen: MagicMock) -> None:
    """HEAD returning 405 triggers a GET fallback."""
    # First call (HEAD) raises 405, second call (GET) succeeds
    mock_urlopen.side_effect = [
        HTTPError("https://example.com/no-head", 405, "Method Not Allowed", {}, None),
        _mock_response(200),
    ]
    result = check_url("https://example.com/no-head")
    assert result.reachable is True
    assert result.status == 200
    assert mock_urlopen.call_count == 2


@patch("wiki.url_checker.urlopen")
def test_check_url_connection_error(mock_urlopen: MagicMock) -> None:
    """Connection error returns status=0, reachable=False."""
    mock_urlopen.side_effect = URLError("DNS resolution failed")
    result = check_url("https://nonexistent.example.com")
    assert result.reachable is False
    assert result.status == 0
    assert result.reason is not None
    assert "DNS resolution failed" in result.reason


@patch("wiki.url_checker.urlopen")
def test_check_url_timeout(mock_urlopen: MagicMock) -> None:
    """Timeout returns status=0, reachable=False."""
    mock_urlopen.side_effect = URLError("timed out")
    result = check_url("https://slow.example.com")
    assert result.reachable is False
    assert result.status == 0
    assert result.reason is not None


def test_check_url_invalid_scheme() -> None:
    """Non-HTTP/HTTPS URLs return reachable=False immediately."""
    result = check_url("ftp://files.example.com/data.csv")
    assert result.reachable is False
    assert result.status == 0
    assert result.reason is not None
    assert "http" in result.reason.lower() or "https" in result.reason.lower()


# ── check_urls (batch) ───────────────────────────────────────────


@patch("wiki.url_checker.urlopen")
def test_check_urls_batch(mock_urlopen: MagicMock) -> None:
    """Batch check returns a result for each unique URL."""
    def side_effect(req, **kwargs):
        url = req.full_url if hasattr(req, 'full_url') else str(req)
        if "good" in url:
            return _mock_response(200)
        raise HTTPError(url, 404, "Not Found", {}, None)

    mock_urlopen.side_effect = side_effect

    results = check_urls([
        "https://example.com/good",
        "https://example.com/missing",
    ])
    assert len(results) == 2
    assert results[0].reachable is True
    assert results[1].reachable is False


def test_check_urls_empty_list() -> None:
    """Empty input returns empty output without any HTTP calls."""
    results = check_urls([])
    assert results == []


@patch("wiki.url_checker.urlopen")
def test_check_urls_deduplicates(mock_urlopen: MagicMock) -> None:
    """Duplicate URLs are checked only once."""
    mock_urlopen.return_value = _mock_response(200)
    results = check_urls([
        "https://example.com/page",
        "https://example.com/page",
        "https://example.com/page",
    ])
    assert len(results) == 1
    assert results[0].url == "https://example.com/page"
    mock_urlopen.assert_called_once()
