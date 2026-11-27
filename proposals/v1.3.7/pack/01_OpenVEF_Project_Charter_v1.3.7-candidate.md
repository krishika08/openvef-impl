# OpenVEF Project Charter v1.3.7-candidate

**Project:** OpenVEF — Open Verification Effectiveness Framework  
**Version:** 1.3.7-candidate (OpenVEF Planning v1.3.6 with the corrections in `CHANGELOG-v1.3.7-candidate.md`; not audited; not frozen; not approved). Based on: 1.3.6 (corrective evidence/metadata release; independent re-audit pending; not frozen)  
**Date:** 23 November 2026  
**Status:** DESIGN DRAFT — OWNER ACCEPTANCE PENDING  
**Project owner:** TO CONFIRM against the actual TEEP application; no legal-name or approver identity is inferred

> **Status note.** The v1.3, v1.3.1, v1.3.2 and v1.3.3 independent document audits returned FAIL for the LLM-call gate. The v1.3.3 audit identified N13: rank 7 missed generator expressions containing `await` when all `is_async` flags were zero. The v1.3.4 corrective release extended the AST_SIGNATURE rank-7 rule to detect `ast.Await` anywhere in a comprehension subtree, defined symbols by AST ancestry, documented compile-stage handling for asynchronous constructs, restored M63 indentation and added M70. The v1.3.4 independent document audit returned FAIL on N14 (stale F18 checklist). The owner-supplied v1.3.5 audit result reports DOCUMENT AUDIT PASS (documents only), with all 144 fixtures still NOT RUN / NOT PASSED. This v1.3.6 corrective evidence/metadata release closes the v1.3.5 cleanup items and includes the exact v1.3.2 audit export, verified against its recorded size and SHA-256; independent v1.3.6 document re-audit is pending. The v1.3.7-candidate pack is not audited. A1–A11 remain PROPOSED / NOT ACCEPTED and X14 remains OWNER CHOICE REQUIRED. Owner/applicant/contributor/approver identities remain TO CONFIRM; signature/date remain NOT RECORDED. Nothing is authorized until the owner records A1–A11 acceptance and an explicit X14 choice; even then, only the limited hand-built FIFO scope may open. No LLM/provider call is authorized until the separate LLM-call gate passes independent re-audit.

## 1. Executive summary

OpenVEF is an open, reproducible empirical study of LLM-generated hardware-verification artifacts for cycle-exact sequential RTL designs. Each artifact is a paired bundle: a deterministic cycle-synchronous stimulus driver and an offline checker that consumes an archived trace.

The study compares two prompt-presentation orders, ORG-A and ORG-B. The exact semantic blocks, task instruction, system prompt, repair prompt, authoring information, feedback policy (triggers, grammar, whitelist and cap), model and settings are held constant; only the order of whole information blocks differs. Hidden block IDs are not model-visible, the task instruction is order-free, and the exact assembly algorithm is specified in a proposed specification and is not frozen until independent F18 sign-off. Evaluator-only mask, reference model/API and mutant data are withheld from artifact authors.

OpenVEF reports three distinct primary pipeline outcomes: artifact validity over all scheduled calls, joint masked exposure per scheduled call × primary mutant, and joint own-checker detection per scheduled call × primary mutant. It separately reports conditional own-driver exposure and own-checker detection, with corrected denominators that include known exposures even when the checker crashes. A common-trace checker panel is a secondary standardized analysis.

OpenVEF does not introduce a new mutation engine, functional-qualification theory, checker-gap concept or activation/propagation/detection theory. Its candidate contribution is a carefully controlled, reproducible measurement configuration. The combination has **not been found in the sources reviewed**, but the literature review remains targeted rather than systematic. No “first” or strong novelty claim is authorized.

## 2. Problem statement

A verification artifact may miss a fault because its stimulus does not produce a specification-observable output effect, or because an observable effect occurs but the artifact's checker accepts it. A simple pass/fail result cannot distinguish these stages.

