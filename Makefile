# Makefile — local entry points for the skill security scanner.
#
# Mirrors the CI scan workflow: same policy file, same hash-locked deps,
# same --fail-on-severity threshold, same scan-output/<plugin>/findings.json
# layout. A clean local scan should match what CI produces on the same SHA.
#
# Usage:
#   make help                       # show targets
#   make scan PLUGIN=build          # scan one plugin
#   make scan-all                   # scan every plugins/<name>/
#   make scan-clean                 # remove scan-output/

SHELL := bash
.SHELLFLAGS := -eu -o pipefail -c
MAKEFLAGS += --no-builtin-rules --no-builtin-variables --warn-undefined-variables
.DELETE_ON_ERROR:
.DEFAULT_GOAL := help

PLUGIN ?=
SCAN_OUTPUT_DIR ?= scan-output
POLICY_FILE ?= policy/skill-scan-policy.yml
REQUIREMENTS_LOCK ?= .github/scripts/requirements.lock
REQUIREMENTS_TXT ?= .github/scripts/requirements.txt
SKILL_SCANNER ?= skill-scanner
SKILL_SCANNER_LLM_MODEL ?= anthropic/claude-opus-4-6
FAIL_ON_SEVERITY ?= high

.PHONY: help scan scan-all scan-clean

help: ## Show this help and exit
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*## / {printf "  \033[36m%-14s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

scan: ## Scan one plugin (PLUGIN=<name> required)
	if [[ -z "$(PLUGIN)" ]]; then \
		echo "error: PLUGIN=<name> is required" >&2; \
		exit 2; \
	fi
	if [[ ! -d "plugins/$(PLUGIN)" ]]; then \
		echo "error: plugins/$(PLUGIN) does not exist" >&2; \
		exit 2; \
	fi
	if [[ -z "$${ANTHROPIC_API_KEY:-}" ]]; then \
		echo "error: ANTHROPIC_API_KEY must be set" >&2; \
		exit 2; \
	fi
	@mkdir -p "$(SCAN_OUTPUT_DIR)/$(PLUGIN)"
	@echo "── prohibited-files check ──"
	@PLUGIN_DIR="plugins/$(PLUGIN)" \
	 POLICY_FILE="$(POLICY_FILE)" \
	 FINDINGS_OUT="$(SCAN_OUTPUT_DIR)/$(PLUGIN)/findings.json" \
		bash .github/scripts/check-prohibited-files.sh
	@echo "── skill-scanner ──"
	SKILL_SCANNER_LLM_MODEL="$(SKILL_SCANNER_LLM_MODEL)" \
	SKILL_SCANNER_LLM_API_KEY="$$ANTHROPIC_API_KEY" \
		$(SKILL_SCANNER) scan-all \
			"plugins/$(PLUGIN)" \
			--recursive \
			--use-llm \
			--format json \
			--output "$(SCAN_OUTPUT_DIR)/$(PLUGIN)/findings.json" \
			--fail-on-severity $(FAIL_ON_SEVERITY)
	@echo "findings written to $(SCAN_OUTPUT_DIR)/$(PLUGIN)/findings.json"

scan-all: ## Scan every plugins/<name>/
	@echo "scanning all plugins..."
	@for plugin in plugins/*/; do \
		name=$$(basename $$plugin); \
		echo "── $$name ──"; \
		$(MAKE) --no-print-directory scan PLUGIN="$$name" || true; \
	done
	@# `|| true` above so one plugin's HIGH finding does not abort the rest;
	@# each plugin's exit status is preserved in its findings.json.
	@echo "done. review $(SCAN_OUTPUT_DIR)/<plugin>/findings.json for each plugin."

scan-clean: ## Remove the scan-output tree
	[[ -n "$(SCAN_OUTPUT_DIR)" ]] || { echo "SCAN_OUTPUT_DIR is empty; refusing to rm" >&2; exit 1; }
	rm -rf -- "$(SCAN_OUTPUT_DIR)"
	@echo "removed $(SCAN_OUTPUT_DIR)"
