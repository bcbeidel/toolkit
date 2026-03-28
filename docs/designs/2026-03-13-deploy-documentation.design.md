---
name: Deploy Documentation Updates
description: Update stale deploy design doc and create user-facing DEPLOYING.md guide
metadata:
  type: design
  status: completed
  related:
    - docs/designs/cross-platform-deploy-design.md
    - docs/research/2026-03-13-cross-platform-hooks.research.md
---

## Purpose

The deploy design doc describes a copy-based approach that no longer exists —
`deploy.py` was refactored to use symlinks and gained `--platform` support.
Users have no guide for deploying WOS to other platforms. Fix both.

## Deliverables

### 1. Update `cross-platform-deploy-design.md`

Replace the stale copy/rewrite/preflight content with the current reality:

- **Symlink-based deployment** (not file copying)
- **Two modes:** `--target` (project-level, into `.agents/`) and
  `--platform` (platform-level, into `~/.<platform>/`)
- **Platform registry:** copilot, cursor, claude, codex, gemini,
  windsurf, opencode
- **Support directories:** `scripts/` and `wos/` symlinked alongside skills
- **Backup behavior:** existing dirs get timestamped backup before relinking
- **Idempotent:** re-running skips already-correct symlinks
- Remove all references to file copying, markdown transforms,
  `uv run` rewriting, and preflight stripping
- Set status to `approved` (implementation is complete)

### 2. Create `DEPLOYING.md`

Root-level user-facing guide covering:

- **Quick start** — one-command deploy for each mode
- **Project-level deployment** (`--target`) — what it creates, directory
  structure, when to use it (per-project skill availability)
- **Platform-level deployment** (`--platform`) — what it creates, when
  to use it (skills available across all projects for that platform)
- **Supported platforms** — table of all 7 platforms with their deploy
  paths and the command to deploy
- **How it works** — symlinks (not copies), backup behavior, idempotency,
  `--dry-run` for previewing
- **Prerequisites** — Python 3.9+, WOS plugin installed or cloned

### 3. Update `README.md`

Add a short "Cross-Platform Deployment" section between "Usage" and
"Script Invocation" that points to DEPLOYING.md. Two sentences and
the deploy command.

## Constraints

- No changes to `deploy.py` — documenting what exists
- No platform capability matrix (separate concern)
- DEPLOYING.md is user-facing, not agent context — written for humans
  reading on GitHub, not for LLM consumption
- Keep DEPLOYING.md under 200 lines — concise reference, not a tutorial

## Acceptance Criteria

1. `cross-platform-deploy-design.md` accurately describes symlink-based
   deployment with `--platform` and `--target` modes
2. `cross-platform-deploy-design.md` contains no references to file
   copying, markdown transforms, or preflight
3. DEPLOYING.md covers all 7 supported platforms with commands
4. DEPLOYING.md explains both `--target` and `--platform` modes
5. README.md links to DEPLOYING.md
6. All commands shown in DEPLOYING.md actually work
