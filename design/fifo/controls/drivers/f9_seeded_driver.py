"""F9 seeded driver (Protocol L518). AI-written (DEV-005, D-039, D-040); not human-written, not independent.

Pseudo-random legal vectors from a local random.Random(seed) only (File 30 L20, L54). Cycle 0 always writes a
random word; later cycles write and read at random. A write without a read is dropped when the sampled full is 1
(FIFO-041). The same decisions as drivers/f9_unseeded_driver.py, from the harness-owned seed.
"""

import random

CYCLES = 24


class Driver:
    def step(self, cycle_index, outputs_after_edge):
        if cycle_index >= CYCLES:
            return "COMPLETE"
        word = format(self.rng.randrange(256), "08b")
        wr_en = "1" if cycle_index == 0 or self.rng.random() < 0.6 else "0"
        rd_en = "1" if cycle_index > 0 and self.rng.random() < 0.4 else "0"
        if outputs_after_edge.get("full") == "1" and wr_en == "1" and rd_en == "0":
            wr_en = "0"
        return {"wr_en": wr_en, "wr_data": word, "rd_en": rd_en}


def create_driver(seed):
    driver = Driver()
    driver.rng = random.Random(seed)
    return driver
