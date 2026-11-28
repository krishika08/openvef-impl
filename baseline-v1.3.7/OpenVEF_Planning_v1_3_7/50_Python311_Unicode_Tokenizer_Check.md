# Python 3.11 Unicode Identifier Tokenizer Check

**Status:** NOT RUN — a CPython 3.11 interpreter is not installed in the current environment.

The v1.3 scanner no longer assumes that every valid Python identifier arrives as `tokenize.NAME`. It checks `NAME` tokens and identifier-relevant non-ASCII code points that appear in `ERRORTOKEN` tokens. An exploratory probe on the available CPython 3.13.5 runtime parsed both `℘ = 1` and `a℘ = 1` and emitted each as a `NAME` token; this is recorded only as 3.13 behavior and does not resolve the 3.11 question. `M55` exercises U+2118 (`℘`) at the start of an identifier; `M56` exercises U+2118 after an ASCII prefix; `M57` confirms that Unicode in strings, a docstring and a comment is allowed.

Run the following on the exact pinned CPython 3.11 interpreter before implementation validation:

```python
import ast
import io
import token
import tokenize

for source in ("℘ = 1\n", "a℘ = 1\n"):
    print("source:", repr(source))
    ast.parse(source)
    for tok in tokenize.generate_tokens(io.StringIO(source).readline):
        print(token.tok_name[tok.type], repr(tok.string), tok.start)
```

Record the exact Python patch version and token output. Then run the corrected identifier-scanner unit logic against both sources, confirming that both are rejected as `NON_ASCII_IDENTIFIER` at the start of the complete identifier lexeme. Also confirm Unicode within STRING and COMMENT tokens is not rejected. A Python 3.13 result is not a substitute for this Python 3.11 check.


## v1.3 external audit update

The owner-provided v1.3 audit summary reports that the non-ASCII fixture columns for M35, M43–M46 and M55–M57 were recomputed on CPython 3.11.18 and matched. The exact runtime to be pinned for implementation remains TO FREEZE, so this is not a pinned-runtime PASS and does not replace the required implementation fixture run.


## v1.3.6 release-lineage note: async-comprehension coverage remains unchanged

M70 adds an `ast.Await`-containing generator expression. It is an AST fixture requirement but does not change the exact pinned-runtime requirement: the project parser/fixture suite must still be run on the frozen CPython 3.11 patch. This note is not evidence of a pinned-runtime run.
