"""F11 watchdog driver (Protocol L520). AI-written (DEV-005, D-039, D-040); not human-written, not independent.

Gives three legal vectors (one write, then reads), then its step call at cycle index 3 never returns, so the
watchdog fires and the trace is truncated.
"""

LOOP_AT = 3


class Driver:
    def step(self, cycle_index, outputs_after_edge):
        while cycle_index >= LOOP_AT:
            cycle_index = cycle_index + 1
        if cycle_index == 0:
            return {"wr_en": "1", "wr_data": "01011010", "rd_en": "0"}
        return {"wr_en": "0", "wr_data": "00000000", "rd_en": "1"}


def create_driver(seed):
    return Driver()
