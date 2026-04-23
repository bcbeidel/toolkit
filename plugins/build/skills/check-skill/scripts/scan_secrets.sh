#!/usr/bin/env bash
#
# scan_secrets.sh — Tier-1 secret scan for Claude Code SKILL.md files.
#
# Prefers `gitleaks detect --no-git --source <path>` when available;
# falls back to a built-in regex set (AWS access keys, GitHub PATs,
# OpenAI / Anthropic / Stripe keys, credential-shaped variable
# assignments) when gitleaks is absent.
#
# Any match is FAIL — skill files are committed config; a committed
# credential is a breach regardless of how it surfaces.
#
# Usage:
#   scan_secrets.sh <path> [<path> ...]
#
# Exit codes:
#   0   no FAIL findings
#   1   one or more FAIL findings
#   64  usage error
#   69  missing dependency (neither gitleaks nor the fallback's tools)
#
# Dependencies:
#   awk, find, basename, grep
#   (optional) gitleaks — used when present

set -Eeuo pipefail
IFS=$'\n\t'

PROGNAME="$(basename "${0}")"
REQUIRED_CMDS=(awk find basename grep)

usage() {
  cat <<'EOF'
scan_secrets.sh — Secret scan for Claude Code SKILL.md files.

Usage:
  scan_secrets.sh <path> [<path> ...]

Options:
  -h, --help   Show this help and exit.

Detection:
  Prefers `gitleaks detect --no-git --source <path>` when available.
  Falls back to built-in regex: AWS access keys, GitHub PATs, OpenAI /
  Anthropic / Stripe keys, credential-shaped variable assignments.

Exit codes:
  0   no FAIL findings
  1   one or more FAIL findings
  64  usage error
  69  missing dependency (grep / awk unavailable)

Installation (optional):
  brew install gitleaks         # macOS
  apt install gitleaks          # Debian/Ubuntu
EOF
}

install_hint() {
  case "${1}" in
    awk|find|basename|grep) printf 'should be preinstalled on any POSIX system' ;;
    gitleaks)               printf 'brew install gitleaks (or see https://github.com/gitleaks/gitleaks)' ;;
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

emit_fail() {
  local path="$1" check="$2" detail="$3" rec="$4"
  printf 'FAIL  %s — %s: %s\n' "${path}" "${check}" "${detail}"
  printf '  Recommendation: %s\n' "${rec}"
}

scan_with_gitleaks() {
  local file="$1"
  # gitleaks writes findings to stdout when --report-format is unset
  # plus a summary to stderr; we want a simple exit-code + find signal.
  local output rc=0
  output="$(gitleaks detect --no-git --no-banner --source "${file}" --report-format json 2>/dev/null || true)"
  # An empty array / absence of "RuleID" means no findings.
  if [ -z "${output}" ] || [ "${output}" = "[]" ]; then
    return 0
  fi
  # Each finding surfaces as a FAIL; include the rule id if present.
  printf '%s' "${output}" | awk '
    /"RuleID":/ {
      match($0, /"RuleID":[[:space:]]*"[^"]*"/)
      if (RLENGTH > 0) {
        rid = substr($0, RSTART, RLENGTH)
        sub(/^"RuleID":[[:space:]]*"/, "", rid)
        sub(/"$/, "", rid)
        print rid
      }
    }
  ' | while IFS= read -r rule; do
    [ -n "${rule}" ] || continue
    emit_fail "${file}" "Secret" \
      "gitleaks matched rule '${rule}'" \
      "Rotate the exposed credential; replace the literal with an env var or vault path"
    rc=1
  done
  return "${rc}"
}

# Built-in regex fallback. Returns 0 if no match, 1 if any match.
scan_with_fallback() {
  local file="$1"
  # Each pattern is ERE (grep -E). Matches anywhere in file including
  # inside code blocks, since committed skills are searchable.
  local patterns=(
    'AKIA[0-9A-Z]{16}'                              # AWS access key ID
    'ghp_[A-Za-z0-9]{36}'                           # GitHub personal access token
    'github_pat_[A-Za-z0-9_]{82}'                   # GitHub fine-grained PAT
    'sk-[A-Za-z0-9]{48}'                            # OpenAI API key
    'sk-ant-[A-Za-z0-9_-]{80,}'                     # Anthropic API key
    'sk_live_[A-Za-z0-9]{24}'                       # Stripe live secret key
  )
  # Credential-shaped variable assignment (non-empty quoted string after
  # password/secret/token/api_key/access_key/private_key).
  local cred_pat='(password|secret|token|api[_-]?key|access[_-]?key|private[_-]?key)[[:space:]]*[=:][[:space:]]*["'"'"'][^"'"'"']+["'"'"']'
  local any=0 pat hits

  for pat in "${patterns[@]}"; do
    if hits="$(grep -En "${pat}" "${file}" 2>/dev/null)"; then
      while IFS= read -r hit; do
        [ -n "${hit}" ] || continue
        local line_no="${hit%%:*}"
        emit_fail "${file}" "Secret (fallback regex)" \
          "line ${line_no}: credential pattern /${pat}/ matched" \
          "Rotate the exposed credential; replace the literal with an env var or vault path"
        any=1
      done <<<"${hits}"
    fi
  done

  # Credential assignment — case-insensitive.
  if hits="$(grep -EniI "${cred_pat}" "${file}" 2>/dev/null)"; then
    while IFS= read -r hit; do
      [ -n "${hit}" ] || continue
      local line_no="${hit%%:*}"
      emit_fail "${file}" "Secret (fallback regex)" \
        "line ${line_no}: credential-shaped variable assignment" \
        "Replace the literal with an env-var reference or vault path (e.g., \${VAR})"
      any=1
    done <<<"${hits}"
  fi

  return "${any}"
}

scan_file() {
  local file="$1"
  if command -v gitleaks >/dev/null 2>&1; then
    scan_with_gitleaks "${file}"
  else
    scan_with_fallback "${file}"
  fi
}

check_path() {
  local target="$1"
  local any=0
  local file
  if [ -f "${target}" ]; then
    scan_file "${target}" || any=1
  elif [ -d "${target}" ]; then
    while IFS= read -r file; do
      scan_file "${file}" || any=1
    done < <(
      find "${target}" -type f -name 'SKILL.md' \
        -not -path '*/_shared/*' \
        2>/dev/null
    )
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
  local any=0 target
  for target in "$@"; do
    check_path "${target}" || any=1
  done
  exit "${any}"
}

if [ "${0}" = "${BASH_SOURCE[0]:-$0}" ]; then
  main "$@"
fi
