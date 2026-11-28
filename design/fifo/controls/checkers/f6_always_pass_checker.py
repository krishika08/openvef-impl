"""F6 always-PASS checker (Protocol L515). AI-written (DEV-005, D-039, D-040); not human-written, not independent.

Returns PASS on every trace without reading it, so it can never detect a mutant.
"""


def check_trace(trace, metadata):
    return {"verdict": "PASS", "diagnostics": []}
