"""gates/gate_b/environment.py — the full frozen environment check (Gate B v0.4 §6; Merge
Specification v0.4 FROZEN §7.4). The citable pin source is `cycle3/requirements.lock.txt`
at the pinned commit 4d9a622 (BOM-prefixed; twenty packages).

Pin-source identity is bound BEFORE any pin is compared (L2 round-2 item 4): the lock
bytes are read as the git blob at the pinned commit (`git show 4d9a622:<path>`), never from
the mutable worktree copy, and verified against the FROZEN full digest. The worktree copy
is checked only as a mirror and reported separately. A mismatch or any read/decode/parse
defect is an `EnvironmentCheckError` (fail-closed, named) before installed-package
comparison. AUTHORITATIVE requires an active venv, Python 3.14.x, and every pin installed
at the pinned version; PROVISIONAL records the same result without refusing."""
from __future__ import annotations

import hashlib
import os
import platform
import subprocess
import sys
from dataclasses import dataclass, field
from importlib import metadata
from typing import Dict, List, Optional, Tuple

LOCK_RELPATH = os.path.join("cycle3", "requirements.lock.txt")
LOCK_GIT_PATH = "cycle3/requirements.lock.txt"
PINNED_COMMIT = "4d9a622"
# Frozen: sha256 of the lock-file blob at 4d9a622 (established from the git object, 2026-09-11).
EXPECTED_LOCK_SHA256 = "c10e02c5db497570ffeb45dc92857fcc633cb38364858a35458096950d02de7c"
EXPECTED_PIN_COUNT = 20
FROZEN_PYTHON_PREFIX = "3.14."


class EnvironmentCheckError(RuntimeError):
    """Fail-closed: the frozen pin source could not be bound, read, decoded, or parsed."""


@dataclass(frozen=True)
class EnvironmentRecord:
    python_version: str
    python_build: Tuple[str, str]
    python_implementation: str
    platform: str
    venv_active: bool
    python_conforms: bool
    lock_sha256: str                                  # measured over the git blob at 4d9a622
    lock_worktree_mirror_matches: Optional[bool]      # worktree copy == blob (None if absent)
    pins: Dict[str, Tuple[str, Optional[str], bool]]  # name -> (pinned, installed, ok)
    conforms: bool
    failures: List[str] = field(default_factory=list)

    def summary(self) -> str:
        ok = sum(1 for v in self.pins.values() if v[2])
        return (f"python{self.python_version} [{self.python_implementation} {self.python_build[0]}] "
                f"{self.platform} venv={self.venv_active} pins_ok={ok}/{len(self.pins)} conforms={self.conforms}")


def read_lock_pins(pinned_root: str) -> Tuple[Dict[str, str], str, Optional[bool]]:
    """Read the lock blob from the pinned commit via git, verify the frozen digest, parse.
    Returns (pins, measured_blob_digest, worktree_mirror_matches)."""
    root = os.path.realpath(pinned_root)
    try:
        out = subprocess.run(["git", "-C", root, "show", f"{PINNED_COMMIT}:{LOCK_GIT_PATH}"],
                             capture_output=True)
    except OSError as e:
        raise EnvironmentCheckError(f"git unavailable at {root}: {e}") from e
    if out.returncode != 0:
        raise EnvironmentCheckError(f"frozen lock blob {PINNED_COMMIT}:{LOCK_GIT_PATH} unreadable at {root}: "
                                    f"{out.stderr.decode(errors='replace').strip() or out.returncode}")
    raw = out.stdout
    digest = hashlib.sha256(raw).hexdigest()
    if digest != EXPECTED_LOCK_SHA256:
        raise EnvironmentCheckError(f"frozen lock blob digest FAILED: {digest} != {EXPECTED_LOCK_SHA256}")
    try:
        text = raw.decode("utf-8-sig")                # BOM-tolerant (spec §7.4 recorded finding)
    except UnicodeDecodeError as e:
        raise EnvironmentCheckError(f"frozen lock blob not UTF-8: {e}") from e
    pins: Dict[str, str] = {}
    for line in text.splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        if "==" not in s:
            raise EnvironmentCheckError(f"unparseable pin line: {s!r}")
        name, ver = s.split("==", 1)
        name, ver = name.strip(), ver.strip()
        if not name or not ver:
            raise EnvironmentCheckError(f"malformed pin line: {s!r}")
        if name in pins:
            raise EnvironmentCheckError(f"duplicate pin: {name}")
        pins[name] = ver
    if len(pins) != EXPECTED_PIN_COUNT:
        raise EnvironmentCheckError(f"lock blob carries {len(pins)} pins; the frozen set is {EXPECTED_PIN_COUNT}")
    mirror: Optional[bool] = None
    wt = os.path.join(root, LOCK_RELPATH)
    if os.path.isfile(wt):
        try:
            mirror = open(wt, "rb").read() == raw
        except OSError:
            mirror = False
    return pins, digest, mirror


def _installed(name: str) -> Optional[str]:
    for cand in (name, name.lower(), name.replace("_", "-"), name.lower().replace("_", "-")):
        try:
            return metadata.version(cand)
        except metadata.PackageNotFoundError:
            continue
    return None


def check_environment(pinned_root: str) -> EnvironmentRecord:
    pins, lock_digest, mirror = read_lock_pins(pinned_root)
    venv = sys.prefix != sys.base_prefix
    pyv = platform.python_version()
    py_ok = pyv.startswith(FROZEN_PYTHON_PREFIX)
    results: Dict[str, Tuple[str, Optional[str], bool]] = {}
    failures: List[str] = []
    if not venv:
        failures.append("venv not active")
    if not py_ok:
        failures.append(f"python {pyv} != {FROZEN_PYTHON_PREFIX}x")
    for name, pinned in pins.items():
        inst = _installed(name)
        ok = inst == pinned
        results[name] = (pinned, inst, ok)
        if not ok:
            failures.append(f"{name}: pinned {pinned}, installed {inst}")
    return EnvironmentRecord(python_version=pyv, python_build=platform.python_build(),
                             python_implementation=platform.python_implementation(),
                             platform=platform.platform(), venv_active=venv, python_conforms=py_ok,
                             lock_sha256=lock_digest, lock_worktree_mirror_matches=mirror, pins=results,
                             conforms=(venv and py_ok and all(v[2] for v in results.values())),
                             failures=failures)
