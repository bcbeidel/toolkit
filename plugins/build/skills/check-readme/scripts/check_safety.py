#!/usr/bin/env python3
"""Tier-1 README safety checker.

Five orthogonal sub-checks:
  - destructive (FAIL): rm -rf, dd if=, mkfs, DROP DATABASE, --force
    inside a fenced block without a blockquote/bold warning in the
    three lines preceding the fence.
  - pipe-to-shell (FAIL): pipe-to-shell installer patterns (curl/wget
    piped into sh/bash/zsh, or PowerShell `iex (iwr ...)`) without a
    manual-alternative marker in the same H2 section (a second fenced
    block, or prose containing "inspect", "download", "manual", or
    "alternatively").
  - tls-disable (FAIL): instructions to disable TLS / SELinux /
    firewall / certificate verification.
  - non-reserved-hosts (FAIL): hostnames outside reserved TLDs or
    IPs outside reserved ranges, found inside fenced blocks or URL
    contexts.
  - emoji-headings (WARN): emoji code points inside heading text.

Example:
    ./check_safety.py README.md path/to/docs/
"""

from __future__ import annotations

import argparse
import ipaddress
import re
import sys
from pathlib import Path

EXIT_USAGE = 64

_MD_EXTENSIONS = (".md", ".markdown")
_FRONTMATTER_FENCE = "---"

_FENCE_RE = re.compile(r"^(?P<fence>`{3,}|~{3,})")
_HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")

_DESTRUCTIVE_RE = re.compile(
    r"\b(rm\s+-[rRf]{1,2}\S*\s+/"
    r"|dd\s+if="
    r"|mkfs(\.|\s)"
    r"|DROP\s+(DATABASE|TABLE|SCHEMA)"
    r"|--force\b)",
    re.IGNORECASE,
)

_PIPE_TO_SHELL_RES = (
    re.compile(r"\bcurl\s[^|]*\|\s*(sh|bash|zsh)\b"),
    re.compile(r"\bwget\s[^|]*\|\s*(sh|bash|zsh)\b"),
    re.compile(r"\biex\s*\(\s*iwr\s", re.IGNORECASE),
    re.compile(r"\bInvoke-Expression.*Invoke-WebRequest", re.IGNORECASE),
)

_ALT_MARKER_RES = (
    re.compile(r"\binspect\b", re.IGNORECASE),
    re.compile(r"\bdownload\b", re.IGNORECASE),
    re.compile(r"\bmanual\w*\b", re.IGNORECASE),
    re.compile(r"\balternatively\b", re.IGNORECASE),
    re.compile(r"\bverify\b", re.IGNORECASE),
)

_TLS_DISABLE_RES = (
    re.compile(r"\bcurl\b[^#\n]*\s(-k|--insecure)\b"),
    re.compile(r"\bwget\b[^#\n]*\s--no-check-certificate\b"),
    re.compile(r"\b(verify|check_hostname)\s*=\s*False\b"),
    re.compile(r"\bSSL_VERIFY\s*=\s*False\b", re.IGNORECASE),
    re.compile(r"\bsetenforce\s+0\b"),
    re.compile(r"\bufw\s+disable\b"),
    re.compile(r"\biptables\s+-F\b"),
    re.compile(r"\bfirewall-cmd\s+--reload.*--permanent.*--zone=trusted"),
    re.compile(r"\bNODE_TLS_REJECT_UNAUTHORIZED\s*=\s*['\"]?0", re.IGNORECASE),
)

_URL_RE = re.compile(r"https?://(?P<host>[A-Za-z0-9.-]+)")
_IPV4_RE = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")

_RESERVED_TLDS = (".test", ".local", ".example", ".invalid", ".localhost")
_RESERVED_HOSTS = (
    "example.com",
    "example.org",
    "example.net",
    "localhost",
)

_RESERVED_V4_NETS = tuple(
    ipaddress.ip_network(cidr)
    for cidr in (
        "127.0.0.0/8",
        "10.0.0.0/8",
        "172.16.0.0/12",
        "192.168.0.0/16",
        "192.0.2.0/24",
        "198.51.100.0/24",
        "203.0.113.0/24",
        "0.0.0.0/32",
        "255.255.255.255/32",
    )
)

_EMOJI_RANGES = (
    (0x1F300, 0x1F9FF),
    (0x2600, 0x26FF),
    (0x2700, 0x27BF),
    (0x1FA70, 0x1FAFF),
)


class _UsageError(Exception):
    pass


def _is_markdown(path: Path) -> bool:
    return path.suffix.lower() in _MD_EXTENSIONS


