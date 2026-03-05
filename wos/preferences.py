"""Communication preferences — dimension mapping and rendering.

Maps user communication preferences to structured dimensions and
renders them as instruction strings for AGENTS.md.
"""

from __future__ import annotations

from typing import Dict, List

# ── Dimensions ───────────────────────────────────────────────────

DIMENSIONS: Dict[str, List[str]] = {
    "directness": ["blunt", "balanced", "diplomatic"],
    "verbosity": ["terse", "moderate", "thorough"],
    "depth": ["just-answers", "context-when-useful", "teach-me"],
    "expertise": ["beginner", "intermediate", "expert"],
    "tone": ["casual", "neutral", "formal"],
}

DIMENSION_INSTRUCTIONS: Dict[tuple, str] = {
    # Directness
    ("directness", "blunt"): (
        "Be direct. State problems and disagreements plainly "
        "without hedging or softening."
    ),
    ("directness", "balanced"): (
        "Be straightforward but considerate. State issues clearly "
        "while acknowledging tradeoffs."
    ),
    ("directness", "diplomatic"): (
        "Frame feedback constructively. Lead with positives, "
        "suggest improvements gently."
    ),
    # Verbosity
    ("verbosity", "terse"): (
        "Keep responses concise. Skip preamble and unnecessary elaboration."
    ),
    ("verbosity", "moderate"): (
        "Provide enough detail to be clear without being exhaustive."
    ),
    ("verbosity", "thorough"): (
        "Be comprehensive. Include context, examples, and edge cases."
    ),
    # Depth
    ("depth", "just-answers"): (
        "Give the answer directly. Skip explanations unless asked."
    ),
    ("depth", "context-when-useful"): (
        "Provide context when it aids understanding, but don't over-explain."
    ),
    ("depth", "teach-me"): (
        "Explain the reasoning and principles behind recommendations. "
        "Help me learn, not just execute."
    ),
    # Expertise
    ("expertise", "beginner"): (
        "Assume limited domain knowledge. Define terms and explain concepts."
    ),
    ("expertise", "intermediate"): (
        "Assume working knowledge. Skip basics but explain advanced concepts."
    ),
    ("expertise", "expert"): (
        "Assume expert-level knowledge. Skip fundamentals."
    ),
    # Tone
    ("tone", "casual"): (
        "Keep it casual and conversational. Informal language is fine."
    ),
    ("tone", "neutral"): (
        "Neutral and professional. No sycophancy or forced enthusiasm."
    ),
    ("tone", "formal"): (
        "Maintain a formal, professional tone throughout."
    ),
}

# Display names for dimensions
_DISPLAY_NAMES = {
    "directness": "Directness",
    "verbosity": "Verbosity",
    "depth": "Depth",
    "expertise": "Expertise",
    "tone": "Tone",
}


# ── Render ───────────────────────────────────────────────────────


def render_preferences(prefs: Dict[str, str]) -> List[str]:
    """Render preference dimensions as instruction strings.

    Each string is formatted as ``**Dimension:** instruction`` without
    a bullet prefix. Pass the returned list to
    ``render_wos_section(preferences=...)`` which adds bullets.

    Args:
        prefs: Mapping of dimension name to level.

    Returns:
        List of formatted instruction strings.

    Raises:
        ValueError: If an unknown dimension or level is provided.
    """
    result: List[str] = []
    for dim, level in prefs.items():
        if dim not in DIMENSIONS:
            raise ValueError(f"Unknown dimension: {dim}")
        if level not in DIMENSIONS[dim]:
            raise ValueError(
                f"Unknown level '{level}' for dimension '{dim}'. "
                f"Valid levels: {DIMENSIONS[dim]}"
            )
        instruction = DIMENSION_INSTRUCTIONS[(dim, level)]
        display = _DISPLAY_NAMES[dim]
        result.append(f"**{display}:** {instruction}")
    return result
