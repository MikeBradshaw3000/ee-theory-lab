"""gates/gate_b/reference.py — Lineage B pinned reference: verify, isolate, load.

Gate B Specification v0.4 (FROZEN 2026-09-04) §2: the reference is
`cycle3/wave_two/c3_w2_tcop.py` at commit 4d9a622; the harness reads the pinned bytes,
verifies the FROZEN expected digest, and hard-fails BEFORE any import or execution;
import is isolated (unique module name, no sys.path insertion, no sys.modules capture);
the harness never establishes identity from its own candidate file.

Verified bytes are the bytes executed (L2 review R1): both modes compile and execute the
`raw` object that was hashed — the path is never reopened after verification.

Two load modes, both digest-gated, both recorded in provenance:
  FULL       — verified bytes executed as a module (their own import-time preflight runs:
               active venv, py3.14, mesa, numpy 2.4.4, cwd at the pinned root). The ONLY
               mode AUTHORITATIVE accepts. Changes process cwd for the duration of the
               exec: Gate B is a serialized, single-process gate (deployment constraint of
               record, L2 O4).
  EXTRACTION — declared function/constant regions of the verified bytes executed without
               the module-level preflight (PROVISIONAL only; refused for AUTHORITATIVE).
               NOT a re-transcription: the source is the verified bytes at line ranges
               fixed here.
Every loader failure is a `ReferenceError` (fail-closed, named); no KeyError/AttributeError
escapes as an accidental verdict.
"""
from __future__ import annotations

import hashlib
import os
import subprocess
import sys
import types
import uuid
from dataclasses import dataclass
from typing import Any, Dict, Optional, Tuple

import numpy as np

PINNED_COMMIT = "4d9a622"
PINNED_RELPATH = os.path.join("cycle3", "wave_two", "c3_w2_tcop.py")
EXPECTED_SHA256 = "466455f20550b8c41a984ce40db49ebe0e832ae56c269ab518b521c6ad83b7e7"   # frozen §2
LOAD_MODES = ("FULL", "EXTRACTION")
LABELS = ("PROVISIONAL", "AUTHORITATIVE")
_EXTRACT_REGIONS = {                # 1-indexed inclusive; verified against the frozen digest
    "constants_L51": (51, 51), "constants_L67_74": (67, 74), "kappa_map_L77_83": (77, 83),
    "neighbor_L228_236": (228, 236), "sigmoid_L242_243": (242, 243),
    "u_t_for_L255_261": (255, 261), "step_L263_272": (263, 272),
}
REQUIRED_SYMBOLS = ("LAMBDA", "LOGIT_L", "KAPPA_MAP", "U_TIERS", "SEEDS",
                    "get_neighbor_count", "sigmoid", "u_t_for", "step_tcop_core")
FULL_EXTRA_SYMBOLS = ("execute_run",)


class ReferenceError(RuntimeError):
    """Fail-closed: raised before any execution of reference code, or on any loader defect."""


@dataclass(frozen=True)
class ReferenceProvenance:
    pinned_root: str                # os.path.realpath
    pinned_path: str                # os.path.realpath
    commit_verified: str
    worktree_dirty: bool            # WHOLE pinned worktree (git status --porcelain)
    source_file_dirty: bool         # the reference file specifically
    expected_sha256: str
    observed_sha256: str            # MEASURED over the executed bytes
    load_mode: str
    module_origin: str
    python_version: str
    numpy_version: str


@dataclass
class PinnedReference:
    ns: Dict[str, Any]
    provenance: ReferenceProvenance
    module: Optional[types.ModuleType] = None

    def __getattr__(self, name: str) -> Any:
        try:
            return self.ns[name]
        except KeyError:
            raise AttributeError(name) from None


def _git(root: str, *args: str) -> str:
    try:
        out = subprocess.run(["git", "-C", root, *args], capture_output=True, text=True)
    except OSError as e:
        raise ReferenceError(f"git unavailable at {root}: {e}") from e
    if out.returncode != 0:
        raise ReferenceError(f"git {' '.join(args)} failed at {root}: {out.stderr.strip() or out.returncode}")
    return out.stdout.strip()


