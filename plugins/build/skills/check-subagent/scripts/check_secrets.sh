#!/usr/bin/env bash
#
# check_secrets.sh — Scan subagent definitions for committed secrets.
#
# Deterministic Tier-1 Safety check invoked by /build:check-subagent.
# Scans .md files under agents/ directories for well-known API key
# patterns and credential-shaped variable assignments, skipping
# obvious placeholders. A FAIL finding excludes the file from Tier-2.
#
# Usage:
#   check_secrets.sh <path> [<path> ...]
#
# Exit codes:
#   0   no findings
#   1   one or more FAIL findings
#   64  usage error
#   69  missing required dependency (grep/find/basename)

set -Eeuo pipefail
IFS=$'\n\t'

PROGNAME="$(basename "${0}")"

REQUIRED_CMDS=(grep find basename)

usage() {
  cat <<'EOF'
check_secrets.sh — Scan subagent definitions for committed secrets.

Usage:
  check_secrets.sh <path> [<path> ...]
EOF
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
      printf '%s: missing required command %q\n' "${PROGNAME}" "${cmd}" >&2
    done
    exit 69
  fi
}

emit_finding() {
  local path="$1" name="$2" line="$3"
  printf 'FAIL  %s — secret: %s at line %s\n' "${path}" "${name}" "${line}"
  printf '  Recommendation: Remove the secret, rotate the credential, '
  printf 'and document an env-var requirement in the body instead.\n'
}

PATTERN_NAMES=(
  "AWS access key"
  "GitHub personal access token"
  "GitHub fine-grained PAT"
  "OpenAI API key"
  "Anthropic API key"
  "Stripe live key"
  "PEM private key header"
)
PATTERN_REGEXES=(
  'AKIA[0-9A-Z]{16}'
  'ghp_[A-Za-z0-9]{36}'
  'github_pat_[A-Za-z0-9_]{82}'
  'sk-[A-Za-z0-9]{48}'
  'sk-ant-[A-Za-z0-9_-]{80,}'
  'sk_live_[A-Za-z0-9]{24}'
  '-----BEGIN (RSA |OPENSSH |EC |DSA )?PRIVATE KEY-----'
)

GENERIC_VAR_REGEX="(password|secret|token|api_key|access_key|private_key)[[:space:]]*[:=][[:space:]]*[\"'][^\"']+[\"']"

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

  while IFS= read -r hit; do
    line="${hit%%:*}"
    emit_finding "${file}" "credential assignment" "${line}"
    found=1
  done < <(
    grep -niE "${GENERIC_VAR_REGEX}" "${file}" 2>/dev/null \
      | grep -Ev "[:=][[:space:]]*[\"']\\\$" \
      | grep -Ev "[:=][[:space:]]*[\"']\\{" \
      | grep -Ev "[:=][[:space:]]*[\"']<" \
      | grep -iEv "[:=][[:space:]]*[\"'](your[-_]|example|redacted|null|none|undefined|placeholder|todo|fixme|xxx|changeme|change[-_]me|foo|bar|baz|abc|xyz)" \
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
      *.md) scan_file "${target}" || any=1 ;;
    esac
  elif [ -d "${target}" ]; then
    while IFS= read -r file; do
      scan_file "${file}" || any=1
    done < <(find "${target}" -maxdepth 1 -type f -name '*.md' 2>/dev/null)
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
