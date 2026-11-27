# OpenVEF Experimental Protocol v1.3.7-candidate

**Project:** OpenVEF — Open Verification Effectiveness Framework  
**Version:** 1.3.7-candidate (OpenVEF Planning v1.3.6 with the corrections in `CHANGELOG-v1.3.7-candidate.md`; not audited; not frozen; not approved). Based on: 1.3.6 (corrective evidence/metadata release; independent re-audit pending; not frozen)  
**Date:** 23 November 2026  
**Status:** DESIGN DRAFT — no work authorized until v0.8 decisions A1–A11 are accepted and X14 is explicitly decided  
**Project owner:** TO CONFIRM against the actual TEEP application; no identity is inferred

> **Canonical protocol.** This document controls all experimental definitions, denominators, pair classes, statistical analysis and feasibility controls. The Charter summarizes the study and points here. The seven v0.7 design directions remain approved. The v1.3, v1.3.1, v1.3.2 and v1.3.3 independent document audits returned FAIL for the LLM-call gate. The v1.3.3 audit identified N13: an async generator expression containing `await` could bypass the rank-7 test. This v1.3.4 corrective release extends rank 7 to detect `ast.Await` anywhere in a comprehension subtree, clarifies AST-ancestry symbol naming and compile-stage async outcomes, restores M63 indentation, and adds M70. At the time of the v1.3.4 release, its independent document re-audit and all implementation validation remained pending; the owner-reported v1.3.5 document-only PASS and v1.3.6 re-audit-pending status, and the not-audited v1.3.7-candidate status, are recorded in §19. Owner acceptance of A1–A11 and the X14 strict-AST branch choice are not recorded; no work is authorized. After both decisions are recorded, only the permitted hand-built FIFO scope may open. No LLM/provider call, including F16, is authorized until the separate LLM-call gate passes independent re-audit.

## 1. Experimental objective

Evaluate the generation-to-detection pipeline for LLM-authored cycle-synchronous driver/offline-checker artifacts on sequential RTL and a declared population of post-synthesis structural netlist signal mutants. Compare two pre-frozen prompt presentation orders, ORG-A and ORG-B, that contain the same semantic blocks, task instruction, system prompt, repair prompt, feedback policy and output contract. Report:

1. artifact validity over every scheduled generation slot;
2. joint masked exposure and joint own-checker detection over every scheduled slot × primary-mutant combination;
3. conditional own-driver exposure and own-checker detection diagnostics among valid, complete-trace pairs; and
4. a pre-registered secondary common-trace checker panel using the same legal trace corpus for every checker.

Miss composition is descriptive only. Do not call any metric generic or universal checker quality. The common-trace panel reports standardized checker sensitivity only for its declared trace population, exposure set and compatibility rules.

## 2. Research question and analysis family

**Primary research question.** For a declared set of cycle-exact sequential RTL designs and a pre-registered population of post-synthesis structural netlist signal mutants, how do two prompt-presentation orders carrying identical semantic information affect (a) artifact validity per scheduled generation call, (b) joint masked exposure per scheduled call × primary mutant, and (c) joint own-checker detection per scheduled call × primary mutant? Conditional own-driver exposure, conditional own-checker detection and miss composition are reported as labelled diagnostics; a common-trace checker panel is a standardized secondary analysis.

**H1 — validity/attrition description (estimation only).** For each arm and design, report the intention-to-treat validity rate and its confidence interval, along with the full scheduled-call funnel. H1 does not create a separate hypothesis test; validity-arm comparison is H2(a).

**H2 — pre-registered two-sided ORG-arm comparison.** Compare ORG-A and ORG-B on exactly three primary outcomes:

- **H2(a):** validity per scheduled generation slot;
- **H2(b):** joint masked exposure per scheduled slot × primary mutant;
- **H2(c):** joint own-checker detection per scheduled slot × primary mutant.

Use two-sided tests because no defensible directional effect is assumed. The presentation factor is exploratory in direction; do not claim that one ordering should improve results absent an independently justified directional rationale. Apply Holm correction across these three outcomes, and only these three. H1 is descriptive and is not counted again in the Holm family. H2 inference is conditional on the frozen declared mutant population; mutants are fixed, not sampled. Scheduled slots are assigned to arms by a balanced within-design schedule generated from a frozen seed and committed before the first call.

**Conditional diagnostics.** For each valid artifact, compute `E_i` from all complete-trace valid pairs and `S_i` among all masked-exposed pairs, including checker crashes after exposure as non-detections. The conditional `E_i` is checker-independent by construction. ITT `J_exposure` is not a pure driver-only quantity: it also depends on the checker through the artifact-validity gate. These diagnostics are conditional on validity and complete-trace availability. They are not independent causal effects of the driver and checker.

**Descriptive miss composition.** `M_i = PND_i / (NP_i + PND_i)` when defined. It is not checker quality, not a causal decomposition and not a confirmatory endpoint. The former `delta_checker` threshold is removed.

**Secondary common-trace panel.** Evaluate all scheduled artifact checkers on a common legal trace corpus. Report compatibility, false alarms and standardized sensitivity. Pre-register arm contrasts in the panel as secondary/exploratory, with both intention-to-treat and compatibility-conditional estimates. The panel measures performance on its declared exposure profile, not universal checker quality.

Human baseline: one time-boxed artifact per design, descriptive only. Its author must not have accessed the evaluator pack (RTL, mask, mutant manifest or panel outcomes). If no independent author is available, label the baseline “evaluator-informed” and do not describe it as an independent human baseline. Random/reference driver: a stimulus baseline and source of legal common traces, not a prompt-arm comparator.

## 3. Conditions, author information and prompt presentation

### 3.1 Conditions

| Condition | Driver | Checker | Role |
|---|---|---|---|
| Human | One cycle-synchronous human-authored driver per design | Human offline checker | Descriptive only |
| Random/reference | Deterministic, legality-respecting seeded driver | Independent evaluator reference-model checker | Stimulus baseline and shared-trace source only |
| ORG-A | Same pinned LLM, ORG-A prompt template | LLM-authored offline checker | Primary arm |
| ORG-B | Same pinned LLM, ORG-B prompt template | LLM-authored offline checker | Primary arm |

### 3.2 Authoring packet: included and excluded information

Both LLM arms receive the same exact authoring packet:

- cycle-exact design specification;
- top-level port manifest and signal directions/widths;
- reset protocol and legal-input assumptions;
- cycle cap and safe-idle policy;
- cycle-synchronous driver API;
- trace schema and field definitions; and
- offline checker contract.

Both arms receive feedback under the same frozen feedback policy (triggers, closed diagnostic grammar, whitelist, byte cap and truncation), not identical artifact-dependent feedback content. No author receives RTL source, internal-signal visibility, evaluator-only materials, expected-output tables, mutant identities, mutation output, mutant traces or mutant results.

**The evaluator-only mask file, reference model/API and expected-output tables are not included in the authoring packet.** Authors derive their own expected-value logic from the specification and the trace contract. A checker may use recorded inputs and legitimate prior public-output/history fields, but may not call a reference model/API or use an evaluator-only expected-output table. If it derives expectations from DUT-reported history, self-consistent corruption may be accepted; this is a measured checker weakness, not a contract violation.

Withholding the evaluator-only materials removes the explicit machine-readable scoring list, not the underlying requirements: every observation obligation and every don't-care window must be stated in the specification authors receive. The evaluator may not score authors on a mask condition that cannot be traced to an explicit specification clause.

### 3.3 Prompt factor: ORG-A versus ORG-B

The manipulation is **prompt presentation order only**. It does not add, remove, paraphrase or prioritize semantic content through arm-specific headings or instructions; attention effects caused by the pre-registered whole-block order are part of the treatment.

- The task-instruction block is identical, appears first in both arms, and has the same internal sentence order.
- The same neutral heading strings are used in both arms. Every block is atomic; the only treatment difference is the order of whole blocks.
- No block may be rewritten, paraphrased, split, merged, emphasized or supplemented in one arm.
- The system prompt, repair prompt, response schema, design data, permitted feedback and all non-prompt settings are identical across arms.
- The exact ORG-A and ORG-B template pair is included in this pack. See the response schema, parser contract and assembly spec files 30–34 for the production contract. Model-visible headings contain no block IDs or arm labels. The response contract is the machine-checkable JSON Schema in `34_OpenVEF_Response_Schema_v1.0.json`, implemented by `30_Response_Parser_and_Execution_Contract_v1.3.7-candidate.md`; assembly is controlled by `31_Prompt_Assembly_and_Canonicalization_Spec_v1.3.7-candidate.md`. The design-specific placeholders must be filled with the same byte-identical authoring-packet payloads before the templates can pass F18.
- Ordering may act through primacy, recency or adjacency. Do not call the factor neutral or claim it changes no attention; that is the mechanism the presentation manipulation may invoke.
- Compare each corresponding block using `31_Prompt_Assembly_and_Canonicalization_Spec_v1.3.7-candidate.md`. Hidden block IDs remain in the assembler sidecar and are never model-visible. Normalized block contents and visible headings must match exactly. Only the permutation of whole blocks may differ.
- Name and pin the tokenizer used for the selected model before F18. Do not use a loose percentage token tolerance. Count each canonical block and wrapper separately; no arm-specific wrapper tokens are permitted. Record assembled-prompt token counts for transparency.

If any task instruction, repair guidance, system message or semantic content differs, F18 fails. Do not relabel a content-changing treatment as organization-only; stop and revise the research question.

### 3.4 Human and LLM feedback policy

- Human baseline: proposed 120-minute time box per design (**TO FREEZE**); the author must not have accessed the evaluator pack, otherwise label the baseline “evaluator-informed”.
- LLM: proposed `k=2` repair attempts after the initial generation (**TO FREEZE**). Repairs are nested within the scheduled slot and do not increase `n`. Initial-call validity and final post-repair validity are both reported; the ITT primary validity endpoint uses the final artifact after the frozen repair budget.
- The repair-message template, failure map, feedback policy and serialization are identical across arms; artifact-specific feedback contents may differ. Only exact diagnostics emitted by the normative map can enter the serializer; arbitrary path-bearing or free-form text is outside the diagnostic grammar and is rejected.

**Normative diagnostic grammar.** Model-feedback diagnostics are closed-vocabulary strings. A diagnostic is either one exact fixed literal sentence listed below, one fixed `CODE` token, or `CODE|key=value` fields separated by a single ASCII vertical bar. `CODE` and keys use `[A-Z][A-Z0-9_]*`. Values are ASCII, non-empty, and may not contain `|`, CR or LF. Fields occur exactly in the order shown. No raw exception message, validator message, source text, file path, trace content, provider prose or arbitrary free-form text is permitted. The feedback serializer accepts only diagnostics produced by the authoritative stage map; it does not rewrite or normalize arbitrary strings.

```text
SCHEMA_REJECT|pointer=<JSON_POINTER>
OUTPUT_TRUNCATED
SOURCE_EMPTY|file=<FILE>
SOURCE_SYNTAX_REJECT|file=<FILE>|line=<LINE>|column=<COLUMN>
IMPORT_NOT_ALLOWED|module=<OFFENDING_ROOT>
IMPORT_FORM_REJECT|file=<FILE>|line=<LINE>|reason=<REASON>
NON_ASCII_IDENTIFIER|file=<FILE>|line=<LINE>|column=<COLUMN>
PROHIBITED_BUILTIN|name=<NAME>
GLOBAL_RANDOM_USE|name=<NAME>
MODULE_STATEMENT_REJECT|file=<FILE>|line=<LINE>|reason=<REASON>
DECORATOR_REJECT|file=<FILE>|symbol=<SYMBOL>
ENTRY_POINT_REJECT|file=<FILE>|symbol=<SYMBOL>|reason=<REASON>
COMPILE_ERROR|file=driver.py|line=<LINE>
COMPILE_ERROR|file=checker.py|line=<LINE>
RUNTIME_EXCEPTION|file=driver.py|phase=<PHASE>|class=<EXCEPTION_CLASS>
DRIVER_VECTOR_INVALID|reason=<REASON>
WATCHDOG_TIMEOUT|phase=driver_step
DRIVER_NONDETERMINISM|reason=NEXT_INPUT_DIVERGENCE
TRACE_INTEGRITY_FAILURE|reason=<REASON>
RTL_NULL_CONTROL_FAILURE|reason=MASKED_OUTPUT_DIVERGENCE
SIMULATOR_ERROR|target=<RTL_OR_NULL>|class=<EXCEPTION_CLASS>
CHECKER_RUNTIME_ERROR|class=<EXCEPTION_CLASS>
CHECKER_RETURN_INVALID|reason=<REASON>
CHECKER_TIMEOUT|phase=null_check
The checker returned FAIL on a legal null-netlist trace.
CHECKER_NONDETERMINISM|reason=RUN_DISAGREEMENT
```

**Diagnostic value enumerations.** `FILE` is `driver.py` or `checker.py`; `LINE` and `COLUMN` are positive decimal integers; `EXCEPTION_CLASS` is the simple Python exception class name matching `[A-Za-z_][A-Za-z0-9_]*`, otherwise the fixed fallback `Exception`; `RTL_OR_NULL` is `rtl` or `null`; `PHASE` is `factory` or `step`. `IMPORT_FORM_REJECT.reason` is one of `RELATIVE_IMPORT`, `STAR_IMPORT`, `FUTURE_FEATURE`, `FROM_IMPORT_FORBIDDEN`, `SUBMODULE_IMPORT`, `IMPORT_ALIAS`, or `MULTIPLE_NAMES`; a disallowed root uses the separate `IMPORT_NOT_ALLOWED|module=<OFFENDING_ROOT>` diagnostic. `MODULE_STATEMENT_REJECT.reason` is one of `MODULE_EXECUTABLE`, `MODULE_CONTROL_FLOW`, or `NON_LITERAL_CONSTANT`; the deprecated `NON_FUNCTION_DEFINITION` value is not emitted. `ENTRY_POINT_REJECT.reason` is one of `MISSING_ENTRY_POINT`, `PARAMETER_NAMES`, `PARAMETER_KIND`, `DEFAULT_OR_VARIADIC`, `EXTRA_ENTRY_POINT`, `WRONG_ENTRY_POINT_KIND`, `CLASS_FORBIDDEN`, `DRIVER_CLASS_FORM`, `FORBIDDEN_METHOD`, `NESTED_CLASS_FORBIDDEN`, `ASYNC_DEFINITION`, `ASYNC_COMPREHENSION`, `RETURN_TYPE`, or `RUNTIME_SIGNATURE`. `DRIVER_VECTOR_INVALID.reason` is one of `RETURN_TYPE`, `MISSING_KEYS`, `EXTRA_KEYS`, `NON_STRING_VALUE`, `WRONG_WIDTH`, `ILLEGAL_SYMBOL`, or `ILLEGAL_PROTOCOL_STATE`. `CHECKER_RETURN_INVALID.reason` is one of `NON_DICTIONARY`, `TOP_LEVEL_KEYS`, `INVALID_VERDICT`, `MISSING_DIAGNOSTICS`, or `DIAGNOSTICS_NOT_LIST`. `TRACE_INTEGRITY_FAILURE.reason` is one of `REPLAY_HASH_MISMATCH`, `MALFORMED_RECORDER_OUTPUT`, `ROW_ALIGNMENT`, or `UNTRUSTED_TRACE_SERIALIZATION`. `GLOBAL_RANDOM_USE.name` is a prohibited module-global attribute such as `random.random`, `random.randint` or `random.SystemRandom`; `random.Random` is the sole permitted `random` attribute. `PROHIBITED_BUILTIN.name` is one of `__import__`, `eval`, `exec`, `compile` or `open`. `DECORATOR_REJECT.symbol` is the qualified function/class/method name. `IMPORT_NOT_ALLOWED.module` is the offending root as written, for example `os`. `NON_ASCII_IDENTIFIER` emits only file, line and column; the identifier itself is never echoed. `SIMULATOR_ERROR.target` is `rtl` or `null`; `CHECKER_TIMEOUT.phase` is `null_check`. No unlisted value is permitted.

