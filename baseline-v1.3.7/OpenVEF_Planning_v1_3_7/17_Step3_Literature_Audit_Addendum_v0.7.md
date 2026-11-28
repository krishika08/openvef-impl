# Step 3 Literature Review — Audit Addendum v0.7

This addendum supersedes the v0.6 addendum where corrected by the Claude v0.6 audit and current source checks. It is a targeted, not systematic, review.

## Closest-overlap ranking

1. **SecTB-RTL** (arXiv:2609.19844): closest repeated prompt-arm/instrument-validation precedent for generated verification plans and hidden-mutant evaluation. Correct run funnel: **1,860 scheduled calls; 1,857 provider-accepted responses; 9 production-semantic-valid outputs**. The nine are not “9 of 1,860 provider-accepted responses.” No prompt-effect estimate was reported from that incident.
2. **LLM-Aided Verification Gap Detection** (Praveen Kumar Vagala, TechRxiv preprint, 10 February 2026; DOI 10.36227/techrxiv.177069683.39144593/v1): closest core checker-gap predicate. The paper reports golden/mutant output divergence with tests still passing and proposes missing-checker detection. It is unreviewed. Earlier draft/secondary notes differ on whether mutation injection was automated or manual; the independent Step 3 audit had abstract-only access, so neither description is verified from the paper text in this pack. Do not state either as settled.
3. **DVBench** (arXiv:2611.25066v1, 18 November 2026): end-to-end UVM verification-agent benchmark with 95 tasks across nine domains; includes generated testbench and intermediate artifact evaluation, and a synchronous FIFO example.
4. **AutoBench / CorrectBench / ConfiBench**: LLM-generated drivers/checkers, golden validation, mutation-related evaluation and iterative refinement.
5. **CovR** (MLCAD 2026; arXiv:2609.19189v2): the authors use the term “RTL mutants” for MCY-Yosys-generated mutants. OpenVEF's note is that MCY operates post-synthesis; do not relabel the authors' phrasing as “netlist mutants” when describing their claim. CovR also establishes driver/stimulus substitution precedent.
6. **PRO-V / GRPO-SMu**: multi-agent and reinforcement-learned testbench/stimulus generation with mutation evaluation.
7. **AssertLLM2 / DeepAssert**: checker/assertion generation evaluated with mutation/formal methods.
8. **GateTruth / From FIPS to FPGA**: semantic and netlist-mutant auditing; disclose FIFO/UART overlap.
9. **Verify the Verifier** (arXiv:2611.26588v1, submitted 19 November 2026): specification-grounded trace analysis of passing UVM regressions, with staged attribution and formal qualification.

## Required claim boundaries

- Do not claim novelty for hybrid driver/checker generation, mutation evaluation, checker-gap detection, activation/propagation/detection decomposition, prompt-arm experiments, MCY use or component substitution.
- Do not describe `PND/(NP+PND)` as checker quality.
- Distinguish output/mask exposure from checker detection; prior work sometimes uses checker-dependent observability.
- Use “not found in sources reviewed as of 22 November 2026,” never “no prior work exists.”
- The prompt factor in OpenVEF is a whole-block presentation-order comparison, not direct-versus-structured prompting and not content/attention scaffolding.

## Source status and unresolved provenance

- SecTB-RTL: arXiv:2609.19844; the current audit records 1,860/1,857/9 as scheduled/provider-accepted/production-semantic-valid. Confirm the exact version/author line and retain a local PDF before external citation.
- TechRxiv: DOI URL is recorded in `22_Source_Access_Provenance_Log.md`. The independent Step 3 audit reports abstract-only access; the original PDF binary, a retrievable mirror/version record and SHA-256 are not retained. Detailed method and injection claims remain unverified until the exact PDF is retrieved and inspected.
- DVBench: arXiv:2611.25066v1, 18 Nov 2026. Current audit opened the arXiv PDF text; page-image inspection and original PDF binary hash are not retained in the local pack.
- CovR: arXiv:2609.19189v2, 19 Sep 2026; MLCAD 2026, DOI 10.1145/3831599.3840347. Prior review reports full text and selected page images inspected; original PDF binary hash is not retained.
- Verify the Verifier: arXiv:2611.26588v1, 19 Nov 2026. Current audit opened the arXiv PDF text; page-image inspection remains pending and source binary hash is not retained.

See the provenance log for URLs, versions, access status and locally retained review-document digests. Do not claim source-binary hashes where none were captured.
