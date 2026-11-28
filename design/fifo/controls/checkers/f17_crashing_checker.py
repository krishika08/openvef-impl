"""F17 crashing checker (Protocol L526). AI-written (DEV-005, D-039, D-040); not human-written, not independent.

Raises on every call, which is a checker error (Protocol L286: "process crash is a checker error").
"""


def check_trace(trace, metadata):
    raise RuntimeError("f17 crashing checker: raises on every call")