`SOURCE_SYNTAX_REJECT.column` is derived from pinned CPython 3.11 `SyntaxError.offset`. If `offset` is absent, null or less than 1, emit `column=1`; otherwise emit the positive one-based source-character column reported by CPython. This is distinct from `NON_ASCII_IDENTIFIER.column`, which is a one-based UTF-8 byte column at the start of the entire offending identifier lexeme. A source-character column and a UTF-8 byte column are not interchangeable when earlier characters on the line are multibyte. Pin the exact Python 3.11 patch release; re-confirm P25a/P25b and M35/M43–M46 under that runtime.

**Import-node classification and total precedence.** Nodes are visited by `(lineno, col_offset, end_lineno, end_col_offset)` within `driver.py`, then `checker.py`. Each `ast.Import` or `ast.ImportFrom` produces at most one failure. For one `ast.Import` node, apply this total order: (1) if `len(names) != 1`, `IMPORT_FORM_REJECT|...|reason=MULTIPLE_NAMES`; (2) if the first component of the imported name is not an allowed root, `IMPORT_NOT_ALLOWED|module=<root>`; (3) if the imported name is dotted, `IMPORT_FORM_REJECT|...|reason=SUBMODULE_IMPORT`; (4) if `asname` is present, `IMPORT_FORM_REJECT|...|reason=IMPORT_ALIAS`; otherwise accept the exact single root. Thus `import math, json` is `MULTIPLE_NAMES`; `import os.path` is `IMPORT_NOT_ALLOWED|module=os`; `import collections.abc` is `SUBMODULE_IMPORT`; and `import math as m` is `IMPORT_ALIAS`.

For one `ast.ImportFrom` node, apply this total order: (1) `level > 0` → `RELATIVE_IMPORT`; (2) any `*` alias → `STAR_IMPORT`; (3) if `len(names) != 1` → `MULTIPLE_NAMES`; (4) if `module == "__future__"`, accept only exactly one unaliased `annotations` name; any other future feature → `FUTURE_FEATURE`, while `annotations as alias` → `IMPORT_ALIAS`; (5) if the first module component is not an allowed root, emit `IMPORT_NOT_ALLOWED|module=<root>`; (6) every remaining non-future `from` import emits `FROM_IMPORT_FORBIDDEN`. Consequently `from collections import abc` and `from collections.abc import Iterable` are `FROM_IMPORT_FORBIDDEN`; `from os import path as p` is `IMPORT_NOT_ALLOWED|module=os`; `from . import x` is `RELATIVE_IMPORT`; `from math import *` is `STAR_IMPORT`; and `from __future__ import annotations, annotations` is `MULTIPLE_NAMES`. `IMPORT_NOT_ALLOWED` is a distinct diagnostic code, not an `IMPORT_FORM_REJECT.reason`.

**Prohibited-name and non-ASCII identifier rules.** Reject AST `Name` nodes whose `id` is `__import__`, `eval`, `exec`, `compile` or `open`, and reject access through `builtins.<name>` for those same names. `re.compile` is allowed. The import root `random` is permitted only to construct a local `random.Random(seed)`; direct `random.<attribute>` use other than `random.Random` emits `GLOBAL_RANDOM_USE`. Static checking may not detect aliases such as `r = random; r.random()` or `getattr(random, "random")`; these are not represented as statically proven violations. If they cause a paired next-input mismatch, that runtime event is classified by the paired-run rule below. Every Python identifier lexeme must be ASCII. After successful `ast.parse`, process `tokenize.NAME` and `tokenize.ERRORTOKEN` tokens in source-position order. For a `NAME` token, reject it if any code point is above U+007F. For an `ERRORTOKEN`, inspect each non-ASCII code point in source order. Under the pinned Python 3.11 runtime, define `START(c)` as `c.isidentifier()` and `CONTINUE(c)` as `("A" + c).isidentifier()`. Reconstruct the maximal same-line contiguous run containing the offending code point by extending left and right across `CONTINUE` characters; the run is an identifier lexeme only when its first character satisfies `START`. Reject that complete lexeme at its first character. This rule identifies both non-ASCII start characters (such as U+2118) and non-ASCII continuation characters inside an ASCII-prefixed identifier. This catches valid non-ASCII identifiers that the tokenizer may expose as `ERRORTOKEN`, including U+2118, rather than silently skipping them. STRING and COMMENT tokens are not scanned; Unicode in strings, bytes and comments remains allowed. Process `driver.py` then `checker.py`; within each file, complete the full identifier scan before import, prohibited-name or module-body classification. This makes the identifier rule win over import-form/root failure on the same statement. `column` is the one-based UTF-8 byte position at the start of the entire identifier lexeme, calculated from the UTF-8 byte length of the source-line prefix. Never echo the offending lexeme. The exact scanner must be verified on the pinned Python 3.11 interpreter; M55–M57 cover U+2118, an ASCII-prefixed identifier with U+2118, and permitted Unicode in strings/comments.

**Module statement policy and stage ownership.** Stage `IMPORT_POLICY` checks module-body statements other than `ast.FunctionDef`, `ast.AsyncFunctionDef` and `ast.ClassDef`; all function/class definition nodes are deliberately deferred to `AST_SIGNATURE`. At module scope, allow only permitted imports, one optional docstring expression, synchronous undecorated function definitions (deferred to signature checks), the single permitted `Driver` class in `driver.py` (deferred to signature checks), and assignments/annotated assignments whose values are recursively literal-only. A non-literal assignment is `NON_LITERAL_CONSTANT`; module-level control-flow statements (`if`, `for`, `while`, `with`, `try`, `match`, `async` control flow) are `MODULE_CONTROL_FLOW`; other executable statements/calls/expressions are `MODULE_EXECUTABLE`. No asynchronous function definition is accepted at any lexical depth; every `ast.AsyncFunctionDef`, including an `async def` nested inside a synchronous helper, is checked exactly once at `AST_SIGNATURE` under the precedence below. An async binding of a required symbol (`create_driver`, `Driver.step`, `check_trace`) emits `WRONG_ENTRY_POINT_KIND` in the required-symbol pass. An async direct `Driver` method other than `step` emits `FORBIDDEN_METHOD` (rank 3). A decorated async definition emits `DECORATOR_REJECT` (rank 5). Every other async function definition emits `ENTRY_POINT_REJECT|file=<FILE>|symbol=<SYMBOL>|reason=ASYNC_DEFINITION` (rank 6). Separately, an asynchronous comprehension is any `ast.GeneratorExp`, `ast.ListComp`, `ast.SetComp` or `ast.DictComp` node that has at least one associated `ast.comprehension` with `is_async == 1`, or that contains an `ast.Await` node anywhere in its AST subtree. Python treats a generator expression containing `await` as an asynchronous generator expression even when every `is_async` flag is 0. The `ast.Await` subtree test also deliberately catches `await` in a generator expression element, filter, later `for` clause or nested lambda, and in list, set or dict comprehensions; these comprehension expressions are rejected at rank 7 before compilation. Such a node is not an `ast.AsyncFunctionDef`: in particular, `(item async for item in stream)` is a valid async generator expression inside an ordinary synchronous function and can parse and compile without an enclosing `async def`. Inspect these expression nodes explicitly at `AST_SIGNATURE`; after the required-symbol pass and ranks 1–6, every remaining asynchronous comprehension emits `ENTRY_POINT_REJECT|file=<FILE>|symbol=<ENCLOSING_SYMBOL>|reason=ASYNC_COMPREHENSION` at category rank 7. `ENCLOSING_SYMBOL` is computed by AST ancestry: collect every ancestor `ast.FunctionDef`, `ast.AsyncFunctionDef` and `ast.ClassDef` of which the expression node is a descendant, ordered outermost first, and join their names with `.`. This includes expressions in a definition's decorators, arguments, defaults, annotations, bases and keywords. Do not use runtime evaluation scope or include lambda names. A `<module>` symbol is unreachable after `IMPORT_POLICY`, because module-body expressions are rejected before `AST_SIGNATURE`; therefore an expression reaching this rule has at least one enclosing definition node. If an async comprehension occurs inside an `AsyncFunctionDef`, rank 6 rejects the enclosing async function first. A standalone `await` expression, `async for` statement or `async with` statement anywhere outside an `ast.AsyncFunctionDef` (including synchronous function bodies and headers, lambdas and class bodies), when not contained in a comprehension expression caught by rank 7, passes `ast.parse` and `AST_SIGNATURE` but is rejected by Python `compile()` as `COMPILE_ERROR|file=<FILE>|line=<LINE>` at `COMPILE_DRIVER` or `COMPILE_CHECKER`. An `await` node anywhere inside a comprehension expression is owned by rank 7 instead. No class is permitted in `checker.py`; any class other than the single valid `Driver` in `driver.py`, and any nested class anywhere, is checked at `AST_SIGNATURE`, not `IMPORT_POLICY`. Any decorator on a function, class or method is also checked at `AST_SIGNATURE` and emits `DECORATOR_REJECT`. This ownership rule prevents a module-level class/function/async-function definition or async-comprehension expression from being rejected by two stages.

**JSON Pointer selection.** Use the pinned Draft 2020-12 validator and collect all schema errors. Convert `absolute_path` to RFC 6901 instance tokens; escape `~` as `~0` and `/` as `~1`; show root as `/`. For `required` and `additionalProperties`, report the parent instance pointer. Sort by: (1) instance-token sequence, Unicode code-point order, shorter equal prefix first; (2) keyword rank `additionalProperties`, `required`, `const`, `type`, `minLength`, `maxItems`, then remaining keywords alphabetically; (3) schema-token sequence under the same ordering; (4) canonical JSON of `validator_value`, sorted object keys and compact separators. Emit the first error's instance pointer. For an assumptions clause-ID rejection, select the lowest numeric `assumptions` index that contains the first invalid `clause_id` and emit `/assumptions/<index>/clause_id`. For duplicate keys, invalid UTF-8, BOM, malformed envelope or JSON syntax, emit `SCHEMA_REJECT|pointer=/`.

**Authoritative failure-to-stage map.** The first applicable row after the exact evaluation order below controls. File-local syntax, tokenizer, import and module-body stages process `driver.py` before `checker.py`; source nodes within a file use ascending `(lineno, col_offset, end_lineno, end_col_offset)`. `AST_SIGNATURE` uses the separate required-symbol pass and global category sort key defined below, not a file-first source-order pass. `DECORATOR_REJECT` has error class `ENTRY_POINT_REJECT`; its diagnostic code remains `DECORATOR_REJECT`.

| First applicable failure | Stage ID | Error class | Diagnostic / disposition |
|---|---|---|---|
| Envelope, schema or clause manifest rejection | `PARSE_SCHEMA` | `SCHEMA_REJECT` | `SCHEMA_REJECT|pointer=<JSON_POINTER>`; repair |
| Provider finish reason explicitly reports max-token truncation | `PARSE_SCHEMA` | `OUTPUT_TRUNCATED` | `OUTPUT_TRUNCATED`; repair |
| Invalid UTF-8/BOM or syntax parse error | `SOURCE_AST` | `SOURCE_SYNTAX_REJECT` | Exact file/line/column template; repair |
| Empty/whitespace-only source | `SOURCE_AST` | `SOURCE_EMPTY` | `SOURCE_EMPTY|file=<FILE>`; repair |
| Disallowed import form/root, prohibited built-in, direct module-global random use, non-ASCII identifier or module-body policy violation | `IMPORT_POLICY` | `IMPORT_POLICY_REJECT` | Exact corresponding diagnostic; repair |
| Decorator, any `ast.AsyncFunctionDef`, any asynchronous comprehension expression at any lexical depth, invalid/missing/extra entry point, class/method/nesting violation, parameter mismatch, inspect-signature mismatch or factory returning non-Driver | `AST_SIGNATURE` | `ENTRY_POINT_REJECT` | `ENTRY_POINT_REJECT|file=<FILE>|symbol=<SYMBOL>|reason=<REASON>` or `DECORATOR_REJECT|file=<FILE>|symbol=<SYMBOL>`; repair |
| Driver compile error | `COMPILE_DRIVER` | `COMPILE_ERROR` | `COMPILE_ERROR|file=driver.py|line=<LINE>`; repair |
| Checker compile error | `COMPILE_CHECKER` | `COMPILE_ERROR` | `COMPILE_ERROR|file=checker.py|line=<LINE>`; repair |
| Driver factory or `step` raises during RTL or null baseline run | `DRIVER_RUNTIME` | `RUNTIME_EXCEPTION` | `RUNTIME_EXCEPTION|file=driver.py|phase=<PHASE>|class=<EXCEPTION_CLASS>`; repair |
| Driver return value/vector is invalid | `DRIVER_VECTOR` | `DRIVER_VECTOR_INVALID` | `DRIVER_VECTOR_INVALID|reason=<REASON>`; repair |
| Driver step watchdog expires | `DRIVER_WATCHDOG` | `WATCHDOG_TIMEOUT` | `WATCHDOG_TIMEOUT|phase=driver_step`; repair |
| Simulator error on RTL or null run | `DESIGN_HALT` | `EVALUATOR_INFRASTRUCTURE_FAILURE` | `SIMULATOR_ERROR|target=<RTL_OR_NULL>|class=<EXCEPTION_CLASS>`; halt design, repair evaluator and apply §7b; no model feedback |
| Harness trace-integrity fault | `DESIGN_HALT` | `TRACE_INTEGRITY_FAILURE` | `TRACE_INTEGRITY_FAILURE|reason=<REASON>`; halt design, repair evaluator and apply §7b |
| Before first raw output divergence, paired next-input schedules differ | `TERMINAL` | `DRIVER_NONDETERMINISM` | `DRIVER_NONDETERMINISM|reason=NEXT_INPUT_DIVERGENCE`; terminal-invalid slot; no repair |
| Same paired inputs produce a masked output divergence under the artifact's own stimulus | `DESIGN_HALT` | `RTL_NULL_CONTROL_FAILURE` | `RTL_NULL_CONTROL_FAILURE|reason=MASKED_OUTPUT_DIVERGENCE`; halt design and apply §7b |
| Both checker null runs have the same runtime exception, invalid-return code or timeout | `CHECKER_NULL` | Corresponding checker error | Exact checker diagnostic; repair |
| Both checker null runs return `FAIL` | `CHECKER_NULL_REJECT` | `CHECKER_NULL_REJECT` | `The checker returned FAIL on a legal null-netlist trace.`; repair |
| Both checker null runs return `PASS` | — | — | Validity check continues |
| Checker results differ in verdict, valid/error status, error code or exception class | `TERMINAL` | `CHECKER_NONDETERMINISM` | `CHECKER_NONDETERMINISM|reason=RUN_DISAGREEMENT`; terminal-invalid slot; no repair |
| Malformed diagnostic item with otherwise valid top-level return and verdict | — | — | Log `DIAGNOSTIC_FORMAT_WARNING`, discard item; `ACCEPT_WITH_WARNING`; verdict retained |

