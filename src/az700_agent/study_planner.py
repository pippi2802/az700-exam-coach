"""Recommend what to study next from weak areas, weights, and dependencies."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from . import KNOWLEDGE_DIR
from .blueprint_loader import Blueprint
from .mistake_tracker import MistakeTracker

DEFAULT_TOPIC_MAP_PATH = KNOWLEDGE_DIR / "topic-map.yaml"

_RELEVANCE_SCORE = {
    "very_high": 4.0,
    "high": 3.0,
    "medium": 2.0,
    "low": 1.0,
}


@dataclass(frozen=True)
class Topic:
    """A node in the topic dependency map."""

    id: str
    label: str
    domain: str
    prerequisites: tuple[str, ...]
    unlocks: tuple[str, ...]
    practical_relevance: str


@dataclass
class Recommendation:
    """A single study recommendation."""

    topic: Topic
    score: float
    reason: str


class TopicMap:
    """Typed accessor over ``topic-map.yaml``."""

    def __init__(self, data: dict[str, Any]) -> None:
        self._topics = {
            raw["id"]: Topic(
                id=raw["id"],
                label=raw["label"],
                domain=raw["domain"],
                prerequisites=tuple(raw.get("prerequisites", [])),
                unlocks=tuple(raw.get("unlocks", [])),
                practical_relevance=raw.get("practical_relevance", "medium"),
            )
            for raw in data.get("topic_map", {}).get("topics", [])
        }

    @classmethod
    def load(cls, path: Path | str | None = None) -> "TopicMap":
        map_path = Path(path) if path is not None else DEFAULT_TOPIC_MAP_PATH
        with map_path.open("r", encoding="utf-8") as handle:
            data = yaml.safe_load(handle) or {}
        return cls(data)

    @property
    def topics(self) -> list[Topic]:
        return list(self._topics.values())

    def get(self, topic_id: str) -> Topic | None:
        return self._topics.get(topic_id)

    def prerequisites_met(self, topic_id: str, completed: set[str]) -> bool:
        topic = self._topics.get(topic_id)
        if topic is None:
            return False
        return all(prereq in completed for prereq in topic.prerequisites)


def recommend_topics(
    blueprint: Blueprint,
    topic_map: TopicMap,
    tracker: MistakeTracker,
    completed: set[str] | None = None,
    limit: int = 3,
) -> list[Recommendation]:
    """Rank study topics.

    Priority signals, combined into a score:
      1. Weak areas (unresolved mistakes per domain).
      2. Exam domain weight.
      3. Topic practical relevance.
    Topics whose prerequisites are unmet are excluded.
    """
    completed = completed or set()
    weak_counts = tracker.counts_by_domain()
    weights = blueprint.weight_midpoints()

    recommendations: list[Recommendation] = []
    for topic in topic_map.topics:
        if topic.id in completed:
            continue
        if not topic_map.prerequisites_met(topic.id, completed):
            continue

        weakness = weak_counts.get(topic.domain, 0)
        weight = weights.get(topic.domain, 0.0)
        relevance = _RELEVANCE_SCORE.get(topic.practical_relevance, 2.0)

        # Weight the signals: mistakes dominate, then exam weight, then relevance.
        score = (weakness * 10.0) + (weight * 0.5) + relevance

        reasons = []
        if weakness:
            reasons.append(f"{weakness} unresolved mistake(s) in {topic.domain}")
        reasons.append(f"domain {topic.domain} carries ~{weight:.0f}% exam weight")
        reasons.append(f"{topic.practical_relevance.replace('_', ' ')} practical relevance")

        recommendations.append(
            Recommendation(topic=topic, score=score, reason="; ".join(reasons))
        )

    recommendations.sort(key=lambda rec: rec.score, reverse=True)
    return recommendations[:limit]
