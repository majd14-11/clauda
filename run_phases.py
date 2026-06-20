# -*- coding: utf-8 -*-
"""Run Phases 2-5 and emit a structured results file (results.txt)."""
import pickle, math
import statlib as S
from collections import Counter, OrderedDict
from analysis import (SYM_LABELS, SYM_AR, fmtp, star)

recs, info = pickle.load(open("recs.pkl", "rb"))
N = len(recs)
OUT = []
def w(line=""):
    OUT.append(str(line))

def col(key, cond=lambda r: True):
    return [r[key] for r in recs if r.get(key) is not None and cond(r)]

def descr(vals):
    return dict(n=len(vals), mean=S.mean(vals), sd=S.sd(vals), median=S.median(vals),
               q1=S.percentile(vals, 25), q3=S.percentile(vals, 75),
               mn=min(vals), mx=max(vals),
               skew=S.skewness(vals), kurt=S.kurtosis_excess(vals))

# =====================================================================
w("="*78); w("PHASE 2 — NORMALITY CHECK (continuous variables)"); w("="*78)
for key, label, rng in [("GI_severity", "GI symptom severity score", "0-39"),
                        ("stress_score", "GHQ psychological stress score", "0-36")]:
    vals = col(key)
    d = descr(vals)
    sw_W, sw_p = S.shapiro_wilk(vals)
    k2, dp = S.dagostino_pearson(vals)
    w(f"\n{label} (theoretical range {rng}), n={d['n']}")
    w(f"  Mean={d['mean']:.2f}  SD={d['sd']:.2f}  Median={d['median']:.1f}  "
      f"IQR=[{d['q1']:.1f}, {d['q3']:.1f}]  Range=[{d['mn']:.0f}, {d['mx']:.0f}]")
    w(f"  Skewness={d['skew']:.3f}  Excess kurtosis={d['kurt']:.3f}")
    w(f"  Shapiro-Wilk:        W={sw_W:.4f}, p={fmtp(sw_p)}")
    w(f"  D'Agostino-Pearson:  K2={k2:.3f}, p={fmtp(dp)}")
    decision = "NON-NORMAL -> use NON-PARAMETRIC tests" if (sw_p < 0.05) else "Normal -> parametric"
    w(f"  DECISION: {decision}")

# =====================================================================
w("\n" + "="*78); w("PHASE 3 — DESCRIPTIVE STATISTICS"); w("="*78)

def freq_table(key, labels=None, order=None):
    c = Counter(r[key] for r in recs if r.get(key) is not None)
    miss = sum(1 for r in recs if r.get(key) is None)
    tot = sum(c.values())
    keys = order if order else sorted(c.keys())
    rows = []
    for k in keys:
        v = c.get(k, 0)
        lab = labels.get(k, k) if labels else k
        rows.append((lab, v, 100.0*v/tot if tot else 0))
    return rows, tot, miss

w("\n--- Table 3.1: Demographic characteristics (n=%d) ---" % N)
age_lab = {1: "<20", 2: "20-24", 3: "25-29", 4: "30+"}
for title, key, labels, order in [
    ("Age group", "age_rank", age_lab, [1,2,3,4]),
    ("Gender", "gender_male", {0:"Female",1:"Male"}, [0,1]),
    ("Academic year", "year_rank", {1:"1st",2:"2nd",3:"3rd",4:"4th",5:"5th+"}, [1,2,3,4,5]),
    ("Chronic GI disease", "chronic_GI", {0:"No",1:"Yes"}, [0,1]),
]:
    rows, tot, miss = freq_table(key, labels, order)
    w(f"  {title} (valid n={tot}, missing={miss}):")
    for lab, v, pct in rows:
        w(f"      {lab:<10} {v:4d} ({pct:4.1f}%)")
# college
c = Counter(r['college'] for r in recs)
w(f"  College (valid n={N}):")
for k, v in c.most_common():
    w(f"      {k:<32} {v:4d} ({100.0*v/N:4.1f}%)")

