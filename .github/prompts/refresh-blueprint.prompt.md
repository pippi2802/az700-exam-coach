---
mode: agent
description: Refresh the cached AZ-700 exam blueprint from official sources.
---

# Refresh Blueprint

Act as the **exam-analyst** agent (`agents/exam-analyst.agent.md`).

Trigger phrases that should run this flow: `/refresh-blueprint`,
`refresh blueprint`, `update exam structure`, `sync with latest AZ-700 guide`,
`check if AZ-700 changed`.

Steps:

1. Attempt to access the Tier 1 official AZ-700 study guide listed in
   `knowledge/approved-sources.yaml`.
2. If accessible:
   - Diff the live guide against `knowledge/exam-blueprint.yaml`.
   - Report added / removed / renamed domains and subtopics and weight changes.
   - Update `cache_version` and `last_verified_against_source`.
   - Append a `change_history` entry: previous version, new version, source used,
     date checked, summary of changes.
3. If sources are **not** accessible:
   - Do not modify the file.
   - Reply exactly: "I am using the cached blueprint only and cannot verify
     whether it is still current."

Never fabricate exam changes.
