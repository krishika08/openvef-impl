> **Historical foundation note:** this review predates the v0.7 decision to use ORG-A/ORG-B whole-block presentation-order-only prompts. Any direct-versus-structured wording below describes an earlier candidate factor and is superseded by the v0.7 Charter and Protocol.

# OpenVEF Research Foundation — Functional Qualification and Mutation Analysis (Revision 0.2)

**Document:** 06 — Step 2 foundation note, revision 0.2  
**Project:** OpenVEF — Open Verification Effectiveness Framework  
**Prepared:** 22 November 2026  
**Status:** Research note, revised after independent Claude audit and source re-check; not a frozen protocol  
**Scope:** Functional qualification, mutation analysis, activation/propagation/detection, Certitude, and implications for OpenVEF.

---

## 1. Executive summary

Functional qualification is established prior art in hardware verification. It applies mutation analysis to the verification environment itself: introduce controlled faults into a design, run the verification environment, and check whether the environment actually reports a failure. The key idea is that code coverage or functional coverage alone does not demonstrate that a testbench can expose and detect faults.

The central conceptual sequence is:

1. **Activation:** the applied stimulus causes the injected fault to affect the design's internal behaviour.
2. **Propagation:** the resulting erroneous effect reaches an observation point.
3. **Detection:** a checker, assertion, scoreboard, or test verdict flags the error.

A testbench can fail at any of these stages. This decomposition is not new and must not be claimed as OpenVEF's invention.

The literature relevant to OpenVEF includes:

- Devadas, Ghosh and Keutzer (ICCAD 1996), who introduced observability-aware coverage for functional simulation by tracking whether the effects of executed statements could reach outputs.
- Bombieri et al. (DATE 2009), who explain functional qualification for TLM verification and distinguish a mutation that changes outputs from one that causes a test case to fail.
- Bombieri et al. (DATE 2009), who explicitly distinguish output-difference mutation analysis from functional qualification, where a testcase must fail. The paper is co-authored by two Certess employees and uses the Certess/Certitude context; it is peer-reviewed but not vendor-independent.
- Bombieri et al. (IEEE Transactions on Computers, 2014), who develop a SystemC TLM protocol mutation model and reduce redundant mutants. Despite the phrase “testbench qualification” in the title, their kill criterion is output-trace difference, not a testcase/checker failure; classify this as mutation-based testbench assessment, not functional qualification under the DATE 2009 definition.
- Huang et al. (VLSI Design, 2015), who explicitly qualify stimulus, a coverage model, and checkers using mutation analysis. Their checker-completeness factor is a direct conceptual precedent for OpenVEF's secondary `checker_gap`, although its exposure proxy differs.
- Lisherness and colleagues' coverage-discounting work (HLDVT 2011; DATE 2013), which links surviving mutants to functional coverpoints and improves interpretation of mutation results.
- Lin et al. (DATE 2012), who develop probabilistic error-propagation analysis for functional qualification and explicitly compare fault-based verification with gate-level stuck-at fault simulation.
- Certitude, a commercial functional-qualification tool launched by Certess in 2007 and now represented in Synopsys' Testbench Quality Assurance offering.

**Implication:** OpenVEF inherits established mutation analysis and functional-qualification concepts. Its candidate study design focuses on newly LLM-generated driver/checker artifacts, matched-information prompt formats, paired executions, and an observation boundary defined by a pre-frozen specification mask. This is not yet a novelty claim: Step 3 must assess LLM-generated hardware verification studies, especially SecTB-RTL, GRPO-SMu, GateTruth, AutoBench and related benchmarks.

## 2. Mutation analysis: the basic idea

Mutation analysis evaluates a test suite by creating modified versions of the design or program. Each modified version is a **mutant**. A mutation operator makes a small, controlled change intended to represent a plausible implementation mistake.

Examples of source-level RTL mutation operators include:

- Replace a relational or Boolean operator (`>` with `<`, `&&` with `||`).
- Change a constant or comparison threshold.
- Force a condition true or false, or invert a condition.
- Delete an assignment.
- Remove a branch or a `case` item.

For each mutant, the same test inputs are applied to the reference and the modified design. If the verification process reports the mutant, the mutant is commonly said to be **killed**; otherwise it **survives**. The exact meaning of “killed” depends on the method:

- In basic output-comparison mutation analysis, an observable output difference can be treated as a kill.
- In functional qualification, a mutant is considered detected only when the verification environment itself reports a failure. A changed output that is not checked is not enough.

