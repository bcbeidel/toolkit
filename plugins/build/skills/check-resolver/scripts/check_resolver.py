#!/usr/bin/env python3
"""Deterministic Tier-1 checks for the RESOLVER.md managed region.

Given a target directory, walks up to the nearest ``RESOLVER.md`` and
audits that resolver. The discovered ancestor becomes the resolver
root, and all checks scope to its subtree (not the filesystem repo).

Seven checks per resolver root:

- **markers-present** — both ``<!-- resolver:begin -->`` and
  ``<!-- resolver:end -->`` appear exactly once. FAIL otherwise.
- **filing-paths-resolve** — every Location column value in the filing
  table resolves to a directory on disk. FAIL on miss.
- **context-paths-resolve** — every doc path in the context table's
  "Load first" column resolves to a file or directory on disk. FAIL
  on miss. Directories are valid context entries — the convention
  is to Glob the directory's naming pattern and read frontmatter
  ``description`` to identify the right file.
- **filing-rows-unique** — the filing table's first column (content
  type) has no duplicates. FAIL on duplicate.
- **context-rows-unique** — the context table's first column (task)
  has no duplicates. FAIL on duplicate.
- **dark-capability** — every depth 1–2 directory under the resolver
  root is classified by filing table, context table, out-of-scope
  list, the ambient default set, or a nested ``RESOLVER.md``
  (delegation — that subtree belongs to the nested resolver). WARN
  on any unclassified directory.
- **mtime-stale** — RESOLVER.md mtime older than 90 days. WARN.

Paths containing template placeholders (``<...>``, ``*``) are skipped
by the resolver checks — they are documented templates, not concrete
paths.

Example:
    ./check_resolver.py .
    ./check_resolver.py /path/to/repo-a /path/to/repo-b
"""

from __future__ import annotations

import argparse
import re
import sys
import time
from pathlib import Path

EXIT_USAGE = 2
EXIT_INTERRUPTED = 130

RESOLVER_FILENAME = "RESOLVER.md"
MARKER_BEGIN = "<!-- resolver:begin -->"
MARKER_END = "<!-- resolver:end -->"
SECONDS_PER_DAY = 24 * 60 * 60
STALE_DAYS = 90
STALE_SECONDS = STALE_DAYS * SECONDS_PER_DAY

# Directories ignored by the dark-capability scan regardless of resolver
# contents. Mirrors the ambient list documented in audit-dimensions.md.
# `.resolver` is the resolver's own machinery (siblings to RESOLVER.md).
AMBIENT_BASENAMES = frozenset(
    {
        ".git",
        "node_modules",
        "dist",
        "build",
        ".cache",
        ".venv",
        "target",
        "__pycache__",
        ".resolver",
    }
)

H2_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
TABLE_ROW_RE = re.compile(r"^\s*\|(.+)\|\s*$")
SEPARATOR_ROW_RE = re.compile(r"^\s*\|[\s\-|:]+\|\s*$")
PLACEHOLDER_RE = re.compile(r"[<>*]")
OOS_BULLET_LINE_RE = re.compile(r"^\s*[-*]\s+")
OOS_PATH_RE = re.compile(r"`([^`]+)`")


def emit_fail(path: Path, check: str, detail: str, recommendation: str) -> None:
    print(f"FAIL  {path} — {check}: {detail}")
    print(f"  Recommendation: {recommendation}")


def emit_warn(path: Path, check: str, detail: str, recommendation: str) -> None:
    print(f"WARN  {path} — {check}: {detail}")
    print(f"  Recommendation: {recommendation}")


def extract_managed_region(text: str) -> str | None:
    begin_count = text.count(MARKER_BEGIN)
    end_count = text.count(MARKER_END)
    if begin_count != 1 or end_count != 1:
        return None
    start = text.index(MARKER_BEGIN) + len(MARKER_BEGIN)
    end = text.index(MARKER_END)
    if end <= start:
        return None
    return text[start:end]


def parse_table_cells(row_line: str) -> list[str]:
    match = TABLE_ROW_RE.match(row_line)
    if not match:
        return []
    inner = match.group(1)
    return [cell.strip() for cell in inner.split("|")]


