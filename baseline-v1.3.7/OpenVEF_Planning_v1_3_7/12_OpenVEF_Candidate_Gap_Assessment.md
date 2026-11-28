# OpenVEF Candidate Research Gap Assessment v1.2

**Status:** DESIGN DRAFT — seven methodological design decisions approved; v1.1 audit returned FAIL for the LLM-call gate; v1.2 correction draft pending independent re-audit; A1–A11 owner acceptance not recorded  
**Date:** 22 November 2026  
**Evidence basis:** Step 1, Step 2 and Step 3 source reviews; Claude's independent Step 3 audit; Claude's v0.6 Charter/Protocol audit; owner-approved v0.7 decisions

## 1. Executive judgement

The broad OpenVEF concept is not novel. Prior work already covers LLM-generated hardware drivers and checkers, mutation-based evaluation, checker-gap detection, stimulus/checker decomposition, prompt-arm comparisons, MCY-Yosys mutation, driver substitution and end-to-end verification-agent evaluation. The reviewed literature does not justify a “first” or new-theory claim.

The remaining candidate contribution is a tightly specified empirical configuration: failure-preserving validity over all scheduled generation calls; checker-independent output exposure at a frozen, specification-derived mask; separate own-driver and own-checker conditional diagnostics; a common-trace checker panel; and a narrowly controlled whole-block prompt-presentation-order comparison. The exact combination was **not found in the sources reviewed as of 22 November 2026**. This is not proof of absence: the search remains targeted rather than systematic, confidence is low-to-moderate, and native IEEE Xplore/ACM DL access remains incomplete.

A credible TEEP/student research study remains possible. Publication strength depends on independent audit, original cycle-exact specifications, instrument validation, sufficient artifact validity, a defensible frozen mutant population, and informative empirical results—including negative results. The current evidence does not guarantee novelty or publication.

## 2. What OpenVEF must not claim as novel

- LLM generation of hybrid hardware driver/checker testbenches.
- Mutation-based evaluation of generated verification artifacts.
- Finding missing checker behavior from golden/mutant divergence while a test passes.
- Activation/propagation/detection, functional qualification or stimulus/checker decomposition.
- Prompt-arm experiments for generated verification plans or testbenches.
- Yosys/MCY mutation or driver/stimulus substitution.
- Checker-gap analysis or common-trace evaluation as general concepts.
- FIFO/UART as benchmark families.
- `PND/(NP+PND)` or own-driver `S_i` as standalone checker quality.

Use “not found in the sources reviewed” and document the search limits. Do not use “first”, “no prior work exists” or broad design-bug-detection claims.

## 3. Current research question

> For a declared set of cycle-exact sequential RTL designs and a pre-registered population of post-synthesis structural netlist signal mutants, how do two prompt-presentation orders carrying identical semantic information affect (a) artifact validity per scheduled generation call, (b) joint masked exposure per scheduled call × primary mutant, and (c) joint own-checker detection per scheduled call × primary mutant? Conditional own-driver exposure, conditional own-checker detection and miss composition are reported as labelled diagnostics; a common-trace checker panel is a standardized secondary analysis.

This wording distinguishes the conditional artifact diagnostics from the three intention-to-treat confirmatory outcomes. H1 reports validity estimates only; H2 contains exactly three two-sided outcomes (validity, joint exposure and joint detection), with Holm correction across those three. One design-stratified contrast is planned per endpoint; exact design set and weights remain TO FREEZE.

The prompt factor is ORG-A versus ORG-B: the same semantic content blocks, identical task instruction, headings, system message, repair message, feedback policy and response schema, with only the order of whole information blocks changing. The treatment is presentation order, not a prompt-organisation or content/attention-scaffolding comparison. Order may affect attention; that mechanism is part of the treatment.

## 4. Metric interpretation

For each valid artifact `i`, `T_i` contains all complete-trace valid artifact–mutant pairs, regardless of checker verdict. It includes normal outcomes, both anomaly classes and both checker-error classes; it excludes invalid pairs, invalid artifact slots and truncated driver/simulator-error or timeout pairs.

