# OpenVEF Step 2 — Claude Audit Resolution

**Date:** 22 November 2026  
**Audited item:** `06_Functional_Qualification_and_Mutation_Analysis.md`  
**Raw audit:** `08_Claude_Step2_Audit_Raw.txt`  
**Claude verdict:** PASS WITH CORRECTIONS  
**OpenVEF status:** CONDITIONAL GO; no implementation started.

## 1. Resolution summary

Claude's audit was accepted as a useful independent challenge. The central conclusion stands: activation/propagation/detection, mutation analysis, and stimulus/checker qualification are established prior art. OpenVEF must not present that decomposition, a checker-side exposed-mutant ratio, or mutation testing itself as a new method.

The Step 2 note and the Charter/Protocol v0.5 were updated to address the audit. The wider LLM-era novelty question remains open for Step 3.

## 2. Claude findings and decisions

| Finding | Resolution |
|---|---|
| IEEE Transactions on Computers (2014) was grouped too closely with functional qualification even though its kill rule is output-trace difference. | **Accepted.** Reclassified as mutation-based testbench assessment/mutant-model engineering. Its kill criterion does not require a testcase/checker failure. The paper extends the earlier DATE 2008 and MTV 2009 TLM mutation work, not the DATE 2009 functional-qualification paper. |
| Public sources use different propagation boundaries (output/probe versus reaching a checker). | **Accepted.** OpenVEF now defines propagation independently of its checker: top-level output divergence on a frozen specification mask. Legacy categories are not mapped mechanically. |
| The old NP mapping omitted raw divergence outside the specification mask and the fixed cycle window. | **Accepted.** NP is now described as “no masked output divergence observed,” with descriptive raw-divergence subcounts. Internal activation is not claimed. |
| Huang et al. (2015) provides a checker-side exposed-mutant metric precedent. | **Accepted.** The integrity/completeness component in Huang's checker-quality term is acknowledged as an analogue for `checker_gap`; it is not numerically interchangeable because the exposure proxy, population and unit differ. |
| Netlist signal mutants should be distinguished from source-level design-error mutation and manufacturing stuck-at grading. | **Accepted.** OpenVEF's safe label remains “structural netlist signal mutants.” The exact MCY mutation modes must be recorded from the pinned version before using more specific terminology. |
| DATE 2009 has Certess co-authors and is not vendor-independent. | **Accepted.** The revised note identifies Hampton and Letombe as Certess-affiliated co-authors and describes the paper as peer-reviewed but not vendor-independent. |
| Three Huang numerical results were not located in Claude's text access. | **Independently checked and resolved.** The accessible Wiley HTML exposes Table 2's 0.51→0.91 random-stimulus trajectory, Table 3's 0.51→0.92 directed-stimulus trajectory, and Table 4's 0.48→0.91 CPU trajectory. These are reported only as values under Huang's own composite metric. |
| The SecTB-RTL execution incident motivates validation of the artifact-generation instrument. | **Accepted.** Added F16: a non-confirmatory end-to-end LLM artifact-contract pilot. Pilot sample size, acceptance threshold and sample-expansion rule must be fixed before the pilot; failures remain in its scheduled denominator. |
| The exact DVCon practitioner paper “Who's Watching the Watchmen” is an important source for one Certitude taxonomy. | **Partly unresolved.** The exact record was not independently located under that title in this source pass. The note records the boundary variation cautiously and does not add the unverified DVCon bibliographic item as a confirmed reference. |

## 3. Independent source checks

The following cross-checks were made in addition to reading Claude's audit:

- **Huang et al. (2015):** Wiley HTML was checked. It states that a mutant surviving while coverage fluctuates indicates checker insufficiency; Equation (4)'s checker integrity component is killed mutants with fluctuating coverage divided by all mutants with fluctuating coverage. Tables 2–4 expose the stated final values.
- **DATE 2009:** the proceedings text confirms the difference between output-difference mutation kill and testcase-failure functional qualification; the author block identifies two authors with Certess.
- **IEEE TC 2014:** the repository manuscript's Section 3.2 explicitly defines a killed mutant by an observable output difference from the fault-free model. The web PDF text was inspected; screenshot retrieval was blocked, so no visual page-image inspection is claimed.
- **MCY:** official documentation describes mutations as modifications of individual signals in a post-synthesis netlist, followed by formal filtering. This supports the safe structural-netlist label, but does not establish equivalence to a manufacturing stuck-at model.
- **SecTB-RTL:** full arXiv HTML reports 1,860 scheduled calls, 1,857 provider-accepted responses and only nine production-semantic-valid artifacts; the study explicitly reports no prompt-effect estimate from that incident.
- **GRPO-SMu and GateTruth:** full arXiv HTML/abstract and relevant sections were checked. They establish close prior art for LLM-generated verification stimuli/testbenches and mutation-based audit of RTL benchmark testbenches.

## 4. Changes made

1. Revised note 06 to distinguish output-difference mutation analysis from testcase-failure functional qualification.
2. Added the Huang checker-integrity precedent for `checker_gap`, with clear denominator and exposure-proxy caveats.
3. Expanded the propagation-boundary discussion and corrected the NP interpretation.
4. Split source-level RTL design-error mutants, post-synthesis netlist signal mutants and manufacturing stuck-at fault models.
5. Added coverage-discounting and probabilistic error-propagation references.
6. Added GRPO-SMu, SecTB-RTL and GateTruth to the LLM-era Step 3 handoff.
7. Added F16 artifact-contract pilot and updated the protocol freeze gate.
8. Updated the Charter's risk section and made its gate reference consistent with F1–F16.
9. Corrected the accessible-source bibliography for Mark Hampton's brief and the Certitude launch report.

## 5. Remaining limits and next work

- The precise MCY mutation modes must be checked on the pinned software version, against exported netlists.
- The exact DVCon “Who's Watching the Watchmen” reference remains unverified.
- Native IEEE Xplore and ACM DL searches have not been exhaustive; no systematic-review claim is made.
- Step 3 must compare SecTB-RTL, GRPO-SMu, GateTruth, AutoBench, CorrectBench, ConfiBench and other LLM-hardware-verification work at the level of study population, experimental factor, artifact type, mutant source, denominator and metric.
- The potential distinctiveness of OpenVEF's exact combination is still provisional.

**Resolution:** Claude's main criticisms were accepted. One numerical-access concern regarding Huang was resolved by direct table verification. The Step 2 foundation note is revised, but the broader related-work review is not complete.
