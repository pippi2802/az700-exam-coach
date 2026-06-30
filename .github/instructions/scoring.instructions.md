---
applyTo: "knowledge/mistake-log.yaml,knowledge/learner-profile.yaml,agents/evaluator.agent.md"
---

# Scoring and mistake-tracking standards

When grading answers or quizzes:

- Score overall and **by domain** (D1-D5).
- Use the mock-exam pass threshold from the blueprint (default 70%).
- Write domain scores to `learner_profile.measured_performance`.

When recording mistakes in `knowledge/mistake-log.yaml`:

- Append one entry per wrong answer using the documented schema (id, date,
  domain, subtopic, topic_id, question_ref, question_summary, chosen_answer,
  correct_answer, misconception, severity, resolved).
- New mistakes start with `resolved: false`.
- Only set `resolved: true` after a successful re-test of the same concept.
- Recompute the `summary` block: total_mistakes, by_domain counts,
  weakest_domains (highest mistake counts), and last_updated.

Keep YAML valid and stable so the Python tooling in `src/` can parse it.
