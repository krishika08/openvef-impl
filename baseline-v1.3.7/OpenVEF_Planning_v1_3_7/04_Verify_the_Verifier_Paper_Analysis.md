> **Historical planning note:** this analysis predates the v0.7 decision to use ORG-A/ORG-B whole-block presentation-order-only prompts. Any direct-versus-structured wording below describes an earlier candidate factor and is superseded by the v0.7 Charter and Protocol.

# OpenVEF Research Foundation — Paper Analysis 01 (Revision 0.2)

## *Verify the Verifier: Specification-Grounded LLM Cross-Checking for Bugs That Escape UVM Scoreboards*

**Authors:** Ana E. Sanchez Villalobos, Michael D. Quinn, Aakash Tyagi, Minh D. Luu, David Kebo Houngninou  
**Affiliation:** Texas A&M University  
**Source:** arXiv:2611.26588v1  
**Submitted:** 19 November 2026  
**Review date:** 22 November 2026  
**Review basis:** Full extracted paper text from a PDF mirror was examined. The original arXiv endpoint rate-limited direct retrieval, and PDF page-image screenshots could not be fetched during this review. Accordingly, this revision does **not** claim that every PDF page image was visually inspected. Numeric and methodological claims below were checked against the extracted paper text and its section/table/figure labels.

---

## 1. Executive summary

*Verify the Verifier* studies bugs that survive a passing UVM regression while violating a specification requirement that the existing scoreboard does not check correctly. The authors call these **scoreboard escapes**. Their framework re-examines passing regression traces using an LLM Anomaly Cross-Checker (ACC), generates SystemVerilog assertions around reported anomalies, qualifies those assertions with formal verification, and attempts to reproduce formal counterexamples as directed UVM tests.

The benchmark starts with at least 564 injected bugs. Of these, 241 pass every regression test. After deduplication, equivalence, activation and miscellaneous exclusions, 68 candidate escapes are evaluated. The framework confirms 41 with at least one qualified assertion; 36 of those 41 are also reproduced by directed UVM tests while the original scoreboard reports PASS.

**Important correction to the earlier analysis:** the paper already contains a stimulus/checker-related decomposition for existing human-written regressions. Its benchmark funnel separates 48 non-activated mutants from 68 activated-but-still-passing candidates after filtering. It also attributes the framework's 27 undetected candidates across two stages: 13 were not observed by the ACC, while 14 had a correct ACC anomaly report but no qualified assertion emerged from the Generator/formal stage. Therefore, “separating stimulus misses from checker misses” or “attributing missed faults” is **not by itself** a defensible OpenVEF novelty claim.

The candidate OpenVEF distinction must be narrower: its study population is newly LLM-authored driver-and-checker pairs; it proposes a controlled direct-versus-structured prompt comparison while keeping design information fixed; and it measures miss composition per artifact against a pre-frozen, specification-derived observation mask. This combination remains only a **candidate contribution** until the broader literature review is complete.

## 2. Research objective and claims

A passing UVM scoreboard result establishes only that the monitored behaviour agrees with the scoreboard's reference model for the tested stimulus and checks. It does not establish full specification compliance. The paper's example of the PATTGEN scoreboard is instructive: it checks serialized data bits but not clock-divider timing or idle output levels.

The paper defines a **scoreboard escape** as a bug for which every test in the regression passes, without UVM_ERROR or UVM_FATAL reports, while the design still violates a specification requirement that the scoreboard does not check or checks incorrectly.

The authors identify two central challenges:

1. **Observability:** the escape must appear in the available trace; scoreboard monitors may not capture the relevant behaviour.
2. **Trust:** a failing LLM-generated assertion is not automatically a valid detection. It may be incorrect or vacuous and must be qualified independently.

### Authors' stated contribution and priority claim

The authors state, “to our knowledge,” that this is the first framework to use an LLM to cross-check passing regression traces against the specification and formally qualify each scoreboard escape. This is the authors' scoped priority claim, not an independently established priority fact.

The paper lists four principal contributions: a problem formulation and qualified-detection criterion; the ACC, which examines a signal digest without RTL access; an assertion/formal/reproduction pipeline; and a benchmark of 68 candidate scoreboard escapes across four OpenTitan IPs.

