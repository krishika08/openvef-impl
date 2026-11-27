"""Run the full unit-test suite inside the pinned container and save the evidence (D-017).

    python3 tools/run_container_tests.py

The tests run in the D-002a image as the runner does: no network, read-only root, no capabilities,
non-root, the repository mounted read-only. Tests that start artifact containers call `docker`,
which inside is tools/container_tests/docker. It forwards to the broker in this file; the Docker
socket is NOT mounted. The broker accepts only: `docker run` with exactly the flags of
runner/artifact-container.args, a name openvef-<12 hex> and the pinned image tag; `docker kill`
and `docker rm -f` of such a name; `docker image inspect` of the tag; and one fixed `docker ps`.
Anything else is refused and recorded. Host Python only brokers and records; no result is computed
here. Output: evidence/container-tests-<UTC>/ (or $OPENVEF_EVIDENCE_ROOT).
"""
from __future__ import annotations

import base64
import datetime as dt
import hashlib
import json
import os
import re
import select
import shutil
import socket
import subprocess
import sys
import tempfile
import threading
import time
import uuid
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "src"))
from openvef import sandbox  # noqa: E402

NAME = re.compile(r"openvef-[0-9a-f]{12}")
PS = ["ps", "-a", "--filter", "name=openvef-", "--format", "{{.Names}}"]
HASHED = ("src", "runner", "sandbox", "tests", "tools", "design", "requirements.lock", "requirements.in")


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def out_of(*argv: str) -> str:
    return subprocess.run(argv, check=True, capture_output=True, text=True).stdout.strip()


def allowed(argv: list, tag: str) -> bool:
    if argv == PS or argv == ["image", "inspect", tag, "--format", "{{.Id}}"]:
        return True
    if len(argv) == 2 and argv[0] == "kill" or len(argv) == 3 and argv[:2] == ["rm", "-f"]:
        return bool(NAME.fullmatch(argv[-1]))
    names = [a[len("--name="):] for a in argv if a.startswith("--name=")]
    if argv[:1] != ["run"] or not names or not NAME.fullmatch(names[0]):
        return False
    prefix = ["run", *sandbox.artifact_flags(names[0]), tag]
    return argv[:len(prefix)] == prefix and len(argv) > len(prefix)


class Broker:
    def __init__(self, path: str, tag: str, log: Path):
        self.tag, self.log, self.refused, self.count, self.lock = tag, open(log, "w"), 0, 0, threading.Lock()
        self.sock = socket.socket(socket.AF_UNIX)
        self.sock.bind(path)
        self.sock.listen(16)
        threading.Thread(target=self.serve, daemon=True).start()

    def serve(self):
        while True:
            conn, _ = self.sock.accept()
            threading.Thread(target=self.handle, args=(conn,), daemon=True).start()

    def handle(self, conn):
        t = time.monotonic()
        request = json.loads(conn.makefile("rb").readline())
        argv, stdin = request["argv"], base64.b64decode(request["stdin"])
        rc, out, err, gone = 125, b"", b"refused by the test broker\n", False
        if allowed(argv, self.tag):
            with tempfile.TemporaryFile() as fin, tempfile.TemporaryFile() as fout, tempfile.TemporaryFile() as ferr:
                fin.write(stdin)
                fin.seek(0)
                p = subprocess.Popen(["docker", *argv], stdin=fin, stdout=fout, stderr=ferr)
                while p.poll() is None:  # the client going away kills the docker CLI, as a direct call would
                    if not gone and select.select([conn], [], [], 0.02)[0] and not conn.recv(1):
                        gone = True
                        p.kill()
                    elif gone:
                        time.sleep(0.02)
                rc = p.returncode
                fout.seek(0), ferr.seek(0)
                out, err = fout.read(), ferr.read()
        else:
            self.refused += 1
        with self.lock:
            self.count += 1
            self.log.write(json.dumps({"argv": ["docker", *argv], "stdin_sha256": sha(stdin), "stdin_bytes": len(stdin),
                                       "returncode": rc, "stdout_sha256": sha(out), "client_gone": gone,
                                       "seconds": round(time.monotonic() - t, 3)}) + "\n")
            self.log.flush()
        try:
            conn.sendall(json.dumps({"rc": rc & 0xFF, "out": base64.b64encode(out).decode(),
                                     "err": base64.b64encode(err).decode()}).encode() + b"\n")
        except OSError:
            pass
        conn.close()


