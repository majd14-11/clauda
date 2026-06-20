# -*- coding: utf-8 -*-
"""Export the cleaned, recoded analytic dataset to cleaned_data.csv (N=370)."""
import pickle, csv
from analysis import SYM_LABELS

recs, info, med_ss = pickle.load(open("recs2.pkl", "rb"))

def colgrp(c):
    if c == "Medicine & Health Sciences": return "Medicine&Health"
    if c == "Engineering & IT": return "Engineering&IT"
    if c in ("Dentistry","Pharmacy","Nursing","Sciences"): return "OtherHealth"
    return "NonHealth"

fields = (["id","age_rank","gender_male","college_clean","college_grp","year_rank","chronic_GI"]
          + [f"S{i+1}_{lab}" for i,lab in enumerate(SYM_LABELS)]
          + ["GI_presence","GI_severity","freq_rank","impact_rank","visit","med",
             "symptom_increase","sleep_rank","caffeine_rank","eating_rank",
             "ghq_n_items","stress_score","stress_level"])

with open("cleaned_data.csv","w",newline="",encoding="utf-8-sig") as f:
    wr = csv.writer(f)
    wr.writerow(fields)
    for i, r in enumerate(recs, 1):
        row = [i, r['age_rank'], r['gender_male'], r['college'], colgrp(r['college']),
               r['year_rank'], r['chronic_GI']]
        row += [r['sym_codes'][j] for j in range(len(SYM_LABELS))]
        row += [r['GI_presence'], r['GI_severity'], r['freq_rank'], r['impact_rank'],
                r['visit'], r['med'], r['symptom_increase'], r['sleep_rank'],
                r['caffeine_rank'], r['eating_rank'], r['ghq_n'],
                round(r['stress_score'],2) if r['stress_score'] is not None else "",
                r['stress_level'] if r['stress_level'] is not None else ""]
        row = ["" if v is None else v for v in row]
        wr.writerow(row)
print("Wrote cleaned_data.csv with", len(recs), "rows and", len(fields), "columns")
print("(median stress used for stress_level split =", med_ss, ")")
