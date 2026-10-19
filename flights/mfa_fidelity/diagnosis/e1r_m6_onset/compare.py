import json, sys, glob, os, collections
S = sys.argv[1]
pred = json.load(open(f"{S}/predicted_rows.json"))
tot = collections.Counter()
for f in sorted(glob.glob(f"{S}/realized_*.jsonl")):
    cls = os.path.basename(f)[9:-6]
    P = {r["sweep"]: r for r in pred[f"design:{cls}"]}
    n = m_p1 = m_fin = m_verdict = m_rule = 0; diffs = []
    for line in open(f):
        r = json.loads(line); p = P[r["sweep_index"]]; n += 1
        p1 = "".join(r["pass1_labels"]); fin = "".join(r["final_labels"])
        m_p1 += p1 == p["p1"]; m_fin += fin == p["final"]; m_verdict += r["final_verdict"] == p["f_verdict"]; m_rule += r["final_rule"] == p["f_rule"]
        if fin != p["final"]: diffs.append((r["sweep_index"], p1, p["p1"], fin, p["final"], r["final_verdict"], p["f_verdict"]))
    print(f"{cls:34} n={n:2} pass1_labels_match={m_p1} final_labels_match={m_fin} verdict_match={m_verdict} rule_match={m_rule}")
    for d in diffs: print("   diff sweep", d[0], "\n     p1 real", d[1], "\n     p1 pred", d[2], "\n     fin real", d[3], "\n     fin pred", d[4], d[5], d[6])
    tot["n"] += n; tot["verdict"] += m_verdict; tot["labels"] += m_fin
print("TOTAL", dict(tot))