OpenVEF runs the same deterministic, cycle-synchronous driver independently on a null-mutant reference netlist and each candidate mutant. The harness passively captures top-level inputs and outputs. A frozen observation mask derived from the design specification determines which output differences count as exposure. The artifact's checker is an offline function over the captured trace and cannot alter simulation or stimulus.

The design deliberately distinguishes: (1) artifact validity, (2) conditional own-driver exposure `E_i`, which is checker-independent among valid complete-trace pairs, (3) checker verdict after exposure, and (4) standardized checker response on a common trace corpus. The ITT joint-exposure endpoint `J_exposure` is not pure driver exposure because it also depends on the checker through the artifact-validity gate.

## 3. Research question and hypotheses

**Primary research question.** For a declared set of cycle-exact sequential RTL designs and a pre-registered population of post-synthesis structural netlist signal mutants, how do two prompt-presentation orders carrying identical semantic information affect (a) artifact validity per scheduled generation call, (b) joint masked exposure per scheduled call × primary mutant, and (c) joint own-checker detection per scheduled call × primary mutant? Conditional own-driver exposure, conditional own-checker detection and miss composition are labelled diagnostics; a common-trace checker panel is a secondary standardized analysis.

**H1 — validity reporting (estimation only).** Report intention-to-treat validity rates and confidence intervals by arm/design with the full attrition funnel. The validity comparison is H2(a), not a separate test.

**H2 — three pre-registered two-sided arm contrasts.** H2(a) compares validity; H2(b) compares joint exposure; H2(c) compares joint detection. Use Holm correction over exactly these three outcomes. The prompt factor is exploratory in direction; no directional effect is assumed.

No hypothesis labels `PND/(NP+PND)` as checker quality. That quantity is miss composition and is reported descriptively only.

## 4. Prior art and novelty boundary

The following components are established prior art: mutation analysis; functional qualification; observability-based coverage; activation/propagation/detection distinctions; generated hardware verification artifacts; mutation-based evaluation of LLM-generated testbenches; checker-gap discovery; prompt-arm experiments; MCY-Yosys use; and stimulus/driver substitution.

The prior-art review specifically includes:

- **Functional qualification and mutation analysis:** established methods distinguish fault activation, output propagation and testbench detection; OpenVEF uses a checker-independent specification mask rather than treating the checker verdict itself as the propagation boundary.
- **Huang et al. (2015) and related qualification work:** prior methods jointly discuss stimulus, coverage and checking. OpenVEF's `E_i` and `S_i` are not numerically interchangeable with those metrics.
- **AutoBench / CorrectBench / ConfiBench / PRO-V / GRPO-SMu / AssertLLM2 / GateTruth:** establish related LLM generation, testbench validation, mutation evaluation, checker generation or test-plan workflows.
- **SecTB-RTL (arXiv:2609.19844):** a close repeated prompt-arm and artifact-validation precedent. The corrected run funnel is 1,860 scheduled calls, 1,857 provider-accepted responses and 9 production-semantic-valid outputs. It is an instrument-validation incident; no prompt-effect estimate is reported.
- **TechRxiv, “LLM-Aided Verification Gap Detection” (Vagala, February 2026):** explicitly studies mutation-induced output divergence with tests still passing as a checker gap. It is an unreviewed preprint. The independent Step 3 audit had abstract-only access; prior notes differ on whether mutation injection was automated or manual, so the detailed method remains unverified and no injection-method claim is treated as settled.
- **DVBench (arXiv:2611.25066v1, 18 November 2026):** an end-to-end UVM verification-agent benchmark with 95 tasks and evaluation of generated testbenches and intermediate artifacts. It is close prior art for whole-workflow agent evaluation.
- **CovR (MLCAD 2026; arXiv:2609.19189v2):** reports the authors' phrase “RTL mutants” generated with MCY-Yosys and uses stimulus/driver substitution in a broader verification workflow. MCY operates post-synthesis; OpenVEF must not claim MCY use or driver substitution as novel.
- **Verify the Verifier (arXiv:2611.26588v1, 19 November 2026):** uses specification-grounded analysis of passing UVM traces and staged qualification of findings. Its studied artifacts are existing human-authored UVM regressions, not independently generated driver/offline-checker pairs.

