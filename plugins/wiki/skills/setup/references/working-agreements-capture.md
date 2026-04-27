# Working Agreements Capture

Use this workflow to seed or review a project's `## Working Agreements`
section during `/wiki:setup`.

`## Working Agreements` is the **single user-owned behavior section** in
AGENTS.md. It covers both how the agent collaborates on the work
(workflow defaults like *Codify repetition*) and any communication-style
bullets the user wants to add (*Be direct*, *Keep responses concise*).
There is no separate Preferences flow — communication style is just
another bullet, written freeform.

The seed below is the **encouraged default for every project**. The
codify-repetition agreement is the high-value default we want every
project to start with; the user can edit or skip, but they should see it.

## Branching rule

Call `has_working_agreements(content)` on the current AGENTS.md to pick
the branch:

- **`False`** — section is absent → follow **Absent branch** below
- **`True`** — section is present → follow **Present branch** below

Either branch always ends with user confirmation. There is no silent
skip — the user always sees the current or proposed state and chooses.

## Absent branch (no section yet)

1. **Show the seed**

   Present the default seed list verbatim:

    ## Working Agreements

    - **Codify repetition.** If something will happen again, do it manually
      once on 3–10 items and show the output. If I approve, codify into a
      skill, hook, or cron. The test: if I have to ask twice, you failed.
    - **Watch for patterns.** When you notice recurring work across
      sessions, propose codifying it proactively — don't wait to be asked.

2. **Three-way prompt**

   > "These are the recommended defaults for every project — they shape
   > how the agent collaborates with you. You can also add your own
   > communication-style bullets (e.g., *Be direct*, *Keep responses
   > concise*) by choosing **edit**. Adopt as-is, edit, or skip?"

3. **Write**

   - **adopt** — append the seed verbatim to AGENTS.md *after* the
     managed `<!-- wiki:end -->` marker (or at end of file if no markers
     are present). Include a blank line before the heading.
   - **edit** — let the user modify or extend the text (add their own
     bullets), then append the result in the same location.
   - **skip** — write nothing. The user has opted out of the defaults
     for this project.

## Present branch (section already exists)

Three-way prompt: **keep / edit / replace**.

1. **Show the current section**

   Read and display the existing `## Working Agreements` section
   verbatim so the user sees exactly what's there today.

2. **Three-way prompt**

   > "Working Agreements already exist in AGENTS.md. Do you want to
   > **keep** them as-is, **edit** them, or **replace** them with the
   > current seed?"

3. **Write**

   - **keep** — no write. Move on.
   - **edit** — let the user modify the text, then write the edited
     version *in the same location* (replace the existing section
     in place; preserve surrounding content).
   - **replace** — overwrite the existing section in place with the
     current seed list verbatim.

   In-place replacement means finding the existing `## Working
   Agreements` heading and rewriting from there through the end of that
   section (next `##` heading or end of file). Never move the section
   to a new location.

## Shape

Each bullet follows:

> `- **Name.** One-line imperative. *(Optional)* one sentence of elaboration.`

The list is user-owned. The skill writes only what the user approved
in the current run.

## Notes

- Writes happen *outside* the managed markers, so `render_wiki_section`
  and `update_agents_md` are not used here. The skill writes the
  section directly to AGENTS.md.
- The seed is the skill's current default; the user decides whether to
  adopt, keep, edit, or replace based on what they see.
