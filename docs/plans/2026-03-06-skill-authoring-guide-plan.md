# Skill Authoring Guide Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Extend `/wos:audit` with deterministic skill quality checks in Python and a reference file that serves as both the skill authoring guide and the judgment rubric.

**Architecture:** Add a `check_skill_meta()` function to `skill_audit.py` that validates SKILL.md frontmatter fields (name format, description length, voice heuristics). Add `skill-authoring-guide.md` as a reference to the audit skill. Update audit SKILL.md with a skill evaluation section.

**Tech Stack:** Python 3.9 (stdlib only), pytest, markdown

---

### Task 1: Parse skill frontmatter metadata

The existing `skill_audit.py` strips frontmatter but doesn't parse it. We need to extract `name` and `description` values for validation. SKILL.md files use YAML `>` block scalars for multi-line descriptions, which `frontmatter.py` doesn't handle. Add a focused helper.

**Files:**
- Modify: `wos/skill_audit.py`
- Test: `tests/test_skill_audit.py`

**Step 1: Write the failing tests**

Add to `tests/test_skill_audit.py`:

```python
class TestParseSkillMeta:
    def test_extracts_name_and_description(self) -> None:
        from wos.skill_audit import parse_skill_meta

        text = "---\nname: my-skill\ndescription: Does something useful\n---\n# Body\n"
        meta = parse_skill_meta(text)
        assert meta["name"] == "my-skill"
        assert meta["description"] == "Does something useful"

    def test_multiline_description_with_fold(self) -> None:
        from wos.skill_audit import parse_skill_meta

        text = (
            "---\n"
            "name: my-skill\n"
            "description: >\n"
            "  First line of description\n"
            "  second line of description.\n"
            "argument-hint: something\n"
            "---\n"
            "# Body\n"
        )
        meta = parse_skill_meta(text)
        assert meta["name"] == "my-skill"
        assert "First line" in meta["description"]
        assert "second line" in meta["description"]

    def test_missing_name_returns_none(self) -> None:
        from wos.skill_audit import parse_skill_meta

        text = "---\ndescription: Does something\n---\n# Body\n"
        meta = parse_skill_meta(text)
        assert meta["name"] is None

    def test_missing_description_returns_none(self) -> None:
        from wos.skill_audit import parse_skill_meta

        text = "---\nname: my-skill\n---\n# Body\n"
        meta = parse_skill_meta(text)
        assert meta["description"] is None

    def test_no_frontmatter_returns_nones(self) -> None:
        from wos.skill_audit import parse_skill_meta

        text = "# Just a body\n"
        meta = parse_skill_meta(text)
        assert meta["name"] is None
        assert meta["description"] is None
```

**Step 2: Run tests to verify they fail**

Run: `uv run python -m pytest tests/test_skill_audit.py::TestParseSkillMeta -v`
Expected: FAIL — `ImportError: cannot import name 'parse_skill_meta'`

**Step 3: Implement `parse_skill_meta`**

Add to `wos/skill_audit.py`:

```python
import re

def parse_skill_meta(text: str) -> dict:
    """Extract name and description from SKILL.md frontmatter.

    Handles YAML ``>`` block scalars for multi-line descriptions.
    Returns dict with ``name`` and ``description`` keys (None if absent).
    """
    if not text.startswith("---"):
        return {"name": None, "description": None}

    close = text.find("\n---", 3)
    if close == -1:
        return {"name": None, "description": None}

    yaml_text = text[4:close]

    name = None
    description = None

    name_match = re.search(r"^name:\s*(.+)$", yaml_text, re.MULTILINE)
    if name_match:
        name = name_match.group(1).strip().strip('"').strip("'")

    desc_match = re.search(r"^description:\s*(.*)$", yaml_text, re.MULTILINE)
    if desc_match:
        value = desc_match.group(1).strip()
        if value in (">", "|", ">-", "|-"):
            # Collect indented continuation lines
            lines = yaml_text.split("\n")
            desc_parts = []
            capture = False
            for line in lines:
                if line.strip().startswith("description:"):
                    capture = True
                    continue
                if capture:
                    if line.startswith("  ") or line.startswith("\t"):
                        desc_parts.append(line.strip())
                    else:
                        break
            description = " ".join(desc_parts)
        else:
            description = value.strip('"').strip("'")

    return {"name": name, "description": description}
```

**Step 4: Run tests to verify they pass**

Run: `uv run python -m pytest tests/test_skill_audit.py::TestParseSkillMeta -v`
Expected: PASS (all 5 tests)

