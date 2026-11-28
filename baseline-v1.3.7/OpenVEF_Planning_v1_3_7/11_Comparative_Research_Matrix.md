# OpenVEF LLM-Era Hardware Verification — Comparative Research Matrix (v0.6 evidence snapshot)

> **Current interpretation:** This is a compact evidence matrix retained from the v0.6 review. The v0.7 adjudicated gap and prompt-factor interpretation are in `12_OpenVEF_Candidate_Gap_Assessment.md` and `17_Step3_Literature_Audit_Addendum_v0.7.md`.

**Status:** Source-comparison record; source-access levels vary  
**Date:** 22 November 2026  
**Interpretation:** This is a targeted literature matrix, not a systematic review. “Not found” is limited to the sources/searches recorded in the package.

| Work | Artifact/population | Evaluation/oracle | Prompt/treatment | Key overlap with OpenVEF | Main difference / caveat |
|---|---|---|---|---|---|
| **LLM-Aided Verification Gap Detection** (Vagala, TechRxiv, Feb 2026) | Existing human UVM testbenches on golden and mutated RTL; LLM proposes missing checker | Abstract supports output divergence while tests still pass, motivating missing-checker analysis | LLM proposes checker improvements (details beyond the abstract are not relied upon here) | Core “output changed but test passes” checker-gap predicate is prior art | Unreviewed preprint. The independent Step 3 audit had abstract-only access; population, FIFO use, checker observability and mutation-injection details remain unverified until the exact PDF is retrieved. |
| **SecTB-RTL** (arXiv:2609.19844, 2026) | Generated constrained JSON/DSL stimulus-plus-check plans; 31 tasks, 124 authored security regressions | Golden validation, hidden mutants, coverage, reference-model accuracy; failure-preserving funnel | Four content/attention arms, randomized complete blocks, repeated calls; 1,860 calls in follow-up, 9 production-semantic valid | Closest study design: generated verification artifacts, prompt arms, golden gate, mutants, repeated samples and task-cluster statistics | It is a trusted-rendered DSL plan, not free-form cocotb driver + offline checker. Prompt arms vary content/attention, not organization only. The treatment run yielded no prompt-effect estimate due to 9/1,860 semantic-valid artifacts. |
| **DVBench** (arXiv:2611.25066, Nov 2026) | Agent-generated full UVM environments; 95 tasks; 13 agent–model configurations | Compile, golden acceptance, 10 mutants, four coverage measures ≥90%, independent reference-model correctness | Agent/model configuration comparison; not a matched-information prompt-organization experiment | Strong whole-verification-agent benchmark; complete testbench and reference model; synchronous FIFO worked example | Task-level overall success, not OpenVEF's per-artifact mask-based exposure/miss composition. Uses UVM and its own task/mutant construction. |
| **AutoBench** (MLCAD 2024) | LLM-generated Verilog driver + Python checker in staged workflow | Golden RTL acceptance; Eval2 compares candidate testbench verdict with golden testbench verdict on generated RTL mutants | Staged generation vs direct generation | Direct precedent for hybrid driver/checker artifacts and mutant evaluation | Golden testbench is the comparison oracle; not an independent spec-derived observation mask or `NP/PND` decomposition. |
| **CorrectBench** (DATE 2025) | Hybrid generated testbench with self-validation and correction | Scenario/RTL consistency and Eval-based pass ratio | Corrector/agent workflow compared with earlier/direct generation | Generation, self-validation and direct baseline precedent | Focuses on repair/validation; no identical per-artifact miss-composition estimand. |
| **ConfiBench** (ACM TODAES, 2026) | Hybrid testbench, scenario masking, testbench ensemble | Eval2 pass ratio against its evaluation framework | Confidence-based scenario mask and ensembles | LLM testbench validity, scenario filtering and ensemble precedent | Its scenario mask filters generated scenarios; it is not OpenVEF's checker-independent output-observation mask. |
| **CovR** (MLCAD 2026; arXiv:2609.19189) | Stimulus-only model; replaces CorrectBench driver track and feeds downstream checker | Coverage and mutation evaluation; MCY-Yosys, 10 mutants per design | Training/refinement and driver substitution | MCY-Yosys mutants and component substitution are already used; important stimulus/oracle interaction evidence | It studies stimulus generation, not LLM-authored checker quality or matched-information prompt-organization effects. |
| **PRO-V / PRO-V-R1** (arXiv:2506.12200, version-dependent naming) | Multi-agent verification/testbench generation | Golden pass, mutant detection and automated testbench-vs-DUT error triage | Agent/model/refinement configurations | Mutation-based testbench scoring and agentic error triage are prior art | Must cite exact version; v1 PRO-V differs from later PRO-V-R1/RL versions. |
| **GRPO-SMu** (arXiv:2601.07593; IEEE record) | Trained model generates test plans and testbenches; 500 designs × 3 mutants | Golden pass and mutation detection | SFT/RL and mutation-aware training setup | Golden validity and mutant detection are established metrics | Training-focused; model generation setup is mutation-aware; do not overstate precisely what buggy RTL is visible at every stage. |
| **AssertLLM2** (arXiv:2605.27472) | SVA/assertion sets only; 83 designs, 13 categories | Formal proof/violation and mutation-based bug detection; mutant non-equivalence checked | Bug-prevention vs bug-hunting task settings | Generated checker/assertion evaluation on mutated RTL | No generated stimulus driver; checker-only population. |
| **GateTruth** (arXiv:2608.12635) | Existing benchmark testbenches; 46 designs and 775 semantic mutants in reported audit | Behavioral simulation failure / mutation kill | Benchmark audit; no prompt arms | Seeded mutation audit; FIFO and UART examples; reveals benchmark/testbench weaknesses | Not a study of newly generated artifact cohorts. Per-design mutant counts vary widely, so denominators matter. |
| **From FIPS to FPGA with LLM Agents** (arXiv:2611.25339) | LLM-agent-built gates/tests for PQC hardware workflow | Netlist-mutant gate audit and functional outcomes | Agentic workflow replay, not randomized prompt arms | Recent netlist-mutant evaluation precedent | Workflow case study, not an independently sampled artifact cohort; timeout classification needs source confirmation before citing. |
| **Verify the Verifier** (arXiv:2611.26588, Nov 2026) | Existing human-authored UVM regressions on OpenTitan IPs; LLM audits traces and proposes SVA | Qualified assertion: mutant cex, reference proof, antecedent non-vacuity | No matched prompt-format experiment | Miss decomposition, trace-based analysis, staged detection | Human UVM tests are the object; LLM checker is a remedy/auditor. |
| **LLM4DV / HAVEN / UVM² / UVMarvel / DeepAssert / data-integrity work** | Stimulus generation, DSL/UVM generation, coverage closure or internal assertion generation | Varies: coverage, build, assertion and reference checks | Varies | Adjacent evidence for structured plans, coverage and checking components | Not all were fully re-audited in this pass; use source-access log and avoid treating summaries as full-text review. |

