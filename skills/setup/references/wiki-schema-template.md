# SCHEMA.md

Define the structure of this project's wiki.
Validated automatically by `/wos:lint` when `wiki/SCHEMA.md` is present.

## Page Types
- concept
- entity
- source-summary
- comparison

## Confidence Tiers
- high
- medium
- low

## Relationship Types
- related_to
- uses
- depends_on
- contradicts
- supersedes

## Lint Rules
- staleness: high-confidence pages flagged after 90 days without update
- min-sources: high-confidence pages require at least 2 sources
