"""Tests for wos/challenge/discover.py."""

from __future__ import annotations

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
