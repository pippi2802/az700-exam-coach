"""Grade learner answers overall and by exam domain."""

from __future__ import annotations

from dataclasses import dataclass, field

DEFAULT_PASS_THRESHOLD = 70.0


@dataclass(frozen=True)
class AnswerKeyItem:
    """One item in the answer key for a quiz or mock exam."""

    question_id: str
    domain_id: str
    correct_answer: str
    subtopic: str = ""


@dataclass
class DomainScore:
    """Score breakdown for a single domain."""

    domain_id: str
    correct: int = 0
    total: int = 0

    @property
    def percent(self) -> float:
        return 0.0 if self.total == 0 else round(100.0 * self.correct / self.total, 1)


@dataclass
class GradeResult:
    """Outcome of grading a submission."""

    correct: int
    total: int
    pass_threshold: float
    by_domain: dict[str, DomainScore] = field(default_factory=dict)
    wrong_question_ids: list[str] = field(default_factory=list)

    @property
    def percent(self) -> float:
        return 0.0 if self.total == 0 else round(100.0 * self.correct / self.total, 1)

    @property
    def passed(self) -> bool:
        return self.percent >= self.pass_threshold

    def weak_domains(self) -> list[str]:
        """Domain ids that scored below the pass threshold, weakest first."""
        scored = [d for d in self.by_domain.values() if d.total > 0]
        weak = [d for d in scored if d.percent < self.pass_threshold]
        weak.sort(key=lambda d: d.percent)
        return [d.domain_id for d in weak]


def _normalise(answer: str) -> str:
    """Normalise an answer letter/value for comparison."""
    return answer.strip().lower().rstrip(".)")


def grade(
    answer_key: list[AnswerKeyItem],
    responses: dict[str, str],
    pass_threshold: float = DEFAULT_PASS_THRESHOLD,
) -> GradeResult:
    """Grade ``responses`` against ``answer_key``.

    ``responses`` maps question_id -> chosen answer. Missing or unknown question
    ids count as incorrect.
    """
    result = GradeResult(correct=0, total=len(answer_key), pass_threshold=pass_threshold)

    for item in answer_key:
        domain = result.by_domain.setdefault(item.domain_id, DomainScore(item.domain_id))
        domain.total += 1
        given = responses.get(item.question_id)
        if given is not None and _normalise(given) == _normalise(item.correct_answer):
            result.correct += 1
            domain.correct += 1
        else:
            result.wrong_question_ids.append(item.question_id)

    return result