def find_section_table(region: str, section_prefix: str) -> list[list[str]]:
    """Return data rows from the first markdown table inside the named H2 section.

    Matches H2 headings whose text starts with ``section_prefix`` (case-insensitive).
    Returns an empty list when the section or table is absent.
    """
    lines = region.splitlines()
    in_section = False
    table_started = False
    data_rows: list[list[str]] = []
    prefix_lower = section_prefix.lower()

    for line in lines:
        h2_match = H2_RE.match(line)
        if h2_match:
            heading = h2_match.group(1).strip().lower()
            if heading.startswith(prefix_lower):
                in_section = True
                table_started = False
                continue
            if in_section:
                break
            continue
        if not in_section:
            continue
        if TABLE_ROW_RE.match(line):
            if SEPARATOR_ROW_RE.match(line):
                table_started = True
                continue
            if not table_started:
                continue
            cells = parse_table_cells(line)
            if cells:
                data_rows.append(cells)
        elif table_started and not line.strip():
            break
    return data_rows


def strip_backticks(value: str) -> str:
    return value.strip().strip("`").strip()


def extract_paths_from_load_cell(cell: str) -> list[str]:
    """Parse one context-table "Load first" cell into a list of doc paths.

    Accepts three shapes:
      - single backticked path:        `foo/bar.md`
      - backticked comma-separated:    `foo.md`, `bar.md`
      - bracketed comma-separated:     [foo.md, bar.md]
    """
    inner = cell.strip()
    if inner.startswith("[") and inner.endswith("]"):
        inner = inner[1:-1]
    parts = [strip_backticks(p) for p in inner.split(",")]
    return [p for p in parts if p]


def check_markers(resolver_path: Path, text: str) -> bool:
    begin_count = text.count(MARKER_BEGIN)
    end_count = text.count(MARKER_END)
    if begin_count == 1 and end_count == 1:
        return True
    emit_fail(
        resolver_path,
        "markers-present",
        f"expected exactly one {MARKER_BEGIN} and one {MARKER_END}; "
        f"found {begin_count} begin, {end_count} end",
        "Restore the managed-region markers and regenerate via "
        "/build:build-resolver --regenerate",
    )
    return False


def check_filing_table(resolver_path: Path, resolver_root: Path, region: str) -> bool:
    rows = find_section_table(region, "Filing")
    ok = True
    seen_keys: dict[str, int] = {}
    for idx, cells in enumerate(rows, start=1):
        if len(cells) < 2:
            continue
        content_type = strip_backticks(cells[0])
        location = strip_backticks(cells[1])
        if not content_type or not location:
            continue
        if content_type in seen_keys:
            emit_fail(
                resolver_path,
                "filing-rows-unique",
                f"duplicate content-type '{content_type}' "
                f"(rows {seen_keys[content_type]} and {idx})",
                "Merge the duplicates into one row, or rename one content-type",
            )
            ok = False
        else:
            seen_keys[content_type] = idx
        if PLACEHOLDER_RE.search(location):
            continue
        resolved = (resolver_root / location).resolve()
        if not resolved.is_dir():
            emit_fail(
                resolver_path,
                "filing-paths-resolve",
                f"filing location '{location}' "
                f"(content-type '{content_type}') does not resolve to a directory",
                "Create the directory, correct the path, or remove the row",
            )
            ok = False
    return ok


def check_context_table(resolver_path: Path, resolver_root: Path, region: str) -> bool:
    rows = find_section_table(region, "Context")
    ok = True
    seen_tasks: dict[str, int] = {}
    for idx, cells in enumerate(rows, start=1):
        if len(cells) < 2:
            continue
        task = strip_backticks(cells[0])
        load_cell = cells[1]
        if not task or not load_cell.strip():
            continue
        if task in seen_tasks:
            emit_fail(
                resolver_path,
                "context-rows-unique",
                f"duplicate task '{task}' (rows {seen_tasks[task]} and {idx})",
                "Merge the duplicates into one row with a unioned doc list",
            )
            ok = False
        else:
            seen_tasks[task] = idx
        for doc_path in extract_paths_from_load_cell(load_cell):
            if PLACEHOLDER_RE.search(doc_path):
                continue
            resolved = (resolver_root / doc_path).resolve()
            if not resolved.exists():
                emit_fail(
                    resolver_path,
                    "context-paths-resolve",
                    f"context doc '{doc_path}' (task '{task}') "
                    "does not resolve to a file or directory",
                    "Correct the path, or remove the entry from the bundle",
                )
                ok = False
    return ok


