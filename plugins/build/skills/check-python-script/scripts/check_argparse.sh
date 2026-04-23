#!/usr/bin/env bash
#
# check_argparse.sh — Deterministic Tier-1 argparse / subprocess checks
# for Python scripts: argparse-when-sys.argv, add_argument help=,
# subprocess.run check=True / return-inspected.
#
# Thin wrapper around _ast_checks.py argparse <file>.
#
# Usage:
#   check_argparse.sh <path> [<path> ...]
#
# Exit codes:
#   0   no FAIL findings (all emitted findings are WARN — exits 0)
#   1   one or more FAIL findings
#   64  usage error
#   69  missing dependency
#
# Dependencies:
#   python3, find, basename

set -Eeuo pipefail
IFS=$'\n\t'

PROGNAME="$(basename "${0}")"
SCRIPT_DIR="$(cd "$(dirname "${0}")" && pwd)"
HELPER="${SCRIPT_DIR}/_ast_checks.py"

REQUIRED_CMDS=(python3 find basename)

usage() {
  cat <<'EOF'
check_argparse.sh — argparse / subprocess checks for Python scripts.

Usage:
  check_argparse.sh <path> [<path> ...]

Checks:
  argparse-when-argv  argparse imported when sys.argv accessed past [0]
  add-argument-help   every add_argument() carries a non-empty help=
  subprocess-check    subprocess.run() sets check=True or inspects result

Options:
  -h, --help   Show this help and exit.

Exit codes:
  0   no FAIL findings
  1   one or more FAIL findings
  64  usage error
  69  missing dependency
EOF
}

install_hint() {
  case "${1}" in
    python3)       printf 'brew install python  |  apt install python3  |  dnf install python3' ;;
    find|basename) printf 'should be preinstalled on any POSIX system' ;;
    *)             printf 'see your package manager' ;;
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
  if [ ! -f "${HELPER}" ]; then
    printf '%s: helper not found: %s\n' "${PROGNAME}" "${HELPER}" >&2
    exit 69
  fi
}

check_file() {
  python3 "${HELPER}" argparse "$1" || return "$?"
}

check_path() {
  local target="$1"
  local any=0
  local file

  if [ -f "${target}" ]; then
    case "${target}" in
      *.py) check_file "${target}" || any=1 ;;
    esac
  elif [ -d "${target}" ]; then
    while IFS= read -r file; do
      check_file "${file}" || any=1
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
    check_path "${target}" || any=1
  done

  exit "${any}"
}

if [ "${0}" = "${BASH_SOURCE[0]:-$0}" ]; then
  main "$@"
fi
