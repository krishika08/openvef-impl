"""F17 nondeterministic checker (Protocol L526). AI-written (DEV-005, D-039, D-040); not human-written, not independent.

Returns FAIL with probability 1/2 on each call, drawn from the module-global random generator through an alias
(the bypass File 30 L20 describes), which the harness does not seed. It reads nothing in the trace. Two calls on the same bytes disagree with
probability 1/2, so it escapes detection with a probability that halves with each benign trace (CONTROLS-WORKSHEET F17); nothing forces it.
"""

import random

FAIL_PROBABILITY = 0.5


def check_trace(trace, metadata):
    generator = random
    if generator.random() < FAIL_PROBABILITY:
        return {"verdict": "FAIL", "diagnostics": [{"code": "COIN", "message": "nondeterministic FAIL",
                                                    "cycle": None, "clause_id": None}]}
    return {"verdict": "PASS", "diagnostics": []}
