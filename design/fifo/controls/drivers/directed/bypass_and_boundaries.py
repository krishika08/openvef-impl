"""Directed scenario bypass_and_boundaries (Protocol L415, DIRECTED stream). AI-written (DEV-005, D-039, D-040);
written against the specification, not human-written and not independent of the evaluator.

A write with a read while empty stores the word and reads nothing (no bypass, FIFO-026); the next read returns it
(FIFO-021). A read while empty is legal and gives rd_valid = 0 (FIFO-023). Three writes raise almost_full at
occupancy 3 (FIFO-029, FIFO-034); a write with a read at occupancy 3 keeps it (FIFO-035); a read takes it to 2
and clears almost_full (FIFO-034); two reads empty the FIFO (FIFO-028). No vector writes at full (FIFO-041).
"""

PLAN = (
    ("1", "11110000", "1"),
    ("0", "00000000", "1"),
    ("0", "00000000", "1"),
    ("1", "00001111", "0"),
    ("1", "00111100", "0"),
    ("1", "11000011", "0"),
    ("1", "01010101", "1"),
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
