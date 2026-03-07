# SIFT Framework Reference

Each SIFT step maps to concrete agent actions during source evaluation.

## S — Stop

Before using any source, pause and ask:
- Do I know this source? Is it reputable?
- Am I reacting emotionally to the claim?
- Should I investigate further before citing this?

**Agent action:** Flag every new source as "unverified" until it passes
the remaining SIFT steps. Do not include unverified claims in findings.

## I — Investigate the Source

Check who's behind the information:
- What organization publishes this? What's their mission?
- Who is the author? What are their credentials?
- Is this source known for accuracy in this domain?
- Does the source have an obvious bias or agenda?

**Agent action:** For each source, check:
1. Domain authority — is this an official/institutional site?
2. Author credentials — do they have relevant expertise?
3. Publication history — is the source consistently reliable?
4. Classify into a source hierarchy tier (T1-T6)

## F — Find Better Coverage

For important claims, search for more authoritative sources:
- Can you find this claim from an official or institutional source?
- Do multiple independent sources agree?
- Is there a primary source (original research, official statement)?

**Agent action:** For each key claim:
1. Search for the same claim from a higher-tier source
2. If found: upgrade to the better source
3. If not found: note the claim has limited sourcing
4. Check for counter-evidence — sources that disagree

## T — Trace Claims

Follow claims back to their origin:
- Where did this claim originate?
- Has it been modified as it spread?
- Does the original context change the meaning?

**Agent action:** For critical claims:
1. Follow citation chains to the primary source
2. Verify the claim matches the original context
3. Note any telephone-game distortion
4. Record the full provenance chain

## SIFT Intensity by Mode

| Mode | Stop | Investigate | Find Better | Trace |
|------|------|-------------|-------------|-------|
| deep-dive | Always | Full | Full | Key claims |
| landscape | Always | Domain only | Top 3 claims | Skip |
| technical | Always | Full | Full | All claims |
| feasibility | Always | Domain only | Key claims | Skip |
| competitive | Always | Full | Key claims | Skip |
| options | Always | Full | Full | Key claims |
| historical | Always | Domain only | Key claims | Key claims |
| open-source | Always | Repo metrics | Key claims | Skip |
