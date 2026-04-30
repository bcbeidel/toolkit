#!/usr/bin/env bash
#
# detect-skill-changes.sh — emit the set of plugin directories that
# contain changed files in a PR.
#
# Usage:
#   BASE_SHA=<sha> HEAD_SHA=<sha> GITHUB_OUTPUT=<path> ./detect-skill-changes.sh
#
# Dependencies: git, jq
#
# Exit codes:
#   0   success
#   1   missing required env var or git error
#
# Output (to GITHUB_OUTPUT):
#   has_changes=<bool>
#   changed_plugins=<json array of plugin directory names>

set -euo pipefail

PROGNAME="$(basename "${0}")"
readonly PROGNAME

REQUIRED_CMDS=(git jq)

die() {
  printf 'error: %s\n' "$*" >&2
  exit 1
}

preflight() {
  local missing=()
  local cmd
  for cmd in "${REQUIRED_CMDS[@]}"; do
    if ! command -v "${cmd}" >/dev/null 2>&1; then
      missing+=("${cmd}")
    fi
  done
  if [[ "${#missing[@]}" -gt 0 ]]; then
    die "missing required commands: ${missing[*]}"
  fi
}

main() {
  preflight

  local base_sha="${BASE_SHA:-}"
  local head_sha="${HEAD_SHA:-}"
  local output="${GITHUB_OUTPUT:-}"

  [[ -n "${base_sha}" ]] || die "BASE_SHA is required"
  [[ -n "${head_sha}" ]] || die "HEAD_SHA is required"
  [[ -n "${output}" ]] || die "GITHUB_OUTPUT is required"

  printf 'detecting plugin changes between %s..%s\n' "${base_sha}" "${head_sha}"

  local changed_files
  changed_files="$(git diff --name-only "${base_sha}" "${head_sha}" -- 'plugins/**' || true)"

  if [[ -z "${changed_files}" ]]; then
    printf 'no plugin changes detected\n'
    {
      printf 'has_changes=false\n'
      printf 'changed_plugins=[]\n'
    } >>"${output}"
    return 0
  fi

  printf 'changed files:\n%s\n' "${changed_files}"

  local plugins
  plugins="$(printf '%s\n' "${changed_files}" \
    | awk -F'/' 'NF >= 2 && $2 != "" {print $2}' \
    | sort -u)"

  if [[ -z "${plugins}" ]]; then
    {
      printf 'has_changes=false\n'
      printf 'changed_plugins=[]\n'
    } >>"${output}"
    return 0
  fi

  local json_array
  json_array="$(printf '%s\n' "${plugins}" | jq -R . | jq -sc .)"

  printf 'changed plugins: %s\n' "${json_array}"

  {
    printf 'has_changes=true\n'
    printf 'changed_plugins=%s\n' "${json_array}"
  } >>"${output}"
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  main "$@"
fi
