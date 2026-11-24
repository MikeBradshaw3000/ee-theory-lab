"""Reverse the packet's exact diff from repaired ZIP bytes; verify all five pins.

Usage: python3 reconstruct_from_archive.py ARCHIVE.zip OUTPUT_DIRECTORY
The before/ copies are used only after every reconstruction has been written.
"""
import hashlib
import json
from pathlib import Path
import re
import sys
import zipfile

EXPECTED_ARCHIVE = "e82a62ed1dacd0d79cfbf72a9f866ae38002791d53d1220253f094e97dcf37f9"
DIFF = "flights/mfa_fidelity/build_records/f9_evaluator_precedence_repair_2026-11-23.diff"
BASE = "flights/mfa_fidelity/instrument/"
FILES = {
    BASE + "mfa_instrument/f9/evaluator.py":
        "73197bfb6dee6fce72dd4f3a7b296c6bc8690dae4a5da3bc442e40668c833acc",
    BASE + "tests/test_f9_m3.py":
        "b09f3026c2a2af4da941f8c3c27df9a366d72d45e2d1c7c0f5978d10ece04aa6",
    BASE + "tests/test_f9_m4.py":
        "ed487a29067084cc6ff21e6e04f5b5bd5be6f527a44429c7dafd7095f061c63b",
    BASE + "tests/test_f9_m5.py":
        "bf8e7989f756c76deb10deb76ebfc05e05ff3f727785c9251114a82174f312d8",
    BASE + "tests/test_f9_m6.py":
        "74a2a8a6d818aa92f9d66a9b543f21a319c1068e14f07f00c19085594d472c56",
}

def sha(data):
    return hashlib.sha256(data).hexdigest()

archive, out = Path(sys.argv[1]), Path(sys.argv[2])
assert sha(archive.read_bytes()) == EXPECTED_ARCHIVE
out.mkdir(parents=True, exist_ok=True)
with zipfile.ZipFile(archive) as z:
    manifest = {}
    for line in z.read("MANIFEST.txt").decode().splitlines():
        if not line.strip():
            continue
        digest, name = line.split(maxsplit=1)
        assert re.fullmatch("[0-9a-f]{64}", digest)
        assert name not in manifest
        manifest[name] = digest
    assert len(manifest) == 85
    # Hashing before/ for receipt does not use it to construct any source.
    for name, digest in manifest.items():
        assert sha(z.read(name)) == digest, name

    sections = re.split(rb"(?=^diff --git )", z.read(DIFF), flags=re.M)
    sections = [s for s in sections if s]
    assert len(sections) == 5
    restored, repaired = {}, {}
    for section in sections:
        lines = section.splitlines(keepends=True)
        header = re.fullmatch(rb"diff --git a/(.+) b/(.+)\n", lines[0])
        assert header and header[1] == header[2]
        name = header[1].decode()
        assert name in FILES and name not in restored
        current = z.read(name)
        source = current.splitlines(keepends=True)
        result, cursor, i = [], 0, 1
        while i < len(lines):
            if not lines[i].startswith(b"@@ "):
                i += 1
                continue
            h = re.match(rb"@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@", lines[i])
            assert h
            old_at, old_n = int(h[1]) - 1, int(h[2] or b"1")
            new_at, new_n = int(h[3]) - 1, int(h[4] or b"1")
            old, new = [], []
            i += 1
            while i < len(lines) and not lines[i].startswith(b"@@ "):
                prefix, data = lines[i][:1], lines[i][1:]
                assert prefix in (b" ", b"+", b"-"), (name, lines[i])
                if prefix in (b" ", b"-"):
                    old.append(data)
                if prefix in (b" ", b"+"):
                    new.append(data)
                i += 1
            assert len(old) == old_n and len(new) == new_n
            assert new_at >= cursor
            assert source[new_at:new_at + new_n] == new, name
            result.extend(source[cursor:new_at])
            assert len(result) == old_at
            result.extend(old)
            cursor = new_at + new_n
        result.extend(source[cursor:])
        prior = b"".join(result)
        assert sha(prior) == FILES[name], name
        repaired[name], restored[name] = current, prior
        (out / Path(name).name).write_bytes(prior)

    assert set(restored) == set(FILES)
    rows = []
    # Only now compare reconstructed sources with the packet's before/ copies.
    for name, expected in FILES.items():
        prior = restored[name]
        before = z.read("packet_only/before/" + Path(name).name)
        assert prior == before
        assert sha(prior) == sha(before) == expected
        rows.append({
            "file": name,
            "repaired_sha256": sha(repaired[name]),
            "reconstructed_sha256": sha(prior),
            "before_sha256": sha(before),
            "byte_equal": prior == before,
        })
result = {"archive_sha256": EXPECTED_ARCHIVE, "reconstructions": rows}
(out / "results.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
