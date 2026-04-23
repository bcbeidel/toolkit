#!/usr/bin/env bash
#
# scan_dangerous_patterns.sh — Tier-1 scan for unverified remote-exec
# and destructive commands inside shell code blocks.
#
# Remote-exec patterns:     curl | bash, wget | bash, eval $(curl ...),
#                           source <(curl ...) and variants.
# Destructive commands:     rm -rf, dd if=, DROP TABLE, TRUNCATE,
#                           force-push (git push -f / --force),
#                           mv without -i / -n.
#
# All findings emit WARN — destructive commands are often legitimate
# when gated; remote-exec is discouraged but occasionally needed (pin
# + hash-verify). Tier-2 Safety Gating judges whether an approval
# gate exists.
#
# Scope: only matches inside fenced code blocks whose language tag
# is one of bash / sh / zsh / shell / console (or no tag). Prose
# hits are deliberately ignored.
#
# Usage:
#   scan_dangerous_patterns.sh <path> [<path> ...]
#
# Exit codes:
#   0   always (WARN only)
#   64  usage error
#   69  missing dependency
#
# Dependencies:
#   awk, find, basename

set -Eeuo pipefail
IFS=$'\n\t'

PROGNAME="$(basename "${0}")"
REQUIRED_CMDS=(awk find basename)

usage() {
  cat <<'EOF'
scan_dangerous_patterns.sh — Remote-exec and destructive-command scan.

Usage:
  scan_dangerous_patterns.sh <path> [<path> ...]

Detects (in shell code blocks only):
  Remote exec         curl | bash, wget | bash, eval $(curl ...),
                      source <(curl ...)
  Destructive cmds    rm -rf, dd if=, DROP TABLE, TRUNCATE, force-push,
                      mv without -i / -n

Options:
  -h, --help   Show this help and exit.

Exit codes:
  0   always (WARN only; no FAILs emitted)
  64  usage error
  69  missing dependency
EOF
}

install_hint() {
  case "${1}" in
    awk|find|basename) printf 'should be preinstalled on any POSIX system' ;;
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

emit_warn() {
  local path="$1" check="$2" detail="$3" rec="$4"
  printf 'WARN  %s — %s: %s\n' "${path}" "${check}" "${detail}"
  printf '  Recommendation: %s\n' "${rec}"
}

