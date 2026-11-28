# OpenVEF v1.3.2 Audit — Owner-Supplied Summary

**Date:** 23 November 2026 (conversation date).  
**Source:** Findings and scope summary supplied by the project owner in the conversation; the linked Claude artifact was not independently retrievable in this environment. This is a summary, not a byte-for-byte export of that artifact.

## Verdict

The v1.3.2 document audit returned **FAIL**, with one narrow blocker, N12. All v1.3.1 findings N8–N11 were reported fixed and verified against pack bytes. All 138 fixture descriptors were reported consistent and deterministic, with every expected value tracing to a Protocol, file 25 or file 30 definition. Hashes, the Protocol §3.4 copy in file 25, the archives and the 239-entry checksum manifest were reported verified.

## N12 — async generator expression not rejected

The pack forbids async comprehensions and assumes async generators are caught as async function definitions. An expression such as `(x async for x in y)` inside an ordinary synchronous function is represented as a generator-expression AST node, not an `AsyncFunctionDef`. On CPython 3.11.18 it parses and compiles, so it can bypass the existing async-function rule and cause parser implementations to disagree.

The corrective rule must explicitly inspect async-comprehension clauses and assign a deterministic AST-stage result after the existing required-symbol and structural precedence. The user-supplied summary states that the exact two proposed fixture sources are in a JSON block in the linked artifact; that artifact URL was not retrievable here. The v1.3.3 fixtures M65/M66 are therefore authored as explicit equivalent cases from the existing M59 fixture shape: a driver helper and the required checker function each contain a valid async generator expression.

## Non-blocking cleanup

- Normalize Markdown-export padding in M61, M63 and M64. This only removes excess indentation/trailing spaces; expected outcomes remain unchanged.
- Add cases for async `check_trace`, an extra async `Driver` method, and a decorated async definition, covering precedence already specified by the contract.

## Authorization

The LLM-call gate remains NOT MET. A1–A11 are NOT ACCEPTED; X14 requires owner choice; identities remain to confirm; authorization is NONE. No implementation or fixture execution is claimed, and the pinned Python 3.11 patch remains to be frozen.
