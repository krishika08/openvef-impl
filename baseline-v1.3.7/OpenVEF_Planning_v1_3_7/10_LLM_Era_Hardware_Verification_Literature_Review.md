> **Historical source-review record:** This is the first-pass Step 3 literature draft prepared against the v0.5/v0.6 planning baseline. Its gap assessment, prompt-factor interpretation, older metric language and some source-access claims are not canonical. Use `12_OpenVEF_Candidate_Gap_Assessment.md` and `17_Step3_Literature_Audit_Addendum_v0.7.md` for the current v0.7 research position, and `22_Source_Access_Provenance_Log.md` for source-access limitations; where an access claim differs, the provenance log controls. Retained here as a source-evidence and review-history record.

# OpenVEF Step 3 — LLM-Era Hardware Verification Literature Review

**Document status:** Research draft; independent audit pending  
**Review date:** 22 November 2026  
**Project baseline:** OpenVEF Charter and Experimental Protocol v0.5 (pre-freeze)  
**Decision status:** CONDITIONAL GO; no novelty determination is final

## 1. Executive finding

The LLM-era hardware-verification literature already covers most broad ingredients that appeared in earlier OpenVEF descriptions:

- LLM generation of testbench drivers and checkers;
- validation of generated testbenches on correct and mutated designs;
- generation of assertions from specifications and mutation-based assessment of their bug-detection ability;
- comparison of direct generation with more structured or refined prompting workflows;
- seeded semantic mutation of RTL benchmarks to audit testbench strength;
- use of LLMs to identify missing checkers from mutation-induced behavioral differences;
- template/DSL-mediated UVM generation and coverage closure (HAVEN);
- multi-agent testbench generation with mutation-based evaluation and testbench-error triage (PRO-V);
- reinforcement-learned stimulus engines that improve coverage and mutation detection in a larger verification flow (CovR);
- fine-grained internal SVA generation (DeepAssert).

The strongest direct overlap is not a single paper. It is a combination of **SecTB-RTL**, **AutoBench and its CorrectBench/ConfiBench successors**, **AssertLLM2**, **GateTruth**, and the February 2026 TechRxiv preprint **LLM-Aided Verification Gap Detection**. A November 2026 PQC accelerator study, **From FIPS to FPGA with LLM Agents**, adds a recent example of netlist-mutant gate auditing and specification-derived tests.

Consequently, OpenVEF must not claim novelty for generating hybrid driver/checker testbenches, using mutations to evaluate them, comparing prompting approaches in general, or decomposing verification misses into stimulus/checker causes. Those ideas have clear prior art.

The only plausible remaining contribution is a much narrower empirical configuration: independently sampled LLM-authored driver/offline-checker pairs as the unit of analysis; a prompt-structure manipulation with information content held constant; a fixed, checker-independent, specification-derived output mask; and a transparent pair-level miss breakdown on a declared structural netlist-mutant population. The reviewed sources do not establish that this exact combination has already been reported, but the exact combination is only a candidate: the nearest checker-gap preprint already covers the basic differential-output/checker-pass logic, while SecTB-RTL, AutoBench/CorrectBench/ConfiBench, PRO-V and CovR cover several generation, prompt, mutant and stimulus components. The review is not systematic and the claim remains provisional.

**Step 3 decision: CONDITIONAL GO, with a material novelty risk.** The research question and the primary metric should not be frozen until Claude audits the newly identified checker-gap preprint, SecTB-RTL, and the exact distinction between a descriptive miss-composition metric and causal attribution.

## 2. Literature map and taxonomy

The papers fall into six overlapping families. Keeping these families separate prevents us from comparing different tasks as though they were the same experiment.

| Family | Typical generated or studied artifact | Typical evidence | Relevance to OpenVEF |
|---|---|---|---|
| Hybrid testbench generation | Driver/stimulus plus checker/oracle | Compile, golden-design pass, mutant evaluation | Direct prior art for the driver+checker artifact concept |
| Testbench self-validation and correction | Complete testbench with scenario list and checker | Golden or generated-imperfect RTL; scenario correctness; pass rates | Prior art for validating and repairing generated tests |
| Assertion generation | SVA or property set | Syntax, formal proof, coverage, mutation bug-kill ratio | Prior art for LLM-generated checkers, but not generated stimulus-driver pairs |
| Mutant-based benchmark auditing | Existing benchmark testbench | Seeded semantic mutants and kill rates | Prior art for auditing whether a benchmark's testbench is trustworthy |
| Security and agentic verification plans | Verification plan with stimulus and checks, rendered by trusted harness | Hidden mutants, golden validation, prompt arms, task-level analysis | Closest large experimental design to an LLM-generated verification artifact study |
| Checker-gap discovery | Existing UVM testbench plus LLM-suggested missing checks | Differential simulation and undetected output divergence | Direct conceptual overlap with checker-gap identification, but a different population of tests |

