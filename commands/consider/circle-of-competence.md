---
description: Scope decisions by distinguishing what you know well from what you don't
argument-hint: "[domain or decision where expertise boundaries matter]"
---

<objective>
Map the boundary between what you genuinely understand and what you only
think you understand. Make better decisions by staying within your circle
where possible, and explicitly flagging when you're operating outside it.
</objective>

<process>
1. Define the decision or domain being evaluated
2. List what you know well from direct experience (inside the circle)
3. List what you know about from reading but haven't practiced (the edge)
4. List what you don't know or are guessing about (outside the circle)
5. For the decision at hand, which zones does it require knowledge from?
6. For areas outside your circle, identify who has that competence
7. Decide: stay in circle, expand the circle, or bring in expertise
</process>

<output_format>
## Circle of Competence: [Topic]

### Domain
[The decision or area being evaluated]

### Inside (know well)
- [Area of genuine expertise — from direct experience]

### Edge (familiar but not deep)
- [Area where you have knowledge but not mastery]

### Outside (don't know)
- [Area where you're guessing or relying on assumptions]

### Decision Requirements
[Which zones does this decision touch?]

### Strategy
[Stay inside / expand the circle / bring in outside expertise]
</output_format>

<example>
## Circle of Competence: Should Our Backend Team Build the Mobile App?

### Domain
Deciding whether our team of 3 backend engineers should build the iOS/Android app ourselves or hire specialists.

### Inside (know well)
- REST API design and backend infrastructure
- PostgreSQL performance tuning and data modeling
- CI/CD pipelines and production monitoring
- Python and Go ecosystem

### Edge (familiar but not deep)
- React Native (one engineer did a tutorial project)
- Mobile app architecture patterns (read about MVVM, never shipped it)
- App Store submission process (know it exists, never done it)

### Outside (don't know)
- iOS/Android platform-specific performance optimization
- Mobile-specific UX patterns (gesture navigation, offline-first)
- App Store review guidelines and rejection recovery
- Push notification infrastructure at scale

### Decision Requirements
Building the mobile app requires deep knowledge in all three zones. API integration is inside our circle, but the entire frontend layer — UI, platform APIs, store submission — is outside it.

### Strategy
Bring in outside expertise. Hire or contract a mobile developer for the app shell and platform integration. Our team owns the API layer and backend (inside our circle). The mobile specialist handles what we'd spend months learning poorly. Review architecture decisions together so knowledge transfers over time.
</example>

<success_criteria>
- Honest self-assessment (not inflating what's "inside")
- At least 2 items in each zone (inside, edge, outside)
- Decision requirements clearly mapped to knowledge zones
- Strategy acknowledges gaps rather than hand-waving them away
- Specific people, resources, or experts identified for outside zones
</success_criteria>
