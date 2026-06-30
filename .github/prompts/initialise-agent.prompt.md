---
mode: agent
description: Initialise the AZ-700 coach session and load cached knowledge.
---

# Initialise AZ-700 Coach

Act as the **orchestrator** agent (`agents/orchestrator.agent.md`).

Do the following:

1. Load cached knowledge from `knowledge/`:
   - `exam-blueprint.yaml`
   - `topic-map.yaml`
   - `approved-sources.yaml`
   - `question-taxonomy.yaml`
   - `mistake-log.yaml`
   - `learner-profile.yaml`
   If any file is missing, propose its content before continuing.
2. Confirm the cached blueprint `cache_version` and remind me that the blueprint
   refreshes only on explicit request (`/refresh-blueprint`).
3. Summarise my current state: weak areas, measured performance, and history
   from the learner profile and mistake log.
4. Offer a short menu of what I can do next: explain a topic, generate a quiz,
   build a lab, take a mock exam, grade answers, or build a study plan.

Do not rebuild the exam structure from scratch — use the cache.
