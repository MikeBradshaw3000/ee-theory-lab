"""NONCANONICAL design evidence. For all 12,000 committed sweeps (ideal-M2/M3 replay rows): does the
measured bracket depend on router resolution, and how does measured post-pass-2 band width relate to
the generator's declared mixing width w?"""
import sys, json, statistics as st
rows = json.load(open(sys.argv[1]))
LV1 = [150000,180435,210870,241304,271739,302174,332609,363043,393478,423913,454348,484783,515217,545652,576087,606522,636957,667391,697826,728261,758696,789130,819565,850000]
def band(lab, lv):
    n=[i for i,c in enumerate(lab) if c=="N"]; s=[i for i,c in enumerate(lab) if c=="S"]
    return (lv[max(n)], lv[min(s)]) if n and s and max(n)<min(s) else None
widen = 0; both = 0
for r in rows:
    b1=band(r["p1"],LV1); b2=band(r["lf"],r["lv"])
    if b1 and b2:
        both += 1; widen += (b2[1]-b2[0]) > (b1[1]-b1[0])
print(f"sweeps with a band at both passes: {both}; pass-2 band wider than pass-1 band: {widen}")
print(f"{'class':28} {'n':>5} {'measured/declared width: p5':>28} {'median':>7} {'p95':>6}")
for cls in ("gentle_onset","off_band_mixture","wide_mixed_boundary","unresolved_heavy_boundary","abrupt_onset","persistent_nonstationary_high_m","nonmonotone_amplitude"):
    ratio=sorted((b[1]-b[0])/r["w"] for r in rows if r["cls"]==cls and r["w"]>0 and (b:=band(r["lf"],r["lv"])))
    q=lambda p: ratio[int(p*(len(ratio)-1))]
    print(f"{cls:28} {len(ratio):5} {q(.05):28.2f} {q(.5):7.2f} {q(.95):6.2f}")
