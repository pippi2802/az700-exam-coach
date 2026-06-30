---
applyTo: "outputs/labs/**,agents/lab-designer.agent.md"
---

# Lab authoring standards

Every lab must include, in order:

1. Title
2. Exam domain (D1-D5)
3. Objective
4. Scenario
5. Azure services used
6. Prerequisites
7. Tasks (numbered, sequential)
8. Azure CLI commands where appropriate (fenced ```bash blocks)
9. Validation steps
10. Expected result
11. Cleanup steps (mandatory — avoid lingering cost)
12. Extension challenge
13. Sources used

Rules:

- Prefer realistic, work-like labs (hub-spoke, peering, UDRs, Azure Firewall,
  VPN, ExpressRoute concepts, Private Endpoints, DNS Private Resolver,
  Application Gateway, Front Door, Load Balancer, Network Watcher).
- If CLI syntax may have changed, instruct the learner to validate against
  Microsoft Learn instead of guessing.
- Never invent resource limits, quotas, or pricing.
- Always provide cleanup steps that fully remove created resources.
