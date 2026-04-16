"""wiki: Claude Code plugin for building and maintaining structured project context."""
# Import type modules so subclasses self-register via @Document.register
import wiki.plan  # noqa: F401
import wiki.research  # noqa: F401
import wiki.skill_chain  # noqa: F401
import wiki.wiki  # noqa: F401