def verify_pinned_source(pinned_root: str) -> Tuple[bytes, str, str, bool, bool, str]:
    """Read pinned bytes once; verify commit and FROZEN digest; hard-fail before any use.
    Returns (raw, realpath, commit, worktree_dirty, source_file_dirty, measured_digest)."""
    root = os.path.realpath(pinned_root)
    path = os.path.realpath(os.path.join(root, PINNED_RELPATH))
    if not os.path.isfile(path):
        raise ReferenceError(f"pinned reference absent: {path}")
    head = _git(root, "rev-parse", "--short=7", "HEAD")
    if head != PINNED_COMMIT:
        raise ReferenceError(f"pinned root HEAD is {head}, expected {PINNED_COMMIT}")
    worktree_dirty = bool(_git(root, "status", "--porcelain"))
    source_dirty = bool(_git(root, "status", "--porcelain", "--", PINNED_RELPATH))
    try:
        with open(path, "rb") as fh:
            raw = fh.read()
    except OSError as e:                               # every loader failure is a ReferenceError (L2 r2 item 3)
        raise ReferenceError(f"pinned reference unreadable: {path}: {type(e).__name__}: {e}") from e
    digest = hashlib.sha256(raw).hexdigest()
    if digest != EXPECTED_SHA256:
        raise ReferenceError(f"pinned reference digest FAILED: {path} has {digest}, expected {EXPECTED_SHA256}")
    return raw, path, head, worktree_dirty, source_dirty, digest


def exec_verified_bytes(raw: bytes, path: str, modname: str, cwd: Optional[str] = None) -> types.ModuleType:
    """Execute EXACTLY the verified byte object as an isolated module. The path is used for
    tracebacks and module metadata only; it is never reopened."""
    mod = types.ModuleType(modname)
    mod.__file__ = path
    mod.__package__ = ""
    code = compile(raw, path, "exec")
    prev = os.getcwd()
    try:
        if cwd is not None:
            os.chdir(cwd)
        exec(code, mod.__dict__)
    finally:
        os.chdir(prev)
    return mod


def _require(ns: Dict[str, Any], names: Tuple[str, ...], mode: str) -> None:
    missing = [k for k in names if k not in ns]
    if missing:
        raise ReferenceError(f"reference load incomplete ({mode}): missing symbols {missing}")


def load_pinned_reference(pinned_root: str, load_mode: str = "EXTRACTION",
                          label: str = "PROVISIONAL") -> PinnedReference:
    if load_mode not in LOAD_MODES:
        raise ReferenceError(f"unknown load_mode {load_mode!r}")
    if label not in LABELS:
        raise ReferenceError(f"unknown label {label!r}")
    if label == "AUTHORITATIVE" and load_mode != "FULL":
        raise ReferenceError("AUTHORITATIVE Gate B requires FULL module import of the verified "
                             "reference; EXTRACTION mode is PROVISIONAL-only")
    raw, path, head, wt_dirty, src_dirty, digest = verify_pinned_source(pinned_root)
    modname = f"gate_b_pinned_reference_{uuid.uuid4().hex}"
    for name in list(sys.modules):
        if name.startswith("gate_b_pinned_reference_") or name == "c3_w2_tcop":
            raise ReferenceError(f"pre-existing reference module in sys.modules: {name}")
    try:
        if load_mode == "FULL":
            mod = exec_verified_bytes(raw, path, modname, cwd=os.path.dirname(os.path.dirname(os.path.dirname(path))))
            full_ns = dict(vars(mod))
            _require(full_ns, REQUIRED_SYMBOLS + FULL_EXTRA_SYMBOLS, "FULL")
            ns = {k: full_ns[k] for k in REQUIRED_SYMBOLS + FULL_EXTRA_SYMBOLS}
            origin = f"module:{path}"
            module: Optional[types.ModuleType] = mod
        else:
            lines = raw.decode("utf-8").split("\n")
            src = "\n".join("\n".join(lines[a - 1:b]) for (a, b) in _EXTRACT_REGIONS.values()) + "\n"
            ex: Dict[str, Any] = {"np": np, "__name__": modname}
            exec(compile(src, f"<{modname}:extraction>", "exec"), ex)
            _require(ex, REQUIRED_SYMBOLS, "EXTRACTION")
            ns = {k: ex[k] for k in REQUIRED_SYMBOLS}
            origin = f"extraction:{path}:{','.join(f'{a}-{b}' for a, b in _EXTRACT_REGIONS.values())}"
            module = None
    except ReferenceError:
        raise
    except Exception as e:                      # any import-time failure is a named loader failure
        raise ReferenceError(f"reference execution failed ({load_mode}): {type(e).__name__}: {e}") from e
    prov = ReferenceProvenance(pinned_root=os.path.realpath(pinned_root), pinned_path=path,
                               commit_verified=head, worktree_dirty=wt_dirty, source_file_dirty=src_dirty,
                               expected_sha256=EXPECTED_SHA256, observed_sha256=digest,
                               load_mode=load_mode, module_origin=origin,
                               python_version=sys.version.split()[0], numpy_version=np.__version__)
    return PinnedReference(ns=ns, provenance=prov, module=module)