**Deterministic `ENTRY_POINT_REJECT` assignment and symbol naming.** `AST_SIGNATURE` runs only after all `IMPORT_POLICY` checks pass. First perform a required-symbol pass in this fixed sequence: (1) module-level `create_driver` in `driver.py`; (2) module-level `Driver` and its required class kind in `driver.py`; (3) direct `Driver.step` in `driver.py`; (4) module-level `check_trace` in `checker.py`. For each required function/method, count all same-name binding definitions at the required scope before inspecting parameters: zero bindings emit `MISSING_ENTRY_POINT`; more than one binding of any AST kind emits `EXTRA_ENTRY_POINT`; exactly one binding with the wrong AST kind emits `WRONG_ENTRY_POINT_KIND`; exactly one binding of the required kind proceeds to parameter checks in the order `PARAMETER_NAMES`, `PARAMETER_KIND`, then `DEFAULT_OR_VARIADIC`. For `Driver`, zero top-level bindings named `Driver` emits `MISSING_ENTRY_POINT`, more than one emits `EXTRA_ENTRY_POINT`, exactly one non-`ClassDef` binding emits `DRIVER_CLASS_FORM`, and exactly one class proceeds. For `Driver.step`, zero direct class-body bindings named `step` emits `MISSING_ENTRY_POINT`, more than one emits `EXTRA_ENTRY_POINT`, exactly one non-`FunctionDef` binding emits `WRONG_ENTRY_POINT_KIND`, and exactly one synchronous function proceeds. Only after every required symbol passes, perform one global remaining-structure pass over both files. Assign category ranks: (1) any nested class at any lexical depth → `NESTED_CLASS_FORBIDDEN`; (2) any other top-level class in `driver.py` or any class in `checker.py` → `CLASS_FORBIDDEN`; (3) `Driver.__init__` or any other direct `Driver` method besides `step` → `FORBIDDEN_METHOD`; (4) invalid `Driver` bases or metaclass keywords → `DRIVER_CLASS_FORM`; (5) any decorator on any function, class or method → `DECORATOR_REJECT` (error class `ENTRY_POINT_REJECT`); (6) any `ast.AsyncFunctionDef` at any lexical depth, including nested helper definitions → `ASYNC_DEFINITION`; (7) any `ast.GeneratorExp`, `ast.ListComp`, `ast.SetComp` or `ast.DictComp` that has at least one associated `ast.comprehension` with `is_async == 1`, or that contains an `ast.Await` node anywhere in its AST subtree → `ASYNC_COMPREHENSION`. Rank 7 is necessary because an async generator expression is not an `AsyncFunctionDef` and may occur in an ordinary synchronous function. Python treats a generator expression containing `await` as asynchronous even when every `comprehension.is_async` flag is 0; checking for any `ast.Await` node in the comprehension subtree closes that form and also gives all await-containing comprehension expressions one deterministic AST-stage owner. For each async-comprehension expression, use the expression node's own `(lineno, col_offset, end_lineno, end_col_offset)` as its source position. Define its `symbol` using AST ancestry: the dot-joined names of every ancestor `ast.FunctionDef`, `ast.AsyncFunctionDef` and `ast.ClassDef` of which the expression is a descendant, outermost first. This includes expressions in decorators, arguments, defaults, annotations, bases and keywords; it excludes lambda names and the expression itself. A `<module>` symbol cannot reach `AST_SIGNATURE` because module-body expressions are rejected earlier by `IMPORT_POLICY`. Select the first global violation using exactly `(category, file_order, lineno, col_offset, end_lineno, end_col_offset)`, where `category` is the numeric rank above and `file_order` is `0` for `driver.py`, `1` for `checker.py`. Do not run this category pass separately per file. Thus every rank 1–6 violation outranks every rank 7 async-comprehension violation; within a category `driver.py` precedes `checker.py`, then the earliest source position wins. `symbol` is a bare top-level name (`create_driver`, `Driver`, `check_trace`), `Driver.<method>` for a `Driver` method, dot-joined lexical enclosing names for a nested definition (for example `helper.Nested` or `helper.nested_async`), and dot-joined lexical enclosing definition names for an async-comprehension expression (for example `helper` or `check_trace`). For an async function definition, include its own name after all lexical enclosing names. M01 resolves to `Driver.__init__ / FORBIDDEN_METHOD`; M02 to `Helper / CLASS_FORBIDDEN`; M39 to `helper.Nested / NESTED_CLASS_FORBIDDEN`; M49 demonstrates required-symbol checks before the global category pass; M51 and M52 test category precedence within one file and across both files; M59 tests a nested async function definition. This priority is normative.

**Deterministic evaluation order.** (1) Response UTF-8/JSON/schema/manifest-clause checks. (2) Source UTF-8/BOM/empty/syntax checks in file order `driver.py`, then `checker.py`. (3) For each file in order `driver.py`, then `checker.py`: after successful `ast.parse`, scan `tokenize.NAME` and identifier-relevant `tokenize.ERRORTOKEN` tokens using the complete non-ASCII identifier rule above; reject the first identifier lexeme containing a non-ASCII code point before classifying imports, prohibited names or module-body statements in that file. If the identifier scan passes, complete that file's import, prohibited-name and module-body checks before advancing to the next file. AST import nodes use ascending source-position order and the per-node import precedence above. A function or class definition itself is deferred to `AST_SIGNATURE`. (4) `AST_SIGNATURE`: first validate required symbols in the fixed sequence `driver.py:create_driver`, `driver.py:Driver`, `driver.py:Driver.step`, `checker.py:check_trace`; only if all pass, evaluate remaining structure across both files using exactly `(category, file_order, lineno, col_offset, end_lineno, end_col_offset)` and the seven category ranks in the preceding paragraph. This is a global category pass, not a per-file pass; nested classes in either file outrank decorators or other lower-priority categories in either file. (5) Compile `driver.py`. (6) Compile `checker.py`. (7) Execute `create_driver(seed)` and `Driver.step` on original RTL, then on null netlist; within each cycle, exception wins over vector validation, which wins over watchdog when observed at the same checkpoint. Factory return type and runtime signatures are checked immediately after factory construction. (8) Compare the two completed traces: compare raw outputs before that row's next-input decision; any next-input mismatch before first raw-output divergence is terminal driver nondeterminism; a same-input masked output divergence is a design halt. (9) Run checker null invocation 1 on the immutable null trace. (10) Run checker null invocation 2 in a separate process on the same immutable trace, even if invocation 1 errors. (11) Adjudicate both checker outcomes: both PASS continues; both FAIL triggers repair; identical error code and exact diagnostic bytes triggers checker repair; any disagreement is terminal. The same checker error means identical error code and identical diagnostic bytes, including exception class/reason/phase. A checker timeout is `CHECKER_TIMEOUT|phase=null_check`; a checker process exception is `CHECKER_RUNTIME_ERROR|class=<EXCEPTION_CLASS>`; an invalid checker return uses the ordered `CHECKER_RETURN_INVALID|reason=<REASON>` enumerations above.

**Feedback serialization.** The serializer accepts only a complete diagnostic emitted by the authoritative stage map. It does not rewrite, substitute or normalize diagnostic content; a path-bearing or otherwise non-normative diagnostic fails the closed-grammar check and is not sent. When the set of diagnostics the stage map emitted is given, a diagnostic that passes the grammar but is not in that set is also rejected at step (1), with the same `FEEDBACK_SERIALIZER_REJECT|reason=NON_NORMATIVE_DIAGNOSTIC`. Apply operations in this exact order: (1) validate the complete, untruncated diagnostic against the normative closed grammar and its enumerated values; (2) if its UTF-8 byte length exceeds 2,048, truncate the diagnostic string to the longest prefix ending at a complete UTF-8 code-point boundary whose byte length plus the UTF-8 byte length of `...[TRUNCATED]` is no greater than 2,048, then append that marker; the marker is included inside the 2,048-byte cap, and output need not fill the cap; (3) JSON-escape and serialize the three-key object. Do not re-run grammar validation after truncation because truncation can end inside a field value; the pre-truncation diagnostic is the value tested against the grammar. The dynamic JSON object has exactly three keys in order `stage_id`, `error_class`, `diagnostic`. Serialize UTF-8 with `ensure_ascii=false`, two-space indentation, LF line endings, exactly one final LF and the same key order. Retain `[VALIDATION_FEEDBACK_JSON]`. Replace `{{STAGE_ID}}` and `{{ERROR_CLASS}}` with JSON string contents (without outer quotes), and `{{DIAGNOSTIC_JSON_STRING}}` with a complete JSON string literal. No raw exception text, validator/compiler message, file path, trace/output value or arbitrary free-form content is sent to the model. A truncation-primitive vector applies step (2) alone to its input string and reports `contains_marker` (whether the output ends with the marker), `valid_utf8` (whether the output bytes are valid UTF-8), `output_diagnostic_bytes` (the output's UTF-8 byte length) and `marker_utf8_bytes` (the marker's UTF-8 byte length). A JSON-escaping-primitive vector applies step (3) alone to its three-key object and reports `diagnostic_utf8` (the serialized text), `diagnostic_sha256` (the lowercase hexadecimal SHA-256 of its UTF-8 bytes) and `diagnostic_bytes` (their number).

**F18-only disposition and error vocabulary (not model feedback).** `F18` and packet-freeze checks use these outcomes only in local test ledgers; they are never inserted into a model repair message:
- Dispositions: `ACCEPT`, `ACCEPT_WITH_WARNING`, `REPAIR`, `TERMINAL_INVALID_NO_REPAIR`, `DESIGN_HALT_NO_SLOT_SCORED`, `DESIGN_ABORTED_NO_SLOTS_SCORED`, `CONTROL_EXPECTATION`, `F18_REJECT`.
- Stages: `PARSE_SCHEMA`, `SOURCE_AST`, `IMPORT_POLICY`, `AST_SIGNATURE`, `COMPILE_DRIVER`, `COMPILE_CHECKER`, `DRIVER_RUNTIME`, `DRIVER_VECTOR`, `DRIVER_WATCHDOG`, `PAIRED_RUN_CONTROL`, `CHECKER_NULL`, `CHECKER_NULL_REJECT`, `TERMINAL`, `DESIGN_HALT`, `FEEDBACK_SERIALIZER`, `F18`.
- F18/packet diagnostics: `PACKET_FREEZE_REJECT|reason=RESERVED_HEADING_LINE`, `ASSEMBLY_REJECT|reason=UNRESOLVED_PLACEHOLDER`, `F18_REJECT|reason=VISIBLE_CLAUSE_ID_SET_MISMATCH`, `F18_REJECT|reason=MALFORMED_CLAUSE_ID_TOKEN`, `FEEDBACK_SERIALIZER_REJECT|reason=NON_NORMATIVE_DIAGNOSTIC`.
- F18/local-ledger error classes: `F18_REJECT` fixtures use error class `ASSEMBLY_OR_MANIFEST_FAILURE`. A truncation-primitive vector uses error class `TRUNCATION` and a JSON-escaping-primitive vector uses error class `JSON_SERIALIZATION`; both are recorded at stage `FEEDBACK_SERIALIZER` with disposition `CONTROL_EXPECTATION`. **OWNER-DECIDED OD-1** (owner decision D-027; v1.3.6 does not state it): a stage-map row with a single diagnostic code and no stated error class has the error class equal to that diagnostic code; the `SIMULATOR_ERROR` row, whose stated error class is `EVALUATOR_INFRASTRUCTURE_FAILURE`, is the stated exception. An error-class cell `—` states that a row has no error class, so OD-1 does not apply to it. OD-1 decides exactly two error classes, those of the local-ledger rows `FEEDBACK_SERIALIZER_REJECT` and `DESIGN_HALT_REPEATED`; every other row of the stage map and of this vocabulary states its error class. By OD-1, `FEEDBACK_SERIALIZER_REJECT|reason=NON_NORMATIVE_DIAGNOSTIC` is recorded at stage `FEEDBACK_SERIALIZER` with error class `FEEDBACK_SERIALIZER_REJECT` and disposition `CONTROL_EXPECTATION`. These are local F18 ledger labels, never model feedback.
- **Closed design-lifecycle/control vocabulary (local ledger only; never model feedback).** `DESIGN_HALT_REPEATED|reason=EVALUATOR_FAILURE_REPRODUCED` means the same halt signature recurred after the single recovery cycle; `DESIGN_HALT_REPEATED|reason=SECOND_HALT_AFTER_RECOVERY` means a different design halt occurred after that recovery; `EVALUATOR_REVISION_REQUIRED|reason=FROZEN_EVALUATOR_CHANGED` means a frozen evaluator source/binary/tool-version/command/option/configuration changed; `AUTHORING_REVISION_REQUIRED|reason=AUTHOR_VISIBLE_OR_ESTIMAND_CHANGED` means an author-visible or estimand-defining item changed and prior confirmatory artifacts are not reusable; `HALT_SIGNATURE_SCHEMA|reason=COMPONENT_VALUES_ENUMERATED` is the `M54` control-expectation diagnostic for validating the closed halt-signature component domains and mapping; and `RERUN_ALL_SCHEDULED_SLOTS_WITH_SAME_FROZEN_ARTIFACTS` (error class `MID_RUN_REEVALUATION`) is the M41 control-expectation diagnostic for a successful operational recovery. It discards pre-halt scores, reruns preflight, and re-evaluates every scheduled slot in the affected scope with identical artifact bytes and seeds and zero new confirmatory generation calls. Error classes of change-class control expectations are stated by rule, not by fixture: a control expectation whose diagnostic CODE is `EVALUATOR_REVISION_REQUIRED` has error class `EVALUATOR_REVISION_REQUIRED`; one whose CODE is `AUTHORING_REVISION_REQUIRED` has error class `AUTHORING_REVISION_REQUIRED`; and one whose CODE is `HALT_SIGNATURE_SCHEMA` has error class `HALT_SIGNATURE_SCHEMA`. This rule applies only to these three codes; it does not change the M41 error class `MID_RUN_REEVALUATION` or any stage-map row. The study-reset vector uses diagnostic `AUTHORING_REVISION_REQUIRED|reason=AUTHOR_VISIBLE_OR_ESTIMAND_CHANGED`; the halt-signature vector uses diagnostic `HALT_SIGNATURE_SCHEMA|reason=COMPONENT_VALUES_ENUMERATED`. All these lifecycle/control diagnostics are local evaluator/F18 ledger values and are never serialized to an LLM or inserted into model feedback.
- **Closed `required_action` literals, by change class and, for `HALT_SIGNATURE_COMPONENT_ENUMERATION`, by domain validation (OD-3):** `FROZEN_EVALUATOR_SOURCE_BINARY_OR_CONFIG_CHANGED` = `new_evaluator_hashes_then_F16_then_rerun_every_slot_in_affected_scope_with_same_frozen_artifact_bytes_no_new_confirmatory_generation`; `SHARED_AUTHOR_VISIBLE_OR_ESTIMAND_DEFINING_ITEM_CHANGED` = `halt_study_invalidate_all_designs_and_all_arm_x_design_slots_archive_and_disclose_partial_confirmatory_ledgers_new_preregistration_refreeze_f16_and_fresh_confirmatory_generation`; `DESIGN_MEMBERSHIP_OR_ESTIMAND_OR_WEIGHT_CHANGED_AFTER_CONFIRMATORY_START` = `archive_and_disclose_all_partial_confirmatory_ledgers_new_preregistration_refreeze_new_design_set_and_weights_F16_then_generate_fresh_slots`; `HALT_SIGNATURE_COMPONENT_ENUMERATION` = `enforce_design_id_halt_code_evaluator_component_stable_error_class_stable_diagnostic_code_domains_and_reason_to_component_mapping; exclude timestamps_process_ids_attempts_hosts_and_trace_row_indices`; and `DESIGN_SPECIFIC_AUTHOR_VISIBLE_ITEM_CHANGED` = `halt_affected_design_invalidate_both_arm_slots_refreeze_design_specific_materials_archive_partial_ledgers_generate_fresh_confirmatory_slots_for_affected_design`. Each literal is a closed local control expectation, not a model-feedback diagnostic. The change classes are closed and have exactly four cases (OWNER-DECIDED OD-3): `FROZEN_EVALUATOR_SOURCE_BINARY_OR_CONFIG_CHANGED` is the evaluator revision of §7b path (b); `SHARED_AUTHOR_VISIBLE_OR_ESTIMAND_DEFINING_ITEM_CHANGED` is a shared-item revision; `DESIGN_MEMBERSHIP_OR_ESTIMAND_OR_WEIGHT_CHANGED_AFTER_CONFIRMATORY_START` is a study reset; and `DESIGN_SPECIFIC_AUTHOR_VISIBLE_ITEM_CHANGED` is a design-specific revision while membership, estimand and weights remain unchanged. `HALT_SIGNATURE_COMPONENT_ENUMERATION` is not a change class: it names the halt-signature domain validation (§7b, L185). Closed scope tokens (OWNER-DECIDED OD-3: owner vocabulary adopted by owner decision D-027; the spellings are not v1.3.6 text, and each token means the §7b text cited with it): for an evaluator revision, `rerun_scope_rule` = `shared_evaluator_component_all_designs_and_all_arm_x_design_slots; design_specific_component_affected_design_in_both_arms` (§7b: shared component, both designs and every slot; design-specific component, that design in both arms). For a shared-item revision, `affected_slots` = `all_designs_x_all_arms` (§7b: every scheduled slot across both designs and both arms). For a design-specific revision, `affected_scope` = `affected_design_in_both_arms` and `unaffected_design_scope` = `not_invalidated_when_membership_estimand_and_weights_are_unchanged`. An evaluator revision re-evaluates the affected scope with the same frozen artifact bytes and zero new confirmatory generation calls. A shared-item revision invalidates all designs and all arm × design slots and starts a new preregistered study. A study reset resets the preregistered design set and weights and requires fresh confirmatory slots. A design-specific revision invalidates both arms for the affected design only when membership, estimand and weights remain unchanged. The input contract and the complete result schema of every control vector are the normative tables of §20 (OWNER-DECIDED OD-3).
- A `CONTROL_EXPECTATION` fixture exercises a serializer, parser, protocol or lifecycle rule; its stage and expected diagnostic are test labels, not an artifact feedback event.

