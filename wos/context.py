"""Context document class with word count and related-field validation."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List

from wos.document import Document


@Document.register("context")
@dataclass
class ContextDocument(Document):
    """A context document with word count and related-field validation."""

    def issues(
        self,
        root: Path,
        max_words: int = 800,
        min_words: int = 100,
        **_: object,
    ) -> List[dict]:
        """Return base issues plus context-specific checks.

        Adds: missing related-fields warning, and word count threshold
        warnings (skipped for _index.md files).

        Args:
            root: Project root directory.
            max_words: Upper word count threshold (default 800).
            min_words: Lower word count threshold (default 100).

        Returns:
            List of issue dicts with keys: file, issue, severity.
        """
        result = super().issues(root)

        if not self.related:
            result.append({
                "file": self.path,
                "issue": "Context file has no related fields",
                "severity": "warn",
            })

        if not self.path.endswith("_index.md"):
            word_count = self.word_count
            if word_count > max_words:
                result.append({
                    "file": self.path,
                    "issue": (
                        f"Context file is {word_count} words"
                        f" (threshold: {max_words})"
                    ),
                    "severity": "warn",
                })
            elif word_count < min_words:
                result.append({
                    "file": self.path,
                    "issue": (
                        f"Context file is {word_count} words"
                        f" (minimum: {min_words})"
                    ),
                    "severity": "warn",
                })

        return result
