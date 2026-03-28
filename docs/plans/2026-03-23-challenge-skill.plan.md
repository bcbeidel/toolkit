---
name: Challenge Skill Implementation Plan
description: Step-by-step plan to implement /wos:challenge — Python discovery module, CLI script, SKILL.md, reference docs, and tests
metadata:
  type: plan
  status: complete
  related:
    - docs/designs/2026-03-23-challenge-skill.design.md
---

# /wos:challenge Implementation Plan

<<<<<<< HEAD
> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.
=======
> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.
>>>>>>> origin/main

**Goal:** Implement the `/wos:challenge` skill — a feedback-layer skill that extracts assumptions from LLM output, sanity-checks them against project context and research documents, and proposes corrections for gaps.

**Architecture:** Hybrid skill + Python module. A new `wos/challenge/` subpackage handles deterministic document discovery and keyword-overlap scoring, reusing `wos.discovery.discover_documents()`. A CLI script (`scripts/discover_context.py`) exposes this as JSON. SKILL.md orchestrates the four-phase workflow (extract → search → analyze → propose), with reference docs guiding assumption quality and gap analysis judgment.

**Tech Stack:** Python 3.9 (stdlib only), pytest, Claude Code skill system

**Branch:** `feat/challenge-skill`

---

## File Structure

| Action | Path | Responsibility |
|--------|------|---------------|
| Create | `wos/challenge/__init__.py` | Empty subpackage init |
| Create | `wos/challenge/discover.py` | `discover_related()`, `discover_by_relevance()`, `keyword_score()` |
| Create | `scripts/discover_context.py` | CLI entry point — JSON output of assumption-to-document matches |
| Create | `tests/test_challenge_discover.py` | Unit tests for discovery module |
| Create | `tests/test_discover_context_script.py` | Integration tests for CLI script |
| Create | `skills/challenge/SKILL.md` | Skill definition — four-phase workflow |
| Create | `skills/challenge/references/assumption-quality.md` | Reference: what makes a well-stated assumption |
| Create | `skills/challenge/references/gap-analysis-guide.md` | Reference: how to evaluate alignment/gap/no-coverage |

---

## Task 1: Create `wos/challenge/` subpackage with `keyword_score()`

The scoring function is the foundation. Build and test it first.

**Files:**
- Create: `wos/challenge/__init__.py`
- Create: `wos/challenge/discover.py`
- Create: `tests/test_challenge_discover.py`

<<<<<<< HEAD
- [x] **Step 1: Write the failing test for `keyword_score()`**
=======
- [ ] **Step 1: Write the failing test for `keyword_score()`**
>>>>>>> origin/main

```python
"""Tests for wos/challenge/discover.py."""

from __future__ import annotations


def test_keyword_score_exact_match():
    """Full keyword overlap scores 1.0."""
    from wos.challenge.discover import keyword_score

    score = keyword_score("OAuth authentication", "OAuth Authentication Patterns")
    assert score == 1.0


def test_keyword_score_partial_match():
    """Partial overlap scores between 0 and 1."""
    from wos.challenge.discover import keyword_score

    score = keyword_score("OAuth authentication", "Database connection pooling patterns")
    assert score == 0.0


def test_keyword_score_case_insensitive():
    """Matching is case-insensitive."""
    from wos.challenge.discover import keyword_score

    score = keyword_score("oauth AUTH", "OAuth Authentication")
    assert score == 1.0


def test_keyword_score_empty_assumption():
    """Empty assumption scores 0."""
    from wos.challenge.discover import keyword_score

    assert keyword_score("", "Some document title") == 0.0


def test_keyword_score_filters_short_tokens():
    """Tokens under 3 characters are ignored as stop words."""
    from wos.challenge.discover import keyword_score

    # "is" and "a" should be filtered, only "oauth" matters
    score = keyword_score("is a oauth", "OAuth Patterns")
    assert score > 0.0
```

<<<<<<< HEAD
- [x] **Step 2: Run tests to verify they fail**
=======
- [ ] **Step 2: Run tests to verify they fail**
>>>>>>> origin/main

Run: `python -m pytest tests/test_challenge_discover.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'wos.challenge'`

<<<<<<< HEAD
- [x] **Step 3: Create `__init__.py` and implement `keyword_score()`**
=======
- [ ] **Step 3: Create `__init__.py` and implement `keyword_score()`**
>>>>>>> origin/main