def _collect_targets(paths: list[Path]) -> list[Path]:
    files: list[Path] = []
    for target in paths:
        if target.is_file():
            if _is_markdown(target):
                files.append(target)
        elif target.is_dir():
            for child in sorted(target.iterdir()):
                if child.is_file() and _is_markdown(child):
                    files.append(child)
        else:
            print(f"check_safety.py: path not found: {target}", file=sys.stderr)
            raise _UsageError
    return files


def _emit(
    severity: str,
    path: Path,
    check: str,
    message: str,
    recommendation: str,
) -> None:
    print(f"{severity}  {path} — {check}: {message}")
    print(f"  Recommendation: {recommendation}.")


def _strip_frontmatter(lines: list[str]) -> list[str]:
    if not lines or lines[0].strip() != _FRONTMATTER_FENCE:
        return lines
    for idx in range(1, len(lines)):
        if lines[idx].strip() == _FRONTMATTER_FENCE:
            return [""] * (idx + 1) + lines[idx + 1 :]
    return lines


def _parse_blocks(lines: list[str]) -> list[dict]:
    """Return a list of dicts, one per fenced block: lineno, end,
    language, content, section_lines (lines inside the same H2
    section the block belongs to)."""
    blocks: list[dict] = []
    fences: list[dict] = []
    in_fence = False
    fence_marker: str | None = None
    current: dict | None = None
    for lineno, line in enumerate(lines, 1):
        m = _FENCE_RE.match(line)
        if m:
            if not in_fence:
                in_fence = True
                fence_marker = m.group("fence")
                current = {
                    "start": lineno,
                    "content": [],
                    "lang": line[len(fence_marker or "") :].strip().lower(),
                }
            elif line.startswith(fence_marker or ""):
                in_fence = False
                if current is not None:
                    current["end"] = lineno
                    fences.append(current)
                    current = None
                fence_marker = None
            continue
        if in_fence and current is not None:
            current["content"].append((lineno, line))
    blocks.extend(fences)
    return blocks


def _section_bounds(lines: list[str], lineno: int) -> tuple[int, int]:
    """Return (start, end) line numbers (1-indexed) of the H2 section
    containing `lineno`."""
    start = 1
    end = len(lines)
    for idx, line in enumerate(lines, 1):
        m = _HEADING_RE.match(line)
        if not m:
            continue
        if len(m.group(1)) == 2:
            if idx <= lineno:
                start = idx
            else:
                end = idx - 1
                break
    return start, end


def _has_warning_callout(lines: list[str], fence_start: int) -> bool:
    window = lines[max(0, fence_start - 4) : fence_start - 1]
    for line in window:
        stripped = line.strip()
        if stripped.startswith(">"):
            return True
        if "**warning**" in stripped.lower() or "**danger**" in stripped.lower():
            return True
        if "⚠" in stripped:
            return True
    return False


def _check_destructive(path: Path, lines: list[str], blocks: list[dict]) -> bool:
    any_fail = False
    for block in blocks:
        flagged = False
        for lineno, line in block["content"]:
            if _DESTRUCTIVE_RE.search(line):
                if not _has_warning_callout(lines, block["start"]):
                    _emit(
                        "FAIL",
                        path,
                        "destructive",
                        f"destructive command at line {lineno} in fence "
                        f"starting {block['start']} has no preceding warning",
                        "Add a `> ⚠ **Warning:** ...` blockquote or bold "
                        "callout immediately before the fence",
                    )
                    any_fail = True
                    flagged = True
                    break
        if flagged:
            continue
    return any_fail


def _check_pipe_to_shell(path: Path, lines: list[str], blocks: list[dict]) -> bool:
    any_fail = False
    for block in blocks:
        matched_line: int | None = None
        for lineno, line in block["content"]:
            if any(r.search(line) for r in _PIPE_TO_SHELL_RES):
                matched_line = lineno
                break
        if matched_line is None:
            continue
        sec_start, sec_end = _section_bounds(lines, block["start"])
        section_text = "\n".join(lines[sec_start - 1 : sec_end])
        block_content_joined = "\n".join(ln for _, ln in block["content"])
        section_minus_this_block = section_text.replace(block_content_joined, "")
        has_alt = any(r.search(section_minus_this_block) for r in _ALT_MARKER_RES)
        has_second_fence = (
            sum(1 for b in blocks if sec_start <= b["start"] <= sec_end) > 1
        )
        if not has_alt and not has_second_fence:
            _emit(
                "FAIL",
                path,
                "pipe-to-shell",
                f"line {matched_line}: pipe-to-shell installer with no manual "
                "alternative in the same section",
                "Add a second fenced block showing `download → inspect → run` "
                "or prose naming the manual path",
            )
            any_fail = True
    return any_fail