This distinction is essential. A test can make the faulty design behave differently without any checker noticing. Counting every output difference as a successful test would overstate verification effectiveness. A useful way to separate the layers is: output-difference comparison is the fault-simulation/exposure layer; requiring the verification environment itself to fail is the functional-qualification layer. OpenVEF deliberately records both an independent masked output divergence and the artifact's own checker verdict.

### Mutation score

A conventional mutation score is commonly expressed as:

`mutation score = killed non-equivalent mutants / all non-equivalent mutants`

The denominator excludes mutants that are functionally equivalent to the original design. Equivalent mutants are important because no test can distinguish a truly equivalent mutant from the reference. In general, deciding equivalence automatically can be difficult or undecidable; a bounded formal pass must not be described as an unbounded equivalence proof.

A mutation score is conditional on the chosen mutation operators and the mutant population. It is not a universal percentage of all possible real design bugs.

### Three fault/mutation families that must not be conflated

1. **Source-level design-error mutants:** syntactic or semantic RTL edits such as operator/condition replacement, constant changes, deleted assignments or missing cases. These aim to approximate plausible design mistakes.
2. **Post-synthesis netlist signal mutants:** mutations applied to individual signals/bits in a synthesized netlist. MCY describes its approach as modifying individual signals in a post-synthesis netlist and formally filtering mutations that can make an important output change. This is the current OpenVEF population. It is structurally closer to netlist-level fault simulation than to source-level RTL design-error mutation.
3. **Manufacturing-test fault models:** e.g., stuck-at-0/stuck-at-1 faults, often graded by whether a test pattern causes a primary-output difference against a fault-free response. These are used for manufacturing test and are not automatically equivalent to MCY's netlist signal mutations.

OpenVEF must not call its MCY population “stuck-at faults” or claim it represents physical silicon defects unless the exact mutation modes generated by the pinned Yosys/MCY release are inspected and shown to implement those fault semantics. The current safe label is **structural netlist signal mutants**. Record each actual `mutate` command, mutation mode, affected netlist object, tool version and exported netlist hash.

## 3. Activation, propagation and detection

These are three separate questions, not synonyms.

| Stage | Meaning | What has to happen? | Typical reason for failure |
|---|---|---|---|
| Activation | The stimulus reaches a condition where the injected fault changes internal behaviour. | Inputs/state sensitise the faulty logic. | The driver never exercises the relevant state or boundary condition. |
| Propagation | The internal difference reaches an observation point. | The erroneous value is not masked and becomes observable. | A controlling value, downstream logic, state transition, or selected observation boundary hides the difference. |
| Detection | The verification environment reports the discrepancy. | A checker/assertion/scoreboard/test verdict flags it. | The checker is missing, too weak, incorrectly conditioned, or does not inspect the affected behaviour. |

**Example — FIFO full-flag fault**

Assume a synchronous FIFO should assert `full` only when all entries are occupied. A mutant changes the threshold so `full` asserts one entry too early.

- If the driver never fills the FIFO near capacity, the fault may never be activated.
- If the faulty internal state changes but the difference does not reach an observed output or selected observation point, the effect has not propagated to that observation boundary.
- If the output `full` differs but the checker never checks it, the fault is exposed but not detected.
- If the checker verifies `full` against the specification and fails, the fault is detected.

The same fault therefore tells us different things about the driver's stimulus, the observation boundary, and the checker.

### Observation boundaries differ across sources

“Propagation” does not have one perfectly uniform operational boundary across the public literature and practitioner descriptions. Some sources define it at the primary outputs or designated observation probes; other Certitude-oriented practitioner taxonomies describe it as reaching a checker. Those definitions can classify the same run differently. For example, an output may differ but remain unchecked: it has propagated to the output under an output-based definition, but has not propagated to a checker under a checker-boundary definition.

OpenVEF defines propagation independently of the generated checker: it is a divergence on a top-level output/cycle selected by the versioned specification observation mask. The artifact's offline checker verdict is then applied as a separate detection stage. This is deliberate and must be stated every time NP/PND are compared with legacy labels.

Under OpenVEF's current partition, `NP` means **no specification-masked output divergence within the fixed run window and checker PASS**. It can contain several different situations:

- no raw top-level output divergence occurred;
- a raw output divergence occurred, but only on an unmasked output or in an unmasked cycle/window;
- the chosen stimulus did not expose the fault within the fixed cycle cap (without proving it could never be exposed by another/longer stimulus).

