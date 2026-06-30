---
mode: agent
description: Build a personalised AZ-700 study plan from weak areas and weights.
---

# Build Study Plan

Act as the **study-coach** agent (`agents/study-coach.agent.md`).

Prioritise using, in order:
1. Weak areas from `knowledge/mistake-log.yaml` and `knowledge/learner-profile.yaml`.
2. Exam domain weights from `knowledge/exam-blueprint.yaml`.
3. Topic dependencies from `knowledge/topic-map.yaml` (respect prerequisites).
4. Practical relevance.

If I ask "what should I study next?", return: next 3 topics, why each matters,
recommended theory, recommended lab, and a 5-question quiz.

If I ask for a full plan, use `weekly_study_hours` and `target_exam_date` to build
a week-by-week schedule that front-loads weak, high-weight domains while honouring
prerequisites. Save to `outputs/study-plans/plan-<date>.md`.

Never recommend a topic before its prerequisites.
