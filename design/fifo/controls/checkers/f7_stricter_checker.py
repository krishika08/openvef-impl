"""Stricter-than-mask checker (F7, Protocol L516; F17, L526). AI-written (DEV-005, D-039, D-040); not human-written,
not independent.

The same model and checks as checkers/f6_correct_checker.py, plus one check the specification does not allow:
it also judges rd_data in rows where rd_valid = 0, which FIFO-022 makes don't-care. It expects rd_data there to
be 00000000 after a reset edge and otherwise to hold the last word read, an assumption that is not in the
specification. On the null trace that assumption holds, so it PASSes; on a design that changes rd_data only in
the don't-care window it FAILs, which is stricter than the mask.
"""

DEPTH = 4
AF_THRESHOLD = 3
MAX_DIAGNOSTICS = 20
ROW_KEYS = ("cycle_index", "inputs_consumed_at_edge_n", "outputs_after_edge_n")
STATUS_CLAUSES = (("rd_valid", "FIFO-021"), ("full", "FIFO-028"), ("empty", "FIFO-028"),
                  ("almost_full", "FIFO-029"))


def diagnostic(code, message, cycle, clause_id):
    return {"code": code, "message": message, "cycle": cycle, "clause_id": clause_id}


def bit(flag):
    return "1" if flag else "0"


def check_trace(trace, metadata):
    diagnostics = []
    if not isinstance(trace, list) or not trace:
        diagnostics.append(diagnostic("TRACE_FORM", "trace is not a non-empty list of rows", None, None))
        return {"verdict": "FAIL", "diagnostics": diagnostics}
    stored = None  # None before the first reset edge (FIFO-013)
    held = None  # the rd_data this checker assumes while rd_valid = 0 (not in the specification)
    for row in trace:
        if not isinstance(row, dict) or any(key not in row for key in ROW_KEYS):
            diagnostics.append(diagnostic("TRACE_FORM", "row without the trace-schema keys", None, None))
            return {"verdict": "FAIL", "diagnostics": diagnostics}
        cycle = row["cycle_index"]
        inputs = row["inputs_consumed_at_edge_n"]
        outputs = row["outputs_after_edge_n"]
        if not isinstance(inputs, dict) or not isinstance(outputs, dict):
            diagnostics.append(diagnostic("TRACE_FORM", "inputs or outputs are not objects", cycle, None))
            return {"verdict": "FAIL", "diagnostics": diagnostics}
        rst = inputs.get("rst", "1" if row.get("reset") else "0")
        if rst == "1":
            stored = []
            held = "00000000"
            expected = {"rd_valid": "0", "full": "0", "empty": "1", "almost_full": "0"}
            word = None
            clause_override = "FIFO-010"
        elif stored is None:
            continue
        else:
            wr_en = inputs.get("wr_en")
            rd_en = inputs.get("rd_en")
            wr_data = inputs.get("wr_data")
            if rst != "0" or wr_en not in ("0", "1") or rd_en not in ("0", "1"):
                diagnostics.append(diagnostic("INPUT_FORM", "consumed inputs are not 0/1 values", cycle, "FIFO-005"))
                return {"verdict": "FAIL", "diagnostics": diagnostics}
            count = len(stored)
            if wr_en == "1" and rd_en == "0" and count == DEPTH:
                diagnostics.append(diagnostic("UNSPECIFIED_AFTER_ILLEGAL_INPUT",
                                              "write while full without a read; later rows are not judged",
                                              cycle, "FIFO-031"))
                break
            read = rd_en == "1" and count > 0
            write = wr_en == "1" and (count < DEPTH or read)
            word = stored.pop(0) if read else None
            if write:
                stored.append(wr_data)
            count = len(stored)
            expected = {"rd_valid": bit(read), "full": bit(count == DEPTH), "empty": bit(count == 0),
                        "almost_full": bit(count >= AF_THRESHOLD)}
            clause_override = None
        for name, clause in STATUS_CLAUSES:
            got = outputs.get(name)
            if got != expected[name]:
                diagnostics.append(diagnostic("OUTPUT_MISMATCH",
                                              f"{name} is {got!r}, the specification gives {expected[name]!r}",
                                              cycle, clause_override or clause))
        if word is None and held is not None and outputs.get("rd_data") != held:
            diagnostics.append(diagnostic("RD_DATA_IN_DONT_CARE_WINDOW",
                                          f"rd_data is {outputs.get('rd_data')!r} while rd_valid = 0; this checker "
                                          f"assumes {held!r}", cycle, "FIFO-022"))
        if word is not None:
            held = word
        if word is not None and outputs.get("rd_data") != word:
            diagnostics.append(diagnostic("OUTPUT_MISMATCH",
                                          f"rd_data is {outputs.get('rd_data')!r}, the word read is {word!r}",
                                          cycle, "FIFO-021"))
        if len(diagnostics) >= MAX_DIAGNOSTICS:
            break
    failed = False
    for item in diagnostics:
        if item["code"] != "UNSPECIFIED_AFTER_ILLEGAL_INPUT":
            failed = True
    return {"verdict": "FAIL" if failed else "PASS", "diagnostics": diagnostics}