Because internal fault activation is not instrumented, OpenVEF cannot distinguish non-activation from internal activation without propagation to a masked top-level output. It must not interpret NP as proof that a mutation was never activated. Report NP split descriptively by whether any raw output divergence occurred; this is possible from the archived raw-divergence indicator and does not require a new outcome class.

## 4. Why code coverage and functional coverage are not enough

Code coverage can tell us whether a line, branch, toggle or state was exercised. Functional coverage can tell us whether engineer-defined behaviours or scenarios were hit. These are useful measurements, but they do not by themselves prove that an injected error would propagate to an observation point or trigger a checker.

The 2015 Huang et al. paper identifies this limitation directly: common coverage approaches emphasise activation/execution and can overlook propagation and checker sufficiency. It also notes that the coverage model and the checker set are themselves human-authored artefacts and can be incomplete.

### Observability-based coverage: an earlier precursor

Devadas, Ghosh and Keutzer's ICCAD 1996 paper proposes an observability-based coverage metric for functional simulation. It tags variables during simulation to track whether effects associated with executed assignments can propagate through the design to circuit outputs. The point is that execution alone is not enough; the effect must be observable.

This work is an important conceptual precursor to the propagation part of functional qualification. However, it is not the same as a full testbench qualification method: its focus is a metric for functional vector sets and observability, not an evaluation of whether the testbench's checker reports a failure.

Fallah, Devadas and Keutzer's OCCOM work (DAC 1998) develops an efficient computation method for observability-based code coverage.

## 5. Functional qualification and Certitude

Functional qualification applies mutation analysis to the verification environment. Instead of only asking whether the stimulus causes a different output, it asks whether the verification environment detects the injected fault.

The practical loop is:

1. Select a fault model and generate controlled mutants.
2. Run the verification environment on the original design to establish the normal result.
3. Run relevant tests on the mutants.
4. Determine which faults were activated, which effects became observable, and which were detected by checks.
5. Use surviving mutants as evidence of weaknesses in stimulus, observation/coverage, or checking.
6. Improve tests, coverage points or checkers, then repeat qualification.

Certess launched Certitude in May 2007 as a commercial functional-qualification tool. A 2009 technical brief by Mark Hampton (Certess) explains Certitude's distinction from conventional mutation analysis: a fault is detected when a test case fails, and detection may occur through internal checks/assertions even when the fault does not reach a primary output. The brief describes deterministic, syntax-oriented mutation operators such as forcing or inverting conditions, deleting assignments or case branches, replacing operators and changing constants.

The same brief describes selective mutation: a practical subset of possible mutation operators is used because the full fault population can be very large. That makes the resulting score useful only in relation to the stated fault model. It does not prove that every possible real-world bug will be caught.

Certitude's public terminology should be handled carefully. DATE 2009 describes functional qualification as requiring testcase failure and permits internal/external assertions. Public practitioner descriptions vary in whether the intermediate “propagation” boundary is described as an output/probe or as reaching a checker. A Synopsys verification bulletin, for example, distinguishes no output difference from an output difference that the testbench does not report, while its summary taxonomy uses “propagated to a checker.” Do not treat all these labels as perfectly interchangeable. OpenVEF's own mask-first definition avoids the ambiguity by fixing the exposure boundary independently of the checker.

Synopsys currently presents a Testbench Quality Assurance offering with “verification improvement” and “metric” modes, and describes identifying weaknesses in stimuli, observability, checkers, assertions and the verification plan. This is evidence that qualification remains an active commercial verification practice; it is not independent evidence for any particular research claim about OpenVEF.

## 6. Academic development of the method

### 6.1 Bombieri et al., DATE 2009 — Functional Qualification of TLM Verification

This paper applies functional qualification to transaction-level modelling. It states the central distinction clearly: traditional mutation analysis may treat a mutation as killed when the output differs, while functional qualification requires that a test case fail. It discusses expected-output checks and assertions monitoring internal or external behaviour.

The paper also proposes a mutation model for SystemC TLM behaviours based on extended finite-state machines (EFSMs), linking protocol-level errors to mutants. This matters because mutation operators should reflect the abstraction and behaviour being tested; arbitrary low-level changes are not automatically a meaningful fault model for a protocol.

### 6.2 Bombieri et al., IEEE Transactions on Computers, 2014 — Testbench Qualification of SystemC TLM Protocols through Mutation Analysis