def main() -> int:
    dirty = out_of("git", "-C", str(REPO), "status", "--porcelain")
    tag = sandbox.image_tag()
    # D-028: the tag must resolve to the pinned image ID; the guard loads the saved tarball if not.
    guard = subprocess.run([str(REPO / "tools" / "ensure_pinned_image.sh"), tag], capture_output=True, text=True)
    if guard.returncode != 0:
        sys.exit(f"pinned-image guard failed: {guard.stderr.strip()}")
    sandbox.check_harness_permissions()
    image = json.loads(out_of("docker", "image", "inspect", tag))[0]
    started = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out = Path(os.environ.get("OPENVEF_EVIDENCE_ROOT", REPO / "evidence")) / f"container-tests-{started}"
    out.mkdir()
    (out / "image-guard.txt").write_text(guard.stdout, encoding="utf-8")
    sockdir = tempfile.mkdtemp(prefix="ovf-broker-")
    broker = Broker(f"{sockdir}/sock", tag, out / "docker-commands.jsonl")
    # Not "openvef-*": a test requires that no such container is left running.
    name = f"ovf-container-tests-{uuid.uuid4().hex[:8]}"
    command = ["docker", "run", "--rm", "--network=none", "--read-only", "--cap-drop=ALL",
               "--security-opt=no-new-privileges", f"--user={os.getuid()}:{os.getgid()}",
               "--tmpfs=/tmp:rw,noexec,nosuid,nodev,size=64m,mode=1777", "--pids-limit=128", "--memory=1g",
               "--memory-swap=1g", "--cpus=2", "--ipc=none", "--hostname=tests", "--env=PYTHONHASHSEED=0",
               "--env=PYTHONDONTWRITEBYTECODE=1", "--env=PYTHONUNBUFFERED=1",
               "--env=PATH=/shim:/usr/local/bin:/usr/bin:/bin", f"--volume={REPO}:{REPO}:ro",
               f"--volume={REPO}/tools/container_tests:/shim:ro", f"--volume={sockdir}:/broker",
               f"--volume={out}:/evidence:rw", "--workdir=/tmp", f"--name={name}", tag,
               "python", "-I", "/shim/inner.py", str(REPO), "/evidence"]
    with open(out / "run.log", "wb") as log:
        rc = subprocess.run(command, stdin=subprocess.DEVNULL, stdout=log, stderr=subprocess.STDOUT).returncode
    shutil.rmtree(sockdir)
    broker.log.close()
    tracked = out_of("git", "-C", str(REPO), "ls-files", "--", *HASHED).splitlines()
    files = json.loads((out / "files.json").read_text())
    env = json.loads((out / "environment.json").read_text())
    summary = {
        "what": "Full unit-test suite inside the pinned container (D-017). Not an F18 run: no fixture status comes from it.",
        "started_utc": started, "finished_utc": dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ"),
        "git_commit": out_of("git", "-C", str(REPO), "rev-parse", "HEAD") + ("+UNCOMMITTED_CHANGES" if dirty else ""),
        "command": command, "host_command": [sys.executable, *sys.argv], "returncode": rc,
        "image": {"tag": tag, "id": image["Id"], "repo_digests": image["RepoDigests"], "base": sandbox.BASE_IMAGE_DIGEST,
                  "dockerfile_sha256": sha((REPO / "sandbox/Dockerfile").read_bytes()),
                  "requirements_lock_sha256": sha((REPO / "requirements.lock").read_bytes())},
        "interpreter": {"version": env["python_version"], "sha256": env["python_executable_sha256"]},
        "docker_server": out_of("docker", "version", "--format", "{{.Server.Version}}"),
        "host_kernel": " ".join(os.uname()[:1] + os.uname()[2:3]),
        "totals": files["totals"], "test_files": len(files["files"]),
        "docker_commands": broker.count, "docker_commands_refused": broker.refused,
        "source_sha256": {n: sha((REPO / n).read_bytes()) for n in tracked}}
    (out / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    names = sorted(str(p.relative_to(out)) for p in out.rglob("*") if p.is_file())
    (out / "SHA256SUMS").write_text("".join(f"{sha((out / n).read_bytes())}  {n}\n" for n in names))
    subprocess.run(["chmod", "-R", "go-w", str(out)], check=True)
    print(json.dumps({k: summary[k] for k in ("git_commit", "returncode", "totals", "test_files", "docker_commands",
                                              "docker_commands_refused")}, indent=2))
    print(out)
    return rc


if __name__ == "__main__":
    sys.exit(main())
