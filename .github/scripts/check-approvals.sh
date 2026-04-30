#!/usr/bin/env bash
#
# check-approvals.sh — label-based merge gate.
#
# Reads risk-summary.json and decides whether the PR may merge:
#   - scan_failed=true        → exit 1 (always block; scan failure is not a pass)
#   - overall_severity=high   → require the `security-override` PR label
#   - any other severity      → exit 0 (pass)
#
# A label-based override (rather than approval-count) keeps the policy simple
# for a single-author repository and records the override decision as a
# label on the PR.
#
# Usage:
#   PR_NUMBER=123 \
#   SUMMARY_FILE=scan-output/<plugin>/risk-summary.json \
#   GH_TOKEN=<token> \
#     ./check-approvals.sh
#
# Dependencies: gh, jq
#
# Exit codes:
#   0   gate passes
#   1   gate fails (HIGH without override, or scan_failed)
#   2   misconfiguration (missing env, missing summary file)

set -euo pipefail

PROGNAME="$(basename "${0}")"
readonly PROGNAME

readonly OVERRIDE_LABEL="security-override"

REQUIRED_CMDS=(gh jq)

die() {
  printf 'error: %s\n' "$*" >&2
  exit 2
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

  local pr_number="${PR_NUMBER:-}"
  local summary_file="${SUMMARY_FILE:-risk-summary.json}"

  [[ -n "${pr_number}" ]] || die "PR_NUMBER is required"
  [[ -f "${summary_file}" ]] || die "summary file not found: ${summary_file}"

  local severity scan_failed
  severity="$(jq -r '.overall_severity // "none"' "${summary_file}")"
  scan_failed="$(jq -r '.scan_failed // false' "${summary_file}")"

  printf 'gate: severity=%s scan_failed=%s\n' "${severity}" "${scan_failed}"

  if [[ "${scan_failed}" == "true" ]]; then
    printf 'GATE FAIL: scan_failed=true; merge blocked unconditionally\n'
    exit 1
  fi

  if [[ "${severity}" != "high" ]]; then
    printf 'GATE PASS: severity=%s\n' "${severity}"
    exit 0
  fi

  local labels
  labels="$(gh pr view "${pr_number}" --json labels --jq '.labels[].name' 2>/dev/null || true)"

  if grep -Fxq "${OVERRIDE_LABEL}" <<<"${labels}"; then
    printf 'GATE PASS: severity=high overridden via "%s" label\n' "${OVERRIDE_LABEL}"
    exit 0
  fi

  printf 'GATE FAIL: severity=high and "%s" label not present\n' "${OVERRIDE_LABEL}" >&2
  printf 'apply the "%s" label and re-run this check to merge.\n' "${OVERRIDE_LABEL}" >&2
  exit 1
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  main "$@"
fi