The paper does **not** claim to introduce mutation-based testbench qualification or to grade testbench quality. It explicitly contrasts its use case with Certitude: Certitude grades a testbench by injecting faults and rerunning the regression for each fault, whereas this paper examines passing regression traces and uses the resulting assertions to identify and help harden the testbench. The paper positions its own goal as framework demonstration rather than a broad testbench-grading study.

## 3. Framework workflow

The framework starts with a passing regression, specification, RTL, UVM environment and coverage results. It has three LLM components—the ACC, assertion Generator and Adversarial Challenger—and deterministic/tool-based stages.

### Stage 1 — Select and observe existing tests

Tests are selected using per-test coverage: a test is selected if it covers a coverage item no other test covers, or exercises a region with remaining coverage holes. Selected tests are rerun at their original seeds with waveform dumping enabled.

The resulting **signal digest** includes every signal of the target module, including internal signals, sampled at every rising clock edge. The representation compresses repeated values, counters and short patterns. The authors state that decoding is checked against the original waveform signal by signal and cycle by cycle. PWM's smoke test alone includes 51,000 cycles of 389 signals.

### Stage 2 — Anomaly Cross-Checker (ACC)

The ACC receives the specification and signal digest. It does **not** receive the RTL, reference design, retrieval system or external tools. It reports the signal, test, relevant requirement, observed behaviour and discrepancy for each possible anomaly.

The prompt asks which behaviours in the trace do not match the specification, rather than whether the behaviour is legal. The authors argue that the latter phrasing can encourage the model to rationalise an anomaly away.

The ACC gets up to three attempts and keeps the **first non-empty result**; attempts are not merged. If all three attempts produce no anomaly, the Generator still runs without an anomaly report. If the Generator then produces no assertion, the mutant is counted as not detected.

### Stage 3 — Assertion generation and deterministic guards

The Generator receives the specification, ACC anomaly report, RTL interface declarations (names, widths and directions, without logic), and a deterministic RTL excerpt around the anomalous signals. The excerpt is intended to provide structural context, not the expected behaviour or mutation location. The assertion's required behaviour must come from the specification.

Deterministic guards validate identifiers and remove or repair malformed constructs. Assertions are bound to the DUT without modifying the RTL.

### Stage 4 — Formal qualification

JasperGold classifies each assertion as proven, counterexample (cex), or undetermined. A cover property checks whether the assertion antecedent can be reached and exposes vacuity.

An assertion is **qualified** only when all three conditions hold:

1. It has a counterexample on the mutant.
2. It is proven on the reference RTL.
3. Its antecedent cover is reached on the reference RTL.

A counterexample on the reference RTL is a **false positive**. An assertion that is vacuous, undetermined, or proven on both mutant and reference is classified as **other**, not as a false positive.

The reference RTL is an evaluation instrument because the benchmark uses injected bugs. The paper says a deployed setting does not have a known bug-free reference; a failing assertion would therefore go to an engineer for review.

### Stage 5 — Counterexample reproduction

The Adversarial Challenger converts a formal counterexample into a directed UVM sequence using the existing testbench's sequences and register-access tasks. The new test starts from reset and runs in the native environment. A formal detection remains a detection even if the existing sequences cannot reproduce it; reproduction is an additional confirmation.

## 4. Experimental setup and benchmark construction

### Designs and verification environments

The paper evaluates four OpenTitan IPs at tag `earlgrey_1.0.0`:

- PWM — Pulse-Width Modulator;
- PATTGEN — Pattern Generator;
- SPI Host;
- CSRNG — Cryptographically Secure Random Number Generator.

The authors use the native UVM environments without modification, through OpenTitan `dvsim` and Cadence Xcelium. The functional test counts are 4 for PWM, 5 for PATTGEN, 12 for SPI Host and 5 for CSRNG. Shared register, alert and bus-integrity tests are excluded. SPI Host's `status_stall` test is also excluded because it fails on the unmodified reference at the fixed seed.

The specifications are OpenTitan's own IP documentation, concatenated without adding or correcting clauses. The target RTL modules contain 655 lines for PWM documentation, 424 for PATTGEN, 2,076 for SPI Host and 1,602 for CSRNG. The authors retain documentation as written even where it disagrees with RTL.

### Mutant generation and filters

BugGen inserts one LLM-written, single-line mutation per run into a functional RTL region, using GPT-4o-mini. The authors invert BugGen's acceptance rule: a mutant that compiles and passes the complete regression is retained as an escape candidate; one that fails a test is set aside because the regression already detects it.