The 2014 article extends the earlier DATE 2008 TLM mutation model and the related MTV 2009 work to the OSCI TLM-2.0 standard; it should not be described as an extension of the DATE 2009 functional-qualification paper. Its methodology includes:

1. Model TLM primitives and protocols with EFSMs.
2. Define an EFSM fault model based on an extension of transition faults.
3. Identify classes of design errors that can occur in protocol implementations.
4. Build a mutant library and map design errors to EFSM faults, seeking a minimal set that reduces redundancy.
5. Automatically inject the mutants into user designs by replacing standard TLM primitives with mutated versions.

Important classification correction: the 2014 paper describes “testbench qualification” and has a mutation score, but its Sec. 3.2 says a mutant is killed when the output trace differs from the fault-free run. It does not require a testcase failure/checker report as the kill condition. It should therefore be cited as mutation-based testbench assessment and mutant-model engineering, not grouped unqualifiedly with the narrower DATE 2009 functional-qualification criterion.

The paper's important lesson for OpenVEF is that a mutation population needs a rationale and a model. A set of syntactically possible changes is not automatically a useful or representative set of faults. It also explicitly discusses equivalence as undecidable and excludes equivalent mutants from the conventional mutation-score denominator; OpenVEF's bounded-equivalence labels must remain explicitly bounded.

### 6.3 Huang et al., VLSI Design, 2015 — Functional Testbench Qualification by Mutation Analysis

This is the closest foundational academic work for OpenVEF's use of the activation/propagation/detection framework.

The authors explicitly model three testbench components:

- **Stimulus** to activate the design.
- **Coverage model** to observe and record whether functions were exercised.
- **Checkers** to verify internal states and outputs.

They identify four possible coverage/checker reaction combinations when a mutant is simulated:

| Coverage result | Checker result | Interpretation in the paper |
|---|---|---|
| Fluctuates | Mutant killed | Coverage points and checkers behave consistently; sufficient region. |
| Fluctuates | Mutant survives | Checker deficiency is suspected. |
| Stable | Mutant killed | Some coverage points may be missing. |
| Stable | Mutant survives | Ambiguous: fault may not be activated, both coverage/checkers may be deficient, or the mutation may be in dead code. |

The last row is explicitly ambiguous; the paper says further analysis of that situation is future work. This is important: even prior functional qualification work recognises that a surviving mutant does not automatically identify one unique cause.

The authors also propose a composite testbench-quality metric that combines stimulus quality, coverage-model quality and checker quality using user-selected weights. The paper's example uses weights 0.2, 0.4 and 0.4, with a target threshold of 0.9. Its stimulus component combines compactness and coverage completeness; its coverage component estimates the useful portion of coverpoints; and its checker component combines checker compactness (the proportion of checkers that fire) with checker integrity/completeness (the proportion of coverage-fluctuating mutants that are killed). OpenVEF's secondary `checker_gap` is analogous only to the latter exposure-conditioned component, not to Huang's entire composite checker-quality term.

**A direct precedent for OpenVEF's secondary checker metric:** Huang et al.'s checker `integrity_factor` is the number of killed mutants with fluctuating coverage divided by the total number of mutants with fluctuating coverage. In other words, it measures checker-side detection among the paper's “exposed” subset. OpenVEF's `checker_gap = PND / (DETECTED + PND)` is the complementary miss fraction among pairs with a masked output exposure. The relationship is conceptual, not an exact numerical equivalence: Huang's exposure proxy is coverage-result fluctuation, whereas OpenVEF's is a frozen specification-mask output divergence; the units and fault populations also differ.

The authors demonstrate the iterative refinement process on an interconnection module and a commercial RISC CPU. For the interconnection module, they report 623 mutants, 64 possible coverpoints and 16 checkers. Under random stimulus, the reported composite quality rises from 0.51 to 0.91 over nine iterations; with directed stimulus, from 0.51 to 0.92 over six iterations. On the commercial CPU, the reported score rises from 0.48 to 0.91 over ten iterations. These values are confirmed in the article's Tables 2–4: 0.91 (random), 0.92 (directed), and 0.48 to 0.91 for the CPU. Claude's audit could not locate these values in the particular text view it accessed, but a fresh check of the open-access Wiley HTML exposes the table cells. They remain results under the paper's own composite metric and setup and are not directly comparable to OpenVEF's outcome rates.

## 7. What this prior art means for OpenVEF

OpenVEF must be explicit about what it inherits and what it changes.

