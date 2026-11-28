"""F6 exposing driver (Protocol L515). AI-written (DEV-005, D-039, D-040); not human-written, not independent.

Three writes take the occupancy to 1, 2 and 3 (FIFO-024, FIFO-027); four reads then empty the FIFO and read once
while empty (FIFO-023). Occupancy 2 is reached, where the specification gives almost_full = 0 (FIFO-029), so a
design that raises almost_full below 3 is exposed. Never writes at full (FIFO-041).
"""

PLAN = (
    ("1", "00010001", "0"),
    ("1", "00100010", "0"),
    ("1", "00110011", "0"),
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
