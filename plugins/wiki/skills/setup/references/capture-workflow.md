# Capture Workflow

Use this workflow to capture communication preferences from the user.

## Steps

1. **Ask one freeform question**

   Ask the user: "How do you prefer AI assistants to communicate with you?
   For example: direct or diplomatic, concise or detailed, casual or formal,
   explain concepts or just give answers."

   Let them describe their style in their own words.

2. **Map to dimensions**

   Based on their response, determine the best level for each of the five
   dimensions:

   - **Directness**: blunt / balanced / diplomatic
   - **Verbosity**: terse / moderate / thorough
   - **Depth**: just-answers / context-when-useful / teach-me
   - **Expertise**: beginner / intermediate / expert
   - **Tone**: casual / neutral / formal

   Only include dimensions the user expressed a clear preference for.
   Leave unmentioned dimensions out — the defaults are fine.

3. **Confirm with user**

   Present the mapped dimensions and ask for confirmation:

   > Based on your description, here's what I'll set:
   >
   > - **Directness:** blunt — "Be direct. State problems plainly."
   > - **Verbosity:** terse — "Keep responses concise."
   >
   > Does this look right? Any adjustments?

4. **Write to AGENTS.md**

   After confirmation, write the preferences using the Python module:

   ```bash
   python <plugin-scripts-dir>/update_preferences.py --root . directness=blunt verbosity=terse
   ```

   This updates the `### Preferences` subsection inside the managed
   section of AGENTS.md.

## Notes

- Only set dimensions the user expressed a preference for
- If updating existing preferences, show what changed
- The writer is idempotent — running twice with the same values is safe
