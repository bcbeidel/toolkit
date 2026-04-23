#!/usr/bin/env bash
#
# check_structure.sh — Deterministic Tier-1 structural checks for
# Python scripts: shebang, __main__ guard shape, main() return
# annotation, KeyboardInterrupt handler, executable bit.
#
# Thin wrapper around _ast_checks.py structure <file>. Lives next to
# the helper; resolves it via the script's own directory so paths are
# stable regardless of the invoker's cwd.
#
# Usage:
#   check_structure.sh <path> [<path> ...]
#
# Paths may be .py files or directories (top-level .py only — scripts
# are single-file by definition, no recursion into subpackages).
#
# Exit codes:
#   0   no FAIL findings
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
check_structure.sh — Structural checks for Python scripts.

Usage:
  check_structure.sh <path> [<path> ...]

Checks:
  shebang             first line is exactly '#!/usr/bin/env python3'
  guard               '__main__' guard exists and invokes sys.exit(main())
  main-returns        main() signature declares '-> int'
  keyboard-interrupt  main() has an 'except KeyboardInterrupt' handler
  exec-bit            executable bit set when shebang present

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
    python3)            printf 'brew install python  |  apt install python3  |  dnf install python3' ;;
    find|basename)      printf 'should be preinstalled on any POSIX system' ;;
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
  if [ ! -f "${HELPER}" ]; then
    printf '%s: helper not found: %s\n' "${PROGNAME}" "${HELPER}" >&2
    exit 69
  fi
}

check_file() {
  # Propagate helper exit code: 1 on FAIL, 0 on clean/WARN/INFO-only.
  python3 "${HELPER}" structure "$1" || return "$?"
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