**Design-level baseline gate (§7a).** Before slots are scheduled, the reference driver and directed legal-input baseline must pass original-RTL/null equivalence under the frozen mask. Any baseline mismatch halts the design before slots exist; no slot is scored. It is recorded at stage `DESIGN_HALT` with error class `RTL_NULL_CONTROL_FAILURE`, diagnostic `RTL_NULL_CONTROL_FAILURE|reason=MASKED_OUTPUT_DIVERGENCE` and disposition `DESIGN_HALT_NO_SLOT_SCORED`.

**Mid-run design halt (§7b).** A *design* is FIFO or UART; an *arm* is ORG-A or ORG-B; a *slot* is exactly one arm × design combination. A *shared study item* is any common system prompt, common repair prompt, response schema, shared driver/checker API, parser/assembly contract, feedback trigger/policy/grammar/whitelist/cap/serializer, or other byte-identical or estimand-defining item shared by FIFO and UART. A design-specific item includes that design's specification/clauses, port manifest, reset/legal-input assumptions, execution envelope, trace schema, design-specific payloads, mask/strict-mask, RTL/netlist or design-specific mutant population. If any shared study item changes after confirmatory generation begins, halt the entire study and invalidate every scheduled slot across both designs and both arms: FIFO × ORG-A, FIFO × ORG-B, UART × ORG-A and UART × ORG-B. Do not limit the halt to the currently executing design. If a design-specific author-visible item changes, halt and invalidate every slot for that design in both arms. No invalidated confirmatory artifact may be reused. Preserve and archive every partial confirmatory ledger, slot, artifact, generation/repair history and seed; disclose the archived partial ledgers and the reason for invalidation in the new preregistration. A shared-item revision requires a new study preregistration, complete refreeze of affected shared and design materials, fresh eligibility work under the new packet, and fresh confirmatory generation for every affected slot. A change in design membership, estimand or any confirmatory weight after confirmatory generation starts always requires a new preregistered study, even if the changed item is otherwise described as design-specific; archive and disclose all partial confirmatory ledgers and generate fresh confirmatory slots under the newly preregistered design set and weights. A study reset is not an operational recovery and cannot retain old confirmatory artifacts.

For a design-local simulator error, evaluator trace-integrity fault or same-input masked RTL/null divergence after slots have begun, pause the affected design immediately and preserve every slot's frozen artifact, generation/repair history, seed and partial ledger rows. One recovery cycle per affected design is allowed. The recovery cycle has two mutually exclusive forms: (a) **operational recovery**, which restarts/re-provisions a failed worker or simulator process using the exact same frozen source, binaries, tool versions, command-line options, configuration, container image, RTL/netlist, harness, recorder, parser, mask and design inputs; it creates no new hashes, requires no new F16 and changes no artifact; or (b) **evaluator revision**, which changes any frozen evaluator source, binary, tool version, command, option or configuration (including simulator, harness, recorder, parser or sandbox). An evaluator revision is not an operational restart: assign a new evaluator version and hashes, run the frozen F16 eligibility procedure with fresh mutant-blind pilot seeds, update the run manifest, and only then re-evaluate every scheduled slot in the affected scope using the same already-generated artifact bytes and no new confirmatory generation calls, provided all author-visible and estimand-defining items remain unchanged. If the revised evaluator component is shared across FIFO and UART, the affected scope is both designs and every arm × design slot; if it is design-specific, the affected scope is that design in both arms. A change to any author-visible or estimand-defining item follows the study/design revision rules in the preceding paragraph, not the evaluator-revision path. A masked RTL/null divergence may use operational recovery only when a documented root-cause review attributes it to a transient evaluator fault; if the cause is a specification, mask, RTL or netlist defect, it requires a design-specific revision (or study-wide revision where a shared item or estimand is affected) and fresh generation rather than an operational restart.

After one permitted recovery cycle succeeds, rerun the full preflight and re-evaluate every scheduled slot in the affected scope, including the triggering slot and all previously evaluated slots, with the same frozen artifact bytes and slot seeds; no confirmatory generation call is made. Discard all pre-halt partial scores and use only the complete post-recovery rerun ledger. Define the **halt signature** as `(design_id, halt_code, evaluator_component, stable_error_class, stable_diagnostic_code)`. Its components have these exact domains: `design_id` is `FIFO` or `UART`; `halt_code` is `SIMULATOR_ERROR`, `TRACE_INTEGRITY_FAILURE` or `RTL_NULL_CONTROL_FAILURE`; `evaluator_component` is `SIMULATOR`, `REPLAY_VERIFIER`, `RECORDER`, `TRACE_ALIGNMENT_CHECKER`, `TRACE_SERIALIZER` or `RTL_NULL_COMPARATOR`; `stable_error_class` is a simple exception class name matching `[A-Za-z_][A-Za-z0-9_]*` for `SIMULATOR_ERROR` and the literal `NONE` for the other two halt codes (rule token `stable_error_class_rule` = `simple_exception_class_for_SIMULATOR_ERROR_else_NONE`); `stable_diagnostic_code` is exactly the corresponding `halt_code` token (rule token `stable_diagnostic_code_rule` = `exact_halt_code_token`). A supplied halt signature with any component outside these domains is an evaluator input error; it is never compared for recurrence. Such an input is outside the executable fixture contract: it is not an outcome, has no diagnostic, stage, error class or disposition, and produces no ledger record. For `TRACE_INTEGRITY_FAILURE`, map reasons `REPLAY_HASH_MISMATCH` → `REPLAY_VERIFIER`, `MALFORMED_RECORDER_OUTPUT` → `RECORDER`, `ROW_ALIGNMENT` → `TRACE_ALIGNMENT_CHECKER`, and `UNTRUSTED_TRACE_SERIALIZATION` → `TRACE_SERIALIZER`. `SIMULATOR_ERROR` maps to `SIMULATOR`; `RTL_NULL_CONTROL_FAILURE` maps to `RTL_NULL_COMPARATOR`. Timestamps, process IDs, attempt numbers, host names and trace row indices are not signature components. If the identical halt signature recurs after recovery, terminate with `DESIGN_HALT_REPEATED|reason=EVALUATOR_FAILURE_REPRODUCED`. If any different design halt occurs after the one recovery cycle, terminate with `DESIGN_HALT_REPEATED|reason=SECOND_HALT_AFTER_RECOVERY`. Both terminations are recorded at stage `DESIGN_HALT` with error class `DESIGN_HALT_REPEATED` (OWNER-DECIDED OD-1, §3.4 local-ledger error classes). No second recovery cycle is permitted. **OWNER-DECIDED OD-4** (owner decision D-027; v1.3.6 does not define it): the *evaluator repair attempt* of a design halt, `evaluator_repair_attempt`, is the ordinal of the recovery cycle that halt opens. A halt that occurs while the design has used no recovery cycle opens its one permitted cycle and has `evaluator_repair_attempt` = `1`. A halt that occurs after that cycle has been used would open a second cycle, which is not permitted: it is not a new attempt but the `DESIGN_HALT_REPEATED` termination above (by recurrence of the identical signature, or as a different halt). No ordinal greater than `1` is valid. The ordinal is a lifecycle count, not a halt-signature component. In either terminal case, mark every scheduled slot in the affected scope `DESIGN_ABORTED_NO_SLOTS_SCORED`; do not drop a design, reweight the confirmatory estimand or report a confirmatory H2 result for an incomplete fixed design set.

Null-trace rejection is oracle-guided repair even though expected values are withheld; report initial-call validity and final post-repair validity separately. Every P, R and M fixture listed in `36_F18_Parser_and_Repair_Fixture_Catalog_v1.3.7-candidate.md` is mandatory for F18. M14 and M17 are explicitly grammar-exempt primitive unit vectors: M14 tests the UTF-8 truncation function in isolation, and M17 tests JSON escaping in isolation. Their deliberately non-grammar strings are not accepted by the full production feedback pipeline; the production serializer still rejects non-normative diagnostics at its initial grammar-validation step.

### 3.5 LLM sampling

At least 10 independently initiated calls per arm/design is a feasibility floor only. Each scheduled call is a separate sample; repair attempts are nested within the original slot and do not increase `n`. Record provider/model/version, call date, prompt hashes, tokenizer ID/version, temperature, top-p, token limits, output, feedback, repair history and cost. A subscription UI is not assumed to provide API access; the generation route must be recorded before sampling.

## 4. Benchmarks and specification requirements

| Design | Role | Specification requirements |
|---|---|---|
| Synchronous FIFO | Feasibility design and main benchmark | Cycle-exact reset, write/read, simultaneous operations, full/empty, valid/data, overflow/underflow and output timing |
| UART transmitter | Main benchmark | Cycle-exact baud/tick, framing, start/stop bits, reset, busy/ready and transmit timing |
| FSM controller | Deferred; excluded from the v1.3 confirmatory set | Adding it requires an owner decision, a revised estimand and a new freeze before F16 |
| 8-bit ALU | Smoke test only | Exact opcode, widths, wraparound, flags and invalid-opcode semantics |

Use the FIFO for the feasibility vertical slice. The ALU does not exercise reactive handshake, don't-care windows or invalid-pair logic. All MVP specs must be cycle-exact. Variable latency is out of scope; an observation mask cannot align arbitrary timing shifts.

## 5. Driver/checker contract

### 5.1 Driver API

The harness owns the clock and scheduler. The module exposes `create_driver(seed)`; the harness calls it exactly once to obtain a `Driver`. The `Driver.step(cycle_index, outputs_after_edge)` method is invoked once per active cycle. Its first call is after reset release, with `cycle_index=0` and the public-output snapshot sampled after the reset-release active edge. Each later call receives the most recent post-edge snapshot and the next integer cycle index. It returns either:
- a complete next-cycle input dictionary; or
- `COMPLETE`, after which the harness drives safe-idle inputs until the fixed cycle cap.

Drivers must not create free-running Cocotb coroutines, wait on `Timer`/edges, own the clock, inspect internal signals, access simulator handles directly, use more than one drive per cycle, or obtain unseeded entropy. The same API and instructions are given to human and LLM authors. The harness calls `create_driver(seed)` exactly once and does not seed global `random`; generated driver code must use a local `random.Random(seed)` instance. NumPy is not used. Forbid `time`, `os.urandom`, environment-derived, filesystem, network, subprocess or other unseeded entropy sources. Every non-`COMPLETE` return must be a dictionary with exactly the frozen top-level input-port keys; every value is a string of the declared width containing only `0` and `1`; X/Z, missing/extra keys, wrong widths and any design-specific illegal input combination are rejected before driving.

### 5.2 Cycle alignment and sampling

For trace row `n`, record three separate fields:
- `inputs_consumed_at_edge_n`: top-level inputs stable immediately before active rising edge `n`;
- `outputs_after_edge_n`: top-level outputs sampled in Cocotb `ReadOnly` after edge `n` settles;
- `next_inputs_scheduled_for_edge_n_plus_1`: the vector returned by the driver after it receives `outputs_after_edge_n`, then applied by the harness in the designated drive phase before edge `n+1`.

The harness—not test code—owns the clock, scheduler and recorder. Ordering is mandatory: sample outputs first, invoke the driver second, record its next-input vector third, drive it before the next active edge. This prevents combinational outputs from being sampled after next inputs have already changed. For pair validity, compare each row's next-input vector after comparing that row's raw outputs. A next-input difference in the same row as the first raw output divergence is output-first; a difference in an earlier row makes the pair invalid. The consumed-input field is retained for audit and must agree with the prior row's scheduled input; the initial reset inputs are defined in the design pack.

Preserve four-state `0`, `1`, `X`, `Z` values distinctly. Record cycle index, reset, consumed inputs, post-edge outputs, next-input decision, driver completion state and run status. Preserve an FST/VCD waveform audit file where supported. F2/F10 must prove the actual ordering before any research run.

### 5.3 Completion and comparison window

All artifacts use the same design-specific fixed cycle cap. If a driver returns `COMPLETE`, the harness records `driver_completed=true` and supplies the fixed safe-idle vector for the remaining cycles. The checker evaluates the entire trace through the cycle cap. There is no per-artifact alternative completion policy. If the driver has not completed at the cap, record `driver_completed=false`; reaching the cap is a normal end, not a timeout.

A wall-clock timeout is separate. A driver waiting for a ready/valid event runs to the cap; a Python loop that prevents clock progress may trigger the watchdog. Cycle cap, safe-idle vectors and timeout formula are **TO FREEZE** after feasibility validation.

## 6. RTL, null netlist and mutant export

The null-mutant netlist is generated from the original RTL by exactly the same synthesis/export script, tool versions and top-level interface as the mutant netlists, with no mutation applied. Export must preserve top module name and public ports. Run the export twice and compare null-netlist hashes.

Use MCY/Yosys for candidate netlist signal mutant generation and supported equivalence work only. OpenVEF's own orchestrator runs the artifact-by-mutant matrix. Do not use MCY batch mode. Verify whether the pinned MCY version exports each mutant outside its own runner; if it does not, test Yosys `mutate` plus `write_verilog` as the fallback. Record the exact commands, mutation modes, affected netlist objects, tool versions and exported hashes.

