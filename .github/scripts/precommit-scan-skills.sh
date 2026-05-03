#!/usr/bin/env bash
#
# precommit-scan-skills.sh — run cisco-ai-skill-scanner against the
# skill directories that contain staged changes. Static analyzers only
# (no --use-llm), so the hook is fast, deterministic, and does not need
# an API key.
#
# Pre-commit framework passes the staged file list as positional args.
# This script maps each file to its parent skill directory
# (plugins/<plugin>/skills/<skill>/), dedupes, and scans each one.
#
# Usage (direct):
#   ./precommit-scan-skills.sh plugins/build/skills/check-skill/SKILL.md ...
#
# Usage (via pre-commit framework): wired through .pre-commit-config.yaml
# with files: '^plugins/[^/]+/skills/[^/]+/'.
#
# Dependencies: skill-scanner (cisco-ai-skill-scanner==2.0.9), bash 4.0+.
#
# Exit codes:
#   0   no in-scope files, or scan clean (no HIGH+ findings)
#   1   one or more skills have HIGH or CRITICAL findings
#   2   scanner not installed or other misconfiguration

set -euo pipefail

PROGNAME="$(basename "${0}")"
readonly PROGNAME

# Regex matching a path inside a skill directory. Capture group 1 is the
# skill directory itself (plugins/<plugin>/skills/<skill>).
readonly SKILL_PATH_RE='^(plugins/[^/]+/skills/[^/]+)/'

die() {
  printf '%s: error: %s\n' "${PROGNAME}" "$*" >&2
  exit 2
}

extract_skill_dirs() {
  local file
  for file in "$@"; do
    if [[ "${file}" =~ ${SKILL_PATH_RE} ]]; then
      printf '%s\n' "${BASH_REMATCH[1]}"
    fi
  done | sort -u
}

scan_one() {
  local skill_dir="$1"
  if [[ ! -d "${skill_dir}" ]]; then
    # Skill was deleted in this commit; nothing to scan.
    return 0
  fi
  printf '\n=== Scanning %s ===\n' "${skill_dir}"
  skill-scanner scan "${skill_dir}" \
    --format summary \
    --fail-on-severity high
}

main() {
  if ! command -v skill-scanner >/dev/null 2>&1; then
    die "skill-scanner not found on PATH. Install with: pip install cisco-ai-skill-scanner==2.0.9"
  fi

  local skill_dirs
  skill_dirs="$(extract_skill_dirs "$@")"

  if [[ -z "${skill_dirs}" ]]; then
    return 0
  fi

  local failed=0
  local skill_dir
  while IFS= read -r skill_dir; do
    if ! scan_one "${skill_dir}"; then
      failed=1
    fi
  done <<<"${skill_dirs}"

  if [[ "${failed}" -ne 0 ]]; then
    printf '\n%s: HIGH or CRITICAL findings detected.\n' "${PROGNAME}" >&2
    printf 'Fix the findings, or bypass intentionally with: git commit --no-verify\n' >&2
    exit 1
  fi
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  main "$@"
fi
