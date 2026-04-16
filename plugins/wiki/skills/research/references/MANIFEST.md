---
name: Reference File Manifest
description: Machine-readable index mapping pipeline stages to reference files for cross-platform agent discovery
---

# Reference File Manifest

Stage-to-file mapping for the research and distill pipelines. Each stage's
methodology is defined in one or more reference files. The first file listed
is the **primary** reference (holds Input, Output, Gate, and Constraints).
Orchestrators read these at runtime for inline execution or compose them
into dispatch prompts for delegation.

## Research Pipeline References

| Stage | Role | Files | Tools | Entry Gate | Purpose |
|-------|------|-------|-------|------------|---------|
| frame | Framing expert — analyzes questions, decomposes into sub-questions | research/frame.md, research/research-modes.md | Read, Glob, Grep | — | Question analysis, mode detection, sub-question decomposition |
| gather | Source discovery expert — finds, extracts, and verifies sources | research/gather-and-extract.md, research/verify-sources.md, research/cli-commands.md | Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch | — | Source discovery, verbatim extraction, URL verification |
| evaluate | Source evaluation expert — applies SIFT framework to assess source quality | research/evaluate-sources-sift.md | Read, Write, Edit, Glob, Grep, Bash | gatherer_exit | SIFT tier assignment (T1-T5), red flag detection |
| challenge | Critical thinking expert — tests assumptions and finds counter-evidence | research/challenge.md | Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch | evaluator_exit | Assumptions check, ACH, premortem |
| synthesize | Synthesis expert — organizes findings with confidence calibration | research/synthesize.md | Read, Write, Edit, Glob, Grep, Bash | challenger_exit | Confidence-annotated findings with source attribution |
| verify | Verification expert — verifies claims via CoVe and citation re-verification | research/self-verify-claims.md, research/citation-reverify.md | Read, Write, Edit, Glob, Grep, Bash, WebFetch | synthesizer_exit | Chain of Verification (CoVe), citation re-verification |
| finalize | Finalization expert — restructures, validates, and publishes | research/finalize.md, research/cli-commands.md | Read, Write, Edit, Glob, Grep, Bash | verifier_exit | Lost-in-the-middle restructuring, search protocol formatting, validation |

## Distill Pipeline References

| Stage | Role | Files | Tools | Entry Gate | Purpose |
|-------|------|-------|-------|------------|---------|
| map | Mapping expert — analyzes research and proposes finding-to-context-file mappings | distill/mapping-guide.md, distill/distillation-guidelines.md | Read, Glob, Grep | — | Finding boundaries, N:M mapping, one-concept test |
| write | Context file writer — distills findings into focused reference documents | distill/distillation-guidelines.md | Read, Write, Edit, Glob, Grep, Bash | — | Context file quality criteria, confidence carry-forward |

## Supporting References

| File | Purpose |
|------|---------|
| research/resumption.md | Phase detection from disk state after context reset |
| research/cli-commands.md | Shared utility commands (audit, reindex, url_checker) |