w("\n--- Table 3.2: Severity of each GI symptom during exams (n=%d) ---" % N)
w("  Symptom                     None        Mild        Moderate    Severe")
for i, lab in enumerate(SYM_LABELS):
    codes = [r['sym_codes'][i] for r in recs if r['sym_codes'][i] is not None]
    tot = len(codes)
    cc = Counter(codes)
    def cell(x):
        v = cc.get(x, 0); return f"{v}({100.0*v/tot:.0f}%)"
    w(f"  {SYM_AR[i]:<14}{lab:<14} {cell(0):<11} {cell(1):<11} {cell(2):<11} {cell(3):<11}")

# GI presence + severity
pres = Counter(r['GI_presence'] for r in recs if r['GI_presence'] is not None)
tot = sum(pres.values())
w(f"\n  GI symptom PRESENCE (Outcome 1): "
  f"No={pres[0]} ({100.0*pres[0]/tot:.1f}%), Yes={pres[1]} ({100.0*pres[1]/tot:.1f}%)")
sev = col("GI_severity"); d = descr(sev)
w(f"  GI SEVERITY score (Outcome 2): Mean={d['mean']:.2f} +/- {d['sd']:.2f}, "
  f"Median={d['median']:.1f} (IQR {d['q1']:.1f}-{d['q3']:.1f}), Range {d['mn']:.0f}-{d['mx']:.0f}")

w("\n--- Table 3.3: Symptom characteristics ---")
for title, key, labels, order in [
    ("Symptom frequency (last week)", "freq_rank", {1:"Never",2:"1-2 times",3:"3-4 times",4:"5+ times"}, [1,2,3,4]),
    ("Impact on daily activity/study", "impact_rank", {1:"None",2:"Mild",3:"Moderate",4:"Large"}, [1,2,3,4]),
    ("Healthcare visit", "visit", {0:"No",1:"Yes"}, [0,1]),
    ("Medication / home remedy use", "med", {0:"No",1:"Yes"}, [0,1]),
]:
    rows, tot, miss = freq_table(key, labels, order)
    w(f"  {title} (valid n={tot}, missing={miss}):")
    for lab, v, pct in rows:
        w(f"      {lab:<12} {v:4d} ({pct:4.1f}%)")

w("\n--- Table 3.4: Lifestyle factors & self-reported comparison ---")
for title, key, labels, order in [
    ("Symptom increase vs regular days (Outcome 3)", "symptom_increase",
     {1:"Don't know",2:"No difference",3:"Sometimes",4:"Yes, clearly"}, [1,2,3,4]),
    ("Sleep hours/night", "sleep_rank", {1:"<5h",2:"5-6h",3:"6-7h",4:">7h"}, [1,2,3,4]),
    ("Daily caffeine", "caffeine_rank", {1:"0",2:"1-2",3:"3-4",4:">4"}, [1,2,3,4]),
    ("Eating habits change", "eating_rank", {1:"Better",2:"No change",3:"Worse"}, [1,2,3]),
]:
    rows, tot, miss = freq_table(key, labels, order)
    w(f"  {title} (valid n={tot}, missing={miss}):")
    for lab, v, pct in rows:
        w(f"      {lab:<14} {v:4d} ({pct:4.1f}%)")

# Stress
ss = col("stress_score"); d = descr(ss)
med_ss = d['median']
w(f"\n--- Table 3.5: Psychological stress (GHQ-12 Likert, 0-36) ---")
w(f"  Total stress score: n={d['n']}, Mean={d['mean']:.2f} +/- {d['sd']:.2f}, "
  f"Median={med_ss:.1f} (IQR {d['q1']:.1f}-{d['q3']:.1f}), Range {d['mn']:.0f}-{d['mx']:.0f}")
# stress level binary (median split): >median = high
for r in recs:
    if r['stress_score'] is not None:
        r['stress_level'] = 1 if r['stress_score'] > med_ss else 0
    else:
        r['stress_level'] = None
sl = Counter(r['stress_level'] for r in recs if r['stress_level'] is not None)
slt = sum(sl.values())
w(f"  Stress level (median split at {med_ss:.1f}): Low={sl[0]} ({100.0*sl[0]/slt:.1f}%), "
  f"High={sl[1]} ({100.0*sl[1]/slt:.1f}%)")

# Save updated recs (with stress_level) for phase 4/5
pickle.dump((recs, info, med_ss), open("recs2.pkl", "wb"))

open("results.txt", "w").write("\n".join(OUT))
print("\n".join(OUT))
print("\n[written results.txt]")