The exact OpenVEF combination—scheduled-call validity, conditional checker-independent exposure, own-checker outcomes with full-failure denominators, and a common-trace checker panel under a block-order-only prompt presentation contrast—has not been found in the sources reviewed as of 22 November 2026. This is a candidate gap, not a proof of novelty. Native IEEE Xplore/ACM DL searches and selected proceedings searches remain incomplete.

## 5. Objectives

1. Define original, cycle-exact design specifications and observation masks before confirmatory generation.
2. Build a deterministic, harness-owned cycle-synchronous driver interface.
3. Export a null-mutant netlist and a fixed candidate population of post-synthesis structural signal mutants.
4. Validate every artifact against RTL-versus-null and null-checker controls.
5. Run paired null/mutant executions and capture traces independently of test code.
6. Apply the same specification-derived observation mask to trace comparison and bounded equivalence.
7. Classify every scheduled slot × mutant combination using a mutually exclusive, predeclared ledger.
8. Compare ORG-A and ORG-B while holding semantic content and all other prompt channels constant.
9. Evaluate generated checkers on a shared legal trace corpus as a secondary analysis.
10. Preserve prompts, model metadata, seeds, traces, tool logs, mutants, masks and analysis scripts for reproduction.

## 6. Scope

### 6.1 Initial feasibility slice

- One synchronous FIFO as the end-to-end feasibility design.
- One null reference and a **hand-built set of distinct control mutants** sufficient to exercise the F1–F15 cases; this is not a one-mutant-only plan.
- Harness-owned cycle scheduler, passive recorder, offline checker, paired trace comparator and classifier.
- Hand-built cases for every normal, anomaly, invalid, timeout and error class.
- ALU may be used as a pipeline smoke test only; it does not validate reactive sequential semantics.

### 6.2 Confirmatory MVP (only after the full freeze gate)

- Proposed main design set: synchronous FIFO and UART transmitter. FSM is excluded from the v0.8 confirmatory estimand unless the owner explicitly adds it before F16; adding it changes the equal-weight design estimand.
- Python orchestration; Verilog/SystemVerilog RTL; Cocotb; Icarus Verilog initially; Yosys/MCY for mutant generation and equivalence support.
- Same prompt model/provider/settings in both arms; sample size determined by pre-study precision/power analysis. Ten calls per arm/design is a feasibility floor only.
- One time-boxed human artifact per design, descriptive only; seeded random/reference stimulus is a baseline and common-trace source only.

### 6.3 Exclusions

New qualification theory or mutation engine; source-level RTL design-error mutants in the MVP; manufacturing stuck-at or silicon fault claims; variable-latency designs; UVM/SVA generation; FPGA implementation, physical design or silicon measurement; materials/process research; image-based defect detection; PPA or commercial chip claims.

## 7. Benchmark design, overlap and contamination

| Design | Role | Required specification |
|---|---|---|
| Synchronous FIFO | Feasibility and main benchmark | Exact reset, enqueue/dequeue, simultaneous operations, full/empty, data-valid, overflow/underflow and timing semantics |
| UART transmitter | Main benchmark | Exact clock/tick, frame format, parity if included, start/stop, reset, busy/ready, break/idle and transmit timing |
| FSM controller | Deferred; excluded from the v0.8 confirmatory set | Adding it requires an owner decision, a revised equal-weight estimand and a new freeze before F16 |
| 8-bit ALU | Smoke test only | Exact opcode, widths, wraparound, flags and invalid-opcode semantics |

