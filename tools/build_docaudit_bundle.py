"""Build dist/openvef-docaudit-bundle.zip for document audit #7 of the v1.3.7 CANDIDATE: D6-1 (the label boundary in
the C19 status test, test only), D6-2 (the D-032 interpretation replaced by the owner-authorized waiver DEV-003),
regression and the owners' stopping rule (D-033; docs/DOC-AUDIT7-BRIEF.md). Audit #1's bundle was built at 8d8be84
(release docaudit1-c4caff40), audit #2's at b9723b5 (docaudit2-4ee28f46), audit #3's at c24be7f (docaudit3-f82e1334),
audit #4's at 95fe05d (docaudit4-f01d344d), audit #5's at 431beaf (docaudit5-5f35d75b), audit #6's at 2451a00
(docaudit6-e9719fb3). D-032 added report #5 with its note, brief #5, audit #5's run, RUN-CONTINUITY-D032.md and
docs/DEVIATIONS.md. D-033 adds report #6 with its note, brief #6, audit #6's run and RUN-CONTINUITY-D033.md; D-034's
owner records (docs/owner-records/, quoted by DEV-004) are bundled for reference. The builder refuses a pre-D6-1 test,
docs without the DEV-003 waiver verbatim, or a DEVIATIONS.md that still carries the pre-D-034 DEV-004 label.

Contents: the candidate pack (with its CHANGELOG), the CORRECTIONS rationale, the build script, the PD records, the
v1.3.6 baseline for diffing, the latest candidate F18 run, the results.jsonl and summary.json of audit #2's, #3's and
#4's runs, the three continuity reports and tools/diff_runs.py with its tests, reports #1 to #4 with their notes, briefs
#3 and #4, the D-029 sweep list, the candidate-pack test, docs/ambiguities.md (D-031) and the brief. D-031 item 3 adds
the C18 candidate snapshot (the pack audit #3 audited), read from git at audit #3's build commit and stored under
prior/c18-candidate-pack/, so E01-E218 and every descriptor can be byte-compared with C19. Apart from that snapshot,
only git-tracked files of HEAD are bundled. The build refuses a dirty tree (any path) and checks the following. The candidate pack
matches its SHA256SUMS, and no file is unlisted. Each baseline file matches 27_SHA256SUMS.txt. The run was made in the
pinned image on a clean commit, from the bundled pack manifest, and its results hash agrees. Each continuity run's
results.jsonl matches its summary and the hash recorded by the audit that used it. The C18 snapshot matches its own
SHA256SUMS, with no file unlisted, and that SHA256SUMS is the manifest audit #3's run pinned; its E01-E218 CHANGELOG rows
and its fixture descriptors equal the current candidate's. Re-running diff_runs reproduces each
continuity report's verbatim section byte for byte, with no critical difference. Entries are sorted, with fixed
timestamps and modes, so the same commit gives the same bytes (for the same Python/zlib). Usage:
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
BRIEF = "docs/DOC-AUDIT7-BRIEF.md"
REPORT1 = "docs/reviews/doc-audit1-gpt6-2026-11-27.md"
REPORT1_SHA256 = "ba81408bde5339291d4b2ef25cab70b5eaa3e518412ecd45cdbeb11f54604b95"
REPORT2 = "docs/reviews/doc-audit2-gpt6-2026-11-27.md"
REPORT2_SHA256 = "b3534eee86e9af1f937e795223354498d994501be90dcc6e910d3a02297b6f13"
REPORT3 = "docs/reviews/doc-audit3-gpt6-2026-11-27.md"
REPORT3_SHA256 = "757ae6e53002b93bc8738cbe07fac36f865b6253dafd1d4d042fa2f3cd94a34f"
REPORT4 = "docs/reviews/doc-audit4-gpt6-2026-11-28.md"
REPORT4_SHA256 = "0cc724cd8c0661c216f956bd98628e2d359fe5702c87f5f3887a6046c8174850"
REPORT5 = "docs/reviews/doc-audit5-gpt6-2026-11-28.md"
REPORT5_SHA256 = "efb7b795c4a3dc5fe36d3151b3657fcfabcce704bd5240a85f23e0ccf1d725bb"
REPORT6 = "docs/reviews/doc-audit6-gpt6-2026-11-28.md"
REPORT6_SHA256 = "809b2d863542ed50353dab64b8ca29509812afffc5691781598ac2046f2078c7"
# D-032 item 2, verbatim (docs/ambiguities.md and docs/DEVIATIONS.md). Superseded by DEV-003 (D-033 item 1) and kept
# visible there, not deleted; the builder checks that it still is.
DEV_RUN_READING = ("the owners authorized development-only regression runs (run_class: development) during the v1.3.7 "
                   "document audits; they are not implementation or fixture execution under Protocol L555(3)'s gate and "
                   "are not F18 acceptance")
# D-033 item 1, verbatim: the owner-authorized deviation DEV-003 (docs/ambiguities.md and docs/DEVIATIONS.md).
DEV003_WAIVER = ("Protocol L555(3) bars implementation or fixture execution until the document audit and owner record are "
                 "complete. The owners waived this bar for development-only regression runs (run_class: development) from "
                 "the candidate's creation (b9f3d54) until v1.3.7 is adopted or rejected, to check that corrections did not "
                 "change outcomes. These runs are fixture execution; they are not F18 acceptance and are not counted as F18 "
                 "evidence. The waiver ends when v1.3.7 is adopted or rejected.")
# D-034: the label DEV-004 used before the owner records were added; it must not remain as the current label.
OLD_DEV004_LABEL = '**Label on every covered run until this closes:** "v1.3.6 gate not shown met (DEV-004)"'
NEW_DEV004_LABEL = '"v1.3.6 gate recorded as met; gaps DEV-004"'
OWNER_RECORDS = {"docs/owner-records/owner-decision-record-rev25.md":
                 "64b836147ea35dbd2c98489513e8575fa3f0d1a130a5cf6973ec76d39c32594b",
                 "docs/owner-records/owner-signoff-pack-rev95.md":
                 "13b805cb3ec9cf91eda4a3cee8aa35e380f5a17512124b834fd4274c8159a83d"}
# D-031 item 3: the C18 candidate (the pack audit #3 audited), from git at audit #3's bundle build commit; its manifest
# is the one audit #3's run pinned (run-v137c-20261127T153351Z, pack_manifest_sha256).
C18_COMMIT = "c24be7f"
C18_MANIFEST_SHA256 = "3294d2a3920e6c06874535fc54dc037e2bc0461473cab33b6558b61f27a84eb1"
C18_PREFIX = "prior/c18-candidate-pack"
# D-031 item 1, verbatim: recorded before audit #5 in docs/ambiguities.md and the brief.
STOPPING_RULE = ("If document audit #5 finds no BLOCKER, MAJOR or MINOR finding, the owners adopt v1.3.7 as the corrected "
                 "pack; every remaining LIMITATION is disclosed in DEVIATIONS.md. A lexical test cannot prove semantic "
                 "correctness; that is established by the audited manual review.")
# D-030 (D3-1): the runs audits #2 and #3 used, with the results hash each audit recorded, and the continuity reports
# (old run, new run; None = the latest candidate run).
PRIOR_RUNS = {"evidence/run-v137c-20261127T134318Z": "81c73e32cc7643c8900dd3f83c5824b5f7ae6ae82d90f140f4465b2f4c8acd09",
              "evidence/run-v137c-20261127T153351Z": "4b9714a43e7dfb4d9833de986302bf5f9d476da200e4e6871e967b608329284b",
              "evidence/run-v137c-20261127T163649Z": "9b07f3c8d390d84bc6096f898188fd9b18cf63192153b5f0a8b77db7f38ce21b",
              "evidence/run-v137c-20261128T033242Z": "51ad41354f1f354fe6b257d552c9d9a0aed96309b58b26876927ae4a9f5d6cfb",
              "evidence/run-v137c-20261128T042052Z": "ad446364ad604b93410c8b55dddeee0756f25b0f2fc71a7124482bf2497623cd"}
CONTINUITY = {"evidence/RUN-CONTINUITY-D030.md": ("evidence/run-v137c-20261127T134318Z",
                                                  "evidence/run-v137c-20261127T153351Z"),
              "evidence/RUN-CONTINUITY-D030-regression.md": ("evidence/run-v137c-20261127T153351Z",
                                                             "evidence/run-v137c-20261127T163649Z"),
              "evidence/RUN-CONTINUITY-D031.md": ("evidence/run-v137c-20261127T163649Z",
                                                  "evidence/run-v137c-20261128T033242Z"),
              "evidence/RUN-CONTINUITY-D032.md": ("evidence/run-v137c-20261128T033242Z",
                                                  "evidence/run-v137c-20261128T042052Z"),
              "evidence/RUN-CONTINUITY-D033.md": ("evidence/run-v137c-20261128T042052Z", None)}
VERBATIM = "## Tool report (verbatim)\n\n"
PATHS = [BASE, CAND, "proposals/v1.3.7/CORRECTIONS-v1.3.7-candidate.md", "proposals/v1.3.7/build_candidate.py",
         "docs/pack-defects.md", BRIEF, RUN, REPORT1,
         "docs/reviews/doc-audit1-gpt6-2026-11-27-NOTE.md", REPORT2, "docs/reviews/doc-audit2-gpt6-2026-11-27-NOTE.md",
         "proposals/v1.3.7/STATUS-SWEEP-D029.md", "tests/test_v137_candidate_pack.py", "docs/ambiguities.md",
         REPORT3, "docs/reviews/doc-audit3-gpt6-2026-11-27-NOTE.md", "docs/DOC-AUDIT3-BRIEF.md",
         "tools/diff_runs.py", "tests/test_diff_runs.py", *CONTINUITY,
         REPORT4, "docs/reviews/doc-audit4-gpt6-2026-11-28-NOTE.md", "docs/DOC-AUDIT4-BRIEF.md",
         "evidence/NOTE-D031-contended-runs.md",
         REPORT5, "docs/reviews/doc-audit5-gpt6-2026-11-28-NOTE.md", "docs/DOC-AUDIT5-BRIEF.md", "docs/DEVIATIONS.md",
         REPORT6, "docs/reviews/doc-audit6-gpt6-2026-11-28-NOTE.md", "docs/DOC-AUDIT6-BRIEF.md",
         *OWNER_RECORDS, "docs/owner-records/NOTE.md",
         *(f"{r}/{f}" for r in PRIOR_RUNS for f in ("results.jsonl", "summary.json"))]
OUT = REPO / "dist" / "openvef-docaudit-bundle.zip"
LIMIT = 20_000_000


def git(*args: str) -> str:
    return subprocess.run(["git", "-C", str(REPO), *args], check=True, capture_output=True, text=True).stdout


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sums(text: str) -> dict[str, str]:
    return {rel: digest for digest, rel in (line.split("  ", 1) for line in text.splitlines())}


def continuity_problems(files: dict[str, bytes]) -> list[str]:
    """D-030 (D3-1): each continuity report's verbatim section is what tools/diff_runs.py gives now, with exit 0."""
    import importlib.util
    import tempfile
    spec = importlib.util.spec_from_file_location("diff_runs", REPO / "tools/diff_runs.py")
    tool = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(tool)
    problems = []
    for doc, (old, new) in CONTINUITY.items():
        new = new or RUN
        text = files[doc]
        if text.count(VERBATIM.encode()) != 1:
            problems.append(f"{doc}: no single verbatim section")
            continue
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / "r.md"
            # Relative paths, as the report names them; run from the repository root.
            cwd = Path.cwd()
            try:
                import os
                os.chdir(REPO)
                code = tool.main([f"{old}/results.jsonl", f"{new}/results.jsonl", "--out", str(out)])
            finally:
                os.chdir(cwd)
            if code != 0:
                problems.append(f"{doc}: diff_runs exit {code} (critical difference)")
            if out.read_bytes() != text.split(VERBATIM.encode(), 1)[1]:
                problems.append(f"{doc}: verbatim section differs from what diff_runs gives now")
    return problems