| Topic | Established prior art | Current OpenVEF design | Consequence |
|---|---|---|---|
| Activation / propagation / detection | Established functional-qualification framework. | Uses the concepts, does not claim to invent them. | Cite as foundational method. |
| Mutation-based qualification | Certitude and academic testbench-qualification work use injected faults to evaluate verification. | Uses a fixed candidate population of netlist signal mutants. | Must justify fault model, exclusions and representativeness. |
| Stimulus and checker weakness | Huang et al. analyse stimulus, coverage and checker components; Certitude provides diagnostic feedback. | Measures NP versus PND at the artifact–mutant-pair level. | This distinction is not novel by itself. |
| Coverage model | Huang et al. include a separate functional coverage model. | OpenVEF MVP does not qualify a separate coverage model. | Do not claim to measure all three Huang components. |
| Observation boundary | Prior functional qualification can use internal checks/assertions; public tool/practitioner sources vary in whether propagation is described at outputs/probes or at the checker. | Uses a pre-frozen specification-derived top-level output mask, independent of the artifact's checker. | State the boundary explicitly; never directly equate labels from different schemes. |
| Checker-side metric | Huang et al. define a checker completeness factor among coverage-fluctuating mutants. | `checker_gap = PND/(DETECTED+PND)` among masked-exposure pairs. | Direct conceptual precedent; exposure proxy and unit differ. |
| Fault model | Literature includes source-level design-error mutants, protocol-specific EFSM faults and manufacturing-test stuck-at faults. | Yosys/MCY post-synthesis netlist signal mutants. | Call them structural netlist signal mutants; do not claim stuck-at or source-bug equivalence without mode-level validation. |
| Study unit | Many qualification methods report suite/testbench-level fault outcomes and may drop redundant faults. | Each generated driver/checker artifact is evaluated against the fixed mutant set. | Potential study-design distinction; verify against LLM-era work before any novelty claim. |
| Unit of analysis | Existing work often evaluates a testbench or suite against a mutant set. | Repeated independently generated driver/checker artifacts; artifact-level summary. | A study-design distinction to test in wider literature. |
| Prompt factor | The foundational studies predate modern LLM prompt-structure experiments. | Direct vs structured prompts with identical design information. | Candidate empirical dimension, not sufficient alone to prove novelty. |
| Equivalence handling | Equivalent mutants should not be scored as killable; general equivalence is difficult. | Mask-aware bounded miter with labels bounded to depth N. | Never describe “no counterexample to N” as unbounded equivalence. |

### 7.1 Mapping the OpenVEF outcomes

OpenVEF defines the propagation boundary as **a top-level output divergence on a signal/cycle admitted by the pre-frozen specification mask**. The boundary is independent of the generated checker.

- `DETECTED`: a specification-masked output divergence occurs and the artifact's offline checker returns `FAIL`.
- `PND`: a specification-masked output divergence occurs and the artifact's checker returns `PASS`.
- `NP`: no specification-masked output divergence occurs within the fixed run window and the checker returns `PASS`.

`NP` is an operational “no masked exposure observed” class, not a direct observation of internal fault activation. It can include (a) no raw output divergence, (b) a raw divergence only on an unmasked signal/cycle, or (c) a fault not exposed by this artifact within the fixed comparison window. Report at least two descriptive NP subcounts: `NP_no_raw_divergence` and `NP_raw_only_unmasked`. Do not introduce these as new primary outcomes; they are diagnostics within NP.

The primary metric `PND / (NP + PND)` is not a conventional mutation score. It is the checker-side share among the artifact's missed faults. The secondary `checker_gap = PND / (DETECTED + PND)` is a checker-miss share among masked-exposure pairs. Huang et al.'s checker-completeness factor is the complementary detection proportion among mutants whose coverage results fluctuate, so it is a close precedent; the exposure proxy differs. Report all denominators and pair counts, and do not compare numerically with Certitude scores, Huang's composite metric, or *Verify the Verifier*'s results.

### 7.2 Important methodological cautions