FIFO and UART are not novel benchmark families. GateTruth includes FIFO/UART tasks; DVBench includes a FIFO example; and a separate data-integrity work reviewed in Step 3 uses asynchronous FIFO and UART-transmitter examples. The TechRxiv checker-gap preprint was mentioned in an earlier note as containing a FIFO, but that detail was not verified during the abstract-only access recorded in the provenance log and is not relied upon here. SecTB-RTL contains sequential security regressions. OpenVEF must author independently specified, distinctive cycle-exact semantics, not reuse public benchmark RTL, masks or test sequences without explicit permission and attribution. Candidate differentiators include a carefully specified simultaneous read/write-at-full policy and registered almost-full semantics for FIFO, and exact parity/break/ready semantics for UART. These must be selected and documented, not presumed novel.

**Training-data contamination risk.** Public FIFO/UART examples and testbenches may appear in model training data or retrieval corpora. This cannot be fully eliminated by prompt wording. Minimize contamination by authoring original RTL/spec parameters, avoiding public benchmark identifiers in prompts, recording model/version and the date of generation, and disclosing residual contamination risk. Do not claim the model was blind to the design family.

## 8. Experimental conditions and information boundary

The primary conditions are ORG-A and ORG-B. Both use the same pinned model, system prompt, task instruction, semantic blocks, repair prompt, response schema, feedback rules and token/output limits. Only the order of whole information blocks varies. Prompt headings are identical. Ordering may affect attention; that is why it is the treatment.

Authoring packet: design specification, port manifest, reset/legal-input protocol, cycle cap/safe-idle policy, driver API, trace schema and checker contract.

Evaluator-only pack: RTL, null and mutant netlists, observation mask, mask-to-spec traceability table, reference model/API, expected-output data, miter assumptions, mutant manifests and scoring implementation.

No LLM/human author receives RTL, internal-signal access, the observation-mask file, reference-model/API, expected-output table, mutant identity or mutant result. Every observation-mask entry must be traceable to an explicit clause in the specification authors receive. Mask withholding removes the explicit scoring file, not the specification information.

## 9. System architecture

1. **Split design packs:** authoring packet and restricted evaluator packet with a signed access boundary.
2. **Driver API:** one deterministic step per cycle; harness owns clock and scheduler.
3. **Harness recorder:** captures inputs consumed at an edge, samples outputs after that edge, then records next-cycle inputs.
4. **Offline checker:** isolated pure process over a versioned trace.
5. **Null/mutant export:** same synthesis/export flow and top-level ports.
6. **Fault classifier:** mask-aware bounded equivalence with reset/legal-input assumptions.
7. **Paired runner:** independent null/mutant reactive runs with identical seed and execution contract.
8. **Trace comparator/classifier:** raw and masked divergence plus mutually exclusive outcome ledger.
9. **Common-trace panel:** same legal null/mutant traces to every generated checker.
10. **Reporting:** ITT and conditional metrics with reproducible statistics.

## 10. Paired-run and trace contract

Use independent reactive runs rather than open-loop replay. For each artifact and mutant, run the same deterministic driver on null and mutant with the same seed, reset, simulator, cap, safe-idle and watchdog. Before the first raw output divergence, next-input decisions must match; after divergence, they may differ because the driver reacts to outputs. Each row records inputs consumed at edge n, outputs after edge n and next inputs scheduled for edge n+1. Outputs are sampled before invoking the driver for the next inputs (output-first same-row tie).

The checker receives only a trace and public metadata. It cannot access live simulator objects, internal signals or mutate the trace. It derives expectations from specification and trace inputs/history; it cannot call evaluator reference models/APIs.

## 11. Fault population and bounded equivalence

The primary population is Yosys/MCY post-synthesis structural netlist signal mutants. These are not automatically source-level design errors, manufacturing stuck-at faults or physical silicon failures. Inspect exact mutation modes for the pinned tools before making stronger claims. CovR authors call its artifacts “RTL mutants” generated with MCY-Yosys; OpenVEF should quote that author terminology and explain separately that MCY operates post-synthesis.