`wos/challenge/__init__.py`:
```python
"""WOS challenge skill support modules."""
```

`wos/challenge/discover.py` (initial — just the scoring function):
```python
"""Assumption-to-document matching for the /wos:challenge skill."""

from __future__ import annotations

from typing import Callable


def keyword_score(assumption: str, text: str) -> float:
    """Score relevance of text to an assumption via keyword overlap.

    Tokenizes both strings, filters tokens under 3 characters, and
    returns the fraction of assumption tokens found in text. Returns 0.0
    if the assumption has no usable tokens.

    This is the default scorer. The interface (assumption, text) -> float
    is swappable for more sophisticated matching later.

    Args:
        assumption: The assumption claim text.
        text: The document text to match against (typically name + description).

    Returns:
        Float between 0.0 and 1.0 inclusive.
    """
    assumption_tokens = {
        t for t in assumption.lower().split() if len(t) >= 3
    }
    if not assumption_tokens:
        return 0.0
    text_tokens = {t for t in text.lower().split() if len(t) >= 3}
    overlap = assumption_tokens & text_tokens
    return len(overlap) / len(assumption_tokens)
```

<<<<<<< HEAD
- [x] **Step 4: Run tests to verify they pass**
=======
- [ ] **Step 4: Run tests to verify they pass**
>>>>>>> origin/main

Run: `python -m pytest tests/test_challenge_discover.py -v`
Expected: All 5 tests PASS

<<<<<<< HEAD
- [x] **Step 5: Commit**
=======
- [ ] **Step 5: Commit**
>>>>>>> origin/main

```bash
git add wos/challenge/__init__.py wos/challenge/discover.py tests/test_challenge_discover.py
git commit -m "feat(challenge): add keyword_score() scoring function with tests"
```

---

## Task 2: Implement `discover_related()`

Parses an artifact's `related` frontmatter and returns parsed documents.

**Files:**
- Modify: `wos/challenge/discover.py`
- Modify: `tests/test_challenge_discover.py`

<<<<<<< HEAD
- [x] **Step 1: Write the failing tests for `discover_related()`**
=======
- [ ] **Step 1: Write the failing tests for `discover_related()`**
>>>>>>> origin/main

Add to `tests/test_challenge_discover.py`:

```python
import os


_ARTIFACT_WITH_RELATED = """\
---
name: Test Artifact
description: An artifact with related docs
related:
  - docs/context/auth.md
  - docs/context/api.md
---

## Content

Some content here.
"""

_RELATED_DOC = """\
---
name: Auth Patterns
description: Authentication patterns for the project
---

## OAuth

We use OAuth for authentication.
"""


def test_discover_related_resolves_paths(tmp_path):
    """discover_related returns parsed Documents for valid related paths."""
    from wos.challenge.discover import discover_related

    # Create artifact
    artifact = tmp_path / "design.md"
    artifact.write_text(_ARTIFACT_WITH_RELATED)

    # Create one related doc (auth.md exists, api.md does not)
    context_dir = tmp_path / "docs" / "context"
    context_dir.mkdir(parents=True)
    (context_dir / "auth.md").write_text(_RELATED_DOC)

    docs = discover_related(str(artifact), str(tmp_path))
    assert len(docs) == 1
    assert docs[0].name == "Auth Patterns"


def test_discover_related_no_related_field(tmp_path):
    """Artifact with no related field returns empty list."""
    from wos.challenge.discover import discover_related

    artifact = tmp_path / "plain.md"
    artifact.write_text("---\nname: Plain\ndescription: No related\n---\n\nContent.\n")

    docs = discover_related(str(artifact), str(tmp_path))
    assert docs == []


def test_discover_related_artifact_not_found():
    """Non-existent artifact returns empty list."""
    from wos.challenge.discover import discover_related

    docs = discover_related("/nonexistent/file.md", "/nonexistent")
    assert docs == []
```

<<<<<<< HEAD
- [x] **Step 2: Run tests to verify they fail**
=======
- [ ] **Step 2: Run tests to verify they fail**
>>>>>>> origin/main

Run: `python -m pytest tests/test_challenge_discover.py::test_discover_related_resolves_paths -v`
Expected: FAIL with `ImportError` (function not defined)

<<<<<<< HEAD
- [x] **Step 3: Implement `discover_related()`**
=======
- [ ] **Step 3: Implement `discover_related()`**
>>>>>>> origin/main