The primary population is called **structural netlist signal mutants**. MCY documents its mutations as modifications to individual signals in a post-synthesis netlist; this is structurally closer to netlist fault simulation than to source-level RTL design-error mutation. It is not automatically a manufacturing stuck-at fault model. Do not call these mutants stuck-at-0/1 or physical silicon faults unless the exact modes generated by the pinned version are inspected and shown to implement those semantics. The raw/masked trace comparison is the fault-simulation/exposure layer; the offline checker verdict is the qualification-like detection layer. Source-level operator/condition/missing-case mutants remain deferred to a separate fault population.

## 7. RTL-versus-null control and artifact validity

Every artifact is run on the original RTL and on the null-mutant netlist. For a scheduled artifact, compare outputs first within each row, then compare that row's scheduled next-input vector. A next-input schedule divergence before any raw output divergence is an artifact-level `DRIVER_NONDETERMINISM` terminal-invalid slot and receives no repair. A masked output divergence under identical inputs is a design-level `RTL_NULL_CONTROL_FAILURE` and halts the design; it is not charged to the artifact. Any post-start halt follows the exact one-recovery/refreeze rules in §3.4 and §7b. Simulator errors and harness/trace-integrity faults also halt the design and are repaired at the evaluator level, not reported as artifact errors. Any X/Z on an always-observable output or mask-predicate signal in a null run blocks design validation.

### 7a. Design-level RTL/null preflight

Before any scheduled artifact slot, run the frozen reference driver and directed legal-input baseline on original RTL and the null netlist. If masked outputs differ under identical inputs, or an always-observable null output/predicate is X/Z, halt the design before slots are scheduled. The design must be repaired and revalidated with the full preflight suite before any slot runs. No scheduled slot is scored during a failed design preflight.

Every artifact is also run on the null netlist. It must parse, satisfy the API, compile, execute under the cycle cap/watchdog and pass the offline checker on the archived null trace. The same checker is then invoked in a second independent process on that exact immutable trace; both invocations must return `PASS`. A checker `FAIL` on both null runs, identical checker runtime/invalid-return/timeout errors, driver runtime errors, invalid driver vectors and driver watchdogs are repair triggers under §3.4. Checker nondeterminism and driver input-schedule nondeterminism are terminal-invalid. Simulator or harness errors halt the design and are never repaired through the LLM feedback path. Repairs are nested within the scheduled slot.

### 7b. Mid-run design halt

The complete pause, evaluator-repair, full-design rerun, no-new-generation and repeated-failure policy is normative in §3.4 “Mid-run design halt”. Affected slots are not final-scored until all scheduled artifacts for the design have been re-evaluated.

## 8. Paired-run method

Open-loop input replay is not the primary method because reactive sequential drivers may legitimately change future inputs after observing outputs.

For each valid artifact and each primary candidate mutant:
1. execute the same deterministic driver on the null netlist;
2. execute the driver independently on the mutant;
3. use identical seed, reset, simulator, cycle cap, safe-idle, driver API and watchdog;
4. allow the driver to react to the outputs of the implementation it is currently running on;
5. capture `inputs_consumed_at_edge_n` and `outputs_after_edge_n` passively, and record the driver-returned `next_inputs_scheduled_for_edge_n_plus_1` in the same row;
6. compare the two traces row by row.

Before the first raw output divergence, paired next-input decisions must match. After a raw output divergence, later next-input differences are allowed because the driver may react to the differing output. Within each row, raw outputs are compared before the next-input decision; a same-row divergence is output-first. A next-input divergence in an earlier row is `INVALID_PAIR`.

## 9. Observation mask and traceability

For each design, the evaluator/mask reviewer derives, versions and hashes the mask from the cycle-exact specification before any artifact is written or generated. The mask is not included in authoring packets.

**Required mask-to-specification traceability table.** Every mask entry must map to an explicit specification clause ID and a readable clause excerpt. For every don't-care window, the specification authors receive must itself state the don't-care condition and its scope. A mask entry with no explicit specification clause is a specification defect and blocks design freeze; it cannot be treated as a hidden evaluator preference. The table is signed by an independent mask reviewer and is checked in F18.

- The mask predicate is evaluated using the null-netlist trace for both members of a pair.
- Every predicate signal (for example `valid`) is itself always observable and compared; a mutant cannot hide a changed predicate by masking a dependent data field.
- Data fields may be masked only in explicitly documented don't-care windows.
- Reset/initialization windows are explicit in the specification and traceability table.
- X/Z on an always-observable output or predicate in a null trace fails design validation.
- The same mask and legal-input assumptions are used by the trace comparator and bounded-equivalence miter.
- A stricter-mask sensitivity variant is independently reviewed and applied to archived traces. Its predicate set/hash is **TO FREEZE**.
- The MVP is cycle-exact; the mask cannot permit arbitrary latency shifts.

## 10. Offline checker contract and trace format

The checker is an isolated synchronous function `check_trace(trace, metadata)` run in a separate process after simulation on an immutable serialized trace. It receives no simulator objects, live DUT handles, RTL source, mutant identity, driver seed, stimulus list, observation mask, reference model/API or expected-output table. `metadata` contains exactly: `design_id` (string), `spec_version_sha256` (64-character lowercase hexadecimal string), `trace_schema_version` (string), `cycle_cap` (positive integer), `reset_release_cycle` (non-negative integer) and `trace_integrity_status` (literal `VALID`). It excludes the driver seed and stimulus list.

The return value is a dictionary with exactly two top-level keys: `verdict` and `diagnostics`. `verdict` is exactly `PASS` or `FAIL`. `diagnostics` is required and must be a list; an empty list is valid. A well-formed diagnostic item has exactly `code` (string), `message` (string), `cycle` (integer or null) and `clause_id` (string or null). A malformed diagnostic item is logged as `DIAGNOSTIC_FORMAT_WARNING` and discarded; it does not change the verdict or create a checker error. A missing/non-list diagnostics field, missing/extra top-level key, invalid verdict, non-dictionary return or process crash is a checker error. Only the `PASS`/`FAIL` verdict determines acceptance. The same immutable null trace is evaluated twice in separate processes; both verdicts must be `PASS` and agree.

Expected values are derived from the design specification and the trace's recorded inputs and legitimate prior public-output/history fields. The checker may not call an executable reference model/API, read evaluator-only expected-output tables, inspect internal signals or depend on artifact-specific literal stimulus sequences. Because prior DUT outputs can themselves be faulty, history-derived expectations may accept self-consistent corruption; this is a known weakness the metrics should expose, not an anomaly label. The exact parser, AST, inspect, import and vector rules are in `30_Response_Parser_and_Execution_Contract_v1.3.7-candidate.md` and must be repeated in the model-visible authoring packet.
## 11. Mask-aware bounded equivalence and candidate labels

Build the miter with the same observation mask as the trace comparator and with the same reset sequence and legal-input assumptions from the design specification. Freeze those assumptions with the design pack.

Use bound `N` no greater than the design cycle cap. Record the shortest counterexample length where one is found. Candidate labels:
- `NON_EQUIVALENT_WITHIN_N`: a legal-input, masked-output counterexample is found within N cycles.
- `BOUNDED_EQUIVALENT_N`: no such counterexample is found through N cycles; this is not unbounded proof.
- `UNDECIDED`: solver/resource limit prevents a classification.
- `OUT_OF_BUDGET_COUNTEREXAMPLE`: a separate diagnostic search finds a first relevant counterexample only beyond the fixed cycle cap; report separately and exclude from primary population.

Only `NON_EQUIVALENT_WITHIN_N` candidates enter the primary mutant denominator. Report all candidate labels, counts, assumptions, BMC depth and exclusions. N, solver and timeout are **TO FREEZE**. MCY's BMC pass must not be described as unbounded formal equivalence.

## 12. Pair outcome partition and classification precedence

Every scheduled slot × primary-mutant combination receives exactly one ledger outcome. For valid artifacts, apply this precedence:

1. `INVALID_PAIR`: next-input schedules diverge before any raw output divergence, or a predeclared determinism/integrity rule is violated.
2. Driver/simulator error, split by whether a masked divergence was recorded before termination.
3. Wall-clock timeout, split by whether a masked divergence was recorded before timeout.
4. Offline checker error, split by whether a masked divergence was recorded on the complete trace.
5. Normal-completion outcomes and anomalies.

**Integrity adjudication for `ANOMALY_PIPELINE_OR_NONDETERMINISM`.** A predeclared harness/trace-integrity failure (for example, replay hash mismatch, malformed recorder output, row alignment failure or untrusted trace serialization) reclassifies the pair as `INVALID_PAIR` under precedence rule 1. A checker-attributable failure (for example, different checker verdicts on byte-identical complete traces) remains in `T_i` and is counted as a checker/pipeline anomaly, not exposure or detection. If the cause cannot be determined from predeclared integrity evidence, classify conservatively as `INVALID_PAIR`. Report harness/trace-integrity and checker-attributable counts separately; do not adjudicate based on prompt arm or desired metric direction.

Normal outcomes:
- `DETECTED`: complete trace; masked divergence; checker returns `FAIL`.
- `PND`: complete trace; masked divergence; checker returns `PASS`.
- `NP`: complete trace; no masked divergence; checker returns `PASS`.
- `ANOMALY_PIPELINE_OR_NONDETERMINISM`: checker returns `FAIL` with no raw output divergence.
- `ANOMALY_CHECKER_STRICTER_THAN_MASK`: raw divergence exists, no masked divergence exists, and checker returns `FAIL`.

Error/timeout outcomes:
- `DRIVER_SIM_ERROR_NO_MASKED_DIVERGENCE`
- `DRIVER_SIM_ERROR_AFTER_MASKED_DIVERGENCE`
- `CHECKER_ERROR_NO_MASKED_DIVERGENCE`
- `CHECKER_ERROR_AFTER_MASKED_DIVERGENCE`
- `TIMEOUT_WITHOUT_MASKED_DIVERGENCE`
- `TIMEOUT_AFTER_MASKED_DIVERGENCE`

A driver/simulator error or timeout produces a truncated trace and is excluded from the primary complete-trace conditional diagnostics. A checker error occurs only after a complete trace and is included in the complete-trace denominator. Checkers are never run on truncated traces. `CHECKER_ERROR_AFTER_MASKED_DIVERGENCE` counts as exposed for `E_i`, but as not detected for `S_i` and `J_detection`. Truncated execution after a recorded masked divergence is excluded from the primary exposure numerator and reported in a separate one-sided sensitivity analysis. Invalid artifacts are represented by an `INVALID_ARTIFACT_SLOT` ledger state for every scheduled mutant combination.

### 12.1 Cycle cap and timeout

- Reaching the cycle cap is normal termination; the checker is run on the complete trace.
- A wall-clock watchdog firing is `TIMEOUT`.
- Proposed timeout: `T_timeout = max(5 × median(null-netlist wall time over 3 runs for the same artifact/design), 2 seconds)`. Validate during FIFO feasibility; freeze or amend before confirmatory generation.
- Record `driver_completed` for every run. A driver still waiting at the cap is incomplete but not timed out.
- A null run must complete within its watchdog for a mutant-run timeout to be interpreted.

## 13. Denominators and metrics

### 13.1 Scheduled generation slots and validity

For prompt arm `c` and design `d`, let `G_cd` be all scheduled initial generation calls. Each initial call is one slot even if the response is missing, malformed, invalid, fails compile/execute or exhausts repairs. Repairs are nested within the slot.

`V_cd = valid artifact slots / |G_cd|`.

A slot is valid only if the final artifact after its pre-registered repair budget passes schema/API validation, AST/inspect entry-point and import checks, compile, RTL-versus-null controls, null execution and two consistent independent `PASS` invocations of the checker on the same immutable null trace. Report the full funnel and all attrition, including initial-call validity before any repair and final post-repair validity after the complete repair budget. `V_cd` is the H1 estimation-only outcome and H2(a) comparison outcome.

### 13.2 Complete-trace conditional diagnostics

For valid artifact `i`, define `T_i` as **all valid artifact–mutant pairs with a complete trace and valid pairing**, regardless of the checker verdict. `T_i` includes the normal classes (`DETECTED`, `PND`, `NP`), both anomaly classes, and both checker-error classes. It excludes `INVALID_PAIR`, invalid artifact slots, driver/simulator errors and timeouts because these lack an eligible complete paired trace.

Define the number of masked-exposed pairs in `T_i`:

`X_i = DET_i + PND_i + CHECKER_ERROR_AFTER_MASKED_DIVERGENCE_i`.

Then:

- `E_i = X_i / |T_i|` — **checker-independent own-driver masked exposure rate** among complete-trace valid pairs. The numerator is a property of the paired trace/mask, not checker success. `CHECKER_ERROR_AFTER_MASKED_DIVERGENCE` remains included because exposure is already known from the complete trace.
- `S_i = DET_i / X_i` — **own-checker detection among all known exposed complete-trace pairs**. A checker crash after masked divergence is a non-detection and remains in the denominator. `S_i` is still conditional on the particular driver's exposure set and is not a standardized checker-quality parameter.
- **Optimistic crash sensitivity only:** `S_i^optimistic = (DET_i + CHECKER_ERROR_AFTER_MASKED_DIVERGENCE_i) / X_i`. This treats every checker crash after known exposure as though it had detected the divergence; it is an intentionally optimistic upper-bound sensitivity, not the primary metric and not separately hypothesis-tested.
- `M_i = PND_i / (NP_i + PND_i)` — descriptive miss composition where `NP_i + PND_i > 0`; it is not checker quality or causal attribution.

Undefined-value rules:
- `E_i = NA` when `|T_i| = 0` (all pairs invalid or truncated); report the number of such artifacts per arm/design.
- `S_i = NA` when `X_i = 0`; report the number of such artifacts per arm/design. Do not silently omit this count.
- `M_i = NA` when `NP_i + PND_i = 0`.

**Outcome-class inclusion table.** This is the canonical inclusion map for one valid artifact's mutant pairs:

| Pair outcome class | Complete trace / valid pair? | In `T_i`? | Masked exposure known? | In `X_i`? | In `DET_i`? | In primary `J_exposure`? | In primary `J_detection`? |
|---|---|---:|---|---:|---:|---:|---:|
| `DETECTED` | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| `PND` | Yes | Yes | Yes | Yes | No | Yes | No |
| `NP` | Yes | Yes | No | No | No | No | No |
| `ANOMALY_PIPELINE_OR_NONDETERMINISM` | Yes | Yes | No | No | No | No | No |
| `ANOMALY_CHECKER_STRICTER_THAN_MASK` | Yes | Yes | No (raw-only divergence) | No | No | No | No |
| `CHECKER_ERROR_NO_MASKED_DIVERGENCE` | Yes | Yes | No | No | No | No | No |
| `CHECKER_ERROR_AFTER_MASKED_DIVERGENCE` | Yes | Yes | Yes | Yes | No | Yes | No |
| `INVALID_PAIR` | Not an eligible paired observation | No | Not scored | No | No | No | No |
| `DRIVER_SIM_ERROR_NO_MASKED_DIVERGENCE` | No (truncated) | No | No | No | No | No | No |
| `DRIVER_SIM_ERROR_AFTER_MASKED_DIVERGENCE` | No (truncated) | No | Known before termination | No (primary) | No | No (primary) | No |
| `TIMEOUT_WITHOUT_MASKED_DIVERGENCE` | No (truncated) | No | No | No | No | No | No |
| `TIMEOUT_AFTER_MASKED_DIVERGENCE` | No (truncated) | No | Known before timeout | No (primary) | No | No (primary) | No |
| `INVALID_ARTIFACT_SLOT` | No artifact / no valid pair | No | Not scored | No | No | No | No |