The passing mutants then go through:

1. **Deduplication:** merge identical mutants and width-equivalent operator variants.
2. **Equivalence:** compare reference and mutant in JasperGold under the same clock, reset and inputs. This is an **unbounded proof over reachable states**, not bounded model checking. Counterexamples establish non-equivalence; mutants proven equivalent are removed; undetermined cases are excluded.
3. **Activation:** simulate reference and mutant under the regression and compare traces. There is a wording ambiguity: Section III defines non-activation by every **output** matching on every cycle, while Section V-B describes the activation check as a signal-by-signal trace comparison. Whether internal signals count in that filter is unresolved from the text and should not be stated as settled.

A further **miscellaneous** bucket excludes mutants that cannot be processed, for example because they do not elaborate in JasperGold, leave an output undriven, reside in a submodule where the checker cannot bind, or produce traces exceeding the LLM context window.

### Table I — Benchmark construction

The counts below are directly present in Table I of the paper's extracted text. They are not inferred only from arithmetic.

| Benchmark stage | PWM | PATTGEN | SPI Host | CSRNG | Total |
|---|---:|---:|---:|---:|---:|
| Bugs inserted (at least) | 62 | 124 | 60 | 318 | 564 |
| Passed all regression tests | 46 | 84 | 50 | 61 | 241 |
| Removed: duplicate | 3 | 33 | 10 | 4 | 50 |
| Removed: equivalent | 4 | 7 | 14 | 9 | 34 |
| Removed: undetermined | 3 | 3 | 0 | 19 | 25 |
| Removed: not activated | 2 | 22 | 10 | 14 | 48 |
| Removed: miscellaneous | 10 | 3 | 0 | 3 | 16 |
| Evaluated candidate escapes | 24 | 16 | 16 | 12 | 68 |
| Confirmed by the framework | 15 | 8 | 14 | 4 | 41 |

The 241 regression survivors split into a **not-activated group (48)** and an **activated-but-still-passing group (68)** after the reported filters. The 68 are called *candidate escapes*, not confirmed specification violations: a changed trace and passing scoreboard do not alone prove that a stated requirement was violated. A qualified assertion is needed. The paper says 41 are confirmed, so 41/68 is a lower bound on the true detection rate; some of the remaining 27 may not violate a stated requirement.

## 5. Results and measurement units

The paper reports results at different units—mutant, assertion, anomaly report and test. These must not be collapsed into one generic “detection rate.”

| Result | Unit | Value | Interpretation |
|---|---|---:|---|
| Inserted bugs | Mutant | 564 | At least this many mutations were inserted. |
| Passed every regression test | Mutant | 241 | Regression survivors before benchmark filters. By subtraction, 323 of the reported 564 failed at least one regression test. |
| Candidate escapes evaluated | Mutant | 68 | Non-equivalent, activated candidates after filters; still not all proven specification violations. |
| Confirmed scoreboard escapes | Mutant | 41/68 | At least 41 candidates received a qualified assertion; the paper treats this as a lower bound. Per IP: PWM 15/24, PATTGEN 8/16, SPI Host 14/16, CSRNG 4/12. |
| ACC observed injected effect | Mutant | 55/68 | The ACC described the injected effect for 55 candidates (about 81%); this is not the end-to-end confirmed-detection rate. |
| ACC failed to observe injected effect | Mutant | 13/68 | The ACC did not identify the injected effect in 13 candidates. |
| Correct ACC report, but no qualified assertion | Mutant | 14/68 | The ACC described the bug, but no Generator/formal assertion qualified. This and the 13 ACC misses account for the 27 not detected. |
| Directed tests reproduced detections | Mutant/test | 36/41 | Thirty-six qualified findings were reproduced in directed UVM tests with scoreboard PASS. Five formal detections were not reproduced, mainly because the existing sequences could not express the counterexample stimulus. |
| Assertions reaching formal | Assertion | 167 | Aggregate across the four designs. |
| Qualified assertions | Assertion | 71/167 | About 42.5%. |
| False-positive assertions | Assertion | 86/167 | A false positive is an assertion with a counterexample on the reference RTL. The paper says almost all other assertions were false positives. |
| Other assertions | Assertion | 10/167 | Undetermined, vacuous, or proven on both mutant and reference. |
| ACC anomalies describing injected bug | Anomaly report | 168/232 | About 72% of anomaly reports described the injected bug. Most of the remaining reports described contradictions also present in the unmodified reference. |
| Findings on unmodified designs | Anomaly report | 9 | The authors verified these as documentation-versus-RTL contradictions, not injected-bug detections. |
| Specification-only baseline | Mutant | 11/68 | Same Generator/formal flow, supplied only with the specification and RTL declarations; compared with 41/68 for the full framework. |

