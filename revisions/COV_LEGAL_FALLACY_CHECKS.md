## CoV Enhancements: Legal Fallacy Detection

Addresses: Reviewer #5(3)

Add rule-based and prompt-based checks in CoV:
1) Statute Applicability Matrix:
   - Age thresholds (e.g., consent irrelevant under POCSO)
   - Procedure mandates: Sec 19 POCSO (mandatory reporting), Sec 33(7) (privacy)
   - Bail considerations differ for JJ vs adult
   - Output: flags when rationale cites inapplicable provisions

2) Burden/Element Checklist:
   - Map options to required statutory elements (penetrative vs. assault; aggravated factors)
   - Verify that cited facts cover elements; else mark incomplete reasoning

3) Temporal/Forum Fallacies:
   - Misuse of anticipatory bail post-arrest
   - Wrong forum/procedure cites (JJ Board vs Sessions Court)

Implementation Note:
- Extend CoV prompt with explicit fallacy checklist; include a structured JSON section: {"misapplication": [...], "missing_elements": [...], "procedural_errors": [...]}.

Reporting:
- Count of detected fallacies per 1k items; correction rate; effect on NLI.