Truncated after-exposure cases are reported in a one-sided, lower-bound exposure sensitivity only. For valid artifact `i`, let `U_i` be all truncated driver/simulator-error or timeout pairs and `U_i^X` those with masked divergence recorded before termination. Report `E_i^trunc = (X_i + |U_i^X|) / (|T_i| + |U_i|)` alongside primary `E_i`; non-exposed truncated pairs are included in the denominator because they might have exposed later. At ITT level, report `J_exposure^trunc` by adding all recorded pre-termination exposures to the primary `J_exposure` numerator, retaining the same scheduled denominator. `INVALID_ARTIFACT_SLOT` is a ledger state for every scheduled mutant combination belonging to a missing/invalid artifact slot; it remains in the ITT denominator and contributes zero primary exposure/detection.

**Aggregation.** The primary arm/design summary for conditional diagnostics is the ratio of sums: `E = ΣX_i / Σ|T_i|`; `S = ΣDET_i / ΣX_i`. Use an artifact-cluster bootstrap for intervals. Also report equal-weight means across defined artifacts as sensitivity analyses, with NA counts beside them. This avoids allowing an artifact with one exposed pair to receive the same primary weight as one with many exposures.

**Miss-composition identity.** The identity `M_i = E_i(1−S_i)/(1−E_iS_i)` does **not** generally hold for the corrected `E_i` and `S_i`, because those include complete-trace checker-error classes. The identity holds only on the normal-outcome subset `C_i = NP_i + PND_i + DET_i`, using `E_i^C = (PND_i+DET_i)/C_i` and `S_i^C = DET_i/(DET_i+PND_i)`. Unit-test the identity on that subset only.

Report `NP` subtypes separately as `NP_NO_RAW_DIVERGENCE` and `NP_RAW_ONLY_UNMASKED`. Do not infer internal activation from either.

### 13.3 Intention-to-treat joint outcomes

For design `d`, let `M_d` be the fixed eligible primary mutant population. The scheduled denominator is `|G_cd| × |M_d|`. Every scheduled slot remains in it. Missing/invalid artifact slots and invalid pairs contribute zero to ITT exposure and detection successes.

- `J_exposure_cd = Σ_valid_slots X_i / (|G_cd| × |M_d|)`.
- `J_detection_cd = Σ_valid_slots DET_i / (|G_cd| × |M_d|)`.

The primary `J_exposure` numerator uses the same exposure rule as `E_i`: only complete-trace valid pairs with masked divergence, including `CHECKER_ERROR_AFTER_MASKED_DIVERGENCE`. `J_detection` includes only normal `DETECTED` outcomes. Driver/simulator error or timeout after a recorded masked divergence is **not** included in the primary exposure numerator; report it as the separate one-sided truncated-exposure sensitivity defined in §13.2. Checker errors after exposure count toward exposure but not primary detection. Also report an optimistic crash sensitivity, `J_detection^optimistic = Σ_valid_slots (DET_i + CHECKER_ERROR_AFTER_MASKED_DIVERGENCE_i) / (|G_cd| × |M_d|)`, which treats every post-exposure checker crash as a detection. This is not a primary outcome and is not a separate H2 test.

Also report the conclusive normal-completion rate and all pair classes separately. For each design/arm, the following should hold to numerical precision:

`J_exposure_cd = V_cd × [Σ_valid_slots X_i / (|valid_slots| × |M_d|)]`.

`J_detection_cd = V_cd × [Σ_valid_slots DET_i / (|valid_slots| × |M_d|)]`.

For the optimistic crash sensitivity, replace `DET_i` by `DET_i + CHECKER_ERROR_AFTER_MASKED_DIVERGENCE_i` in the `J_detection` numerator. This alternative is descriptive only. For truncated exposure sensitivity, add pairs exposed before truncation to the numerator while retaining the scheduled denominator. If no slots are valid, the primary ITT metrics remain zero and conditional RHS expressions are not evaluated.

These identities and the full pair-class ledger must be executable F15 assertions. F15 must also include a zero-valid-slot case: `J_exposure` and `J_detection` remain zero because their scheduled-slot numerators are zero; do not evaluate the right-hand conditional-mean expressions above, which are undefined with no valid slots. Report that no valid artifacts were observed.

### 13.4 Common-trace checker panel (secondary, standardized analysis)

**Corpus legality and construction.** Build the shared corpus through the production harness. It contains (a) multiple seeds of a reactive random driver that respects the specification's legal-input rules, and (b) a directed corner-case suite written against the specification only, before any LLM generation and independently of generated artifacts. Do not use unconstrained random input sequences that violate protocol legality (for example, undefined writes while full). For every stream/seed/scenario, run the original RTL and null netlist to create benign baseline traces, and run the null netlist plus each fixed eligible mutant to construct the mutant panel. Only baseline scenarios that pass the frozen RTL-versus-null masked-equivalence and legal-input controls enter the benign-trace corpus. Retain both original-RTL and null-netlist benign traces for false-alarm checks. Use the same cycle alignment, paired-run rules and mask. The two separate streams are `REACTIVE_RANDOM` and `DIRECTED`. `k_null` counts distinct legal reactive-random seeds only; the directed suite is a separately frozen finite list of spec-derived scenarios. For each scenario, retain separate benign original-RTL and null-netlist traces. Freeze the stream definitions, corpus cases, seeds, cycle cap and benign trace hashes before generating the panel mutant traces. Proposed `k_null=20` reactive-random seeds per design is a planning value; final `k_null` is **TO FREEZE**.

**Per-checker, per-stream null classification.** Run each valid checker twice in separate processes on each byte-identical benign original-RTL and null-netlist reference trace for that stream. A disagreement between the two verdicts is nondeterminism and a `PANEL_ERROR`. Let `B_ds` be the number of frozen benign trace files in that stream, counting the original-RTL and null-netlist trace for each included scenario separately. Record separate flags for crash/schema error, nondeterminism and false alarm. Assign one mutually exclusive summary partition with this precedence:

1. `PANEL_ERROR`: any crash, schema mismatch, unsupported required field or inconsistent verdict on repeated evaluation of the same trace bytes;
2. `PANEL_FALSE_ALARM`: no `PANEL_ERROR`, but the checker returns `FAIL` on one or more valid benign original-RTL/null-netlist reference traces;
3. `PANEL_COMPATIBLE`: no error and `PASS` on every benign original-RTL/null-netlist reference trace.

Keep the underlying event counts as well as the partition, so an error does not hide a simultaneous false alarm. A false alarm is an error of commission, not a compatibility failure. Sensitivity is scored only for `PANEL_COMPATIBLE` checkers, separately per stream.

**Standardized exposure set and panel metrics.** Let `Q_ds` be the frozen set of exposed cases for design `d` and stream `s`; each case is a stream/seed/scenario × mutant combination with checker-independent masked divergence. The set is identical for every generated checker. If `|Q_ds|=0`, both conditional and ITT panel sensitivity are `NA` (their exposure-case denominator is zero); compatibility, error and false-alarm outcomes remain reportable, and the zero-exposure stream is identified.

For checker artifact `i`, sensitivity conditional on compatibility is `Sens_i,ds = # FAIL verdicts on Q_ds / |Q_ds|`, defined only when the checker is `PANEL_COMPATIBLE` for that stream. A checker crash on a mutant trace counts as a non-detection. Also report checker `FAIL` on raw-only unmasked divergences as a separate `PANEL_STRICTER_THAN_MASK_EVENT`; it is not a detection. A checker error or nondeterministic verdict on a mutant trace is a panel error event and is not a detection.

Define the per-arm intention-to-treat panel sensitivity as `PanelSens_ITT_cds = successful detections on Q_ds from valid, PANEL_COMPATIBLE scheduled slots / (|G_cd| × |Q_ds|)`. Missing/invalid artifact slots, `PANEL_ERROR` streams and `PANEL_FALSE_ALARM` streams contribute zero detections. Define `PanelCompat_ITT_cds = scheduled slots with PANEL_COMPATIBLE / |G_cd|`; `PanelError_ITT_cds = scheduled slots with PANEL_ERROR / |G_cd|`; and `PanelFalseAlarmPartition_ITT_cds = scheduled slots with PANEL_FALSE_ALARM / |G_cd|`. These three mutually exclusive partition proportions must sum to `V_cd` for each stream/design/arm, because invalid or missing artifact slots contribute zero to all three ITT proportions. Define the false-alarm event rate as the number of `FAIL` outcomes on the `B_ds` benign original-RTL/null-netlist reference traces divided by `|G_cd| × B_ds`; invalid slots contribute zero false-alarm events. Also report the proportion of scheduled slots with at least one false alarm, independent of the mutually exclusive partition label, so a checker with both an error and false alarm does not hide the false-alarm event. For conditional reporting, show each proportion among valid checker artifacts and report the underlying event counts.

As secondary/exploratory contrasts, compare ORG-A and ORG-B on ITT and compatibility-conditional standardized sensitivity, false-alarm rate and compatibility/error rate. Compatibility-conditioned estimates are selection-conditioned and must never replace ITT rates. Record both the mutually exclusive partition and the underlying event flags/counts.

**Inference and interpretation.** Treat the declared mutant population and stream corpus as fixed, declared populations; panel inference is conditional on them. Resample at checker/artifact level; treat streams as fixed strata. A two-way bootstrap over a mutant sample is not required. The panel measures checkers on its fixed exposure profile, not on the exposure distribution typical of LLM-generated drivers. Do not call it “true checker quality”.

**Mutant-trace repeat rule.** Each checker evaluates each exposed mutant trace twice in separate processes using identical trace bytes. Only two consistent `FAIL` verdicts count as a panel detection; two consistent `PASS` verdicts are a miss. Any crash, malformed top-level return, invalid verdict or disagreement on a mutant trace is a `PANEL_ERROR_EVENT` and is not a detection. This event does not change the stream's mutually exclusive compatibility partition, which is computed only from benign traces; retain it as a separate mutant-event count.

**Streams and corpus validity.** `REACTIVE_RANDOM` and `DIRECTED` are separate streams and are analyzed separately; `k_null` applies only to distinct legal reactive-random seeds. Exclude any corpus null/mutant pair that violates the paired-input or trace-integrity rule from `Q_ds` at corpus freeze and report the excluded count by stream/design. A checker that returns `FAIL` on a mutant trace byte-identical to a benign null trace it passed, or produces inconsistent verdicts on repeated evaluation of identical trace bytes, generates a `PANEL_ERROR_EVENT`, not a detection. Add known-answer controls for a stricter-than-mask checker and a nondeterministic checker.

**Freeze ordering / blinding.** The initial F16 and every predeclared instrument re-pilot must finish first on original RTL and null netlist only. After the final passing initial pilot, freeze and hash the FIFO/UART authoring packet, prompt templates, system/repair prompts, response schema, feedback policy, mask, directed suite and analysis plan; only then generate the confirmatory mutant manifest and confirmatory panel mutant traces. Any subsequent change to an author-visible packet item or estimand-defining item requires a new F16/re-pilot cycle, a new packet freeze and fresh confirmatory artifact generation; old confirmatory artifacts are not reusable. **Post-freeze evaluator-revision exception:** if a mid-run halt requires only evaluator implementation/tooling changes, with every author-visible and estimand-defining item unchanged, §3.4 permits one mutant-blind evaluator-requalification run under the same F16 eligibility procedure using fresh pilot seeds on original RTL and null netlist only. This exceptional requalification occurs after the evaluator revision is hashed and before any artifact/slot is re-evaluated; it does not reopen or alter the authoring packet, directed suite, mask, mutant manifest or estimand, and it makes no confirmatory generation calls. If the evaluator-requalification floor is met, re-evaluate all scheduled slots for the affected design using the same already-generated artifact bytes and seeds. If the floor is not met, abort that design with no final-scored slots; do not relax the floor or regenerate confirmatory artifacts under the same packet. If requalification reveals that an author-visible or estimand-defining item must change, the author-visible revision path in §3.4 applies and fresh confirmatory generation is required after refreeze. For pre-freeze feasibility, F17 uses only the hand-built FIFO control mutants defined in Charter §6.1. F17 on the confirmatory MCY manifest runs only after the final authoring-packet freeze. No LLM-generated checker is run on any mutant trace before the analysis freeze.

### 13.5 Power, minimums and reporting

The F16 mutant-blind pilot can estimate artifact validity only. It cannot estimate exposure or detection because it sees no mutant outcomes. Power/precision simulation must use per-design validity estimates and a grid of plausible exposure and detection rates, plus any separately obtained human/random baseline estimates collected under a frozen procedure. With the equal-weight estimand, the lower-validity/noisier design can dominate variance; do not substitute a pooled validity estimate. Do not use F16 mutant-blind pilot data as inputs for exposure/detection.

At least 10 independent calls per arm/design is a feasibility floor only. Confirmatory `n` is **TO FREEZE** after a pre-study precision/power simulation. Report each design as a fixed stratum (two designs are not a sample of all sequential RTL). Do not replace NA with zero. The old minimum-miss count and minimum-defined-artifact rules are not retained unless re-justified and pre-registered.

## 14. Statistical analysis

- Assign scheduled calls using a balanced within-design ORG-A/ORG-B schedule generated from a frozen seed and committed before the first call; archive the schedule and seed.
- Primary analysis unit for all H2 outcomes is the **scheduled generation slot**. H2(a) uses the slot's valid/invalid indicator. For H2(b)/(c), reduce each slot to the fraction of the fixed primary-mutant population exposed/detected; do not permute mutant-pair rows as if independently randomized.
- The confirmatory family contains **one design-stratified treatment-effect test per endpoint**, not separate tests per design. For each endpoint, compute the ORG-B minus ORG-A difference within each pre-declared design stratum, then combine the design-specific differences with equal design weights (recommended; exact design set and weighting are TO FREEZE before generation). Permute arm labels at the slot level within each design stratum and recompute this single combined statistic. Report design-specific estimates and intervals descriptively; do not attach additional confirmatory p-values to each design.
- Use design-stratified slot-level bootstrap confidence intervals, preserving the same fixed design weights.
- Apply two-sided alpha 0.05 and Holm correction across exactly H2(a), H2(b), H2(c). No separate H1 validity test is performed.
- Report effect sizes and confidence intervals, not only adjusted p-values. Designs are fixed strata; no population-level generalization across all sequential RTL is warranted.
- Conditional `E` and `S` use ratio-of-sums as primary descriptive summaries with artifact-cluster bootstrap; equal-weight means are sensitivity analyses.
- Common-trace panel is secondary/exploratory. The mutant set is a fixed declared population; inference is conditional on it. Resample at checker/artifact level and preserve streams as fixed strata. Pre-register exact interval/test method before confirmatory generation.
- `M_i` is descriptive only. No `delta_checker` threshold, no causal checker attribution.
- Missing/malformed/invalid artifacts remain in ITT denominators. Valid-only metrics are explicitly conditional.

## 15. Pre-registration freeze values

Every item marked **TO FREEZE** must be resolved and timestamped before confirmatory generation. Proposed planning values are not evidence that a parameter has passed feasibility.

