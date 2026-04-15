# Ad-Hoc Validation

Protocol for building a validation hypothesis without a plan. Three signal
sources produce a prioritized criteria list for user confirmation.

## 1. Git Diff Analysis

Gather changes from both the branch and working tree:

```bash
git diff main...HEAD --stat        # committed branch changes
git diff --stat                    # unstaged changes
git diff --cached --stat           # staged changes
```

Categorize changed files:

| Category | Pattern | Validation signal |
|----------|---------|-------------------|
| Source code | `src/`, `lib/`, `wos/`, `app/` | Run tests covering these modules |
| Tests | `tests/`, `test_*`, `*_test.*` | Run the modified tests directly |
| Config | `pyproject.toml`, `package.json`, `Cargo.toml` | Lint + build checks |
| Docs | `*.md`, `docs/` | Human review for accuracy |
| CI/Infra | `.github/`, `Makefile`, `Dockerfile` | Build/lint, human review |

Use changed file categories to scope which checks to propose. Don't
propose running the full test suite if only docs changed.

## 2. Convention Detection

Scan config files to discover available project checks:

| Config file | Signal | Inferred check |
|------------|--------|----------------|
| `pyproject.toml` — `[tool.pytest]` or pytest in deps | Test runner | `python python -m pytest tests/ -v` |
| `pyproject.toml` — `[tool.ruff]` | Linter | `ruff check .` |
| `pyproject.toml` — `[tool.mypy]` | Type checker | `mypy .` |
| `package.json` — `scripts.test` | Test runner | `npm test` |
| `package.json` — `scripts.lint` | Linter | `npm run lint` |
| `package.json` — `scripts.build` | Build | `npm run build` |
| `tsconfig.json` | Type checker | `npx tsc --noEmit` |
| `.eslintrc*` / `eslint.config.*` | Linter | `npx eslint .` |
| `Makefile` — `test` target | Test runner | `make test` |
| `Cargo.toml` | Test + lint | `cargo test`, `cargo clippy` |
| `go.mod` | Test + vet | `go test ./...`, `go vet ./...` |

Only propose checks for tools actually configured. Read the config file
to confirm — don't guess from file extension alone.

## 3. Project Doc Scanning

Read project documentation for explicit commands and conventions:

| File | What to extract |
|------|----------------|
| `CLAUDE.md` | Build/test commands, lint rules, conventions |
| `AGENTS.md` | Quality standards, validation expectations |
| `README.md` | Setup instructions, documented test commands |
| `CONTRIBUTING.md` | CI expectations, quality gates, PR checklist |

If a doc mentions a specific command (e.g., "run `make lint` before
submitting"), include it as a proposed criterion.

## Hypothesis Assembly

Combine signals into a prioritized criteria list:

1. **Tests for changed code** (if tests exist) — highest priority
2. **Linter** (if configured and source code changed)
3. **Type checker** (if configured and source code changed)
4. **Build** (if configured and source/config changed)
5. **Human review** for doc or behavior changes

Rules:
- Scope automated checks to changed files where the tool supports it
- Every proposed check must cite its signal source
- Classify each as `[auto]` or `[human]`
- If no checks can be inferred, say so and ask the user what to validate
