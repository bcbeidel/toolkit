# Platform-Specific Notes

The core workflow (draft → test → review → improve → repeat) is the same everywhere.
The mechanics change based on what the runtime supports.

---

## Cross-Platform Skill Placement

No single directory path is discovered by all platforms. If a skill needs to work on both Claude Code and Copilot (or other tools), it must exist in both locations:

| Path | Discovered by |
|------|--------------|
| `.claude/skills/<name>/` | Claude Code (CLI, Desktop) — primary path |
| `.agents/skills/<name>/` | GitHub Copilot, Codex CLI, Cursor, Windsurf, Kiro, Gemini CLI |
| `.github/skills/<name>/` | GitHub Copilot (project-level alternative) |

The practical pattern when working across Claude Code and Copilot: keep the authoritative skill in `.claude/skills/` and symlink or copy to `.agents/skills/`. Or maintain both paths with the same content. The `${CLAUDE_SKILL_DIR}` variable in Claude Code points to whichever path loaded the skill, so relative resource references work regardless.

**Skills do not sync across surfaces.** A skill in a project directory is only available in that project. A personal skill in `~/.claude/skills/` is only available to Claude Code — not to Copilot, which looks in `~/.copilot/skills/` or `~/.agents/skills/` for personal skills.

---

## GitHub Copilot

GitHub Copilot supports skills across three surfaces — VS Code agent mode, the CLI, and Copilot Workspace (cloud agent) — and all three use the same SKILL.md format. This makes it the most directly interoperable platform with Claude Code.

### What's shared with Claude Code

Copilot supports these frontmatter fields from the open standard:
- `name`, `description` (required)
- `argument-hint`, `user-invocable`, `disable-model-invocation`, `allowed-tools` (optional)

Skills are discovered progressively (metadata → full body → resources), and the `/skill-name` slash command invocation works the same way.

### What's different from Claude Code

**`allowed-tools` semantics differ.** In Claude Code, `allowed-tools` grants permission for listed tools while the skill is active. In Copilot, it bypasses the per-use confirmation prompt — listed tools run without asking the user each time. This difference doesn't usually matter if you're just listing tools you expect the skill to use, but be aware the enforcement model is different.

**Claude Code extensions are silently ignored.** These frontmatter fields and syntax patterns have no effect on Copilot and should be avoided in cross-platform skills:

| Claude Code feature | Behavior on Copilot |
|--------------------|---------------------|
| `context: fork` | Silently ignored — no subagent spawning |
| `agent:`, `model:`, `effort:` | Silently ignored |
| `hooks:`, `paths:`, `shell:` | Silently ignored |
| `` !`command` `` dynamic shell blocks | Treated as literal Markdown text |
| `$ARGUMENTS`, `${CLAUDE_SKILL_DIR}` | Not substituted — rendered as literal strings |
| Plugin namespacing (`plugin:skill`) | Not supported |

**No subagent spawning from skill frontmatter.** Claude Code's `context: fork` has no equivalent in Copilot. Multi-agent coordination in Copilot is handled at the Workspace level (`agents:` field in Copilot Workspace), not from within a skill.

**No `claude -p` CLI.** The description optimization loop (`run_loop.py`) requires the Claude CLI, which is only available in Claude Code. Skip description optimization when working in Copilot.

### Discovery paths

**Project-level** (committed to repo, applies to this project):
```
.github/skills/<skill-name>/SKILL.md
.claude/skills/<skill-name>/SKILL.md
.agents/skills/<skill-name>/SKILL.md
```
Additional directories can be added via the `chat.skillsLocations` VS Code setting.

**Personal** (cross-project, lives in home directory):
```
~/.copilot/skills/<skill-name>/SKILL.md
~/.claude/skills/<skill-name>/SKILL.md
~/.agents/skills/<skill-name>/SKILL.md
```

When the same skill name exists in multiple locations, higher-priority locations win. Project skills override personal skills.

**Note on org/enterprise skills:** Organization-level and enterprise-level skill distribution was listed as "coming soon" in January 2026 documentation. Check current Copilot docs before relying on centralized distribution.

### Running test cases on Copilot

Copilot agent mode has no equivalent to Claude Code's subagent spawning, so the parallel eval workflow doesn't apply. Run test cases sequentially:

1. Invoke the skill with the test prompt in Copilot agent mode
2. Review the output in the chat panel
3. For file outputs, check the workspace filesystem
4. Ask for feedback inline: "How does this look? Anything you'd change?"

Skip baseline runs and quantitative benchmarking — they require parallel execution and the `aggregate_benchmark.py` script. Focus on qualitative review.

The eval viewer (`generate_review.py`) requires a running HTTP server or static file output. In Copilot's VS Code context, use `--static /tmp/eval_review.html` and open the file in a browser tab.

