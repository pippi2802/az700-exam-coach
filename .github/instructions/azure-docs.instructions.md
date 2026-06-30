---
applyTo: "**"
---

# Azure documentation grounding

When making factual claims about Azure networking services, behaviour, limits,
SKUs, or capabilities for AZ-700 content:

- Ground claims in Microsoft Learn (Tier 1) sources listed in
  `knowledge/approved-sources.yaml`.
- Use the Azure Architecture Center, Cloud Adoption Framework, and
  Well-Architected Framework (Tier 2) for design and scenario examples.
- Do **not** invent Azure limits, SKU capabilities, quotas, or pricing.
- If you are unsure whether a detail (especially CLI syntax, limits, or a recent
  feature) is current, say so and tell the learner to verify against Microsoft Learn.
- Prefer the cached `knowledge/exam-blueprint.yaml` over re-deriving exam scope.

Always include a "Sources used" section for substantive answers unless the
learner explicitly asks for a quick answer.
