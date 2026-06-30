---
mode: agent
description: Generate a full weighted AZ-700 mock exam.
---

# Generate Mock Exam

Act as the **exam-simulator** agent (`agents/exam-simulator.agent.md`).

Inputs (ask if not provided):
- Question count (default: blueprint `mock_exam_defaults.question_count`).
- Time limit (default: blueprint default).

Build a balanced mock exam:
- Allocate questions by domain weight midpoints (D1 27, D2 22, D3 17, D4 12, D5 17).
- Use mostly scenario-based questions with realistic distractors.
- Do **not** reveal answers inline. Put the full answer key + explanations in a
  separate "Answer key" section at the bottom.

Save to `outputs/mock-exams/mock-<date>.md`.

After I submit answers, hand off to the **evaluator** agent to grade by domain,
identify weak areas, and recommend next theory + labs.

Original questions only.
