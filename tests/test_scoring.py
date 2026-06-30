"""Tests for answer scoring."""

from __future__ import annotations

from az700_agent.scoring import AnswerKeyItem, grade


def _key():
    return [
        AnswerKeyItem("q1", "D1", "A"),
        AnswerKeyItem("q2", "D1", "B"),
        AnswerKeyItem("q3", "D2", "C"),
        AnswerKeyItem("q4", "D5", "D"),
    ]


def test_perfect_score():
    result = grade(_key(), {"q1": "A", "q2": "B", "q3": "C", "q4": "D"})
    assert result.correct == 4
    assert result.total == 4
    assert result.percent == 100.0
    assert result.passed is True
    assert result.wrong_question_ids == []


def test_partial_score_and_weak_domains():
    result = grade(_key(), {"q1": "A", "q2": "A", "q3": "A", "q4": "D"})
    assert result.correct == 2
    assert result.percent == 50.0
    assert result.passed is False
    # D1: 1/2 = 50%, D2: 0/1 = 0%, D5: 1/1 = 100%
    assert result.by_domain["D2"].percent == 0.0
    assert result.by_domain["D1"].percent == 50.0
    assert result.by_domain["D5"].percent == 100.0
    # Weakest first.
    assert result.weak_domains()[0] == "D2"


def test_answer_normalisation():
    result = grade([AnswerKeyItem("q1", "D1", "A")], {"q1": " a) "})
    assert result.correct == 1


def test_missing_answer_counts_wrong():
    result = grade(_key(), {"q1": "A"})
    assert result.correct == 1
    assert "q2" in result.wrong_question_ids
    assert "q3" in result.wrong_question_ids


def test_custom_pass_threshold():
    result = grade(
        [AnswerKeyItem("q1", "D1", "A"), AnswerKeyItem("q2", "D1", "B")],
        {"q1": "A", "q2": "X"},
        pass_threshold=50.0,
    )
    assert result.percent == 50.0
    assert result.passed is True


def test_empty_key():
    result = grade([], {})
    assert result.total == 0
    assert result.percent == 0.0