Add to `wos/challenge/discover.py`:

```python
import os
from pathlib import Path
from typing import List, Optional

from wos.document import Document, parse_document


def discover_related(artifact_path: str, project_root: str) -> List[Document]:
    """Parse an artifact's related frontmatter and return linked documents.

    Resolves each path in the ``related`` field relative to project_root.
    Skips paths that don't exist or fail to parse.

    Args:
        artifact_path: Path to the artifact file.
        project_root: Project root for resolving relative paths.

    Returns:
        List of parsed Document instances for valid related paths.
    """
    if not os.path.isfile(artifact_path):
        return []

    with open(artifact_path, encoding="utf-8") as f:
        text = f.read()

    try:
        doc = parse_document(artifact_path, text)
    except ValueError:
        return []

    if not doc.related:
        return []

    results: List[Document] = []
    root = Path(project_root)
    for rel_path in doc.related:
        full = root / rel_path
        if not full.is_file():
            continue
        try:
            related_doc = parse_document(str(rel_path), full.read_text(encoding="utf-8"))
            results.append(related_doc)
        except ValueError:
            continue

    return results
```

<<<<<<< HEAD
- [x] **Step 4: Run tests to verify they pass**
=======
- [ ] **Step 4: Run tests to verify they pass**
>>>>>>> origin/main

Run: `python -m pytest tests/test_challenge_discover.py -v`
Expected: All 8 tests PASS

<<<<<<< HEAD
- [x] **Step 5: Commit**
=======
- [ ] **Step 5: Commit**
>>>>>>> origin/main

```bash
git add wos/challenge/discover.py tests/test_challenge_discover.py
git commit -m "feat(challenge): add discover_related() for explicit layer search"
```

---

## Task 3: Implement `discover_by_relevance()`

Scans all managed documents and scores them against assumptions.

**Files:**
- Modify: `wos/challenge/discover.py`
- Modify: `tests/test_challenge_discover.py`

<<<<<<< HEAD
- [x] **Step 1: Write the failing tests for `discover_by_relevance()`**
=======
- [ ] **Step 1: Write the failing tests for `discover_by_relevance()`**
>>>>>>> origin/main

Add to `tests/test_challenge_discover.py`:

```python
_CONTEXT_AUTH = """\
---
name: Auth Patterns
description: OAuth authentication patterns for the project
---

## OAuth

We use OAuth 2.0 for all authentication.
"""

_CONTEXT_DB = """\
---
name: Database Design
description: PostgreSQL schema conventions and migration patterns
---

## Schema

All tables use UUID primary keys.
"""

_RESEARCH_RATE = """\
---
name: API Rate Limiting
description: Research on rate limiting strategies and thresholds
type: research
sources:
  - https://example.com/rate-limits
---

## Findings

Rate limits should be 500 req/min.
"""


def test_discover_by_relevance_matches_keywords(tmp_path):
    """Assumptions match documents with overlapping keywords."""
    from wos.challenge.discover import discover_by_relevance

    # Create docs directory structure
    ctx = tmp_path / "docs" / "context"
    ctx.mkdir(parents=True)
    (ctx / "auth.md").write_text(_CONTEXT_AUTH)
    (ctx / "db.md").write_text(_CONTEXT_DB)

    res = tmp_path / "docs" / "research"
    res.mkdir(parents=True)
    (res / "rate.md").write_text(_RESEARCH_RATE)

    results = discover_by_relevance(
        ["OAuth authentication is required"],
        str(tmp_path),
    )
    assert "OAuth authentication is required" in results
    matches = results["OAuth authentication is required"]
    # Auth doc should rank highest (has "OAuth" and "authentication")
    assert len(matches) > 0
    assert matches[0].name == "Auth Patterns"


def test_discover_by_relevance_no_matches(tmp_path):
    """Assumption with no keyword overlap returns empty list."""
    from wos.challenge.discover import discover_by_relevance

    ctx = tmp_path / "docs" / "context"
    ctx.mkdir(parents=True)
    (ctx / "db.md").write_text(_CONTEXT_DB)

    results = discover_by_relevance(
        ["Quantum entanglement drives the cache layer"],
        str(tmp_path),
    )
    matches = results["Quantum entanglement drives the cache layer"]
    assert matches == []


def test_discover_by_relevance_multiple_assumptions(tmp_path):
    """Each assumption gets its own match list."""
    from wos.challenge.discover import discover_by_relevance

    ctx = tmp_path / "docs" / "context"
    ctx.mkdir(parents=True)
    (ctx / "auth.md").write_text(_CONTEXT_AUTH)
    (ctx / "db.md").write_text(_CONTEXT_DB)

    results = discover_by_relevance(
        ["OAuth authentication", "PostgreSQL schema design"],
        str(tmp_path),
    )
    assert len(results) == 2
    assert "OAuth authentication" in results
    assert "PostgreSQL schema design" in results
```