def _check_tls_disable(path: Path, lines: list[str]) -> bool:
    any_fail = False
    for lineno, line in enumerate(lines, 1):
        for pattern in _TLS_DISABLE_RES:
            if pattern.search(line):
                _emit(
                    "FAIL",
                    path,
                    "tls-disable",
                    f"line {lineno}: instruction weakens TLS / SELinux / "
                    "firewall posture",
                    "Remove the workaround and document the real fix, or file "
                    "a tracking issue",
                )
                any_fail = True
                break
    return any_fail


def _is_reserved_host(host: str) -> bool:
    host = host.lower().rstrip(".")
    if host in _RESERVED_HOSTS:
        return True
    return any(host.endswith(tld) for tld in _RESERVED_TLDS)


def _is_reserved_ipv4(addr: str) -> bool:
    try:
        ip = ipaddress.ip_address(addr)
    except ValueError:
        return False
    return any(ip in net for net in _RESERVED_V4_NETS)


def _check_non_reserved_hosts(path: Path, blocks: list[dict]) -> bool:
    any_fail = False
    emitted: set[str] = set()
    for block in blocks:
        for lineno, line in block["content"]:
            for m in _URL_RE.finditer(line):
                host = m.group("host")
                if _IPV4_RE.fullmatch(host):
                    if not _is_reserved_ipv4(host) and host not in emitted:
                        _emit(
                            "FAIL",
                            path,
                            "non-reserved-hosts",
                            f"line {lineno}: non-reserved IPv4 `{host}` in example",
                            "Swap for a reserved IP: 127.0.0.1, 192.0.2.x, "
                            "198.51.100.x, or 203.0.113.x",
                        )
                        emitted.add(host)
                        any_fail = True
                    continue
                if not _is_reserved_host(host) and host not in emitted:
                    _emit(
                        "FAIL",
                        path,
                        "non-reserved-hosts",
                        f"line {lineno}: non-reserved hostname `{host}` in example",
                        "Swap for a reserved host: example.com, *.test, "
                        "*.local, or *.example",
                    )
                    emitted.add(host)
                    any_fail = True
            for host in _IPV4_RE.findall(line):
                if host in emitted:
                    continue
                if not _is_reserved_ipv4(host):
                    _emit(
                        "FAIL",
                        path,
                        "non-reserved-hosts",
                        f"line {lineno}: non-reserved IPv4 `{host}` in example",
                        "Swap for a reserved IP: 127.0.0.1, 192.0.2.x, "
                        "198.51.100.x, or 203.0.113.x",
                    )
                    emitted.add(host)
                    any_fail = True
    return any_fail


def _has_emoji(text: str) -> bool:
    return any(
        any(start <= ord(ch) <= end for start, end in _EMOJI_RANGES) for ch in text
    )


def _check_emoji_headings(path: Path, lines: list[str]) -> None:
    in_fence = False
    fence_marker: str | None = None
    for lineno, line in enumerate(lines, 1):
        m = _FENCE_RE.match(line)
        if m:
            if not in_fence:
                in_fence = True
                fence_marker = m.group("fence")
            elif line.startswith(fence_marker or ""):
                in_fence = False
                fence_marker = None
            continue
        if in_fence:
            continue
        h = _HEADING_RE.match(line)
        if h and _has_emoji(h.group(2)):
            _emit(
                "WARN",
                path,
                "emoji-headings",
                f"line {lineno}: heading `{h.group(2)}` contains emoji",
                "Remove emoji from headings; anchor slugs and screen readers "
                "rely on plain text",
            )
            return


def _check_file(path: Path) -> bool:
    try:
        raw = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError as err:
        print(f"check_safety.py: cannot read {path}: {err}", file=sys.stderr)
        return False
    lines = _strip_frontmatter(raw)
    blocks = _parse_blocks(lines)
    any_fail = False
    any_fail |= _check_destructive(path, lines, blocks)
    any_fail |= _check_pipe_to_shell(path, lines, blocks)
    any_fail |= _check_tls_disable(path, lines)
    any_fail |= _check_non_reserved_hosts(path, blocks)
    _check_emoji_headings(path, lines)
    return any_fail


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="check_safety.py",
        description="Tier-1 README safety checker (5 sub-checks).",
    )
    parser.add_argument(
        "paths",
        nargs="+",
        type=Path,
        metavar="path",
        help="One or more .md files or directories (non-recursive).",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = get_parser().parse_args(argv)
    any_fail = False
    try:
        files = _collect_targets(args.paths)
        for f in files:
            if _check_file(f):
                any_fail = True
    except _UsageError:
        return EXIT_USAGE
    except KeyboardInterrupt:
        return 130
    return 1 if any_fail else 0


if __name__ == "__main__":
    sys.exit(main())