### Two details that change the interpretation

**The 27 misses have their own stage attribution.** The paper says 13 candidates were missed by the ACC. In 14 others the ACC's anomaly report was correct, but no generated assertion qualified. This is the paper's own observation-to-assertion failure split; it is relevant prior art for any OpenVEF claim about attributing verification misses.

**The specification-only baseline is not a clean one-variable ablation.** The baseline uses the same Generator and formal flow but provides only the specification and RTL declarations. It omits the signal digest, ACC anomaly report and RTL excerpt. The Generator therefore runs once per design rather than once per mutant, and the resulting assertions are checked against every mutant for that design. The result (11/68 versus 41/68) does not isolate the effect of trace information alone because multiple input elements and the generation schedule change together.

## 6. Model, tool and cost configuration

The three LLM components (ACC, Generator and Adversarial Challenger) use Claude Opus 5.5 with adaptive reasoning at high effort. BugGen uses GPT-4o-mini to write the injected mutations. The formal tool is Cadence JasperGold 2024.09 with a 900-second proof limit; assertions not decided within that limit are undetermined. The framework uses Cadence Xcelium for simulation through OpenTitan `dvsim`.

Each mutant receives one framework run, except PWM20, which received two Generator runs. The median runtime was 9.6 minutes per mutant, mostly simulation time, with about 620,000 input and 18,000 output LLM tokens per mutant.

## 7. Limitations and threats to validity

### 7.1 Limitations explicitly stated by the authors

1. **One framework run and one regression seed:** each mutant was evaluated with one framework run and each regression test used one seed. The authors explain that the goal was to demonstrate the framework, not grade the testbenches. They note that other seeds might catch some candidates and that such cases would reveal stimulus gaps.
2. **Public OpenTitan design exposure:** the design and documentation are public and may have appeared in model training data. The authors argue that the injected mutations were created by the study and could not have been seen in training.
3. **ACC misses:** 13 candidates were not observed by the ACC, often because an existing documentation/RTL contradiction dominated its report or a trace exceeded the context window. The authors suggest reading traces in parts.
4. **Assertion-generation misses and false positives:** 14 candidates had a correct anomaly report but no assertion qualified. Of 167 assertions reaching formal, 71 qualified and 86 were false positives; 10 were other. The paper says many false positives encode documented requirements that the reference RTL does not implement, while others constrain timing too tightly.
5. **Reproduction gap:** five of 41 qualified detections were not reproduced, mainly because the existing UVM sequences could not generate the formal counterexample stimulus. The authors suggest allowing new sequences.
6. **Candidate uncertainty:** some of the 27 undetected candidates may not violate any stated specification requirement; 41/68 is therefore a lower bound.
7. **No known reference in deployment:** the reference RTL is an evaluation instrument for injected bugs. In real use, failing assertions require engineer review.
8. **Diminishing returns:** successive runs may return only anomalies already reviewed, so the marginal value of repeated runs can fall.
9. **Specification fidelity:** the paper uses OpenTitan documentation as written and does not repair inconsistencies with RTL; those contradictions affect anomaly and assertion results.

### 7.2 Reviewer observations, not author-acknowledged limitations

1. **No uncertainty estimates:** 68 evaluated candidates over four IPs and one run each provide limited evidence for comparing per-IP rates; the paper does not report intervals or variance estimates.
2. **Selection effects:** candidates that are undetermined, unbindable, undriven, non-elaborating or too large for the context window are excluded. Findings therefore apply to the retained subset, not automatically to every inserted mutant.
3. **Unequal per-IP funnel retention:** the numbers retained differ substantially by IP. Direct comparisons of per-IP rates need caution.
4. **Mutation-model scope:** the benchmark uses single-line RTL mutations generated by one model through BugGen. It does not establish coverage of all real design bugs or multi-line defect patterns.
5. **Tool accessibility:** Xcelium and JasperGold are commercial tools. This can make independent reproduction harder, but the paper does not list commercial-tool dependence as an author-acknowledged limitation.
6. **Baseline confounding:** the specification-only baseline removes multiple information inputs and changes generation frequency, so its performance difference cannot be attributed solely to the absence of traces.
7. **Activation-definition ambiguity:** Section III says “every output” matches; Section V-B says activation compares traces signal by signal. The text does not settle whether internal signals count for the benchmark activation filter.

