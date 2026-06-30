"""Persist and summarise learner mistakes in ``knowledge/mistake-log.yaml``."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any

import yaml

from . import KNOWLEDGE_DIR

DEFAULT_MISTAKE_LOG_PATH = KNOWLEDGE_DIR / "mistake-log.yaml"
DOMAIN_IDS = ("D1", "D2", "D3", "D4", "D5")


@dataclass
class Mistake:
    """A single recorded learner mistake."""

    domain: str
    subtopic: str
    question_summary: str
    chosen_answer: str
    correct_answer: str
    misconception: str
    id: str = ""
    date: str = ""
    topic_id: str = ""
    question_ref: str = ""
    severity: str = "medium"
    resolved: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "date": self.date,
            "domain": self.domain,
            "subtopic": self.subtopic,
            "topic_id": self.topic_id,
            "question_ref": self.question_ref,
            "question_summary": self.question_summary,
            "chosen_answer": self.chosen_answer,
            "correct_answer": self.correct_answer,
            "misconception": self.misconception,
            "severity": self.severity,
            "resolved": self.resolved,
        }


class MistakeTracker:
    """Read/append/summarise the mistake log."""

    def __init__(self, data: dict[str, Any] | None = None) -> None:
        self._data: dict[str, Any] = data or {"mistakes": [], "summary": {}}
        self._data.setdefault("mistakes", [])

    # -- persistence ----------------------------------------------------------
    @classmethod
    def load(cls, path: Path | str | None = None) -> "MistakeTracker":
        log_path = Path(path) if path is not None else DEFAULT_MISTAKE_LOG_PATH
        if not log_path.exists():
            return cls()
        with log_path.open("r", encoding="utf-8") as handle:
            data = yaml.safe_load(handle) or {}
        if not isinstance(data, dict):
            data = {"mistakes": []}
        return cls(data)

    def save(self, path: Path | str | None = None) -> None:
        log_path = Path(path) if path is not None else DEFAULT_MISTAKE_LOG_PATH
        log_path.parent.mkdir(parents=True, exist_ok=True)
        self.recompute_summary()
        with log_path.open("w", encoding="utf-8") as handle:
            yaml.safe_dump(self._data, handle, sort_keys=False, allow_unicode=True)

    # -- accessors ------------------------------------------------------------
    @property
    def mistakes(self) -> list[dict[str, Any]]:
        return list(self._data.get("mistakes", []))

    @property
    def summary(self) -> dict[str, Any]:
        return dict(self._data.get("summary", {}))

    def _next_id(self) -> str:
        existing = self._data.get("mistakes", [])
        return f"M-{len(existing) + 1:04d}"

    # -- mutation -------------------------------------------------------------
    def add(self, mistake: Mistake) -> Mistake:
        """Append a mistake, assigning id/date when not provided."""
        if not mistake.id:
            mistake.id = self._next_id()
        if not mistake.date:
            mistake.date = date.today().isoformat()
        self._data.setdefault("mistakes", []).append(mistake.to_dict())
        self.recompute_summary()
        return mistake

    def resolve(self, mistake_id: str) -> bool:
        """Mark a mistake resolved (after a successful re-test)."""
        for entry in self._data.get("mistakes", []):
            if entry.get("id") == mistake_id:
                entry["resolved"] = True
                self.recompute_summary()
                return True
        return False

    # -- analysis -------------------------------------------------------------
    def counts_by_domain(self, include_resolved: bool = False) -> dict[str, int]:
        counts = {domain: 0 for domain in DOMAIN_IDS}
        for entry in self._data.get("mistakes", []):
            if not include_resolved and entry.get("resolved"):
                continue
            domain = entry.get("domain")
            if domain in counts:
                counts[domain] += 1
            elif domain:
                counts[domain] = counts.get(domain, 0) + 1
        return counts

    def weakest_domains(self, limit: int = 3) -> list[str]:
        """Domains with the most unresolved mistakes, strongest signal first."""
        counts = self.counts_by_domain()
        ranked = sorted(
            (d for d in counts if counts[d] > 0),
            key=lambda d: counts[d],
            reverse=True,
        )
        return ranked[:limit]

    def recompute_summary(self) -> dict[str, Any]:
        counts = self.counts_by_domain()
        total = sum(1 for _ in self._data.get("mistakes", []))
        summary = {
            "total_mistakes": total,
            "by_domain": counts,
            "weakest_domains": self.weakest_domains(),
            "last_updated": date.today().isoformat(),
        }
        self._data["summary"] = summary
        return summary