Only legal-input mutants with a masked-output counterexample within the fixed bound enter the primary eligible set. `BOUNDED_EQUIVALENT_N` means no counterexample through depth N, not unbounded equivalence. `UNDECIDED` and out-of-budget candidates are reported and excluded under a pre-registered rule.

## 12. Outcomes and denominators

The canonical formulas and precedence are in Protocol §§12–14. In brief:
- ITT validity: valid artifacts / all scheduled generation slots.
- Conditional complete-trace exposure `E_i = X_i/|T_i|`, where `X_i = DET + PND + CHECKER_ERROR_AFTER_MASKED_DIVERGENCE` and `T_i` includes every complete-trace valid pair, irrespective of checker response. `E_i` is checker-independent by construction; ITT `J_exposure` depends on the checker through the validity gate.
- Detection `S_i = DET_i/X_i`; checker crashes after exposure count as non-detections.
- Miss composition `M_i = PND_i/(NP_i+PND_i)` is descriptive only.
- ITT joint exposure and detection use all scheduled slot × primary-mutant combinations as denominator.
- Common-trace checker sensitivity is a secondary standardized measure with explicit compatibility/false-alarm/error handling.

## 13. Statistical analysis

The primary H2 unit is the scheduled generation slot. For joint outcomes, compute the per-slot fraction of the fixed mutant set exposed/detected. Use one design-stratified treatment-effect test per endpoint, with the proposed equal-weight combination of fixed design strata; randomize/permutate at slot level within design. Apply Holm across exactly three two-sided outcomes (one each for validity, joint exposure and joint detection), not separate confirmatory tests for each design. The exact design set and weights must be frozen before generation. Conditional diagnostics use ratio-of-sums and artifact-cluster bootstrap; common-trace panel inference is secondary, conditional on its fixed corpus and resampled at checker/artifact level.

## 14. Risks and limitations

1. This is an incremental empirical study and open implementation, not a new verification theory or mutation engine.
2. The literature review is targeted, not systematic; native IEEE Xplore/ACM DL and some conference proceedings remain incompletely searched.
3. “Not found in sources reviewed” is not “does not exist”; no first/novel-method claim is permitted.
4. The TechRxiv preprint is unreviewed. Earlier secondary notes differ on its mutation-injection description, but the independent Step 3 audit had abstract-only access; neither method description is verified from the paper text in this pack.
5. FIFO/UART overlap with GateTruth, DVBench and the reviewed data-integrity work; the alleged TechRxiv FIFO example is unverified and is not counted as established overlap. Original specs and residual contamination risk must be disclosed.
6. LLM training data may include similar public designs/testbenches; complete exclusion cannot be guaranteed.
7. The mask can be wrong or the design specification incomplete; independent review and mask-to-clause traceability are required.
8. The evaluator-only mask removes the explicit scoring file, not the underlying specification obligations.
9. Own-driver `S_i` conditions on artifact-specific exposure and is not a pure checker-quality estimate.
10. `NP` is no masked output divergence, not proof that internal fault activation did not occur.
11. Structural signal mutants are not automatically source-level bugs or manufacturing fault models.
12. Checker history derived from faulty DUT outputs may accept self-consistent corruption.
13. Common-trace results are conditional on the frozen corpus, mutant population and compatibility rules.
14. Valid-only diagnostics condition on a post-prompt outcome; ITT outcomes retain all scheduled slots.
15. LLM nondeterminism, model drift, prompt leakage, repair asymmetry and low artifact-validity rates may limit inference.
16. Small design counts and a selective mutant population limit generalization.

## 15. Project milestones and gates

