"""F17 REACTIVE_RANDOM driver (Protocol L415, L526). AI-written (DEV-005, D-039, D-040); not human-written, not
independent.

Legal reactive random stimulus from a local random.Random(seed) only (File 30 L20, L54). Each cycle it draws
wr_en, rd_en and wr_data. When the sampled full is 1 and it drew a write without a read, it adds the read, which
is legal (FIFO-030, FIFO-041). It never returns COMPLETE, so each run lasts to the cycle cap.
"""

import random


class Driver:
    def step(self, cycle_index, outputs_after_edge):
        wr_en = "1" if self.rng.random() < 0.55 else "0"
        rd_en = "1" if self.rng.random() < 0.45 else "0"
        word = format(self.rng.randrange(256), "08b")
        if outputs_after_edge.get("full") == "1" and wr_en == "1" and rd_en == "0":
            rd_en = "1"
        return {"wr_en": wr_en, "wr_data": word, "rd_en": rd_en}


def create_driver(seed):
    driver = Driver()
    driver.rng = random.Random(seed)
    return driver
