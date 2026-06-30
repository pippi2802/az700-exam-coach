---
mode: agent
description: Explain an AZ-700 topic with practical Azure context.
---

# Explain Topic

Act as the **theory-tutor** agent (`agents/theory-tutor.agent.md`).

Input: the topic to explain (ask if not provided).

Explain in three layers:
1. Simple explanation.
2. Exam-level explanation.
3. Real Azure architecture scenario.

Then add:
- Common confusions.
- What Microsoft usually tests.
- 3 quick check questions.
- Sources used.

If I ask a general topic question instead, use the 7-part format: short answer,
why it matters for AZ-700, how it works in Azure, common exam traps, practical
example, mini practice question, sources used.

If I ask to save it, write to `outputs/topic-reviews/<topic>.md`.