| Parameter | Current value/proposal | Status |
|---|---|---|
| Feasibility design | Synchronous FIFO | Fixed for feasibility |
| Confirmatory design set | FIFO + UART only; FSM excluded from v1.3 confirmatory set | Proposed; owner must confirm before F16; adding FSM changes the estimand |
| Design semantics | Independently authored, cycle-exact specs with distinctive corner cases | TO FREEZE; disclose benchmark overlap |
| Driver API/alignment | One deterministic step/cycle; harness-owned clock; outputs sampled before next-input decision | Validate F2/F10 |
| Comparison window | Full trace to fixed cap; safe idle after completion | Validate F11 |
| Timeout | max(5×median of 3 null runs, 2 seconds), or validated alternative | Validate F11; then freeze |
| Null export | Same synthesis/export script and tool versions; no mutation | Validate F14 |
| Mutant model | Yosys/MCY post-synthesis structural signal mutations; exact modes and pinned versions | TO FREEZE |
| Primary mutant set | Fixed, reproducible eligible population per design | TO FREEZE |
| Observation mask | Derived from spec, evaluator-only, every entry maps to spec clause | F18 + mask reviewer sign-off |
| Strict-mask sensitivity | One independent stricter-mask variant | Proposed; exact rule TO FREEZE |
| Prompt arm names | ORG-A / ORG-B | Approved |
| Prompt factor | Whole-block presentation order only; content, headings, system and repair prompts fixed | Approved; F18 required |
| Prompt templates | `19_ORG_A_Prompt_Template.txt`, `20_ORG_B_Prompt_Template.txt` | Structural pair drafted; design payloads TO FREEZE |
| Tokenizer | Pinned selected-model tokenizer ID/version | TO FREEZE |
| Wrapper-token rule | Identical wrappers/headings; no arm-specific wrapper tokens | Approved; F18 verifies |
| Human time box | 120 minutes/design | Proposed; TO FREEZE |
| LLM repair budget | 2 repairs after initial generation | Proposed; TO FREEZE |
| F16 pilot size | fixed `n_pilot` per arm/design | TO FREEZE before pilot |
| F16 validity floor | `V_min` independently applied to each arm × design stratum | TO FREEZE before pilot; no between-arm difference stop |
| Common panel corpus | `REACTIVE_RANDOM` and `DIRECTED` are separate streams; `k_null` applies only to reactive-random seeds | `k_null=20` proposed; directed cases/seeds/hashes TO FREEZE |
| Panel categories | PANEL_ERROR / PANEL_FALSE_ALARM / PANEL_COMPATIBLE | Defined; validate F17 |
| Empty panel exposure set | `|Q_ds|=0` | Panel sensitivity ITT and conditional are NA; compatibility/error/false-alarm remain reportable |
| Panel known-answer controls | reference, always-PASS, always-FAIL, stimulus-literal, crashing, stricter-than-mask and nondeterministic checkers | Validate F17 |
| Power inputs | assumed grid for exposure/detection; F16 supplies validity only | Approved rule; grid TO FREEZE |
| Statistics | One design-stratified slot-level test per H2 endpoint; equal design weights proposed; artifact-slot bootstrap; Holm across 3 H2 outcomes | Freeze exact design set/weights, code, seeds and resamples |
| Model/provider/settings | one pinned model and same settings both arms | TO FREEZE |
| Response schema | JSON Schema v1.0 (schema version independent of pack version); Python 3.11; exact entry points and stdlib-only imports | Proposed contract in files 30 and 34; parser/runtime image to validate and freeze |
| Prompt assembly | file 31; UTF-8 no BOM, LF, exact rendering and canonicalization | Proposed; F18 independent sign-off required |
| Repair context/feedback | same conversation; full history resent byte-identically; stage/error whitelist; 2,048-byte diagnostic cap | Proposed; `k=2`, runtime provider message handling TO FREEZE |
| Re-pilot cap | `R_max=2` proposed; at most 3 pilot runs total (initial + 2 re-pilots) | TO FREEZE before F16 |
| Toolchain | Python, Cocotb, simulator, Yosys, MCY versions | TO FREEZE |
| Immutable freeze | signed Git tag or equivalent | TO FREEZE |

## 16. Security and reproducibility

Run generated driver/checker code in disposable containers or restricted accounts with network disabled, no credentials mounted, minimal filesystem access, process/memory limits and watchdog. Preserve specifications, authoring/evaluator packs, mask traceability table, masks and hashes, prompt templates and assembled prompt hashes, raw outputs, model/tokenizer metadata, repairs, seeds, tool versions, null/mutant hashes, miter assumptions, raw traces, waveforms, checker outputs, every pair classification and analysis scripts. Every table must be reproducible from archived artifacts without new LLM calls.

## 17. Feasibility controls F1–F18 (all must pass)

The feasibility experiment uses the synchronous FIFO. Controls are hand-built engineering tests and do not count as confirmatory study evidence. F17 feasibility uses only hand-built FIFO control mutants. F16 is a mutant-blind LLM pilot and is not authorized until the current LLM-call gate passes independent document and implementation review; it runs before the final confirmatory packet/mutant freeze. F17 on the confirmatory MCY manifest occurs only after that freeze. F18 is a hand-built parser/prompt/assembly test and does not require an LLM call.

| ID | Control | Setup | Expected result |
|---|---|---|---|
| F1 | Determinism and checker null repeat | Run one artifact on null netlist three times; run its checker twice in separate processes on the same immutable null trace | Traces match excluding explicitly non-deterministic metadata; both checker runs return identical `PASS` |
| F2 | Alignment | Driver echoes a registered output into next-cycle input | Row n records outputs after edge n and the driver's decision for edge n+1; consumed inputs agree with prior scheduled vector |
| F3 | RTL versus null | Run F1 artifact on RTL and null netlist | No masked divergence and no scheduled next-input divergence before first raw divergence |
| F4 | Miter/simulation agreement | Replay mask-aware miter counterexample in simulator | Masked divergence appears at predicted cycle |
| F5 | Masked don't-care | Mutant changes FIFO data only while valid is low, where spec says data is don't-care | Raw divergence but no masked divergence; miter agrees through fixed N |
| F6 | Pair classes | Hand-built correct checker, always-PASS checker, and non-exposing driver | `DETECTED`, `PND`, `NP` respectively |
| F7 | Checker stricter than mask | Checker compares data during an explicit don't-care window | `ANOMALY_CHECKER_STRICTER_THAN_MASK` |
| F8 | Pipeline anomaly | Checker returns FAIL on a trace identical to null | `ANOMALY_PIPELINE_OR_NONDETERMINISM` |
| F9 | Invalid pair | Driver reads unseeded entropy; rerun with harness-owned seed | First `INVALID_PAIR`; seeded version obeys paired input schedule |
| F10 | Same-row tie | Mutant changes `full`; driver changes next input based on sampled output | Pair is valid under output-first sampling rule |
| F11 | Cycle cap/timeout | Driver completes at cap vs watchdog fires | Cap is normal incomplete-driver termination; watchdog is timeout |
| F12 | Driver/simulator error | Driver converts X output to integer on mutant | Driver/simulator error, not detection; truncated trace excluded from `T_i` |
| F13 | Checker non-interference | Run checker in separate process on trace file | Checker cannot access simulator handles or alter trace |
| F14 | Export repeatability | Export null netlist twice with same pinned scripts | Stable null hash, top module and ports |
| F15 | Classifier, ledger and metric identities | Feed hand-built cases for every outcome; include invalid artifact slots and a zero-valid-slot arm/design; verify complete-trace categories, `T_i`, `X_i`, H2 denominators and aggregation identities | Exactly one ledger class for every scheduled slot × mutant; total = `|G_cd|×|M_d|`; for each valid artifact, `|T_i|+|U_i|+|INVALID_PAIR_i|=|M_d|`; for each arm/design, valid-slot pair rows plus invalid-slot ledger rows equal `|G_cd|×|M_d|`; `X_i≤|T_i|`, `DET_i≤X_i`, and `|U_i^X|≤|U_i|`; `X_i` includes only DET+PND+checker-error-after-exposure; `E_i`/`S_i` and optimistic crash sensitivities match definitions; `J_exposure` and `J_detection` identities hold, including zero-valid-slot behavior; truncated-exposure sensitivity is one-sided; miss-composition identity tested only on `C_i=NP+PND+DET`; panel partition sums equal `V_cd` separately for each stream. |
| F16 | Two-arm production-path artifact-contract pilot | Predeclare `n_pilot` per arm/design; run both ORG templates through the production parser, schema/API validation, compile, original-RTL-versus-null control, null execution, checker repeat and the complete pre-frozen repair budget (proposed `k=2` repairs after the initial call). Run original RTL and null netlist only; do not run primary mutants or expose mutant results. Retain every scheduled call; repairs nested. Discard all pilot artifacts/data from confirmatory analysis. | Each arm × design stratum separately meets the pre-registered minimum validity floor `V_min`. Report between-arm difference descriptively; do not stop because of an arm difference. Permitted post-pilot changes are limited to symmetric parser, schema, API, envelope, repair-grammar and payload-wording changes. Block order, arm definitions and arm-specific changes are prohibited. Set `R_max` before F16 (proposed `R_max=2`, meaning at most three pilot runs total: the initial pilot plus two re-pilots), each using fresh seeds. If either arm × design stratum remains below `V_min` after `R_max`, declare the confirmatory study infeasible for the pre-declared design set and model; do not drop the failing design or reweight the estimand after observing pilot data, and do not relax the floor. Pilot and confirmatory seeds/slots must be disjoint. Any permitted contract change triggers a complete re-pilot. Pilot contributes validity estimates only, not exposure/detection inputs for power simulation. |
| F17 | Common-trace panel controls and freeze ordering | Pre-freeze feasibility F17 uses only hand-built FIFO control mutants, not the confirmatory MCY manifest. Build separate legal `REACTIVE_RANDOM` and `DIRECTED` streams through the production harness; run RTL and null benign traces; repeat each checker twice on identical benign and mutant trace bytes; exclude paired-input/integrity-invalid corpus pairs from `Q_ds`. Confirmatory F17 is run only after F16/re-pilots and the complete authoring packet, directed suite, mask and analysis plan are frozen and hashed, before any confirmatory panel mutant trace is scored by an LLM checker. | Correct reference checker: compatible and detects every exposed case; always-PASS: compatible with zero sensitivity; always-FAIL: `PANEL_FALSE_ALARM`; stimulus-literal: false alarm on at least one distinct legal benign trace; crashing checker: `PANEL_ERROR`; stricter-than-mask checker: `PANEL_STRICTER_THAN_MASK_EVENT`, not detection; nondeterministic checker: `PANEL_ERROR`. Mutant-trace errors/disagreements count as `PANEL_ERROR_EVENT`, not detection, but do not change the benign-trace compatibility partition. Report event counts separately; `PANEL_ERROR`, `PANEL_FALSE_ALARM` and `PANEL_COMPATIBLE` partition proportions sum to `V_cd` within each stream/design/arm. |
| F18 | Prompt, parser, repair, assembly and mask traceability | Use frozen parser/schema and repair fixture catalog; validate AST/inspect entry points, allowed imports, vector validation, clause IDs, failure-stage map, exact repair feedback grammar and all template/system/repair assembly hashes. Verify no model-visible arm/ordinal cues, exact block equality/permutation, mask-to-spec traceability and independent signatures. | Every parser/repair fixture in file 36 returns its declared single outcome; model-visible B5/B7/B8 contract text agrees with file 30; system/repair bytes reproduce from file 25 extraction rules; schema hash/length and payload hashes are recorded; reserved-heading payloads hard-fail; independent reviewer signs. Any failed fixture, contract mismatch or untraceable mask row blocks freeze. |

F15 ledger assertions must include: (1) per valid artifact, `|T_i| + |U_i| + |INVALID_PAIR_i| = |M_d|`; (2) per arm/design, valid pair rows plus `INVALID_ARTIFACT_SLOT` rows equal `|G_cd|×|M_d|`; (3) `X_i≤|T_i|`, `DET_i≤X_i` and `|U_i^X|≤|U_i|`; (4) on the normal subset `C_i`, `NP_i+PND_i+DET_i=C_i≤|T_i|` and the miss-composition identity holds only using `C_i`-restricted quantities; and (5) for each stream/design/arm, the three panel partition proportions sum to `V_cd`.

F2, F4, F5, F9, F15, F16, F17 and F18 are critical gates. A failure requires an arm-symmetric instrument correction and rerun of affected controls. Feasibility/pilot artifacts are never included in confirmatory analysis.

## 18. Canonical freeze checklist

This is the single canonical checklist. Before confirmatory LLM generation:

- [ ] Complete targeted and best-available literature search; document inaccessible databases and source versions/access limitations.
- [ ] Freeze original cycle-exact FIFO and UART specifications, port manifests, reset/legal-input rules and distinctive semantics.
- [ ] Complete and sign mask-to-specification traceability table; every don't-care window is specified in author packet.
- [ ] Freeze observation mask and stricter-mask sensitivity variant; evaluator-only.
- [ ] Freeze authoring/evaluator information boundary; no reference model/API or expected-output tables in authoring packet.
- [ ] Freeze driver API, scheduler, alignment, same-row tie, cap, safe-idle and watchdog.
- [ ] Freeze checker contract, trace schema and double-run null determinism requirement.
- [ ] Freeze Yosys/MCY versions, mutation modes, export scripts, mutant population and bounded-equivalence assumptions.
- [ ] Freeze ORG-A/ORG-B template pair, machine-readable response schema/parser, assembly spec, system and repair prompts, tokenizer and all assembled-message hashes; independent F18 sign-off.
- [ ] Freeze model/provider/settings, same-conversation repair policy and bounded feedback grammar, repair budget, balanced within-design randomization schedule/seed and sample size.
- [ ] Complete F1–F18 on FIFO; F16 validity pilot passes both per-arm floors; F17 panel controls pass.
- [ ] Freeze statistical code, two-sided alpha, slot-level randomization/permutation, cluster bootstrap, Holm family and secondary panel inference.
- [ ] Complete pre-study precision/power simulation using assumed exposure/detection grids and independent baseline estimates; do not use F16 for exposure/detection.
- [ ] Freeze pair classifier and verify F15 identities.
- [ ] Repeat a pre-registered 10% subset of confirmatory executions; traces match after excluding explicitly nondeterministic metadata.
- [ ] Resolve all Charter–Protocol and source-log discrepancies.
- [ ] Seal the registration with signed Git tag or equivalent immutable record.

**Release gates and required execution order.** (1) Complete the v1.3.7-candidate document pack, carry forward unchanged model-visible prompt hashes/sidecar, and index the 144-fixture set. (2) Obtain an independent document-only v1.3.7-candidate audit of the actual pack, including the operative F18 checklist, every fixture expectation and all cross-document rules; a pass authorizes nothing by itself. (3) Only after that document re-audit passes, the owner must explicitly record acceptance or rejection of A1–A11 and choose the X14 strict-AST branch. Until both the document audit and owner record are complete, no implementation or fixture execution is authorized. (4) After those prerequisites, only the limited hand-built FIFO feasibility scope may open: FIFO specification and mask-traceability rows first, then the hand-built harness/ledger, F1–F15, parser/assembler implementation and fixture-suite execution against hand-written fixtures on the pinned CPython 3.11 runtime, and F17 using only hand-built FIFO control mutants. The standalone U+2118 tokenizer probe may be completed earlier on the exact pinned Python 3.11 interpreter; otherwise it must be recorded during this implementation-validation stage. (5) Independently re-audit the implementation, parser/assembler, Python 3.11 behavior and all mandatory fixture results. (6) Only after that independent implementation re-audit may the owner consider and explicitly authorize the separate LLM-call gate; F16, smoke tests and provider-format probes remain prohibited until that gate is affirmatively opened. Confirmatory generation remains prohibited until F16/F17/F18, the full canonical §18 freeze checklist and the signed immutable preregistration are complete. Any change to audited model-visible text or normative behavior requires the affected document/hash/fixture checks and independent re-audit to be repeated.

## 19. Review provenance and status

