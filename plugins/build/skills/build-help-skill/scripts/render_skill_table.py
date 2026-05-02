#!/usr/bin/env python3
"""Render a help-skill's skill-index table from sibling SKILL.md frontmatter.

Walks a plugin's skills/ directory, parses each sibling SKILL.md's YAML
frontmatter (name + description), and emits either a markdown table
suitable for embedding inside a help-skill's managed region, or a JSON
list of {name, description, triggers} entries. The skill named ``help``
is always excluded.

Examples:
    ./render_skill_table.py build
    ./render_skill_table.py --skills-dir plugins/work/skills
    ./render_skill_table.py work --format json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

EXIT_USAGE = 2
EXIT_INTERRUPTED = 130
TRIGGER_WORD_LIMIT = 12

PLUGIN_ROOT = Path(__file__).resolve().parents[3]
PLUGINS_DIR = PLUGIN_ROOT.parent


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Render a help-skill's skill-index table from sibling SKILL.md frontmatter."
        ),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "plugin", nargs="?", help="Plugin name (resolves to plugins/<plugin>/skills/)."
    )
    parser.add_argument(
        "--skills-dir",
        type=Path,
        help="Explicit skills directory; overrides positional plugin.",
    )
    parser.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
        help="Output format.",
    )
    parser.add_argument(
        "--word-limit",
        type=int,
        default=TRIGGER_WORD_LIMIT,
        help="Word cap for the triggers cell.",
    )
    return parser


def resolve_skills_dir(args: argparse.Namespace) -> Path:
    if args.skills_dir:
        return args.skills_dir
    if not args.plugin:
        raise ValueError("either a plugin name or --skills-dir is required")
    return PLUGINS_DIR / args.plugin / "skills"


def parse_frontmatter(text: str) -> dict[str, str]:
    """Parse a minimal subset of YAML frontmatter into a flat str->str dict.

    Handles scalar lines (``name: foo``) and folded/literal block scalars
    (``description: >-`` followed by indented continuation lines). Lists,
    nested mappings, and quoted multi-line strings are out of scope —
    unknown structures are skipped.
    """
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}
    body = text[4:end]
    out: dict[str, str] = {}
    lines = body.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        m = re.match(r"^([A-Za-z][A-Za-z0-9_-]*):\s*(.*)$", line)
        if not m:
            i += 1
            continue
        key, val = m.group(1), m.group(2).strip()
        if val in (">-", ">", "|", "|-"):
            chunks: list[str] = []
            i += 1
            while i < len(lines) and (
                lines[i].startswith("  ") or not lines[i].strip()
            ):
                if lines[i].strip():
                    chunks.append(lines[i].strip())
                i += 1
            out[key] = " ".join(chunks)
            continue
        out[key] = val.strip("\"'")
        i += 1
    return out


def first_n_words(s: str, n: int) -> str:
    words = s.split()
    if len(words) <= n:
        return s.strip()
    return " ".join(words[:n]) + "…"


def collect_siblings(skills_dir: Path, word_limit: int) -> list[dict[str, str]]:
    if not skills_dir.is_dir():
        raise FileNotFoundError(f"skills directory does not exist: {skills_dir}")
    entries: list[dict[str, str]] = []
    for child in sorted(skills_dir.iterdir()):
        if not child.is_dir() or child.name.startswith("_") or child.name == "help":
            continue
        skill_md = child / "SKILL.md"
        if not skill_md.is_file():
            continue
        fm = parse_frontmatter(skill_md.read_text(encoding="utf-8"))
        name = fm.get("name", child.name)
        description = fm.get("description", "")
        entries.append(
            {
                "name": name,
                "description": description,
                "triggers": first_n_words(description, word_limit),
            }
        )
    return entries


def render_markdown(entries: list[dict[str, str]]) -> str:
    lines = ["| Skill | Triggers on |", "|---|---|"]
    for e in entries:
        triggers = e["triggers"].replace("|", "\\|")
        lines.append(f"| `{e['name']}` | {triggers} |")
    return "\n".join(lines) + "\n"


def render_json(entries: list[dict[str, str]]) -> str:
    return json.dumps(entries, indent=2) + "\n"


def run(args: argparse.Namespace) -> int:
    skills_dir = resolve_skills_dir(args)
    entries = collect_siblings(skills_dir, args.word_limit)
    if args.format == "json":
        sys.stdout.write(render_json(entries))
    else:
        sys.stdout.write(render_markdown(entries))
    return 0


def main(argv: list[str] | None = None) -> int:
    args = get_parser().parse_args(argv)
    try:
        return run(args)
    except KeyboardInterrupt:
        return EXIT_INTERRUPTED
    except (FileNotFoundError, ValueError) as err:
        print(f"error: {err}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
