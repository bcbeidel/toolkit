#!/usr/bin/env bash
#
# check_ruff.sh — Deterministic Tier-1 lint / format check for Python
# scripts, wrapping the external `ruff` tool and reshaping its output
# to the fixed lint format.
#
# Ruff is optional — when absent, this script emits a single INFO line
# naming the reduced coverage and exits 0, matching the peer
# check-shell's Missing Tools preamble pattern. Other Tier-1 scripts
# continue running.
#
# Covers:
#   D100      module docstring missing                     WARN
#   E722      bare except:                                 FAIL
#   SIM115    open() not wrapped in with                   WARN
#   PLW1514   text-mode open() missing encoding=           WARN
#   PTH       os.path.* where pathlib.Path fits            WARN
#   S602/604  shell=True in subprocess                     FAIL
#   S307      eval / exec                                  FAIL
#   F401      unused imports                               WARN
#   ANN       missing type annotations (ANN001/201/204)    WARN
#   F403      wildcard imports                             FAIL
#   S108      hardcoded /tmp/ path literals                FAIL
#   UP031     %-format where f-string fits                 WARN
#   UP032     .format() where f-string fits                WARN
#   format    `ruff format --check` drift                  WARN
#
# Usage:
#   check_ruff.sh <path> [<path> ...]
#
# Exit codes:
#   0   no FAIL findings (including when ruff is absent)
#   1   one or more FAIL findings
#   64  usage error
#   69  missing dependency (python3 / awk — not ruff)

set -Eeuo pipefail
IFS=$'\n\t'

PROGNAME="$(basename "${0}")"

REQUIRED_CMDS=(awk find basename)

# Rule codes that escalate to FAIL; all other ruff findings are WARN.
# S604 is included with S602 (subprocess shell=True variants).
FAIL_CODES="E722 F403 S108 S307 S602 S604"

# The explicit selector set we pass to ruff. Kept in lockstep with the
# severity map in emit_finding() so drift is visible at review time.
RUFF_SELECT="D100,E722,SIM115,PLW1514,PTH,S602,S604,S307,F401,ANN,F403,S108,UP031,UP032"

usage() {
  cat <<'EOF'
check_ruff.sh — Ruff-backed lint and format check for Python scripts.

Usage:
  check_ruff.sh <path> [<path> ...]

Ruff is optional. When absent, one INFO line is emitted naming the
reduced coverage and the script exits 0.

Options:
  -h, --help   Show this help and exit.

Exit codes:
  0   no FAIL findings
  1   one or more FAIL findings
  64  usage error
  69  missing required dependency (not ruff)
EOF
}

install_hint() {
  case "${1}" in
    awk|find|basename) printf 'should be preinstalled on any POSIX system' ;;
    python3)           printf 'brew install python  |  apt install python3  |  dnf install python3' ;;
    *)                 printf 'see your package manager' ;;
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

# Return "FAIL" or "WARN" for a ruff rule code.
severity_for() {
  local code="$1"
  case " ${FAIL_CODES} " in
    *" ${code} "*) printf 'FAIL' ;;
    *)             printf 'WARN' ;;
  esac
}

# Given a ruff rule code, emit a one-line repair hint.
recommend_for() {
  case "$1" in
    D100)    printf 'Add a module docstring as the first statement, naming the purpose and one example invocation.' ;;
    E722)    printf 'Catch a specific exception type (FileNotFoundError, ValueError, ...) or use except Exception as err in main().' ;;
    SIM115)  printf "Wrap the open() in a with statement so cleanup runs on exceptions." ;;
    PLW1514) printf "Pass encoding='utf-8' to open() to avoid platform-dependent defaults." ;;
    PTH*)    printf 'Use pathlib.Path instead of os.path string manipulation.' ;;
    S602|S604) printf 'Pass subprocess args as a list; never shell=True with interpolated input.' ;;
    S307)    printf 'Replace eval/exec with ast.literal_eval or an explicit dispatch table.' ;;
    F401)    printf 'Remove the unused import.' ;;
    ANN*)    printf 'Add type annotations to the function signature.' ;;
    F403)    printf 'Replace wildcard import with explicit named imports.' ;;
    S108)    printf 'Use tempfile.TemporaryDirectory()/NamedTemporaryFile() instead of hand-built /tmp paths.' ;;
    UP031|UP032) printf 'Rewrite as an f-string.' ;;
    *)       printf 'See the ruff docs for this rule.' ;;
  esac
}

# Parse one ruff concise line: `<path>:<line>:<col>: <code> <message>`.
# Emit a single Tier-1 finding in the fixed format. Return FAIL status
# through the exit variable in the caller (uses global for bash-3.2).
emit_finding() {
  local line="$1"
  local path lineno col code message severity
  # Split on the first three colons only (paths can contain them too;
  # relative paths typically don't, so this is robust in practice).
  path="${line%%:*}"
  line="${line#*:}"
  lineno="${line%%:*}"
  line="${line#*:}"
  col="${line%%:*}"
  line="${line#*:}"
  # Remaining: " <code> <message>"
  line="${line# }"
  code="${line%% *}"
  message="${line#* }"

  severity="$(severity_for "${code}")"
  printf '%s  %s — ruff-%s: %s (line %s:%s)\n' \
    "${severity}" "${path}" "${code}" "${message}" "${lineno}" "${col}"
  printf '  Recommendation: %s\n' "$(recommend_for "${code}")"

  if [ "${severity}" = "FAIL" ]; then
    return 1
  fi
  return 0
}

check_one() {
  local target="$1"
  local any=0
  local line

  # `ruff check` exits 1 when findings present; we want the output regardless.
  # `ruff check` output format: `<path>:<line>:<col>: <code> <message>`.
  while IFS= read -r line; do
    # Skip ruff's trailing summary lines ("Found N errors.").
    case "${line}" in
      ""|"Found "*|"All checks passed"*) continue ;;
    esac
    emit_finding "${line}" || any=1
  done < <(ruff check --no-cache --output-format=concise --select="${RUFF_SELECT}" "${target}" 2>/dev/null || true)

  # Format drift — separate invocation.
  if ! ruff format --check --no-cache "${target}" >/dev/null 2>&1; then
    printf 'WARN  %s — ruff-format: formatter drift detected\n' "${target}"
    printf "  Recommendation: Run 'ruff format %s' to fix.\n" "${target}"
  fi

  return "${any}"
}

check_path() {
  local target="$1"
  local any=0
  local file

  if [ -f "${target}" ]; then
    case "${target}" in
      *.py) check_one "${target}" || any=1 ;;
    esac
  elif [ -d "${target}" ]; then
    while IFS= read -r file; do
      check_one "${file}" || any=1
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

  # Ruff is optional — emit an INFO and exit 0 if absent.
  if ! command -v ruff >/dev/null 2>&1; then
    printf 'INFO  <ruff> — tool-missing: ruff not installed; %d AST/format checks skipped\n' 14
    printf "  Recommendation: Install ruff to enable D100 / E722 / SIM115 / PLW1514 / "
    printf 'PTH / S602 / S307 / F401 / ANN / F403 / S108 / UP031 / UP032 / format checks. '
    printf "Try 'pip install ruff' or 'brew install ruff'.\n"
    exit 0
  fi

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
