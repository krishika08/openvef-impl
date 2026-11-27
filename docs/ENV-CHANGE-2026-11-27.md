# Environment change, 27 Nov 2026: pinned sandbox image rebuilt

**Recorded by:** Claude (Claude Opus 5.5, via Claude Code), at Krishika's instruction, before any evidence run on the
rebuilt image. This is a recorded environment change under D-002a, not a silent swap. Nothing in `sandbox/Dockerfile`
or `requirements.lock` changed, so the image tag is the same (`openvef-sandbox:693f422c7a112dcd`). The image ID and the
two Yosys binaries changed.

## 1. Why

- During D-027 Phase B, on 27 Nov 2026 between the 10:34 UTC host restart and about 11:10 UTC, every container start failed with
  `failed to extract layer sha256:dd57f903…: NotFound: failed to get reader from content store: content digest
  sha256:37fb86c2…: not found`. `docker image ls` showed the tag at image ID `22fd0c527d66…` with 13.9 kB of content. The
  image's layers were missing from Docker's content store.
- **Cause: not determined.** The host was restarted at 2026-11-27 10:34 UTC (`uptime -s`). That is after the last good
  evidence runs (05:22–05:32 UTC, all on image ID `565e5547…`). Docker's event history starts at that restart, and the
  daemon's storage directory cannot be read from this account, so it cannot be shown when or why the layers went
  missing, or why the tag pointed at `22fd0c52…` instead of `565e5547…`.
- **Disk was not the cause.** After the failure: `df -h /` 32G size, 17G used, 14G available (56%); `docker system df`:
  0 images, 0 containers, 0 volumes, 196.7 MB build cache. After the rebuild: 62% used; 1 image (387.4 MB), build cache
  1.567 GB. No dangling or unused images existed to prune, so none were pruned.
- **Disclosure: what Claude removed.** Before the owner's instruction on this change, Claude ran
  `docker image rm -f openvef-sandbox:693f422c7a112dcd` (deleted the broken `22fd0c52…`) and
  `docker builder prune -af`. That command removed the whole BuildKit build cache, whose size was not recorded, and is
  broader than pruning dangling or unused images. The image was then rebuilt with
  `docker build -q -t openvef-sandbox:693f422c7a112dcd -f sandbox/Dockerfile .`, finished 2026-11-27T11:37:39Z.

## 2. Old and new image

| Item | Old image (recorded in `run-20261126T163836Z`, `run-20261127T052242Z`, `run-v137c-20261127T052443Z`, `controls-20261127T052649Z`, `container-tests-20261127T053222Z`) | New image (probed 27 Nov 2026 in the rebuilt image, with `openvef.sandbox.toolchain_identity()`) | Same? |
|---|---|---|---|
| Image tag | `openvef-sandbox:693f422c7a112dcd` | `openvef-sandbox:693f422c7a112dcd` | yes |
| Image ID | `sha256:565e55470476be93f0b6b6ea6ec88776b0332598c77a9a3fba0aa305c2971c3f` | `sha256:fa254bba381bfe04e1d1c5dc2607511cdb0f982a881c2ecb9a40ed691fe866e0` | **no** |
| Base image digest | `python@sha256:07d4824036af339fa1b6ef769cc99d9c10a141769538b52b3b597c84f7a7b535` | same (pinned in `sandbox/Dockerfile`) | yes |
| `sandbox/Dockerfile` SHA-256 | `f40c5f43…fe48` | unchanged | yes |
| `requirements.lock` SHA-256 | `e12f3a4c…d7d1` | unchanged | yes |
| `sys.version` | `3.11.18 (main, Nov  5 2026, 07:57:53) [GCC 14.2.0]` | same | yes |
| Interpreter SHA-256 (`/usr/local/bin/python`) | `92d7e40ec50be176cb1b790c7568b7e08cd862137b5aa69f1413ba1967886b79` | same | **yes** |
| Yosys version line | `Yosys 0.71+post (git sha1 5628c13240f670b97aaaca3d47940c4afb8ff572, Release, GNU /usr/bin/c++ 14.2.0)` | same | yes |
| Yosys source pin (`EDA_PINS`) | yosys 0.71, tarball `2ec7c2ee…ef2a5`; mcy `5a2cad0c…`; Debian snapshot `20261104T212339Z` | same | yes |
| `yosys` binary SHA-256 | `0bf886591a8e2b0f45fea92b2022f61d5a2213c370904ff87bbdeadbbee4e6af` | `3d4e300dcea16992b214f53e4b06a4f9d199685b874b035f2c9a390454e9e62f` | **no** |
| `yosys-abc` binary SHA-256 | `2bc88ba4923042e96ce0da15b993b892a70ed14d9f0c625c394aa6cad48bcf7b` | `e8fc5ad6be3dc54f673c143a0a226c98f2fba488a6f395b7226ee9a7312ecfe2` | **no** |
| Icarus `iverilog` | `Icarus Verilog version 12.0 (stable) ()`, deb `12.0-2+b1`, SHA-256 `99633b21…8462` | same | yes |
| Icarus `vvp` | `Icarus Verilog runtime version 12.0 (stable) ()`, SHA-256 `dc287630…c1df` | same | yes |
| MCY | commit `5a2cad0c…`, SHA-256 `e56df004…4a01` | same | yes |
| cocotb | 2.1.0 | 2.1.0 (`cocotb/__init__.py` SHA-256 `9233c62d…9566`; not recorded in the old image) | version yes |
| jsonschema | 4.26.0 | 4.26.0 (`jsonschema/__init__.py` SHA-256 `a7e470e1…4c67`; not recorded in the old image) | version yes |
| All 13 distributions the runner records | as in the old runs | equal (name-normalised); installed with `pip install --require-hashes` from the unchanged lock | yes |

**Reading of the differences.**
- Yosys and yosys-abc are compiled from the pinned source in the Dockerfile's first stage. The same source,
  compiler and flags gave different binaries, so that build is not byte-reproducible. The cause (for example embedded
  build paths, timestamps or link order) has not been investigated. Every other recorded toolchain binary comes from a
  pinned Debian package or the pinned base image, and is byte-identical.
- The image ID changes whenever any layer's bytes change, so the Yosys difference alone is enough to change it.
- The old image's per-file package hashes were never recorded and the image no longer exists, so for cocotb and
  jsonschema only the versions and the hash-checked lock show that they are the same.

## 3. Equivalence check (owner instruction, 27 Nov 2026)

The v1.3.6 run on the new image must reproduce every record of `run-20261126T163836Z` except measured timings. If
anything else differs, work stops and the owner is told. Result: section 4, added after the run.
