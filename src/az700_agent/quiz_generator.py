"""Build weighted quiz and mock-exam question plans from the blueprint.

This module does not write question prose (the LLM agents do that). It computes
the *plan*: how many questions per domain, per difficulty, and per type, so that
generated quizzes and mock exams stay faithful to the official exam weights.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .blueprint_loader import Blueprint


@dataclass(frozen=True)
class QuestionSlot:
    """A single planned question position in a quiz or exam."""

    index: int
    domain_id: str
    difficulty: str
    qtype: str


@dataclass
class QuizPlan:
    """A computed plan for a quiz or mock exam."""

    total: int
    slots: list[QuestionSlot] = field(default_factory=list)

    def by_domain(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for slot in self.slots:
            counts[slot.domain_id] = counts.get(slot.domain_id, 0) + 1
        return counts


def _parse_percent(value: str | float | int) -> float:
    """Parse a weight that may be '27', '27%', or '20-25%' into a float."""
    if isinstance(value, (int, float)):
        return float(value)
    text = str(value).strip().rstrip("%")
    if "-" in text:
        low, high = text.split("-", 1)
        return (float(low) + float(high)) / 2
    return float(text)


def _largest_remainder(weights: dict[str, float], total: int) -> dict[str, int]:
    """Apportion ``total`` items across keys by weight using largest remainder.

    Guarantees the allocated counts sum exactly to ``total``.
    """
    if total <= 0 or not weights:
        return {key: 0 for key in weights}
    weight_sum = sum(weights.values())
    if weight_sum <= 0:
        # Even split fallback.
        base = total // len(weights)
        counts = {key: base for key in weights}
        for key in list(weights)[: total - base * len(weights)]:
            counts[key] += 1
        return counts

    raw = {key: (weight / weight_sum) * total for key, weight in weights.items()}
    floors = {key: int(value) for key, value in raw.items()}
    remainder = total - sum(floors.values())
    # Distribute the remaining units to the largest fractional parts.
    order = sorted(raw, key=lambda key: raw[key] - floors[key], reverse=True)
    for key in order[:remainder]:
        floors[key] += 1
    return floors


def allocate_by_domain(blueprint: Blueprint, total: int) -> dict[str, int]:
    """Return domain id -> question count weighted by blueprint midpoints."""
    weights = {
        domain.id: domain.weight_midpoint or _parse_percent(domain.weight)
        for domain in blueprint.domains
    }
    return _largest_remainder(weights, total)


def allocate_difficulty(blueprint: Blueprint, total: int) -> dict[str, int]:
    """Return difficulty -> question count from the blueprint distribution."""
    weights = {
        key: _parse_percent(value)
        for key, value in blueprint.difficulty_distribution().items()
    }
    return _largest_remainder(weights, total)


def allocate_types(blueprint: Blueprint, total: int) -> dict[str, int]:
    """Return question type -> count from the blueprint distribution."""
    weights = {
        key: _parse_percent(value)
        for key, value in blueprint.question_distribution().items()
    }
    return _largest_remainder(weights, total)


def build_plan(
    blueprint: Blueprint,
    total: int,
    domain_id: str | None = None,
) -> QuizPlan:
    """Build a quiz plan.

    If ``domain_id`` is given, all questions target that domain (a focused quiz);
    otherwise questions are spread across domains by exam weight (a mock exam).
    """
    if total <= 0:
        return QuizPlan(total=0)

    if domain_id is not None:
        blueprint.domain(domain_id)  # validate
        domain_counts = {domain_id: total}
    else:
        domain_counts = allocate_by_domain(blueprint, total)

    difficulty_counts = allocate_difficulty(blueprint, total)
    type_counts = allocate_types(blueprint, total)

    difficulty_pool = _expand(difficulty_counts)
    type_pool = _expand(type_counts)
    domain_pool = _expand(domain_counts)

    slots: list[QuestionSlot] = []
    for index in range(total):
        slots.append(
            QuestionSlot(
                index=index + 1,
                domain_id=domain_pool[index],
                difficulty=difficulty_pool[index] if index < len(difficulty_pool) else "medium",
                qtype=type_pool[index] if index < len(type_pool) else "scenario_based",
            )
        )
    return QuizPlan(total=total, slots=slots)


def _expand(counts: dict[str, int]) -> list[str]:
    """Expand a count map into a flat list (e.g. {'a':2} -> ['a','a'])."""
    pool: list[str] = []
    for key, count in counts.items():
        pool.extend([key] * count)
    return pool
