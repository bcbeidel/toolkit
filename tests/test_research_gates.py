"""Tests for research pipeline gate checks against fixture files.

Each exit fixture should pass its corresponding gate.
Entry fixtures should fail the exit gate (negative test).
"""

from __future__ import annotations

import os

import pytest

from wos.research import ResearchDocument

FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures", "research")


def _fixture(name: str) -> str:
    return os.path.join(FIXTURES_DIR, name)


@pytest.mark.parametrize(
    "gate_name,fixture_file",
    [
        ("gatherer_exit", "gatherer_exit.md"),
        ("evaluator_exit", "evaluator_exit.md"),
        ("challenger_exit", "challenger_exit.md"),
        ("synthesizer_exit", "synthesizer_exit.md"),
        ("verifier_exit", "verifier_exit.md"),
        ("finalizer_exit", "finalizer_exit.md"),
    ],
)
def test_exit_fixture_passes_gate(gate_name: str, fixture_file: str) -> None:
    """Exit fixtures should pass their corresponding gate check."""
    result = ResearchDocument.check_single_gate(_fixture(fixture_file), gate_name)
    assert result["pass"], (
        f"{fixture_file} failed {gate_name}: {result.get('checks', {})}"
    )


def test_gatherer_entry_fails_gatherer_exit() -> None:
    """Entry fixture should fail the exit gate (negative test)."""
    result = ResearchDocument.check_single_gate(
        _fixture("gatherer_entry.md"), "gatherer_exit"
    )
    assert not result["pass"], "gatherer_entry.md should fail gatherer_exit gate"