**Step 5: Commit**

```bash
git add wos/skill_audit.py tests/test_skill_audit.py
git commit -m "feat: add parse_skill_meta for SKILL.md frontmatter extraction"
```

---

### Task 2: Add `check_skill_meta()` with deterministic checks

**Files:**
- Modify: `wos/skill_audit.py`
- Test: `tests/test_skill_audit.py`

**Step 1: Write the failing tests**

Add to `tests/test_skill_audit.py`:

```python
class TestCheckSkillMeta:
    def test_valid_skill_no_issues(self, tmp_path: Path) -> None:
        from wos.skill_audit import check_skill_meta

        _create_skill(
            tmp_path, "good-skill",
            "---\nname: good-skill\n"
            "description: Performs good actions. Use when the user asks for good things.\n"
            "---\n# Good Skill\n\n- Do good\n",
        )
        issues = check_skill_meta(tmp_path / "good-skill")
        assert len(issues) == 0

    def test_name_uppercase_fails(self, tmp_path: Path) -> None:
        from wos.skill_audit import check_skill_meta

        _create_skill(
            tmp_path, "BadName",
            "---\nname: BadName\ndescription: Valid description here.\n---\n# X\n",
        )
        issues = check_skill_meta(tmp_path / "BadName")
        assert any("lowercase" in i["issue"] for i in issues)
        assert any(i["severity"] == "fail" for i in issues)

    def test_name_too_long_fails(self, tmp_path: Path) -> None:
        from wos.skill_audit import check_skill_meta

        long_name = "a" * 65
        _create_skill(
            tmp_path, long_name,
            f"---\nname: {long_name}\ndescription: Valid.\n---\n# X\n",
        )
        issues = check_skill_meta(tmp_path / long_name)
        assert any("64 characters" in i["issue"] for i in issues)

    def test_name_reserved_word_fails(self, tmp_path: Path) -> None:
        from wos.skill_audit import check_skill_meta

        _create_skill(
            tmp_path, "claude-helper",
            "---\nname: claude-helper\ndescription: Valid.\n---\n# X\n",
        )
        issues = check_skill_meta(tmp_path / "claude-helper")
        assert any("reserved" in i["issue"] for i in issues)

    def test_description_too_long_warns(self, tmp_path: Path) -> None:
        from wos.skill_audit import check_skill_meta

        long_desc = "x " * 600  # > 1024 chars
        _create_skill(
            tmp_path, "verbose",
            f"---\nname: verbose\ndescription: {long_desc}\n---\n# X\n",
        )
        issues = check_skill_meta(tmp_path / "verbose")
        assert any("1024" in i["issue"] for i in issues)
        assert any(i["severity"] == "warn" for i in issues)

    def test_description_xml_tags_warns(self, tmp_path: Path) -> None:
        from wos.skill_audit import check_skill_meta

        _create_skill(
            tmp_path, "xml-desc",
            "---\nname: xml-desc\ndescription: Use <b>bold</b> text.\n---\n# X\n",
        )
        issues = check_skill_meta(tmp_path / "xml-desc")
        assert any("XML" in i["issue"] for i in issues)

    def test_description_second_person_warns(self, tmp_path: Path) -> None:
        from wos.skill_audit import check_skill_meta

        _create_skill(
            tmp_path, "voice",
            "---\nname: voice\n"
            "description: You can use this to process files.\n"
            "---\n# X\n",
        )
        issues = check_skill_meta(tmp_path / "voice")
        assert any("third person" in i["issue"].lower() for i in issues)

    def test_raw_line_count_over_500_warns(self, tmp_path: Path) -> None:
        from wos.skill_audit import check_skill_meta

        lines = "\n".join(f"line {i}" for i in range(510))
        _create_skill(
            tmp_path, "long-skill",
            f"---\nname: long-skill\ndescription: Valid skill.\n---\n{lines}\n",
        )
        issues = check_skill_meta(tmp_path / "long-skill")
        assert any("500" in i["issue"] for i in issues)

    def test_no_skill_md_returns_empty(self, tmp_path: Path) -> None:
        from wos.skill_audit import check_skill_meta

        (tmp_path / "empty-dir").mkdir()
        issues = check_skill_meta(tmp_path / "empty-dir")
        assert issues == []
```

**Step 2: Run tests to verify they fail**

Run: `uv run python -m pytest tests/test_skill_audit.py::TestCheckSkillMeta -v`
Expected: FAIL — `ImportError: cannot import name 'check_skill_meta'`