scan_file() {
  local file="$1"
  # awk emits lines of form: LINE_NO\tCATEGORY\tDETAIL
  local hits
  hits="$(awk '
    function is_shell_tag(tag) {
      if (tag == "") return 1
      return tag == "bash" || tag == "sh" || tag == "zsh" || tag == "shell" || tag == "console"
    }
    BEGIN {
      in_fence = 0
      shell_fence = 0
    }
    {
      line = $0
      if (line ~ /^[[:space:]]*```/) {
        if (!in_fence) {
          in_fence = 1
          tag = line
          sub(/^[[:space:]]*```/, "", tag)
          sub(/[[:space:]]+$/, "", tag)
          shell_fence = is_shell_tag(tag) ? 1 : 0
        } else {
          in_fence = 0
          shell_fence = 0
        }
        next
      }
      if (line ~ /^[[:space:]]*~~~/) {
        if (!in_fence) {
          in_fence = 1
          tag = line
          sub(/^[[:space:]]*~~~/, "", tag)
          sub(/[[:space:]]+$/, "", tag)
          shell_fence = is_shell_tag(tag) ? 1 : 0
        } else {
          in_fence = 0
          shell_fence = 0
        }
        next
      }
      if (!in_fence || !shell_fence) next

      # Remote-exec patterns
      if (line ~ /curl[^|]*\|[[:space:]]*(sudo[[:space:]]+)?(bash|sh|zsh)/) {
        print NR "\tRemote exec\tcurl piped to a shell"
      }
      if (line ~ /wget[^|]*\|[[:space:]]*(sudo[[:space:]]+)?(bash|sh|zsh)/) {
        print NR "\tRemote exec\twget piped to a shell"
      }
      if (line ~ /eval[[:space:]]*\$\([[:space:]]*curl/) {
        print NR "\tRemote exec\teval $(curl ...) pattern"
      }
      if (line ~ /eval[[:space:]]*\$\([[:space:]]*wget/) {
        print NR "\tRemote exec\teval $(wget ...) pattern"
      }
      if (line ~ /source[[:space:]]+<\([[:space:]]*curl/) {
        print NR "\tRemote exec\tsource <(curl ...) pattern"
      }
      if (line ~ /\.[[:space:]]+<\([[:space:]]*curl/) {
        print NR "\tRemote exec\t. <(curl ...) pattern"
      }

      # Destructive commands
      if (line ~ /(^|[^A-Za-z0-9_])rm[[:space:]]+(-[A-Za-z]*r[A-Za-z]*f|-[A-Za-z]*f[A-Za-z]*r|-rf|-fr)/) {
        print NR "\tDestructive cmd\trm -rf variant"
      }
      if (line ~ /(^|[^A-Za-z0-9_])dd[[:space:]]+[^#]*if=/) {
        print NR "\tDestructive cmd\tdd if= (can overwrite devices)"
      }
      if (line ~ /DROP[[:space:]]+TABLE[[:space:]]+/) {
        print NR "\tDestructive cmd\tSQL DROP TABLE"
      }
      if (line ~ /DROP[[:space:]]+DATABASE[[:space:]]+/) {
        print NR "\tDestructive cmd\tSQL DROP DATABASE"
      }
      if (line ~ /(^|[^A-Za-z0-9_])TRUNCATE[[:space:]]+/) {
        print NR "\tDestructive cmd\tSQL TRUNCATE"
      }
      if (line ~ /git[[:space:]]+push[[:space:]]+[^#]*(-f([[:space:]]|$)|--force([[:space:]=]|$))/) {
        print NR "\tDestructive cmd\tgit push --force"
      }
      # mv without -i or -n (basic heuristic; skip if -i / -n present on the line)
      if (line ~ /(^|[^A-Za-z0-9_])mv[[:space:]]+/ && line !~ /mv[[:space:]]+(-[^[:space:]]*[in]|--interactive|--no-clobber)/) {
        # Skip mv with --help/--version style
        if (line !~ /mv[[:space:]]+(-{1,2}help|-{1,2}version)/) {
          print NR "\tDestructive cmd\tmv without -i / -n safety flag"
        }
      }
    }
  ' "${file}")"
  [ -n "${hits}" ] || return 0
  local row line_no category detail
  while IFS= read -r row; do
    [ -n "${row}" ] || continue
    line_no="$(printf '%s' "${row}" | awk -F'\t' '{print $1}')"
    category="$(printf '%s' "${row}" | awk -F'\t' '{print $2}')"
    detail="$(printf '%s' "${row}" | awk -F'\t' '{print $3}')"
    emit_warn "${file}" "${category}" \
      "line ${line_no}: ${detail}" \
      "Precede with an explicit approval gate or convert to a dry-run default; for curl|bash, pin a version and verify a hash"
  done <<<"${hits}"
  return 0
}

check_path() {
  local target="$1"
  local file
  if [ -f "${target}" ]; then
    scan_file "${target}"
  elif [ -d "${target}" ]; then
    while IFS= read -r file; do
      scan_file "${file}"
    done < <(
      find "${target}" -type f -name 'SKILL.md' \
        -not -path '*/_shared/*' \
        2>/dev/null
    )
  else
    printf '%s: path not found: %s\n' "${PROGNAME}" "${target}" >&2
    return 64
  fi
  return 0
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
  local target
  for target in "$@"; do
    check_path "${target}" || exit 64
  done
  exit 0
}

if [ "${0}" = "${BASH_SOURCE[0]:-$0}" ]; then
  main "$@"
fi
