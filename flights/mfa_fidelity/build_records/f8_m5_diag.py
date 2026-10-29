"""F8 M5 placement diagnostic: how far do this machine's fixed-point tables sit from the committed Appendix A?"""
import json, os, re, sys, platform, math
sys.path.insert(0, os.getcwd())
from mfa_instrument.f8 import closure as CL, config as C

root = os.environ.get("MFA_PINNED_REPO_ROOT") or os.path.abspath(os.path.join(os.getcwd(), "..", "..", ".."))
path = os.path.join(root, "flights", "mfa_fidelity", "contracts", "flight8", "APPENDIX_A_OF_RECORD.md")
raw = open(path, "rb").read()
j = json.loads(re.search(r"```json\n(.*?)```", raw.decode("utf-8"), re.S).group(1))
sk, re_ = CL.tables()
dm = CL.delta_m()
print("platform:", platform.platform(), "python:", sys.version.split()[0])
print("exp(-0.2) repr:", repr(math.exp(-0.2)), " exp(-0.01) repr:", repr(math.exp(-0.01)))
for name, mine, theirs in (("rho_sk", sk, j["rho_sk"]), ("rho_re", re_, j["rho_re"])):
    diffs = {k: mine[k] - float(theirs[k]) for k in theirs}
    worst = max(diffs, key=lambda k: abs(diffs[k]))
    nz = sum(1 for v in diffs.values() if v != 0.0)
    print(f"{name}: {nz}/24 levels differ; max |diff| = {abs(diffs[worst]):.3e} at m={worst} (mine {mine[worst]!r}, A {theirs[worst]})")
jd = j["delta_m"]
print("delta_m lower/upper/s/value equal:", [float(jd[k]) == getattr(dm, k) for k in ("lower", "upper", "s", "value")], " mine:", dm.value, " A:", jd["value"])
print("m_infl equal:", float(j["m_infl"]) == CL.m_infl(), CL.m_infl(), " m_lat equal:", float(j["m_lat"]) == CL.m_lat(), repr(CL.m_lat()), j["m_lat"])