## 8. Relationship to OpenVEF

### 8.1 Direct comparison

| Dimension | *Verify the Verifier* | OpenVEF (Charter/Protocol v0.4 draft) |
|---|---|---|
| Main goal | Find specification violations hidden by a passing, existing regression and help harden that regression | Evaluate effectiveness of LLM-generated verification artifacts under controlled conditions |
| Test population | Existing, human-authored OpenTitan UVM regressions and scoreboards | Newly generated LLM-authored driver + checker pairs |
| LLM role | ACC inspects traces; Generator writes SVA; Challenger creates directed UVM reproductions | LLM authors the driver and checker being evaluated |
| Existing stimulus/checker decomposition | Table I separates non-activated mutants from activated-but-passing candidates; end-to-end misses split 13 ACC misses vs 14 later assertion/formal misses | NP and PND distinguish no specification-masked divergence from divergence accepted by the artifact's checker |
| Observation basis | Signal digest contains all target-module signals, including internal signals; qualification is specification-grounded | Explicit pre-frozen, specification-derived observation mask applied to paired traces |
| Unit of analysis | Primarily mutant and generated assertion; one framework run per mutant (PWM20 exception) | Artifact-level aggregation across artifact–mutant pairs and repeated independent prompt samples |
| Prompt factor | No direct-versus-structured prompt comparison; the specification-only baseline changes several inputs at once | Direct vs structured prompts with the same design information is a central planned factor |
| Fault model | LLM-written single-line RTL source mutations via BugGen/GPT-4o-mini | Planned Yosys/MCY netlist signal mutants in the primary MVP; different fault population |
| Equivalence strength | JasperGold proof over reachable states (unbounded) | Bounded miter/BMC to depth N in the current protocol; not equivalent proof strength |
| Checker | Generated SVA formally qualified on mutant and reference, with non-vacuity check | Artifact's own offline checker evaluated over harness-captured traces |
| Execution | Four OpenTitan IPs with native UVM environments, `dvsim` and Xcelium | Small cycle-exact sequential RTL benchmarks (FIFO and UART planned) and open tooling |

### 8.2 What overlaps and what does not

The earlier analysis understated the overlap. The following ideas are already present in the paper or its benchmark construction:

- **Stimulus versus checker-related decomposition:** the funnel distinguishes non-activated mutants from activated mutants that still pass the regression. This is a close conceptual precedent for NP versus PND, although the denominator, signal semantics and specification-mask treatment differ.
- **Stage attribution of misses:** 13 candidates are missed by the ACC and 14 more fail to obtain a qualified assertion after a correct anomaly report.
- **Reference-based checker qualification:** the paper's mutant/reference assertion check and antecedent cover are a close precedent for treating a checker failure as valid only after checking it against a known-good reference.
- **Specification observability:** the paper states that a change in behaviour is not necessarily a specification violation; a mutant may change only unstated behaviour. This supports the need for OpenVEF's observation mask, but does not itself validate OpenVEF's chosen mask.

These overlaps must be acknowledged. OpenVEF must not claim that it invented stimulus-versus-checker attribution, mutation-based testbench evaluation, trace-based miss classification, reference-side qualification, or LLM-generated hardware stimulus/checkers.

### 8.3 Narrow candidate distinction for OpenVEF

Based on this paper alone, the most defensible candidate contribution is the **combination** of:

1. **Population:** newly LLM-authored driver-and-checker artifact pairs are the objects being measured, rather than human-authored UVM regressions being audited by an LLM.
2. **Controlled prompt factor:** direct and structured prompt conditions receive identical design information, with prompt structure as the planned independent variable.
3. **Per-artifact masked measurement:** the miss composition is aggregated per generated artifact and judged against an explicit, pre-frozen specification-derived observation mask.
4. **Reproducible repeated sampling:** multiple independent artifact samples per condition and pre-registered analysis are planned, rather than one run per mutant.

This is a **candidate contribution, not a novelty finding**. Each component has related prior art somewhere, and Step 2 must test whether their combination is already covered by functional-qualification research and LLM hardware-verification benchmarks.