<<<<<<< HEAD
- [x] **Step 2: Run tests to verify they fail**
=======
- [ ] **Step 2: Run tests to verify they fail**
>>>>>>> origin/main

Run: `python -m pytest tests/test_challenge_discover.py::test_discover_by_relevance_matches_keywords -v`
Expected: FAIL with `ImportError`

<<<<<<< HEAD
- [x] **Step 3: Implement `discover_by_relevance()`**
=======
- [ ] **Step 3: Implement `discover_by_relevance()`**
>>>>>>> origin/main

Add to `wos/challenge/discover.py`:

```python
from typing import Callable, Dict

from wos.discovery import discover_documents


def discover_by_relevance(
    assumptions: List[str],
    docs_root: str,
    scorer: Callable[[str, str], float] = keyword_score,
) -> Dict[str, List[Document]]:
    """Match assumptions to project documents by relevance scoring.

    Calls ``discover_documents()`` to find all managed documents, then
    scores each document's name + description against each assumption
    using the provided scorer. Returns only documents with score > 0,
    sorted by descending score.

    Args:
        assumptions: List of assumption claim strings.
        docs_root: Project root directory to scan.
        scorer: Callable (assumption, text) -> float. Defaults to
            keyword_score.

    Returns:
        Dict mapping each assumption string to a list of Documents,
        sorted by relevance score (highest first). Documents with
        score 0 are excluded.
    """
    all_docs = discover_documents(Path(docs_root))

    results: Dict[str, List[Document]] = {}
    for assumption in assumptions:
        scored = []
        for doc in all_docs:
            text = f"{doc.name} {doc.description}"
            score = scorer(assumption, text)
            if score > 0:
                scored.append((score, doc))
        scored.sort(key=lambda x: x[0], reverse=True)
        results[assumption] = [doc for _, doc in scored]

    return results
```

<<<<<<< HEAD
- [x] **Step 4: Run tests to verify they pass**
=======
- [ ] **Step 4: Run tests to verify they pass**
>>>>>>> origin/main

Run: `python -m pytest tests/test_challenge_discover.py -v`
Expected: All 11 tests PASS

<<<<<<< HEAD
- [x] **Step 5: Commit**
=======
- [ ] **Step 5: Commit**
>>>>>>> origin/main

```bash
git add wos/challenge/discover.py tests/test_challenge_discover.py
git commit -m "feat(challenge): add discover_by_relevance() for broad layer search"
```

---

## Task 4: Create `scripts/discover_context.py` CLI script

Exposes the discovery module as a JSON CLI tool for SKILL.md invocation.

**Files:**
- Create: `scripts/discover_context.py`
- Create: `tests/test_discover_context_script.py`

<<<<<<< HEAD
- [x] **Step 1: Write the failing integration test**
=======
- [ ] **Step 1: Write the failing integration test**
>>>>>>> origin/main

