#!/usr/bin/env bash
#
# check-prohibited-files.sh — fail-fast pre-scan check for opaque
# artifacts (binaries, archives) inside a plugin directory.
#
# Reads the prohibited-extension list from the policy file so the
# rule lives there, not here. Runs before the LLM scanner because
# opaque content cannot be reviewed by the scanner or by humans.
#
# Usage:
#   PLUGIN_DIR=plugins/<name> \
#   POLICY_FILE=policy/skill-scan-policy.yml \
#   FINDINGS_OUT=scan-output/<name>/findings.json \
#     ./check-prohibited-files.sh
#
# Dependencies: awk, find, python3 (only when FINDINGS_OUT is set)
#
# Exit codes:
#   0   no prohibited files found
#   1   one or more prohibited files found
#   2   misconfiguration (missing PLUGIN_DIR or policy file)

set -euo pipefail

PROGNAME="$(basename "${0}")"
readonly PROGNAME

die() {
  printf 'error: %s\n' "$*" >&2
  exit 2
}

extract_extensions() {
  awk '
    /^prohibited_extensions:/ { in_block = 1; next }
    in_block && /^[a-zA-Z]/    { in_block = 0 }
    in_block && /^[[:space:]]*-/ {
      gsub(/^[[:space:]]*-[[:space:]]*/, "")
      gsub(/[[:space:]]+$/, "")
      print
    }
  ' "${1}"
}

main() {
  local plugin_dir="${PLUGIN_DIR:-}"
  local policy_file="${POLICY_FILE:-policy/skill-scan-policy.yml}"
  local findings_out="${FINDINGS_OUT:-}"

  [[ -n "${plugin_dir}" ]] || die "PLUGIN_DIR is required"
  [[ -d "${plugin_dir}" ]] || die "plugin directory not found: ${plugin_dir}"
  [[ -f "${policy_file}" ]] || die "policy file not found: ${policy_file}"

  local extensions
  extensions="$(extract_extensions "${policy_file}")"

  if [[ -z "${extensions}" ]]; then
    printf 'warning: no prohibited_extensions parsed from %s\n' "${policy_file}" >&2
  fi

  printf 'scanning %s for prohibited file types...\n' "${plugin_dir}"

  local find_args=()
  local first=1
  local ext
  while IFS= read -r ext; do
    [[ -z "${ext}" ]] && continue
    if [[ "${first}" -eq 1 ]]; then
      find_args+=("-name" "*${ext}")
      first=0
    else
      find_args+=("-o" "-name" "*${ext}")
    fi
  done <<<"${extensions}"

  local violations=()
  local match
  if [[ "${#find_args[@]}" -gt 0 ]]; then
    while IFS= read -r match; do
      [[ -n "${match}" ]] && violations+=("${match}")
    done < <(find "${plugin_dir}" -type f \( "${find_args[@]}" \) 2>/dev/null)
  fi

  if command -v file >/dev/null 2>&1; then
    local path mime skip v
    while IFS= read -r path; do
      skip=0
      for v in "${violations[@]:-}"; do
        if [[ "${v}" == "${path}" ]]; then
          skip=1
          break
        fi
      done
      [[ "${skip}" -eq 1 ]] && continue

      mime="$(file --brief --mime-type "${path}" 2>/dev/null || true)"
      case "${mime}" in
        text/* | inode/x-empty | application/json | application/xml) ;;
        application/x-yaml | application/x-sh | application/javascript) ;;
        "") ;;
        *) violations+=("${path} (mime: ${mime})") ;;
      esac
    done < <(find "${plugin_dir}" -type f 2>/dev/null)
  fi

  if [[ "${#violations[@]}" -eq 0 ]]; then
    printf 'ok — no prohibited files found in %s\n' "${plugin_dir}"
    return 0
  fi

  printf '\nPROHIBITED FILES DETECTED in %s:\n' "${plugin_dir}"
  local item
  for item in "${violations[@]}"; do
    printf '  - %s\n' "${item}"
  done
  printf '\nPlugins may not contain binaries, archives, or other opaque artifacts.\n'
  printf 'Remove the files above (or move binary assets to an external, audited location).\n'
  printf 'Policy: %s  (key: prohibited_extensions)\n' "${policy_file}"

  if [[ -n "${findings_out}" ]]; then
    mkdir -p "$(dirname "${findings_out}")"
    python3 - "${findings_out}" "${violations[@]}" <<'PY'
import json
import sys

out_path = sys.argv[1]
violations = sys.argv[2:]
findings = [
    {
        "rule_id": "PROHIBITED_BINARY_OR_ARCHIVE",
        "severity": "critical",
        "analyzer": "policy",
        "description": f"Prohibited file in plugin: {v}",
    }
    for v in violations
]
payload = {"findings": findings, "scan_failed": True, "skip_reason": "prohibited_files"}
with open(out_path, "w") as f:
    json.dump(payload, f, indent=2)
PY
    printf 'synthetic findings written to %s\n' "${findings_out}"
  fi

  exit 1
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  main "$@"
fi
