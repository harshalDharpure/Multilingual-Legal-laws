## CALSD-Real: Subset Dataset Specification for Realistic User Queries

Purpose: Address Reviewer #1 and #5(1) by creating a realistic subset reflecting real-world query inputs (non-legal wording, ambiguity, misspellings, extraneous details), plus robustness tags for retrieval mismatch.

Scope: 2,000 items sampled from `train_data.jsonl` and `test_data.json` with paired (a) canonical MCQ and (b) user-style noisy query view mapped to the same gold answer/rationale.

Target Users (documented in paper):
- Non-lawyers (survivors/caregivers) seeking information
- Frontline service providers (counsellors, helpline, police desk)
- Paralegals/NGO case workers

Schema (JSONL per line):
{
  "id": string,                      // stable id
  "passage": string,                 // original legal context (optional in user split)
  "question_canonical": string,      // original CALSD multiple-choice question
  "options": {"A": str, "B": str, "C": str, "D": str},
  "correct_answer_text": string,     // full text of the correct option
  "rationale_statutory": string,     // gold legal rationale
  "question_user": string,           // realistic user-style query
  "noise": {                         // noise/transformation metadata
    "misspellings": int,
    "colloquialisms": int,
    "extraneous": bool,
    "ambiguity": bool
  },
  "robustness_tags": [               // for analysis
    "retrieval_hard",                // low lexical overlap with statutes
    "long_context",                  // long passage
    "multi_statute",                 // requires combining provisions
    "temporal_issue",                // timing/age/bail window
    "entity_coref"                    // pronouns/names
  ]
}

Construction Protocol:
1) Sampling: stratify by topic (POCSO sections, JJ, IPC), difficulty, and option confusability.
2) Transformations (apply 1–3 per item):
   - Misspellings: Levenshtein 1–2 edits (e.g., "POCSO"→"POCS0", "juvenile"→"juvanile").
   - Colloquial paraphrase: replace legalese with everyday terms ("anticipatory bail"→"bail before arrest").
   - Extraneous details: prepend or append unrelated but plausible narrative.
   - Ambiguity: remove explicit statute names while keeping facts.
3) Quality Checks:
   - Deterministic seed; store noise counts.
   - Ensure gold answer remains correct under the noisy query.
   - Flag items where retrieval degrades (robustness_tags.add("retrieval_hard")).

Evaluation Additions:
- Report accuracy and NLI on (a) canonical and (b) user-style queries.
- Robustness slices by tags (retrieval_hard, multi_statute, etc.).
- Human rater study (see HUMAN_EVAL_PROTOCOL.md) for usefulness/faithfulness on user-style queries.

Release Files:
- `calsd_real_train.jsonl` (≈1,500)
- `calsd_real_test.jsonl` (≈500)

Licensing/Safety:
- Remove personally identifying details; synthetic noise only.
- Keep statutory text excerpts minimal; cite sources.


