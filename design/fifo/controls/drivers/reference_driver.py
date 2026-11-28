"""Reference driver for the FIFO feasibility controls (checklist item 14; F1, F3, F5, F7, F8, F13).

AI-written (DEV-005): the logic was written by Claude Code under owner decision D-039. The interface shell
(class Driver, step, create_driver) was typed by Krishika (commit 1f7d87b). Not human-written, not independent.

Stimulus: the driver vectors of the worked example in the FIFO specification (edges 1 to 19), then three reads
that empty the FIFO and read once more while empty (FIFO-023), then COMPLETE. The rows reach full (FIFO-028),
the simultaneous read and write at full (FIFO-030), no bypass at empty (FIFO-026), the registered almost-full
edges (FIFO-034, FIFO-035), and rd_valid = 0 rows after writes, where rd_data is don't-care (FIFO-022).

Legal inputs (FIFO-041): a planned write without a read is dropped when the sampled full is 1, so no vector
has wr_en = 1 and rd_en = 0 while full = 1. On the original RTL and the null netlist this never fires.
"""

# (wr_en, wr_data, rd_en) for cycle_index 0, 1, 2, ...; wr_data is MSB first (FIFO-005).
PLAN = (
    ("1", "00010001", "0"),
    ("1", "00100010", "1"),
    ("1", "00110011", "0"),
    ("1", "01000100", "0"),
    ("1", "01010101", "0"),
    ("1", "01100110", "1"),
    ("0", "00000000", "1"),
    ("0", "00000000", "1"),
    ("0", "00000000", "1"),
    ("1", "01110111", "1"),
    ("0", "00000000", "1"),
    ("1", "10001000", "1"),
    ("0", "00000000", "1"),
    ("0", "00000000", "1"),
    ("1", "10011001", "0"),
    ("1", "10101010", "0"),
    ("1", "10111011", "0"),
    ("1", "11001100", "1"),
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
        if outputs_after_edge.get("full") == "1" and wr_en == "1" and rd_en == "0":
            wr_en = "0"
        return {"wr_en": wr_en, "wr_data": wr_data, "rd_en": rd_en}


def create_driver(seed):
    return Driver()