**Step 3: Implement `check_skill_meta`**

Add to `wos/skill_audit.py`:

```python
_NAME_RE = re.compile(r"^[a-z0-9-]+$")
_XML_TAG_RE = re.compile(r"<[a-zA-Z]")
_RESERVED_WORDS = ("anthropic", "claude")
_SECOND_PERSON_PATTERNS = (
    "you can",
    "you should",
    "you will",
    "your ",
    "i can",
    "i will",
    "this skill should be used when",
)


def check_skill_meta(skill_dir: Path) -> List[dict]:
    """Validate SKILL.md frontmatter and structure conventions.

    Returns a list of issues in standard validator format.
    """
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return []

    raw = skill_md.read_text(encoding="utf-8")
    meta = parse_skill_meta(raw)
    file_str = str(skill_md)
    issues: List[dict] = []

    # Name checks
    name = meta.get("name")
    if name:
        if not _NAME_RE.match(name):
            issues.append({
                "file": file_str,
                "issue": f"skill name '{name}' must be lowercase letters, numbers, and hyphens only",
                "severity": "fail",
            })
        if len(name) > 64:
            issues.append({
                "file": file_str,
                "issue": f"skill name exceeds 64 characters ({len(name)})",
                "severity": "fail",
            })
        for word in _RESERVED_WORDS:
            if word in name:
                issues.append({
                    "file": file_str,
                    "issue": f"skill name contains reserved word '{word}'",
                    "severity": "fail",
                })

    # Description checks
    desc = meta.get("description")
    if desc:
        if len(desc) > 1024:
            issues.append({
                "file": file_str,
                "issue": f"skill description exceeds 1024 characters ({len(desc)})",
                "severity": "warn",
            })
        if _XML_TAG_RE.search(desc):
            issues.append({
                "file": file_str,
                "issue": "skill description contains XML tags",
                "severity": "warn",
            })
        desc_lower = desc.lower()
        for pattern in _SECOND_PERSON_PATTERNS:
            if pattern in desc_lower:
                issues.append({
                    "file": file_str,
                    "issue": (
                        f"skill description may not use third person "
                        f"(found '{pattern}')"
                    ),
                    "severity": "warn",
                })
                break

    # Raw line count
    body = strip_frontmatter(raw)
    raw_lines = sum(1 for line in body.splitlines() if line.strip())
    if raw_lines > 500:
        issues.append({
            "file": file_str,
            "issue": f"SKILL.md body exceeds 500 non-blank lines ({raw_lines})",
            "severity": "warn",
        })

    return issues
```

**Step 4: Run tests to verify they pass**

Run: `uv run python -m pytest tests/test_skill_audit.py::TestCheckSkillMeta -v`
Expected: PASS (all 9 tests)

**Step 5: Run full test suite**

Run: `uv run python -m pytest tests/ -v -q`
Expected: All 230+ tests pass

**Step 6: Commit**

```bash
git add wos/skill_audit.py tests/test_skill_audit.py
git commit -m "feat: add check_skill_meta with 7 deterministic skill quality checks

Validates SKILL.md frontmatter against Anthropic conventions:
- name: lowercase+hyphens, ≤64 chars, no reserved words
- description: ≤1024 chars, no XML tags, third-person heuristic
- body: ≤500 non-blank lines"
```

---

### Task 3: Wire `check_skill_meta` into audit.py

**Files:**
- Modify: `scripts/audit.py:143-168`

**Step 1: Add check_skill_meta call after existing skill density check**

In `scripts/audit.py`, after the `check_skill_sizes` block (line 151), add:

```python
        from wos.skill_audit import check_skill_meta

        for entry in sorted(skills_dir.iterdir()):
            if not entry.is_dir() or entry.name.startswith("_"):
                continue
            if (entry / "SKILL.md").exists():
                issues.extend(check_skill_meta(entry))
```

**Step 2: Verify by running audit against the project**

Run: `uv run scripts/audit.py --root . --no-urls`
Expected: No new failures on existing WOS skills (all names/descriptions comply)

**Step 3: Run full test suite**

Run: `uv run python -m pytest tests/ -v -q`
Expected: All tests pass

**Step 4: Commit**

```bash
git add scripts/audit.py
git commit -m "feat: wire check_skill_meta into audit.py

Skill meta checks run automatically during project-wide audit
when a skills/ directory exists."
```

---

### Task 4: Write the skill authoring guide

This is the single source of truth — the reference file that teaches humans how to write skills AND provides the rubric for Claude's judgment checks.

