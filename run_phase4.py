# -*- coding: utf-8 -*-
"""Phase 4 — Bivariate associations between predictors and the 3 outcomes."""
import pickle, math
import statlib as S
from collections import Counter

recs, info, med_ss = pickle.load(open("recs2.pkl", "rb"))
OUT = []
def w(x=""): OUT.append(str(x))
from analysis import fmtp, star

def pairs(pk, ok):
    return [(r[pk], r[ok]) for r in recs if r.get(pk) is not None and r.get(ok) is not None]

def chi_presence(pk):
    pr = pairs(pk, 'GI_presence')
    levels = sorted(set(p[0] for p in pr))
    table = [[sum(1 for p in pr if p[0]==lv and p[1]==o) for o in (0,1)] for lv in levels]
    res = S.chi2_independence(table)
    extra = ""
    if len(levels)==2:
        fe = S.fisher_exact_2x2(table)
        extra = f"; Fisher p={fmtp(fe['p'])}"
    return f"chi2({res['df']})={res['chi2']:.2f}, p={fmtp(res['p'])}{star(res['p'])}{extra} [min E={res['min_expected']:.1f}, {res['pct_cells_low']:.0f}% cells E<5; n={res['N']}]"

def mwu_out(pk, ok):
    pr = pairs(pk, ok)
    g = {}
    for lv, ov in pr: g.setdefault(lv, []).append(ov)
    ks = sorted(g.keys())
    if len(ks)!=2: return "n/a (not 2 groups)"
    res = S.mannwhitney_u(g[ks[0]], g[ks[1]])
    return (f"U={res['U']:.0f}, z={res['z']:.2f}, p={fmtp(res['p'])}{star(res['p'])} "
            f"[med {ks[0]}={res['median_a']:.1f} (n={res['n_a']}) vs {ks[1]}={res['median_b']:.1f} (n={res['n_b']})]")

def kw_out(pk, ok):
    pr = pairs(pk, ok)
    g = {}
    for lv, ov in pr: g.setdefault(lv, []).append(ov)
    ks = sorted(g.keys())
    groups = [g[k] for k in ks]
    res = S.kruskal_wallis(groups)
    return f"H({res['df']})={res['H']:.2f}, p={fmtp(res['p'])}{star(res['p'])} [k={len(ks)} groups, n={sum(len(x) for x in groups)}]"

def spear(pk, ok):
    pr = pairs(pk, ok)
    x=[p[0] for p in pr]; y=[p[1] for p in pr]
    res = S.spearman_r(x, y)
    return f"rho={res['rho']:.3f}, p={fmtp(res['p'])}{star(res['p'])} (n={res['n']})"

w("="*78); w("PHASE 4 — BIVARIATE ASSOCIATIONS"); w("="*78)
w("Outcomes: GI_presence (binary), GI_severity (continuous, NON-NORMAL -> non-parametric),")
w("          symptom_increase (ordinal 1-4). Significance: * p<.05, ** p<.01, *** p<.001")

# predictor metadata: (label, key, type)  type in {nom2, ord, nommulti, cont}
PREDS = [
    ("Gender (M vs F)", "gender_male", "nom2"),
    ("Age group", "age_rank", "ord"),
    ("College", "college", "nommulti"),
    ("Academic year", "year_rank", "ord"),
    ("Chronic GI disease", "chronic_GI", "nom2"),
    ("Sleep hours (rank)", "sleep_rank", "ord"),
    ("Caffeine intake (rank)", "caffeine_rank", "ord"),
    ("Eating habit change (rank)", "eating_rank", "ord"),
    ("Stress level (High/Low)", "stress_level", "nom2"),
    ("Stress score (continuous)", "stress_score", "cont"),
]

for lab, key, typ in PREDS:
    w("\n" + "-"*70)
    w(f"PREDICTOR: {lab}   [type: {typ}]")
    # GI_presence
    if typ in ("nom2", "ord", "nommulti"):
        w(f"  vs GI_presence    : {chi_presence(key)}")
    else:  # continuous -> MWU split by presence
        pr = pairs(key, 'GI_presence')
        g={}
        for v,o in pr: g.setdefault(o,[]).append(v)
        res=S.mannwhitney_u(g[0],g[1])
        w(f"  vs GI_presence    : Mann-Whitney U (predictor split by presence) U={res['U']:.0f}, "
          f"z={res['z']:.2f}, p={fmtp(res['p'])}{star(res['p'])} "
          f"[med No={res['median_a']:.1f} (n={res['n_a']}) vs Yes={res['median_b']:.1f} (n={res['n_b']})]")
    # GI_severity
    if typ == "nom2":
        w(f"  vs GI_severity    : Mann-Whitney U: {mwu_out(key,'GI_severity')}")
    elif typ == "nommulti":
        w(f"  vs GI_severity    : Kruskal-Wallis: {kw_out(key,'GI_severity')}")
    elif typ == "ord":
        w(f"  vs GI_severity    : Spearman {spear(key,'GI_severity')}; KW {kw_out(key,'GI_severity')}")
    else:
        w(f"  vs GI_severity    : Spearman {spear(key,'GI_severity')}")
    # symptom_increase
    if typ == "nom2":
        w(f"  vs symptom_increase: Mann-Whitney U: {mwu_out(key,'symptom_increase')}")
    elif typ == "nommulti":
        w(f"  vs symptom_increase: Kruskal-Wallis: {kw_out(key,'symptom_increase')}")
    elif typ == "ord":
        w(f"  vs symptom_increase: Spearman {spear(key,'symptom_increase')}; KW {kw_out(key,'symptom_increase')}")
    else:
        w(f"  vs symptom_increase: Spearman {spear(key,'symptom_increase')}")

txt = "\n".join(OUT)
open("results_p4.txt","w").write(txt)
print(txt)
