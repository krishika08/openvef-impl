"""F11 runs-to-cap driver (Protocol L520, L227). AI-written (DEV-005, D-039, D-040); not human-written, not independent.

Never returns COMPLETE: it alternates one write and one read for as long as the harness calls it, so the run ends
at the cycle cap with driver_completed = false. The occupancy stays at 0 or 1, so it never writes at full
(FIFO-041).
"""


class Driver:
    def step(self, cycle_index, outputs_after_edge):
        if cycle_index % 2 == 0:
            return {"wr_en": "1", "wr_data": format(cycle_index % 256, "08b"), "rd_en": "0"}
        return {"wr_en": "0", "wr_data": "00000000", "rd_en": "1"}


def create_driver(seed):
    return Driver()
