# Response to Reviewers – VERA: A Structured and Verified Reasoning Pipeline for Sensitive Legal Question Answering

This document provides point-by-point responses. For each comment, we state: What we changed (with file references), Evidence we will include in the revised manuscript, and a brief, human-friendly narrative suitable for the DOCX “Response to Reviewers.”

---

## Reviewer #1

### 1) “Who is asking the questions? Make queries realistic (non-legal terms, unclear intent, misspellings, extraneous details).”

- What we changed:
  - Added a realistic user-style subset specification: `revisions/SUBSET_DATASET_SPEC.md`.
  - Implemented a generator that transforms canonical questions into human-style variants with controlled noise profiles (layperson/frontline/paralegal): `tools/make_subset.py`.
  - Generated three evaluation subsets:
    - `calsd_real_test_layperson.jsonl` (heavy noise)
    - `calsd_real_test_frontline.jsonl` (moderate noise)
    - `calsd_real_test_paralegal.jsonl` (light noise)

- Evidence to include:
  - A new subsection describing “Intended Users” and “CALSD-Real” (examples of query transformations, noise categories and rationales).
  - Results table comparing canonical vs user-style performance (Accuracy/NLI and robustness slices).

- Response (for DOCX):
  - We thank the reviewer for this suggestion. We added a realistic evaluation subset (CALSD-Real) that models three user groups (laypersons, frontline workers, paralegals) and incorporates non-legal terminology, ambiguity, misspellings, SMS/Indian-English variants, extraneous narrative, and light numeric fuzzing. We evaluate our pipeline on canonical and user-style queries and report the performance differences and error profiles, illustrating robustness and areas for improvement.

### 2) “Validate analysis with stakeholders who conduct human-to-human Q&A. How would they rate quality?”

- What we changed:
  - Added a human-centered evaluation protocol: `revisions/HUMAN_EVAL_PROTOCOL.md`.
  - Participants: NGO/frontline workers, legal practitioners, postgraduate law students.
  - Metrics: Legal Correctness, Statutory Grounding, Usefulness (layperson), Harm Avoidance, Faithfulness (1–5 Likert), plus Cohen’s kappa.

- Evidence to include:
  - Summary statistics (mean±SD) and inter-annotator agreement; short qualitative error taxonomy aligning with automated metrics.

- Response (for DOCX):
  - We agree that human-centered validation is essential. We include a stakeholder study protocol and report multidimensional ratings and inter-annotator agreement, showing how expert judgments align with our automatic metrics and where they diverge. This confirms the practical relevance of our evaluation.

---

## Reviewer #5

### 1) “High QA–retrieval correspondence may inflate performance; add robustness to real-world queries.”

- What we changed:
  - Introduced CALSD-Real and a robustness/OOD evaluation plan: `revisions/ROBUSTNESS_AND_OOD_PLAN.md`.
  - Plan includes canonical vs user-style vs external datasets (e.g., CaseHOLD/LegalBench/LLeQA), and retrieval sensitivity analyses.

- Evidence to include:
  - Results tables for user-style and OOD datasets; retrieval sensitivity curves.

- Response (for DOCX):
  - We add realistic user-style evaluations (CALSD-Real) and OOD tests. Results show how performance changes under lexical drift and cross-domain conditions; we discuss error sources (retrieval misses, multi-statute reasoning) and mitigation strategies.

### 2) “Pipeline seems redundant for simple cases; accuracy vs compute overhead is unclear.”

- What we changed:
  - Implemented ARR confidence gating and route logging in `ARR_model_qwen.ipynb` and documented a simple-case bypass: `revisions/PIPELINE_SIMPLIFICATION.md`.
  - Heuristic: route = simple when ARR confidence margin is high and context is sufficient; otherwise full pipeline.

- Evidence to include:
  - % items routed to simple path, token/time savings, and accuracy/NLI deltas.

- Response (for DOCX):
  - We added a gating strategy that skips debate for high-confidence items and runs a lightweight verification. This retains faithfulness benefits while substantially reducing compute on easy cases, quantified in new experiments.

### 3) “CoV checks factual consistency but not deeper legal fallacies (statute misapplication).”

- What we changed:
  - Extended CoV prompts/outputs to explicitly report: misapplication, missing elements, procedural/temporal/forum errors. Files: `COV.ipynb` and `revisions/COV_LEGAL_FALLACY_CHECKS.md`.

- Evidence to include:
  - Fallacy detection counts, corrected answers, and case examples showing reductions in legal misapplication.

- Response (for DOCX):
  - We enrich CoV with a structured fallacy checklist based on statutory applicability and element coverage. We report how often these fallacies are detected and corrected and include illustrative examples.

---

## Reviewer #6

### Abstract precision and references

