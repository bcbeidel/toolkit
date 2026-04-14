#!/usr/bin/env bash
# skill-lint.sh: post-write lint check for SKILL.md files
# Event: PostToolUse (Write | Edit | MultiEdit on *SKILL.md)
# PostToolUse is advisory — this hook cannot block execution

set -Eeuo pipefail

command -v jq &>/dev/null || { echo "skill-lint: jq required" >&2; exit 0; }

INPUT=$(cat)

TOOL_NAME="$(echo "${INPUT}" | jq -r '.tool_name // empty')"
case "${TOOL_NAME}" in
  Write)
    FILE_PATH="$(echo "${INPUT}" | jq -r '.tool_input.file_path // empty')"
    ;;
  Edit|MultiEdit)
    FILE_PATH="$(echo "${INPUT}" | jq -r '.tool_input.path // empty')"
    ;;
  *)
    exit 0
    ;;
esac

[[ -z "${FILE_PATH}" ]] && exit 0

# Resolve relative paths using cwd from payload
CWD="$(echo "${INPUT}" | jq -r '.cwd // empty')"
if [[ -n "${CWD}" && "${FILE_PATH}" != /* ]]; then
  FILE_PATH="${CWD}/${FILE_PATH}"
fi

# Project root: .claude/hooks/ is 2 levels below project root
HOOK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${HOOK_DIR}/../.." && pwd)"
LINT_SCRIPT="${PROJECT_ROOT}/scripts/lint.py"

if [[ ! -f "${LINT_SCRIPT}" ]]; then
  echo "skill-lint: scripts/lint.py not found at ${PROJECT_ROOT}" >&2
  exit 0
fi

echo "skill-lint: ${FILE_PATH#"${PROJECT_ROOT}/"}" >&2
python "${LINT_SCRIPT}" "${FILE_PATH}" --root "${PROJECT_ROOT}" --no-urls >&2 || true

exit 0