1. **Fault-model validity:** netlist signal mutants are not the same as source-level RTL design-bug mutants and neither is a model of all physical silicon defects. Name the population precisely.
2. **Equivalent and redundant mutants:** report how generated mutants are filtered. Keep duplicate, invalid, equivalent and undecided counts visible rather than hiding them.
3. **Bounded proof:** a miter with no counterexample through depth N establishes only bounded equivalence under the stated assumptions and bound, not unbounded equivalence.
4. **Observation mask:** a masked divergence is only as trustworthy as the specification and the mask predicates. Freeze them before generation, and validate them independently.
5. **Internal activation is unobserved:** NP must remain an output-observation category, not a claim about what happened inside the DUT.
6. **Selective mutation bias:** conclusions apply to the chosen operators and mutant set. Do not generalise to every real design error.
7. **Higher-order and omission faults:** first-order syntactic mutations may not represent multi-line bugs or missing functionality that has no code location to mutate.
8. **Checker independence:** if the checker is derived from the same incorrect specification assumptions as the design or mask, it can produce misleading results. OpenVEF's independent reference and null-design controls mitigate some risks but do not prove specification correctness.
9. **No single scalar score is enough:** publish the complete outcome partition and the fault-population accounting, not only the primary share.

## 8. Fault-model positioning and adjacent LLM-era work

### 8.1 Netlist signal mutation versus source-level and manufacturing fault models

OpenVEF's current MCY/Yosys population is generated after synthesis by modifying individual netlist signals/bits and filtering candidates with formal techniques. It is therefore a **structural netlist signal fault population**. It is not a source-level RTL design-error population like operator/condition/missing-case mutation, and it is not automatically a manufacturing stuck-at test population. The DATE 2012 probabilistic qualification paper explicitly notes the analogy between fault-based verification and gate-level stuck-at fault simulation, but that analogy does not establish identity between its fault model and MCY's modes.

For OpenVEF, the raw/masked trace comparison is the fault-simulation/exposure part: it asks whether the injected netlist signal perturbation creates a reference-relative observable effect. The offline checker verdict then adds a functional-qualification-style question: does the verification artifact report the effect? Both layers must be reported separately. Before freezing the population, inspect the exact mutation modes in the pinned Yosys/MCY release and record mutation commands; do not describe them as stuck-at-0/1 unless the selected modes literally implement those semantics.

### 8.2 LLM-era adjacent work already known before Step 3

The following works are important early findings. They do not complete the LLM-era literature review; they define the minimum items for Step 3.

| Work | What it evaluates | Relevance and distinction from OpenVEF | Review status |
|---|---|---|---|
| **GRPO with State Mutations** (arXiv:2601.07593, 2026) | A two-stage LLM workflow generates test plans and then executable testbenches; tests run on golden and mutated RTL; reports golden pass rate and mutation-detection rate; also trains with mutation-derived rewards. | Directly studies LLM-generated hardware verification stimuli/testbench artifacts under mutated RTL. The retrieved paper does not report OpenVEF's specific NP/PND decomposition, matched direct-vs-structured prompt-format comparison, or offline-checker artifact metric. Very close adjacent prior art. | Full arXiv HTML reviewed; full bibliographic/venue status to verify. |
| **SecTB-RTL — Trust, but Validate the Instrument** (arXiv:2609.19844, 2026) | AI generates executable stimulus-and-oracle plans for security-regression tasks; 31 tasks and 124 prequalified mutants; task-level repeated prompt arms and paired statistical design were planned. The R3 run had 1,857 provider-accepted outputs but only 9 production-semantic-valid artifacts out of 1,860 calls, so no prompt-effect estimate was reported. | Very close on persisted stimulus-plus-oracle artifacts, golden validation, hidden mutants and controlled prompt arms. Its prompt arms vary information (functional/security content), not merely prompt formatting with identical content; its unit is task-level, and it reports no confirmatory prompt effect. It makes end-to-end artifact-contract validation a mandatory OpenVEF gate. | Full arXiv HTML reviewed. |
| **GateTruth** (arXiv:2608.12635, 2026) | Mutation-testing engine audits whether RTL benchmark testbenches catch seeded semantic mutants; applies its engine to an internal suite and RTLLM v2.0. | Important precedent for using mutation testing to audit the reliability of RTL benchmark testbenches. It is not, in the retrieved paper, a controlled study of LLM-authored driver/checker pairs or an NP/PND attribution analysis. | Full arXiv HTML reviewed. |
| **AutoBench / CorrectBench / ConfiBench** | LLM testbench or related verification-artifact generation and evaluation. | Must be read directly in Step 3, not treated only through secondary descriptions. | Source-level review still required. |