- `X_i = DET_i + PND_i + CHECKER_ERROR_AFTER_MASKED_DIVERGENCE_i` is the number of complete-trace pairs with known masked exposure.
- `E_i = X_i/|T_i|` is checker-independent own-driver masked exposure. A checker crash after a masked divergence stays in the numerator because exposure is known from the paired trace.
- `S_i = DET_i/X_i` is own-checker detection among all known exposed complete-trace pairs. A checker crash after exposure is a non-detection. This remains conditional on that driver's exposure set; it is not standardized checker quality.
- `M_i = PND_i/(NP_i+PND_i)` is descriptive miss composition only. It is not a causal decomposition or an independent checker-quality estimate.

The primary intention-to-treat outcomes retain every scheduled generation slot × primary-mutant combination in their denominators:

- `J_exposure` counts complete-trace valid masked exposures, including checker errors after exposure; it is checker-dependent through the artifact-validity gate.
- `J_detection` counts normal `DETECTED` outcomes only.
- Invalid artifacts/pairs and checker errors contribute zero ITT successes. Truncated runs that recorded exposure before termination are reported only in a separate one-sided sensitivity analysis.

The common-trace panel provides secondary standardized sensitivity on a frozen, common exposure set, with explicit checker compatibility, false-alarm and error handling. It is conditional on that corpus and mutant population; it does not establish universal checker quality.

## 5. Candidate distinguishing configuration

The candidate configuration combines:

1. LLM-generated deterministic cycle-synchronous stimulus drivers and separate offline trace checkers as the sampled artifact pair.
2. Intention-to-treat artifact validity over every scheduled generation slot, including malformed, missing and invalid artifacts.
3. Paired null/mutant reactive runs with passive top-level trace capture and explicit paired-input validity rules.
4. A checker-independent, specification-derived output observation mask held by the evaluator. Every scored mask entry must map to a clause in the author-visible specification; the mask file and executable reference model/API are not supplied to authors.
5. A declared Yosys/MCY post-synthesis structural netlist signal-mutant population, with scope claims restricted to the exact pinned mutation modes and eligible set.
6. Conditional own-driver exposure and own-checker detection metrics with explicit complete-trace denominators and checker-crash treatment.
7. A secondary common-trace checker panel with legal multi-trace benign baselines, shared exposed cases, known-answer controls and mutant-result blinding.
8. ORG-A/ORG-B whole-block presentation-order comparison with matched semantic content and frozen common system/repair messages.
9. An open, reproducible implementation and archived experiment ledger.

Each element has precedent or a close analogue. The project is an empirical combination and operational study, not a new mutation engine, formal method, functional-qualification theory or checker-gap concept.

## 6. Closest prior-art boundaries

- **TechRxiv LLM-Aided Verification Gap Detection:** closest checker-gap predicate. It studies golden/mutant output divergence while existing tests still pass and proposes missing-checker detection. It is an unreviewed preprint; the independent Step 3 audit had abstract-only access, so detailed method/injection claims remain unverified and original-PDF retrieval/page inspection/hash are pending.
- **SecTB-RTL:** closest repeated prompt-arm and instrument-validation precedent for generated verification plans with hidden-mutant evaluation. The corrected funnel is 1,860 scheduled calls, 1,857 provider-accepted responses and nine production-semantic-valid outputs; no prompt-effect estimate was produced from that run.
- **DVBench:** end-to-end agent-generated UVM environments with golden acceptance, mutants, coverage and an independent reference model. It includes a FIFO example.
- **AutoBench / CorrectBench / ConfiBench:** hybrid testbench generation, validation, repair and scenario evaluation already exist.
- **CovR:** MCY-Yosys mutation and driver/stimulus substitution are prior art. Preserve the authors' term “RTL mutants”; state separately that MCY operates post-synthesis.
- **GateTruth / From FIPS to FPGA / GRPO-SMu / AssertLLM2 / PRO-V:** mutation-based testbench or assertion evaluation is already established in adjacent hardware-verification literature.
- **Verify the Verifier:** specification-grounded analysis of passing human UVM regressions with staged attribution and formal qualification; it is relevant prior art for trace-based verification gap analysis.
- **Functional qualification and mutation-analysis literature:** activation, propagation, detection and checker completeness are prior concepts; OpenVEF must not claim them as new.

