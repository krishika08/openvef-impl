"""F2 alignment driver (Protocol L511). AI-written (DEV-005, D-039, D-040); not human-written, not independent.

Echoes the registered output empty (FIFO-028) into the next-cycle input wr_en, as drivers/f2_echo.json declares:
the wr_en scheduled for edge n+1 is the empty sampled after edge n. rd_en is 1 on odd cycle indexes, and wr_data
is the cycle index (MSB first, FIFO-005). A write is requested only when empty = 1, so never while full (FIFO-041).
"""

CYCLES = 32


class Driver:
    def step(self, cycle_index, outputs_after_edge):
        if cycle_index >= CYCLES:
            return "COMPLETE"
        return {"wr_en": outputs_after_edge["empty"], "wr_data": format(cycle_index % 256, "08b"),
                "rd_en": "1" if cycle_index % 2 == 1 else "0"}


def create_driver(seed):
    return Driver()
