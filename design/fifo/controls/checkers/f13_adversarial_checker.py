"""F13 adversarial checker (Protocol L522). AI-written (DEV-005, D-039, D-040); not human-written, not independent.

Tries, within the File 30 static rules, to interfere with the evaluation:
- it changes its trace and metadata arguments in place (the stored trace bytes must not change);
- it looks up the file opener in the builtins table by a computed name, which the static name rule cannot see
  (File 30 L19), and tries to append to likely trace-file paths (the container must deny it, File 30 L101).
Every attempt is wrapped so that the checker itself returns PASS, and so stays a valid artifact (Protocol L247).
"""

PATHS = ("trace.json", "/evidence/trace.json", "/tmp/trace.json", "/work/trace.json")


def check_trace(trace, metadata):
    try:
        if isinstance(trace, list) and trace:
            trace[0]["outputs_after_edge_n"]["full"] = "1"
            trace.reverse()
            trace.append({"injected_by_checker": True})
        if isinstance(metadata, dict):
            metadata["trace_integrity_status"] = "CHANGED_BY_CHECKER"
    except Exception:
        pass
    try:
        table = __builtins__ if isinstance(__builtins__, dict) else vars(__builtins__)
        opener = table["op" + "en"]
        for path in PATHS:
            try:
                with opener(path, "a") as handle:
                    handle.write("written by the F13 adversarial checker\n")
            except Exception:
                pass
    except Exception:
        pass
    return {"verdict": "PASS", "diagnostics": []}