The following are not direct contribution claims: “separating stimulus and checker misses”; “using mutation testing”; “comparing against a reference”; “using LLMs to generate tests or assertions”; or “checking whether a fault changes behaviour.”

### 8.4 Important methodological differences and caveats

- **Fault population:** the paper uses single-line RTL source mutants; OpenVEF plans netlist signal mutants. Results are not directly comparable, and this difference is not automatically a research contribution.
- **Equivalence:** the paper uses unbounded formal equivalence; OpenVEF's planned BMC result is only bounded to depth N. OpenVEF must label this honestly and avoid implying the same guarantee.
- **Observation:** the paper's trace includes every target-module signal, whereas OpenVEF proposes a specification-derived mask. The mask is a methodological choice that requires independent justification and validation.
- **Classification:** OpenVEF's NP category is an output-level/no-masked-divergence category. Because it does not measure internal state activation separately, it may combine what functional-qualification literature calls non-activation and non-propagation. State this mapping explicitly when reviewing that literature.
- **Reactive paired runs:** OpenVEF has explicit rules for paired runs where a reactive driver may produce different subsequent inputs after observing divergent outputs. No equivalent rule was located in this paper's description of its regression activation check; do not claim this is a broad new principle without further comparison.

## 9. Required changes to OpenVEF planning

1. Replace any claim that “miss attribution” or “stimulus-versus-checker separation” is the novelty. Describe it as an established evaluation concept that OpenVEF applies to LLM-authored artifact pairs under a controlled prompt study.
2. Add the Table I non-activated/activated-but-passing funnel as a prominent prior-art comparison.
3. Add the paper's own 13-versus-14 miss attribution across ACC and Generator/formal stages.
4. State that the defensible candidate contribution is the conjunction of LLM-authored driver/checker population, controlled prompt-structure comparison with matched information, and per-artifact measurement against a pre-frozen specification mask.
5. Do not compare OpenVEF's PND/(NP+PND) directly with 41/68, 55/68, 48/241, 68/241, or 71/167; these have different units, selection rules and meanings.
6. Explicitly distinguish source-level RTL mutations from netlist signal mutants.
7. Explicitly distinguish the paper's unbounded equivalence proof from OpenVEF's bounded equivalence-to-depth-N classification.
8. Cite the paper's statement that a behavioural difference need not violate a stated requirement as support for requiring a specification-derived observation mask, while retaining independent mask validation as an OpenVEF requirement.
9. Add the activation-definition ambiguity (outputs versus signal-by-signal trace) to the related-work notes.
10. In the OpenVEF statistical design, retain repeated samples, uncertainty estimates, model/prompt version pinning, deterministic seeds, checker false-alarm controls and explicit exclusions.

## 10. Review verdict and Step 1 status

**Claude's verdict: PASS WITH CORRECTIONS. Our reconciled verdict: PASS WITH CORRECTIONS.** The audit's central criticism is valid: the earlier analysis understated the stimulus/checker decomposition already present in the benchmark funnel and did not report the 13-versus-14 framework miss split. It also correctly identified incomplete definitions and a source-inspection statement that was too strong.

This revision checks the full extracted paper text available through a PDF mirror, including Table I and the results sections. It resolves the five Table I filter counts that Claude could not locate in the search-index excerpts. However, because the original arXiv PDF was not directly retrieved and the mirror's PDF page screenshots could not be fetched, this should be described as **full extracted-text review, pending visual page-level verification**, not as inspection of all seven rendered PDF pages.

**Research decision:** Keep OpenVEF CONDITIONAL GO. Narrow its candidate contribution to the controlled study of LLM-authored driver/checker pairs, matched-information prompt-structure manipulation, and per-artifact masked measurement. Do not claim novelty until Step 2's broader literature audit is complete.

**Step 1 status:** Complete for this selected paper's extracted text; pending page-image/PDF visual verification if page-specific visual checking is required. The next research stage is the broader functional-qualification and mutation-analysis literature review, including Certitude and academic work.

---

## Bibliographic reference

Sanchez Villalobos, A. E., Quinn, M. D., Tyagi, A., Luu, M. D., & Houngninou, D. K. (2026). *Verify the Verifier: Specification-Grounded LLM Cross-Checking for Bugs That Escape UVM Scoreboards*. arXiv:2611.26588v1. https://arxiv.org/abs/2611.26588
