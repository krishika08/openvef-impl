"""F17 always-FAIL checker (Protocol L526). AI-written (DEV-005, D-039, D-040); not human-written, not independent.

Returns FAIL on every trace without reading it, so it raises a false alarm on every benign trace.
"""


def check_trace(trace, metadata):
    return {"verdict": "FAIL", "diagnostics": [{"code": "ALWAYS_FAIL", "message": "this checker fails every trace",
                                                "cycle": None, "clause_id": None}]}
