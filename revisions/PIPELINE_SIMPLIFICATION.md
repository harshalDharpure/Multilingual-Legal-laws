## Simple-Case Bypass and Compute Budget

Addresses: Reviewer #5(2)

Observation: Accuracy of full pipeline (0.9380) is close to pretrained/fine-tuned baselines; the gain is mainly in NLI/faithfulness. For simple items, full CDA+CoV may be redundant.

Proposal:
- Add a gating heuristic before CDA:
  - High-confidence ARR: margin between top-2 option scores ≥ τ
  - Context sufficiency: retrieval coverage score ≥ γ
  - No multi-statute tag
- If all satisfied → skip CDA; run lightweight CoV (option check only)

Metrics to Report:
- % items routed to simple path
- Wall-clock/token savings
- Accuracy/NLI differences per path

Expected Outcome:
- 30–50% compute reduction on easy items with negligible accuracy delta; maintain NLI gains via light CoV.