def c18_snapshot() -> dict[str, bytes]:
    """D-031 item 3: every file of the candidate pack at C18_COMMIT, read from git objects (not the working tree)."""
    names = [n for n in subprocess.run(["git", "-C", str(REPO), "ls-tree", "-r", "-z", "--name-only", C18_COMMIT, "--",
                                        CAND], check=True, capture_output=True).stdout.decode().split("\0") if n]
    return {n[len(CAND) + 1:]: subprocess.run(["git", "-C", str(REPO), "show", f"{C18_COMMIT}:{n}"], check=True,
                                              capture_output=True).stdout for n in names}


def changelog_rows(text: bytes) -> dict[str, str]:
    import re
    return {m.group(1): m.group(0) for m in re.finditer(r"^\| (E\d+) \|.*$", text.decode("utf-8"), re.M)}


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
    if sha(files[REPORT3]) != REPORT3_SHA256:
        problems.append("audit #3 report is not the saved verbatim copy")
    if "C19 (D3-2)" not in files["proposals/v1.3.7/build_candidate.py"].decode() or \
            "| E237 | C19 |" not in files[f"{CAND}/CHANGELOG-v1.3.7-candidate.md"].decode():
        problems.append("the candidate predates D-030 cycle 4 (no C19 entries)")
    if sha(files[REPORT4]) != REPORT4_SHA256:
        problems.append("audit #4 report is not the saved verbatim copy")
    if sha(files[REPORT5]) != REPORT5_SHA256:
        problems.append("audit #5 report is not the saved verbatim copy")
    if sha(files[REPORT6]) != REPORT6_SHA256:
        problems.append("audit #6 report is not the saved verbatim copy")
    for rec, digest in OWNER_RECORDS.items():
        if sha(files[rec]) != digest:
            problems.append(f"{rec} is not the saved export")
    test_src = files["tests/test_v137_candidate_pack.py"].decode()
    if "class LabelledStatusRuleTests" not in test_src or ".isalnum()" in test_src or \
            'LABEL_PRECEDERS = frozenset(" (|*")' not in test_src or "_is_word_char(before" in test_src:
        problems.append("the candidate-pack test predates D-033 (D6-1)")
    for doc in ("docs/ambiguities.md", "docs/DEVIATIONS.md"):
        flat = " ".join(files[doc].decode().split())
        if DEV_RUN_READING not in flat:
            problems.append(f"{doc}: the superseded D-032 owner interpretation is not kept verbatim")
        if DEV003_WAIVER not in flat:
            problems.append(f"{doc}: the DEV-003 waiver (D-033 item 1) is not there verbatim")
    deviations = files["docs/DEVIATIONS.md"].decode()
    if OLD_DEV004_LABEL in deviations or NEW_DEV004_LABEL not in deviations:
        problems.append("docs/DEVIATIONS.md: DEV-004 predates D-034")
    if RUN.removeprefix("evidence/") not in deviations.split("## DEV-003", 1)[-1].split("## DEV-004", 1)[0]:
        problems.append(f"docs/DEVIATIONS.md: the latest run {RUN} is not listed in DEV-003")
    for doc in ("docs/ambiguities.md", BRIEF):
        if STOPPING_RULE not in " ".join(t for t in files[doc].decode().split() if t != ">"):  # blockquote markers
            problems.append(f"{doc}: the D-031 stopping rule is not there verbatim")
    c18 = c18_snapshot()
    c18_sums = c18.get(CAND_SUMS[len(CAND) + 1:], b"")
    if sha(c18_sums) != C18_MANIFEST_SHA256:
        problems.append("the C18 snapshot's SHA256SUMS is not the manifest audit #3's run pinned")
    c18_listed = sums(c18_sums.decode())
    if [r for r, h in c18_listed.items() if r not in c18 or sha(c18[r]) != h] or \
            set(c18) - set(c18_listed) - {CAND_SUMS[len(CAND) + 1:]}:
        problems.append("the C18 snapshot does not match its SHA256SUMS")
    changelog = "CHANGELOG-v1.3.7-candidate.md"
    old_rows, new_rows = changelog_rows(c18[changelog]), changelog_rows(cand[changelog])
    if len(old_rows) != 218 or any(new_rows.get(e) != row for e, row in old_rows.items()):
        problems.append("E01-E218 in the current CHANGELOG are not the C18 rows")
    descriptors = [r for r in c18 if r.startswith("41_F18_Fixture_Inputs/") and not r.endswith("fixture-index.json")]
    if not descriptors or any(cand.get(r) != c18[r] for r in descriptors):
        problems.append("a fixture descriptor differs between C18 and the current candidate")
    c18_vs_now = sorted(r for r in set(c18) | set(cand) if c18.get(r) != cand.get(r))
    if RUN in PRIOR_RUNS:
        problems.append(f"the latest candidate run {RUN} is a prior audit's run; re-run after D6-1")
    for run, recorded in PRIOR_RUNS.items():  # D-030 (D3-1): the prior runs are the ones the audits recorded
        res, summ = files[f"{run}/results.jsonl"], json.loads(files[f"{run}/summary.json"])
        if sha(res) != recorded or summ["results_sha256"] != recorded:
            problems.append(f"{run}: results.jsonl is not the file the audit recorded ({recorded[:8]})")
    problems += continuity_problems(files)
    if "OWNER-DECIDED" not in (summary.get("counts_by_category") or {}):
        problems.append("the run predates D-027 Phase B (no OWNER-DECIDED category)")
    if problems:
        sys.exit("; ".join(problems))

    for n, d in c18.items():
        files[f"{C18_PREFIX}/{n}"] = d
    info = {"purpose": "document audit #7 of the v1.3.7 CANDIDATE: D6-1 (the label boundary in the C19 status test; test "
                       "only, no pack text change), D6-2 (the owner-authorized waiver DEV-003 replacing the D-032 "
                       "interpretation), regression and the owners' stopping rule (D-033); not an implementation audit, "
                       "not F18",
            "stopping_rule": STOPPING_RULE, "stopping_rule_applies_to": "document audit #7 (D-033)",
            "owner_waiver_l555_3_dev003": DEV003_WAIVER,
            "superseded_owner_interpretation_l555_3": DEV_RUN_READING,
            "owner_records": OWNER_RECORDS,
            "c18_snapshot": {"path": C18_PREFIX, "from_commit": C18_COMMIT, "manifest_sha256": C18_MANIFEST_SHA256,
                             "files": len(c18), "e01_e218_rows_identical": len(old_rows),
                             "descriptors_identical": len(descriptors), "files_differing_from_current": c18_vs_now},
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
                 "bundle_sha256": "4ee28f4651c8af4dd09c50299f2909b641ddadf55c0c70255bb2e529cb2c5cee", "verdict": "NOT CLEARED"},
                {"report": REPORT3, "report_sha256": REPORT3_SHA256,
                 "bundle_sha256": "f82e13342664679e5caa8f56f42c5e6dde0ee1b04bab653fb7cc3c313290b26b", "verdict": "NOT CLEARED"},
                {"report": REPORT4, "report_sha256": REPORT4_SHA256,
                 "bundle_sha256": "f01d344d150d89aae0f545890a0e5c97ad2f49a4f6a0e88a9add6731fbfe73cb", "verdict": "NOT CLEARED"},
                {"report": REPORT5, "report_sha256": REPORT5_SHA256,
                 "bundle_sha256": "5f35d75bd7a5fdac36aa8f49be1ad049fa339f61f62d5a8af20143408136cd47", "verdict": "NOT CLEARED"},
                {"report": REPORT6, "report_sha256": REPORT6_SHA256,
                 "bundle_sha256": "e9719fb37ff9c548b22c6b8262ef93b911bca9bb06bc79844acf684d91f86982", "verdict": "NOT CLEARED"}],
            "continuity": {doc: {"old": old, "new": new or RUN} for doc, (old, new) in CONTINUITY.items()},
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
