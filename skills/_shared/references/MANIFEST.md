---
name: Reference File Manifest
description: Machine-readable index mapping pipeline stages to reference files for cross-platform agent discovery
---

# Reference File Manifest

Stage-to-file mapping for the research and distill pipelines. Each stage's
methodology is defined in one or more reference files. Agents inline these
at definition time; orchestrators read them at runtime for inline execution.

## Research Pipeline References

| Stage | Files | Purpose |
|-------|-------|---------|
| frame | research/frame.md, research/research-modes.md | Question analysis, mode detection, sub-question decomposition |
| gather | research/gather-and-extract.md, research/verify-sources.md, research/cli-commands.md | Source discovery, verbatim extraction, URL verification |
| evaluate | research/evaluate-sources-sift.md | SIFT tier assignment (T1-T5), red flag detection |
| challenge | research/challenge.md | Assumptions check, ACH, premortem |
| synthesize | research/synthesize.md | Confidence-annotated findings with source attribution |
| verify | research/self-verify-claims.md, research/citation-reverify.md | Chain of Verification (CoVe), citation re-verification |
| finalize | research/finalize.md, research/cli-commands.md | Lost-in-the-middle restructuring, search protocol formatting, validation |

## Distill Pipeline References

| Stage | Files | Purpose |
|-------|-------|---------|
| map | distill/mapping-guide.md, distill/distillation-guidelines.md | Finding boundaries, N:M mapping, one-concept test |
| write | distill/distillation-guidelines.md | Context file quality criteria, confidence carry-forward |

## Supporting References

| File | Purpose |
|------|---------|
| research/resumption.md | Phase detection from disk state after context reset |
| research/cli-commands.md | Shared utility commands (audit, reindex, url_checker) |
| preflight.md | uv availability check, canary script validation |
