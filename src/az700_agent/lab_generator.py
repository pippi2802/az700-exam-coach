"""Scaffold lab definitions for the lab-designer agent.

Provides a structured, validated lab template so generated labs always contain the
required sections defined in ``.github/instructions/labs.instructions.md``.
"""

from __future__ import annotations

from dataclasses import dataclass, field

# Canonical, ordered set of sections every lab must contain.
REQUIRED_SECTIONS = (
    "Title",
    "Exam domain",
    "Objective",
    "Scenario",
    "Azure services used",
    "Prerequisites",
    "Tasks",
    "Validation steps",
    "Expected result",
    "Cleanup steps",
    "Extension challenge",
    "Sources used",
)


@dataclass
class LabSpec:
    """Inputs used to scaffold a lab."""

    title: str
    domain_id: str
    objective: str
    scenario: str = ""
    services: list[str] = field(default_factory=list)
    prerequisites: list[str] = field(default_factory=list)
    tasks: list[str] = field(default_factory=list)
    validation: list[str] = field(default_factory=list)
    expected_result: str = ""
    cleanup: list[str] = field(default_factory=list)
    extension: str = ""
    sources: list[str] = field(default_factory=list)


def scaffold_lab(spec: LabSpec) -> str:
    """Render a Markdown lab skeleton from ``spec``.

    Empty fields are rendered as TODO placeholders so the agent can fill them in
    while guaranteeing every required section is present.
    """

    def bullet_list(items: list[str], placeholder: str) -> str:
        if not items:
            return f"- _{placeholder}_"
        return "\n".join(f"- {item}" for item in items)

    def numbered_list(items: list[str], placeholder: str) -> str:
        if not items:
            return f"1. _{placeholder}_"
        return "\n".join(f"{i}. {item}" for i, item in enumerate(items, start=1))

    parts = [
        f"# {spec.title or '_TODO: lab title_'}",
        "",
        f"**Exam domain:** {spec.domain_id}",
        "",
        "## Objective",
        spec.objective or "_TODO: objective_",
        "",
        "## Scenario",
        spec.scenario or "_TODO: scenario_",
        "",
        "## Azure services used",
        bullet_list(spec.services, "TODO: services"),
        "",
        "## Prerequisites",
        bullet_list(spec.prerequisites, "TODO: prerequisites"),
        "",
        "## Tasks",
        numbered_list(spec.tasks, "TODO: tasks"),
        "",
        "## Validation steps",
        numbered_list(spec.validation, "TODO: validation"),
        "",
        "## Expected result",
        spec.expected_result or "_TODO: expected result_",
        "",
        "## Cleanup steps",
        numbered_list(spec.cleanup, "TODO: cleanup"),
        "",
        "## Extension challenge",
        spec.extension or "_TODO: extension challenge_",
        "",
        "## Sources used",
        bullet_list(spec.sources, "TODO: sources"),
        "",
    ]
    return "\n".join(parts)


def missing_sections(markdown: str) -> list[str]:
    """Return required sections not present in a rendered lab document."""
    missing = []
    for section in REQUIRED_SECTIONS:
        # Title appears as an H1; the rest as H2 or bold labels.
        if section == "Title":
            if not markdown.lstrip().startswith("#"):
                missing.append(section)
        elif section == "Exam domain":
            if "Exam domain" not in markdown:
                missing.append(section)
        elif f"## {section}" not in markdown:
            missing.append(section)
    return missing
