"""Command-line interface for the AZ-700 agent support tooling.

This CLI exposes the deterministic helpers (blueprint queries, quiz planning,
scoring, mistake tracking, study recommendations) so they can be used outside the
Copilot agent flow and exercised in CI.

Examples::

    python -m src.cli blueprint
    python -m src.cli plan --total 50
    python -m src.cli plan --total 5 --domain D5
    python -m src.cli next
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

# Allow `python -m src.cli`, `python src/cli.py`, and installed-script invocation
# to all locate the az700_agent package living alongside this file.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from az700_agent.blueprint_loader import Blueprint, is_refresh_request
from az700_agent.mistake_tracker import MistakeTracker
from az700_agent.quiz_generator import build_plan
from az700_agent.source_registry import SourceRegistry
from az700_agent.study_planner import TopicMap, recommend_topics


def _cmd_blueprint(_: argparse.Namespace) -> int:
    blueprint = Blueprint.load()
    print(f"{blueprint.code}: {blueprint.name}")
    print(f"Cache version: {blueprint.cache_version}\n")
    for domain in blueprint.domains:
        print(f"  {domain.id} [{domain.weight}] {domain.name} ({len(domain.subtopics)} subtopics)")
    return 0


def _cmd_sources(_: argparse.Namespace) -> int:
    registry = SourceRegistry.load()
    for tier in (1, 2, 3):
        print(f"Tier {tier}:")
        for source in registry.by_tier(tier):
            print(f"  - {source.name} (trust: {source.trust})")
    return 0


def _cmd_plan(args: argparse.Namespace) -> int:
    blueprint = Blueprint.load()
    plan = build_plan(blueprint, total=args.total, domain_id=args.domain)
    print(f"Planned {plan.total} questions")
    print("By domain:")
    for domain_id, count in sorted(plan.by_domain().items()):
        print(f"  {domain_id}: {count}")
    return 0


def _cmd_next(args: argparse.Namespace) -> int:
    blueprint = Blueprint.load()
    topic_map = TopicMap.load()
    tracker = MistakeTracker.load()
    recs = recommend_topics(blueprint, topic_map, tracker, limit=args.limit)
    if not recs:
        print("No recommendations available (check prerequisites/completed topics).")
        return 0
    print("Study next:")
    for rank, rec in enumerate(recs, start=1):
        print(f"  {rank}. {rec.topic.label} [{rec.topic.domain}] (score {rec.score:.1f})")
        print(f"     why: {rec.reason}")
    return 0


def _cmd_refresh_check(args: argparse.Namespace) -> int:
    text = " ".join(args.text)
    if is_refresh_request(text):
        print("Refresh trigger detected. Delegate to the exam-analyst agent.")
        print("If sources are unavailable, report that the cached blueprint is unverified.")
    else:
        print("No refresh trigger. Use the cached blueprint as-is.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="az700", description="AZ-700 coach tooling")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("blueprint", help="Show cached exam blueprint summary").set_defaults(
        func=_cmd_blueprint
    )
    sub.add_parser("sources", help="List approved sources by tier").set_defaults(
        func=_cmd_sources
    )

    plan = sub.add_parser("plan", help="Compute a weighted quiz/exam plan")
    plan.add_argument("--total", type=int, default=50, help="Number of questions")
    plan.add_argument("--domain", default=None, help="Focus a single domain (e.g. D5)")
    plan.set_defaults(func=_cmd_plan)

    nxt = sub.add_parser("next", help="Recommend what to study next")
    nxt.add_argument("--limit", type=int, default=3, help="Number of recommendations")
    nxt.set_defaults(func=_cmd_next)

    refresh = sub.add_parser("refresh-check", help="Test if text triggers a blueprint refresh")
    refresh.add_argument("text", nargs="+", help="Text to test")
    refresh.set_defaults(func=_cmd_refresh_check)

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
