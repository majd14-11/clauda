# -*- coding: utf-8 -*-
"""Phase 5 — Regression models (binary logistic, multiple linear, ordinal logistic)."""
import pickle, math
import statlib as S
from analysis import fmtp, star

recs, info, med_ss = pickle.load(open("recs2.pkl", "rb"))
OUT = []
def w(x=""): OUT.append(str(x))

# collapsed college for regression stability
def college_grp(c):
    if c == "Medicine & Health Sciences": return "ref"
    if c == "Engineering & IT": return "EngIT"
    if c in ("Dentistry", "Pharmacy", "Nursing", "Sciences"): return "OtherHealth"
    return "NonHealth"   # Humanities, Arts, Other
for r in recs:
    r['col_grp'] = college_grp(r['college'])

CONT = ['gender_male', 'age_rank', 'year_rank', 'chronic_GI',
        'sleep_rank', 'caffeine_rank', 'eating_rank', 'stress_score']
COLDUM = ['EngIT', 'OtherHealth', 'NonHealth']

def build(dv, preds_cont, with_college=True):
    rows = []
    need = list(preds_cont)
    comp = [r for r in recs if all(r.get(p) is not None for p in need) and r.get(dv) is not None]
    names = ['(Intercept)']
    X = []; y = []
    for r in comp:
        xi = [1.0]
        for p in preds_cont:
            xi.append(float(r[p]))
        if with_college:
            for d in COLDUM:
                xi.append(1.0 if r['col_grp'] == d else 0.0)
        X.append(xi); y.append(float(r[dv]))
    names = ['(Intercept)'] + list(preds_cont) + (COLDUM if with_college else [])
    return X, y, names, len(comp)

PRETTY = {'gender_male':'Gender (Male vs Female)','age_rank':'Age group (rank)',
          'year_rank':'Academic year (rank)','chronic_GI':'Chronic GI disease (Yes vs No)',
          'sleep_rank':'Sleep hours (rank)','caffeine_rank':'Caffeine intake (rank)',
          'eating_rank':'Eating habit change (rank)','stress_score':'Stress score (0-36)',
          'EngIT':'College: Engineering & IT','OtherHealth':'College: Other Health',
          'NonHealth':'College: Non-Health','(Intercept)':'(Intercept)'}

# ---------------- MODEL 2: multiple linear regression (GI_severity) ----------
w("="*78); w("PHASE 5 — REGRESSION MODELS"); w("="*78)
w("\nNote on College: the 9 faculty categories were collapsed to 4 groups for")
w("regression stability (ref=Medicine & Health Sciences; Engineering & IT;")
w("Other Health = Dentistry/Pharmacy/Nursing/Sciences; Non-Health = Humanities/Arts/Other).")
w("All models use listwise deletion; analytic n is limited by GHQ stress availability (n=279).")

w("\n" + "="*78)
w("MODEL 2 — Multiple Linear Regression: predictors of GI_severity (0-39)")
w("="*78)
X, y, names, n = build('GI_severity', CONT, with_college=True)
res = S.ols(X, y, names)
w(f"n={res['n']} | R2={res['r2']:.3f} | Adjusted R2={res['adj_r2']:.3f} | "
  f"F({res['df_model']},{res['df_res']})={res['F']:.2f}, p={fmtp(res['Fp'])}")
w(f"{'Predictor':<34}{'B':>9}{'SE':>8}{'Beta':>8}{'t':>8}{'p':>10}   95% CI")
for j, nm in enumerate(names):
    b=res['beta'][j]; se=res['se'][j]; bt=res['std_beta'][j]; t=res['t'][j]; p=res['p'][j]
    ci=res['ci'][j]
    w(f"{PRETTY.get(nm,nm):<34}{b:>9.3f}{se:>8.3f}{bt:>8.3f}{t:>8.2f}{fmtp(p):>10}{star(p)}   "
      f"[{ci[0]:.2f}, {ci[1]:.2f}]")
w("VIF (multicollinearity check):")
for k,v in res.get('__vif__', S.compute_vif(X,names)).items():
    pass
vif = S.compute_vif(X, names)
w("   " + ", ".join(f"{PRETTY.get(k,k).split(':')[0]}={v:.2f}" for k,v in vif.items()))