def parse_out_of_scope(region: str) -> set[str]:
    """Extract directory paths from the 'Out of scope' bullet list."""
    paths: set[str] = set()
    in_section = False
    for line in region.splitlines():
        h2 = H2_RE.match(line)
        if h2:
            heading = h2.group(1).strip().lower()
            if heading.startswith("out of scope"):
                in_section = True
                continue
            if in_section:
                break
            continue
        if not in_section:
            continue
        if not OOS_BULLET_LINE_RE.match(line):
            continue
        for match in OOS_PATH_RE.finditer(line):
            paths.add(match.group(1).strip().rstrip("/"))
    return paths


def collect_classified(region: str) -> tuple[set[str], set[str], set[str]]:
    """Return (filing_dirs, recursive_dirs, oos_dirs) drawn from the managed region.

    - **filing_dirs**: filing-table locations. Only the directory itself is
      classified — subdirectories beneath a filing dir are *dark* unless
      separately classified, since the filing rule names files directly
      inside.
    - **recursive_dirs**: context-table paths plus the out-of-scope list.
      Descendants are classified — the agent descends into context dirs on
      need and out-of-scope dirs are pruned entirely.
    - **oos_dirs**: out-of-scope subset of recursive_dirs, used to skip
      descent during the depth-2 walk.
    """
    filing_dirs: set[str] = set()
    for cells in find_section_table(region, "Filing"):
        if len(cells) < 2:
            continue
        location = strip_backticks(cells[1]).rstrip("/")
        if location and not PLACEHOLDER_RE.search(location):
            filing_dirs.add(location)
    context_dirs: set[str] = set()
    for cells in find_section_table(region, "Context"):
        if len(cells) < 2:
            continue
        for doc_path in extract_paths_from_load_cell(cells[1]):
            if PLACEHOLDER_RE.search(doc_path):
                continue
            context_dirs.add(doc_path.rstrip("/"))
    oos_dirs = parse_out_of_scope(region)
    recursive_dirs = context_dirs | oos_dirs
    return filing_dirs, recursive_dirs, oos_dirs


def is_classified(rel: str, filing_dirs: set[str], recursive_dirs: set[str]) -> bool:
    if rel in filing_dirs or rel in recursive_dirs:
        return True
    if any(rel.startswith(p + "/") for p in recursive_dirs):
        return True
    rel_prefix = rel + "/"
    return any(p.startswith(rel_prefix) for p in (filing_dirs | recursive_dirs))


def is_under_oos(rel: str, oos: set[str]) -> bool:
    return rel in oos or any(rel.startswith(prefix + "/") for prefix in oos)


def emit_dark(resolver_path: Path, rel: str) -> None:
    emit_warn(
        resolver_path,
        "dark-capability",
        f"directory '{rel}/' not in filing table, context table, or out of scope",
        "Add a filing row, mark out-of-scope, or place a nested "
        "RESOLVER.md inside it; regenerate via "
        "/build:build-resolver --regenerate",
    )


def scan_subdir(
    resolver_path: Path,
    entry: Path,
    rel: str,
    filing_dirs: set[str],
    recursive_dirs: set[str],
) -> bool:
    """Scan one depth-1 directory's children. Returns True if all clean."""
    ok = True
    try:
        children = sorted(entry.iterdir())
    except (OSError, PermissionError):
        return ok
    for sub in children:
        if not sub.is_dir():
            continue
        if sub.name in AMBIENT_BASENAMES:
            continue
        if (sub / RESOLVER_FILENAME).is_file():
            continue
        sub_rel = f"{rel}/{sub.name}"
        if is_classified(sub_rel, filing_dirs, recursive_dirs):
            continue
        emit_dark(resolver_path, sub_rel)
        ok = False
    return ok