### Security note

The Copilot documentation explicitly warns against pre-approving `shell`/`bash` tools in `allowed-tools` unless you have reviewed the skill source — this is a prompt injection vector. Only list tools you trust for the specific skill, and be cautious with community-sourced skills.

### Updating an existing skill in Copilot

The same update guidance as Claude.ai applies: preserve the original name, copy to a writable location before editing if the installed path is read-only.

---

## Claude.ai

Claude.ai has no subagents and runs in a sandboxed VM environment.

**Environment constraints:**
- Runs in a VM/container. Filesystem writes are scoped to the VM.
- Network access varies by user/admin settings — may be full, partial, or none.
- No runtime package installation — only pre-installed packages are available.
- Skills are deployed as zip file uploads (Settings → Features), not filesystem directories. This is separate from Claude Code's filesystem-based skills and does not sync between surfaces.

**Running test cases**: No parallel execution. For each test case, read the skill's SKILL.md, then follow its instructions to accomplish the test prompt yourself, one at a time. This is less rigorous than independent subagents (you wrote the skill and are also running it), but it's a useful sanity check — human review compensates. Skip baseline runs — just use the skill as requested.

**Reviewing results**: If no browser is available, skip the viewer entirely. Present results directly in the conversation: show the prompt and the output for each test case. If the output is a file (e.g., .docx, .xlsx), save it to the filesystem and tell the user where to find it. Ask for feedback inline: "How does this look? Anything you'd change?"

**Benchmarking**: Skip quantitative benchmarking — baseline comparisons aren't meaningful without subagents. Focus on qualitative feedback.

**The iteration loop**: Same as always — improve the skill, rerun test cases, ask for feedback — without the browser viewer in the middle. You can still organize results into iteration directories on the filesystem.

**Description optimization**: Requires the `claude` CLI tool (`claude -p`), available only in Claude Code. Skip it on Claude.ai.

**Blind comparison**: Requires subagents. Skip it.

**Packaging**: `package_skill.py` works anywhere with Python and a filesystem. The user can download the resulting `.skill` file.

**Updating an existing skill**:
- **Preserve the original name.** Use the skill's directory name and `name` frontmatter field unchanged.
- **Copy to a writeable location before editing.** The installed skill path may be read-only. Copy to `/tmp/skill-name/`, edit there, and package from the copy.
- **If packaging manually, stage in `/tmp/` first**, then copy to the output directory — direct writes may fail due to permissions.

---

## Cowork

Cowork has subagents but no browser or display. It runs in an Apple Virtualization Framework sandbox on macOS.

**Environment constraints:** Writes are restricted to user-designated directories only. Claude has read, edit, and create access only within the directories the user explicitly grants. Eval workspaces and result files must be placed within these designated directories — paths outside them will fail.

- Subagents work, so the full parallel workflow (spawn test cases, run baselines, grade) applies. If timeouts are severe, it's OK to run test prompts in series.
- No browser/display: use `--static <output_path>` when generating the eval viewer to write a standalone HTML file. Proffer a link the user can click to open it.
- Generate the eval viewer before revising the skill yourself — human review must come before self-evaluation, because having written the skill biases your judgment. Get results in front of the human before making any changes.
- Feedback works differently: "Submit All Reviews" downloads `feedback.json` as a file rather than posting to a server. Read it from there (you may need to request access first).
- Packaging works — `package_skill.py` just needs Python and a filesystem.
- Description optimization (`run_loop.py` / `run_eval.py`) works fine via subprocess. Save it until the skill is fully finished and the user agrees it's in good shape.
- **Updating an existing skill**: Follow the update guidance in the Claude.ai section above.

---

## Other Platforms (brief notes)

**Gemini CLI**: Skills activate after an explicit per-session user consent prompt (not automatic). The user sees the skill name, purpose, and directory path before approving. Skill stays active for the full session after the initial consent — no per-invocation prompts. Design skill descriptions to be self-explanatory to a user who may not know what the skill is.

**CrewAI**: `allowed-tools` is metadata-only — it does not provision or inject any tools. Tools must be registered separately via `tools=[]`, `mcps=[]`, or `apps=[]` parameters. Skills are injected directly into the agent's task prompt rather than loaded on demand.

**LangChain Deep Agents**: Hard 10 MB limit on SKILL.md files. Paths must use forward slashes and be relative to the backend root. Large eval workspace outputs should not be co-located with SKILL.md.

**General anti-pattern (all platforms):** Never hard-code absolute paths (e.g., `/Users/alice/`). Use relative paths or well-known variables. On Claude Code, `${CLAUDE_SKILL_DIR}` points to the skill directory at runtime.