**Files:**
- Create: `skills/audit/references/skill-authoring-guide.md`

**Step 1: Write the guide**

```markdown
# Skill Authoring Guide

How to write effective skills for Claude Code. This guide covers
structure, conventions, and quality criteria. It also serves as the
rubric when `/wos:audit` evaluates skill quality.

## The Loading Model

Skills load progressively in three levels:

| Level | When Loaded | Token Cost | Content |
|-------|------------|------------|---------|
| L1: Metadata | Always (startup) | ~100 tokens | `name` + `description` from frontmatter |
| L2: Instructions | When triggered | <5K tokens | SKILL.md body |
| L3: Resources | As needed | Unbounded | Reference files, scripts, assets |

Only L1 is always in context. L2 loads when Claude decides the skill
is relevant — based entirely on the description. L3 loads only when
SKILL.md references a file and the task needs it.

## Required Frontmatter

Every SKILL.md starts with YAML frontmatter:

```yaml
---
name: my-skill-name
description: >
  Performs specific actions on target artifacts. Use when the user
  wants to "do X", "run Y", or "check Z".
argument-hint: "[optional hint for slash command input]"
user-invocable: true
references:
  - references/detailed-guide.md
  - ../_shared/references/preflight.md
---
```

### `name` (required)

- Lowercase letters, numbers, and hyphens only
- Maximum 64 characters
- Cannot contain "anthropic" or "claude"
- Should describe the action, not the target: `audit` not `audit-documents`

### `description` (required)

The most important field. Claude uses it to decide whether to load
the skill from 100+ available skills. Must include:

1. **What** the skill does (lead with this)
2. **When** to use it (trigger phrases)

Conventions:
- Third person voice: "Converts research into..." not "You can use this to..."
- Maximum 1024 characters
- No XML tags
- Be specific — vague descriptions prevent discovery

**Good:**
```yaml
description: >
  Converts research artifacts into focused context documents. Use when
  the user wants to "distill research", "extract findings", or "create
  context from research".
```

**Bad:**
```yaml
description: Helps with documents
```

## SKILL.md Body

The body contains instructions Claude follows when the skill triggers.

### Size Limits

- **≤500 non-blank lines** in SKILL.md body
- **≤200 instruction lines** across SKILL.md + all references (configurable)
- If approaching either limit, split content into reference files

### Writing Style

- **Imperative voice:** "Read the document" not "The document should be read"
- **Consistent terminology:** Pick one term and use it throughout
- **No time-sensitive information**

### The Conciseness Test

For every instruction, ask: "Does Claude already know this?" Claude is
a highly capable model — only add context it doesn't have. A paragraph
explaining what PDFs are wastes tokens. A line showing which library to
use earns its place.

### Freedom Matches Fragility

Match instruction specificity to how fragile the operation is:

| Fragility | Freedom | Example |
|-----------|---------|---------|
| High (exact sequence matters) | Low — exact commands | Database migrations, phase gates |
| Medium (preferred pattern) | Medium — pseudocode | Report generation with parameters |
| Low (many valid approaches) | High — general guidance | Code review, analysis |

## Reference Files

Additional files in `references/` that SKILL.md links to:

- **One level deep from SKILL.md** — Claude may partially read nested
  references. Never reference a file from another reference file.
- **Table of contents** for files >100 lines
- **Domain-organized** — split by topic, not by arbitrary size cuts
- File names should describe content: `source-evaluation.md` not `ref2.md`

## Examples Beat Explanations

One concrete example often replaces a paragraph of description. When
steering output format or depth, show an input/output pair rather than
describing the expected result.

Use `<example>` tags for examples in skill instructions. 3-5 diverse
examples is the sweet spot for output-sensitive skills.

## Canonical Example: `distill`

The `distill` skill demonstrates these conventions well:

**Frontmatter:** Third-person description with trigger phrases, 63
instruction lines total (well under threshold).

**Body:** 5 sequential workflow phases, each 3-6 lines. High-freedom
for judgment calls (what to distill), low-freedom for integration
steps (exact `uv run` commands).

**Reference:** One file (`distillation-guidelines.md`) at 41 lines,
covering splitting heuristics and word count rationale.

**What makes it effective:**
- Every instruction earns its tokens — no explaining what "distill" means
- Freedom varies: user controls granularity (high), but integration
  runs exact commands (low)
- Concise constraints section uses bold keywords for scannability

## Evaluation Criteria

When evaluating a skill, check these criteria:

### Automated (Python — checked by `audit.py`)

| Check | Severity | Standard |
|-------|----------|----------|
| `name` format | fail | lowercase, hyphens, ≤64 chars |
| `name` reserved words | fail | no "anthropic" or "claude" |
| `description` length | warn | ≤1024 characters |
| `description` XML tags | warn | none present |
| `description` voice | warn | third person (no "you can", "I can") |
| SKILL.md body size | warn | ≤500 non-blank lines |
| Instruction density | warn | ≤200 instruction lines (configurable) |

### Judgment (Claude — guided by this document)

| Check | What to evaluate |
|-------|-----------------|
| Description triggers | Does it include both what + when? |
| Freedom ↔ fragility | Do guardrail vs. guidance levels match the task? |
| Unnecessary context | Does the skill explain things Claude already knows? |
| Examples quality | Are examples concrete and demonstrate expected depth? |
| Terminology consistency | Is vocabulary consistent throughout? |
| Reference depth | Are all references one level deep from SKILL.md? |
```

