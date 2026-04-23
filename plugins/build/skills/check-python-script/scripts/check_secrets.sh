#!/usr/bin/env bash
#
# check_secrets.sh — Scan Python scripts for committed secrets.
#
# Deterministic Tier-1 Safety check invoked by /build:check-python-script.
# Scans *.py files for well-known API key patterns and for
# credential-shaped variable assignments, skipping obvious placeholders.
#
# Toolkit convention — not from the ensemble synthesis. Adapted from the
# peer check-rule/scripts/scan_secrets.sh. A FAIL finding excludes the
# file from Tier-2 judgment (the model should not evaluate content that
# leaks credentials).
#
# Usage:
#   check_secrets.sh <path> [<path> ...]
#
# Paths may be .py files or directories (top-level .py only).
#
# Exit codes:
#   0   no findings
#   1   one or more FAIL findings
#   64  usage error
#   69  missing dependency
#
# Dependencies:
#   grep, find, basename

set -Eeuo pipefail
IFS=$'\n\t'

PROGNAME="$(basename "${0}")"

REQUIRED_CMDS=(grep find basename)

usage() {
  cat <<'EOF'
check_secrets.sh — Scan Python scripts for committed secrets.

Usage:
  check_secrets.sh <path> [<path> ...]

Arguments:
  <path>   A .py file or directory to scan (top-level .py only).

Options:
  -h, --help   Show this help and exit.

Exit codes:
  0   no findings
  1   one or more FAIL findings
  64  usage error
  69  missing dependency
EOF
}

install_hint() {
  case "${1}" in
    grep|find|basename) printf 'should be preinstalled on any POSIX system' ;;
    *)                  printf 'see your package manager' ;;
  esac
}

preflight() {
  local missing=()
  local cmd
  for cmd in "${REQUIRED_CMDS[@]}"; do
    if ! command -v "${cmd}" >/dev/null 2>&1; then
      missing+=("${cmd}")
    fi
  done
  if [ "${#missing[@]}" -gt 0 ]; then
    for cmd in "${missing[@]}"; do
      printf '%s: missing required command %q. Install: %s\n' \
        "${PROGNAME}" "${cmd}" "$(install_hint "${cmd}")" >&2
    done
    exit 69
  fi
}

emit_finding() {
  local path="$1" name="$2" line="$3"
  printf 'FAIL  %s — secret: %s at line %s\n' "${path}" "${name}" "${line}"
  printf '  Recommendation: Remove the secret, rotate the credential, '
  printf 'and read it from os.environ.get("<VAR_NAME>") instead.\n'
}

# Parallel arrays: specific API key patterns and their display names.
# bash 3.2 has no associative arrays — use ordered arrays.
PATTERN_NAMES=(
  "AWS access key"
  "GitHub personal access token"
  "GitHub fine-grained PAT"
  "OpenAI API key"
  "Anthropic API key"
  "Stripe live key"
)
PATTERN_REGEXES=(
  'AKIA[0-9A-Z]{16}'
  'ghp_[A-Za-z0-9]{36}'
  'github_pat_[A-Za-z0-9_]{82}'
  'sk-[A-Za-z0-9]{48}'
  'sk-ant-[A-Za-z0-9_-]{80,}'
  'sk_live_[A-Za-z0-9]{24}'
)

# Credential-shaped variable assignment with a non-empty quoted value.
# Python idiom — looks for `NAME = "value"` at any indent level.
GENERIC_VAR_REGEX="(password|secret|token|api_key|access_key|private_key)[[:space:]]*=[[:space:]]*[\"'][^\"']+[\"']"

scan_file() {
  local file="$1"
  local found=0
  local i name pattern hit line

  i=0
  while [ "${i}" -lt "${#PATTERN_REGEXES[@]}" ]; do
    name="${PATTERN_NAMES[${i}]}"
    pattern="${PATTERN_REGEXES[${i}]}"
    while IFS= read -r hit; do
      line="${hit%%:*}"
      emit_finding "${file}" "${name}" "${line}"
      found=1
    done < <(grep -nE "${pattern}" "${file}" 2>/dev/null || true)
    i=$((i + 1))
  done

  # Credential-shaped assignments, minus obvious placeholders.
  while IFS= read -r hit; do
    line="${hit%%:*}"
    emit_finding "${file}" "credential variable assignment" "${line}"
    found=1
  done < <(
    grep -niE "${GENERIC_VAR_REGEX}" "${file}" 2>/dev/null \
      | grep -Ev "=[[:space:]]*[\"']\\\$" \
      | grep -Ev "=[[:space:]]*[\"']\\{" \
      | grep -Ev "=[[:space:]]*[\"']<" \
      | grep -iEv "=[[:space:]]*[\"'](your[-_]|example|redacted|null|none|undefined|placeholder|todo|fixme|xxx|changeme|change[-_]me|foo|bar|baz|abc|xyz)" \
      || true
  )

  return "${found}"
}

scan_path() {
  local target="$1"
  local any=0
  local file

  if [ -f "${target}" ]; then
    case "${target}" in
      *.py) scan_file "${target}" || any=1 ;;
    esac
  elif [ -d "${target}" ]; then
    while IFS= read -r file; do
      scan_file "${file}" || any=1
    done < <(find "${target}" -maxdepth 1 -type f -name '*.py' 2>/dev/null)
  else
    printf '%s: path not found: %s\n' "${PROGNAME}" "${target}" >&2
    return 64
  fi
  return "${any}"
}

main() {
  if [ "$#" -eq 0 ]; then
    usage >&2
    exit 64
  fi

  case "${1:-}" in
    -h|--help) usage; exit 0 ;;
  esac

  preflight

  local any=0
  local target
  for target in "$@"; do
    scan_path "${target}" || any=1
  done

  exit "${any}"
}

if [ "${0}" = "${BASH_SOURCE[0]:-$0}" ]; then
  main "$@"
fi