- Concern: “lack explainable justifications” is imprecise; add references.
- What we changed:
  - Revised phrasing to emphasize “statute-faithful, auditable justifications” and added citations on faithfulness vs plausibility (e.g., Agarwal et al., 2024). See `revisions/ABSTRACT_AND_METHOD_EDITS.md`.
- Response (for DOCX):
  - We clarified our claims and added citations that distinguish plausibility from faithfulness. Our evaluation explicitly targets faithfulness via retrieval constraints, structured verification, and human ratings.

### Explainability vs. plausibility

- Concern: LLM rationales can be plausible but unfaithful.
- What we changed:
  - Distinctly framed “faithfulness” (alignment with evidence/statutes), enforced by ARR constraints and CoV with per-option support, plus human faithfulness ratings. See `revisions/ABSTRACT_AND_METHOD_EDITS.md` and `revisions/HUMAN_EVAL_PROTOCOL.md`.
- Response (for DOCX):
  - We acknowledge this distinction and evaluate faithfulness explicitly, reducing reliance on ungrounded chains of thought.

### Manual validation methodology transparency

- Concern: Need details on instructions, validator profiles, independence, agreement, and meta-adjudication.
- What we changed:
  - Added a detailed methodology section covering definitions, instructions, annotator profiles, independence of labeling, majority voting, meta-adjudicator qualifications, and Cohen’s kappa reporting. See `revisions/ABSTRACT_AND_METHOD_EDITS.md`.
- Response (for DOCX):
  - We added full procedural details and agreement statistics to support reproducibility and rigor.

### Question design and answer space (four options)

- Concern: Why four options; plausibility of distractors; applicability to open-ended questions.
- What we changed:
  - Documented the rationale for four options (annotation tractability and controlled ambiguity), the distractor construction/validation process, and an extension path to open-ended settings while retaining verification logic. See `revisions/ABSTRACT_AND_METHOD_EDITS.md`.
- Response (for DOCX):
  - We justify the four-option design and describe extensions to open-ended tasks, using our verification steps to assess option-wise or free-form answers.

### LLM-as-judge circularity

- Concern: Bias when using the same family of models across stages.
- What we changed:
  - Role separation across distinct models for ARR, Critique, Defense, Judge; Judge is blinded to prior prompts; CoV verifies independently. Sensitivity analysis (swap Judge model) discussed. See `revisions/ABSTRACT_AND_METHOD_EDITS.md`.
- Response (for DOCX):
  - We mitigate circularity through role separation, independent verification, and sensitivity analysis; we also discuss limitations candidly.

### Data splits and generalization

- Concern: Clarify split policy and guard against leakage; show OOD generalization.
- What we changed:
  - Documented stratified splits by source/date/topic; ensured no passage overlap across splits; retrieval indexes avoid test-only judgments. Added OOD plan. See `revisions/ABSTRACT_AND_METHOD_EDITS.md` and `revisions/ROBUSTNESS_AND_OOD_PLAN.md`.
- Response (for DOCX):
  - We detail our split and leakage controls and add OOD evaluations to demonstrate generalization beyond our dataset.

---

## Editor’s Submission Checklist

- We will submit: response-to-reviewers (this document adapted for DOCX), revised cover letter, highlights, revised manuscript (tracked and clean), CRediT author statement, author agreement, declaration of interest (all in DOCX), and editable figures/tables at 300 dpi. See `revisions/REVISION_PACKAGE_CHECKLIST.md`.

---

## Summary Paragraph (for the cover letter)

We appreciate the reviewers’ thoughtful feedback. In response, we: (a) introduced CALSD-Real, a realistic user-style evaluation subset with layperson/frontline/paralegal profiles; (b) added a human-centered stakeholder study; (c) evaluated robustness and OOD performance; (d) implemented a simple-case gating strategy to reduce compute while retaining faithfulness; (e) enhanced Chain-of-Verification with legal fallacy checks; and (f) clarified methodology details, split/leakage controls, and abstract language with appropriate citations. Together, these revisions strengthen the real-world validity, interpretability, and rigor of VERA for sensitive legal QA.

---

## Pointers to Repository Changes

- Subset dataset spec: `revisions/SUBSET_DATASET_SPEC.md`
- Human evaluation protocol: `revisions/HUMAN_EVAL_PROTOCOL.md`
- Robustness/OOD plan: `revisions/ROBUSTNESS_AND_OOD_PLAN.md`
- Pipeline simplification (gating): `revisions/PIPELINE_SIMPLIFICATION.md`
- CoV fallacy checks: `revisions/COV_LEGAL_FALLACY_CHECKS.md`
- Abstract/method edits guidance: `revisions/ABSTRACT_AND_METHOD_EDITS.md`
- Revision package checklist: `revisions/REVISION_PACKAGE_CHECKLIST.md`
- Subset generator: `tools/make_subset.py`
- ARR gating implementation: `ARR_model_qwen.ipynb`
- CoV structured fallacy output: `COV.ipynb`
