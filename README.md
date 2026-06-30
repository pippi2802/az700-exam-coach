# AZ-700 Certification Agent

A local, GitHub Copilot–powered **multi-agent assistant** for preparing for
**Microsoft Exam AZ-700: Designing and Implementing Microsoft Azure Networking
Solutions**.

It behaves like a structured Azure networking exam coach: it explains theory,
generates original scenario questions, designs hands-on labs, runs weighted mock
exams, grades answers, tracks mistakes, and recommends what to study next — all
grounded in trusted Microsoft sources and a **cached exam blueprint**.

## Quick start

```bash
# 1. Clone the repository
git clone https://github.com/pippi2802/az700-exam-coach.git
cd AZ-700-exam-coach

# 2. (Optional) install the Python tooling + dev dependencies
python -m pip install -e ".[dev]"

# 3. Verify everything works
python -m pytest -q
python -m src.cli blueprint
```

Then study with the agents:

1. Open the folder in **VS Code** with **GitHub Copilot Chat** enabled.
2. In Copilot Chat, open the prompt picker (type `/`) and run a command such as
   `initialise-agent`, `generate-quiz`, `generate-mock-exam`, or `build-study-plan`.
3. Or just ask the coach directly — e.g. *"explain VNet peering"* or
   *"what should I study next?"* — and the
   [orchestrator](agents/orchestrator.agent.md) routes to the right specialist.

Generated artefacts (quizzes, labs, mock exams, study plans, topic reviews) are
saved under [`outputs/`](outputs/). Your progress is tracked in
[`knowledge/mistake-log.yaml`](knowledge/mistake-log.yaml) and
[`knowledge/learner-profile.yaml`](knowledge/learner-profile.yaml).

> **Requirements:** Python 3.10+ and VS Code with GitHub Copilot. The Python
> tooling is optional — the agents work from the prompts alone — but it powers
> the CLI and the test suite.

## Key ideas

- **Layered multi-agent architecture.** A central orchestrator routes work to
  specialised agents (see [`agents/`](agents/)).
- **Persistent local memory.** Knowledge lives in [`knowledge/`](knowledge/) as
  YAML files and is reused instead of being rebuilt each session.
- **Cached blueprint.** The exam structure is cached in
  [`knowledge/exam-blueprint.yaml`](knowledge/exam-blueprint.yaml) and only
  refreshed on explicit request.
- **Source traceability.** Approved sources and trust tiers are defined in
  [`knowledge/approved-sources.yaml`](knowledge/approved-sources.yaml).
- **No exam dumps.** The system generates original content only.

## Agents

| Agent | Responsibility |
| --- | --- |
| [orchestrator](agents/orchestrator.agent.md) | Routes requests, keeps knowledge consistent |
| [exam-analyst](agents/exam-analyst.agent.md) | Owns the cached blueprint + refresh lifecycle |
| [theory-tutor](agents/theory-tutor.agent.md) | Explains theory with practical context |
| [question-writer](agents/question-writer.agent.md) | Generates original practice questions |
| [lab-designer](agents/lab-designer.agent.md) | Designs hands-on labs |
| [exam-simulator](agents/exam-simulator.agent.md) | Builds weighted mock exams |
| [evaluator](agents/evaluator.agent.md) | Grades answers, records mistakes |
| [source-curator](agents/source-curator.agent.md) | Enforces source trust tiers |
| [study-coach](agents/study-coach.agent.md) | Recommends what to study next |

## Prompts (Copilot slash commands)

Run these from the Copilot Chat prompt picker:

- `initialise-agent` — load cached knowledge and show your status.
- `refresh-blueprint` — refresh the cached exam structure (explicit only).
- `generate-quiz` — original practice quiz.
- `generate-lab` — hands-on lab.
- `generate-mock-exam` — full weighted mock exam.
- `explain-topic` — three-layer topic explanation.
- `grade-answers` — grade and record mistakes.
- `build-study-plan` — personalised study plan / "what next?".

## Refreshing the blueprint

The blueprint is treated as cached memory. It is **only** refreshed when you
explicitly ask using one of:

- `/refresh-blueprint`
- `refresh blueprint`
- `update exam structure`
- `sync with latest AZ-700 guide`
- `check if AZ-700 changed`

If source access is unavailable during a refresh, the agent will say it is using
the cached blueprint only and cannot verify whether it is current.

## Python tooling

Deterministic helpers back the agents and are independently testable.

```bash
# install (editable, with dev deps)
pip install -e ".[dev]"

# explore
python -m src.cli blueprint
python -m src.cli plan --total 50
python -m src.cli plan --total 5 --domain D5
python -m src.cli next

# test
pytest
```

| Module | Purpose |
| --- | --- |
| `blueprint_loader` | Load/query the cached blueprint; detect refresh triggers |
| `source_registry` | Load approved sources, enforce trust tiers |
| `quiz_generator` | Weighted quiz/mock-exam planning |
| `lab_generator` | Lab scaffolding + section validation |
| `scoring` | Grade overall and by domain |
| `mistake_tracker` | Persist/summarise mistakes |
| `study_planner` | Recommend topics from weak areas + weights |

## Repository layout

```text
.github/            Copilot instructions and prompt commands
agents/             Specialised agent definitions
knowledge/          Persistent YAML memory (blueprint, sources, topics, mistakes)
outputs/            Generated quizzes, labs, mock exams, study plans, reviews
src/                Python support library + CLI
tests/              Pytest suite
```

## Guardrails

- No real exam dumps or copied proprietary questions.
- No invented Azure limits, SKU capabilities, or pricing.
- Tier 3 sources are never the sole basis for a factual claim.
