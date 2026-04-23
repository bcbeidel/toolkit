#!/usr/bin/env bash
#
# check_shfmt.sh — Deterministic Tier-1 format check for Bash scripts,
# wrapping the external `shfmt` tool.
#
# `shfmt` is optional — when absent, this script emits a single INFO
# line and exits 0, matching the Missing Tools preamble pattern.
#
# Format flags: `-i 2 -ci -bn` per the bash-script-best-practices.md
# style guidance (2-space indent, switch-case indent, binop on next
# line). Aligns with Google Shell Style Guide.
#
# Usage:
#   check_shfmt.sh <path> [<path> ...]
#
# Exit codes:
#   0   no FAIL findings (including when shfmt is absent)
#   1   one or more FAIL findings (not produced — format drift is WARN)
#   64  usage error
#   69  missing required dependency (not shfmt)

set -Eeuo pipefail
IFS=$'\n\t'

PROGNAME="$(basename "${0}")"

REQUIRED_CMDS=(find basename head)

SHFMT_FLAGS=(-i 2 -ci -bn)

usage() {
  cat <<'EOF'
check_shfmt.sh — shfmt format check for Bash scripts.

Usage:
  check_shfmt.sh <path> [<path> ...]

shfmt is optional. When absent, one INFO line is emitted and the
script exits 0.

Options:
  -h, --help   Show this help and exit.

Exit codes:
  0   no FAIL findings
  1   one or more FAIL findings (not produced by this script)
  64  usage error
  69  missing required dependency (not shfmt)
EOF
}

install_hint() {
  case "${1}" in
    find|basename|head) printf 'should be preinstalled on any POSIX system' ;;
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

is_bash_script() {
  local file="$1"
  case "${file}" in
    *.sh|*.bash) return 0 ;;
  esac
  local first
  first="$(head -n 1 "${file}" 2>/dev/null || true)"
  case "${first}" in
    "#!/usr/bin/env bash"|"#!/bin/bash"|"#!/usr/bin/env -S bash"*) return 0 ;;
  esac
  return 1
}

check_one() {
  local target="$1"
  if shfmt "${SHFMT_FLAGS[@]}" -d "${target}" >/dev/null 2>&1; then
    return 0
  fi
  printf 'WARN  %s — format: shfmt -d reports drift\n' "${target}"
  printf "  Recommendation: Run 'shfmt -i 2 -ci -bn -w %s' to apply the canonical format.\n" \
    "${target}"
}

check_path() {
  local target="$1"
  local file

  if [ -f "${target}" ]; then
    if is_bash_script "${target}"; then
      check_one "${target}"
    fi
  elif [ -d "${target}" ]; then
    while IFS= read -r file; do
      if is_bash_script "${file}"; then
        check_one "${file}"
      fi
    done < <(find "${target}" -maxdepth 1 -type f \( -name '*.sh' -o -name '*.bash' -o ! -name '*.*' \) 2>/dev/null)
  else
    printf '%s: path not found: %s\n' "${PROGNAME}" "${target}" >&2
    return 64
  fi
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

  if ! command -v shfmt >/dev/null 2>&1; then
    printf 'INFO  <shfmt> — tool-missing: shfmt not installed; format check skipped\n'
    printf "  Recommendation: Install shfmt — 'brew install shfmt' (macOS), "
    printf "'apt install shfmt' (Debian/Ubuntu), 'go install mvdan.cc/sh/v3/cmd/shfmt@latest'.\n"
    exit 0
  fi

  local target
  for target in "$@"; do
    check_path "${target}" || exit "$?"
  done

  exit 0
}

if [ "${0}" = "${BASH_SOURCE[0]:-$0}" ]; then
  main "$@"
fi
