"""Reference computation for F9_MASTER_RULING_RECORD: a stage's master from the commit its authorization sits on and the
value Mike generates at authorization. Usage: python f9_master_rule_reference.py /path/to/instrument
It imports the placed stream module only for its three constants (retired list, test limit, master limit) and prints
test vectors. The commits and values used below are made up, so that nothing printed here can be a master of record."""
import hashlib, sys
sys.path.insert(0, sys.argv[1])
from mfa_instrument.f9 import config as C, streams as ST

STAGES = ("benchmark", "calibration", "design", "held_out", "canonical", "stability")     # contract §8 steps 10, 4, 7, 8, 11-13, 14
N_MAX = 15                                                                                 # candidates n = 0 .. 15, then the derivation fails
HEX = set("0123456789abcdef")


class NoAdmissibleMaster(Exception):
    pass


def candidate(stage: str, base_commit: str, value: str, n: int) -> int:
    text = f"ee-theory-lab|flight9|{C.F9_VERSION}|master|{stage}|{base_commit}|{value}|{n}"
    return int.from_bytes(hashlib.sha256(text.encode("ascii")).digest()[:8], "big")


def master(stage: str, base_commit: str, value: str, registered=()):
    """(master, n): the first admissible candidate for n = 0 .. N_MAX. `registered` is every Flight 9 master in an
    authorization that is an ancestor of the base commit."""
    if stage not in STAGES: raise ValueError("not a stage")
    if len(base_commit) != 40 or not set(base_commit) <= HEX: raise ValueError("base commit: 40 lower-case hex characters")
    if len(value) != 64 or not set(value) <= HEX: raise ValueError("value: 64 lower-case hex characters (32 bytes)")
    for n in range(N_MAX + 1):
        m = candidate(stage, base_commit, value, n)
        if ST.TEST_MASTER_LIMIT <= m < ST.MASTER_LIMIT and m not in ST.RETIRED_MASTERS and m not in registered:
            return m, n
    raise NoAdmissibleMaster(stage)


if __name__ == "__main__":
    print("version", C.F9_VERSION, "| retired", len(ST.RETIRED_MASTERS), "| test limit", ST.TEST_MASTER_LIMIT, "| master limit 2^64:", ST.MASTER_LIMIT == 2 ** 64)
    zero, ramp = "0" * 40, "0123456789abcdef0123456789abcdef01234567"
    v0, v1 = "0" * 64, "f" * 64
    for base, value in ((zero, v0), (zero, v1), (ramp, v0)):
        registered = []
        for s in STAGES:
            m, n = master(s, base, value, registered)
            assert ST.master_class(m) == "stage"
            registered.append(m)
            print(f"base={base} value={value[:4]}..{value[-4:]} {s:<11} n={n} master={m}")
    # the same commit with a different value gives a different master: the commit alone does not determine it
    assert master("design", zero, v0)[0] != master("design", zero, v1)[0]
    # a different commit with the same value gives a different master
    assert master("design", zero, v0)[0] != master("design", ramp, v0)[0]
    # the retry: with the n = 0 value already registered, the next candidate is taken
    m0, _ = master("design", zero, v0)
    m1, n1 = master("design", zero, v0, registered=(m0,))
    assert n1 == 1 and m1 == candidate("design", zero, v0, 1) and m1 != m0
    print("retry: with the n=0 value already registered, design on the zero commit and zero value gives n=%d master=%d" % (n1, m1))
    # the terminal failure: all sixteen candidates registered
    taken = tuple(candidate("design", zero, v0, n) for n in range(N_MAX + 1))
    try: master("design", zero, v0, registered=taken); raise SystemExit("no failure")
    except NoAdmissibleMaster: print("terminal failure: with all 16 candidates registered the derivation refuses")
    for bad in (("design", zero[:39], v0), ("design", zero.upper().replace("0", "A"), v0), ("design", zero, v0[:63]), ("pricing", zero, v0)):
        try: master(*bad); raise SystemExit("accepted a malformed input")
        except ValueError: pass
    print("malformed inputs refused: 4 of 4")
    print("chance that one candidate is below the test limit: 10^6 / 2^64 = %.2e" % (1e6 / 2 ** 64))
