# AGENTS.md

Operating guide for AI agents working in this repository. This complements
[`.github/copilot-instructions.md`](.github/copilot-instructions.md).

## What this repository is

A multi-agent AZ-700 (Azure Networking) certification coach. Agents read
persistent YAML memory in `knowledge/`, generate study artefacts into `outputs/`,
and are backed by a deterministic Python library in `src/`.

## Architecture

```
orchestrator
├── exam-analyst      (owns cached blueprint + refresh)
├── theory-tutor      (explanations)
├── question-writer   (practice questions)
├── lab-designer      (hands-on labs)
├── exam-simulator    (mock exams)
├── evaluator         (grading + mistake logging)
├── source-curator    (source trust enforcement)
└── study-coach       (what to study next)
```

The orchestrator routes each request to a specialist (see
[`agents/orchestrator.agent.md`](agents/orchestrator.agent.md)).

## Persistent memory (read before acting)

| File | Use |
| --- | --- |
| `knowledge/exam-blueprint.yaml` | Cached exam structure — do **not** rebuild it |
| `knowledge/topic-map.yaml` | Topic dependencies and study order |
| `knowledge/approved-sources.yaml` | Source trust tiers and citation policy |
| `knowledge/question-taxonomy.yaml` | Required question fields and types |
| `knowledge/mistake-log.yaml` | Recorded learner mistakes |
| `knowledge/learner-profile.yaml` | Learner state, weak areas, history |

Always prefer cached knowledge over re-deriving exam scope.

## Blueprint refresh policy

Refresh `knowledge/exam-blueprint.yaml` **only** when the user explicitly uses a
trigger: `/refresh-blueprint`, `refresh blueprint`, `update exam structure`,
`sync with latest AZ-700 guide`, `check if AZ-700 changed`.

If sources are unavailable during refresh, do not modify the file and state that
the cached blueprint is unverified. Preserve `change_history`.

## Output conventions

| Artefact | Location |
| --- | --- |
| Quizzes | `outputs/quizzes/` |
| Labs | `outputs/labs/` |
| Mock exams | `outputs/mock-exams/` |
| Study plans | `outputs/study-plans/` |
| Topic reviews | `outputs/topic-reviews/` |

## Hard rules

- No real exam dumps or copied proprietary questions — original content only.
- No invented Azure limits, SKU capabilities, quotas, or pricing.
- Tier 3 sources are never the sole basis for a factual claim.
- Every substantive answer ends with a "Sources used" section unless the user
  asks for a quick answer.
- Keep YAML valid so the `src/` tooling and `tests/` keep passing.

## Validating changes

```bash
pip install -e ".[dev]"
pytest
```
