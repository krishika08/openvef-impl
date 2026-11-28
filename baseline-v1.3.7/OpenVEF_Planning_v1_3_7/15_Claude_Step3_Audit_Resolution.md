> **Historical Step 3 audit record:** this file is retained as the audit resolution that led to v0.6. Its prompt-factor language, any TechRxiv full-text/method wording, and any SecTB-RTL shorthand are superseded by the v0.7 correction/addendum, canonical v0.7 Protocol and `22_Source_Access_Provenance_Log.md`. Where source-access statements differ, the provenance log controls.

# OpenVEF Step 3 Claude Audit Resolution (v0.6)

**Date:** 22 November 2026  
**Source:** Claude Pro audit, supplied by project owner (`14_Claude_Step3_Audit_Raw.txt`, retained in this package)  
**Resolution status:** Findings adjudicated; v0.6 revisions drafted, owner approval pending  
**Project status:** CONDITIONAL GO; no implementation or confirmatory experiment has begun

## 1. Executive decision

Claude's central critique is accepted. The v0.5 primary metric `PND/(NP+PND)` is a **miss-composition statistic for a coupled driver/checker artifact**, not a checker-quality score. Because the driver determines which faults become observable, the ratio blends exposure and conditional checker detection. In addition, v0.5 conditions the headline comparison on artifact validity, which is itself affected by prompt assignment. A valid comparison must retain every scheduled generation slot in the validity and joint pipeline denominators.

The Step 3 review remains **CONDITIONAL GO**. The general concepts are prior art. The exact OpenVEF combination was not found in the reviewed sources, but this is low-to-moderate confidence and not a novelty finding. The revised candidate contribution is a controlled measurement configuration, not a new method.

## 2. Claude findings accepted

1. **TechRxiv checker-gap prior art.** The core predicate—outputs differ between golden and faulty RTL while existing tests continue to pass, indicating missing checks—is prior art. The preprint is unreviewed. Its abstract says automated fault injection, while its detailed text also describes manual injection; the injection mechanism is internally ambiguous and must not be stated as settled. Its reported observability rule is checker-dependent, unlike OpenVEF's planned evaluator-held specification mask.
2. **SecTB-RTL is the closest study-design precedent.** It uses generated verification plans, golden and hidden-mutant execution, multiple prompt arms, repetitions, randomized blocks and task-clustered inference. Its treatment run did not produce a prompt-effect estimate because only 9 of 1,860 scheduled calls passed production semantic validation (1,857 of the calls were provider-accepted). It is a calibration/validity warning, not evidence for an arm effect.
3. **DVBench was omitted in the first Step 3 review.** It evaluates agent-generated end-to-end UVM environments on golden acceptance, mutants, coverage and independent reference-model correctness across 95 tasks and 13 configurations; FIFO is a worked example. It occupies much of the whole-verification-agent benchmark space.
4. **CovR establishes MCY-Yosys and component substitution precedent.** It uses MCY-Yosys mutants and replaces the driver/stimulus track in CorrectBench while retaining downstream checking. OpenVEF must not claim either MCY use or component substitution as novel.
5. **Own-driver `E_i` and own-checker `S_i` are conditional diagnostics.** `E_i=(PND_i+DET_i)/C_i`; `S_i=DET_i/(DET_i+PND_i)`. `S_i` depends on the particular driver's exposure set and is not a standardized checker-quality comparison.
6. **The miss share is algebraically a blend.** For a complete conclusive partition, `M_i=PND_i/(NP_i+PND_i)=E_i(1-S_i)/(1-E_iS_i)`. Different driver/checker combinations can yield the same `M_i`.
7. **Validity is post-treatment.** Prompt assignment can change artifact validity. Valid-only comparisons must be labelled conditional; intention-to-treat validity and joint funnel outcomes must use all scheduled calls.
8. **Mask should be evaluator-only.** Providing the observation mask to generation authors may tell the checker exactly what to check and suppress the measured gap. Proposed v0.6 withholds the mask while providing the specification and trace contract.
9. **Prompt factor must be genuinely narrow.** Proposed treatment is ordering, headings and formatting only. If task instructions/attention guidance differ, the factor is prompt scaffolding, not pure formatting.
10. **A shared-trace checker panel is recommended.** A common, frozen trace corpus allows compatible checkers to be evaluated on a standardized exposure population. The checker must derive expected behavior from trace inputs/history, not hard-coded stimulus-specific values.
11. **FIFO/UART are not novel benchmark families.** Retain them only as practical strata, author distinctive original cycle-exact specs, disclose overlap, and avoid broad generalization.
12. **F16 must be expanded.** Pilot both prompt arms, report per-arm validity, retain all failures, keep pilot blind to mutant outcomes, set a stop rule, re-pilot after contract changes, and check common-panel compatibility if adopted.