A survey published in October 2026 organizes LLM-integrated hardware verification across SVA generation, stimulus/testbench generation, debugging and repair, formal verification, benchmarks, and agentic tool workflows. It is useful as a field map, not a substitute for primary-source analysis. [Survey, arXiv:2610.10580](https://arxiv.org/abs/2610.10580)

## 3. Core papers and findings

### 3.1 AutoBench (2024): hybrid driver and checker generation

**Reference:** Ruidi Qiu, Grace Li Zhang, Rolf Drechsler, Ulf Schlichtmann, and Bing Li, “AutoBench: Automatic Testbench Generation and Evaluation Using LLMs for HDL Design,” arXiv:2407.03891; MLCAD 2024.  
**Source:** https://arxiv.org/abs/2407.03891

**What it does.** AutoBench takes a natural-language DUT specification and generates a testbench using separate scenario, driver, and Python-checker stages. The Verilog driver supplies inputs and exports signal traces; the Python checker computes expected signals and checks the trace. The paper explicitly separates the driver from the checker and standardizes the sequential-driver trace format because LLMs sometimes omit per-cycle inputs.

**Evaluation.** It uses multiple gates: syntax/compilation (Eval0), passing the golden RTL (Eval1), and a mutant-oriented Eval2. In Eval2 the testbench under evaluation and a golden testbench are run on each mutant; success is defined as matching pass/fail reports. Thus Eval2 is not simply an independent specification oracle: it measures agreement with the golden testbench. The paper reports, for 75 sequential circuits, Eval2 pass@1 of 26.00% for AutoBench versus 7.73% for the direct-generation baseline. The overall task suite has a broader set of reported pass@k results.

**Overlap with OpenVEF.** Very high for the existence of an LLM-generated driver/checker pair, offline trace processing, golden validation, and mutation-based testbench evaluation.

**Difference.** AutoBench's primary quality criterion compares the testbench-under-evaluation against the golden testbench on mutants. It does not report OpenVEF's per-artifact `NP` versus `PND` miss composition under a pre-frozen, checker-independent specification mask. Its oracle is not an independent formal specification check in the same sense as OpenVEF's proposed mask.

**Planning implication.** OpenVEF must not describe hybrid driver/checker generation or mutation-based evaluation as novel. It should explain why its outcome classification is different from Eval2 and why the golden testbench is not its evaluation oracle. [Paper and results](https://arxiv.org/abs/2407.03891)

### 3.2 CorrectBench (2024 preprint; DATE 2025): functional self-validation and correction

**Reference:** Qiu et al., “CorrectBench: Automatic Testbench Generation with Functional Self-Correction using LLMs for HDL Design,” arXiv:2411.08510; DATE 2025.  
**Source:** https://arxiv.org/abs/2411.08510

**What it does.** CorrectBench extends AutoBench with a scenario-based validator, an LLM corrector, and an action agent that chooses whether to correct, restart generation, or stop. The validator uses only the natural-language DUT specification. It simulates testbench scenarios against a collection of LLM-generated imperfect RTL implementations and builds an RTL–Scenario matrix to identify scenarios that appear incorrect.

**Reported results.** The paper reports 88.85% average validation accuracy and a 70.13% testbench pass ratio, compared with 52.18% for AutoBench and 33.33% for direct generation. These are framework-specific validation/pass metrics, not directly comparable to OpenVEF's miss-checker share.

**Overlap with OpenVEF.** Strong prior art for specification-only testbench generation, a generated driver/checker workflow, independent evaluation of checker/scenario correctness, and a direct-generation comparator.

**Difference.** Its focus is functional self-validation and repairing generated testbenches, not a repeated, controlled study of where each artifact misses a fixed population of mutants. Its generated imperfect RTL variants serve as a validator for scenarios, not an OpenVEF-style frozen specification mask on paired traces.

**Planning implication.** Avoid claims that a structured generation pipeline or direct-versus-generated comparison is new. State the exact manipulated variable in OpenVEF: prompt organization only, with semantic information, output contract, and resource budget held fixed. [Paper](https://arxiv.org/abs/2411.08510)

### 3.3 ConfiBench (ACM TODAES, 2025): scenario masks and testbench ensembles

**Reference:** Qiu, Zhang, Drechsler, Ho, Schlichtmann, and Li, “ConfiBench: Automatic Testbench Generation with Confidence-Based Scenario Mask and Testbench Ensemble using LLMs for HDL Design,” ACM Transactions on Design Automation of Electronic Systems, DOI 10.1145/3773087.  
**Sources:** https://doi.org/10.1145/3773087 and https://robotik.dfki-bremen.de/de/forschung/publikationen/16691

**What it does.** ConfiBench builds on AutoBench and CorrectBench. It adds a confidence-based **scenario mask** to disable risky generated scenarios and combines multiple testbenches into an ensemble to compensate for the resulting coverage loss. The scenario mask is a confidence/validity mechanism over generated test scenarios.

**Reported results.** It reports a 72.22% testbench pass rate overall, compared with 70.13% for CorrectBench, 52.18% for AutoBench, and 33.33% for direct generation. It reports additional improvements from scenario masking and ensembles, with different effects for large and small LLMs.

**Important terminology distinction.** ConfiBench's scenario mask is **not** OpenVEF's observation mask. ConfiBench masks unreliable test scenarios in the generated testbench. OpenVEF's proposed mask is derived from the design specification before generation and identifies which output signals/cycles count as specification-observable divergence; it is independent of the artifact's checker.

**Overlap with OpenVEF.** Strong prior art for LLM-generated self-checking testbenches, validity gating, masking concepts, and ensembles.

**Difference.** It does not define OpenVEF's checker-independent output-observation boundary or publish the same `NP`/`PND` per-artifact analysis. Its masked entities are test scenarios, not output observations.

**Planning implication.** OpenVEF must explicitly define “observation mask” and distinguish it from scenario masking. [ACM/DFKI record](https://robotik.dfki-bremen.de/de/forschung/publikationen/16691)

### 3.4 GRPO-SMu (2026): mutation-informed test-plan generation and training

**Reference:** Dimple Vijay Kochar et al., “GRPO with State Mutations: Improving LLM-Based Hardware Test Plan Generation,” arXiv:2601.07593.  
**Source:** https://arxiv.org/abs/2601.07593

**What it does.** It separates generation of a structured test plan from rendering/execution of a testbench. The plan-generation model is trained using supervised fine-tuning and a reinforcement-learning approach that diversifies states through mutations. Evaluation uses golden-design pass (M1) and mutation failure/detection rate (M2). The evaluation set includes 500 RTL designs with three mutated variants per design (1,500 variants).

**Important information-boundary point.** In its mutation-informed evaluation/training setup, the test-plan model can receive buggy RTL/mutated code and generate reasoning aimed at distinguishing golden and mutated implementations. That is not the same as OpenVEF's model generating an artifact without access to mutant identities or faulty RTL.

**Reported result.** The GRPO-SMu 7B model reports 33.3% golden pass rate and 13.9% mutation detection rate. These numbers are specific to its task, models, training regime, and denominator.

**Overlap with OpenVEF.** Strong prior art for LLM test-plan generation, a two-stage plan-to-testbench architecture, golden validity gating, and mutation-detection metrics.

**Difference.** It studies model training and mutation-informed test-plan reasoning, not prompt-structure effects on paired driver/checker artifacts under a frozen, checker-independent output mask.

**Planning implication.** OpenVEF must state clearly that generator inputs exclude RTL/mutant identities and that it is measuring independently generated artifacts rather than training a model to target supplied mutants. [Paper](https://arxiv.org/abs/2601.07593)

### 3.5 AssertLLM2 (2026): specification-generated assertions tested against mutated RTL

**Reference:** Yuchao Wu et al., “AssertLLM2: A Comprehensive LLM Benchmark for Assertion Generation from Design Specifications,” arXiv:2605.27472.  
**Source:** https://arxiv.org/abs/2605.27472

**What it does.** AssertLLM2 contains 83 real-world designs across 13 functional categories, structured specifications, golden RTL, and systematically mutated buggy RTL. It evaluates two settings: bug prevention (specification-only SVA generation) and bug hunting (specification plus buggy RTL). Generated assertions are assessed for syntax, formal provability, coverage, and mutation-based bug detection.

**Reported evaluation.** A variant is killed if at least one proven assertion is violated on it. The benchmark therefore provides a large-scale precedent for evaluating LLM-generated checker artifacts with a gold implementation and mutation set.

**Overlap with OpenVEF.** Very high for the checker side: a model generates verification checks from a specification and the checks are measured against mutated designs. It also reinforces the distinction between specification-only generation and bug-hunting with buggy RTL supplied.

**Difference.** AssertLLM2 generates SVAs, not a coupled driver/offline-checker pair. It does not study stimulus generation or the decomposition of misses into no masked divergence versus a divergence accepted by the generated checker.

**Planning implication.** The contribution cannot be “evaluating LLM-generated checkers against mutants.” It would need to be the paired driver-plus-checker population and the carefully defined experimental question. [Paper](https://arxiv.org/abs/2605.27472)

### 3.6 GateTruth (2026): mutation audit of RTL benchmark testbenches

**Reference:** Meet Bhadra, “GateTruth: Auditing the Rigor of RTL Design Benchmarks via Mutation Testing,” arXiv:2608.12635.  
**Source:** https://arxiv.org/abs/2608.12635

**What it does.** GateTruth injects deterministic, seeded semantic mutants into reference RTL designs and measures whether benchmark testbenches kill them. It audits its own reference suite and the external RTLLM v2.0 benchmark. It identifies both weak testbenches and evaluation hazards, including testbench revisions that overfit the mutation gate and token caps that silently alter model rankings.

**Reported external audit.** Under the paper's reported Icarus `-g2012` condition, it evaluates 46 auditable RTLLM designs and 775 mutants; 440 are killed, 320 survive, and 15 are indeterminate. Its pooled kill rate is 56.8%, median per-design kill rate 74.0%, and 72% of designs fall below its proposed 95% floor.

**Direct design overlap.** Its benchmark includes synchronous FIFO and UART transmitter tasks. For its three pilot tasks, it reports 24 valid mutants for the synchronous FIFO and 46 for the UART transmitter in the scaled mutation generator; the UART pilot kill rate is 43/46 (93.48%). Thus FIFO and UART are not, by themselves, novel benchmark choices.

**Overlap with OpenVEF.** Strong prior art for deterministic seeded mutation, evaluating a testbench's actual fault-detection strength, and exposing benchmark/testbench weaknesses.

**Difference.** GateTruth primarily audits testbenches attached to RTL-generation benchmarks; it is not a controlled study of LLM-authored driver/checker artifacts or prompt conditions. Its semantic mutants and benchmark construction differ from OpenVEF's planned Yosys/MCY structural netlist signal mutant population.

**Planning implication.** OpenVEF must justify its fault model, publish the full mutant denominator and indeterminate exclusions, avoid tuning generated artifacts to a public mutation gate, and ensure FIFO/UART benchmarks have original specifications and independent test/fault sets. [Paper](https://arxiv.org/abs/2608.12635)

### 3.7 SecTB-RTL (2026): closest controlled verification-plan study

**Reference:** Hang Xiao, Chuhong Xu, Kainan Zhou, Gangzhen Qian, and Lu Yi, “Trust, but Validate the Instrument: Auditing AI-Generated RTL Verification Plans on Authored Security-Regression Proxies,” arXiv:2609.19844.  
**Sources:** https://arxiv.org/abs/2609.19844 and https://research.google/pubs/trust-but-validate-the-instrument-auditing-ai-generated-rtl-verification-plans-on-authored-security-regression-proxies/

**What it does.** SecTB-RTL uses 31 RTL tasks and 124 authored hardware-security regression mutants. The model emits a constrained JSON stimulus plan; a trusted execution layer renders and runs it. The artifact is checked on the golden design and four hidden mutants. It distinguishes provider/schema acceptance from actual production-semantic validity and preserves all scheduled failures.

**Prompt/experimental design.** It uses four prompt arms (functional objective, equal-attention functional control, abstract security context, and explicit security requirements), three model aliases, five repetitions, randomized complete blocks, and a pre-registered task-level analysis. It planned to compare the explicit-security arm with the equal-attention functional control. The primary statistical unit is the RTL task, not each mutant row.

**Crucial result: the treatment experiment did not yield a valid prompt-effect estimate.** In the 1,860-call follow-up, 1,857 responses were provider-accepted but only nine passed the production semantic validator. The generation-facing response contract and execution reset-state rules disagreed. The authors retained the full failure denominator and reported no prompt-effect estimate. This is a strong methodological warning, not evidence that a particular prompt arm performed better.

**Overlap with OpenVEF.** Very high for LLM-generated stimulus-and-check artifacts, golden validation plus hidden mutants, multiple prompts with repeated generations, matched task information, randomized schedules, task-level statistics, and failure-preserving denominators.

**Difference.** SecTB studies security-oriented plans for existing authored regression proxies; its output is a restricted stimulus-and-assertion DSL, not the exact paired cocotb driver plus independent offline checker in OpenVEF. Its prompt arms vary security information/attention, not merely presentation structure while holding all semantic information fixed. The intended primary study did not achieve an analyzable treatment effect.

**Planning implication.** F16 is essential. OpenVEF must validate the exact persisted artifact through the full execution contract before confirmatory calls. A provider-accepted JSON response, a syntactically valid script, or a compile-pass is not enough. The prompt-organization comparison must also be distinguished from SecTB's content/attention contrast. [Paper and experimental disposition](https://arxiv.org/abs/2609.19844)

### 3.8 LLM-Aided Verification Gap Detection (TechRxiv preprint, February 2026): direct checker-gap overlap

**Reference:** Praveen Kumar Vagala, “LLM-Aided Verification Gap Detection: A Methodology for Identifying Missing Checkers in UVM Testbenches,” TechRxiv preprint, posted 10 February 2026, DOI 10.36227/techrxiv.177069683.39144593/v1.  
**Source:** https://doi.org/10.36227/techrxiv.177069683.39144593/v1

**Publication status.** The manuscript itself identifies TechRxiv e-prints as preliminary reports that are not peer reviewed. It must be treated as an unreviewed preprint, not as established peer-reviewed evidence.

**What it does.** The method runs the same existing UVM testbench and test suite on golden and mutated RTL. If output values differ while both golden and variant tests pass, it declares a verification gap. An LLM then analyzes the specification, differential evidence, coverage and integration constraints to suggest a missing checker; the suggested checker is reviewed and validated by an engineer. The mutation operators are manually injected RTL edits, including arithmetic, relational, logical, value, boundary and bitwise changes.

**Important observation-boundary nuance.** The paper's own Definition of Output Observability says an output is observable when at least one checker validates it; the gap is the set of outputs not covered by any checker (Section II-A, around the definition at PDF page 2). Thus its checker-gap predicate is not simply a checker-independent specification mask over all top-level outputs. It is explicitly checker-domain-dependent. Under OpenVEF, by contrast, a top-level output divergence that satisfies the frozen specification mask is classified as exposed even when the generated checker does not monitor that output; if that checker returns PASS, it is PND. The same concrete event may therefore be labelled differently depending on the propagation boundary.

**Reported proof of concept (unverified).** An earlier draft attributed a synchronous-FIFO case and numerical results to this preprint. Those details are not verified from its text (abstract-only access, File 22) and are not relied upon. The preprint is not peer reviewed.

**Overlap with OpenVEF.** This is the closest conceptual match to the checker-gap predicate: mutation-induced output divergence plus a passing existing testbench is used to identify missing checks. OpenVEF cannot claim that this basic differential-simulation checker-gap concept is new.

**Difference.** The paper studies an existing UVM testbench and asks an LLM to discover/add missing checkers. OpenVEF's proposed population is newly LLM-authored driver/checker pairs; its question is how those artifacts behave under controlled prompt formats and repeated samples, not how to repair an established UVM suite. OpenVEF's checker-independent specification mask also defines exposure differently from the preprint's checker-dependent definition of output observability. That difference is real but requires justification and sensitivity analysis; it is not by itself evidence of novelty.

**Planning implication.** This preprint must be cited in the related-work section and explicitly distinguished. OpenVEF must not claim a novel LLM-aided method for discovering checker gaps through mutation-induced divergence. Its unreviewed status affects evidentiary weight, but not whether the conceptual overlap must be disclosed. [TechRxiv preprint](https://doi.org/10.36227/techrxiv.177069683.39144593/v1)

### 3.9 From FIPS to FPGA with LLM Agents (November 2026): netlist-mutant gates and specification-derived tests

**Reference:** Jungmin Park, Eunha Kim, Wooseop Kim, Seongjoon Cho, and Byungho Cha, “From FIPS to FPGA with LLM Agents: Measuring What Tests and Reviews Miss in Post-Quantum Cryptographic Hardware,” arXiv:2611.25339, submitted 19 November 2026.  
**Source:** https://arxiv.org/abs/2611.25339

**What it does.** The paper reports an LLM-agent-assisted post-quantum accelerator port and a verification-gated workflow. Each gate is required to pass on real code and fail on a negative control and mutants. It uses tool-selected netlist mutants to audit existing simulation gates, and specification-derived tests guided by surviving mutants.

**Reported result.** Across three RTL modules, the first mutant draw contains 399 tool-selected netlist mutants and existing gates kill 76%. A fresh draw of 150 yields 70.7% existing-gate kills; additional specification-derived tests raise the fresh-draw decapsulation kill rate from 48% to 74%. The paper notes a timeout counts as a kill in its reported gate metric, so this denominator and outcome semantics must not be equated with OpenVEF's rules.

**Overlap with OpenVEF.** Very recent prior art using netlist mutants, specification-derived tests, negative controls, and mutation-gate audits in an LLM-assisted hardware workflow.

**Difference.** It is a deployed PQC accelerator case study with modules, board tests, conformance vectors, and agentic review. It does not present an independently sampled population of LLM-generated driver/offline-checker pairs or a matched prompt-structure experiment with OpenVEF's `NP`/`PND` mask-based estimand.

**Planning implication.** OpenVEF should not claim to be the first use of netlist mutants to audit tests in an LLM-assisted hardware project. Its structural mutant population and outcome semantics must be fully documented; comparisons to this paper's kill rates are invalid because the gates, denominator, timeouts, and engineering setting differ. [Paper](https://arxiv.org/abs/2611.25339)

### 3.10 LLM4DV (FCCM 2025): prompt optimization for test stimulus generation

**Reference:** Zixi Zhang et al., “LLM4DV: Using Large Language Models for Hardware Test Stimuli Generation,” IEEE FCCM 2025, DOI 10.1109/FCCM62733.2025.00048.  
**Source:** https://doi.org/10.1109/FCCM62733.2025.00048

The paper presents an open-source benchmarking framework for LLM-based hardware test-stimulus generation and evaluates six LLMs, six prompting improvements, and eight hardware designs. It is stimulus-focused and does not, from the accessible abstract/record, establish OpenVEF's offline-checker miss classification. It does mean that prompt improvements and multi-model comparisons in hardware verification are not new as broad research themes.

**Planning implication.** OpenVEF's prompt experiment must be narrowly defined as a matched-content prompt-structure manipulation, not generic “prompt engineering for hardware verification.” Full-text method details remain to be checked in the independent audit. [IEEE record](https://doi.org/10.1109/FCCM62733.2025.00048)

### 3.11 VerifLLMBench (DVCon 2025): UVM testbench generation benchmark

**Reference:** Nishanth Somashekara Murthy, Eldon Nelson, Sachin S. Sapatnekar, and John Sartori, “VerifLLMBench: An Open-Source Benchmark for Testbenches Generated with Large Language Models,” DVCon U.S. 2025.  
**Source:** https://people.ece.umn.edu/users/jsartori/papers/dvcon25.pdf

VerifLLMBench benchmarks LLM-generated UVM testbenches using verified DUTs, iterative prompt refinement for syntax, build success, coverage analysis, and UVM lint. The paper describes the challenge of generating robust testbenches but does not report mutant-based bug-detection or an `NP`/`PND` split. It is a relevant benchmark precedent, not a direct match to OpenVEF's outcome model.

### 3.12 Independent Data-Integrity Verification for LLM-Driven Functional Coverage Closure (2026)

**Reference:** Venkata Krishna Kumar Vedantam, “Independent Data-Integrity Verification for LLM-Driven Functional Coverage Closure in Hardware Design,” arXiv:2610.21570.  
**Source:** https://arxiv.org/abs/2610.21570

The work uses an LLM agent to improve functional coverage on an asynchronous FIFO, UART transmitter, and AHB2APB bridge, while a separate scoreboard checks data integrity. The author explicitly notes that the independent monitor is not yet attached to the LLM-generated tests and that one manual FIFO check is preliminary; reported weaknesses include no baseline, no ablation, three designs, and logs from multiple agent checkpoints. It reinforces that coverage is not the same as checking data correctness, but its current evidence does not establish mutation-based artifact qualification.

### 3.13 Software-side caution: mutation score is not automatically real-bug effectiveness

**Reference:** Junda Zhao, Shurui Zhou, and Eldan Cohen, “Do Coverage and Mutation Scores of LLM-Generated Test Suites Correlate with Their Effectiveness? (Replicability Study),” PACMSE/ISSTA 2026, DOI 10.1145/3832093.  
**Source:** https://arxiv.org/abs/2607.22880

This is software-testing research, not hardware verification. It finds that the usefulness of coverage and mutation scores is context-dependent: they can be informative in regression settings where code supplied to the LLM is presumed correct, but become unreliable in some settings where the code under test may itself be buggy. It is a warning against treating a mutation score as a universal proxy for real-world defect detection. It supports cautious, fault-population-specific conclusions in OpenVEF; it does not directly answer the hardware research question.

### 3.14 HAVEN (2026): template-mediated UVM generation and coverage closure

**Reference:** Chang-Chih Meng, Yu-Ren Lu, Guan-Yu Lin, Tsung Tai Yeh, Kai-Chiang Wu, and I-Chen Wu, “HAVEN: Hybrid Automated Verification ENgine for UVM Testbench Synthesis with LLMs,” arXiv:2604.27643.  
**Source:** https://arxiv.org/abs/2604.27643

**What it does.** HAVEN uses LLM agents to translate specifications into a structured architecture blueprint, then a deterministic Jinja2 template engine emits UVM components. Its Protocol-Aware Sequence DSL mediates sequence generation; pre-defined patterns establish baseline coverage, and LLM agents analyze coverage reports to add targeted sequences. It is explicitly designed to avoid asking the LLM to directly emit all raw HDL components.

**Reported results.** The abstract reports 19 open-source IP designs over Direct, Wishbone and AXI4-Lite interfaces, 100% compilation success, 90.6% code coverage and 87.9% functional coverage on average. These are coverage/build metrics, not a mutation-based miss-composition result.

**Overlap.** Strong prior art for specification-driven LLM-assisted UVM artifact generation and coverage-guided iterative sequence closure.

**Difference.** The LLM primarily emits structured plans/DSL and deterministic templates render UVM. The accessible paper record does not report the OpenVEF-style repeated, independently sampled driver/offline-checker artifact study or a per-artifact NP/PND classification.

**Planning implication.** OpenVEF should not claim first LLM-generated UVM/testbench or first structured artifact-generation pipeline. HAVEN is a useful example of constrained generation through a trusted intermediate representation. [Paper](https://arxiv.org/abs/2604.27643)

### 3.15 PRO-V (2025): multi-agent testbench generation, mutant evaluation and error triage

**Reference:** Yujie Zhao et al., “PRO-V: An Efficient Program Generation Multi-Agent System for Automatic RTL Verification,” arXiv:2506.12200.  
**Source:** https://arxiv.org/abs/2506.12200

**What it does.** PRO-V uses program-generation agents, inference-time best-of-n sampling for functional models and stimulus, and an LLM-as-judge enhancement that converts compiler/static-analysis information into natural-language feedback to help distinguish RTL faults from testbench errors.

**Evaluation.** The paper uses 156 HDLBits-derived Verilog problems. Its Eval1 checks functional correctness on golden RTL. Its Eval2-alpha evaluates agreement with golden-testbench reports over LLM-generated RTL mutants; the mutant population is imbalanced (82% incorrect DUTs, 18% correct DUTs). The paper reports 87.17% golden-Rtl verification accuracy and 76.28% total Eval2-100% for PRO-V, versus 78.85% and 55.77% for CorrectBench in its table.

**Overlap.** High for generated verification workflows, generated testbench artifacts, mutation-based evaluation, golden validity, and LLM-assisted discrimination of failures.

**Difference.** Its endpoint is verification accuracy / agreement with golden reports, not a per-artifact decomposition of no masked divergence versus masked divergence accepted by that artifact's checker. Its LLM judge is used to triage whether simulation/verification errors are from DUT or testbench; it is not a frozen independent specification observation mask.

**Planning implication.** PRO-V is another reason not to claim that mutant testing, golden controls, generated testbench validation, or LLM-assisted fault/testbench triage is new. [Paper](https://arxiv.org/abs/2506.12200)

### 3.16 CovR (MLCAD 2026): coverage-optimized stimuli plus mutation detection

**Reference:** Manar Abdelatty, Maryam Nouh, and Sherief Reda, “CovR: Coverage-Aware Hardware Verification via Reasoning-Guided Reinforcement Learning,” MLCAD 2026, DOI 10.1145/3831599.3840347; arXiv:2609.19189.  
**Source:** https://arxiv.org/abs/2609.19189

**What it does.** CovR trains and deploys a reasoning-guided stimulus-generation model inside an agentic self-refinement pipeline, using simulation and coverage feedback. It can be plugged into broader verification workflows as a stimulus engine.

**Reported results and important interpretation.** It reports improved coverage by 18.95% and mutation detection score by 1.19% in integrated workflows. The abstract says it revealed 4.46% more undetected failures. The detailed evaluation clarifies that replacing the native stimulus generator lowered Eval1 by 4.46%, indicating that broader stimulus exposed latent bugs in the functional reference model (FRM), not necessarily 4.46% additional DUT mutant escapes. OpenVEF must not paraphrase this as a percentage of checker escapes without checking the exact metric/denominator.

**Overlap.** High for LLM-generated stimulus, coverage-guided refinement, mutation detection, and exposing reference-model/test-oracle defects.

**Difference.** CovR is principally a stimulus optimization and training contribution; its plug-in evaluation does not provide OpenVEF's per-artifact NP/PND decomposition or a separately sampled LLM-authored offline checker as the unit.

**Planning implication.** CovR strengthens the case for recording both stimulus exposure and oracle validity. A checker-gap metric must not assume the reference model is infallible. [Paper](https://arxiv.org/abs/2609.19189)

### 3.17 DeepAssert (2025): internal, specification-derived assertion generation

**Reference:** Yonghao Wang et al., “DeepAssert: An LLM-Aided Verification Framework with Fine-Grained Assertion Generation for Modules with Extracted Module Specifications,” arXiv:2509.14668.  
**Source:** https://arxiv.org/abs/2509.14668

**What it does.** DeepAssert extracts module relationships and module-level specifications from RTL hierarchy and a top-level specification, then generates fine-grained internal assertions for module signals. It targets the limitations of top-level-only specifications and assertion sets.

**Overlap.** Adjacent prior art for LLM-generated checkers/assertions and for the fact that top-level observation can miss internal behavior.

**Difference.** It focuses on internal SVA generation and localization, rather than a complete stimulus-driver/offline-checker artifact cohort and matched prompt-format experiment. It is still relevant to OpenVEF's deliberate top-level-only observation boundary: OpenVEF must frame that as a scope restriction, not a universally complete verification view. [Paper](https://arxiv.org/abs/2509.14668)

## 4. Cross-paper conclusions

### 4.1 What is already established

| Candidate claim | Status after Step 3 | Evidence |
|---|---|---|
| LLMs can generate a hybrid hardware driver and checker | Established | AutoBench and successors |
| Generated testbenches can be checked on golden RTL and mutants | Established | AutoBench, GRPO-SMu, SecTB-RTL, GateTruth |
| A generated checker can be validated or corrected | Established | CorrectBench, ConfiBench, AssertLLM2 |
| LLM-generated assertions can be scored on mutated RTL | Established | AssertLLM2 |
| Mutation-induced output divergence with passing tests reveals a checker gap | Already explicitly proposed in a TechRxiv preprint; also related to Verify the Verifier | Vagala preprint, Verify the Verifier |
| Direct or prompting-improvement comparisons exist in LLM hardware verification | Established broadly | AutoBench baselines, CorrectBench, LLM4DV, SecTB-RTL prompt arms |
| Repeated prompt-arm study with randomized blocks and task-level inference exists | Yes, but its intended treatment run failed calibration | SecTB-RTL |
| Mutation testing has been used to audit RTL benchmark testbench rigor | Established | GateTruth |
| Netlist-mutant gates appear in recent LLM-assisted hardware projects | Established | From FIPS to FPGA |
| The exact OpenVEF combination (LLM-authored driver/checker unit, same-information prompt-format factor, fixed checker-independent spec-output mask, artifact-level miss composition) has been found in the reviewed primary sources | Not found in sources reviewed; not a novelty proof | Comparative assessment in this report |

### 4.2 What is not established by these comparisons

The reported rates across these papers must not be compared numerically. They vary in artifact population, task, model, exposure definition, fault operator, denominator, use of a golden testbench, timeout handling, equivalence filtering, and unit of analysis. For example:

- AutoBench Eval2 is agreement with a golden testbench, not an independent spec-mask divergence measure.
- AssertLLM2's bug-kill ratio is based on proven SVAs and buggy RTL variants, not a driver/checker artifact.
- GateTruth audits benchmark testbenches and uses seeded semantic mutants.
- SecTB-RTL's primary prompt effect was not estimable because the production semantic validator accepted only 9/1,860 calls.
- The TechRxiv preprint is an unreviewed proof of concept; its numerical results and designs are not verified from its text (File 22) and are not relied upon.
- From FIPS to FPGA counts timeout as a kill and is a hardware deployment case study.

### 4.3 OpenVEF's observation mask is a specific construct

Three similarly named ideas must not be conflated:

1. **ConfiBench scenario mask:** selectively disables risky generated test scenarios based on their confidence/validity.
2. **Certitude-style checker propagation boundary:** whether a fault effect reaches a checker's observation domain.
3. **OpenVEF specification observation mask:** a checker-independent, pre-frozen predicate over top-level outputs/cycles, derived from a design specification, that determines which trace differences count as specification-observable divergence.

The proposed OpenVEF mask is a methodological boundary choice. It is not simply “a mask like ConfiBench,” and its correctness depends on a trustworthy, unambiguous specification and reviewed predicates.

## 5. OpenVEF comparison: candidate distinction and remaining risks

### 5.1 Potentially distinguishing combination (not a novelty finding)

A defensible candidate framing is the combination of:

1. **Population:** newly LLM-authored deterministic driver plus offline checker, treated as one artifact and sampled repeatedly;
2. **Information boundary:** generation receives a versioned specification, interface/port manifest, observation mask and execution contract, but no RTL implementation, mutation identity, mutation output, or mutant run feedback;
3. **Prompt factor:** prompt presentation-order organization while preserving all semantic information and output constraints;
4. **Exposure definition:** paired null-netlist/mutant traces and a fixed checker-independent specification mask;
5. **Outcome granularity:** per-artifact reporting of `NP`, `PND`, `DETECTED`, invalid pairs, errors, timeouts and anomalies, alongside raw-divergence diagnostics;
6. **Fault population:** an explicitly bounded structural post-synthesis netlist-signal mutant population, with claims restricted to that population;
7. **Reproducibility:** frozen prompts, seeds, toolchain, masks, mutant hashes, artifact hashes, trace data and pre-registered analysis.

Every element has precedents or close analogues. The research contribution, if any, would be the empirical study of this exact combination—not a new mutation framework, a new A/P/D decomposition, a new LLM testbench generator, or a new checker-gap detection method.

### 5.2 A serious interpretation issue: the primary share is descriptive, not causal

The v0.5 primary metric is `PND_i / (NP_i + PND_i)`. It answers: **among the missed pairs for this artifact, what fraction had a masked output divergence that its checker accepted?**

It does not, on its own, estimate a causal or independent “checker quality” parameter. ORG-A and ORG-B presentation orders can change both driver behavior and checker behavior. A change in the composition of missed pairs may therefore occur even if checker quality itself is unchanged. The protocol already calls for companion rates `NP/N`, `PND/N`, and `DETECTED/N`; the secondary `checker_gap = PND/(DETECTED + PND)` conditions on masked exposures. These improve interpretation but do not fully isolate drivers from checkers.

Before freezing, consider whether a crossed driver–checker experiment is feasible: run each eligible driver's traces against a common set of checkers, or cross drivers and checkers across artifacts within design/condition. This would estimate driver and checker effects more directly, but increases experimental complexity and requires a well-defined compatibility contract. If the project retains the current design, describe the primary share strictly as **miss composition**, not causal attribution or a standalone checker-quality score.

### 5.3 Fault-model risk

OpenVEF's present MVP uses Yosys/MCY post-synthesis netlist signal mutants. GateTruth and From FIPS to FPGA show that netlist-level mutation is being used in current hardware-verification studies; nevertheless, these mutants are not equivalent to source-level design errors, realistic RTL bug distributions, or manufacturing stuck-at fault populations by default. The paper must identify exact mutation modes and equivalence/observability filters on the pinned tool version. It must not claim broad design-bug detection based solely on signal-level mutations.

A source-level semantic mutant population could be considered as a separate fault model, but it should not be casually added to the MVP. It increases scope and requires its own operators, legality checks, equivalence proof, and denominators.

### 5.4 Benchmark overlap risk

GateTruth already includes synchronous FIFO and UART transmitter tasks; whether the TechRxiv checker-gap preprint also evaluates a synchronous FIFO is not verified (File 22); SecTB-RTL includes sequential security regression tasks. Reusing common design *types* is not automatically disqualifying, but OpenVEF must use independently written, fully specified designs/parameters and an independently frozen fault population. The exact benchmark artifacts, specs, masks and mutants must be original or reused with explicit permission and source attribution. Avoid presenting “FIFO + UART” as a novel benchmark selection.

### 5.5 Feasibility and validity risk

SecTB-RTL demonstrates that high provider/schema acceptance can coexist with almost total failure at the actual semantic execution boundary. OpenVEF's F16 pilot should therefore test the full persisted artifact, not just JSON syntax, parser acceptance or compilation. The pilot must be outcome-blind, separate from confirmatory sampling, and used to estimate whether the planned sample size can be achieved under the exact production contract.

## 6. Step 3 decision and recommendation

**Decision: CONDITIONAL GO; candidate contribution narrowed; no final novelty claim.**

Proceed to Step 4 only after an independent audit resolves these four decisions:

1. Is the current primary research question genuinely differentiated from the TechRxiv checker-gap method, SecTB-RTL and the related benchmark literature once their artifact populations and units of analysis are stated precisely?
2. Is `PND/(NP+PND)` intended only as descriptive miss composition, or should the design add a crossed driver–checker experiment to support component-level attribution?
3. Is the post-synthesis netlist-signal mutant population sufficiently aligned with the scientific claim, or does it force OpenVEF to narrow its conclusions to structural signal faults?
4. Do prompt arms differ only in organization while preserving information, or does any content/attention difference remain? If so, the independent variable must be renamed and the interpretation revised.

Do not rewrite the Charter or Experimental Protocol as frozen v1.0 yet. Keep v0.5 as the current source of truth, with this Step 3 review attached as a provisional related-work assessment.

## 7. Source-access and confidence log

| Source | Access in this review | Confidence / limitation |
|---|---|---|
| AutoBench | arXiv HTML text, including methodology and evaluation definitions | High for the reviewed sections |
| CorrectBench | arXiv HTML text, including validator and correction workflow | High for the reviewed sections |
| ConfiBench | Extracted full PDF text via university repository; DOI/ACM bibliographic details checked | Text reviewed; screenshot page-image requests failed (429/timeouts), so no visual page inspection |
| GRPO-SMu | arXiv HTML text, including generation, mutation and reward definitions | High for the reviewed sections |
| AssertLLM2 | arXiv HTML text, including benchmark construction and metrics | High for the reviewed sections |
| GateTruth | arXiv HTML text, including test suite, mutation audit and limitations | High for the reviewed sections |
| SecTB-RTL | arXiv HTML text plus Google Research publication page | High for the accessible paper text; confirm version and publication venue before final bibliography |
| LLM-Aided Verification Gap Detection | Abstract only, per File 22; the earlier statement that extracted full text was read is superseded | Low for method and limitations until the exact PDF is retrieved and inspected; unreviewed preprint; disclose as prior art |
| From FIPS to FPGA | arXiv HTML text | High for abstract, gates, netlist-mutant findings and reported denominator; full deployment details are beyond this review |
| LLM4DV | IEEE Xplore abstract/metadata | Limited; full method details not independently reviewed |
| VerifLLMBench | Extracted PDF text from author-hosted copy | Moderate; page-image screenshot attempts timed out; venue is DVCon 2025 |
| Independent Data-Integrity Verification | arXiv/alphaXiv abstract and metadata | Limited; preprint abstract only in this pass |
| Mutation-score replication study | arXiv HTML text | High for its software-testing result; adjacent, not hardware evidence |
| LLM-integrated verification survey | arXiv HTML text | High for taxonomy/scope; survey, not a primary empirical result |
| HAVEN | arXiv HTML text, including architecture and abstract-level experimental results | High for accessible text; no claim of mutant-based evaluation beyond what the paper reports |
| PRO-V | arXiv HTML text, including generation pipeline and evaluation criteria | High for accessible text; golden-report agreement must not be confused with a checker-independent mask |
| CovR | arXiv HTML text, including integrated workflow and Eval0/Eval1/Eval2 interpretation | High for accessible text; 4.46% is a functional-reference-model failure signal in the described integration, not a DUT checker-gap percentage |
| DeepAssert | arXiv HTML text, including internal assertion generation and experimental metrics | High for accessible text; assertion-only adjacent work |

This is a targeted literature review, not a systematic review. Native IEEE Xplore and ACM Digital Library full-text searches, paywalled proceedings, and workshop program archives were not comprehensively searched. Accordingly, the correct wording is **“not found in the sources reviewed”**, never “no one has done this.”

## 8. Selected bibliography

1. Qiu et al., AutoBench, arXiv:2407.03891, https://arxiv.org/abs/2407.03891.
2. Qiu et al., CorrectBench, arXiv:2411.08510; DATE 2025, https://arxiv.org/abs/2411.08510.
3. Qiu et al., ConfiBench, ACM TODAES, DOI:10.1145/3773087, https://doi.org/10.1145/3773087.
4. Kochar et al., GRPO-SMu, arXiv:2601.07593, https://arxiv.org/abs/2601.07593.
5. Wu et al., AssertLLM2, arXiv:2605.27472, https://arxiv.org/abs/2605.27472.
6. Bhadra, GateTruth, arXiv:2608.12635, https://arxiv.org/abs/2608.12635.
7. Xiao et al., SecTB-RTL, arXiv:2609.19844, https://arxiv.org/abs/2609.19844.
8. Vagala, LLM-Aided Verification Gap Detection, TechRxiv, DOI:10.36227/techrxiv.177069683.39144593/v1, https://doi.org/10.36227/techrxiv.177069683.39144593/v1.
9. Park et al., From FIPS to FPGA with LLM Agents, arXiv:2611.25339, https://arxiv.org/abs/2611.25339.
10. Zhang et al., LLM4DV, IEEE FCCM 2025, DOI:10.1109/FCCM62733.2025.00048, https://doi.org/10.1109/FCCM62733.2025.00048.
11. Murthy et al., VerifLLMBench, DVCon U.S. 2025, https://people.ece.umn.edu/users/jsartori/papers/dvcon25.pdf.
12. Vedantam, Independent Data-Integrity Verification for LLM-Driven Functional Coverage Closure, arXiv:2610.21570, https://arxiv.org/abs/2610.21570.
13. Zhao, Zhou & Cohen, Coverage and Mutation Scores of LLM-Generated Test Suites, arXiv:2607.22880 / PACMSE ISSTA 2026, https://arxiv.org/abs/2607.22880.
14. Zheng et al., A Survey on LLM-Integrated Hardware Design Verification, arXiv:2610.10580, https://arxiv.org/abs/2610.10580.
15. Sanchez Villalobos et al., Verify the Verifier, arXiv:2611.26588, https://arxiv.org/abs/2611.26588 (Step 1 analysis in the OpenVEF pack).
16. Meng et al., HAVEN, arXiv:2604.27643, https://arxiv.org/abs/2604.27643.
17. Zhao et al., PRO-V, arXiv:2506.12200, https://arxiv.org/abs/2506.12200.
18. Abdelatty, Nouh & Reda, CovR, MLCAD 2026, DOI:10.1145/3831599.3840347, https://arxiv.org/abs/2609.19189.
19. Wang et al., DeepAssert, arXiv:2509.14668, https://arxiv.org/abs/2509.14668.

---

**v1.3.7 CANDIDATE, not audited.** This file is OpenVEF Planning v1.3.6 with only the corrections listed for it in `CHANGELOG-v1.3.7-candidate.md` (owner decision D-024). It is not part of any released, audited or approved pack; v1.3.6 remains the default.