v1.3.7-candidate is OpenVEF Planning v1.3.6 with the corrections in `CHANGELOG-v1.3.7-candidate.md`; it is not audited, frozen or approved, and v1.3.6 remains the default pack. v1.3.6 is a corrective evidence/metadata release following the owner-reported v1.3.5 document-audit PASS. It updates the File 21 diagnostic-assignment cross-reference to include M70, corrects the approval-record title, Charter status history, sidecar prompt-hash history and file 50 heading, and includes the exact v1.3.2 independent audit export. The v1.3.2 export is included as file 62 and under `archive_v1.3.2/release_documents/`; its exact size (36,940 bytes) and SHA-256 (`3f23cabb8f38cfbed41b33276bdca8b28d8a59de9a74961a74a9080a92fc6f52`) are verified in file 60. The full v1.3.5 audit export was not attached; file 63 is only an owner-supplied outcome summary. No model-visible prompt, schema or common-message bytes changed, so the 13,377-byte template-stage hashes carry forward unchanged. Status of all 144 fixture descriptors: Development-run evidence: runs of a project implementation are development runs, not F18 acceptance; Formal F18 status: NOT RUN / NOT PASSED; Approval: nothing is approved. The seven v0.7 design directions remain owner-approved. The v0.8 A1–A11 decisions remain proposals and owner acceptance has not been recorded; X14 (strict-AST branch) is also pending explicit owner choice. No LLM call, parser/assembler run against a generated response, feasibility engineering or confirmatory experiment is authorized by this draft. The only work that may open after explicit A1–A11 owner acceptance and the X14 branch choice is the hand-built FIFO scope in §17/§18. The LLM gate remains closed until the gates in this section are met; confirmatory generation remains prohibited until every §18 freeze item is sealed.

## 20. Control-vector input contracts and result schemas (v1.3.7 candidate, OWNER-DECIDED OD-3)

**OWNER-DECIDED OD-3** (owner decision D-027). v1.3.6 names the properties of its control vectors only in fixture descriptors and does not state their schema. The owners adopt the tables below as normative. Each row names one property, its type, its allowed values and the Protocol text that fixes its value. Basis `pack` means that the cited text fixes the value. `C1`, `C3`, `C9`, `C12`, `C13` and `C14` name candidate corrections, `OD-1` is the owner rule of L174, `OS-1` is the owner specification of owner decision D-026, and `A-033` is the reading approved under owner decision D-009. Basis `OD-3` means owner vocabulary or schema adopted by D-027: its spelling is not v1.3.6 text, and its meaning is the text cited with it. A control-vector result has exactly the properties its table lists and is compared whole (File 36 L176). An input with a value outside its allowed values, or with any other property, is an input error, not an outcome.

**Properties no rule fixes:** none. Every property of every control vector below has a rule. Two rows rest on a reading rather than on one sentence: the stage `DESIGN_HALT` of the change-class and domain-validation results (A-033), and the order of the three domain arrays, which is the order L185 lists them in (OD-3).

### 20.1 Inputs of the change-class and domain-validation vectors

| Vector | Property | Type | Allowed values | Rule | Basis |
| --- | --- | --- | --- | --- | --- |
| Change-class vector | `change_class` | string | exactly one of `FROZEN_EVALUATOR_SOURCE_BINARY_OR_CONFIG_CHANGED`, `SHARED_AUTHOR_VISIBLE_OR_ESTIMAND_DEFINING_ITEM_CHANGED`, `DESIGN_MEMBERSHIP_OR_ESTIMAND_OR_WEIGHT_CHANGED_AFTER_CONFIRMATORY_START`, `DESIGN_SPECIFIC_AUTHOR_VISIBLE_ITEM_CHANGED` | L176: the four change classes. The input is the class alone, so the result states the rule for that class and names no design, component or slot. | OD-3 |
| Domain-validation vector | `domain_validation` | string | exactly `HALT_SIGNATURE_COMPONENT_ENUMERATION` | L185: the halt-signature domains. The result states the closed component domains and the two component rules. | OD-3 |

### 20.2 Properties of every change-class and domain-validation result

| Property | Type | Value | Rule | Basis |
| --- | --- | --- | --- | --- |
| `disposition` | string | `CONTROL_EXPECTATION` | L176 "Each literal is a closed local control expectation"; L177 | pack |
| `stage_id` | string | `DESIGN_HALT` | L172 stage list; §7b, which L251 makes normative in §3.4 "Mid-run design halt" (L181–L185) | A-033 |
| `error_class` | string | the CODE of `diagnostic` | L175 error-class rule for `EVALUATOR_REVISION_REQUIRED`, `AUTHORING_REVISION_REQUIRED` and `HALT_SIGNATURE_SCHEMA` | C1 |
| `diagnostic` | string | the value given for the input in §20.3 | L175 | pack |
| `required_action` | string | the L176 literal of the change class, or of `HALT_SIGNATURE_COMPONENT_ENUMERATION` | L176 | pack |

### 20.3 Further properties of each result

| Input value | Property | Type | Value | Rule | Basis |
| --- | --- | --- | --- | --- | --- |
| `FROZEN_EVALUATOR_SOURCE_BINARY_OR_CONFIG_CHANGED` | `diagnostic` | string | `EVALUATOR_REVISION_REQUIRED|reason=FROZEN_EVALUATOR_CHANGED` | L175 "means a frozen evaluator source/binary/tool-version/command/option/configuration changed" | pack |
| `FROZEN_EVALUATOR_SOURCE_BINARY_OR_CONFIG_CHANGED` | `new_evaluator_version_hashes_required` | Boolean | `true` | L183 "assign a new evaluator version and hashes" | pack |
| `FROZEN_EVALUATOR_SOURCE_BINARY_OR_CONFIG_CHANGED` | `f16_required` | Boolean | `true` | L183 "run the frozen F16 eligibility procedure with fresh mutant-blind pilot seeds" | pack |
| `FROZEN_EVALUATOR_SOURCE_BINARY_OR_CONFIG_CHANGED` | `reuse_same_artifact_bytes` | Boolean | `true` | L183 "using the same already-generated artifact bytes" | pack |
| `FROZEN_EVALUATOR_SOURCE_BINARY_OR_CONFIG_CHANGED` | `new_confirmatory_generation_calls` | integer | `0` | L183 "and no new confirmatory generation calls" | pack |
| `FROZEN_EVALUATOR_SOURCE_BINARY_OR_CONFIG_CHANGED` | `rerun_scope_rule` | string | `shared_evaluator_component_all_designs_and_all_arm_x_design_slots; design_specific_component_affected_design_in_both_arms` | L183 "If the revised evaluator component is shared across FIFO and UART, the affected scope is both designs and every arm × design slot; if it is design-specific, the affected scope is that design in both arms" | OD-3 |
| `SHARED_AUTHOR_VISIBLE_OR_ESTIMAND_DEFINING_ITEM_CHANGED` | `diagnostic` | string | `AUTHORING_REVISION_REQUIRED|reason=AUTHOR_VISIBLE_OR_ESTIMAND_CHANGED` | L175 "means an author-visible or estimand-defining item changed and prior confirmatory artifacts are not reusable" | pack |
| `SHARED_AUTHOR_VISIBLE_OR_ESTIMAND_DEFINING_ITEM_CHANGED` | `reuse_old_confirmatory_artifacts` | Boolean | `false` | L181 "No invalidated confirmatory artifact may be reused" | pack |
| `SHARED_AUTHOR_VISIBLE_OR_ESTIMAND_DEFINING_ITEM_CHANGED` | `new_confirmatory_generation_required` | Boolean | `true` | L181 "fresh confirmatory generation for every affected slot" | pack |
| `SHARED_AUTHOR_VISIBLE_OR_ESTIMAND_DEFINING_ITEM_CHANGED` | `affected_slots` | string | `all_designs_x_all_arms` | L181 "invalidate every scheduled slot across both designs and both arms" | OD-3 |
| `SHARED_AUTHOR_VISIBLE_OR_ESTIMAND_DEFINING_ITEM_CHANGED` | `archive_and_disclose_partial_ledgers` | Boolean | `true` | L181 "Preserve and archive every partial confirmatory ledger" and "disclose the archived partial ledgers" | pack |
| `SHARED_AUTHOR_VISIBLE_OR_ESTIMAND_DEFINING_ITEM_CHANGED` | `new_preregistration_required` | Boolean | `true` | L181 "A shared-item revision requires a new study preregistration" | pack |
| `DESIGN_MEMBERSHIP_OR_ESTIMAND_OR_WEIGHT_CHANGED_AFTER_CONFIRMATORY_START` | `diagnostic` | string | `AUTHORING_REVISION_REQUIRED|reason=AUTHOR_VISIBLE_OR_ESTIMAND_CHANGED` | L175 "means an author-visible or estimand-defining item changed and prior confirmatory artifacts are not reusable"; L175 study-reset sentence | pack, C1 |
| `DESIGN_MEMBERSHIP_OR_ESTIMAND_OR_WEIGHT_CHANGED_AFTER_CONFIRMATORY_START` | `old_confirmatory_artifacts_reusable` | Boolean | `false` | L181 "A study reset is not an operational recovery and cannot retain old confirmatory artifacts" | pack |
| `DESIGN_MEMBERSHIP_OR_ESTIMAND_OR_WEIGHT_CHANGED_AFTER_CONFIRMATORY_START` | `new_preregistration_required` | Boolean | `true` | L181 "always requires a new preregistered study" | pack |
| `DESIGN_MEMBERSHIP_OR_ESTIMAND_OR_WEIGHT_CHANGED_AFTER_CONFIRMATORY_START` | `all_partial_ledgers_archived_and_disclosed` | Boolean | `true` | L181 "archive and disclose all partial confirmatory ledgers" | pack |
| `DESIGN_MEMBERSHIP_OR_ESTIMAND_OR_WEIGHT_CHANGED_AFTER_CONFIRMATORY_START` | `fresh_confirmatory_generation_required` | Boolean | `true` | L181 "generate fresh confirmatory slots under the newly preregistered design set and weights" | pack |
| `DESIGN_SPECIFIC_AUTHOR_VISIBLE_ITEM_CHANGED` | `diagnostic` | string | `AUTHORING_REVISION_REQUIRED|reason=AUTHOR_VISIBLE_OR_ESTIMAND_CHANGED` | L175 "means an author-visible or estimand-defining item changed and prior confirmatory artifacts are not reusable" | pack |
| `DESIGN_SPECIFIC_AUTHOR_VISIBLE_ITEM_CHANGED` | `affected_scope` | string | `affected_design_in_both_arms` | L181 "If a design-specific author-visible item changes, halt and invalidate every slot for that design in both arms" | OD-3 |
| `DESIGN_SPECIFIC_AUTHOR_VISIBLE_ITEM_CHANGED` | `unaffected_design_scope` | string | `not_invalidated_when_membership_estimand_and_weights_are_unchanged` | L181 "every slot for that design in both arms" (the other design is outside that scope) and "A change in design membership, estimand or any confirmatory weight after confirmatory generation starts always requires a new preregistered study" | OD-3 |
| `DESIGN_SPECIFIC_AUTHOR_VISIBLE_ITEM_CHANGED` | `reuse_old_artifacts_for_affected_design` | Boolean | `false` | L181 "No invalidated confirmatory artifact may be reused" | pack |
| `DESIGN_SPECIFIC_AUTHOR_VISIBLE_ITEM_CHANGED` | `new_study_preregistration_required_if_design_membership_estimand_or_weights_change` | Boolean | `true` | L181 "always requires a new preregistered study, even if the changed item is otherwise described as design-specific" | pack |
| `HALT_SIGNATURE_COMPONENT_ENUMERATION` | `diagnostic` | string | `HALT_SIGNATURE_SCHEMA|reason=COMPONENT_VALUES_ENUMERATED` | L175 "control-expectation diagnostic for validating the closed halt-signature component domains and mapping" | pack |
| `HALT_SIGNATURE_COMPONENT_ENUMERATION` | `design_id_values` | array of strings | [`FIFO`, `UART`] | L185 "`design_id` is `FIFO` or `UART`", in that order | pack; order OD-3 |
| `HALT_SIGNATURE_COMPONENT_ENUMERATION` | `halt_code_values` | array of strings | [`SIMULATOR_ERROR`, `TRACE_INTEGRITY_FAILURE`, `RTL_NULL_CONTROL_FAILURE`] | L185 "`halt_code` is `SIMULATOR_ERROR`, `TRACE_INTEGRITY_FAILURE` or `RTL_NULL_CONTROL_FAILURE`", in that order | pack; order OD-3 |
| `HALT_SIGNATURE_COMPONENT_ENUMERATION` | `evaluator_component_values` | array of strings | [`SIMULATOR`, `REPLAY_VERIFIER`, `RECORDER`, `TRACE_ALIGNMENT_CHECKER`, `TRACE_SERIALIZER`, `RTL_NULL_COMPARATOR`] | L185 "`evaluator_component` is `SIMULATOR`, `REPLAY_VERIFIER`, `RECORDER`, `TRACE_ALIGNMENT_CHECKER`, `TRACE_SERIALIZER` or `RTL_NULL_COMPARATOR`", in that order | pack; order OD-3 |
| `HALT_SIGNATURE_COMPONENT_ENUMERATION` | `stable_error_class_rule` | string | `simple_exception_class_for_SIMULATOR_ERROR_else_NONE` | L185: the label of the `stable_error_class` rule stated there | C3 |
| `HALT_SIGNATURE_COMPONENT_ENUMERATION` | `stable_diagnostic_code_rule` | string | `exact_halt_code_token` | L185: the label of the `stable_diagnostic_code` rule stated there | C3 |

### 20.4 The other control vectors (schemas stated elsewhere, listed for completeness)

| Vector | Result properties besides `disposition`, `stage_id` and `error_class` | Where fixed | Basis |
| --- | --- | --- | --- |
| Serializer-grammar vector (File 36 L195) | `diagnostic` = `FEEDBACK_SERIALIZER_REJECT|reason=NON_NORMATIVE_DIAGNOSTIC` | L168, L174 | C12, OD-1 |
| Truncation-primitive vector (File 36 L196) | `contains_marker` (Boolean), `valid_utf8` (Boolean), `output_diagnostic_bytes` (integer), `marker_utf8_bytes` (integer); no `diagnostic` | L168, L174 | C13 |
| JSON-escaping-primitive vector (File 36 L197) | `diagnostic_utf8` (string), `diagnostic_sha256` (string of 64 lowercase hexadecimal digits), `diagnostic_bytes` (integer); no `diagnostic` | L168, L174 | C14 |
| Parser unit vector (File 36 L27) | `diagnostic` by the L127 column rule | File 36 L27 | C9 |
| Operational-recovery vector (File 36 L205) | `diagnostic` = `RERUN_ALL_SCHEDULED_SLOTS_WITH_SAME_FROZEN_ARTIFACTS`, `discard_pre_halt_scores` (Boolean `true`), `rerun_slots` (integer, equal to the input `scheduled_slots`), `reuse_same_artifact_bytes` (Boolean `true`), `new_confirmatory_generation_calls` (integer `0`); or the `FROZEN_EVALUATOR_SOURCE_BINARY_OR_CONFIG_CHANGED` result of §20.2–§20.3 | L175, L183, L185 | OS-1 |

The lifecycle halt-event vector (File 36 L198) and the design-preflight vector (File 36 L199) give stage-map records with the four comparison keys. They are not control-vector results.

---

**v1.3.7 CANDIDATE, not audited.** This file is OpenVEF Planning v1.3.6 with only the corrections listed for it in `CHANGELOG-v1.3.7-candidate.md` (owner decision D-024). It is not part of any released, audited or approved pack; v1.3.6 remains the default.
