## Robustness and OOD Evaluation Plan

Addresses: Reviewer #5(1), Reviewer #6 (generalization)

Datasets:
- In-domain user-style: CALSD-Real (subset spec)
- OOD legal QA: CaseHOLD (holdings), LegalBench subsets (Indian/English tasks), LLeQA (long-form QA)

Setups:
1) Zero-shot inference with existing pipeline (no re-tuning)
2) Retrieval-only augmentation using public statutes (for non-Indian corpora, restrict to generic criminal procedure where applicable)

Metrics:
- MCQ Accuracy (semantic matching for free-form answers)
- NLI entailment to reference rationales (where available)
- Citation density and statute hit-rate (where statutes exist)

Analyses:
- Performance deltas vs CALSD canonical; vs CALSD-Real
- Error breakdown: retrieval misses, statute mismatch, temporal/age errors
- Sensitivity to retrieval K, chunk sizes

Reporting:
- Tables for OOD datasets and user-style subset
- Appendix with ablations and retrieval sensitivity curves