## 3. Independent source checks performed in this resolution

The audit's key claims were cross-checked against available extracted primary-source text:

- The TechRxiv paper's abstract and body support the missing-checker predicate and its checker-dependent observation definition. Its automated-versus-manual fault injection descriptions are not fully consistent, so that uncertainty is retained.
- DVBench's extracted full text supports its 95-task benchmark, multiple agent/model configurations, golden/mutant/coverage/reference-model evaluations, and synchronous FIFO worked example.
- CovR's full paper section 4.4 explicitly describes replacing CorrectBench's driver/stimulus track with CovR stimulus and using MCY-Yosys mutants.
- SecTB-RTL claims are based on author-hosted/search-indexed passages and the original audit's source log; full text was not independently extracted in this resolution. Its reported 1,860/1,857/9 funnel is treated as audit-verified, but a future submission should cite the source and archive the exact version.

Some PDFs could be read as extracted text but not visually inspected page-by-page because screenshot/page-image rendering failed. This is stated rather than concealed.

## 4. Recommended methodological decisions drafted into v0.6

| Decision | Proposed resolution | Status |
|---|---|---|
| Research question | Validity, own-driver exposure, own-checker detection and pipeline outcomes; miss composition descriptive | Drafted; owner approval pending |
| Primary validity denominator | All scheduled generation slots, with repairs nested in the slot | Drafted; owner approval pending |
| Prompt factor | Prompt organization/formatting only; byte-identical semantic content and instructions | Drafted; owner approval pending |
| Observation mask | Withheld from generation; evaluator-only and independently reviewed | Drafted; owner approval pending |
| Common-trace checker panel | Adopt as pre-registered secondary analysis | Drafted; owner approval pending |
| Checker API | Expected values derived from trace inputs/history; no artifact-specific literal sequence | Drafted; owner approval pending |
| Miss share | Descriptive only; remove `delta_checker` significance threshold | Drafted; owner approval pending |
| Co-primary prompt outcomes | ITT validity, joint exposure and joint detection | Drafted; owner approval pending |
| Designs | FIFO/UART retained as strata with distinctive specs and explicit overlap disclosure | Drafted; exact specs not frozen |
| Sample size | Precision/power simulation before confirmatory calls; ≥10 only a feasibility floor | Drafted; sample size TO FREEZE |
| F16 | Two-arm, production-path, no-mutant-feedback pilot with per-arm validity and stop rule | Drafted; thresholds TO FREEZE |

## 5. Revised candidate research question

> For a declared set of cycle-exact sequential RTL designs and a pre-registered population of post-synthesis structural netlist signal mutants, how do two prompt-organization formats carrying identical semantic information affect (a) validity of generated LLM driver/offline-checker artifacts, (b) driver exposure of mutants at outputs selected by an evaluator-held, pre-frozen specification mask, and (c) detection of exposed behaviour by each artifact's own checker? The composition of missed pairs is reported descriptively, with a shared-trace checker panel used as a secondary standardized-checker analysis.

This question is more defensible than the v0.5 wording, but remains a candidate until the owner approves it and the broader database search is completed.

## 6. Exact metric interpretation

Let `C_i=NP_i+PND_i+DET_i` be conclusive normal outcomes for valid artifact `i`.

- `E_i=(PND_i+DET_i)/C_i` is own-driver masked exposure among conclusive pairs.
- `S_i=DET_i/(DET_i+PND_i)` is own-checker detection conditional on own-driver exposure.
- `M_i=PND_i/(NP_i+PND_i)` is miss composition, not checker quality.
- `M_i=E_i(1-S_i)/(1-E_iS_i)` when the conclusive partition is complete.

The common-trace panel separately estimates checker response on a shared trace population, conditional on checker compatibility. It is not a replacement for the own-artifact evaluation; it is a standardized secondary measurement.

## 7. Remaining source and research limitations

- Native IEEE Xplore/ACM DL and conference-proceeding searches have not been systematic.
- The TechRxiv preprint should be manually downloaded and read by page before any paper submission; automated/manual injection wording must be reconciled.
- DVBench and CovR should be fully checked against current canonical versions before formal citation.
- SecTB-RTL author names/version metadata should be taken from the arXiv author line and citation record, not copied from secondary webpages.
- Re-run forward-citation searches immediately before proposal/submission; the field is moving quickly.
- No claim that the reviewed combination is new is authorized. Use “not found in the sources reviewed as of [date]”.

## 8. Release and implementation status

The v0.6 Charter and Experimental Protocol are proposed revisions only. They do not authorize confirmatory generation or code implementation. No F1–F18 control has been run, the common-trace panel is not implemented, the prompts are not frozen, and the sample size is not powered. Next step is owner review of the proposed design decisions, then Step 4 research-gap finalization and the documented database search.