# ---------------- MODEL 1: binary logistic (GI_presence) ---------------------
w("\n" + "="*78)
w("MODEL 1 — Binary Logistic Regression: predictors of GI_presence (1=any symptom)")
w("="*78)
def run_logit(preds, with_college, label):
    X, y, names, n = build('GI_presence', preds, with_college=with_college)
    ev = int(sum(y)); nonev = int(len(y)-sum(y))
    try:
        r = S.logistic_regression(X, y, names, ridge=1.0)
    except Exception as e:
        w(f"  [{label}] FAILED to converge: {e}"); return
    unstable = any(abs(b)>15 for b in r['beta']) or any(s>50 for s in r['se'])
    w(f"\n[{label}] n={r['n']} (events: Yes={ev}, No={nonev}) | "
      f"Model LR chi2({len(names)-1})={r['lr_chi2']:.2f}, p={fmtp(r['lr_p'])} | "
      f"Nagelkerke R2={r['nagelkerke']:.3f}" + ("  <-- UNSTABLE (separation likely)" if unstable else ""))
    w(f"{'Predictor':<34}{'B':>9}{'OR':>9}{'p':>10}   95% CI(OR)")
    for j, nm in enumerate(names):
        if nm=='(Intercept)':
            w(f"{PRETTY.get(nm,nm):<34}{r['beta'][j]:>9.3f}{'':>9}{fmtp(r['p'][j]):>10}"); continue
        w(f"{PRETTY.get(nm,nm):<34}{r['beta'][j]:>9.3f}{r['OR'][j]:>9.3f}{fmtp(r['p'][j]):>10}{star(r['p'][j])}   "
          f"[{r['ci'][j][0]:.3f}, {r['ci'][j][1]:.3f}]")
w("WARNING: only 22 'No' events in complete-case data -> events-per-variable ~2.")
w("Maximum-likelihood logistic regression DID NOT CONVERGE (quasi-complete separation).")
w("A ridge-penalised logistic regression (L2, lambda=1.0, intercept unpenalised) is reported")
w("instead; coefficients are shrunk toward 0 and these results are EXPLORATORY only.")
run_logit(CONT, True, "Full model, ridge-penalised (per protocol predictors)")
run_logit(['gender_male','chronic_GI','sleep_rank','caffeine_rank','eating_rank','stress_score'],
          False, "Parsimonious model, ridge-penalised")

# ---------------- MODEL 3: ordinal logistic (symptom_increase) ---------------
w("\n" + "="*78)
w("MODEL 3 — Ordinal Logistic Regression (proportional odds): symptom_increase (1-4)")
w("="*78)
# build covariate matrix WITHOUT intercept
comp = [r for r in recs if all(r.get(p) is not None for p in CONT) and r.get('symptom_increase') is not None]
Xc=[]; yo=[]
cov_names = list(CONT) + COLDUM
for r in comp:
    xi=[float(r[p]) for p in CONT] + [1.0 if r['col_grp']==d else 0.0 for d in COLDUM]
    Xc.append(xi); yo.append(int(r['symptom_increase']))
res = S.ordinal_logistic(Xc, yo, cov_names)
w(f"n={res['n']} | categories J={res['J']} | "
  f"Model LR chi2({len(cov_names)})={res['lr_chi2']:.2f}, p={fmtp(res['lr_p'])} | "
  f"Nagelkerke R2={res['nagelkerke']:.3f}")
w("(In the parameterisation logit P(Y<=j)=theta_j - x*beta, a POSITIVE beta => higher predictor")
w(" value increases the odds of being in a HIGHER symptom-increase category. OR=exp(beta).)")
w(f"{'Predictor':<34}{'B':>9}{'OR':>9}{'p':>10}   95% CI(OR)")
for j, nm in enumerate(cov_names):
    w(f"{PRETTY.get(nm,nm):<34}{res['beta'][j]:>9.3f}{res['OR'][j]:>9.3f}{fmtp(res['p'][j]):>10}{star(res['p'][j])}   "
      f"[{res['ci'][j][0]:.3f}, {res['ci'][j][1]:.3f}]")
w(f"Thresholds (theta): " + ", ".join(f"{t:.3f}" for t in res['thresholds']))

txt = "\n".join(OUT)
open("results_p5.txt","w").write(txt)
print(txt)
