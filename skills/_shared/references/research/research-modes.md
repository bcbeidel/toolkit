---
name: Research Modes
description: Eight research modes with distinct methodology intensity, SIFT rigor, and challenge requirements
stage: frame
pipeline: research
---

## Purpose
Defines the eight research modes and their methodology intensity parameters. Used by the framer to select the appropriate mode and by other stages to determine conditional behavior (e.g., which challenge sub-steps to apply).

# Research Modes

Eight modes with distinct methodology and intensity. All produce a
standard research document.

## Mode Matrix

| Mode | Min Sources | SIFT Rigor | Counter-Evidence | Challenge | Claim Verification |
|------|-------------|------------|------------------|-----------|-------------------|
| deep-dive | 8+ | High | Required | Full | Full |
| landscape | 6+ | Medium | Optional | Partial | Full |
| technical | 6+ | High | Required | Partial | Full |
| feasibility | 4+ | Medium | Required | Full | Full |
| competitive | 6+ | Medium | Optional | Full | Full |
| options | 6+ | High | Required | Full | Full |
| historical | 4+ | Low | Optional | Partial | Full |
| open-source | 4+ | Medium | Optional | Partial | Full |

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

**Full** = Assumptions check + ACH + Premortem.
**Partial** = Assumptions check + Premortem (no ACH).

## Mode Descriptions

- **deep-dive** ("What do we know about X?") — Comprehensive single-topic investigation. Cast wide net, narrow to highest-quality sources. Cover background, current state, key debates, implications.
- **landscape** ("What's the landscape for X?") — Broad domain survey. Map major players, trends, categories. Prioritize breadth over depth.
- **technical** ("How does X work technically?") — Deep technical investigation. Focus on architecture, implementation, performance, tradeoffs. Prefer official docs and expert practitioners.
- **feasibility** ("Can we do X given our constraints?") — Evaluate achievability given constraints. Identify blockers, risks, prerequisites. Actively search for reasons it might fail.
- **competitive** ("How does X compare to competitors?") — Systematic comparison across defined criteria. Watch for vendor bias in sources.
- **options** ("Should we use A or B?") — Structured comparison of alternatives. Each option gets equal investigation depth.
- **historical** ("How did X evolve?") — Trace development over time. Identify key inflection points, decisions, and consequences.
- **open-source** ("What open source options exist for X?") — Survey projects by stars, maintenance activity, community health, documentation quality, and license compatibility.
