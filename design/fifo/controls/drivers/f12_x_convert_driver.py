"""F12 X-converting driver (Protocol L521). AI-written (DEV-005, D-039, D-040); not human-written, not independent.

Converts the sampled almost_full to an integer with int(..., 2) on every call, and reads when it is 1, writes
otherwise. On the null netlist almost_full is always 0 or 1 (FIFO-029), so the driver runs cleanly; on a design
that leaves almost_full undriven the conversion raises. A write without a read is dropped when the sampled full is
1 (FIFO-041).
"""

CYCLES = 30


class Driver:
    def step(self, cycle_index, outputs_after_edge):
        level = int(outputs_after_edge["almost_full"], 2)
        if cycle_index >= CYCLES:
            return "COMPLETE"
        if level == 1:
            return {"wr_en": "0", "wr_data": "00000000", "rd_en": "1"}
        wr_en = "0" if outputs_after_edge.get("full") == "1" else "1"
        return {"wr_en": wr_en, "wr_data": format((cycle_index * 29) % 256, "08b"), "rd_en": "0"}


def create_driver(seed):
    return Driver()
