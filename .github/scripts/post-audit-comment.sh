#!/usr/bin/env bash
#
# post-audit-comment.sh — upsert a security-audit comment on a PR.
#
# The comment body is written by write-comment.py and already contains the
# stable HTML marker `<!-- skill-audit:report -->` on its first line. This
# script finds an existing comment carrying the same marker and PATCHes it,
# or POSTs a new one if none exists. The fixed marker means one audit
# comment per PR — multi-plugin PRs will see the latest plugin's report.
#
# Usage:
#   PR_NUMBER=123 \
#   COMMENT_FILE=scan-output/<plugin>/audit-comment.md \
#   GITHUB_REPOSITORY=owner/repo \
#   GH_TOKEN=<token> \
#     ./post-audit-comment.sh
#
# Dependencies: gh, jq
#
# Exit codes:
#   0   comment posted or updated
#   1   missing required env or comment file
#   2   gh api call failed

set -euo pipefail

PROGNAME="$(basename "${0}")"
readonly PROGNAME

readonly MARKER='<!-- skill-audit:report -->'

REQUIRED_CMDS=(gh jq)

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

  local pr_number="${PR_NUMBER:-}"
  local comment_file="${COMMENT_FILE:-audit-comment.md}"
  local repo="${GITHUB_REPOSITORY:-}"

  [[ -n "${pr_number}" ]] || die "PR_NUMBER is required"
  [[ -n "${repo}" ]] || die "GITHUB_REPOSITORY is required"
  [[ -f "${comment_file}" ]] || die "comment file not found: ${comment_file}"

  local body
  body="$(cat "${comment_file}")"

  if ! grep -q 'skill-audit:report' <<<"${body}"; then
    die "comment body missing required marker: ${MARKER}"
  fi

  local existing_id
  existing_id="$(
    gh api "repos/${repo}/issues/${pr_number}/comments" \
      --jq "[.[] | select(.body | contains(\"${MARKER}\"))] | first | .id // empty" \
      2>/dev/null || true
  )"

  if [[ -n "${existing_id}" ]]; then
    printf 'updating existing audit comment %s\n' "${existing_id}"
    gh api "repos/${repo}/issues/comments/${existing_id}" \
      --method PATCH \
      --field "body=${body}" \
      --silent \
      || die "PATCH failed for comment ${existing_id}"
    printf 'comment updated\n'
  else
    printf 'creating new audit comment\n'
    gh api "repos/${repo}/issues/${pr_number}/comments" \
      --field "body=${body}" \
      --silent \
      || die "POST failed for PR ${pr_number}"
    printf 'comment posted\n'
  fi
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  main "$@"
fi
