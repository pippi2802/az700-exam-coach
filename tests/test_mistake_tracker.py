"""Tests for the mistake tracker."""

from __future__ import annotations

from az700_agent.mistake_tracker import Mistake, MistakeTracker


def _mistake(domain="D2", subtopic="ExpressRoute FastPath"):
    return Mistake(
        domain=domain,
        subtopic=subtopic,
        question_summary="When to use FastPath",
        chosen_answer="B",
        correct_answer="C",
        misconception="Confused FastPath with Global Reach",
    )


def test_add_assigns_id_and_date():
    tracker = MistakeTracker()
    added = tracker.add(_mistake())
    assert added.id == "M-0001"
    assert added.date  # non-empty ISO date
    assert len(tracker.mistakes) == 1


def test_ids_increment():
    tracker = MistakeTracker()
    tracker.add(_mistake())
    second = tracker.add(_mistake())
    assert second.id == "M-0002"


def test_summary_counts_by_domain():
    tracker = MistakeTracker()
    tracker.add(_mistake(domain="D2"))
    tracker.add(_mistake(domain="D2"))
    tracker.add(_mistake(domain="D5"))
    summary = tracker.recompute_summary()
    assert summary["total_mistakes"] == 3
    assert summary["by_domain"]["D2"] == 2
    assert summary["by_domain"]["D5"] == 1
    assert summary["weakest_domains"][0] == "D2"


def test_resolve_excludes_from_weak_counts():
    tracker = MistakeTracker()
    first = tracker.add(_mistake(domain="D2"))
    tracker.add(_mistake(domain="D5"))
    assert tracker.resolve(first.id) is True
    counts = tracker.counts_by_domain()
    assert counts["D2"] == 0
    assert counts["D5"] == 1
    # Resolving an unknown id returns False.
    assert tracker.resolve("M-9999") is False


def test_round_trip_save_and_load(tmp_path):
    path = tmp_path / "mistake-log.yaml"
    tracker = MistakeTracker()
    tracker.add(_mistake(domain="D3"))
    tracker.save(path)

    reloaded = MistakeTracker.load(path)
    assert len(reloaded.mistakes) == 1
    assert reloaded.mistakes[0]["domain"] == "D3"
    assert reloaded.summary["total_mistakes"] == 1


def test_load_missing_file_is_empty(tmp_path):
    tracker = MistakeTracker.load(tmp_path / "nope.yaml")
    assert tracker.mistakes == []
