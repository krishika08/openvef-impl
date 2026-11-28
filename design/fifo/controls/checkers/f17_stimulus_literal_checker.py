"""F17 stimulus-literal checker (Protocol L526). AI-written (DEV-005, D-039, D-040); not human-written, not
independent.

Keyed to one literal stimulus sequence: the driver vectors of the directed scenario fill_and_drain. It PASSes a
trace exactly when the first driver vectors consumed after reset (the rows whose consumed rst is 0) equal that
sequence, and FAILs every other trace. It never looks at the outputs. So it false-alarms on any legal benign
trace with other stimulus.
"""

LITERAL = (
    ("1", "10100001", "0"),
    ("1", "10100010", "0"),
    ("1", "10100011", "0"),
    ("1", "10100100", "0"),
    ("1", "10100101", "1"),
    ("0", "00000000", "1"),
    ("0", "00000000", "1"),
    ("0", "00000000", "1"),
    ("0", "00000000", "1"),
    ("0", "00000000", "1"),
)


def check_trace(trace, metadata):
    seen = []
    for row in trace:
        inputs = row["inputs_consumed_at_edge_n"]
        if inputs.get("rst") == "0" and len(seen) < len(LITERAL):
            seen.append((inputs.get("wr_en"), inputs.get("wr_data"), inputs.get("rd_en")))
    if tuple(seen) == LITERAL:
        return {"verdict": "PASS", "diagnostics": []}
    return {"verdict": "FAIL", "diagnostics": [{"code": "STIMULUS_NOT_LITERAL",
                                                "message": "the driver vectors are not the fill_and_drain sequence",
                                                "cycle": None, "clause_id": None}]}