**Consequence for novelty:** prompt comparison, generated stimulus/checking artifacts, golden-design validation, and mutant-based measurement already have close precedents in hardware verification. OpenVEF must not claim any of these elements individually as new. The candidate remaining contribution is the precise combination of an LLM-authored cycle-synchronous driver plus offline checker as the artifact-level unit, a fixed checker-independent specification mask, the NP/PND missed-fault composition, and a matched-information prompt-format comparison. Whether this combination is distinct remains unresolved until Step 3 compares the full methods and denominators of GRPO-SMu, SecTB-RTL, GateTruth, AutoBench, CorrectBench and related work.

### 8.3 Instrument validation is a required feasibility gate

SecTB-RTL demonstrates that provider/schema acceptance can be radically different from production-semantic and execution validity. OpenVEF must therefore run a small, non-confirmatory end-to-end generation pilot before confirmatory LLM sampling. Every scheduled response must be retained in the denominator. The exact persisted artifact must pass the actual parser, API validation, compile, null-netlist control and full production execution path. The acceptable artifact-validity rate and sample-expansion rule must be fixed before the pilot. Pilot outputs are feasibility evidence only and are excluded from confirmatory analysis.

## 9. Current research conclusion

The Step 2 foundation review confirms that the activation/propagation/detection decomposition, mutation-based testbench qualification, and diagnosis of stimulus-versus-checker weaknesses are established. Huang et al. (2015) is particularly direct prior art; Certitude is important commercial prior art; the TLM papers show the methodology's extension to protocol-level and system-level verification.

The current defensible OpenVEF direction remains an empirical study of LLM-authored driver/checker artifacts under a controlled prompt-format experiment, with a checker-independent top-level observation mask and artifact-level analysis. However, GRPO-SMu and SecTB-RTL make the LLM-generated verification-artifact space much more crowded than the initial note suggested. The novelty boundary must remain provisional. It is not a claim that OpenVEF invents functional qualification, prompt-controlled hardware-verification evaluation, or mutation analysis.

**Step 2 status:** Core concepts and the principal functional-qualification lineage reviewed. The broader Step 2 audit is not complete until the source register, related LLM-era studies, and an independent Claude review are reconciled.

## 10. References and source-access notes

