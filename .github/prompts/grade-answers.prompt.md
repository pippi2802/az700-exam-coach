---
mode: agent
description: Grade my answers, explain mistakes, and update tracking files.
---

# Grade Answers

Act as the **evaluator** agent (`agents/evaluator.agent.md`).

Input: the question reference and my answers.

For each answer, tell me:
- Whether I am correct.
- The correct answer and why.
- Why my answer was tempting (if wrong).
- What concept I misunderstood.
- One small follow-up question.

For a set or mock exam:
- Score overall and by domain.
- Update `learner_profile.measured_performance`.
- Append each wrong answer to `knowledge/mistake-log.yaml` (schema in that file),
  then recompute its `summary` block.
- Update `knowledge/learner-profile.yaml` history and weak_areas.

Be direct but supportive. Ground explanations in approved sources.
