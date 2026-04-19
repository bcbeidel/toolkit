# Working Agreements Capture

Use this workflow to seed a project's `## Working Agreements` section
during `/wiki:setup`.

## Idempotency rule

Before doing anything, call `has_working_agreements(content)` on the
current AGENTS.md. If it returns `True`, the step is a **no-op** — do
not prompt, do not diff, do not overwrite. Move on.

## Steps (only when the section is absent)

1. **Show the seed**

   Present the default seed list verbatim:

   ```markdown
   ## Working Agreements

   - **Codify repetition.** If something will happen again, do it manually
     once on 3–10 items and show the output. If I approve, codify into a
     skill, hook, or cron. The test: if I have to ask twice, you failed.
   - **Watch for patterns.** When you notice recurring work across
     sessions, propose codifying it proactively — don't wait to be asked.
   ```

2. **Three-way prompt**

   Ask the user:

   > "Working Agreements describe how we collaborate on the work itself
   > — what behaviors the agent should default to. Here is a seed you
   > can **adopt** as-is, **edit**, or **skip**. Which?"

3. **Write**

   - **adopt** — append the seed verbatim to AGENTS.md *after* the
     managed `<!-- wiki:end -->` marker (or at end of file if no markers
     are present). Include a blank line before the heading.
   - **edit** — let the user modify the text, then append the edited
     version in the same location.
   - **skip** — write nothing.

## Shape

Each bullet follows:

> `- **Name.** One-line imperative. *(Optional)* one sentence of elaboration.`

The list is user-owned after the first write. The skill never
re-renders or rewrites it.

## Notes

- Writes happen *outside* the managed markers, so `render_wiki_section`
  and `update_agents_md` are not used here. The skill writes the
  section directly to AGENTS.md.
- Running setup on a project with Working Agreements already present
  (from any prior run, any location in the file) skips this step
  entirely — see the idempotency rule above.
