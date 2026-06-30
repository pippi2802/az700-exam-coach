---
applyTo: "outputs/quizzes/**,outputs/mock-exams/**,agents/question-writer.agent.md,agents/exam-simulator.agent.md"
---

# Question authoring standards

Conform to `knowledge/question-taxonomy.yaml`. Each question must include:

- Domain (D1-D5)
- Subtopic
- Type (theory_recall | scenario_design | troubleshooting | lab_design)
- Difficulty (easy | medium | hard | exam_like)
- Scenario
- Question
- Options A-D
- Correct answer
- Explanation
- Why each wrong option is wrong
- Source references
- Skill being tested

Quality rules:

- Generate **original** questions only. Never reproduce real exam dumps or
  copied proprietary questions.
- Prefer scenario-based, requirement-driven questions over trivia (target ~70%).
- Distractors must be real Azure services/features and plausible in context.
- Test trade-offs: cost, availability, security, management overhead, performance.
- Avoid length/grammar cues that leak the correct answer.
- For mock exams, follow domain weight midpoints from the blueprint and keep the
  answer key in a separate, clearly-marked section.