**Step 2: Verify word count is reasonable**

Run: `wc -w skills/audit/references/skill-authoring-guide.md`
Expected: ~700-800 words

**Step 3: Commit**

```bash
git add skills/audit/references/skill-authoring-guide.md
git commit -m "docs: add skill authoring guide as audit reference

Single source of truth for skill quality — teaches humans how to
write skills and provides the rubric for audit evaluation.

Closes #128"
```

---

### Task 5: Update audit SKILL.md with skill evaluation section

**Files:**
- Modify: `skills/audit/SKILL.md`

**Step 1: Add skill evaluation section and reference**

Add `skill-authoring-guide.md` to the references list in frontmatter:

```yaml
references:
  - ../_shared/references/preflight.md
  - references/skill-authoring-guide.md
```

Add a new section after "## Cleanup Actions":

```markdown
## Skill Evaluation

When audit encounters a skill directory (a directory containing `SKILL.md`),
it runs two layers of checks:

1. **Automated checks** (Python) — name format, description length/voice,
   body size, instruction density. These appear in the standard issue table.

2. **Judgment checks** (guided by this section) — evaluate the skill against
   the criteria in [skill-authoring-guide.md](references/skill-authoring-guide.md).

For judgment checks, read the target skill's SKILL.md and references, then
evaluate against the "Judgment" criteria table in the guide. Report findings
with explanations that reference the relevant guide section.

Present judgment findings as a narrative after the automated results:

```
Skill Evaluation: [skill-name]

- **Description triggers:** [finding + explanation]
- **Freedom ↔ fragility:** [finding + explanation]
- **Unnecessary context:** [finding + explanation]
- **Examples:** [finding + explanation]
- **Terminology:** [finding + explanation]
- **Reference depth:** [finding + explanation]
```

Only report issues — if a criterion passes, omit it.
```

**Step 2: Run audit to verify no issues with updated skill**

Run: `uv run scripts/audit.py --root . --no-urls`
Expected: No new issues from the audit skill itself

**Step 3: Commit**

```bash
git add skills/audit/SKILL.md
git commit -m "feat: add skill evaluation section to audit skill

Audit now performs judgment checks on skill directories using
the skill-authoring-guide.md reference."
```

---

### Task 6: Reindex and final verification

**Files:**
- Regenerate: `docs/plans/_index.md`, `docs/research/_index.md`

**Step 1: Reindex**

Run: `uv run scripts/reindex.py --root .`

**Step 2: Run full audit**

Run: `uv run scripts/audit.py --root . --no-urls`
Expected: Only the known research skill density warning

**Step 3: Run full test suite**

Run: `uv run python -m pytest tests/ -v -q`
Expected: All tests pass

**Step 4: Commit any index changes**

```bash
git add docs/ && git commit -m "chore: reindex after skill authoring guide additions"
```

---

### Task 7: Update CLAUDE.md validation check count

**Files:**
- Modify: `CLAUDE.md`

**Step 1: Update the validation checks section**

The "Validation (8 checks)" section in CLAUDE.md should reflect the new
skill meta checks. Update check #8 description to include the new checks:

Change the skill density entry to:
```
8. **Skill quality** (fail + warn) — skill name format/reserved words (fail), description length/XML/voice (warn), instruction lines exceeding threshold (warn, default 200, configurable), SKILL.md body exceeding 500 lines (warn)
```

**Step 2: Commit**

```bash
git add CLAUDE.md
git commit -m "docs: update CLAUDE.md skill validation check description"
```
