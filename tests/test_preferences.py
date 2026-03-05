"""Tests for wos/preferences.py — communication preferences."""

from __future__ import annotations

import pytest

# ── Dimension mapping ────────────────────────────────────────────


class TestDimensionInstruction:
    def test_all_dimensions_have_instructions(self) -> None:
        from wos.preferences import DIMENSION_INSTRUCTIONS, DIMENSIONS

        for dim in DIMENSIONS:
            for level in DIMENSIONS[dim]:
                assert (dim, level) in DIMENSION_INSTRUCTIONS

    def test_instruction_is_nonempty_string(self) -> None:
        from wos.preferences import DIMENSION_INSTRUCTIONS

        for key, instruction in DIMENSION_INSTRUCTIONS.items():
            assert isinstance(instruction, str), f"{key} is not a string"
            assert len(instruction) > 0, f"{key} is empty"


# ── Render preferences ──────────────────────────────────────────


class TestRenderPreferences:
    def test_renders_all_dimensions(self) -> None:
        from wos.preferences import render_preferences

        prefs = {
            "directness": "blunt",
            "verbosity": "terse",
            "depth": "just-answers",
            "expertise": "expert",
            "tone": "casual",
        }
        result = render_preferences(prefs)
        assert isinstance(result, list)
        assert len(result) == 5
        assert any("Directness" in line for line in result)
        assert any("Verbosity" in line for line in result)
        assert any("Depth" in line for line in result)
        assert any("Expertise" in line for line in result)
        assert any("Tone" in line for line in result)

    def test_renders_subset_of_dimensions(self) -> None:
        from wos.preferences import render_preferences

        prefs = {"directness": "blunt", "tone": "formal"}
        result = render_preferences(prefs)
        assert len(result) == 2
        assert any("Directness" in line for line in result)
        assert any("Tone" in line for line in result)
        assert not any("Verbosity" in line for line in result)

    def test_no_bullet_prefix(self) -> None:
        from wos.preferences import render_preferences

        result = render_preferences({"directness": "blunt"})
        assert not result[0].startswith("- ")
        assert result[0].startswith("**Directness:**")

    def test_invalid_dimension_raises(self) -> None:
        from wos.preferences import render_preferences

        with pytest.raises(ValueError, match="Unknown dimension"):
            render_preferences({"nonexistent": "value"})

    def test_invalid_level_raises(self) -> None:
        from wos.preferences import render_preferences

        with pytest.raises(ValueError, match="Unknown level"):
            render_preferences({"directness": "nonexistent"})

    def test_compatible_with_render_wos_section(self) -> None:
        from wos.agents_md import render_wos_section
        from wos.preferences import render_preferences

        prefs = render_preferences({"directness": "blunt"})
        result = render_wos_section(areas=[], preferences=prefs)
        assert "### Preferences" in result
        assert "- **Directness:**" in result