1. S. Devadas, A. Ghosh and K. Keutzer, “An Observability-Based Code Coverage Metric for Functional Simulation,” *Proceedings of ICCAD*, 1996, pp. 418–425. DOI: [10.1109/ICCAD.1996.569832](https://doi.org/10.1109/ICCAD.1996.569832). Access level and host should be recorded in the final bibliography; full visual page verification remains pending.
2. F. Fallah, S. Devadas and K. Keutzer, “OCCOM: Efficient Computation of Observability-Based Code Coverage Metrics for Functional Verification,” *Proceedings of DAC*, 1998, pp. 152–157. DOI: [10.1145/277044.277078](https://doi.org/10.1145/277044.277078); journal version, *IEEE TCAD*, 20(8), 1003–1015, 2001, DOI: [10.1109/43.936381](https://doi.org/10.1109/43.936381). Abstract/metadata reviewed.
3. N. Bombieri, F. Fummi, G. Pravadelli, M. Hampton and F. Letombe, “Functional Qualification of TLM Verification,” *DATE*, 2009, pp. 190–195, DOI: [10.1109/DATE.2009.5090656](https://doi.org/10.1109/DATE.2009.5090656). [Proceedings PDF](https://past.date-conference.com/proceedings-archive/2009/DATE09/PDFFILES/03.4_2.PDF). Full proceedings text reviewed. The author block lists the last two authors with Certess; disclose this industry co-authorship.
4. N. Bombieri, F. Fummi, V. Guarnieri and G. Pravadelli, “Testbench Qualification of SystemC TLM Protocols through Mutation Analysis,” *IEEE Transactions on Computers*, 63(5), 1248–1261, 2014. DOI: [10.1109/TC.2012.301](https://doi.org/10.1109/TC.2012.301). University repository manuscript text reviewed; Sec. 3.2 uses output-difference kill semantics. PDF screenshot retrieval returned HTTP 403; no claim of visual page-image inspection is made.
5. K. Huang, P. Zhu, R. Yan and X. Yan, “Functional Testbench Qualification by Mutation Analysis,” *VLSI Design*, 2015, Article ID 256474. DOI: [10.1155/2015/256474](https://doi.org/10.1155/2015/256474). Open-access Wiley HTML reviewed, including equations and Tables 2–4. The 0.91, 0.92 and CPU 0.48→0.91 values are confirmed in the accessible tables.
6. P. Lisherness and K.-T. Cheng, “Coverage Discounting: A Generalized Approach for Testbench Qualification,” *IEEE HLDVT*, 2011, pp. 49–56. DOI: [10.1109/HLDVT.2011.6114165](https://doi.org/10.1109/HLDVT.2011.6114165). Abstract/metadata reviewed.
7. P. Lisherness, N. Lesperance and K.-T. Cheng, “Mutation Analysis with Coverage Discounting,” *DATE*, 2013, pp. 31–34. DOI: [10.7873/DATE.2013.021](https://doi.org/10.7873/DATE.2013.021). Full proceedings PDF text reviewed.
8. H.-Y. Lin et al., “A Probabilistic Analysis Method for Functional Qualification under Mutation Analysis,” *DATE*, 2012. [Proceedings PDF](https://past.date-conference.com/proceedings-archive/2012/PDFFILES/03.2_3.PDF). Full proceedings text reviewed. This work discusses the analogy between fault-based verification and gate-level stuck-at fault simulation.
9. M. Hampton, “Functional qualification: a technical brief,” *edadesignline.com* reprint hosted by Design & Reuse, 2 March 2009. [Article copy reviewed](https://us.design-reuse.com/articles/20223/functional-qualification.html). Hampton was CTO of Certess; this is a vendor perspective, not independent academic validation.
10. Clive (Max) Maxfield, “Certess launches Certitude, first product to enable the functional qualification of electronic designs,” *EDN*, 7 May 2007. [Article](https://www.edn.com/certess-launches-certitude-first-product-to-enable-the-functional-qualification-of-electronic-designs/). Trade-press launch report; corroborated by the contemporaneous Certess announcement.
11. Synopsys, “Testbench Quality Assurance.” [Product page](https://www.synopsys.com/verification/simulation/testbench-quality-assurance.html). Current commercial product description; not evidence for academic novelty.
12. YosysHQ, “Mutation Cover with Yosys (MCY),” [repository](https://github.com/YosysHQ/mcy) and [mutation export documentation](https://yosyshq.readthedocs.io/projects/mcy/en/latest/mutate.html). Tool documentation reviewed; pin a release and inspect actual generated mutation modes before describing them at a more specific fault-model level.
13. D. Große, H. M. Le, M. Hassan and R. Drechsler, “Guided Lightweight Software Test Qualification for IP Integration using Virtual Prototypes,” *ICCD*, 2016, pp. 606–613. [Proceedings PDF](https://ics.jku.at/files/2016ICCD_SWTestQualificationIPVP.pdf). Adjacent work on software-driven IP-integration tests, not a direct RTL testbench study.
14. D. V. Kochar et al., “GRPO with State Mutations: Improving LLM-Based Hardware Test Plan Generation,” arXiv:2601.07593, 2026. [arXiv](https://arxiv.org/abs/2601.07593). Full arXiv HTML reviewed.
15. H. Xiao et al., “Trust, but Validate the Instrument: Auditing AI-Generated RTL Verification Plans on Authored Security-Regression Proxies,” arXiv:2609.19844, 2026. [arXiv](https://arxiv.org/abs/2609.19844). Full arXiv HTML reviewed.
16. M. Bhadra, “GateTruth: Auditing the Rigor of RTL Design Benchmarks via Mutation Testing,” arXiv:2608.12635, 2026. [arXiv](https://arxiv.org/abs/2608.12635). Full arXiv HTML reviewed; include in Step 3.

A practitioner taxonomy source described by the Claude audit as a DVCon “Who's Watching the Watchmen” paper was not independently located under that exact title in this source check. The broad point that some Certitude-oriented sources define propagation at a checker is supported by accessible practitioner material, but the exact DVCon bibliographic record should be verified before formal citation.

---

## 11. Scope of this note — what remains open

This note is the first foundation deliverable for Step 2. Remaining work includes:

- Verify the precise mutation terminology and denominator conventions across the cited sources.
- Examine the complete 2014 IEEE Transactions paper and its fault-model details where access permits.
- Review additional RTL/SystemC mutation tools and fault models to place Yosys/MCY netlist signal mutants accurately.
- Complete Step 3: compare the LLM-era work directly, including GRPO-SMu, SecTB-RTL, GateTruth, AutoBench, CorrectBench, ConfiBench, Verify the Verifier and relevant testbench/benchmark datasets.
- Verify exact Yosys/MCY mutation modes for the pinned version and decide whether the fault population should be described only as structural netlist signal mutations or with a narrower mode-specific taxonomy.
- Update the OpenVEF prior-art comparison and contribution statement only after that wider review.
