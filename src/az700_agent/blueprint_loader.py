"""Load and query the cached AZ-700 exam blueprint.

The blueprint is the persistent memory of the exam structure. Agents and tooling
read it instead of rebuilding the exam scope on every run. Refreshing is a manual,
explicit action handled elsewhere; this module is read-only.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from . import KNOWLEDGE_DIR

DEFAULT_BLUEPRINT_PATH = KNOWLEDGE_DIR / "exam-blueprint.yaml"

# Phrases that explicitly request a blueprint refresh.
REFRESH_TRIGGERS = (
    "/refresh-blueprint",
    "refresh blueprint",
    "update exam structure",
    "sync with latest az-700 guide",
    "check if az-700 changed",
)


@dataclass(frozen=True)
class Domain:
    """A single exam domain from the blueprint."""

    id: str
    name: str
    weight: str
    weight_midpoint: float
    priority: str
    subtopics: tuple[str, ...]


class BlueprintError(RuntimeError):
    """Raised when the blueprint file is missing or malformed."""


class Blueprint:
    """Typed accessor over the cached exam blueprint YAML."""

    def __init__(self, data: dict[str, Any]) -> None:
        if "exam" not in data:
            raise BlueprintError("Blueprint is missing the top-level 'exam' key.")
        self._data = data
        self._exam = data["exam"]

    # -- construction ---------------------------------------------------------
    @classmethod
    def load(cls, path: Path | str | None = None) -> "Blueprint":
        """Load the blueprint from ``path`` (defaults to the cached file)."""
        blueprint_path = Path(path) if path is not None else DEFAULT_BLUEPRINT_PATH
        if not blueprint_path.exists():
            raise BlueprintError(f"Blueprint file not found: {blueprint_path}")
        with blueprint_path.open("r", encoding="utf-8") as handle:
            data = yaml.safe_load(handle)
        if not isinstance(data, dict):
            raise BlueprintError("Blueprint YAML did not parse to a mapping.")
        return cls(data)

    # -- metadata -------------------------------------------------------------
    @property
    def code(self) -> str:
        return self._exam.get("code", "")

    @property
    def name(self) -> str:
        return self._exam.get("name", "")

    @property
    def cache_version(self) -> str:
        return str(self._exam.get("cache_version", ""))

    # -- domains --------------------------------------------------------------
    @property
    def domains(self) -> list[Domain]:
        domains: list[Domain] = []
        for raw in self._exam.get("domains", []):
            domains.append(
                Domain(
                    id=raw["id"],
                    name=raw["name"],
                    weight=str(raw.get("weight", "")),
                    weight_midpoint=float(raw.get("weight_midpoint", 0)),
                    priority=raw.get("priority", ""),
                    subtopics=tuple(raw.get("subtopics", [])),
                )
            )
        return domains

    def domain(self, domain_id: str) -> Domain:
        """Return a single domain by id (e.g. ``"D1"``)."""
        for domain in self.domains:
            if domain.id == domain_id:
                return domain
        raise KeyError(f"Unknown domain id: {domain_id}")

    def domain_ids(self) -> list[str]:
        return [domain.id for domain in self.domains]

    def weight_midpoints(self) -> dict[str, float]:
        """Map of domain id -> weight midpoint percentage."""
        return {domain.id: domain.weight_midpoint for domain in self.domains}

    def subtopics(self, domain_id: str) -> tuple[str, ...]:
        return self.domain(domain_id).subtopics

    # -- distributions --------------------------------------------------------
    def difficulty_distribution(self) -> dict[str, str]:
        return dict(self._exam.get("difficulty_distribution", {}))

    def question_distribution(self) -> dict[str, str]:
        return dict(self._exam.get("question_distribution_guidance", {}))

    def mock_exam_defaults(self) -> dict[str, Any]:
        return dict(self._exam.get("mock_exam_defaults", {}))


def is_refresh_request(text: str) -> bool:
    """Return True if ``text`` contains an explicit blueprint refresh trigger."""
    lowered = text.strip().lower()
    return any(trigger in lowered for trigger in REFRESH_TRIGGERS)
