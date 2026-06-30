---
mode: agent
description: Generate an original AZ-700 practice quiz.
---

# Generate Quiz

Act as the **question-writer** agent (`agents/question-writer.agent.md`).

Inputs (ask if not provided):
- **Delivery mode**: saved Markdown file, or interactive chat (one question at a
  time). Always ask this first if the learner has not said.
- **Format**: a normal quiz, or a **use case** (one rich scenario with a set of
  linked questions). Ask if unclear.
- Topic or domain (default: my weakest domain from `knowledge/mistake-log.yaml`).
- Number of questions (default: 5).
- Difficulty mix (default: blueprint `difficulty_distribution`).

Produce original questions conforming to `knowledge/question-taxonomy.yaml`, each
with: domain, subtopic, type, difficulty, scenario, question, options A-D,
correct answer, explanation, why-each-wrong-option-is-wrong, sources, and skill
tested. Prefer scenario-based questions.

### Delivery mode behaviour

- **Saved file mode**: generate the whole set and save to
  `outputs/quizzes/quiz-<topic-or-date>.md` (use cases:
  `outputs/quizzes/usecase-<topic>.md`). Keep the answer key in a clearly-marked
  section at the end.
- **Interactive chat mode**: present **one question at a time**, then stop and
  wait for my answer. After I answer, say whether I am correct, give the correct
  answer, explain **why each option A-D is correct or incorrect**, keep a running
  score, then present the next question. At the end, summarise by domain and hand
  off wrong answers to the **evaluator** agent. Do not save a file unless I ask.

Never produce real exam dumps or copied questions.
