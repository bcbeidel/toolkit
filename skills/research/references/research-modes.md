# Research Modes

Eight investigation modes, each with distinct methodology, intensity, and
output expectations. All modes produce a standard research document but
vary in SIFT rigor, source requirements, and counter-evidence needs.

## Mode Matrix

| Mode | Min Sources | SIFT Rigor | Counter-Evidence | Challenge | Claim Verification | Typical Duration |
|------|-------------|------------|------------------|-----------|-------------------|------------------|
| deep-dive | 8+ | High | Required | Full | Full | Long |
| landscape | 6+ | Medium | Optional | Partial | Full | Medium |
| technical | 6+ | High | Required | Partial | Full | Long |
| feasibility | 4+ | Medium | Required | Full | Full | Medium |
| competitive | 6+ | Medium | Optional | Full | Full | Medium |
| options | 6+ | High | Required | Full | Full | Long |
| historical | 4+ | Low | Optional | Partial | Full | Short |
| open-source | 4+ | Medium | Optional | Partial | Full | Medium |

## Challenge Sub-Steps by Mode

| Mode | Assumptions Check | ACH | Premortem |
|------|-------------------|-----|----------|
| deep-dive | Yes | Yes | Yes |
| landscape | Yes | No | Yes |
| technical | Yes | No | Yes |
| feasibility | Yes | Yes | Yes |
| competitive | Yes | Yes | Yes |
| options | Yes | Yes | Yes |
| historical | Yes | No | Yes |
| open-source | Yes | No | Yes |

- **Full** = Assumptions check + ACH + Premortem
- **Partial** = Assumptions check + Premortem (no ACH)

See `references/challenge-phase.md` for detailed procedures.

## Mode Descriptions

### deep-dive
**Question pattern:** "What do we know about X?"
**Methodology:** Comprehensive investigation of a single topic. Cast a wide
net, then narrow to highest-quality sources. Cover background, current state,
key debates, and practical implications. Counter-evidence actively sought.

### landscape
**Question pattern:** "What's the landscape for X?"
**Methodology:** Broad survey across a domain. Map the major players, trends,
and categories. Prioritize breadth over depth. Goal is orientation, not
exhaustive coverage.

### technical
**Question pattern:** "How does X work technically?"
**Methodology:** Deep technical investigation. Focus on architecture,
implementation details, performance characteristics, and tradeoffs.
Prefer official documentation and expert practitioners. Counter-evidence
required for claimed advantages.

### feasibility
**Question pattern:** "Can we do X given our constraints?"
**Methodology:** Evaluate whether a goal is achievable given specific
constraints (time, resources, technology, skills). Identify blockers,
risks, and prerequisites. Counter-evidence required — actively search
for reasons it might fail.

### competitive
**Question pattern:** "How does X compare to competitors?"
**Methodology:** Systematic comparison across defined criteria. Identify
differentiators, market positioning, and relative strengths. Watch for
vendor bias in sources.

### options
**Question pattern:** "Should we use A or B?"
**Methodology:** Structured comparison of specific alternatives against
evaluation criteria. Each option gets equal investigation depth. Counter-
evidence required — for each option, find arguments against it.

### historical
**Question pattern:** "How did X evolve?"
**Methodology:** Trace the development of a topic over time. Identify key
inflection points, decisions, and their consequences. Lower SIFT intensity
since historical sources are often secondary.

### open-source
**Question pattern:** "What open source options exist for X?"
**Methodology:** Survey available open-source projects. Evaluate by stars,
maintenance activity, community health, documentation quality, and license
compatibility. Use repository metrics as proxy for quality.
