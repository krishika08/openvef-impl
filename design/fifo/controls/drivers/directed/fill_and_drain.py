"""Directed scenario fill_and_drain (Protocol L415, DIRECTED stream). AI-written (DEV-005, D-039, D-040); written
against the specification, not human-written and not independent of the evaluator.

Four writes fill the FIFO (FIFO-001, FIFO-028: full after the fourth; FIFO-029, FIFO-034: almost_full after the
third). A write with a read at full keeps it full and reads the oldest word (FIFO-030, FIFO-035). Four reads
return the words in order (FIFO-025) and clear almost_full at occupancy 2 (FIFO-034). A last read while empty
gives rd_valid = 0 (FIFO-023). No vector writes at full without a read (FIFO-041).
"""

PLAN = (
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


class Driver:
    def step(self, cycle_index, outputs_after_edge):
        if cycle_index >= len(PLAN):
            return "COMPLETE"
        wr_en, wr_data, rd_en = PLAN[cycle_index]
        return {"wr_en": wr_en, "wr_data": wr_data, "rd_en": rd_en}


def create_driver(seed):
    return Driver()