```python
"""Tests for scripts/discover_context.py CLI."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


_CONTEXT_DOC = """\
---
name: Auth Patterns
description: OAuth authentication patterns for the project
---

## OAuth

We use OAuth 2.0.
"""

_ARTIFACT_DOC = """\
---
name: Design Spec
description: A design document
related:
  - docs/context/auth.md
---

## Design

Uses OAuth.
"""


def test_discover_context_json_output(tmp_path):
    """Script outputs valid JSON with assumption-to-match mapping."""
    ctx = tmp_path / "docs" / "context"
    ctx.mkdir(parents=True)
    (ctx / "auth.md").write_text(_CONTEXT_DOC)

    script = Path(__file__).resolve().parent.parent / "scripts" / "discover_context.py"
    result = subprocess.run(
        [
            sys.executable, str(script),
            "--assumptions", "OAuth authentication",
            "--root", str(tmp_path),
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    data = json.loads(result.stdout)
    assert len(data) == 1
    assert data[0]["assumption"] == "OAuth authentication"
    assert len(data[0]["matches"]) > 0
    assert "score" in data[0]["matches"][0]
    assert "path" in data[0]["matches"][0]
    assert "name" in data[0]["matches"][0]


def test_discover_context_with_artifact(tmp_path):
    """--artifact flag includes explicit layer results."""
    ctx = tmp_path / "docs" / "context"
    ctx.mkdir(parents=True)
    (ctx / "auth.md").write_text(_CONTEXT_DOC)

    artifact = tmp_path / "design.md"
    artifact.write_text(_ARTIFACT_DOC)

    script = Path(__file__).resolve().parent.parent / "scripts" / "discover_context.py"
    result = subprocess.run(
        [
            sys.executable, str(script),
            "--assumptions", "OAuth authentication",
            "--root", str(tmp_path),
            "--artifact", str(artifact),
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    data = json.loads(result.stdout)
    assert len(data) == 1
    # Should have matches from both explicit (related) and broad layers
    assert len(data[0]["matches"]) > 0


def test_discover_context_no_matches(tmp_path):
    """Assumptions with no matches return empty match lists."""
    # Empty docs directory
    (tmp_path / "docs" / "context").mkdir(parents=True)

    script = Path(__file__).resolve().parent.parent / "scripts" / "discover_context.py"
    result = subprocess.run(
        [
            sys.executable, str(script),
            "--assumptions", "Quantum entanglement",
            "--root", str(tmp_path),
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    data = json.loads(result.stdout)
    assert data[0]["matches"] == []
```

<<<<<<< HEAD
- [x] **Step 2: Run tests to verify they fail**
=======
- [ ] **Step 2: Run tests to verify they fail**
>>>>>>> origin/main