See `10_LLM_Era_Hardware_Verification_Literature_Review.md`, `11_Comparative_Research_Matrix.md`, `17_Step3_Literature_Audit_Addendum_v0.7.md` and `22_Source_Access_Provenance_Log_v1.2.md`. The first two are retained as source-review/evidence records; the v0.7 addendum and this assessment state the current adjudicated position.

## 7. Benchmark overlap and contamination risks

FIFO and UART are common benchmark families. GateTruth includes FIFO/UART tasks and DVBench includes a FIFO example. A prior note mentions a FIFO in the TechRxiv checker-gap preprint, but this was not verified from the abstract-only access record and is not relied upon as an established overlap. Reusing a design family is not itself disqualifying, but OpenVEF must author its own cycle-exact RTL/specification parameters, masks, trace corpus and mutant population, or explicitly obtain permission and attribute reused artifacts. The exact distinguishing behaviors must be selected and documented rather than presumed novel.

Public RTL and testbench patterns may have entered model training or retrieval corpora. This risk cannot be eliminated by prompt wording. Record the exact model/version and generation date, avoid public benchmark identifiers in prompts, and disclose residual family-level contamination risk. Do not claim the model was blind to FIFO/UART as design families.

## 8. What would support a defensible contribution

- A complete, independently reviewed v1.0 prompt/schema/repair/assembly audit with no unresolved blockers to the proposed instrument.
- Original, unambiguous cycle-exact specifications and a signed mask-to-clause traceability table.
- Successful F1–F18 instrument controls, including metric identity tests, known-answer panel controls and an mutant-blind two-arm validity pilot.
- A frozen source-level provenance record, toolchain, MCY mutation mode/population, seeds, prompts, authoring/evaluator separation and statistical code.
- Adequate validity and pre-study precision/power for the declared outcomes; the F16 mutant-blind pilot may estimate validity only, not exposure/detection.
- An honest report of arm effects, confidence intervals, failures, missingness, design overlap and limits. A null or negative result is still reportable if the instrument and design are sound.
- A broader and better documented literature search, including accessible IEEE/ACM proceedings and forward citations, before making any external novelty statement.

## 9. Remaining TO FREEZE values

- Exact FIFO/UART specifications, legal-input semantics and port manifests; v1.0 proposes FSM excluded from the confirmatory set, pending owner decision before F16.
- Mask entries, don't-care windows, clause mapping and independent sign-off.
- Exact mutant candidate set, MCY/Yosys versions, mutation modes, equivalence bound and exclusion rules.
- Confirmatory design set and design-stratum weights for the single H2 test per endpoint; equal weights are proposed.
- `n_pilot`, per-arm `V_min`, confirmatory sample size and precision/power grid.
- Panel random seeds, directed scenarios, `k_null`, benign trace count, exposure set and hashes.
- Provider/model, tokenizer/version, API message roles, decoding settings, token limits and final assembled prompt hashes.
- Repair trigger, repair budget, human time box and permitted feedback content.
- Cycle cap, safe-idle vectors, watchdog formula, BMC/solver limits and strict-mask sensitivity variant.
- Statistical test/interval code, bootstrap count/seeds, randomization schedule and immutable release tag.
- Owner's full legal name and authorship/contribution roles for faculty/public release.
- Original source-PDF binaries and SHA-256 values for sources whose full-text claims will be cited externally.

## 10. Current status and scope gate

OpenVEF remains a design-stage research proposal, not an authorized implementation. The seven v0.7 methodological directions are owner-approved. The v0.7 independent audit returned `PASS WITH CORRECTIONS`; the v0.8, v0.9, v1.0 and v1.1 independent audits returned `FAIL` for the LLM-call gate. This v1.2 draft proposes responses to the v1.1 audit blockers N1–N5; it has not yet received an independent re-audit. A1–A11 remain unaccepted and X14 (strict-AST branch) remains an explicit owner choice. Nothing is authorized until A1–A11 acceptance and X14 choice are recorded. After both, only hand-built FIFO feasibility (specification/mask first, then harness/F1–F15, hand-written parser/assembler fixture tests, and F17 using hand-built FIFO control mutants only) may begin. No LLM call, including F16, is permitted until N1–N5 and the complete mandatory fixture set pass independent re-audit, and A1–A11 plus X14 are accepted in the owner record. Confirmatory generation remains prohibited until every canonical freeze item is complete. No F1–F18 result is claimed.
