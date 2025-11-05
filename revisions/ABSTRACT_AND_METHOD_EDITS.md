## Abstract Clarifications (Reviewer #6)

Revise phrasing:
- Replace "lack explainable justifications" with: "often do not provide legally faithful, auditable justifications traceable to statutes and procedures; prior works emphasize answer accuracy over statute-grounded reasoning (e.g., LegalBench, CaseHOLD), with limited evaluation of rationale faithfulness."
- Add citations on faithfulness vs plausibility (Agarwal et al., 2024) and LLM explanation reliability.

## Explainability vs Plausibility Statement

Add to methodology/limitations:
- "We distinguish plausibility (LLM-produced chains) from faithfulness (ground-truth alignment). Our pipeline enforces faithfulness via: (1) retrieval-constrained ARR; (2) CoV per-option support judgments; (3) human evaluation of faithfulness (see protocol)."

## Manual Validation Details (Sec 3.5)

Add subsections:
- Annotator profiles: postgraduate law students (n=2), external legal practitioner (meta-adjudicator); years of experience.
- Instructions: attach rubric/examples; define topical relevance, answer correctness, rationale faithfulness.
- Independence: no discussion during labeling; disagreements resolved by majority; meta-adjudicator breaks ties.
- Agreement: report Cohen’s kappa for (answer, rationale); include rater vs meta-adjudicator audit.

## Question Design Rationale (MCQ)

Add:
- Four options chosen to balance ambiguity and annotation load; at least two plausible distractors per item; procedure for distractor generation and validation.
- Discuss extension to open-ended QA; our evaluation still enforces option-wise support via CoV and semantic mapping.

## LLM-as-Judge Mitigations

Add:
- Different models/roles for ARR, Critique, Defense, Judge; no shared parameters for Judge and CoV.
- Judge blinded to earlier stage system prompts; CoV re-verifies independently with rule checks.
- Sensitivity analysis: swap Judge model; report stability.

## Data Splitting & Generalization

Add:
- Document stratified split by case source/date/topic; no overlap of passages across splits.
- Retrieval index built only on training statutes + public statutes; hold out test-only judgment passages.
- OOD results (see ROBUSTNESS_AND_OOD_PLAN.md) to be added in appendix.


