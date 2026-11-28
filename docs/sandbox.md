# Artifact-execution sandbox

Owner decision **D-002** (Krishika, 23 Nov 2026; Ayush's confirmation pending): F18
artifact execution uses Docker image `python:3.11.18-slim` pinned by digest, run with
`--network=none --read-only --cap-drop=ALL --security-opt=no-new-privileges`, a non-root
user, tmpfs for scratch, pids/memory/CPU limits and a wall-clock timeout. The pinned
`requirements.lock` is installed with `--require-hashes` inside the image.

Owner decision **D-002a** (Krishika, 23 Nov 2026; Ayush's confirmation pending): the
pinned interpreter for all F18 evidence is the CPython in that container. The whole
runner, static stages included, runs in the image; host Python is for development only.

Owner decision **D-003** (Krishika, 23 Nov 2026; Ayush's confirmation pending): toolchain
per the Charter ("Cocotb; Icarus Verilog initially"), pinned at the latest stable versions
installable in the image: cocotb from `requirements.lock` with hashes, Icarus Verilog from
the image's package manager with its exact version recorded.

Pack requirements this implements: File 30 §3 L39 ("Runtime signature checks and the
`create_driver` return-type check run after import in the restricted execution container.
The container sandbox is the security boundary and must be pinned and tested before
F16.") and File 30 §6 ("The runtime sandbox denies network, filesystem access beyond the
designated temporary output directory, environment variables, wall-clock reads,
subprocess and simulator access. It must allow the interpreter to initialize the
standard-library `random` module … F18 must test `import random` plus
construction/use of `random.Random(seed)` inside the sandbox before F16.").

**Status:** development configuration. The pack also requires the sandbox to be "pinned
and tested before F16". The tests below are the F18-side part of that. Whether this
configuration is adequate as the security boundary for F16 is for the owners to review.

## Image

| Item | Value |
|---|---|
| Base image | `python@sha256:07d4824036af339fa1b6ef769cc99d9c10a141769538b52b3b597c84f7a7b535` (`python:3.11.18-slim`, linux/amd64, resolved with `docker pull` on 23 Nov 2026) |
| Pinned interpreter (D-002a) | `3.11.18 (main, Nov  5 2026, 07:57:53) [GCC 14.2.0]`, `/usr/local/bin/python3.11`, SHA-256 `92d7e40ec50be176cb1b790c7568b7e08cd862137b5aa69f1413ba1967886b79` |
| Icarus Verilog (D-003) | Debian package `iverilog` `12.0-2+b1` from snapshot.debian.org (`iverilog -V`: "Icarus Verilog version 12.0 (stable)"); `.deb` SHA-256 `febe027d2d3f5a7e570844d55758339ab5490acc09f404f214a8719d89d07056`, checked with `sha256sum -c` before `dpkg -i`; `/usr/bin/iverilog` SHA-256 `99633b21…8462`, `/usr/bin/vvp` SHA-256 `dc287630…c1df` |
| cocotb (D-003) | `cocotb==2.1.0` (cp311 manylinux wheel) and its dependencies `find-libpython==0.5.1`, `iniconfig==2.3.1`, `packaging==26.3`, `pluggy==1.7.0`, `pygments==2.21.0`, `pytest==9.2.0`, all with hashes in `requirements.lock` (pip-tools 7.7.0 `pip-compile --generate-hashes`, run in the pinned base image). Earlier pins are unchanged. |
| Yosys (D-004) | v0.71 (latest release, 12 Nov 2026), built from the release tarball `yosys.tar.gz`, SHA-256 `2ec7c2ee63bb9b4065d6d5fff2786a1455e834f90ede8eb1d47791153ebef2a5` (GitHub-published digest), checked with `sha256sum -c`; tag `v0.71` → commit `b4c586fd37d0ec61bb38fc1a85fd6a2fde48fcd1`; tarball `.gitcommit` `5628c13240f670b97aaaca3d47940c4afb8ff572` (asserted; GitHub compare: 0 files differ from the tag commit). CMake `release` preset, Tcl/editline/Python/unit tests off, static libs. Installed in `/usr/local/bin`: `yosys` SHA-256 `0bf886591a8e2b0f45fea92b2022f61d5a2213c370904ff87bbdeadbbee4e6af`, `yosys-abc` SHA-256 `2bc88ba4923042e96ce0da15b993b892a70ed14d9f0c625c394aa6cad48bcf7b`; `yosys -V` reports "Yosys 0.71+post (git sha1 5628c132…)": the `+post` comes from the tarball being built from the CI merge commit, which has no file differences from the tag |
| MCY (D-004) | v0.71, tag object `b062a44a1978ed41c5dcb87a5dad41d8112497d2` → commit `5a2cad0cbefceb7f23051c08348bd23128fd1046` (no release asset; pinned by commit, asserted after checkout). `/usr/local/bin/mcy` (= `mcy.py`) SHA-256 `e56df004f5960d811cf8f468b21fce77922ce5cb541c4faf400fdab8af944a01`, scripts in `/usr/local/share/mcy/scripts`. Its `click` dependency is `click==8.5.1` in `requirements.lock` (D-004a); `mcy --help` runs |
| EDA build stage | Separate stage `eda-build`, same base digest; build tools (gcc, cmake, bison, flex, …) from snapshot.debian.org `20261104T212339Z`, the snapshot in the base image's own apt sources. Only `/opt/eda` is copied into the final image. `/usr/local/share/EDA_PINS` records the pins; `toolchain_identity` records versions and binary hashes in every run |
| Build | [sandbox/Dockerfile](../sandbox/Dockerfile): base by digest; iverilog `.deb` from snapshot.debian.org by URL, version and SHA-256; `pip install --require-hashes --no-deps -r requirements.lock`; user `sandbox` uid/gid 10001. The pip step alone sets `OPENSSL_CONF` to a temporary file limiting TLS groups to X25519/P-256: the base image's OpenSSL 3.5.7 offers a post-quantum key share, and its large ClientHello is dropped on this Codespace's path to PyPI (handshake timeout; the same container reaches PyPI with the classical groups). Every installed file is still hash-checked, so the installed bytes do not depend on it |
| click (D-004a) | `click==8.5.1` with both hashes in `requirements.lock`. MCY states no version bound, so this is what pip-tools 7.7.0 resolved in the pinned base image (same command and TLS setting as above); the other pins are unchanged |
| Build context | `.dockerignore` admits only `requirements.lock` |
| Local tag | `openvef-sandbox:<first 16 hex of SHA-256 of the sha256sum listing of sandbox/Dockerfile and requirements.lock>`, rebuilt automatically when either changes |

"Latest stable" was checked on 23 Nov 2026 in the pinned base image: `pip index versions
cocotb` lists 2.1.0 as newest; `apt-cache policy iverilog` lists only 12.0-2+b1 (Debian
13 "trixie"), and Icarus 12.0 is the upstream stable release.

Source of the `.deb`: snapshot.debian.org,
`https://snapshot.debian.org/archive/debian/20240313T032420Z/pool/main/i/iverilog/iverilog_12.0-2%2Bb1_amd64.deb`.
`20240313T032420Z` is the archive timestamp at which this file (SHA-1
`dfb2b1db5303c41fcb565ab69480165875ad39d3`, 2,046,080 bytes) was first seen, per the
snapshot `mr/binary/iverilog/12.0-2+b1/binfiles` API. The same SHA-256 check runs before
`dpkg -i`. The build therefore no longer depends on the live Debian archive. After the
switch, `/usr/bin/iverilog` and `/usr/bin/vvp` have the same SHA-256 as before, and a
containerized smoke run gave results identical to run-20261123T195936Z. The image ID
changes, because the Dockerfile changed, and each run records it.

D-004 "latest stable" was checked on 24 Nov 2026 with the GitHub API: Yosys
`releases/latest` is `v0.71` (published 2026-11-12), and MCY's newest `v*` tag is `v0.71`
(tagged 2026-11-10; MCY publishes no releases). Debian trixie carries only Yosys 0.52,
so Yosys is built from source. The null-netlist export uses Yosys only; the frozen
export script, mutation modes and mutant population stay owner items (Protocol L544).
Repeatability is tested by `tests/test_netlist_export.py` on a test-only toy design.
After D-004a, `mcy --help` runs in the image, and the test checks it. The containerized
smoke run on the new image (24 Nov 2026, outside `evidence/`) gave 129/0/15/0, with
per-fixture results identical to run-20261123T195936Z.

## Where things run (D-002a)

| Role | Where | Interpreter |
|---|---|---|
| F18 runner: index/hash checks, all static stages, ledger, serializer, comparisons, evidence writing | runner container from the pinned image ([runner/runner-container.args](../runner/runner-container.args)) | pinned |
| Each artifact execution (factory, checker invocation, later simulation) | a fresh artifact container from the same image ([runner/artifact-container.args](../runner/artifact-container.args)) | pinned |
| Host | [runner/run_f18_container.sh](../runner/run_f18_container.sh): bash only; builds the image, starts the runner, launches artifact containers on request | none |

The runner container has no Docker access. When it needs an artifact execution it writes
`OPENVEF_SANDBOX_REQUEST <timeout> <base64 JSON>` on stdout; the broker starts one
artifact container running the fixed command `python -I /opt/openvef/harness.py` with
that JSON on stdin and the flags from `artifact-container.args`, and replies with the
exit code and base64 output, or `TIMEOUT` (after `docker kill` and `docker rm -f`). The
runner chooses neither the command, the image nor the flags. The broker does not read
results.

The runner container is isolated like an artifact container (`--network=none`,
`--read-only`, `--cap-drop=ALL`, `no-new-privileges`, tmpfs `/tmp`) except: it runs as the
invoking host uid so it can write its one evidence directory, which is the only writable
mount; the baseline and the `src/`, `runner/`, `sandbox/` trees are mounted read-only; it
has larger limits (1 GiB, 128 pids, 2 CPUs).

Every run's `summary.json` records `interpreter_status` (`PINNED` only when the runner is
in the container and `sys.version` and the interpreter SHA-256 equal the pinned values),
the interpreter, all distributions, and under `sandbox`: base digest, image tag and ID,
Dockerfile and lock SHA-256, broker SHA-256, both flag lists, the artifact command,
harness SHA-256s, Docker server version, host kernel, and the toolchain (cocotb version,
`iverilog -V`/`vvp -V` lines, `.deb` version, binary SHA-256s). A run started with
`python runner/run_f18.py` on the host records `NOT_PINNED` and is not evidence.

`OPENVEF_EVIDENCE_ROOT` redirects the run directory for smoke tests outside `evidence/`.

## What is isolated, and how

Artifact-container flags are defined only in
[runner/artifact-container.args](../runner/artifact-container.args), read by both the
broker and the development launcher (`docker_argv` in
[src/openvef/sandbox.py](../src/openvef/sandbox.py)). Each execution starts a new
container and removes it afterwards (`--rm`).

| Concern | Mechanism | Test (`tests/test_sandbox.py`) |
|---|---|---|
| Network | `--network=none`: only the loopback interface exists; no route, no DNS | `test_no_network`: TCP connect fails, `getaddrinfo` fails, interfaces are `['lo']` |
| Filesystem | `--read-only` root; harness directory mounted `:ro`; only `/tmp` writable: tmpfs, 16 MiB, `noexec,nosuid,nodev` | `test_read_only_root_and_writable_tmp`: writes to `/usr/local/lib`, `/opt/openvef`, `/`, `/home` fail; `/tmp` writable; a file in `/tmp` cannot be executed |
| Identity and privileges | `--user=10001:10001` (also the image `USER`); `--cap-drop=ALL`; `--security-opt=no-new-privileges` | `test_non_root_no_capabilities_no_new_privileges`: uid/euid/gid 10001; `CapEff` and `CapPrm` are zero; `NoNewPrivs: 1` |
| Environment variables | No host variables are passed; only `PYTHONHASHSEED=0`, `PYTHONDONTWRITEBYTECODE=1`, `PYTHONUNBUFFERED=1` and the image's own `PATH`/`HOME`/`HOSTNAME`/`LANG`/`GPG_KEY`/`PYTHON_*` | `test_environment_is_minimal` (it caught `PIP_*` variables leaking from the Dockerfile; now scoped to the build step) |
| Processes | `--pids-limit=64`; `--ipc=none` | `test_pids_limit`: fork loop stops at the limit |
| Memory, CPU, files | `--memory=256m --memory-swap=256m` (no swap); `--cpus=1`; `--ulimit nofile=64:64` | — (configuration only) |
| Wall-clock time | Host timeout (default 20 s per container). On expiry the launcher runs `docker kill` and `docker rm -f` by the container's unique name | `test_timeout_kills_and_removes_container`: a busy loop under a 4 s limit is reported as timed out, and no `openvef-*` container remains |
| Simulator | Icarus Verilog and cocotb are installed (D-003) for the harness. Artifact code cannot reach them: `cocotb` is not on the import allow-list (static and runtime), and subprocess/`os` are not importable | `test_artifact_cannot_import_cocotb` |
| Determinism | `PYTHONHASHSEED=0`, so `str`/`bytes` hashing (set iteration order) is the same in every run (A-036) | — |
| `random` | Standard-library `random` initializes normally; artifacts may only use a local `random.Random(seed)` (enforced statically at IMPORT_POLICY) | `test_seeded_local_random_works`: same sequence as the host for seed 7 |

What the container does **not** do by itself: it does not stop artifact code from
calling allowed standard-library functions. The import allow-list, prohibited names and
module-global `random` are enforced statically at IMPORT_POLICY. At runtime, the
artifact process enforces the same import allow-list for imports made by artifact code (File 30
§6 "Enforce the same import allow-list statically and at runtime"; see
`sandbox/artifact_worker.py`). The seccomp filter and the container flags are what contain anything the static and
runtime checks miss.

## Harness and integrity guard

**Process separation (D-015, audit A9-1).** No artifact code runs in an evaluator interpreter.
- [sandbox/artifact_worker.py](../sandbox/artifact_worker.py) is the artifact process. Before
  loading artifact code it keeps only its two pipes, limits its address space, and installs a
  seccomp allow-list (pipe, memory and exit calls). Everything else fails with EPERM: file opens,
  `/proc`, sockets, fork/exec, signals, ptrace. It checks that the filter works, and refuses to
  continue otherwise.
- [sandbox/artifact_proc.py](../sandbox/artifact_proc.py) is the evaluator side: plain JSON in,
  schema-checked tagged plain data out. It and the harness compute every verdict.
- A separate process without seccomp is not enough: a same-uid child can write to the
  evaluator's stdout through `/proc` (observed). Tests: `tests/test_artifact_isolation.py`.
- Residuals: those under "Runtime checks" (D-019); CPU is
  shared, so the watchdog still matters; and those under "Wall-clock reads" below.

### Runtime checks (D-019, audit A9-2; File 30 §3 L35, L37, L39)

A process in which artifact code has run can report anything: it can replace globals, code objects and
closures, or write to the pipe. So:

| Check | Where measured | Can artifact code forge it? |
|---|---|---|
| `create_driver`, `Driver.step`, `check_trace` as defined: names, kinds, counts, defaults, plain `def`, bound once | a fresh confined process that only compiles the source (`inspect_source`) | No: no artifact code has run there |
| the same functions' code objects as they are after execution (replaced at run time) | the artifact process, self-reported; a wrong report rejects | **Yes** |
| the literal `inspect.signature` of the same functions, after import (File 30 L35, L37, L39; D-022): must not raise, and its names, kinds and counts must equal the first row's | the artifact process, self-reported; a wrong report rejects | **Yes** |
| `create_driver(seed)` returned a `Driver` | the artifact process, self-reported; a wrong report rejects | **Yes** |
| driver vectors, checker returns, verdicts | computed by the evaluator from plain data | No; the data is the artifact's own answer |

**Both measurements are taken (D-022).** File 30 L35 and L37 name `inspect.signature`, so the worker calls it after
import, as well as the trusted compile-only measurement. `__signature__` or `__wrapped__` that makes it raise or disagree is
`RUNTIME_SIGNATURE`; one that agrees changes nothing. The comparison covers names, kinds and counts, as L35 says (A-058).
The literal result is self-reported: outside the PROVEN fragment an artifact can still forge it, so the
SELF_REPORTED residual below remains. An artifact that breaks its own builtins can now fail here too.

**Static proof.** `src/openvef/runtime_basis.py` marks each source PROVEN or SELF_REPORTED from its text. PROVEN
means the source uses only listed builtins and module names, no dunder, frame or namespace access, never
rebinds or passes on `Driver` or `create_driver`, and returns only `Driver()` objects, so the three forgeable rows
hold by construction, if CPython behaves as documented. SELF_REPORTED means not shown; it is not evidence of forgery.
F18 runs record it per fixture (`runtime_checks`) and list the rest (`runtime_checks_self_reported`).

**Residual (not closed).** A SELF_REPORTED driver can return an object that is not a `Driver`, or replace
`Driver.step` (or what `inspect.signature` says of it) at run time, and report otherwise; a SELF_REPORTED checker can replace `check_trace` likewise.
`test_residual_forged_state_after_execution` pins this.
- **Consequence:** a structurally invalid artifact can be counted valid (no `ENTRY_POINT_REJECT`, `RETURN_TYPE` or
  `RUNTIME_SIGNATURE`), which affects the validity endpoint for that artifact.
- **Not affected:** traces, masked comparison, verdict classification, other artifacts and later runs. A driver's
  vectors are still checked one by one, and the checker's return is classified by the evaluator.
- **For the owners:** whether a SELF_REPORTED artifact may count as valid in confirmatory use.

**Owner decision (D-020).** No pack rule changed, so this is a decision, not a deviation.
- **F18:** a SELF_REPORTED runtime check does not change the fixture verdict. A SELF_REPORTED pass
  stays PASS and carries the visible label "SELF_REPORTED (D-020): runtime check not statically
  PROVEN", recorded per result (`self_reported_runtime_checks`, `self_reported_label`) and listed
  in the run summary (`runtime_checks_self_reported`, `self_reported_label`).
- **Confirmatory use:** the validity endpoint is reported two ways — **primary**, as measured (each
  runtime report at face value); and a **pre-registered sensitivity**, with every SELF_REPORTED
  artifact counted invalid. The **count of SELF_REPORTED artifacts per arm** (and design) is
  reported alongside (analysis rule in [F1-F17-plan.md](F1-F17-plan.md)).
- This takes the owner decision the residual left open; it does **not** close A9-2, which is still
  not re-audited.

### Wall-clock reads (D-016; File 30 §6 L101)

**What IMPORT_POLICY already rejects** (File 30 §2; `StaticClockRouteTests`):
- importing `time`, `datetime`, `os`, `sys`, `ctypes`, `threading`, `asyncio`, `signal`, `select` or
  `resource`, at any depth (`IMPORT_NOT_ALLOWED`);
- `__import__`, `eval`, `exec`, `compile`, `open` as names (`PROHIBITED_BUILTIN`);
- `random._os` and every other direct `random.` attribute except `Random` (`GLOBAL_RANDOM_USE`).

**What it does not reject:** attribute paths through allowed modules, such as
`collections._sys.modules["time"].time()` or `statistics.sys`, `getattr(random, "_os")`, and
`object.__subclasses__()`. The pack's static rules do not cover them (A-016, A-017), so only the
sandbox stops them.

**What the worker removes before artifact code loads** (`remove_clocks`, `SYSCALLS`). "Before" is the
D-015 worker probed in the pinned container on 25 Nov 2026.

| Clock source | Before | Now | Relies on |
|---|---|---|---|
| `time`, `clock_gettime` system calls | allowed | not on the seccomp allow-list: EPERM, every clock ID | seccomp(2) filter, deny by default |
| vDSO (libc `clock_gettime`, `time`, `gettimeofday`; Python `time.time()` and the rest) | live time | vDSO code replaced by "return -EPERM"; `[vvar*]` data pages unmapped; `/proc/self/maps` is re-read and must list neither | vdso(7): these calls need no kernel entry, so seccomp does not see them |
| `fstat` on the pipes | `st_mtime` is the current time | EPERM (also stat, newfstatat, statx) | seccomp allow-list |
| `futex` with an absolute CLOCK_REALTIME deadline | says whether that time has passed | EPERM; the worker has one thread and needs no futex | futex(2) FUTEX_WAIT_BITSET, FUTEX_CLOCK_REALTIME |
| RDTSC, RDTSCP | live counter | SIGSEGV | prctl(2) PR_SET_TSC, PR_TSC_SIGSEGV (read back with PR_GET_TSC) |
| RDPRU (AMD) | live counter | killed (SIGILL) | observed on this host with the same setting; not documented in prctl(2) |
| vsyscall page `time()` | live time | returns -1 | the kernel applies the seccomp filter when emulating it; observed |
| RDPMC; `int 0x80` | already killed | killed | observed; the filter's architecture check |
| sleeps, timers, poll/select, getrusage, times, sysinfo, perf events, `/proc` | already EPERM | EPERM | seccomp allow-list |

After installing the filter the worker requires `os.open`, `fstat`, `time.time`, `time.monotonic`
and `clock_gettime` for IDs 0–11 to fail with EPERM, and otherwise does not start. Any failed step
is an evaluator error, never a run with a clock. A native instruction that traps kills the artifact
process (A-054: `class=Exception`).

Calls that hide the error return a constant or garbage instead of time: `localtime`, `gmtime` and
`asctime` give 31 Dec 1969; libc `time` gives -1; `process_time` falls back to glibc `times()` and
does not advance with work.

Tests: `WallClockTests` (7, in the pinned container) and `StaticClockRouteTests` (2). With the D-015
worker in place, six of the seven `WallClockTests` fail (the seventh is the allowed-modules check).

**Not closed** (also in [DEVIATIONS.md](DEVIATIONS.md)):
1. **Hardware.** RDTSC, RDTSCP and RDPRU were tested on one host (AMD EPYC 7763, Linux
   6.8.0-1070-azure, x86_64). TPAUSE and UMWAIT do not exist on it (SIGILL) and are untested where
   they do exist. Another CPU or kernel needs `WallClockTests` re-run, as does any unprivileged
   counter instruction not listed here.
2. **Native code.** `ctypes` stays in the worker's memory and executable pages can be mapped, so an
   artifact that escapes Python can run instructions. The clocks are denied at that level too, but
   only for the instructions tested.
3. **Startup remnants.** Interpreter startup reads clocks before confinement. A stale value may remain
   in the process's own memory. It would give an earlier instant, not the current time.
4. **Not clocks, but not constant:** process ID, memory addresses and uninitialised stack values
   (`times()`). `random.Random()` without a seed differs between runs. The pack prohibits it
   (File 30 L54), and no static rule here detects it.

[sandbox/harness.py](../sandbox/harness.py) runs inside each container (standard library
only). Each request runs one task:
- `factory`: restricted import of `driver.py`, `create_driver(0)`, return type, runtime
  signatures;
- `checker`: one null invocation of `check_trace`.

Evaluator-only tasks (no artifact code): `simulate`, `export`, `interface`, `yosys`, and
`icarus` (D-036 follow-up). `icarus` compiles one Verilog text with `iverilog -g2012 -s <top>`
and reports the exit code and messages. The compiled program is not run. It serves the mutant
check of `tools/check_control_file.py`.

It writes one framed result line to stdout. The artifact process has no access to that stdout
(`test_artifact_output_cannot_forge_result`). The harness directory is bind-mounted
read-only. Before every run the launcher refuses to start if any file in it is group- or
other-writable, or unreadable by the sandbox uid (`check_harness_permissions`). That guard
was added after new files in this checkout were found created with mode 646. Directory
ACLs (the `+` in `ls -l`) were not inspected: `getfacl` is not installed here.

## Simulation stage (Protocol §3.4 L166 (7)-(8); D-003)

Task `simulate` ([sandbox/sim.py](../sandbox/sim.py), [sandbox/sim_cocotb.py](../sandbox/sim_cocotb.py))
runs one driver on one target (`rtl` or `null`) in its own artifact container:
`iverilog -g2012` compiles the design sources, `vvp` runs them with cocotb's Icarus VPI
library, and the cocotb test module runs the cycle loop. The artifact runs in its own
confined process (D-015); `step` receives only a dict of strings, and the loop receives one
schema-checked plain value. `sim.py` watches a heartbeat
file and kills `vvp` when a `step` call exceeds the per-step watchdog (`WATCHDOG_TIMEOUT|phase=driver_step`).
The runner side is [src/openvef/simulation.py](../src/openvef/simulation.py): RTL run, then
null run, then the L166 (8) paired comparison.

Request fields (design materials; **all supplied by the caller, no defaults**):
`toplevel`, `verilog_sources`, `clock_port`, `input_ports` (name → width), `output_ports`,
`reset_sequence`, `cycle_cap`, `safe_idle`, `legal_input_predicate`, plus `seed`,
`step_timeout_s`, `budget_s`. Optional: `held_inputs` (name → bits), harness-owned inputs
such as a reset port. They are not driver-vector keys, are held after reset release, and
are recorded as consumed inputs (A-042).

`legal_input_predicate` is either:
- the test-only literal `ALL_INPUTS_LEGAL`;
- or a design-pack Python 3.11 function `{"language": "python3.11", "function": <name>,
  "source": <text>}`, called as `f(vector, sampled)`, where `sampled` is the outputs the
  driver was given in the same step (A-041). False gives
  `DRIVER_VECTOR_INVALID|reason=ILLEGAL_PROTOCOL_STATE`. An exception or a non-bool return
  is a design-materials error (ERROR), not a driver failure.

Anything else makes the result not determined (A-027, A-038), never a pass. For the FIFO,
[src/openvef/design_materials.py](../src/openvef/design_materials.py) takes the source
verbatim from the FIFO-042 code block of the specification.

Timeout (Protocol L334, A-043): `simulation.l334_timeout` makes three null-netlist runs
of the artifact (each capped at 120 s, a build default). T_timeout = max(5 × median wall
time, 2 s) is then the per-run budget and the per-step watchdog.

F18 wiring (D-005, provisional): when a response fixture passes the factory checks,
`runner/run_f18.py` calls [src/openvef/simulator_stages.py](../src/openvef/simulator_stages.py)
for L166 (7)–(11), on the DRAFT materials named by `design/fifo/design-materials-DRAFT.json`.
- At the start of the run, the null netlist is exported twice through the harness's
  `export` task (Yosys in an artifact container), and the two SHA-256 must agree.
- For each response: the L334 timeout, the RTL and null runs, the comparison under the
  primary mask, freezing of the null trace, then two checker invocations on the same
  bytes.
- The runner container mounts `design/` and `docs/` read-only.
- Every such result carries a `provisional` block in `results.jsonl`, and the summary
  lists them in `provisional_fixtures`.

Trace for the checker (DRAFT schema, item 11): [src/openvef/trace.py](../src/openvef/trace.py)
serializes the rows as UTF-8 JSON (sorted keys, no whitespace) and records the bytes'
SHA-256. Each checker invocation gets a value freshly decoded from those bytes.

**Build defaults for choices the pack leaves TO FREEZE** (Protocol L229 "Cycle cap,
safe-idle vectors and timeout formula are **TO FREEZE**"; L542 "Freeze driver API,
scheduler, alignment, same-row tie, cap, safe-idle and watchdog"). These are not
readings of the text. Each result records them under `scheduler`, and the owners must
freeze them:
- timescale 1ns/1ps;
- clock period 10 ns, starting low (first active edge at half a period);
- inputs driven at the falling edge before the next active edge (the pack says only "the
  designated drive phase before edge `n+1`", Protocol L219);
- (specified, not a default: outputs are sampled in Cocotb `ReadOnly` after the edge,
  L218);
- `reset_sequence[i]` is driven before active edge *i*, and the edge after the last
  vector is the reset-release edge.

Correction (23 Nov 2026): an earlier version of this list also called the sampling point a
build default. It is specified by the pack: "`outputs_after_edge_n`: top-level outputs
sampled in Cocotb `ReadOnly` after edge `n` settles" (Protocol L218), and the harness
follows it.

**Trace rows (Protocol §5.2 L216–L223; A-040).** Each row records:
- `cycle_index`;
- `reset`;
- `inputs_consumed_at_edge_n`, captured passively at the edge and checked against the
  prior row's scheduled vector;
- `outputs_after_edge_n`;
- `next_inputs_scheduled_for_edge_n_plus_1`;
- `driver_completed`.

Each trace also records `reset_release_cycle` and `run_status`
(`COMPLETE_TRACE`/`TRUNCATED_TRACE`). Four-state values are kept as `0`/`1`/`X`/`Z`. An
FST waveform is produced for every run and returned with its SHA-256. This closes the
gap recorded on 23 Nov 2026. Names the pack does not give are A-040 decisions
(pack-defects PD-23). In each result, `SCHEDULER` marks every entry as `specified` (with
its Protocol line) or `build_default`.

Tests: [tests/test_simulation.py](../tests/test_simulation.py) (22). They use
**test-only** toy designs in `tests/sim_designs/`, which are not a FIFO and not derived
from any owner material.

## Running the tests

```
.venv/bin/python -I tests/test_sandbox.py -v
.venv/bin/python -I tests/test_simulation.py -v
.venv/bin/python -I tests/test_broker.py -v
```

Docker must be available; without it the tests are reported as skipped, never as
passed. They run real containers with exactly the flags used for artifacts.

## Not covered here

- The simulator-backed stages need FIFO design materials (RTL, null netlist, port
  manifest, reset/legal-input rules, cycle cap, safe-idle vector, trace schema, mask)
  that are owner-written or still TO FREEZE; see docs/traceability.md.
- The resource limits and timeout values are this build's defaults, not frozen pack
  values.
- Development host: Docker 29.9.2 (not rootless), default AppArmor profile, built-in
  seccomp profile, cgroup v2. A different Docker setup needs the tests re-run before its
  results count.
