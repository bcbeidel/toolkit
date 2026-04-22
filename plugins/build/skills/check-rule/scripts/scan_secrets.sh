#!/usr/bin/env bash
#
# scan_secrets.sh — Scan Claude Code rule files for committed secrets.
#
# Deterministic Tier-1 "Secrets Safety" check invoked by /build:check-rule.
# Scans *.md rule files for well-known API key patterns and for
# credential-shaped variable assignments, skipping obvious placeholders.
#
# Usage:
#   scan_secrets.sh <path> [<path> ...]
#
# Paths may be .md files or directories (recursively scanned for *.md).
#
# Exit codes:
#   0   no findings
#   1   one or more findings
#   64  usage error (no paths, path not found)
#   69  missing dependency
#
# Dependencies:
#   grep, awk, find, sed, head

set -Eeuo pipefail
IFS=$'\n\t'

PROGNAME="$(basename "${0}")"

REQUIRED_CMDS=(grep awk find sed head)

usage() {
  cat <<'EOF'
scan_secrets.sh — Scan Claude Code rule files for committed secrets.

Usage:
  scan_secrets.sh <path> [<path> ...]

Arguments:
  <path>   A .md rule file or directory to scan recursively.

Options:
  -h, --help   Show this help and exit.

Exit codes:
  0   no findings
  1   one or more findings
  64  usage error
  69  missing dependency
EOF
}

install_hint() {
  case "${1}" in
    grep|awk|find|sed|head) printf 'should be preinstalled on any POSIX system' ;;
    *)                      printf 'see your package manager' ;;
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

# Emit the closing frontmatter line number, or 0 if the file has no
# frontmatter or the frontmatter is unclosed (treat as no frontmatter).
frontmatter_end_line() {
  local file="$1"
  local first end
  first="$(head -n 1 "${file}")"
  if [ "${first}" = "---" ]; then
    end="$(awk 'NR > 1 && /^---$/ { print NR; exit }' "${file}")"
    if [ -n "${end}" ]; then
      printf '%s' "${end}"
      return
    fi
  fi
  printf '0'
}

emit_finding() {
  local path="$1" name="$2" line="$3"
  printf 'FAIL  %s — Secrets Safety: %s at line %s\n' "${path}" "${name}" "${line}"
  printf '  Recommendation: Remove the secret, rotate the credential, and reference it via env var name instead.\n'
}

# Parallel arrays: specific API key patterns and their display names.
# bash 3.2 has no associative arrays, so use ordered arrays.
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
GENERIC_VAR_REGEX="(password|secret|token|api_key|access_key|private_key)[[:space:]]*[=:][[:space:]]*[\"'][^\"']+[\"']"

scan_file() {
  local file="$1"
  local fm_end
  fm_end="$(frontmatter_end_line "${file}")"

  local found=0
  local i name pattern hit line

  # Six specific API key patterns.
  i=0
  while [ "${i}" -lt "${#PATTERN_REGEXES[@]}" ]; do
    name="${PATTERN_NAMES[${i}]}"
    pattern="${PATTERN_REGEXES[${i}]}"
    while IFS= read -r hit; do
      line="${hit%%:*}"
      if [ "${line}" -gt "${fm_end}" ]; then
        emit_finding "${file}" "${name}" "${line}"
        found=1
      fi
    done < <(grep -nE "${pattern}" "${file}" 2>/dev/null || true)
    i=$((i + 1))
  done

  # Credential-shaped variable assignments, minus obvious placeholders.
  while IFS= read -r hit; do
    line="${hit%%:*}"
    if [ "${line}" -gt "${fm_end}" ]; then
      emit_finding "${file}" "credential variable assignment" "${line}"
      found=1
    fi
  done < <(
    grep -nE "${GENERIC_VAR_REGEX}" "${file}" 2>/dev/null \
      | grep -Ev "[=:][[:space:]]*[\"']\\\$" \
      | grep -Ev "[=:][[:space:]]*[\"']\\{" \
      | grep -Ev "[=:][[:space:]]*[\"']<" \
      | grep -iEv "[=:][[:space:]]*[\"'](your[-_]|example|redacted|null|none|undefined|placeholder|todo|fixme|xxx|changeme|change[-_]me|foo|bar|baz|abc|xyz)" \
      || true
  )

  return "${found}"
}

scan_path() {
  local target="$1"
  local any=0
  local file

  if [ -f "${target}" ]; then
    scan_file "${target}" || any=1
  elif [ -d "${target}" ]; then
    while IFS= read -r file; do
      scan_file "${file}" || any=1
    done < <(find "${target}" -type f -name '*.md' 2>/dev/null)
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
