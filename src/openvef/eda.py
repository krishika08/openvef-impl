"""Host-side calls to the evaluator-only EDA harness tasks (sandbox/harness.py).

All Yosys work runs in the pinned image through the D-002 sandbox, like the null export.
"""
from __future__ import annotations

from openvef.sandbox import run_harness
from openvef.simulation import SimulationError

INTERFACE_TIMEOUT_S = 120.0  # build default


def interface(verilog: str, top: str) -> dict:
    """Top module and public ports (harness task `interface`)."""
    r = run_harness({"task": "interface", "verilog": verilog, "top": top}, INTERFACE_TIMEOUT_S)
    if r.timed_out or r.result is None or "error" in r.result:
        raise SimulationError(f"interface extraction failed: {r.result!r} {r.stderr_tail[-300:]}")
    return r.result


def icarus_compile(verilog: str, top: str) -> dict:
    """Compile with the pinned Icarus, `iverilog -g2012` (harness task `icarus`); the program is not run."""
    r = run_harness({"task": "icarus", "verilog": verilog, "top": top}, INTERFACE_TIMEOUT_S)
    if r.timed_out or r.result is None or "error" in r.result:
        raise SimulationError(f"icarus task failed: {r.result!r} {r.stderr_tail[-300:]}")
    return r.result


def run_yosys(files: dict, scripts: list, timeout_s: float) -> dict:
    """Run Yosys scripts on evaluator files (harness task `yosys`); `timeout_s` per script."""
    r = run_harness({"task": "yosys", "files": files, "scripts": scripts, "timeout_s": timeout_s},
                    timeout_s * max(1, len(scripts)) + 60.0)
    if r.timed_out or r.result is None or "error" in r.result:
        raise SimulationError(f"yosys task failed: {r.result!r} {r.stderr_tail[-300:]}")
    return r.result
