"""AZ-700 certification agent support library.

This package provides the deterministic, testable building blocks that back the
multi-agent AZ-700 study system:

* :mod:`blueprint_loader` - load and query the cached exam blueprint.
* :mod:`source_registry` - load approved sources and enforce trust tiers.
* :mod:`quiz_generator` - build weighted quiz/exam question plans.
* :mod:`lab_generator` - scaffold lab definitions.
* :mod:`scoring` - grade answers overall and by domain.
* :mod:`mistake_tracker` - persist and summarise learner mistakes.
* :mod:`study_planner` - recommend topics from weak areas and weights.
"""

from __future__ import annotations

from pathlib import Path

__all__ = [
    "REPO_ROOT",
    "KNOWLEDGE_DIR",
    "OUTPUTS_DIR",
    "__version__",
]

__version__ = "0.1.0"

# src/az700_agent/__init__.py -> repo root is two levels up.
REPO_ROOT = Path(__file__).resolve().parents[2]
KNOWLEDGE_DIR = REPO_ROOT / "knowledge"
OUTPUTS_DIR = REPO_ROOT / "outputs"
