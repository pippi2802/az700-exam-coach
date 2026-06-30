"""Load approved sources and enforce the source trust policy."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from . import KNOWLEDGE_DIR

DEFAULT_SOURCES_PATH = KNOWLEDGE_DIR / "approved-sources.yaml"

# Section name -> numeric tier.
_TIER_SECTIONS = {
    "tier_1_authoritative": 1,
    "tier_2_design_guidance": 2,
    "tier_3_optional": 3,
}


@dataclass(frozen=True)
class Source:
    """An approved (or restricted) reference source."""

    name: str
    tier: int
    trust: str
    use_for: tuple[str, ...]
    url: str | None = None
    rule: str | None = None

    @property
    def is_authoritative(self) -> bool:
        return self.tier == 1

    @property
    def can_be_sole_source(self) -> bool:
        """Tier 3 sources may never be the only source for a factual claim."""
        return self.tier <= 2


class SourceRegistryError(RuntimeError):
    """Raised when the sources file is missing or malformed."""


class SourceRegistry:
    """Typed accessor over ``approved-sources.yaml``."""

    def __init__(self, data: dict[str, Any]) -> None:
        if "approved_sources" not in data:
            raise SourceRegistryError("Missing top-level 'approved_sources' key.")
        self._data = data
        self._sources = self._parse(data["approved_sources"])

    @staticmethod
    def _parse(approved: dict[str, Any]) -> list[Source]:
        sources: list[Source] = []
        for section, tier in _TIER_SECTIONS.items():
            for raw in approved.get(section, []):
                sources.append(
                    Source(
                        name=raw["name"],
                        tier=tier,
                        trust=raw.get("trust", ""),
                        use_for=tuple(raw.get("use_for", [])),
                        url=raw.get("url"),
                        rule=raw.get("rule"),
                    )
                )
        return sources

    @classmethod
    def load(cls, path: Path | str | None = None) -> "SourceRegistry":
        sources_path = Path(path) if path is not None else DEFAULT_SOURCES_PATH
        if not sources_path.exists():
            raise SourceRegistryError(f"Sources file not found: {sources_path}")
        with sources_path.open("r", encoding="utf-8") as handle:
            data = yaml.safe_load(handle)
        if not isinstance(data, dict):
            raise SourceRegistryError("Sources YAML did not parse to a mapping.")
        return cls(data)

    @property
    def sources(self) -> list[Source]:
        return list(self._sources)

    def by_tier(self, tier: int) -> list[Source]:
        return [source for source in self._sources if source.tier == tier]

    def find(self, name: str) -> Source | None:
        lowered = name.strip().lower()
        for source in self._sources:
            if source.name.lower() == lowered:
                return source
        return None

    def is_trusted(self, name: str) -> bool:
        """A source is 'trusted' for factual claims if it is Tier 1 or Tier 2."""
        source = self.find(name)
        return source is not None and source.tier <= 2

    def validate_citation(self, source_names: list[str]) -> bool:
        """A citation set is valid when at least one Tier 1/Tier 2 source backs it.

        Tier 3 sources alone are never sufficient for a factual claim.
        """
        return any(self.is_trusted(name) for name in source_names)
