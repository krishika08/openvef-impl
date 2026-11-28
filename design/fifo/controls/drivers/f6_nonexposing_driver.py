"""F6 non-exposing driver (Protocol L515). AI-written (DEV-005, D-039, D-040); not human-written, not independent.

Alternates one write and one read, so the occupancy is only ever 0 or 1 (FIFO-027). At those occupancies the
specification gives almost_full = 0 and full = 0 (FIFO-028, FIFO-029), so a change to the almost-full threshold
between 2 and 3 is never reached. Never writes at full (FIFO-041).
"""

CYCLES = 12


class Driver:
    def step(self, cycle_index, outputs_after_edge):
        if cycle_index >= CYCLES:
            return "COMPLETE"
        if cycle_index % 2 == 0:
            return {"wr_en": "1", "wr_data": format((cycle_index * 37) % 256, "08b"), "rd_en": "0"}
        return {"wr_en": "0", "wr_data": "00000000", "rd_en": "1"}


def create_driver(seed):
    return Driver()
