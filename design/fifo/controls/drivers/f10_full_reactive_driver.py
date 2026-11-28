"""F10 full-reactive driver (Protocol L519). AI-written (DEV-005, D-039, D-040); not human-written, not independent.

Its next input depends on the sampled full (FIFO-040): it writes until the sampled full is 1, then reads until the
sampled empty is 1, twice, then completes. It writes only while it has not seen full in the current round, so
never while full without a read (FIFO-041).
"""

ROUNDS = 2
CYCLES = 60


class Driver:
    def step(self, cycle_index, outputs_after_edge):
        if outputs_after_edge.get("full") == "1":
            self.draining = True
        elif self.draining and outputs_after_edge.get("empty") == "1":
            self.draining = False
            self.rounds = self.rounds + 1
        if self.rounds >= ROUNDS or cycle_index >= CYCLES:
            return "COMPLETE"
        if self.draining:
            return {"wr_en": "0", "wr_data": "00000000", "rd_en": "1"}
        return {"wr_en": "1", "wr_data": format((cycle_index * 17) % 256, "08b"), "rd_en": "0"}


def create_driver(seed):
    driver = Driver()
    driver.draining = False
    driver.rounds = 0
    return driver
