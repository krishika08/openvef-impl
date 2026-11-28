"""Correct reference checker for F17 (Protocol L526); the same logic as checkers/f6_correct_checker.py.

AI-written (DEV-005): written by Claude Code under owner decision D-039. Not human-written, not independent.

It checks each trace row against the FIFO specification. The state is modelled from the inputs consumed at
each active edge (FIFO-003):
- reset edges (rst = 1) empty the FIFO (FIFO-010);
- otherwise a read occurs when rd_en = 1 and the FIFO is not empty (FIFO-020, FIFO-023), and a write occurs
  when wr_en = 1 and the FIFO is not full or a read occurs at the same edge (FIFO-024, FIFO-030); the read
  takes the oldest word before the write is stored, so there is no bypass (FIFO-025, FIFO-026).
The outputs after the edge must then be: rd_valid = 1 exactly when a read occurred (FIFO-021); rd_data equal
to the word read when rd_valid = 1, and not judged otherwise (FIFO-022); full, empty and almost_full from the
occupancy (FIFO-028, FIFO-029). Rows before the first reset edge are not judged (FIFO-013). After an illegal
input (FIFO-031), the behaviour is not specified, so no later row is judged.
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
