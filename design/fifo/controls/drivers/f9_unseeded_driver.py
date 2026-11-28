"""F9 unseeded driver (Protocol L518). AI-written (DEV-005, D-039, D-040); not human-written, not independent.

The same decisions as drivers/f9_seeded_driver.py, but drawn from the module-global random generator, reached
through an alias (the bypass File 30 L20 describes: "Static detection may be bypassed by aliasing"). The harness
does not seed it, so the null and mutant runs draw different words at cycle 0, a next-input divergence before any
raw divergence. A write without a read is dropped when the sampled full is 1 (FIFO-041).
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
    driver.rng = random
    return driver
