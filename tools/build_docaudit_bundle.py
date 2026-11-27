"""Build dist/openvef-docaudit-bundle.zip for document audit #3 of the v1.3.7 CANDIDATE: correction cycle 3 (C18,
D2-1 and the status sweep) and regression (D-029; docs/DOC-AUDIT3-BRIEF.md). Audit #1's bundle was built at 8d8be84
(release docaudit1-c4caff40), audit #2's at b9723b5 (release docaudit2-4ee28f46).

Contents: the candidate pack (with its CHANGELOG), the CORRECTIONS rationale, the build script, the PD records, the
v1.3.6 baseline for diffing, the latest candidate F18 run, reports #1 and #2 with their notes, the status sweep list,
the candidate-pack test, docs/ambiguities.md (D-029, A-059) and the brief. Only git-tracked files are bundled. The build
refuses a dirty tree (any path) and checks the following. The candidate pack matches its SHA256SUMS, and no file is
unlisted. Each baseline file matches 27_SHA256SUMS.txt. The run was made in the pinned image on a clean commit, from the
bundled pack manifest, and its results hash agrees. Entries are sorted, with fixed timestamps and modes, so the same
commit gives the same bytes (for the same Python/zlib). Usage:
    python3 tools/build_docaudit_bundle.py
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
BASE = "baseline/OpenVEF_Planning_v1_3_6"
CAND = "proposals/v1.3.7/pack"
CAND_SUMS = f"{CAND}/SHA256SUMS-v1.3.7-candidate.txt"
RUN = max((p.parent for p in (REPO / "evidence").glob("run-v137c-*/summary.json")),
          default=REPO / "missing").relative_to(REPO).as_posix()
BRIEF = "docs/DOC-AUDIT3-BRIEF.md"
REPORT1 = "docs/reviews/doc-audit1-gpt6-2026-11-27.md"
REPORT1_SHA256 = "ba81408bde5339291d4b2ef25cab70b5eaa3e518412ecd45cdbeb11f54604b95"
REPORT2 = "docs/reviews/doc-audit2-gpt6-2026-11-27.md"
REPORT2_SHA256 = "b3534eee86e9af1f937e795223354498d994501be90dcc6e910d3a02297b6f13"
PATHS = [BASE, CAND, "proposals/v1.3.7/CORRECTIONS-v1.3.7-candidate.md", "proposals/v1.3.7/build_candidate.py",
         "docs/pack-defects.md", BRIEF, RUN, REPORT1,
         "docs/reviews/doc-audit1-gpt6-2026-11-27-NOTE.md", REPORT2, "docs/reviews/doc-audit2-gpt6-2026-11-27-NOTE.md",
         "proposals/v1.3.7/STATUS-SWEEP-D029.md", "tests/test_v137_candidate_pack.py", "docs/ambiguities.md"]
OUT = REPO / "dist" / "openvef-docaudit-bundle.zip"
LIMIT = 20_000_000


def git(*args: str) -> str:
    return subprocess.run(["git", "-C", str(REPO), *args], check=True, capture_output=True, text=True).stdout


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sums(text: str) -> dict[str, str]:
    return {rel: digest for digest, rel in (line.split("  ", 1) for line in text.splitlines())}


def main() -> int:
    if git("status", "--porcelain"):  # clean-tree guard (as D-020 for the code bundle)
        sys.exit("working tree is not clean: refuse to build")
    names = sorted(p for p in git("ls-files", "-z", "--", *PATHS).split("\0") if p)
    files = {n: (REPO / n).read_bytes() for n in names}
    missing = [p for p in PATHS if not any(n == p or n.startswith(p + "/") for n in names)]
    if missing:
        sys.exit(f"not tracked: {missing}")

    cand = {n[len(CAND) + 1:]: d for n, d in files.items() if n.startswith(CAND + "/")}
    listed = sums(cand[CAND_SUMS[len(CAND) + 1:]].decode())
    bad = [r for r, h in listed.items() if r not in cand or sha(cand[r]) != h]
    unlisted = sorted(set(cand) - set(listed) - {CAND_SUMS[len(CAND) + 1:]})
    if bad or unlisted:
        sys.exit(f"candidate pack does not match its SHA256SUMS: bad {bad}, unlisted {unlisted}")
    base = {n[len(BASE) + 1:]: d for n, d in files.items() if n.startswith(BASE + "/")}
    base_sums = sums(base["27_SHA256SUMS.txt"].decode())
    bad = [r for r, d in base.items() if r != "27_SHA256SUMS.txt" and base_sums.get(r) != sha(d)]
    if bad:
        sys.exit(f"baseline files do not match 27_SHA256SUMS.txt: {bad}")

    summary = json.loads(files[f"{RUN}/summary.json"])
    problems = []
    if sha(files[f"{RUN}/results.jsonl"]) != summary["results_sha256"]:
        problems.append("results.jsonl does not match the run summary")
    if summary.get("pack_manifest_sha256") != sha(files[CAND_SUMS]):
        problems.append("the run used a different candidate manifest")
    if "+" in summary["git_commit"] or not summary["interpreter_status"].startswith("PINNED"):
        problems.append(f"run not from a clean commit in the pinned image: {summary['git_commit']}")
    if sha(files[REPORT1]) != REPORT1_SHA256:
        problems.append("audit #1 report is not the saved verbatim copy")
    if sha(files[REPORT2]) != REPORT2_SHA256:
        problems.append("audit #2 report is not the saved verbatim copy")
    if "C18 (D2-1" not in files["proposals/v1.3.7/build_candidate.py"].decode() or \
            "| E218 | C18 |" not in files[f"{CAND}/CHANGELOG-v1.3.7-candidate.md"].decode():
        problems.append("the candidate predates D-029 cycle 3 (no C18 entries)")
    if "OWNER-DECIDED" not in (summary.get("counts_by_category") or {}):
        problems.append("the run predates D-027 Phase B (no OWNER-DECIDED category)")
    if problems:
        sys.exit("; ".join(problems))

    info = {"purpose": "document audit #3 of the v1.3.7 CANDIDATE: correction cycle 3 (C18: D2-1 and the status sweep) "
                       "and regression (D-029); not an implementation audit, not F18",
            "brief": BRIEF, "candidate_pack": CAND, "candidate_pack_manifest_sha256": sha(files[CAND_SUMS]),
            "candidate_pack_files": len(cand), "baseline": BASE, "baseline_files": len(base),
            "candidate_run": RUN, "candidate_run_commit": summary["git_commit"],
            "candidate_run_counts": summary["counts"], "candidate_run_counts_by_category": summary.get("counts_by_category"),
            "owner_specified_fixtures": summary.get("owner_specified_fixtures"),
            "owner_decided_fixtures": summary.get("owner_decided_fixtures"),
            "previous_audits": [
                {"report": REPORT1, "report_sha256": REPORT1_SHA256,
                 "bundle_sha256": "c4caff409692797b4292a1c6851c79a722d1c60cbf4371e5611f5ef4f0a4cbd7", "verdict": "NOT CLEARED"},
                {"report": REPORT2, "report_sha256": REPORT2_SHA256,
                 "bundle_sha256": "4ee28f4651c8af4dd09c50299f2909b641ddadf55c0c70255bb2e529cb2c5cee", "verdict": "NOT CLEARED"}],
            "build_commit": git("rev-parse", "HEAD").strip(), "files": len(files),
            "label": "v1.3.7 CANDIDATE, not audited",
            "disclosure": "The corrections and this brief were written by Claude (Anthropic), the implementation author. "
                          "The auditor must not be a Claude model."}
    files["BUNDLE-INFO.json"] = (json.dumps(info, indent=2) + "\n").encode()
    files["MANIFEST.sha256"] = "".join(f"{sha(d)}  {n}\n" for n, d in sorted(files.items())).encode()
    OUT.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for n in sorted(files):
            entry = zipfile.ZipInfo(n, (1980, 1, 1, 0, 0, 0))
            entry.compress_type, entry.external_attr = zipfile.ZIP_DEFLATED, 0o100644 << 16
            z.writestr(entry, files[n])
    data = OUT.read_bytes()
    if len(data) >= LIMIT:
        OUT.unlink()
        sys.exit(f"bundle is {len(data)} bytes; the limit is {LIMIT}")
    (OUT.parent / "openvef-docaudit-bundle.zip.sha256").write_text(f"{sha(data)}  {OUT.name}\n")
    print(json.dumps({"zip": str(OUT.relative_to(REPO)), "bytes": len(data), "sha256": sha(data), **info}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