Run: `python -m pytest tests/test_discover_context_script.py -v`
Expected: FAIL (script doesn't exist yet)

<<<<<<< HEAD
- [x] **Step 3: Implement `scripts/discover_context.py`**
=======
- [ ] **Step 3: Implement `scripts/discover_context.py`**
>>>>>>> origin/main

```python
#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""Discover context and research documents relevant to a set of assumptions.

Outputs JSON mapping each assumption to ranked document matches.
Used by the /wos:challenge skill during Phase 2 (Layered Search).
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

# Ensure `import wos` works whether pip-installed or run from plugin cache.
_env_root = os.environ.get("CLAUDE_PLUGIN_ROOT", "")
# scripts/ -> plugin root
_plugin_root = (
    Path(_env_root) if _env_root and os.path.isdir(_env_root)
    else Path(__file__).resolve().parent.parent
)
if str(_plugin_root) not in sys.path:
    sys.path.insert(0, str(_plugin_root))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Discover documents relevant to assumptions."
    )
    parser.add_argument(
        "--assumptions",
        nargs="+",
        required=True,
        help="One or more assumption claim strings.",
    )
    parser.add_argument(
        "--root",
        default=".",
        help="Project root directory (default: cwd).",
    )
    parser.add_argument(
        "--artifact",
        default=None,
        help="Path to an artifact file for explicit-layer search.",
    )
    args = parser.parse_args()

    from wos.challenge.discover import (
        discover_by_relevance,
        discover_related,
        keyword_score,
    )

    root = str(Path(args.root).resolve())

    # Broad layer: scan all docs
    broad = discover_by_relevance(args.assumptions, root)

    # Explicit layer: if artifact provided, get related docs
    related_docs = []
    if args.artifact:
        related_docs = discover_related(args.artifact, root)

    # Build output
    output = []
    for assumption in args.assumptions:
        # Merge explicit + broad, dedup by path, explicit first
        seen_paths: set = set()
        matches = []

        # Explicit layer matches: score each related doc against assumption
        for doc in related_docs:
            text = f"{doc.name} {doc.description}"
            score = keyword_score(assumption, text)
            if doc.path not in seen_paths:
                seen_paths.add(doc.path)
                matches.append({
                    "path": doc.path,
                    "name": doc.name,
                    "description": doc.description,
                    "score": round(score, 3),
                    "layer": "explicit",
                })

        # Broad layer matches
        for doc in broad.get(assumption, []):
            if doc.path not in seen_paths:
                seen_paths.add(doc.path)
                text = f"{doc.name} {doc.description}"
                score = keyword_score(assumption, text)
                matches.append({
                    "path": doc.path,
                    "name": doc.name,
                    "description": doc.description,
                    "score": round(score, 3),
                    "layer": "broad",
                })

        # Sort by score descending
        matches.sort(key=lambda m: m["score"], reverse=True)
        output.append({"assumption": assumption, "matches": matches})

    json.dump(output, sys.stdout, indent=2)
    print()  # trailing newline


if __name__ == "__main__":
    main()
```

<<<<<<< HEAD
- [x] **Step 4: Run tests to verify they pass**
=======
- [ ] **Step 4: Run tests to verify they pass**
>>>>>>> origin/main

Run: `python -m pytest tests/test_discover_context_script.py -v`
Expected: All 3 tests PASS

<<<<<<< HEAD
- [x] **Step 5: Commit**
=======
- [ ] **Step 5: Commit**
>>>>>>> origin/main

```bash
git add scripts/discover_context.py tests/test_discover_context_script.py
git commit -m "feat(challenge): add discover_context.py CLI script"
```

---

## Task 5: Create skill reference documents

These guide the LLM's judgment during Phases 1 and 3.

**Files:**
- Create: `skills/challenge/references/assumption-quality.md`
- Create: `skills/challenge/references/gap-analysis-guide.md`

<<<<<<< HEAD
- [x] **Step 1: Create `references/` directory**
=======
- [ ] **Step 1: Create `references/` directory**
>>>>>>> origin/main

```bash
mkdir -p skills/challenge/references
```

<<<<<<< HEAD
- [x] **Step 2: Write `assumption-quality.md`**
=======
- [ ] **Step 2: Write `assumption-quality.md`**
>>>>>>> origin/main

```markdown
# Assumption Quality Guide

## What Makes a Good Assumption

A well-stated assumption is:

1. **Testable** — Can be checked against evidence. "We use OAuth" is testable.
   "The auth is fine" is not.
2. **Specific** — Names concrete things. "Rate limits are 500 req/min" is
   specific. "There are rate limits" is vague.
3. **Non-trivial** — Worth checking. "The code is written in Python" is
   trivially verifiable from the codebase. "Users will authenticate via
   OAuth 2.0 with PKCE" carries real design implications.
4. **Falsifiable** — Could be wrong. "We should use a database" is a
   recommendation, not an assumption. "The existing database supports
   JSON columns" is falsifiable.

## Common Assumption Categories

- **Architectural** — Technology choices, patterns, integration points
- **Behavioral** — How users/systems interact, expected workflows
- **Constraint** — Performance limits, compliance requirements, deadlines
- **Dependency** — What exists, what's available, what's compatible
- **Scope** — What's included/excluded, boundaries of the work

## Anti-Patterns

- **Opinions disguised as assumptions** — "React is the best framework" is
  not an assumption about the project.
- **Compound assumptions** — "Users authenticate via OAuth and sessions
  expire after 30 minutes" is two assumptions. Split them.
- **Tautologies** — "The system will work correctly" is not checkable.
- **Implementation details** — "We'll use a for loop" is too low-level to
  be worth challenging.
```

<<<<<<< HEAD
- [x] **Step 3: Write `gap-analysis-guide.md`**
=======
- [ ] **Step 3: Write `gap-analysis-guide.md`**
>>>>>>> origin/main

```markdown
# Gap Analysis Guide

## Classification Rules

For each assumption, read the matched documents and classify:

### Aligned

The assumption is **aligned** when a document explicitly supports the claim.
The document must directly address the same concept — not merely mention
a related term.

**Confidence levels:**
- **High** — The document explicitly states or strongly implies the same
  claim. No inference needed. Example: assumption says "OAuth 2.0",
  document says "We use OAuth 2.0 with PKCE."
- **Moderate** — The document discusses the same topic with a compatible
  position, but doesn't state the exact claim. Requires inference.
  Example: assumption says "OAuth 2.0", document discusses "token-based
  authentication patterns."
- **Low** — The document touches on a related area. The connection is
  plausible but indirect. Example: assumption says "OAuth 2.0", document
  discusses "third-party API integration."

### Gap

The assumption is a **gap** when a document contradicts or conflicts with
the claim. The contradiction must be substantive, not a difference in
wording.

**Confidence levels:**
- **High** — Direct contradiction. Document explicitly states the opposite.
  Example: assumption says "1000 req/min", document says "500 req/min."
- **Moderate** — Implied contradiction. Document's position is incompatible
  but doesn't directly address the claim.
- **Low** — Tension exists but both positions could coexist under certain
  interpretations.

### No Coverage

The assumption has **no coverage** when no document addresses the topic.
No Coverage items have no confidence level — evidence is absent, not weak.

Do not classify as No Coverage if a document is tangentially relevant.
Use Low confidence Aligned or Gap instead. Reserve No Coverage for
assumptions the knowledge base is genuinely silent on.

## Key Principles

1. **Don't manufacture evidence.** If a document doesn't clearly address
   the assumption, classify as No Coverage rather than stretching to
   claim Low confidence alignment.
2. **Cite specifically.** Reference the document path and the relevant
   section or claim within it.
3. **One source per row.** If multiple documents address an assumption,
   use the strongest evidence. Mention supporting sources in the
   Evidence column.
4. **Gaps over alignment when ambiguous.** If evidence could support
   either classification, flag it as a Gap. False gaps are safer than
   false alignment — they prompt review rather than false confidence.
```

<<<<<<< HEAD
- [x] **Step 4: Commit**
=======
- [ ] **Step 4: Commit**
>>>>>>> origin/main

```bash
git add skills/challenge/references/assumption-quality.md skills/challenge/references/gap-analysis-guide.md
git commit -m "docs(challenge): add assumption-quality and gap-analysis reference guides"
```

---

## Task 6: Create SKILL.md

The core skill definition that orchestrates the four-phase workflow.

**Files:**
- Create: `skills/challenge/SKILL.md`

<<<<<<< HEAD
- [x] **Step 1: Write SKILL.md**
=======
- [ ] **Step 1: Write SKILL.md**
>>>>>>> origin/main

```markdown
---
name: challenge
description: >
  Surfaces and sanity-checks assumptions behind an output or recent
  conversation against project context and research documents. Use when
  the user asks to "check your assumptions", "challenge this", "what are
  you assuming", "sanity check", "ground check", "challenge reasoning",
  "what assumptions", or "verify reasoning".
argument-hint: "[file path or quoted output]"
user-invocable: true
references:
  - references/assumption-quality.md
  - references/gap-analysis-guide.md
---

# /wos:challenge

Surface implicit assumptions, check them against project knowledge, and
propose corrections where evidence conflicts or is absent.

## Input

Two modes based on arguments:

- **No argument (conversation mode):** Extract assumptions from the most
  recent substantive output in the current session.
- **File path or quoted text (artifact mode):** Extract assumptions from
  the specified artifact. If the file has `related` frontmatter, those
  linked documents are searched first.

## Workflow

Four phases. Do not skip phases or combine them.

### Phase 1 — Extract Assumptions

Read the input (conversation output or artifact) and enumerate every
implicit assumption and piece of reasoning as a numbered list. Each
assumption must be a testable, specific, non-trivial claim. See
@assumption-quality.md for quality criteria.

Present the numbered list to the user:

> "Here are the assumptions I identified. Want to add, remove, or
> rephrase any before I check them?"

**Wait for the user.** Do not proceed to Phase 2 until the user confirms
or modifies the list. Numbering stabilizes after this gate.

If zero assumptions are extracted, report this and ask the user if they
want to supply assumptions manually or point to a different output. Do
not proceed.

If more than 15 assumptions are extracted, ask the user to prioritize
before proceeding.

### Phase 2 — Layered Search

Run the discovery script to find relevant documents:

```bash
python <plugin-scripts-dir>/discover_context.py \
  --assumptions "assumption 1" "assumption 2" ... \
  --root <project-root>
```

If in artifact mode with a file path, add `--artifact <path>`.

Parse the JSON output. For each assumption, read the top-scoring
documents (up to 5 per assumption) using the Read tool. Evaluate which
assumptions each document supports, contradicts, or is silent on.

Log each search step for the search protocol:
- Which assumptions were searched
- Which documents matched (with scores)
- Which documents were read in full
- What evidence was extracted

No user-facing output in this phase.

### Phase 3 — Gap Analysis

Present a summary table:

| # | Assumption | Status | Confidence | Evidence | Source |
|---|-----------|--------|------------|----------|--------|
| 1 | ... | Aligned | High | ... | `path` |
| 2 | ... | Gap | Moderate | ... | `path` |
| 3 | ... | No coverage | — | ... | — |

See @gap-analysis-guide.md for classification rules and confidence
level definitions.

Below the table, write a one-line narrative:
"X assumptions aligned, Y gaps found, Z with no coverage."

Below the narrative, add a collapsed search protocol log:

```markdown
<details>
<summary>Search protocol</summary>

[Table of searches performed, documents matched, documents read]

</details>
```

If all assumptions are aligned, present the table and stop. Do not
proceed to Phase 4.

### Phase 4 — Propose Corrections

For each **Gap** item, draft:
- **Proposed correction:** Revised assumption or artifact change
- **Rationale:** Why, citing the source document
- **Action:** `accept` / `adjust` / `skip`

For each **No Coverage** item, recommend:
- Whether research is needed (suggest `/wos:research`)
- Whether the assumption is safe to hold

Present all proposals:

> "Here are my proposed corrections. Approve, adjust, or skip each one."

**Wait for the user.** Do not edit any files until the user responds.

After user approval:
- **Artifact mode:** Apply accepted corrections to the artifact file.
- **Conversation mode:** Summarize the revised assumption set.

## Key Rules

1. **Read-only until Phase 4 approval.** No file edits until the user
   explicitly approves corrections.
2. **Numbering is stable.** Once shared in Phase 1, assumption numbers
   persist through all phases.
3. **Show your sources.** Every classification cites a document path.
   "No coverage" is explicit, not a missing cell.
4. **Don't manufacture evidence.** If no doc addresses an assumption,
   report No Coverage. Don't stretch tangential docs.
5. **Conversation mode scopes to the recent exchange.** Don't reach back
   through the entire session unless the user asks.
6. **Corrections are proposals.** Frame as "Consider revising X to Y
   because Z." The user has final say.
```

<<<<<<< HEAD
- [x] **Step 2: Verify skill structure**
=======
- [ ] **Step 2: Verify skill structure**
>>>>>>> origin/main

Run: `ls -R skills/challenge/`
Expected:
```
skills/challenge/:
SKILL.md
references/

skills/challenge/references:
assumption-quality.md
gap-analysis-guide.md
```

<<<<<<< HEAD
- [x] **Step 3: Run the audit to check skill quality**
=======
- [ ] **Step 3: Run the audit to check skill quality**
>>>>>>> origin/main

Run: `python scripts/audit.py --root . --no-urls 2>&1 | grep -i challenge`
Expected: No fail-severity issues for the challenge skill.

<<<<<<< HEAD
- [x] **Step 4: Commit**
=======
- [ ] **Step 4: Commit**
>>>>>>> origin/main

```bash
git add skills/challenge/SKILL.md
git commit -m "feat(challenge): add SKILL.md with four-phase workflow"
```

---

## Task 7: Run full test suite and lint

Verify everything works together.

**Files:**
- No new files. Verification only.

<<<<<<< HEAD
- [x] **Step 1: Run full test suite**
=======
- [ ] **Step 1: Run full test suite**
>>>>>>> origin/main

Run: `python -m pytest tests/ -v`
Expected: All tests PASS, including new challenge tests.

<<<<<<< HEAD
- [x] **Step 2: Run linter**
=======
- [ ] **Step 2: Run linter**
>>>>>>> origin/main

Run: `ruff check wos/ tests/ scripts/`
Expected: No errors. Fix any issues found.

<<<<<<< HEAD
- [x] **Step 3: Run audit on the project**
=======
- [ ] **Step 3: Run audit on the project**
>>>>>>> origin/main

Run: `python scripts/audit.py --root . --no-urls`
Expected: No new fail-severity issues introduced.

<<<<<<< HEAD
- [x] **Step 4: Commit any lint fixes**
=======
- [ ] **Step 4: Commit any lint fixes**
>>>>>>> origin/main

If lint fixes were needed:
```bash
git add -u
git commit -m "style(challenge): fix lint issues"
```

---

## Validation Criteria

The implementation is complete when:

1. `python -m pytest tests/ -v` passes with all new tests green
2. `ruff check wos/ tests/ scripts/` reports no errors
3. `python scripts/audit.py --root . --no-urls` shows no new fail-severity issues
4. `python scripts/discover_context.py --assumptions "test" --root .` outputs valid JSON
5. `skills/challenge/SKILL.md` exists with valid frontmatter and references
6. `skills/challenge/references/` contains both guide documents