## What the matrix establishes

1. Hybrid driver/checker generation and mutant-based scoring are established.
2. Prompt-arm experiments for generated verification artifacts are established, though SecTB-RTL did not produce a valid treatment estimate in its reported follow-up.
3. Checker-gap discovery from golden/mutant divergence with passing tests is prior art.
4. MCY-Yosys mutation and driver substitution are prior art through CovR.
5. End-to-end UVM verification agents with golden/mutant/coverage/reference checks are prior art through DVBench.
6. The remaining candidate distinction is the precise combined measurement: all-scheduled-slot validity funnel; an evaluator-held checker-independent specification mask; per-artifact own-driver exposure and own-checker outcomes; and a common-trace checker panel under a narrowly controlled prompt-organization factor. This is still only a candidate gap.

## Source access / confidence

- TechRxiv checker-gap paper: abstract-only access is recorded (File 22); full-text and injection-method claims are not verified.
- SecTB-RTL: audit relied on arXiv/search-indexed and author-hosted passages; full text not independently re-extracted in this resolution.
- DVBench: full extracted text read; PDF page-image screenshots unavailable.
- CovR: full extracted paper text and selected page images inspected.
- Other studies: access ranges from abstracts/excerpts to extracted text; see the paper-by-paper literature review and Claude audit for source-specific access notes.

No exact-combination novelty claim is established. Use “not found in the sources reviewed as of 22 November 2026,” and re-run forward citations/native database searches before any submission.

---

**v1.3.7 CANDIDATE, not audited.** This file is OpenVEF Planning v1.3.6 with only the corrections listed for it in `CHANGELOG-v1.3.7-candidate.md` (owner decision D-024). It is not part of any released, audited or approved pack; v1.3.6 remains the default.
