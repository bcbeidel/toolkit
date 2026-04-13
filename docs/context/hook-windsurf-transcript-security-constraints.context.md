---
name: "Windsurf Transcript Security Constraints"
description: "Windsurf post_cascade_response_with_transcript writes sensitive codebase data to JSONL files with 0600 permissions; schema is explicitly unstable; 100-file cap prunes oldest silently"
type: context
sources:
  - https://docs.windsurf.com/windsurf/cascade/hooks
related:
  - docs/research/2026-04-13-hooks-platform-comparison.research.md
  - docs/context/hook-windsurf-model-and-constraints.context.md
  - docs/context/hook-supply-chain-attack-surface-cross-platform.context.md
---

The `post_cascade_response_with_transcript` hook event writes full conversation transcripts to disk after every Cascade response. Three constraints govern these files: security sensitivity, schema instability, and a hard file count cap.

**What transcript files contain**

Transcripts include "detailed step-by-step data with file contents and command outputs" from the full session. The Windsurf documentation explicitly warns: "transcript files will contain sensitive information from your codebase including file contents, command outputs, and conversation history, and should be handled according to your organization's security and privacy policies."

This means transcript directories can accumulate files containing complete copies of edited source files, full outputs of executed shell commands, and the entire conversation history — all in one place.

**File permissions**

Transcript files are written with `0600` permissions (owner read/write only). This provides baseline access control on POSIX systems, but does not protect against processes running as the same user, backup systems that archive without preserving permissions, or code that explicitly reads and transmits these files.

**Schema instability**

The Windsurf documentation explicitly states: "The exact structure of each step may change in future versions, so consumers of hook data should be built to be resilient." Any parsing logic written against the transcript schema may break silently on a Windsurf update. There is no versioning or backward compatibility guarantee.

**100-file cap with silent pruning**

Windsurf automatically limits the transcripts directory to 100 files. When the cap is reached, the oldest files by modification time are pruned. This pruning is silent — no notification, no archive, no warning. Long-running setups will lose historical transcripts without indication.

**Operational guidance**

- Do not store transcript directories in shared or backed-up locations without stripping or redacting sensitive fields first.
- Do not write production parsers against the transcript schema without a version check; treat the format as advisory.
- If transcript history matters, implement your own export before the 100-file cap is reached.
- The `show_output` flag does not apply to `post_cascade_response` hooks; output display constraints from that flag are irrelevant here.