def check_dark_capabilities(
    resolver_path: Path, resolver_root: Path, region: str
) -> bool:
    """Walk depth 1–2 directories and warn on any unclassified entry.

    A directory is classified when it appears in the filing table, the
    context table, the out-of-scope list, the ambient basename set, or
    contains a nested ``RESOLVER.md`` (delegation seed for future
    nested-resolver work). Subdirectories of a filing dir are *not*
    auto-classified — the filing rule covers files inside the dir, not
    nested directories.
    """
    filing_dirs, recursive_dirs, oos_dirs = collect_classified(region)
    ok = True
    try:
        depth1 = sorted(resolver_root.iterdir())
    except (OSError, PermissionError) as err:
        print(f"error: cannot list {resolver_root}: {err}", file=sys.stderr)
        return False
    for entry in depth1:
        if not entry.is_dir():
            continue
        name = entry.name
        if name in AMBIENT_BASENAMES:
            continue
        if (entry / RESOLVER_FILENAME).is_file():
            continue
        rel = name
        if not is_classified(rel, filing_dirs, recursive_dirs):
            emit_dark(resolver_path, rel)
            ok = False
            continue
        if is_under_oos(rel, oos_dirs):
            continue
        if not scan_subdir(resolver_path, entry, rel, filing_dirs, recursive_dirs):
            ok = False
    return ok


def check_mtime(resolver_path: Path) -> None:
    age_seconds = time.time() - resolver_path.stat().st_mtime
    if age_seconds > STALE_SECONDS:
        days = int(age_seconds / SECONDS_PER_DAY)
        emit_warn(
            resolver_path,
            "mtime-stale",
            f"RESOLVER.md mtime is {days} days old (threshold {STALE_DAYS})",
            "Run /build:build-resolver --regenerate to refresh "
            "against current disk state",
        )


def find_resolver_root(target: Path) -> Path | None:
    """Walk up from ``target`` returning the nearest dir with RESOLVER.md."""
    current = target.resolve()
    for _ in range(64):
        if (current / RESOLVER_FILENAME).is_file():
            return current
        if current.parent == current:
            return None
        current = current.parent
    return None


def check_target(target: Path) -> bool:
    if not target.is_dir():
        print(f"error: not a directory: {target}", file=sys.stderr)
        raise SystemExit(EXIT_USAGE)
    resolver_root = find_resolver_root(target)
    if resolver_root is None:
        emit_fail(
            target / RESOLVER_FILENAME,
            "markers-present",
            f"no {RESOLVER_FILENAME} found walking up from {target}",
            "Create RESOLVER.md via /build:build-resolver",
        )
        return False
    resolver_path = resolver_root / RESOLVER_FILENAME
    try:
        text = resolver_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as err:
        print(f"error: cannot read {resolver_path}: {err}", file=sys.stderr)
        return False
    ok = True
    if not check_markers(resolver_path, text):
        check_mtime(resolver_path)
        return False
    region = extract_managed_region(text)
    if region is None:
        return False
    if not check_filing_table(resolver_path, resolver_root, region):
        ok = False
    if not check_context_table(resolver_path, resolver_root, region):
        ok = False
    if not check_dark_capabilities(resolver_path, resolver_root, region):
        ok = False
    check_mtime(resolver_path)
    return ok


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Tier-1 deterministic checks for the RESOLVER.md managed region.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "paths",
        nargs="*",
        type=Path,
        default=[Path()],
        help="One or more target directories (defaults to current "
        "directory). Walks up to the nearest RESOLVER.md and audits "
        "that resolver.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = get_parser().parse_args(argv)
    try:
        all_ok = True
        for target in args.paths:
            if not check_target(target):
                all_ok = False
        return 0 if all_ok else 1
    except KeyboardInterrupt:
        return EXIT_INTERRUPTED


if __name__ == "__main__":
    sys.exit(main())
