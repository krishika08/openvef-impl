> **Historical audit record:** this Step 1 resolution predates the v0.7 prompt-factor decision. Its direct-versus-structured wording is not the current experimental factor. See the v0.7 Charter/Protocol.

# OpenVEF Step 1 — Claude Audit Resolution

**Date:** 22 November 2026  
**Input:** Claude Pro's independent audit, *OpenVEF Step 1 Audit: Verify the Verifier* (`07_Claude_Step1_Audit_Raw.txt`)  
**Disposition:** PASS WITH CORRECTIONS; paper analysis revised to v0.2.

## 1. Findings accepted

The following Claude findings are accepted and incorporated:

1. The benchmark funnel already separates non-activated mutants from activated-but-still-passing candidates. OpenVEF cannot claim stimulus-versus-checker attribution itself as a novel idea.
2. The paper's 27 undetected candidates split into 13 not observed by the ACC and 14 for which the ACC described the bug but no assertion qualified.
3. The earlier analysis omitted the authors' scoped “to our knowledge, first framework” claim and the distinction from testbench grading.
4. The “other” assertion category includes undetermined, vacuous, and assertions proven on both mutant and reference.
5. A false positive means an assertion has a counterexample on the reference RTL.
6. The specification-only baseline removes multiple inputs and changes generator scheduling; it is not a clean one-factor trace/no-trace ablation.
7. The paper's equivalence filter is an unbounded proof over reachable states, unlike OpenVEF's planned bounded miter result.
8. The distinction between output-only non-activation and signal-by-signal activation comparison is textually ambiguous and must remain an open question.
9. Commercial-tool dependence and several other consequences should be labelled reviewer observations, not author-acknowledged limitations.
10. The analysis must not claim all PDF page images were inspected when the original PDF retrieval was blocked.

## 2. Claude findings refined after checking the extracted paper text

The following clarifications were made while reconciling Claude's report with the complete extracted text available through a PDF mirror:

- The five Table I filter totals (50 duplicates, 34 equivalent, 25 undetermined, 48 not activated, 16 miscellaneous) are directly visible in Table I in the extracted text. Their status is now **verified**, not merely arithmetically consistent.
- The first-non-empty ACC result rule is explicitly present in Section IV-B. It is retained in the revised analysis.
- The paper explicitly says the ACC may be called up to three times; if all attempts are empty, the Generator still runs without an anomaly report. If it produces no assertion, the mutant is not detected.
- The baseline removes the signal digest, anomaly report and RTL excerpt; the Generator is given only the specification and RTL declarations. The baseline runs once per design, with assertions checked against each mutant for that design.
- The paper explicitly describes false positives and “other” assertions, so those categories are corrected with their precise meanings.
- The extracted paper text confirms 41/68 is presented as a lower bound because some of the remaining 27 candidates may not violate a stated requirement.

## 3. Findings not treated as novelty

OpenVEF must not present any of the following as a new idea on the basis of this paper:

- stimulus-versus-checker or activation-versus-detection decomposition;
- mutation-based testbench qualification;
- trace-based analysis of faults that pass an existing regression;
- reference-side qualification of a generated checker/assertion;
- LLM generation of hardware stimulus, assertions or testbench code.

The candidate contribution retained for further investigation is the conjunction of:

- LLM-authored driver-and-checker pairs as the study population;
- a controlled direct-versus-structured prompt factor with matched design information;
- repeated independent samples and per-artifact miss composition;
- an explicit pre-frozen specification-derived observation mask.

This is not yet a novelty finding. Step 2 must compare it against functional-qualification, Certitude and LLM-based hardware-verification literature.

## 4. Source-inspection disclosure

Claude was unable to access the original arXiv PDF directly and used search-indexed extracts. In this review, the complete extracted paper text was available from a PDF mirror. PDF page-image screenshot retrieval also failed. The revised analysis therefore claims full extracted-text review, not visual inspection of all seven PDF pages. Page-specific visual verification remains open if required.

## 5. Files updated

- `04_Verify_the_Verifier_Paper_Analysis_v0.2.md` — corrected paper analysis.
- This file — audit findings and resolution log.

The prior `04_Verify_the_Verifier_Paper_Analysis.md` is retained as the earlier revision for audit history. It should not be used as the current analysis.
