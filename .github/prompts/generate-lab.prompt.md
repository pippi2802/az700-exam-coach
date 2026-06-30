---
mode: agent
description: Generate a hands-on AZ-700 Azure networking lab.
---

# Generate Lab

Act as the **lab-designer** agent (`agents/lab-designer.agent.md`).

Inputs (ask if not provided):
- Lab topic (e.g. hub-spoke, Azure Firewall, Private Endpoint, VPN).
- Difficulty / depth.

Produce a lab with: title, exam domain, objective, scenario, Azure services used,
prerequisites, numbered tasks, Azure CLI commands where appropriate, validation
steps, expected result, cleanup steps, extension challenge, and sources used.

Save to `outputs/labs/lab-<topic>.md`.

If CLI syntax may be outdated, tell me to validate against Microsoft Learn. Always
include cleanup steps. Never invent limits or pricing.
