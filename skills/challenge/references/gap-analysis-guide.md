# Gap Analysis Guide

## Classification Rules

For each assumption, read the matched documents and classify:

### Aligned

The assumption is **aligned** when a document explicitly supports the claim.
The document must directly address the same concept — not merely mention
a related term.

**Confidence levels:**
- **High** — The document explicitly states or strongly implies the same
  claim. No inference needed. Example: assumption says "OAuth 2.0",
  document says "We use OAuth 2.0 with PKCE."
- **Moderate** — The document discusses the same topic with a compatible
  position, but doesn't state the exact claim. Requires inference.
  Example: assumption says "OAuth 2.0", document discusses "token-based
  authentication patterns."
- **Low** — The document touches on a related area. The connection is
  plausible but indirect. Example: assumption says "OAuth 2.0", document
  discusses "third-party API integration."

### Gap

The assumption is a **gap** when a document contradicts or conflicts with
the claim. The contradiction must be substantive, not a difference in
wording.

**Confidence levels:**
- **High** — Direct contradiction. Document explicitly states the opposite.
  Example: assumption says "1000 req/min", document says "500 req/min."
- **Moderate** — Implied contradiction. Document's position is incompatible
  but doesn't directly address the claim.
- **Low** — Tension exists but both positions could coexist under certain
  interpretations.

### No Coverage

The assumption has **no coverage** when no document addresses the topic.
No Coverage items have no confidence level — evidence is absent, not weak.

Do not classify as No Coverage if a document is tangentially relevant.
Use Low confidence Aligned or Gap instead. Reserve No Coverage for
assumptions the knowledge base is genuinely silent on.

## Key Principles

1. **Don't manufacture evidence.** If a document doesn't clearly address
   the assumption, classify as No Coverage rather than stretching to
   claim Low confidence alignment.
2. **Cite specifically.** Reference the document path and the relevant
   section or claim within it.
3. **One source per row.** If multiple documents address an assumption,
   use the strongest evidence. Mention supporting sources in the
   Evidence column.
4. **Gaps over alignment when ambiguous.** If evidence could support
   either classification, flag it as a Gap. False gaps are safer than
   false alignment — they prompt review rather than false confidence.