1. **Research-design approval:** complete — owner approved the seven v0.7 methodological decisions on 22 November 2026.
2. **Independent v0.7 audit:** completed with `PASS WITH CORRECTIONS`. The limited hand-built feasibility scope is conditionally available after owner acceptance; any LLM call remains blocked pending an independent audit of the v1.1 prompt/schema/repair/assembly corrections.
3. **Design/mask specification:** pending; includes original FIFO/UART semantics and mask-to-clause table.
4. **Feasibility engineering:** after owner acceptance, only the FIFO specification/mask, hand-built harness, F1–F15 and F17 using hand-built FIFO control mutants and hand-built known-answer checkers may start. No F16 or other LLM call yet.
5. **F1–F18:** formal status not run, since no authorized F1–F18 acceptance run exists (development-run evidence: runs of a project implementation, recorded outside this pack, are development runs, not F1–F18 acceptance; approval: nothing is qualified or approved); all must pass on FIFO.
6. **F16 pilot:** not run; mutant-blind; each arm × design stratum must separately meet the proposed frozen validity floor.
7. **Power/precision and freeze:** not done; exposure/detection inputs come from prespecified assumed grids and independent baselines, never from F16.
8. **Confirmatory generation:** prohibited until every Protocol §18 item is complete and sealed.

## 16. Review provenance

The v1.3.6 release retains the seven owner-approved v0.7 design directions and records the historical v0.8, v0.9, v1.0, v1.1, v1.2, v1.3, v1.3.1, v1.3.2 and v1.3.3 audit outcomes. The v1.3, v1.3.1, v1.3.2, v1.3.3 and v1.3.4 independent document audits returned FAIL for the LLM-call gate; the owner-supplied v1.3.5 audit summary reports a document-only PASS. The current formulas, outcome classes, F1–F18 controls and freeze checklist are specified in `02_OpenVEF_Experimental_Protocol_v1.3.7-candidate.md`. This v1.3.6 corrective evidence/metadata release incorporates the verified v1.3.2 audit export and the non-blocking cleanup from the v1.3.5 audit. Its own independent document re-audit remains pending. No implementation or LLM/provider call is implied.


## 17. v0.9 audit response status (historical)

The Claude v0.9 audit found N1/N2 resolved and N3/N4/N9 partly resolved. This Charter adopts its D1–D15 correction list as proposed requirements, including model-visible driver/checker contracts, an exhaustive failure-to-stage map, deterministic repair serialization, system/repair extraction rules, schema sidecar hashes, parser fixtures, hand-built-only feasibility F17 and consistent owner/gate records. No implementation or LLM execution is implied. The v0.9 audit returned FAIL for the LLM-call gate; its V1–V7 correction set is historical and the current v1.0 audit blockers B1–B9 plus the full mandatory fixture suite remain subject to independent re-audit.


## 18. v1.0 independent audit response status

The v1.0 independent audit returned FAIL for the LLM-call gate. Its nine blockers B1–B9 concern fixture input shape, intended-stage isolation, error-class agreement, module-level AST stage ownership, total import precedence, non-ASCII identifier and column rules, mid-run design-halt lifecycle, F18-only disposition/error vocabulary, and clause-ID token/near-match rules. The v1.2 package proposed document and fixture corrections only; it does not claim the blockers have passed re-audit. The strict-AST branch remains a pending owner choice (X14); A1–A11 remain unaccepted. That response executed no parser, assembler, harness or fixture suite. Current status, in three separate parts: development-run evidence: fixture runs of a project implementation, recorded outside this pack, are development runs, not F18 acceptance; formal F18 status: **NOT RUN / NOT PASSED**, since no authorized F18 acceptance run exists; approval: no implementation is qualified or approved.

---

**v1.3.7 CANDIDATE, not audited.** This file is OpenVEF Planning v1.3.6 with only the corrections listed for it in `CHANGELOG-v1.3.7-candidate.md` (owner decision D-024). It is not part of any released, audited or approved pack; v1.3.6 remains the default.
