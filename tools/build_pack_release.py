"""Build dist/openvef-planning-v1.3.7.zip, the release of the adopted v1.3.7 pack (owner decision D-035 item 2).

Contents: baseline-v1.3.7/OpenVEF_Planning_v1_3_7/ (the adopted pack, byte-identical to the audited candidate
proposals/v1.3.7/pack) and baseline-v1.3.7/LABEL-v1.3.7-ADOPTED.md (the only "v1.3.7 ADOPTED" label; outside the pack
directory, so the pack manifest stays exact). Only git-tracked files of HEAD are bundled. The build refuses a dirty tree,
a pack that does not match its SHA256SUMS (missing, mismatched or unlisted files), a manifest or fixture index other
than the ones document audit #7 cleared, or any byte difference from the candidate. Entries are sorted, with fixed
timestamps and modes, so the same commit gives the same bytes (for the same Python/zlib). Usage:
    python3 tools/build_pack_release.py
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
TOP = "baseline-v1.3.7"
PACK = f"{TOP}/OpenVEF_Planning_v1_3_7"
LABEL = f"{TOP}/LABEL-v1.3.7-ADOPTED.md"
CAND = "proposals/v1.3.7/pack"
MANIFEST = "SHA256SUMS-v1.3.7-candidate.txt"
# Document audit #7 (CLEARED) and the runner's pinned values (runner/run_f18.py PACKS).
MANIFEST_SHA256 = "d64a91a8a13483866eb2788c19ce17ae268eac54d829d916bdd2926e161b3fff"
INDEX = "41_F18_Fixture_Inputs/fixture-index.json"
INDEX_SHA256 = "b43da9263e690951754526d8bd334680df96db5bb20a9c19fd4f01f681d4c65d"
OUT = REPO / "dist" / "openvef-planning-v1.3.7.zip"


def git(*args: str) -> str:
    return subprocess.run(["git", "-C", str(REPO), *args], check=True, capture_output=True, text=True).stdout


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def tracked(prefix: str) -> dict[str, bytes]:
    names = [n for n in git("ls-files", "-z", "--", prefix).split("\0") if n]
    return {n[len(prefix) + 1:]: (REPO / n).read_bytes() for n in names}


def problems() -> list[str]:
    out = []
    pack, cand = tracked(PACK), tracked(CAND)
    if MANIFEST not in pack:
        return [f"{PACK}/{MANIFEST} is not tracked"]
    if sha(pack[MANIFEST]) != MANIFEST_SHA256:
        out.append("the pack manifest is not the one document audit #7 cleared")
    if sha(pack.get(INDEX, b"")) != INDEX_SHA256:
        out.append("the fixture index is not the one document audit #7 cleared")
    listed = {rel: digest for digest, rel in (line.split("  ", 1) for line in pack[MANIFEST].decode().splitlines())}
    bad = sorted(r for r, h in listed.items() if r not in pack or sha(pack[r]) != h)
    unlisted = sorted(set(pack) - set(listed) - {MANIFEST})
    if bad or unlisted:
        out.append(f"the pack does not match its SHA256SUMS: bad {bad}, unlisted {unlisted}")
    if pack != cand:
        diff = sorted(r for r in set(pack) | set(cand) if pack.get(r) != cand.get(r))
        out.append(f"the adopted pack differs from the audited candidate: {diff}")
    if not (REPO / LABEL).is_file() or LABEL not in git("ls-files", "--", LABEL):
        out.append(f"{LABEL} is not tracked")
    return out


def main() -> int:
    if git("status", "--porcelain"):
        sys.exit("working tree is not clean: refuse to build")
    found = problems()
    if found:
        sys.exit("; ".join(found))
    names = sorted(n for n in git("ls-files", "-z", "--", TOP).split("\0") if n)
    OUT.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for n in names:
            entry = zipfile.ZipInfo(n, (1980, 1, 1, 0, 0, 0))
            entry.compress_type, entry.external_attr = zipfile.ZIP_DEFLATED, 0o100444 << 16  # read-only
            z.writestr(entry, (REPO / n).read_bytes())
    data = OUT.read_bytes()
    (OUT.parent / f"{OUT.name}.sha256").write_text(f"{sha(data)}  {OUT.name}\n")
    print(json.dumps({"zip": str(OUT.relative_to(REPO)), "bytes": len(data), "sha256": sha(data), "files": len(names),
                      "pack_manifest_sha256": MANIFEST_SHA256, "fixture_index_sha256": INDEX_SHA256,
                      "build_commit": git("rev-parse", "HEAD").strip()}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
