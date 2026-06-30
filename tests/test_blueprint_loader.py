"""Tests for the blueprint loader and quiz planning."""

from __future__ import annotations

import pytest

from az700_agent.blueprint_loader import Blueprint, BlueprintError, is_refresh_request
from az700_agent.quiz_generator import allocate_by_domain, build_plan


def test_blueprint_loads_from_cache():
    blueprint = Blueprint.load()
    assert blueprint.code == "AZ-700"
    assert len(blueprint.domains) == 5
    assert blueprint.domain_ids() == ["D1", "D2", "D3", "D4", "D5"]


def test_domain_lookup_and_subtopics():
    blueprint = Blueprint.load()
    d1 = blueprint.domain("D1")
    assert d1.priority == "very_high"
    assert any("VNet" in s for s in d1.subtopics)
    with pytest.raises(KeyError):
        blueprint.domain("D9")


def test_weight_midpoints_present():
    blueprint = Blueprint.load()
    midpoints = blueprint.weight_midpoints()
    assert set(midpoints) == {"D1", "D2", "D3", "D4", "D5"}
    assert all(value > 0 for value in midpoints.values())


@pytest.mark.parametrize(
    "text,expected",
    [
        ("/refresh-blueprint", True),
        ("please refresh blueprint now", True),
        ("update exam structure", True),
        ("sync with latest AZ-700 guide", True),
        ("check if AZ-700 changed", True),
        ("explain VNet peering", False),
        ("", False),
    ],
)
def test_refresh_trigger_detection(text, expected):
    assert is_refresh_request(text) is expected


def test_missing_blueprint_raises(tmp_path):
    with pytest.raises(BlueprintError):
        Blueprint.load(tmp_path / "does-not-exist.yaml")


def test_allocation_sums_to_total():
    blueprint = Blueprint.load()
    for total in (10, 25, 50, 7):
        counts = allocate_by_domain(blueprint, total)
        assert sum(counts.values()) == total


def test_focused_plan_targets_single_domain():
    blueprint = Blueprint.load()
    plan = build_plan(blueprint, total=5, domain_id="D5")
    assert plan.total == 5
    assert set(plan.by_domain()) == {"D5"}
    assert plan.by_domain()["D5"] == 5


def test_mock_plan_spreads_across_domains():
    blueprint = Blueprint.load()
    plan = build_plan(blueprint, total=50)
    by_domain = plan.by_domain()
    assert sum(by_domain.values()) == 50
    # D1 has the highest weight, so it should receive the most questions.
    assert by_domain["D1"] >= by_domain["D4"]
